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
- commit: `fa1f90b5516389aadbecf654deecf9da38823c4b`

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
| `paper_main` | 300 | Three main OfficeWorld configurations. |
| `paper_table6` | 500 | Five configurations summarized in the paper table. |
| `paper_appendix_15` | 4500 | Appendix sweep over map1-map3, exp1-exp5, 30 seeds. |
| `officeworld_discrete` | 2100 | Full encoded OfficeWorld sweep. |

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
OfficeWorld runner: `QL`, `QRM`, `RMAX`, `RMAXRM`, `QRMAX`, `QRMAXRM`,
`UCBVI-sB`, `UCBVI-B`, `UCBVI-H`, and `OPSRL`.

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

The reported Table 6 OfficeWorld values from the paper are included as
`paper_results/table6_officeworld_steps.csv` for reference.
The extended 15-configuration OfficeWorld breakdown is included as
`paper_results/table4_officeworld_15_configs.csv`.

<details>
<summary>Table 4: OfficeWorld 15-Configuration Breakdown</summary>

Training steps to reach the optimal policy compared with Value Iteration (VI).
The last two columns report the VI policy average length and success rate.

| Map | Exp | Q-Learning | R-MAX | QR-MAX | QRM | R-MAXRM | QR-MAXRM | Avg. Length (VI) | Success Rate (VI %) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Map1 | exp1 | 128,973 | 59,691 | 30,376 | 66,693 | 21,777 | 10,964 | 21.08 | 66.76 |
| Map1 | exp2 | 201,835 | 77,797 | 27,619 | 129,804 | 26,232 | 9,339 | 39.31 | 39.40 |
| Map1 | exp3 | 355,070 | 155,347 | 30,325 | 122,827 | 28,682 | 6,087 | 40.94 | 38.68 |
| Map1 | exp4 | 469,313 | 103,211 | 29,950 | 135,119 | 26,953 | 6,062 | 42.23 | 34.37 |
| Map1 | exp5 | 1,267,449 | 287,066 | 38,312 | 231,870 | 30,238 | 4,107 | 77.86 | 15.47 |
| Map2 | exp1 | 334,894 | 213,942 | 83,593 | 225,491 | 74,250 | 28,729 | 52.46 | 54.69 |
| Map2 | exp2 | 326,306 | 88,636 | 56,445 | 220,334 | 49,577 | 19,214 | 53.10 | 37.92 |
| Map2 | exp3 | 723,051 | 316,672 | 62,583 | 280,763 | 63,066 | 12,415 | 63.04 | 37.25 |
| Map2 | exp4 | 889,842 | 196,334 | 61,775 | 249,912 | 47,873 | 12,445 | 73.80 | 28.18 |
| Map2 | exp5 | 2,613,669 | 723,441 | 83,076 | 438,213 | 65,523 | 8,396 | 123.39 | 14.15 |
| Map3 | exp1 | 501,559 | 201,731 | 98,663 | 297,975 | 73,832 | 33,815 | 55.83 | 33.32 |
| Map3 | exp2 | 553,517 | 170,926 | 99,952 | 353,658 | 66,949 | 33,853 | 63.76 | 32.57 |
| Map3 | exp3 | 1,105,417 | 388,562 | 110,808 | 406,122 | 111,349 | 21,856 | 68.69 | 32.42 |
| Map3 | exp4 | 1,466,896 | 495,878 | 112,165 | 449,594 | 107,115 | 21,869 | 81.91 | 21.27 |
| Map3 | exp5 | 5,471,046 | 1,581,301 | 159,597 | 891,160 | 128,950 | 14,717 | 156.46 | 6.55 |

</details>

## Paper Figures

<p align="center">
  <img src="paper_results/figures/config_map0_exp0.png" alt="Configuration 1: map0 exp0" width="32%">
  <img src="paper_results/figures/config_map1_exp5.png" alt="Configuration 2: map1 exp5" width="32%">
  <img src="paper_results/figures/config_map4_exp6.png" alt="Configuration 3: map4 exp6" width="32%">
</p>

See `REPRODUCIBILITY.md` for the full workflow.

## Citation

Use `CITATION.cff` for repository metadata. The final IJCAI citation can be
added once the camera-ready bibliographic metadata is available.
