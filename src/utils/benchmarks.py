"""
Built-in benchmark functions for testing and demonstration.

Includes classic optimization test functions:
- Sphere, Rastrigin, Rosenbrock, Ackley, Griewank, Schwefel, Booth, Beale
"""

import math


def sphere(x):
    """Sphere function. Global minimum: f(0,...,0) = 0"""
    return sum(xi ** 2 for xi in x)


def rastrigin(x):
    """Rastrigin function. Global minimum: f(0,...,0) = 0"""
    n = len(x)
    return 10 * n + sum(xi ** 2 - 10 * math.cos(2 * math.pi * xi) for xi in x)


def rosenbrock(x):
    """Rosenbrock function. Global minimum: f(1,...,1) = 0"""
    return sum(
        100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
        for i in range(len(x) - 1)
    )


def ackley(x):
    """Ackley function. Global minimum: f(0,...,0) = 0"""
    n = len(x)
    sum_sq = sum(xi ** 2 for xi in x)
    sum_cos = sum(math.cos(2 * math.pi * xi) for xi in x)
    return (
        -20 * math.exp(-0.2 * math.sqrt(sum_sq / n))
        - math.exp(sum_cos / n)
        + 20
        + math.e
    )


def griewank(x):
    """Griewank function. Global minimum: f(0,...,0) = 0"""
    sum_sq = sum(xi ** 2 for xi in x) / 4000
    prod_cos = 1
    for i, xi in enumerate(x):
        prod_cos *= math.cos(xi / math.sqrt(i + 1))
    return sum_sq - prod_cos + 1


def schwefel(x):
    """Schwefel function. Global minimum: f(420.9687,...,420.9687) ≈ 0"""
    n = len(x)
    return 418.9829 * n - sum(xi * math.sin(math.sqrt(abs(xi))) for xi in x)


def booth(x):
    """Booth function (2D). Global minimum: f(1,3) = 0"""
    return (x[0] + 2 * x[1] - 7) ** 2 + (2 * x[0] + x[1] - 5) ** 2


def beale(x):
    """Beale function (2D). Global minimum: f(3,0.5) = 0"""
    return (
        (1.5 - x[0] + x[0] * x[1]) ** 2
        + (2.25 - x[0] + x[0] * x[1] ** 2) ** 2
        + (2.625 - x[0] + x[0] * x[1] ** 3) ** 2
    )


def three_hump_camel(x):
    """Three-Hump Camel function (2D). Global minimum: f(0,0) = 0"""
    return 2 * x[0] ** 2 - 1.05 * x[0] ** 4 + x[0] ** 6 / 6 + x[0] * x[1] + x[1] ** 2


def easom(x):
    """Easom function (2D). Global minimum: f(pi,pi) = -1"""
    return (
        -math.cos(x[0]) * math.cos(x[1])
        * math.exp(-((x[0] - math.pi) ** 2 + (x[1] - math.pi) ** 2))
    )


# Benchmark registry with metadata
BENCHMARKS = {
    "sphere": {
        "func": sphere,
        "bounds": [(-5.12, 5.12)],
        "optimum": 0.0,
        "optimum_pos": [0.0],
        "description": "Simple unimodal bowl-shaped function",
    },
    "rastrigin": {
        "func": rastrigin,
        "bounds": [(-5.12, 5.12)],
        "optimum": 0.0,
        "optimum_pos": [0.0],
        "description": "Highly multimodal with many local minima",
    },
    "rosenbrock": {
        "func": rosenbrock,
        "bounds": [(-5, 10)],
        "optimum": 0.0,
        "optimum_pos": [1.0],
        "description": "Classic valley-shaped function, hard to optimize",
    },
    "ackley": {
        "func": ackley,
        "bounds": [(-5, 5)],
        "optimum": 0.0,
        "optimum_pos": [0.0],
        "description": "Nearly flat outer region with deep hole at center",
    },
    "griewank": {
        "func": griewank,
        "bounds": [(-600, 600)],
        "optimum": 0.0,
        "optimum_pos": [0.0],
        "description": "Widespread local minima, cosine modulation helps",
    },
    "schwefel": {
        "func": schwefel,
        "bounds": [(-500, 500)],
        "optimum": 0.0,
        "optimum_pos": [420.9687],
        "description": "Complex multimodal, deceptive second-best minimum",
    },
    "booth": {
        "func": booth,
        "bounds": [(-10, 10)],
        "optimum": 0.0,
        "optimum_pos": [1.0, 3.0],
        "description": "Simple 2D unimodal function",
    },
    "beale": {
        "func": beale,
        "bounds": [(-4.5, 4.5)],
        "optimum": 0.0,
        "optimum_pos": [3.0, 0.5],
        "description": "2D function with sharp peaks",
    },
    "three_hump_camel": {
        "func": three_hump_camel,
        "bounds": [(-5, 5)],
        "optimum": 0.0,
        "optimum_pos": [0.0, 0.0],
        "description": "Simple 3-hump function",
    },
    "easom": {
        "func": easom,
        "bounds": [(-100, 100)],
        "optimum": -1.0,
        "optimum_pos": [math.pi, math.pi],
        "description": "2D function with very narrow global minimum",
    },
}
