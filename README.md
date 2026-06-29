# QR-MAX IJCAI Artifact

This repository contains the reproducibility layer for:

> Model-Based Reinforcement Learning in Discrete-Action Non-Markovian Reward
> Decision Processes

Paper: https://arxiv.org/abs/2512.14617

Reusable implementation code lives in the companion library:

https://github.com/Alee08/multiagent-rl-rm

`qrmax` keeps only the experiment-facing pieces: pinned dependency metadata,
OfficeWorld experiment matrices, launchers, reproducibility notes, and
post-processing scripts.

## Dependency Freeze

The artifact is pinned to the companion-library release tag:

- package: `multiagent-rl-rm`
- package version: `0.3.0`
- tag: `v0.3.0-ijcai2026`
- commit: `17da42eed2db4ae736d64c1dc22bf135dc00bb91`

Before making this repository public, push the tag to
`Alee08/multiagent-rl-rm` or publish the matching PyPI release and update
`requirements.txt` to `multiagent-rl-rm==0.3.0`.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Sanity Checks

Validate configured suite sizes:

```bash
python scripts/validate_config.py
```

Dry-run the smoke suite:

```bash
python scripts/reproduce_officeworld.py --suite smoke --dry-run
```

Run a short smoke experiment:

```bash
python scripts/reproduce_officeworld.py --suite smoke
```

## Experiment Suites

Suites are defined in `configs/officeworld_discrete.json`.

| Suite | Runs | Purpose |
| --- | ---: | --- |
| `smoke` | 1 | Fast local/CI sanity check. |
| `paper_main` | 80 | Main OfficeWorld configuration. |
| `officeworld_discrete` | 1680 | Full encoded OfficeWorld sweep. |

Run a suite:

```bash
python scripts/reproduce_officeworld.py --suite paper_main
```

Filter a larger suite without editing JSON:

```bash
python scripts/reproduce_officeworld.py \
  --suite officeworld_discrete \
  --algorithms QRMAX QRMAXRM \
  --maps map1 map2 \
  --seeds 0 1 2
```

The configured algorithm identifiers are the ones exposed by the frozen
OfficeWorld runner: `QL`, `QRM`, `RMAX`, `RMAXRM`, `QRMAX`, `QRMAXRM`, `UCBVI`,
and `OPSRL`.

## Outputs

The upstream OfficeWorld runner writes raw logs under `results/` and summary
text files named `results_<map>_<experiment>.txt`. These files are ignored by
Git.

Generate a compact aggregate CSV:

```bash
python scripts/summarize_officeworld.py \
  --results-dir results \
  --output paper_results/officeworld_summary.csv
```

See `REPRODUCIBILITY.md` for the full workflow.

## Citation

Use `CITATION.cff` for repository metadata. The final IJCAI citation can be
added once the camera-ready bibliographic metadata is available.
