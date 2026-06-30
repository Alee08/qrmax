#!/usr/bin/env python3
"""Thin launcher for the discrete OfficeWorld experiments in multiagent-rl-rm."""

from __future__ import annotations

import importlib
import importlib.util
import os
import signal
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OFFICE_MAIN = "multiagent_rlrm.environments.office_world.office_main"


def _load_office_main():
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/qrmax-matplotlib")

    spec = importlib.util.find_spec(OFFICE_MAIN)
    if spec is None or spec.origin is None:
        raise SystemExit(
            "Cannot import multiagent_rlrm OfficeWorld. "
            "Run `pip install -r requirements.txt` first."
        )

    office_dir = Path(spec.origin).resolve().parent
    if str(office_dir) not in sys.path:
        sys.path.insert(0, str(office_dir))

    return importlib.import_module(OFFICE_MAIN)


def _prepare_output_paths(office_main) -> None:
    os.chdir(PROJECT_ROOT)
    (PROJECT_ROOT / "results").mkdir(exist_ok=True)

    # The upstream runner uses inspect.getsourcefile(...) to decide where to put
    # train/test CSVs. Point it at this repo so outputs stay in qrmax/results.
    office_main.inspect.getsourcefile = lambda _obj: str(PROJECT_ROOT / "office_main.py")


def _apply_wandb_config(office_main, args):
    if not args.wandb:
        return args

    hyperparameters = {
        "environment": args.env_str,
        "map": args.map,
        "experiment": args.experiment,
        "stochastic": args.stochastic,
        "highprob": args.highprob if args.stochastic else None,
        "algorithm": args.algorithm,
        "seed": args.seed,
        "gamma": args.gamma,
        "learning_rate": args.learning_rate if "RMAX" not in args.algorithm else None,
        "VIdeltarel": args.VIdeltarel if "RMAX" in args.algorithm else None,
        "VIdelta": args.VIdelta if "RMAX" in args.algorithm else None,
        "Kthreshold": args.Kthreshold if "RMAX" in args.algorithm else None,
        "early_stop": args.early_stop,
        "render": args.render,
        "generate_heatmap": args.generate_heatmap,
    }

    office_main.wandb.init(
        project=office_main.config["wandb"]["project"],
        entity=office_main.config["wandb"]["entity"],
        config=hyperparameters,
        reinit=True,
    )

    args.map = office_main.wandb.config.get("map", args.map)
    args.experiment = office_main.wandb.config.get("experiment", args.experiment)
    args.algorithm = office_main.wandb.config.get("algorithm", args.algorithm)
    args.seed = office_main.wandb.config.get("seed", args.seed)
    args.Kthreshold = office_main.wandb.config.get("Kthreshold", args.Kthreshold)
    args.gamma = office_main.wandb.config.get("gamma", args.gamma)
    args.VIdelta = office_main.wandb.config.get("VIdelta", args.VIdelta)
    args.stochastic = office_main.wandb.config.get("stochastic", args.stochastic)
    args.highprob = office_main.wandb.config.get("highprob", args.highprob)
    args.early_stop = office_main.wandb.config.get("early_stop", args.early_stop)
    args.render = office_main.wandb.config.get("render", args.render)
    args.generate_heatmap = office_main.wandb.config.get(
        "generate_heatmap", args.generate_heatmap
    )
    args.learning_rate = office_main.wandb.config.get(
        "learning_rate", args.learning_rate
    )

    office_main.getenvstr(args)
    office_main.wandb.run.name = f"{args.env_str}_{args.map}_{args.experiment}"
    office_main.wandb.run.save()
    return args


def main() -> None:
    office_main = _load_office_main()
    _prepare_output_paths(office_main)

    signal.signal(signal.SIGINT, office_main.signal_handler)
    default_algorithm = office_main.config["maps"][office_main.DEFAULT_MAP]["agents"][0][
        "algorithm"
    ]
    args = office_main.parse_arguments(
        office_main.DEFAULT_MAP,
        office_main.DEFAULT_EXPERIMENT,
        default_algorithm,
    )
    office_main.getenvstr(args)
    args = _apply_wandb_config(office_main, args)

    office_main.args = args
    office_main.run_experiment(args)


if __name__ == "__main__":
    main()
