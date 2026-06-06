"""Basic tests for SwarmOracle algorithms."""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms import PSO, ACO, GA, DE
from src.utils.benchmarks import sphere, rastrigin, rosenbrock, ackley


def test_sphere_pso():
    """Test PSO on sphere function."""
    dim = 5
    bounds = [(-5.12, 5.12)] * dim
    optimizer = PSO(objective_func=sphere, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=200, pop_size=30)
    assert result.best_fitness < 0.01, f"PSO sphere failed: {result.best_fitness}"
    assert len(result.convergence_history) == 200
    print(f"  ✅ PSO on Sphere: fitness={result.best_fitness:.8f}")


def test_sphere_ga():
    """Test GA on sphere function."""
    dim = 5
    bounds = [(-5.12, 5.12)] * dim
    optimizer = GA(objective_func=sphere, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=200, pop_size=30)
    assert result.best_fitness < 0.1, f"GA sphere failed: {result.best_fitness}"
    print(f"  ✅ GA on Sphere: fitness={result.best_fitness:.8f}")


def test_sphere_de():
    """Test DE on sphere function."""
    dim = 5
    bounds = [(-5.12, 5.12)] * dim
    optimizer = DE(objective_func=sphere, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=200, pop_size=30)
    assert result.best_fitness < 0.01, f"DE sphere failed: {result.best_fitness}"
    print(f"  ✅ DE on Sphere: fitness={result.best_fitness:.8f}")


def test_sphere_aco():
    """Test ACO on sphere function."""
    dim = 5
    bounds = [(-5.12, 5.12)] * dim
    optimizer = ACO(objective_func=sphere, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=200, pop_size=30)
    assert result.best_fitness < 1.0, f"ACO sphere failed: {result.best_fitness}"
    print(f"  ✅ ACO on Sphere: fitness={result.best_fitness:.8f}")


def test_rastrigin_pso():
    """Test PSO on rastrigin function."""
    dim = 5
    bounds = [(-5.12, 5.12)] * dim
    optimizer = PSO(objective_func=rastrigin, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=500, pop_size=50)
    assert result.best_fitness < 5.0, f"PSO rastrigin failed: {result.best_fitness}"
    print(f"  ✅ PSO on Rastrigin: fitness={result.best_fitness:.8f}")


def test_rosenbrock_de():
    """Test DE on rosenbrock function."""
    dim = 5
    bounds = [(-5, 10)] * dim
    optimizer = DE(objective_func=rosenbrock, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=500, pop_size=50)
    assert result.best_fitness < 10.0, f"DE rosenbrock failed: {result.best_fitness}"
    print(f"  ✅ DE on Rosenbrock: fitness={result.best_fitness:.8f}")


def test_maximize():
    """Test maximization mode."""
    dim = 2
    bounds = [(-5, 5)] * dim

    def neg_sphere(x):
        return -sum(xi ** 2 for xi in x)

    optimizer = PSO(objective_func=neg_sphere, dim=dim, bounds=bounds, maximize=True, seed=42)
    result = optimizer.optimize(max_iter=100, pop_size=20)
    assert result.best_fitness < 0.01, f"Maximize failed: {result.best_fitness}"
    print(f"  ✅ Maximize mode: fitness={result.best_fitness:.8f}")


def test_result_serialization():
    """Test result to_dict and summary."""
    dim = 3
    bounds = [(-5, 5)] * dim
    optimizer = PSO(objective_func=sphere, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=50, pop_size=10)

    d = result.to_dict()
    assert "algorithm" in d
    assert "best_fitness" in d
    assert "convergence_history" in d

    summary = result.summary()
    assert "PSO" in summary
    print(f"  ✅ Result serialization: OK")


def test_export():
    """Test export functionality."""
    from src.export.formats import export_json, export_csv, export_markdown
    import tempfile

    dim = 3
    bounds = [(-5, 5)] * dim
    optimizer = PSO(objective_func=sphere, dim=dim, bounds=bounds, seed=42)
    result = optimizer.optimize(max_iter=50, pop_size=10)

    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = export_json(result, os.path.join(tmpdir, "test.json"))
        assert os.path.exists(json_path)
        print(f"  ✅ JSON export: OK")

        csv_path = export_csv(result, os.path.join(tmpdir, "test.csv"))
        assert os.path.exists(csv_path)
        print(f"  ✅ CSV export: OK")

        md_path = export_markdown(result, os.path.join(tmpdir, "test.md"))
        assert os.path.exists(md_path)
        print(f"  ✅ Markdown export: OK")


def run_all_tests():
    """Run all tests."""
    print("\n🐝 SwarmOracle Test Suite")
    print("=" * 50)

    tests = [
        test_sphere_pso,
        test_sphere_ga,
        test_sphere_de,
        test_sphere_aco,
        test_rastrigin_pso,
        test_rosenbrock_de,
        test_maximize,
        test_result_serialization,
        test_export,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'=' * 50}\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
