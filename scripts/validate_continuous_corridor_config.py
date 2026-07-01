#!/usr/bin/env python3
"""Validate configured continuous-corridor suite run counts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace

from reproduce_continuous_corridor import DEFAULT_CONFIG, _iter_jobs


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--suite", default=None)
    return parser.parse_args()


def _empty_overrides() -> SimpleNamespace:
    return SimpleNamespace(
        algorithms=None,
        event_aware=None,
        sequence=None,
        layout=None,
        bucket_mode=None,
        buckets_x=None,
        buckets_y=None,
        thresholds=None,
        noise_std=None,
        reset_x_low=None,
        reset_x_high=None,
        reset_y_low=None,
        reset_y_high=None,
        horizon=None,
        seeds=None,
        train_episodes=None,
        eval_episodes=None,
    )


def main() -> None:
    args = _parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    suites = config.get("suites", {})
    selected = [args.suite] if args.suite else sorted(suites)

    failed = False
    for suite_name in selected:
        if suite_name not in suites:
            raise SystemExit(f"Unknown suite '{suite_name}'")
        jobs = list(_iter_jobs(config, suite_name, _empty_overrides()))
        expected = suites[suite_name].get("expected_runs")
        actual = len(jobs)
        status = "ok"
        if expected is not None and actual != expected:
            failed = True
            status = f"expected {expected}"
        print(f"{suite_name}: {actual} runs ({status})")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
