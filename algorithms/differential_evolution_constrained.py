"""
Differential Evolution for Constrained Problems
Evolutionary algorithm with constraint handling
"""

import numpy as np
from scipy.optimize import differential_evolution
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult


class DifferentialEvolutionConstrained(BaseOptimizer):
    """Differential Evolution with constraint handling"""

    def __init__(self):
        super().__init__("Differential Evolution")

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using Differential Evolution with constraints
        """
        self.history = []

        # Wrap objective to include penalty for constraints
        def penalized_objective(x):
            f = objective(x)
            self.history.append(f)

            if constraints:
                violation, _ = self._evaluate_constraints(x, constraints)
                return f + 1e6 * violation
            return f

        try:
            # Convert constraints to scipy format for DE
            scipy_constraints = []
            if constraints:
                for c in constraints:
                    if c['type'] == 'ineq':
                        # scipy wants g(x) >= 0 format
                        scipy_constraints.append({
                            'type': 'ineq',
                            'fun': c['fun']
                        })
                    else:
                        scipy_constraints.append({
                            'type': 'eq',
                            'fun': c['fun']
                        })

            result = differential_evolution(
                penalized_objective,
                bounds,
                maxiter=max_iter,
                tol=tol,
                seed=42,
                polish=True,
                init='latinhypercube',
                atol=0,
                updating='deferred',
                workers=1
            )

            return OptimizationResult(
                x=result.x,
                fun=objective(result.x),
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
                message=f"Differential Evolution failed: {str(e)}",
                nit=0,
                nfev=len(self.history),
                history=self.history
            )
