"""
Genetic Algorithm for Constrained Problems
Uses tournament selection and constraint handling
"""

import numpy as np
from typing import Callable, List, Tuple, Optional, Dict
from .base import BaseOptimizer, OptimizationResult


class GeneticAlgorithmConstrained(BaseOptimizer):
    """Genetic Algorithm with constraint handling"""

    def __init__(self, population_size=50):
        super().__init__("Genetic Algorithm")
        self.population_size = population_size

    def optimize(self, objective: Callable, x0: np.ndarray, bounds: List[Tuple[float, float]],
                 constraints: Optional[List[Dict]] = None,
                 max_iter: int = 1000, tol: float = 1e-6) -> OptimizationResult:
        """
        Optimize using Genetic Algorithm with constraints
        """
        self.history = []
        dim = len(x0)

        # GA parameters
        mutation_rate = 0.1
        crossover_rate = 0.8
        tournament_size = 3

        # Initialize population
        population = np.zeros((self.population_size, dim))
        for i in range(self.population_size):
            for j in range(dim):
                population[i, j] = np.random.uniform(bounds[j][0], bounds[j][1])

        # Set first individual to initial guess
        population[0] = x0

        # Fitness function with penalty
        def fitness(x):
            f = objective(x)
            if constraints:
                violation, _ = self._evaluate_constraints(x, constraints)
                return f + 1e6 * violation
            return f

        # Evolution loop
        best_fitness = float('inf')
        best_individual = None

        for generation in range(max_iter // self.population_size):
            # Evaluate fitness
            fitness_values = np.array([fitness(ind) for ind in population])

            # Track best
            gen_best_idx = np.argmin(fitness_values)
            if fitness_values[gen_best_idx] < best_fitness:
                best_fitness = fitness_values[gen_best_idx]
                best_individual = population[gen_best_idx].copy()

            self.history.append(objective(best_individual))

            # Selection (Tournament)
            def tournament_selection():
                tournament_indices = np.random.choice(self.population_size, tournament_size, replace=False)
                tournament_fitness = fitness_values[tournament_indices]
                winner_idx = tournament_indices[np.argmin(tournament_fitness)]
                return population[winner_idx].copy()

            # Create new population
            new_population = []

            # Elitism: keep best individual
            new_population.append(best_individual.copy())

            while len(new_population) < self.population_size:
                # Selection
                parent1 = tournament_selection()
                parent2 = tournament_selection()

                # Crossover
                if np.random.rand() < crossover_rate:
                    # Simulated Binary Crossover (SBX)
                    alpha = np.random.rand(dim)
                    child1 = alpha * parent1 + (1 - alpha) * parent2
                    child2 = (1 - alpha) * parent1 + alpha * parent2
                else:
                    child1 = parent1.copy()
                    child2 = parent2.copy()

                # Mutation
                if np.random.rand() < mutation_rate:
                    for i in range(dim):
                        if np.random.rand() < 1.0 / dim:
                            child1[i] = np.random.uniform(bounds[i][0], bounds[i][1])

                if np.random.rand() < mutation_rate:
                    for i in range(dim):
                        if np.random.rand() < 1.0 / dim:
                            child2[i] = np.random.uniform(bounds[i][0], bounds[i][1])

                # Apply bounds
                child1 = self._clip_to_bounds(child1, bounds)
                child2 = self._clip_to_bounds(child2, bounds)

                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)

            population = np.array(new_population)

            # Check convergence
            if len(self.history) > 10:
                recent_change = abs(self.history[-1] - self.history[-10])
                if recent_change < tol:
                    break

        return OptimizationResult(
            x=best_individual,
            fun=objective(best_individual),
            success=True,
            message="Genetic Algorithm optimization completed",
            nit=len(self.history),
            nfev=len(self.history) * self.population_size,
            history=self.history
        )
