"""Algorithms module - all swarm intelligence algorithms."""

from .pso import PSO
from .aco import ACO
from .ga import GA
from .de import DE

__all__ = ["PSO", "ACO", "GA", "DE"]

ALGORITHM_REGISTRY = {
    "pso": PSO,
    "aco": ACO,
    "ga": GA,
    "de": DE,
}
