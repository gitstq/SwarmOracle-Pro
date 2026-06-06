#!/usr/bin/env python3
"""
SwarmOracle - Lightweight Swarm Intelligence Prediction Engine

A zero-dependency Python CLI tool for swarm intelligence optimization.
Supports PSO, ACO, GA, and DE algorithms with TUI dashboard visualization.

Usage:
    python -m swarmoracle run --algo pso --func sphere --dim 10 --iter 100
    python -m swarmoracle bench --dim 5 --iter 50
    python -m swarmoracle compare --func rastrigin --dim 10 --iter 100
    python -m swarmoracle list
"""

import sys
import os
import argparse
import json
import time
import math

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms import PSO, ACO, GA, DE, ALGORITHM_REGISTRY
from src.utils.benchmarks import BENCHMARKS
from src.ui.dashboard import TUIDashboard
from src.export.formats import export_result
from src.core.models import OptimizationResult


VERSION = "1.0.0"


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="swarmoracle",
        description="🐝 SwarmOracle - Lightweight Swarm Intelligence Prediction Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python swarmoracle run --algo pso --func sphere --dim 10 --iter 100
  python swarmoracle run --algo ga --func rosenbrock --dim 5 --iter 200 --pop 50
  python swarmoracle bench --dim 5 --iter 50
  python swarmoracle compare --func rastrigin --dim 10 --iter 100
  python swarmoracle list
  python swarmoracle custom --algo pso --dim 3 --bounds "-5,5" "-5,5" "-5,5" --iter 100
        """,
    )
    parser.add_argument("--version", action="version", version=f"SwarmOracle v{VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a single optimization")
    run_parser.add_argument("--algo", "-a", choices=list(ALGORITHM_REGISTRY.keys()), default="pso", help="Algorithm to use")
    run_parser.add_argument("--func", "-f", choices=list(BENCHMARKS.keys()), default="sphere", help="Benchmark function")
    run_parser.add_argument("--dim", "-d", type=int, default=10, help="Number of dimensions")
    run_parser.add_argument("--iter", "-i", type=int, default=100, help="Max iterations")
    run_parser.add_argument("--pop", "-p", type=int, default=30, help="Population size")
    run_parser.add_argument("--seed", "-s", type=int, default=None, help="Random seed")
    run_parser.add_argument("--maximize", action="store_true", help="Maximize instead of minimize")
    run_parser.add_argument("--export", "-e", type=str, default=None, help="Export directory")
    run_parser.add_argument("--no-ui", action="store_true", help="Disable TUI dashboard")
    run_parser.add_argument("--params", type=str, default=None, help="Extra params as JSON string")

    # Benchmark command
    bench_parser = subparsers.add_parser("bench", help="Run all algorithms on all benchmarks")
    bench_parser.add_argument("--dim", "-d", type=int, default=5, help="Number of dimensions")
    bench_parser.add_argument("--iter", "-i", type=int, default=50, help="Max iterations")
    bench_parser.add_argument("--pop", "-p", type=int, default=20, help="Population size")
    bench_parser.add_argument("--seed", "-s", type=int, default=42, help="Random seed")
    bench_parser.add_argument("--export", "-e", type=str, default=None, help="Export directory")

    # Compare command
    cmp_parser = subparsers.add_parser("compare", help="Compare all algorithms on one function")
    cmp_parser.add_argument("--func", "-f", choices=list(BENCHMARKS.keys()), default="sphere", help="Benchmark function")
    cmp_parser.add_argument("--dim", "-d", type=int, default=10, help="Number of dimensions")
    cmp_parser.add_argument("--iter", "-i", type=int, default=100, help="Max iterations")
    cmp_parser.add_argument("--pop", "-p", type=int, default=30, help="Population size")
    cmp_parser.add_argument("--seed", "-s", type=int, default=None, help="Random seed")
    cmp_parser.add_argument("--export", "-e", type=str, default=None, help="Export directory")

    # List command
    subparsers.add_parser("list", help="List available algorithms and benchmark functions")

    # Custom function command
    custom_parser = subparsers.add_parser("custom", help="Run with custom bounds")
    custom_parser.add_argument("--algo", "-a", choices=list(ALGORITHM_REGISTRY.keys()), default="pso")
    custom_parser.add_argument("--dim", "-d", type=int, default=3, help="Number of dimensions")
    custom_parser.add_argument("--bounds", "-b", nargs="+", required=True, help="Bounds as 'min,max' pairs")
    custom_parser.add_argument("--iter", "-i", type=int, default=100, help="Max iterations")
    custom_parser.add_argument("--pop", "-p", type=int, default=30, help="Population size")
    custom_parser.add_argument("--seed", "-s", type=int, default=None, help="Random seed")
    custom_parser.add_argument("--export", "-e", type=str, default=None, help="Export directory")

    return parser


def cmd_list(args):
    """List available algorithms and benchmarks."""
    c = lambda code, text: text  # No color in list mode for compatibility

    print("\n🐝 SwarmOracle - Available Components")
    print("=" * 60)

    print("\n📊 Algorithms:")
    for name, cls in ALGORITHM_REGISTRY.items():
        print(f"  • {name.upper():4s} - {cls.__doc__.strip().split(chr(10))[0]}")

    print("\n📐 Benchmark Functions:")
    for name, info in BENCHMARKS.items():
        print(f"  • {name:20s} - {info['description']}")
        print(f"    Bounds: {info['bounds'][0]}, Optimum: {info['optimum']}")

    print()


def cmd_run(args):
    """Run a single optimization."""
    bench = BENCHMARKS[args.func]
    func = bench["func"]
    bounds = [bench["bounds"][0]] * args.dim

    algo_cls = ALGORITHM_REGISTRY[args.algo]
    extra_params = {}
    if args.params:
        extra_params = json.loads(args.params)

    optimizer = algo_cls(
        objective_func=func,
        dim=args.dim,
        bounds=bounds,
        maximize=args.maximize,
        seed=args.seed,
    )

    dashboard = TUIDashboard() if not args.no_ui else None

    if dashboard:
        dashboard.print_header(args.algo.upper(), args.dim, args.pop, args.iter)

    start = time.time()
    result = optimizer.optimize(max_iter=args.iter, pop_size=args.pop, **extra_params)
    elapsed = time.time() - start

    if dashboard:
        dashboard.print_newline()
        dashboard.print_convergence_chart(result.convergence_history)
        dashboard.print_summary(result)

    if args.export:
        exported = export_result(result, args.export, name=f"{args.algo}_{args.func}")
        print(f"\n  📁 Results exported to: {args.export}/")
        for fmt, path in exported.items():
            print(f"     • {fmt.upper()}: {path}")

    return result


def cmd_bench(args):
    """Run benchmark across all algorithms and functions."""
    dashboard = TUIDashboard()
    print(f"\n  🏋️ Running Full Benchmark Suite (dim={args.dim}, iter={args.iter})")
    print(f"  {TUIDashboard().use_color and '━' or '-'}" * 60)

    all_results = []

    for func_name, bench_info in BENCHMARKS.items():
        func = bench_info["func"]
        bounds = [bench_info["bounds"][0]] * args.dim

        print(f"\n  📐 Function: {func_name}")
        func_results = []

        for algo_name, algo_cls in ALGORITHM_REGISTRY.items():
            seed = args.seed
            optimizer = algo_cls(
                objective_func=func,
                dim=args.dim,
                bounds=bounds,
                seed=seed,
            )
            result = optimizer.optimize(max_iter=args.iter, pop_size=args.pop)
            func_results.append(result)
            all_results.append(result)

            status = "✅" if abs(result.best_fitness - bench_info["optimum"]) < 0.01 else "⚠️"
            print(
                f"    {status} {algo_name.upper():4s}: "
                f"fitness={result.best_fitness:.6f} | "
                f"time={result.elapsed_time:.3f}s"
            )

        dashboard.print_comparison(func_results)

    if args.export:
        for r in all_results:
            export_result(r, args.export, name=f"{r.algorithm_name}_{args.dim}d")

    return all_results


def cmd_compare(args):
    """Compare all algorithms on a single function."""
    bench = BENCHMARKS[args.func]
    func = bench["func"]
    bounds = [bench["bounds"][0]] * args.dim

    dashboard = TUIDashboard()
    dashboard.print_header(f"All Algorithms", args.dim, args.pop, args.iter)

    results = []
    for algo_name, algo_cls in ALGORITHM_REGISTRY.items():
        optimizer = algo_cls(
            objective_func=func,
            dim=args.dim,
            bounds=bounds,
            seed=args.seed,
        )
        result = optimizer.optimize(max_iter=args.iter, pop_size=args.pop)
        results.append(result)

        if not args.no_ui:
            dashboard.print_progress(
                len(results), len(ALGORITHM_REGISTRY),
                result.best_fitness, result.elapsed_time
            )
            dashboard.print_newline()

    dashboard.print_comparison(results)

    # Show best convergence chart
    best = min(results, key=lambda r: r.best_fitness)
    dashboard.print_convergence_chart(best.convergence_history, f"{best.algorithm_name} Convergence")

    if args.export:
        for r in results:
            export_result(r, args.export, name=f"{r.algorithm_name}_{args.func}")

    return results


def cmd_custom(args):
    """Run optimization with custom bounds."""
    bounds = []
    for b_str in args.bounds:
        parts = b_str.split(",")
        bounds.append((float(parts[0]), float(parts[1])))

    if len(bounds) != args.dim:
        print(f"  ❌ Error: Expected {args.dim} bounds, got {len(bounds)}")
        sys.exit(1)

    # Use sphere as default objective for custom bounds
    from src.utils.benchmarks import sphere
    func = sphere

    algo_cls = ALGORITHM_REGISTRY[args.algo]
    optimizer = algo_cls(
        objective_func=func,
        dim=args.dim,
        bounds=bounds,
        seed=args.seed,
    )

    dashboard = TUIDashboard()
    dashboard.print_header(args.algo.upper(), args.dim, args.pop, args.iter)

    result = optimizer.optimize(max_iter=args.iter, pop_size=args.pop)

    dashboard.print_newline()
    dashboard.print_convergence_chart(result.convergence_history)
    dashboard.print_summary(result)

    if args.export:
        export_result(result, args.export, name=f"{args.algo}_custom")

    return result


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "list": cmd_list,
        "run": cmd_run,
        "bench": cmd_bench,
        "compare": cmd_compare,
        "custom": cmd_custom,
    }

    cmd_fn = commands.get(args.command)
    if cmd_fn:
        try:
            cmd_fn(args)
        except KeyboardInterrupt:
            print("\n  ⏹️ Optimization interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
