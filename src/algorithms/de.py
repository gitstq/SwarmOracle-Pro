"""
Differential Evolution (DE) Algorithm Implementation.

DE/rand/1/bin variant with adaptive control parameters.
"""

import math
import random
from typing import Callable, List, Tuple, Optional

from ..core.models import BaseOptimizer, Particle, OptimizationResult


class DE(BaseOptimizer):
    """
    Differential Evolution optimizer.

    Parameters:
        objective_func: Function to minimize
        dim: Number of dimensions
        bounds: List of (min, max) tuples
        maximize: Set True to maximize
        seed: Random seed
        F: Mutation scaling factor (default: 0.5)
        CR: Crossover probability (default: 0.9)
        strategy: DE strategy - "rand1", "best1", "rand2" (default: "rand1")
    """

    def __init__(
        self,
        objective_func: Callable[[List[float]], float],
        dim: int,
        bounds: List[Tuple[float, float]],
        maximize: bool = False,
        seed: Optional[int] = None,
        F: float = 0.5,
        CR: float = 0.9,
        strategy: str = "rand1",
    ):
        super().__init__(objective_func, dim, bounds, maximize, seed)
        self.F = F
        self.CR = CR
        self.strategy = strategy

    def _mutate_rand1(self, idx: int, pop: List[Particle]) -> List[float]:
        """DE/rand/1 mutation."""
        candidates = [i for i in range(len(pop)) if i != idx]
        r1, r2, r3 = random.sample(candidates, 3)
        mutant = [
            pop[r1].position[d] + self.F * (pop[r2].position[d] - pop[r3].position[d])
            for d in range(self.dim)
        ]
        return mutant

    def _mutate_best1(self, idx: int, pop: List[Particle]) -> List[float]:
        """DE/best/1 mutation."""
        best = min(pop, key=lambda p: p.fitness)
        candidates = [i for i in range(len(pop)) if i != idx]
        r1, r2 = random.sample(candidates, 2)
        mutant = [
            best.position[d] + self.F * (pop[r1].position[d] - pop[r2].position[d])
            for d in range(self.dim)
        ]
        return mutant

    def _mutate_rand2(self, idx: int, pop: List[Particle]) -> List[float]:
        """DE/rand/2 mutation."""
        candidates = [i for i in range(len(pop)) if i != idx]
        r1, r2, r3, r4, r5 = random.sample(candidates, 5)
        mutant = [
            pop[r1].position[d] + self.F * (
                pop[r2].position[d] - pop[r3].position[d]
            ) + self.F * (
                pop[r4].position[d] - pop[r5].position[d]
            )
            for d in range(self.dim)
        ]
        return mutant

    def _crossover(self, target: List[float], mutant: List[float]) -> List[float]:
        """Binomial crossover."""
        trial = target.copy()
        j_rand = random.randint(0, self.dim - 1)
        for d in range(self.dim):
            if random.random() <= self.CR or d == j_rand:
                trial[d] = mutant[d]
        return trial

    def optimize(
        self, max_iter: int = 100, pop_size: int = 30, **kwargs
    ) -> OptimizationResult:
        """Run DE optimization."""
        import time

        start_time = time.time()

        self.F = kwargs.get("F", self.F)
        self.CR = kwargs.get("CR", self.CR)
        self.strategy = kwargs.get("strategy", self.strategy)

        # Initialize population
        population = self._init_particles(pop_size)
        convergence = []
        diversity_history = []

        mutation_map = {
            "rand1": self._mutate_rand1,
            "best1": self._mutate_best1,
            "rand2": self._mutate_rand2,
        }
        mutate_fn = mutation_map.get(self.strategy, self._mutate_rand1)

        for iteration in range(max_iter):
            self._iteration = iteration + 1

            for i, target in enumerate(population):
                # Mutation
                mutant = mutate_fn(i, population)
                mutant = self._clip_position(mutant)

                # Crossover
                trial = self._crossover(target.position, mutant)
                trial = self._clip_position(trial)

                # Selection (greedy)
                trial_fitness = self._evaluate(trial)
                if trial_fitness <= target.fitness:
                    target.position = trial
                    target.fitness = trial_fitness
                    if trial_fitness < target.best_fitness:
                        target.best_fitness = trial_fitness
                        target.best_position = trial.copy()

            best = min(population, key=lambda p: p.fitness)
            convergence.append(best.fitness)
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
                "F": self.F,
                "CR": self.CR,
                "strategy": self.strategy,
                "pop_size": pop_size,
                "max_iter": max_iter,
            },
            population_diversity=diversity_history,
            all_particles=self._get_top_particles(10),
        )

        return self._result
