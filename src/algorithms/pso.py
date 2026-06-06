"""
Particle Swarm Optimization (PSO) Algorithm Implementation.

Classic PSO with inertia weight, cognitive and social components.
Supports adaptive inertia and velocity clamping.
"""

import math
import random
from typing import Callable, List, Tuple, Optional, Dict, Any

from ..core.models import BaseOptimizer, Particle, OptimizationResult


class PSO(BaseOptimizer):
    """
    Particle Swarm Optimization optimizer.

    Parameters:
        objective_func: Function to minimize (or maximize if maximize=True)
        dim: Number of dimensions
        bounds: List of (min, max) tuples for each dimension
        maximize: Set True to maximize instead of minimize
        seed: Random seed for reproducibility
        w: Inertia weight (default: 0.7)
        c1: Cognitive coefficient (default: 1.5)
        c2: Social coefficient (default: 1.5)
        w_decay: Inertia weight decay rate (default: 0.99)
        v_max_ratio: Velocity max as ratio of bound range (default: 0.2)
    """

    def __init__(
        self,
        objective_func: Callable[[List[float]], float],
        dim: int,
        bounds: List[Tuple[float, float]],
        maximize: bool = False,
        seed: Optional[int] = None,
        w: float = 0.7,
        c1: float = 1.5,
        c2: float = 1.5,
        w_decay: float = 0.99,
        v_max_ratio: float = 0.2,
    ):
        super().__init__(objective_func, dim, bounds, maximize, seed)
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.w_decay = w_decay
        self.v_max_ratio = v_max_ratio

    def optimize(
        self, max_iter: int = 100, pop_size: int = 30, **kwargs
    ) -> OptimizationResult:
        """
        Run PSO optimization.

        Args:
            max_iter: Maximum number of iterations
            pop_size: Number of particles

        Returns:
            OptimizationResult with best solution found
        """
        import time

        start_time = time.time()

        # Override params from kwargs
        self.w = kwargs.get("w", self.w)
        self.c1 = kwargs.get("c1", self.c1)
        self.c2 = kwargs.get("c2", self.c2)
        self.w_decay = kwargs.get("w_decay", self.w_decay)

        # Calculate velocity bounds
        v_max = [
            (b[1] - b[0]) * self.v_max_ratio for b in self.bounds
        ]

        # Initialize particles
        self._particles = self._init_particles(pop_size)
        self._iteration = 0

        # Track global best
        global_best_pos = self._particles[0].best_position.copy()
        global_best_fit = self._particles[0].best_fitness

        for p in self._particles:
            if p.fitness < global_best_fit:
                global_best_fit = p.fitness
                global_best_pos = p.position.copy()

        convergence = []
        diversity_history = []

        for iteration in range(max_iter):
            self._iteration = iteration + 1

            for p in self._particles:
                # Update velocity
                for d in range(self.dim):
                    r1 = random.random()
                    r2 = random.random()
                    cognitive = self.c1 * r1 * (p.best_position[d] - p.position[d])
                    social = self.c2 * r2 * (global_best_pos[d] - p.position[d])
                    p.velocity[d] = (
                        self.w * p.velocity[d] + cognitive + social
                    )
                    # Clamp velocity
                    p.velocity[d] = max(-v_max[d], min(v_max[d], p.velocity[d]))

                # Update position
                p.position = [
                    p.position[d] + p.velocity[d] for d in range(self.dim)
                ]
                p.position = self._clip_position(p.position)

                # Evaluate
                p.fitness = self._evaluate(p.position)

                # Update personal best
                if p.fitness < p.best_fitness:
                    p.best_fitness = p.fitness
                    p.best_position = p.position.copy()

                # Update global best
                if p.fitness < global_best_fit:
                    global_best_fit = p.fitness
                    global_best_pos = p.position.copy()

            # Apply inertia decay
            self.w *= self.w_decay

            convergence.append(global_best_fit)
            diversity_history.append(self._calculate_diversity())

        elapsed = time.time() - start_time

        self._result = OptimizationResult(
            best_position=global_best_pos,
            best_fitness=global_best_fit,
            convergence_history=convergence,
            iteration_count=max_iter,
            elapsed_time=elapsed,
            algorithm_name=self.name,
            parameters={
                "w": kwargs.get("w", 0.7),
                "c1": kwargs.get("c1", 1.5),
                "c2": kwargs.get("c2", 1.5),
                "w_decay": kwargs.get("w_decay", 0.99),
                "pop_size": pop_size,
                "max_iter": max_iter,
            },
            population_diversity=diversity_history,
            all_particles=self._get_top_particles(10),
        )

        return self._result
