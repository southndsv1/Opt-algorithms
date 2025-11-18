"""
Augmented Lagrangian Method
Handles constraints through Lagrange multipliers and penalty terms
"""

import numpy as np
from scipy.optimize import minimize
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult


class AugmentedLagrangian(BaseOptimizer):
    """Augmented Lagrangian Method optimizer"""

    def __init__(self):
        super().__init__("Augmented Lagrangian")

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using Augmented Lagrangian method
        """
        self.history = []

        # Initialize Lagrange multipliers
        n_constraints = len(constraints) if constraints else 0
        lambdas = np.zeros(n_constraints)
        mu = 10.0  # Penalty parameter

        x = x0.copy()
        outer_iter = 0
        max_outer_iter = 50

        while outer_iter < max_outer_iter:
            # Define augmented Lagrangian
            def augmented_lagrangian(x_var):
                f = objective(x_var)
                self.history.append(f)

                if not constraints:
                    return f

                # Add Lagrangian and penalty terms
                aug_term = 0.0
                for i, c in enumerate(constraints):
                    c_val = c['fun'](x_var)
                    if c['type'] == 'ineq':
                        # For inequality c(x) >= 0
                        aug_term += lambdas[i] * min(0, c_val) + (mu / 2) * min(0, c_val) ** 2
                    else:  # 'eq'
                        # For equality c(x) == 0
                        aug_term += lambdas[i] * c_val + (mu / 2) * c_val ** 2

                return f + aug_term

            # Solve unconstrained subproblem
            result = minimize(
                augmented_lagrangian,
                x,
                method='L-BFGS-B',
                bounds=bounds,
                options={'maxiter': max_iter // max_outer_iter}
            )

            x = result.x

            # Check convergence
            violation, feasible = self._evaluate_constraints(x, constraints)
            if feasible and violation < tol:
                return OptimizationResult(
                    x=x,
                    fun=objective(x),
                    success=True,
                    message="Optimization converged successfully",
                    nit=outer_iter,
                    nfev=len(self.history),
                    history=self.history
                )

            # Update Lagrange multipliers
            if constraints:
                for i, c in enumerate(constraints):
                    c_val = c['fun'](x)
                    if c['type'] == 'ineq':
                        lambdas[i] = max(0, lambdas[i] + mu * min(0, c_val))
                    else:
                        lambdas[i] = lambdas[i] + mu * c_val

            # Increase penalty parameter
            mu *= 1.5
            outer_iter += 1

        return OptimizationResult(
            x=x,
            fun=objective(x),
            success=outer_iter < max_outer_iter,
            message="Maximum iterations reached",
            nit=outer_iter,
            nfev=len(self.history),
            history=self.history
        )
