"""
SwarmOracle Quick Start Example

Demonstrates basic usage of the swarm intelligence optimization engine.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms import PSO, GA, DE, ACO
from src.utils.benchmarks import sphere, rastrigin, rosenbrock
from src.ui.dashboard import TUIDashboard
from src.export.formats import export_result


def example_basic():
    """Basic optimization example."""
    print("\n  📌 Example 1: Basic PSO on Sphere Function")
    print("  " + "-" * 45)

    dim = 10
    bounds = [(-5.12, 5.12)] * dim

    optimizer = PSO(
        objective_func=sphere,
        dim=dim,
        bounds=bounds,
        seed=42,
    )
    result = optimizer.optimize(max_iter=100, pop_size=30)
    print(result.summary())


def example_comparison():
    """Compare algorithms example."""
    print("\n  📌 Example 2: Algorithm Comparison on Rastrigin")
    print("  " + "-" * 45)

    dim = 5
    bounds = [(-5.12, 5.12)] * dim
    results = []

    for name, cls in [("PSO", PSO), ("GA", GA), ("DE", DE), ("ACO", ACO)]:
        opt = cls(objective_func=rastrigin, dim=dim, bounds=bounds, seed=42)
        result = opt.optimize(max_iter=200, pop_size=30)
        results.append(result)
        print(f"  {name}: fitness={result.best_fitness:.6f} | time={result.elapsed_time:.3f}s")

    dashboard = TUIDashboard()
    dashboard.print_comparison(results)


def example_custom_function():
    """Custom objective function example."""
    print("\n  📌 Example 3: Custom Objective Function")
    print("  " + "-" * 45)

    def custom_func(x):
        """Custom: minimize distance from point (2, 3, -1)."""
        target = [2.0, 3.0, -1.0]
        return sum((xi - ti) ** 2 for xi, ti in zip(x, target))

    dim = 3
    bounds = [(-10, 10)] * dim

    optimizer = DE(objective_func=custom_func, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=100, pop_size=20)
    print(result.summary())
    print(f"  Expected position: [2.0000, 3.0000, -1.0000]")


def example_with_export():
    """Export results example."""
    print("\n  📌 Example 4: Export Results")
    print("  " + "-" * 45)

    dim = 5
    bounds = [(-5.12, 5.12)] * dim

    optimizer = PSO(objective_func=rosenbrock, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=200, pop_size=30)

    exported = export_result(result, "/tmp/swarmoracle_example", name="rosenbrock_pso")
    for fmt, path in exported.items():
        print(f"  📁 {fmt.upper()}: {path}")


if __name__ == "__main__":
    example_basic()
    example_comparison()
    example_custom_function()
    example_with_export()
    print("\n  ✅ All examples completed!\n")
