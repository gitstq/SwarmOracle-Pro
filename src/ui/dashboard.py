"""
Terminal UI Dashboard for SwarmOracle.

Provides real-time visualization of optimization progress using
only standard library (no external dependencies).
"""

import math
import time
import sys
from typing import List, Optional


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"


def supports_color() -> bool:
    """Check if terminal supports ANSI colors."""
    if sys.platform == "win32":
        return True
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


class TUIDashboard:
    """
    Terminal-based dashboard for displaying optimization progress.

    Features:
    - ASCII convergence chart
    - Progress bar
    - Real-time statistics
    - Color-coded output
    """

    def __init__(self, use_color: bool = True, width: int = 60, height: int = 12):
        self.use_color = use_color and supports_color()
        self.width = width
        self.height = height
        self._last_print_len = 0

    def _c(self, code: str, text: str) -> str:
        """Apply color code if enabled."""
        if self.use_color:
            return f"{code}{text}{Colors.RESET}"
        return text

    def _clear_line(self):
        """Clear the current line."""
        sys.stdout.write("\r" + " " * self._last_print_len + "\r")
        self._last_print_len = 0

    def print_header(self, algorithm: str, dim: int, pop_size: int, max_iter: int):
        """Print dashboard header."""
        c = self._c
        header = (
            f"\n"
            f"{c(Colors.BOLD + Colors.CYAN, '╔══════════════════════════════════════════════════════════╗')}\n"
            f"{c(Colors.BOLD + Colors.CYAN, '║')}  {c(Colors.BOLD + Colors.WHITE, '🐝 SwarmOracle - Swarm Intelligence Engine')}              {c(Colors.BOLD + Colors.CYAN, '║')}\n"
            f"{c(Colors.BOLD + Colors.CYAN, '╠══════════════════════════════════════════════════════════╣')}\n"
            f"{c(Colors.BOLD + Colors.CYAN, '║')}  Algorithm: {c(Colors.GREEN, algorithm + ' ' * (44 - len(algorithm)))}  {c(Colors.BOLD + Colors.CYAN, '║')}\n"
            f"{c(Colors.BOLD + Colors.CYAN, '║')}  Dimensions: {c(Colors.YELLOW, str(dim) + ' ' * (44 - len(str(dim))))}  {c(Colors.BOLD + Colors.CYAN, '║')}\n"
            f"{c(Colors.BOLD + Colors.CYAN, '║')}  Population: {c(Colors.YELLOW, str(pop_size) + ' ' * (43 - len(str(pop_size))))}  {c(Colors.BOLD + Colors.CYAN, '║')}\n"
            f"{c(Colors.BOLD + Colors.CYAN, '║')}  Max Iter:   {c(Colors.YELLOW, str(max_iter) + ' ' * (43 - len(str(max_iter))))}  {c(Colors.BOLD + Colors.CYAN, '║')}\n"
            f"{c(Colors.BOLD + Colors.CYAN, '╚══════════════════════════════════════════════════════════╝')}\n"
        )
        print(header)

    def print_progress(
        self,
        iteration: int,
        max_iter: int,
        best_fitness: float,
        elapsed: float,
        diversity: float = 0.0,
    ):
        """Print current iteration progress."""
        c = self._c
        progress = iteration / max_iter
        bar_width = 40
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)

        line = (
            f"\r  {c(Colors.BLUE, f'[{bar}]')} "
            f"{c(Colors.WHITE, f'{progress * 100:5.1f}%')} │ "
            f"{c(Colors.GREEN, f'Best: {best_fitness:.6f}')} │ "
            f"{c(Colors.YELLOW, f'Div: {diversity:.4f}')} │ "
            f"{c(Colors.DIM, f'{elapsed:.1f}s')}"
        )
        sys.stdout.write(line)
        sys.stdout.flush()
        self._last_print_len = len(line)

    def print_newline(self):
        """Print newline after progress."""
        sys.stdout.write("\n")
        sys.stdout.flush()

    def print_convergence_chart(self, history: List[float], title: str = "Convergence"):
        """Print ASCII convergence chart."""
        if not history:
            return

        c = self._c
        chart_h = self.height
        chart_w = min(self.width, len(history))

        # Sample history to fit chart width
        if len(history) > chart_w:
            step = len(history) / chart_w
            sampled = [history[int(i * step)] for i in range(chart_w)]
        else:
            sampled = history

        min_val = min(sampled)
        max_val = max(sampled)
        val_range = max_val - min_val if max_val != min_val else 1.0

        print(f"\n  {c(Colors.BOLD + Colors.WHITE, f'📊 {title}')}")
        print(f"  {c(Colors.DIM, f'Min: {min_val:.6f} | Max: {max_val:.6f}')}")

        # Y-axis labels
        for row in range(chart_h):
            y_val = max_val - (row / (chart_h - 1)) * val_range
            label = f"{y_val:10.4f}"
            line = f"  {c(Colors.DIM, label)} │"

            for col_idx in range(len(sampled)):
                val = sampled[col_idx]
                normalized = (val - min_val) / val_range
                target_row = int((1 - normalized) * (chart_h - 1))

                if target_row == row:
                    line += c(Colors.GREEN, "●")
                elif abs(target_row - row) <= 1:
                    line += c(Colors.DIM, "·")
                else:
                    line += " "

            print(line)

        # X-axis
        print(f"  {'':>10s} └{'─' * len(sampled)}")
        print(f"  {'':>10s}  {c(Colors.DIM, '0')}{' ' * max(0, len(sampled) - 8)}{c(Colors.DIM, str(len(history)))}")

    def print_summary(self, result):
        """Print final result summary."""
        c = self._c
        print(f"\n  {c(Colors.BOLD + Colors.GREEN, '✅ Optimization Complete!')}")
        print(f"  {c(Colors.CYAN, '━' * 56)}")
        print(f"  {c(Colors.WHITE, '  Algorithm:')}    {c(Colors.GREEN, result.algorithm_name)}")
        print(f"  {c(Colors.WHITE, '  Best Fitness:')}  {c(Colors.BOLD + Colors.YELLOW, f'{result.best_fitness:.8f}')}")
        print(f"  {c(Colors.WHITE, '  Iterations:')}    {c(Colors.YELLOW, str(result.iteration_count))}")
        print(f"  {c(Colors.WHITE, '  Time:')}          {c(Colors.YELLOW, f'{result.elapsed_time:.4f}s')}")
        print(f"  {c(Colors.WHITE, '  Best Position:')}")
        for i, val in enumerate(result.best_position):
            print(f"    {c(Colors.DIM, f'x[{i}]:')} {c(Colors.CYAN, f'{val:.8f}')}")
        print(f"  {c(Colors.CYAN, '━' * 56)}")

    def print_comparison(self, results: list):
        """Print comparison table for multiple results."""
        c = self._c
        print(f"\n  {c(Colors.BOLD + Colors.WHITE, '🏆 Algorithm Comparison')}")
        print(f"  {c(Colors.CYAN, '━' * 70)}")
        print(
            f"  {c(Colors.BOLD, 'Algorithm'):12s} │ "
            f"{c(Colors.BOLD, 'Best Fitness'):14s} │ "
            f"{c(Colors.BOLD, 'Iterations'):10s} │ "
            f"{c(Colors.BOLD, 'Time'):10s}"
        )
        print(f"  {'─' * 12}─┼─{'─' * 14}─┼─{'─' * 10}─┼─{'─' * 10}")

        sorted_results = sorted(results, key=lambda r: r.best_fitness)
        for i, r in enumerate(sorted_results):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
            print(
                f"  {medal} {c(Colors.WHITE, r.algorithm_name):10s} │ "
                f"{c(Colors.GREEN, f'{r.best_fitness:.8f}'):14s} │ "
                f"{c(Colors.YELLOW, str(r.iteration_count)):10s} │ "
                f"{c(Colors.YELLOW, f'{r.elapsed_time:.4f}s'):10s}"
            )
        print(f"  {c(Colors.CYAN, '━' * 70)}")
