"""
Penalty Method
Converts constrained problem to unconstrained by adding penalty terms
"""

import numpy as np
from scipy.optimize import minimize
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult


class PenaltyMethod(BaseOptimizer):
    """Penalty Method optimizer"""

    def __init__(self):
        super().__init__("Penalty Method")

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using Penalty Method
        """
        self.history = []

        mu = 1.0  # Initial penalty parameter
        mu_max = 1e6
        mu_multiplier = 10.0

        x = x0.copy()
        outer_iter = 0
        max_outer_iter = 20

        while outer_iter < max_outer_iter and mu < mu_max:
            # Define penalty function
            def penalty_function(x_var):
                f = objective(x_var)
                self.history.append(f)

                if not constraints:
                    return f

                # Add penalty terms
                penalty = 0.0
                for c in constraints:
                    c_val = c['fun'](x_var)
                    if c['type'] == 'ineq':
                        # For inequality c(x) >= 0, penalize violations
                        penalty += mu * max(0, -c_val) ** 2
                    else:  # 'eq'
                        # For equality c(x) == 0
                        penalty += mu * c_val ** 2

                return f + penalty

            # Solve unconstrained subproblem
            result = minimize(
                penalty_function,
                x,
                method='L-BFGS-B',
                bounds=bounds,
                options={'maxiter': max_iter // max_outer_iter}
            )

            x = result.x

            # Check convergence
            violation, feasible = self._evaluate_constraints(x, constraints)
            if violation < tol:
                return OptimizationResult(
                    x=x,
                    fun=objective(x),
                    success=True,
                    message="Optimization converged successfully",
                    nit=outer_iter,
                    nfev=len(self.history),
                    history=self.history
                )

            # Increase penalty parameter
            mu *= mu_multiplier
            outer_iter += 1

        return OptimizationResult(
            x=x,
            fun=objective(x),
            success=violation < tol if constraints else True,
            message="Maximum iterations or penalty parameter reached",
            nit=outer_iter,
            nfev=len(self.history),
            history=self.history
        )
