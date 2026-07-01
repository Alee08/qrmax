#!/usr/bin/env python3
"""Run continuous-FrozenLake Bucket QR-MAX suites."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/qrmax-matplotlib")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "continuous_frozen_lake_bucket_qrmax.json"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "paper_results" / "continuous_frozen_lake_bucket_qrmax_summary.csv"
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--suite", default="continuous_frozen_lake_smoke")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-runs", type=int, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--algorithms", nargs="+", default=None)
    parser.add_argument(
        "--event-aware", choices=["true", "false"], nargs="+", default=None
    )
    parser.add_argument("--map", nargs="+", default=None)
    parser.add_argument("--sequence", nargs="+", default=None)
    parser.add_argument("--bucket-mode", nargs="+", default=None)
    parser.add_argument("--buckets-x", nargs="+", type=int, default=None)
    parser.add_argument("--buckets-y", nargs="+", type=int, default=None)
    parser.add_argument("--thresholds", nargs="+", type=int, default=None)
    parser.add_argument("--noise-std", nargs="+", type=float, default=None)
    parser.add_argument("--slip-probability", nargs="+", type=float, default=None)
    parser.add_argument("--step-size", nargs="+", type=float, default=None)
    parser.add_argument("--horizon", nargs="+", type=int, default=None)
    parser.add_argument("--start-x", nargs="+", type=int, default=None)
    parser.add_argument("--start-y", nargs="+", type=int, default=None)
    parser.add_argument("--seeds", nargs="+", type=int, default=None)
    parser.add_argument("--train-episodes", type=int, default=None)
    parser.add_argument("--eval-episodes", type=int, default=None)
    return parser.parse_args()


def _selected(value, allowed):
    return value if value is not None else allowed


def _event_values(values):
    if values is None:
        return None
    return [value.lower() == "true" for value in values]


def _iter_jobs(config: dict, suite_name: str, overrides: argparse.Namespace):
    defaults = config.get("defaults", {})
    suites = config.get("suites", {})
    if suite_name not in suites:
        raise SystemExit(
            f"Unknown suite '{suite_name}'. Available: {', '.join(sorted(suites))}"
        )

    suite = suites[suite_name]
    seeds = (
        overrides.seeds
        if overrides.seeds is not None
        else suite.get("seeds", defaults.get("seeds", [2000]))
    )
    train_episodes = (
        overrides.train_episodes
        if overrides.train_episodes is not None
        else suite.get("train_episodes", defaults.get("train_episodes", 1200))
    )
    eval_episodes = (
        overrides.eval_episodes
        if overrides.eval_episodes is not None
        else suite.get("eval_episodes", defaults.get("eval_episodes", 50))
    )
    event_filter = _event_values(overrides.event_aware)

    for group in suite.get("runs", []):
        algorithms = _selected(overrides.algorithms, group.get("algorithms", []))
        event_aware_values = _selected(event_filter, group.get("event_aware", []))
        map_values = _selected(
            overrides.map,
            group.get("map", defaults.get("map", ["map1"])),
        )
        sequence_values = _selected(
            overrides.sequence,
            group.get("sequence", defaults.get("sequence", ["ABC"])),
        )
        bucket_mode_values = _selected(
            overrides.bucket_mode,
            group.get("bucket_mode", defaults.get("bucket_mode", ["uniform"])),
        )
        buckets_x_values = _selected(
            overrides.buckets_x,
            group.get("buckets_x", defaults.get("buckets_x", [10])),
        )
        buckets_y_values = _selected(
            overrides.buckets_y,
            group.get("buckets_y", defaults.get("buckets_y", [10])),
        )
        threshold_values = _selected(
            overrides.thresholds,
            group.get("thresholds", defaults.get("thresholds", [8])),
        )
        noise_values = _selected(
            overrides.noise_std,
            group.get("noise_std", defaults.get("noise_std", [0.0])),
        )
        slip_values = _selected(
            overrides.slip_probability,
            group.get("slip_probability", defaults.get("slip_probability", [0.0])),
        )
        step_size_values = _selected(
            overrides.step_size,
            group.get("step_size", defaults.get("step_size", [0.65])),
        )
        horizon_values = _selected(
            overrides.horizon,
            group.get("horizon", defaults.get("horizon", [180])),
        )
        start_x_values = _selected(
            overrides.start_x,
            group.get("start_x", defaults.get("start_x", [5])),
        )
        start_y_values = _selected(
            overrides.start_y,
            group.get("start_y", defaults.get("start_y", [0])),
        )

        for algorithm in algorithms:
            for event_aware in event_aware_values:
                for map_name in map_values:
                    for sequence in sequence_values:
                        for bucket_mode in bucket_mode_values:
                            for buckets_x in buckets_x_values:
                                for buckets_y in buckets_y_values:
                                    for threshold in threshold_values:
                                        for noise_std in noise_values:
                                            for slip_probability in slip_values:
                                                for step_size in step_size_values:
                                                    for horizon in horizon_values:
                                                        for start_x in start_x_values:
                                                            for (
                                                                start_y
                                                            ) in start_y_values:
                                                                yield {
                                                                    "algorithm": algorithm,
                                                                    "include_event_label": event_aware,
                                                                    "map_name": map_name,
                                                                    "event_sequence": sequence,
                                                                    "bucket_mode": bucket_mode,
                                                                    "buckets_x": buckets_x,
                                                                    "buckets_y": buckets_y,
                                                                    "threshold": threshold,
                                                                    "noise_std": noise_std,
                                                                    "slip_probability": slip_probability,
                                                                    "step_size": step_size,
                                                                    "horizon": horizon,
                                                                    "start_x": start_x,
                                                                    "start_y": start_y,
                                                                    "seeds": seeds,
                                                                    "train_episodes": train_episodes,
                                                                    "eval_episodes": eval_episodes,
                                                                }


def _command_for_job(job):
    cmd = [
        sys.executable,
        "-m",
        "multiagent_rlrm.environments.continuous_frozen_lake.bucket_qrmax_experiment",
        "--algorithm",
        job["algorithm"],
        "--map",
        job["map_name"],
        "--sequence",
        job["event_sequence"],
        "--bucket-mode",
        job["bucket_mode"],
        "--buckets-x",
        str(job["buckets_x"]),
        "--buckets-y",
        str(job["buckets_y"]),
        "--threshold",
        str(job["threshold"]),
        "--noise-std",
        str(job["noise_std"]),
        "--slip-probability",
        str(job["slip_probability"]),
        "--step-size",
        str(job["step_size"]),
        "--horizon",
        str(job["horizon"]),
        "--start-x",
        str(job["start_x"]),
        "--start-y",
        str(job["start_y"]),
        "--train-episodes",
        str(job["train_episodes"]),
        "--eval-episodes",
        str(job["eval_episodes"]),
        "--seeds",
        ",".join(str(seed) for seed in job["seeds"]),
    ]
    if job["include_event_label"]:
        cmd.append("--event-aware")
    return cmd


def _row_from_summary(suite_name: str, job: dict, summary: dict, source: str) -> dict:
    avg_len = summary["average_length_mean"]
    first_perfect = summary["first_perfect_eval_episode_mean"]
    return {
        "suite": suite_name,
        "algorithm": job["algorithm"],
        "event_aware": job["include_event_label"],
        "map": job["map_name"],
        "sequence": job["event_sequence"],
        "bucket_mode": job["bucket_mode"],
        "buckets_x": job["buckets_x"],
        "buckets_y": job["buckets_y"],
        "threshold": job["threshold"],
        "noise_std": job["noise_std"],
        "slip_probability": job["slip_probability"],
        "step_size": job["step_size"],
        "horizon": job["horizon"],
        "start_x": job["start_x"],
        "start_y": job["start_y"],
        "seeds": " ".join(str(seed) for seed in job["seeds"]),
        "train_episodes": job["train_episodes"],
        "eval_episodes": job["eval_episodes"],
        "success_mean": f"{summary['success_mean']:.6f}",
        "success_min": f"{summary['success_min']:.6f}",
        "success_max": f"{summary['success_max']:.6f}",
        "average_length_mean": "" if avg_len is None else f"{avg_len:.6f}",
        "first_perfect_eval_episode_mean": (
            "" if first_perfect is None else f"{first_perfect:.6f}"
        ),
        "training_successes_mean": f"{summary['training_successes_mean']:.6f}",
        "training_failures_mean": f"{summary['training_failures_mean']:.6f}",
        "event_count_means": json.dumps(summary["event_count_means"], sort_keys=True),
        "source": source,
    }


def main() -> None:
    args = _parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    commit = config.get("library", {}).get("commit", "unknown")
    source = f"local sweep with multiagent-rl-rm commit {commit}"

    rows = []
    count = 0
    run_bucket_qrmax_sweep = None
    for job in _iter_jobs(config, args.suite, args):
        count += 1
        print(" ".join(_command_for_job(job)), flush=True)
        if not args.dry_run:
            if run_bucket_qrmax_sweep is None:
                from multiagent_rlrm.environments.continuous_frozen_lake import (
                    bucket_qrmax_experiment,
                )

                run_bucket_qrmax_sweep = bucket_qrmax_experiment.run_bucket_qrmax_sweep
            summary = run_bucket_qrmax_sweep(**job)
            rows.append(_row_from_summary(args.suite, job, summary, source))
        if args.max_runs is not None and count >= args.max_runs:
            break

    if count == 0:
        raise SystemExit("No runs matched the selected filters.")

    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
