# Reproducibility

This repository is the reproducibility layer for the QR-MAX IJCAI artifact.
The implementation is provided by the pinned `multiagent-rl-rm` release tag in
`requirements.txt`; this repository keeps the experiment matrices, launchers,
and post-processing scripts.

## Environment

Recommended setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The pinned companion library is:

- package: `multiagent-rl-rm`
- version: `0.3.0`
- tag: `v0.3.0-ijcai2026`
- commit: `fa1f90b5516389aadbecf654deecf9da38823c4b`

Before making this repository public, push that tag to
`https://github.com/Alee08/multiagent-rl-rm` or publish the matching PyPI
release and update `requirements.txt` to `multiagent-rl-rm==0.3.0`.

## Sanity Checks

Validate the configured run counts:

```bash
python scripts/validate_config.py
```

Print the smoke command without running it:

```bash
python scripts/reproduce_officeworld.py --suite smoke --dry-run
```

Run the smoke check:

```bash
python scripts/reproduce_officeworld.py --suite smoke
```

## Experiment Suites

Run the main OfficeWorld suite:

```bash
python scripts/reproduce_officeworld.py --suite paper_main
```

Run the five-configuration paper table suite:

```bash
python scripts/reproduce_officeworld.py --suite paper_table6
```

Run the 30-seed appendix sweep:

```bash
python scripts/reproduce_officeworld.py --suite paper_appendix_15
```

Run the full encoded OfficeWorld sweep:

```bash
python scripts/reproduce_officeworld.py --suite officeworld_discrete
```

Use filters for partial reruns:

```bash
python scripts/reproduce_officeworld.py \
  --suite officeworld_discrete \
  --algorithms QRMAX QRMAXRM \
  --maps map1 map2 \
  --seeds 0 1 2
```

## Outputs

The runner writes raw logs under `results/` and summary text files named
`results_<map>_<experiment>.txt`. Raw logs are ignored by Git.

After runs complete, generate an aggregate CSV suitable for archiving:

```bash
python scripts/summarize_officeworld.py \
  --results-dir results \
  --output paper_results/officeworld_summary.csv
```

Keep committed artifacts small: prefer aggregate CSVs, checksums, and plotting
inputs under `paper_results/`, not full raw logs.
