#!/usr/bin/env python3
"""Summarize OfficeWorld test CSV logs into one aggregate CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = PROJECT_ROOT / "results"
DEFAULT_OUTPUT = PROJECT_ROOT / "paper_results" / "officeworld_summary.csv"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def _float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_test_row(row: list[str]) -> dict[str, str | float] | None:
    if len(row) < 11 or row[0] == "env":
        return None

    base = {
        "env": row[0],
        "map": row[1],
        "experiment": row[2],
        "algorithm": row[3],
        "seed": row[4],
        "episode": row[5],
        "total_steps": row[6],
        "log_total_steps": row[7],
        "elapsed_min": "",
    }

    metrics = row[8:]
    if len(metrics) in {4, 7}:
        base["elapsed_min"] = metrics[0]
        metrics = metrics[1:]

    metric_names = [
        "avg_reward",
        "success_rate",
        "avg_length",
        "avg_reward_stoc",
        "success_rate_stoc",
        "avg_length_stoc",
    ]
    for name, value in zip(metric_names, metrics):
        base[name] = _float(value)
    for name in metric_names:
        base.setdefault(name, "")
    return base


def _read_last_rows(results_dir: Path) -> list[dict[str, str | float]]:
    rows: list[dict[str, str | float]] = []
    for path in sorted(results_dir.glob("test_*.csv")):
        parsed_rows: list[dict[str, str | float]] = []
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle, delimiter=";")
            for raw in reader:
                parsed = _parse_test_row(raw)
                if parsed is not None:
                    parsed_rows.append(parsed)
        if parsed_rows:
            last = parsed_rows[-1]
            try:
                last["source"] = str(path.resolve().relative_to(PROJECT_ROOT))
            except ValueError:
                last["source"] = str(path)
            rows.append(last)
    return rows


def main() -> None:
    args = _parse_args()
    rows = _read_last_rows(args.results_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "env",
        "map",
        "experiment",
        "algorithm",
        "seed",
        "episode",
        "total_steps",
        "log_total_steps",
        "elapsed_min",
        "avg_reward",
        "success_rate",
        "avg_length",
        "avg_reward_stoc",
        "success_rate_stoc",
        "avg_length_stoc",
        "source",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
