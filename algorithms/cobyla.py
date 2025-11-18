"""
COBYLA - Constrained Optimization BY Linear Approximation
Derivative-free method for constrained optimization
"""

import numpy as np
from scipy.optimize import minimize
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult


class COBYLA(BaseOptimizer):
    """COBYLA optimizer - derivative-free constrained optimization"""

    def __init__(self):
        super().__init__("COBYLA")

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using COBYLA method
        """
        self.history = []

        def objective_wrapper(x):
            val = objective(x)
            self.history.append(val)
            return val

        # Convert bounds to constraints for COBYLA
        bound_constraints = []
        for i, (lb, ub) in enumerate(bounds):
            # Lower bound: x[i] - lb >= 0
            bound_constraints.append({
                'type': 'ineq',
                'fun': lambda x, idx=i, lower=lb: x[idx] - lower
            })
            # Upper bound: ub - x[i] >= 0
            bound_constraints.append({
                'type': 'ineq',
                'fun': lambda x, idx=i, upper=ub: upper - x[idx]
            })

        # Combine with user constraints
        all_constraints = bound_constraints
        if constraints:
            all_constraints.extend(constraints)

        try:
            result = minimize(
                objective_wrapper,
                x0,
                method='COBYLA',
                constraints=all_constraints,
                options={'maxiter': max_iter, 'rhobeg': 1.0, 'tol': tol}
            )

            return OptimizationResult(
                x=result.x,
                fun=result.fun,
                success=result.success,
                message=result.message if hasattr(result, 'message') else "Optimization completed",
                nit=result.nfev,  # COBYLA doesn't report nit separately
                nfev=result.nfev,
                history=self.history
            )
        except Exception as e:
            return OptimizationResult(
                x=x0,
                fun=objective(x0),
                success=False,
                message=f"COBYLA failed: {str(e)}",
                nit=0,
                nfev=len(self.history),
                history=self.history
            )
