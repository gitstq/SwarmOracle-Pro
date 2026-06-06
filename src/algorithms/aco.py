"""
Ant Colony Optimization (ACO) Algorithm Implementation.

Continuous ACO adapted for function optimization using Gaussian sampling
around pheromone-weighted ant positions.
"""

import math
import random
from typing import Callable, List, Tuple, Optional

from ..core.models import BaseOptimizer, Particle, OptimizationResult


class ACO(BaseOptimizer):
    """
    Ant Colony Optimization for continuous domains.

    Parameters:
        objective_func: Function to minimize
        dim: Number of dimensions
        bounds: List of (min, max) tuples
        maximize: Set True to maximize
        seed: Random seed
        evaporation_rate: Pheromone evaporation rate (default: 0.1)
        q: Pheromone deposit factor (default: 1.0)
        sigma_init: Initial Gaussian kernel width (default: 1.0)
        sigma_min: Minimum kernel width (default: 0.01)
    """

    def __init__(
        self,
        objective_func: Callable[[List[float]], float],
        dim: int,
        bounds: List[Tuple[float, float]],
        maximize: bool = False,
        seed: Optional[int] = None,
        evaporation_rate: float = 0.1,
        q: float = 1.0,
        sigma_init: float = 1.0,
        sigma_min: float = 0.01,
    ):
        super().__init__(objective_func, dim, bounds, maximize, seed)
        self.evaporation_rate = evaporation_rate
        self.q = q
        self.sigma_init = sigma_init
        self.sigma_min = sigma_min

    def optimize(
        self, max_iter: int = 100, pop_size: int = 30, **kwargs
    ) -> OptimizationResult:
        """Run ACO optimization."""
        import time

        start_time = time.time()

        self.evaporation_rate = kwargs.get("evaporation_rate", self.evaporation_rate)
        self.q = kwargs.get("q", self.q)
        self.sigma_init = kwargs.get("sigma_init", self.sigma_init)
        self.sigma_min = kwargs.get("sigma_min", self.sigma_min)

        # Solution archive (pheromone matrix)
        archive_size = pop_size
        archive = [self._random_position() for _ in range(archive_size)]
        archive_fitness = [self._evaluate(pos) for pos in archive]

        # Sort archive by fitness
        sorted_indices = sorted(
            range(archive_size), key=lambda i: archive_fitness[i]
        )
        archive = [archive[i] for i in sorted_indices]
        archive_fitness = [archive_fitness[i] for i in sorted_indices]

        sigma = self.sigma_init
        convergence = []
        diversity_history = []

        for iteration in range(max_iter):
            self._iteration = iteration + 1
            new_solutions = []

            for k in range(pop_size):
                # Select solution from archive using weighted probability
                weights = [
                    1.0 / (rank + 1 + 0.1) for rank in range(archive_size)
                ]
                total_w = sum(weights)
                weights = [w / total_w for w in weights]

                r = random.random()
                cumulative = 0.0
                selected_idx = 0
                for idx, w in enumerate(weights):
                    cumulative += w
                    if r <= cumulative:
                        selected_idx = idx
                        break

                # Generate new solution using Gaussian kernel
                new_pos = []
                for d in range(self.dim):
                    mean = archive[selected_idx][d]
                    std = max(sigma * (self.bounds[d][1] - self.bounds[d][0]), self.sigma_min)
                    val = random.gauss(mean, std)
                    new_pos.append(val)

                new_pos = self._clip_position(new_pos)
                new_solutions.append(new_pos)

            # Evaluate new solutions
            new_fitness = [self._evaluate(pos) for pos in new_solutions]

            # Merge and keep best
            combined = list(zip(archive + new_solutions, archive_fitness + new_fitness))
            combined.sort(key=lambda x: x[1])
            archive = [c[0] for c in combined[:archive_size]]
            archive_fitness = [c[1] for c in combined[:archive_size]]

            # Decay sigma
            sigma = max(sigma * 0.98, self.sigma_min)

            convergence.append(archive_fitness[0])
            diversity_history.append(
                sum(
                    math.sqrt(
                        sum(
                            (archive[i][d] - archive[0][d]) ** 2
                            for d in range(self.dim)
                        )
                    )
                    for i in range(1, min(5, archive_size))
                )
                / min(5, archive_size)
            )

        elapsed = time.time() - start_time

        # Build particles for result
        self._particles = [
            Particle(position=archive[i], fitness=archive_fitness[i])
            for i in range(min(10, archive_size))
        ]

        self._result = OptimizationResult(
            best_position=archive[0],
            best_fitness=archive_fitness[0],
            convergence_history=convergence,
            iteration_count=max_iter,
            elapsed_time=elapsed,
            algorithm_name=self.name,
            parameters={
                "evaporation_rate": self.evaporation_rate,
                "q": self.q,
                "sigma_init": self.sigma_init,
                "pop_size": pop_size,
                "max_iter": max_iter,
            },
            population_diversity=diversity_history,
            all_particles=self._get_top_particles(10),
        )

        return self._result
