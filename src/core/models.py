"""
Core data structures and base classes for SwarmOracle.
"""

import time
import json
import math
import random
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Callable, Optional, Tuple


@dataclass
class Particle:
    """Represents a single particle/individual in the swarm."""
    position: List[float]
    velocity: List[float] = field(default_factory=list)
    fitness: float = float('inf')
    best_position: List[float] = field(default_factory=list)
    best_fitness: float = float('inf')
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.velocity:
            self.velocity = [0.0] * len(self.position)
        if not self.best_position:
            self.best_position = self.position.copy()


@dataclass
class OptimizationResult:
    """Stores the complete result of an optimization run."""
    best_position: List[float] = field(default_factory=list)
    best_fitness: float = float('inf')
    convergence_history: List[float] = field(default_factory=list)
    iteration_count: int = 0
    elapsed_time: float = 0.0
    algorithm_name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    population_diversity: List[float] = field(default_factory=list)
    all_particles: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization."""
        return {
            "algorithm": self.algorithm_name,
            "best_position": self.best_position,
            "best_fitness": self.best_fitness,
            "iterations": self.iteration_count,
            "elapsed_time": round(self.elapsed_time, 4),
            "convergence_history": self.convergence_history,
            "population_diversity": self.population_diversity,
            "parameters": self.parameters,
            "top_particles": self.all_particles[:10],
        }

    def summary(self) -> str:
        """Generate a human-readable summary."""
        lines = [
            f"Algorithm: {self.algorithm_name}",
            f"Best Fitness: {self.best_fitness:.6f}",
            f"Best Position: [{', '.join(f'{x:.4f}' for x in self.best_position)}]",
            f"Iterations: {self.iteration_count}",
            f"Elapsed Time: {self.elapsed_time:.4f}s",
        ]
        if self.convergence_history:
            lines.append(
                f"Convergence Range: {self.convergence_history[-1]:.6f} -> {self.convergence_history[0]:.6f}"
            )
        return "\n".join(lines)


class BaseOptimizer:
    """Abstract base class for all swarm intelligence optimizers."""

    def __init__(
        self,
        objective_func: Callable[[List[float]], float],
        dim: int,
        bounds: List[Tuple[float, float]],
        maximize: bool = False,
        seed: Optional[int] = None,
    ):
        self.objective_func = objective_func
        self.dim = dim
        self.bounds = bounds
        self.maximize = maximize
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self._particles: List[Particle] = []
        self._result = OptimizationResult()
        self._iteration = 0

    def _evaluate(self, position: List[float]) -> float:
        """Evaluate fitness with optional maximization support."""
        val = self.objective_func(position)
        return -val if self.maximize else val

    def _clip_position(self, position: List[float]) -> List[float]:
        """Clip position to stay within bounds."""
        return [
            max(self.bounds[i][0], min(self.bounds[i][1], position[i]))
            for i in range(self.dim)
        ]

    def _random_position(self) -> List[float]:
        """Generate a random position within bounds."""
        return [
            random.uniform(self.bounds[i][0], self.bounds[i][1])
            for i in range(self.dim)
        ]

    def _init_particles(self, pop_size: int) -> List[Particle]:
        """Initialize particle population."""
        particles = []
        for _ in range(pop_size):
            pos = self._random_position()
            p = Particle(position=pos)
            p.fitness = self._evaluate(pos)
            p.best_fitness = p.fitness
            particles.append(p)
        return particles

    def _calculate_diversity(self) -> float:
        """Calculate population diversity (average distance to centroid)."""
        if not self._particles:
            return 0.0
        n = len(self._particles)
        centroid = [
            sum(p.position[i] for p in self._particles) / n
            for i in range(self.dim)
        ]
        total_dist = sum(
            math.sqrt(sum((p.position[i] - centroid[i]) ** 2 for i in range(self.dim)))
            for p in self._particles
        )
        return total_dist / n

    def _get_top_particles(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N particles sorted by fitness."""
        sorted_p = sorted(self._particles, key=lambda p: p.fitness)
        return [
            {
                "position": p.position,
                "fitness": p.fitness,
                "best_fitness": p.best_fitness,
            }
            for p in sorted_p[:n]
        ]

    def optimize(self, max_iter: int, pop_size: int, **kwargs) -> OptimizationResult:
        """Run the optimization. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement optimize()")

    @property
    def name(self) -> str:
        return self.__class__.__name__
