"""
Genetic Algorithm (GA) Implementation.

Classic GA with tournament selection, blend crossover, and Gaussian mutation.
"""

import math
import random
from typing import Callable, List, Tuple, Optional

from ..core.models import BaseOptimizer, Particle, OptimizationResult


class GA(BaseOptimizer):
    """
    Genetic Algorithm optimizer.

    Parameters:
        objective_func: Function to minimize
        dim: Number of dimensions
        bounds: List of (min, max) tuples
        maximize: Set True to maximize
        seed: Random seed
        tournament_size: Tournament selection size (default: 3)
        crossover_rate: Crossover probability (default: 0.8)
        mutation_rate: Mutation probability (default: 0.1)
        mutation_strength: Gaussian mutation std dev ratio (default: 0.1)
        elitism_count: Number of elite individuals to preserve (default: 2)
    """

    def __init__(
        self,
        objective_func: Callable[[List[float]], float],
        dim: int,
        bounds: List[Tuple[float, float]],
        maximize: bool = False,
        seed: Optional[int] = None,
        tournament_size: int = 3,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.1,
        mutation_strength: float = 0.1,
        elitism_count: int = 2,
    ):
        super().__init__(objective_func, dim, bounds, maximize, seed)
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.elitism_count = elitism_count

    def _tournament_select(self, population: List[Particle]) -> Particle:
        """Select individual via tournament selection."""
        candidates = random.sample(population, min(self.tournament_size, len(population)))
        return min(candidates, key=lambda p: p.fitness)

    def _blend_crossover(self, parent1: List[float], parent2: List[float]) -> Tuple[List[float], List[float]]:
        """Blend crossover (BLX-alpha)."""
        alpha = 0.5
        child1, child2 = [], []
        for d in range(self.dim):
            low = min(parent1[d], parent2[d])
            high = max(parent1[d], parent2[d])
            range_val = high - low
            child1.append(random.uniform(low - alpha * range_val, high + alpha * range_val))
            child2.append(random.uniform(low - alpha * range_val, high + alpha * range_val))
        return child1, child2

    def _mutate(self, individual: List[float]) -> List[float]:
        """Apply Gaussian mutation."""
        mutated = individual.copy()
        for d in range(self.dim):
            if random.random() < self.mutation_rate:
                range_val = self.bounds[d][1] - self.bounds[d][0]
                mutated[d] += random.gauss(0, range_val * self.mutation_strength)
        return self._clip_position(mutated)

    def optimize(
        self, max_iter: int = 100, pop_size: int = 30, **kwargs
    ) -> OptimizationResult:
        """Run GA optimization."""
        import time

        start_time = time.time()

        self.crossover_rate = kwargs.get("crossover_rate", self.crossover_rate)
        self.mutation_rate = kwargs.get("mutation_rate", self.mutation_rate)
        self.mutation_strength = kwargs.get("mutation_strength", self.mutation_strength)
        self.elitism_count = kwargs.get("elitism_count", self.elitism_count)

        # Initialize population
        population = self._init_particles(pop_size)
        convergence = []
        diversity_history = []

        for iteration in range(max_iter):
            self._iteration = iteration + 1

            # Sort by fitness
            population.sort(key=lambda p: p.fitness)
            best_fitness = population[0].fitness

            # Elitism: preserve top individuals
            new_population = population[:self.elitism_count]

            # Generate offspring
            while len(new_population) < pop_size:
                parent1 = self._tournament_select(population)
                parent2 = self._tournament_select(population)

                if random.random() < self.crossover_rate:
                    c1_pos, c2_pos = self._blend_crossover(parent1.position, parent2.position)
                else:
                    c1_pos, c2_pos = parent1.position.copy(), parent2.position.copy()

                c1_pos = self._mutate(c1_pos)
                c2_pos = self._mutate(c2_pos)

                c1 = Particle(position=c1_pos, fitness=self._evaluate(c1_pos))
                c2 = Particle(position=c2_pos, fitness=self._evaluate(c2_pos))

                c1.best_fitness = c1.fitness
                c1.best_position = c1.position.copy()
                c2.best_fitness = c2.fitness
                c2.best_position = c2.position.copy()

                new_population.extend([c1, c2])

            population = new_population[:pop_size]

            convergence.append(best_fitness)
            diversity_history.append(self._calculate_diversity())

        elapsed = time.time() - start_time

        population.sort(key=lambda p: p.fitness)
        self._particles = population

        self._result = OptimizationResult(
            best_position=population[0].position,
            best_fitness=population[0].fitness,
            convergence_history=convergence,
            iteration_count=max_iter,
            elapsed_time=elapsed,
            algorithm_name=self.name,
            parameters={
                "crossover_rate": self.crossover_rate,
                "mutation_rate": self.mutation_rate,
                "mutation_strength": self.mutation_strength,
                "elitism_count": self.elitism_count,
                "pop_size": pop_size,
                "max_iter": max_iter,
            },
            population_diversity=diversity_history,
            all_particles=self._get_top_particles(10),
        )

        return self._result
