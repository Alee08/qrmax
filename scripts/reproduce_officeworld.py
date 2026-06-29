#!/usr/bin/env python3
"""Run OfficeWorld discrete experiment suites from configs/officeworld_discrete.json."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "officeworld_discrete.json"
RUNNER = PROJECT_ROOT / "scripts" / "run_officeworld.py"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--suite", default="smoke")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-runs", type=int, default=None)
    parser.add_argument("--maps", nargs="+", default=None)
    parser.add_argument("--experiments", nargs="+", default=None)
    parser.add_argument("--algorithms", nargs="+", default=None)
    parser.add_argument("--seeds", nargs="+", type=int, default=None)
    parser.add_argument("--steps", type=float, default=None)
    parser.add_argument("--eval", type=int, default=None)
    return parser.parse_args()


def _iter_commands(config: dict, suite_name: str, overrides: argparse.Namespace):
    defaults = config.get("defaults", {})
    suites = config.get("suites", {})
    if suite_name not in suites:
        raise SystemExit(
            f"Unknown suite '{suite_name}'. Available: {', '.join(sorted(suites))}"
        )

    suite = suites[suite_name]
    seeds = overrides.seeds if overrides.seeds is not None else suite.get("seeds", [100])
    steps = overrides.steps if overrides.steps is not None else suite.get("steps")
    eval_interval = (
        overrides.eval
        if overrides.eval is not None
        else suite.get("eval", defaults.get("eval"))
    )
    stochastic = suite.get("stochastic", False)
    highprob = suite.get("highprob", defaults.get("highprob", 0.8))
    gamma = suite.get("gamma", defaults.get("gamma", 0.99))
    kthreshold = suite.get("Kthreshold", defaults.get("Kthreshold", 39))
    vi_delta = suite.get("VIdelta", defaults.get("VIdelta", 0.01))
    early_stop = suite.get("early_stop", defaults.get("early_stop", False))
    wandb = suite.get("wandb", defaults.get("wandb", False))

    for group in suite.get("runs", []):
        map_name = group["map"]
        if overrides.maps is not None and map_name not in overrides.maps:
            continue

        experiments = group.get("experiments", [])
        if overrides.experiments is not None:
            experiments = [exp for exp in experiments if exp in overrides.experiments]

        algorithms = group.get("algorithms", [])
        if overrides.algorithms is not None:
            algorithms = [alg for alg in algorithms if alg in overrides.algorithms]

        for experiment in experiments:
            for algorithm in algorithms:
                for seed in seeds:
                    cmd = [
                        sys.executable,
                        str(RUNNER),
                        "--map",
                        map_name,
                        "--experiment",
                        experiment,
                        "--algorithm",
                        algorithm,
                        "--seed",
                        str(seed),
                        "--gamma",
                        str(gamma),
                        "--Kthreshold",
                        str(kthreshold),
                        "--VIdelta",
                        str(vi_delta),
                    ]
                    if steps is not None:
                        cmd.extend(["--steps", str(steps)])
                    if eval_interval is not None:
                        cmd.extend(["--eval", str(eval_interval)])
                    if stochastic:
                        cmd.extend(["--stochastic", "--highprob", str(highprob)])
                    if early_stop:
                        cmd.append("--early_stop")
                    if wandb:
                        cmd.append("--wandb")
                    yield cmd


def main() -> None:
    args = _parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))

    count = 0
    for cmd in _iter_commands(config, args.suite, args):
        count += 1
        print(" ".join(cmd), flush=True)
        if not args.dry_run:
            subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
        if args.max_runs is not None and count >= args.max_runs:
            break

    if count == 0:
        raise SystemExit("No runs matched the selected filters.")


if __name__ == "__main__":
    main()
