"""
Bayesian Optimization
Uses Gaussian Processes for black-box optimization
"""

import numpy as np
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult
from scipy.stats import norm
from scipy.optimize import minimize


class BayesianOpt(BaseOptimizer):
    """Bayesian Optimization using Gaussian Processes"""

    def __init__(self):
        super().__init__("Bayesian Optimization")

    def _rbf_kernel(self, X1, X2, length_scale=1.0, sigma_f=1.0):
        """Radial Basis Function kernel"""
        sqdist = np.sum(X1 ** 2, 1).reshape(-1, 1) + np.sum(X2 ** 2, 1) - 2 * np.dot(X1, X2.T)
        return sigma_f ** 2 * np.exp(-0.5 / length_scale ** 2 * sqdist)

    def _acquisition_ei(self, X, X_sample, Y_sample, gp_params, xi=0.01):
        """Expected Improvement acquisition function"""
        mu, sigma = self._gp_predict(X, X_sample, Y_sample, gp_params)
        mu_sample_opt = np.min(Y_sample)

        with np.errstate(divide='warn'):
            imp = mu_sample_opt - mu - xi
            Z = imp / sigma
            ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
            ei[sigma == 0.0] = 0.0

        return -ei  # Negative because we minimize

    def _gp_predict(self, X, X_sample, Y_sample, gp_params):
        """Gaussian Process prediction"""
        length_scale, sigma_f, noise = gp_params

        K = self._rbf_kernel(X_sample, X_sample, length_scale, sigma_f) + noise ** 2 * np.eye(len(X_sample))
        K_s = self._rbf_kernel(X_sample, X, length_scale, sigma_f)
        K_ss = self._rbf_kernel(X, X, length_scale, sigma_f)

        K_inv = np.linalg.inv(K)

        mu = K_s.T.dot(K_inv).dot(Y_sample)
        sigma = np.sqrt(np.diag(K_ss - K_s.T.dot(K_inv).dot(K_s)))

        return mu, sigma

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using Bayesian Optimization
        """
        self.history = []
        dim = len(x0)

        # Initial samples (including x0)
        n_init = min(10, max_iter // 10)
        X_sample = [x0]
        Y_sample = []

        # Add random initial points
        for _ in range(n_init - 1):
            x_rand = np.array([np.random.uniform(b[0], b[1]) for b in bounds])
            X_sample.append(x_rand)

        # Evaluate initial points
        for x in X_sample:
            # Check constraints
            if constraints:
                violation, feasible = self._evaluate_constraints(x, constraints)
                if not feasible:
                    y = objective(x) + 1e6 * violation  # Penalize infeasible points
                else:
                    y = objective(x)
            else:
                y = objective(x)

            Y_sample.append(y)
            self.history.append(objective(x))

        X_sample = np.array(X_sample)
        Y_sample = np.array(Y_sample).reshape(-1, 1)

        # GP hyperparameters
        gp_params = (1.0, 1.0, 1e-5)  # length_scale, sigma_f, noise

        # Bayesian optimization loop
        for iteration in range(max_iter - n_init):
            # Find next point by optimizing acquisition function
            def acq_wrapper(x):
                return self._acquisition_ei(x.reshape(1, -1), X_sample, Y_sample, gp_params)

            # Try multiple random starts for acquisition optimization
            best_acq = float('inf')
            best_x = None

            for _ in range(10):
                x_start = np.array([np.random.uniform(b[0], b[1]) for b in bounds])
                res = minimize(acq_wrapper, x_start, bounds=bounds, method='L-BFGS-B')
                if res.fun < best_acq:
                    best_acq = res.fun
                    best_x = res.x

            # Evaluate objective at new point
            x_next = best_x
            if constraints:
                violation, feasible = self._evaluate_constraints(x_next, constraints)
                if not feasible:
                    y_next = objective(x_next) + 1e6 * violation
                else:
                    y_next = objective(x_next)
            else:
                y_next = objective(x_next)

            self.history.append(objective(x_next))

            # Update sample sets
            X_sample = np.vstack([X_sample, x_next])
            Y_sample = np.vstack([Y_sample, y_next])

            # Check convergence
            if len(self.history) > 5:
                recent_improvement = abs(min(self.history[-5:]) - min(self.history[-6:-1]))
                if recent_improvement < tol:
                    break

        # Return best found solution
        best_idx = np.argmin(Y_sample)
        best_x = X_sample[best_idx]
        best_y = objective(best_x)

        return OptimizationResult(
            x=best_x,
            fun=best_y,
            success=True,
            message="Bayesian optimization completed",
            nit=len(self.history),
            nfev=len(self.history),
            history=self.history
        )
