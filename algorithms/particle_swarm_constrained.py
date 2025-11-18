"""
Particle Swarm Optimization for Constrained Problems
Uses penalty-based constraint handling
"""

import numpy as np
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult


class ParticleSwarmConstrained(BaseOptimizer):
    """Particle Swarm Optimization with constraint handling"""

    def __init__(self, n_particles=30):
        super().__init__("Particle Swarm Optimization")
        self.n_particles = n_particles

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using Particle Swarm Optimization with constraints
        """
        self.history = []
        dim = len(x0)

        # PSO parameters
        w = 0.7298  # Inertia weight
        c1 = 1.49618  # Cognitive parameter
        c2 = 1.49618  # Social parameter

        # Initialize particles
        particles = np.zeros((self.n_particles, dim))
        velocities = np.zeros((self.n_particles, dim))

        for i in range(self.n_particles):
            for j in range(dim):
                particles[i, j] = np.random.uniform(bounds[j][0], bounds[j][1])
                velocities[i, j] = np.random.uniform(
                    -(bounds[j][1] - bounds[j][0]) * 0.1,
                    (bounds[j][1] - bounds[j][0]) * 0.1
                )

        # Set first particle to initial guess
        particles[0] = x0

        # Evaluate fitness with penalty for constraint violations
        def penalized_objective(x):
            f = objective(x)
            if constraints:
                violation, _ = self._evaluate_constraints(x, constraints)
                return f + 1e6 * violation
            return f

        # Initialize personal best and global best
        personal_best_positions = particles.copy()
        personal_best_scores = np.array([penalized_objective(p) for p in particles])

        global_best_idx = np.argmin(personal_best_scores)
        global_best_position = personal_best_positions[global_best_idx].copy()
        global_best_score = personal_best_scores[global_best_idx]

        self.history.append(objective(global_best_position))

        # PSO iterations
        for iteration in range(max_iter):
            for i in range(self.n_particles):
                # Update velocity
                r1, r2 = np.random.rand(2)
                velocities[i] = (w * velocities[i] +
                                 c1 * r1 * (personal_best_positions[i] - particles[i]) +
                                 c2 * r2 * (global_best_position - particles[i]))

                # Update position
                particles[i] = particles[i] + velocities[i]

                # Apply bounds
                particles[i] = self._clip_to_bounds(particles[i], bounds)

                # Evaluate fitness
                score = penalized_objective(particles[i])

                # Update personal best
                if score < personal_best_scores[i]:
                    personal_best_scores[i] = score
                    personal_best_positions[i] = particles[i].copy()

                    # Update global best
                    if score < global_best_score:
                        global_best_score = score
                        global_best_position = particles[i].copy()

            # Record true objective value
            true_obj = objective(global_best_position)
            self.history.append(true_obj)

            # Check convergence
            if iteration > 10:
                recent_change = abs(self.history[-1] - self.history[-10])
                if recent_change < tol:
                    break

        return OptimizationResult(
            x=global_best_position,
            fun=objective(global_best_position),
            success=True,
            message="PSO optimization completed",
            nit=iteration + 1,
            nfev=len(self.history) * self.n_particles,
            history=self.history
        )
