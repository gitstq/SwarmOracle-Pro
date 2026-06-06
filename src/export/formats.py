"""
Export module - Multi-format result export.

Supports JSON, CSV, and Markdown export formats.
"""

import json
import os
from typing import Dict, Any, List, Optional

from ..core.models import OptimizationResult


def export_json(result: OptimizationResult, filepath: str) -> str:
    """Export optimization result to JSON file."""
    data = result.to_dict()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath


def export_csv(result: OptimizationResult, filepath: str) -> str:
    """Export convergence history to CSV file."""
    lines = ["iteration,fitness,diversity"]
    for i, fit in enumerate(result.convergence_history):
        div = result.population_diversity[i] if i < len(result.population_diversity) else ""
        lines.append(f"{i + 1},{fit:.8f},{div:.8f}" if div else f"{i + 1},{fit:.8f},")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return filepath


def export_markdown(result: OptimizationResult, filepath: str) -> str:
    """Export optimization result to Markdown report."""
    lines = [
        f"# SwarmOracle Optimization Report",
        "",
        f"## Algorithm: {result.algorithm_name}",
        "",
        f"## Results Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| **Best Fitness** | {result.best_fitness:.8f} |",
        f"| **Iterations** | {result.iteration_count} |",
        f"| **Elapsed Time** | {result.elapsed_time:.4f}s |",
        "",
        f"## Best Position",
        "",
    ]
    for i, val in enumerate(result.best_position):
        lines.append(f"- **Dimension {i + 1}**: {val:.8f}")

    lines.extend([
        "",
        "## Parameters",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
    ])
    for key, val in result.parameters.items():
        lines.append(f"| {key} | {val} |")

    lines.extend([
        "",
        "## Convergence History (sampled)",
        "",
        "| Iteration | Fitness |",
        "|-----------|---------|",
    ])
    step = max(1, len(result.convergence_history) // 20)
    for i in range(0, len(result.convergence_history), step):
        lines.append(f"| {i + 1} | {result.convergence_history[i]:.8f} |")
    if len(result.convergence_history) % step != 0:
        lines.append(
            f"| {len(result.convergence_history)} | {result.convergence_history[-1]:.8f} |"
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return filepath


def export_result(
    result: OptimizationResult,
    output_dir: str,
    name: str = "result",
    formats: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Export result in multiple formats.

    Args:
        result: OptimizationResult to export
        output_dir: Directory to save files
        name: Base filename (without extension)
        formats: List of formats to export ("json", "csv", "md")
                 Defaults to all formats

    Returns:
        Dict mapping format to filepath
    """
    if formats is None:
        formats = ["json", "csv", "md"]

    os.makedirs(output_dir, exist_ok=True)
    exported = {}

    if "json" in formats:
        path = os.path.join(output_dir, f"{name}.json")
        exported["json"] = export_json(result, path)

    if "csv" in formats:
        path = os.path.join(output_dir, f"{name}.csv")
        exported["csv"] = export_csv(result, path)

    if "md" in formats:
        path = os.path.join(output_dir, f"{name}.md")
        exported["md"] = export_markdown(result, path)

    return exported
