"""
Interior Point Method
Uses barrier functions to handle inequality constraints
"""

import numpy as np
from scipy.optimize import minimize
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult


class InteriorPoint(BaseOptimizer):
    """Interior Point Method optimizer"""

    def __init__(self):
        super().__init__("Interior Point")

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using Interior Point method with logarithmic barrier
        """
        self.history = []

        def objective_wrapper(x):
            val = objective(x)
            self.history.append(val)
            return val

        # Convert constraints to scipy format
        scipy_constraints = []
        if constraints:
            for c in constraints:
                scipy_constraints.append({
                    'type': c['type'],
                    'fun': c['fun']
                })

        try:
            # Use trust-constr which is an interior point method
            result = minimize(
                objective_wrapper,
                x0,
                method='trust-constr',
                bounds=bounds,
                constraints=scipy_constraints if scipy_constraints else (),
                options={'maxiter': max_iter, 'gtol': tol}
            )

            return OptimizationResult(
                x=result.x,
                fun=result.fun,
                success=result.success,
                message=result.message,
                nit=result.nit,
                nfev=result.nfev,
                history=self.history
            )
        except Exception as e:
            return OptimizationResult(
                x=x0,
                fun=objective(x0),
                success=False,
                message=f"Interior Point failed: {str(e)}",
                nit=0,
                nfev=len(self.history),
                history=self.history
            )
