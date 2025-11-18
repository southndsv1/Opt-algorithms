"""
Optimization Algorithms Package
Contains state-of-the-art constrained optimization algorithms
"""

from .sequential_quadratic_programming import SQP
from .augmented_lagrangian import AugmentedLagrangian
from .penalty_method import PenaltyMethod
from .interior_point import InteriorPoint
from .trust_region_constrained import TrustRegionConstrained
from .bayesian_optimization import BayesianOpt
from .particle_swarm_constrained import ParticleSwarmConstrained
from .differential_evolution_constrained import DifferentialEvolutionConstrained
from .genetic_algorithm_constrained import GeneticAlgorithmConstrained
from .cobyla import COBYLA

__all__ = [
    'SQP',
    'AugmentedLagrangian',
    'PenaltyMethod',
    'InteriorPoint',
    'TrustRegionConstrained',
    'BayesianOpt',
    'ParticleSwarmConstrained',
    'DifferentialEvolutionConstrained',
    'GeneticAlgorithmConstrained',
    'COBYLA'
]
