"""
Base class for optimization algorithms
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, List, Callable, Optional, Tuple


class OptimizationResult:
    """Container for optimization results"""
    def __init__(self, x: np.ndarray, fun: float, success: bool, message: str,
                 nit: int, nfev: int, history: Optional[List[float]] = None):
        self.x = x  # Optimal solution
        self.fun = fun  # Objective function value at optimal solution
        self.success = success  # Whether optimization succeeded
        self.message = message  # Status message
        self.nit = nit  # Number of iterations
        self.nfev = nfev  # Number of function evaluations
        self.history = history if history is not None else []  # Convergence history


class BaseOptimizer(ABC):
    """Base class for all optimization algorithms"""

    def __init__(self, name: str):
        self.name = name
        self.history = []

    @abstractmethod
    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize the objective function

        Args:
            objective: Objective function to minimize
            x0: Initial guess
            bounds: List of (min, max) tuples for each variable
            constraints: List of constraint dictionaries
                        {'type': 'eq' or 'ineq', 'fun': constraint_function}
                        where constraint_function(x) >= 0 for 'ineq'
                        and constraint_function(x) == 0 for 'eq'
            max_iter: Maximum number of iterations
            tol: Tolerance for convergence

        Returns:
            OptimizationResult object
        """
        pass

    def _evaluate_constraints(self, x: np.ndarray, constraints: List[Dict]) -> Tuple[float, bool]:
        """
        Evaluate constraint violations

        Returns:
            (total_violation, is_feasible)
        """
        if not constraints:
            return 0.0, True

        total_violation = 0.0
        is_feasible = True

        for constraint in constraints:
            c_val = constraint['fun'](x)
            if constraint['type'] == 'ineq':
                # Inequality: c(x) >= 0
                if c_val < 0:
                    total_violation += abs(c_val)
                    is_feasible = False
            else:  # 'eq'
                # Equality: c(x) == 0
                if abs(c_val) > 1e-6:
                    total_violation += abs(c_val)
                    is_feasible = False

        return total_violation, is_feasible

    def _clip_to_bounds(self, x: np.ndarray, bounds: List[Tuple[float, float]]) -> np.ndarray:
        """Clip solution to bounds"""
        x_clipped = x.copy()
        for i, (lb, ub) in enumerate(bounds):
            x_clipped[i] = np.clip(x_clipped[i], lb, ub)
        return x_clipped
