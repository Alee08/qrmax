# Reproducibility

This repository is the reproducibility package for the QR-MAX IJCAI experiments.
The implementation is provided by the pinned `multiagent-rl-rm` commit in
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
- OfficeWorld IJCAI tag: `v0.3.0-ijcai2026`
- pinned commit: `79ba46fd0add6040ee933f1eca93584bcd4ebc82`

The pinned commit includes the OfficeWorld IJCAI code and the continuous-line
and continuous-corridor Bucket QR-MAX checks.

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

Validate the continuous-line suite counts:

```bash
python scripts/validate_continuous_line_config.py
```

Validate the continuous-corridor suite counts:

```bash
python scripts/validate_continuous_corridor_config.py
```

Run the continuous-line smoke check:

```bash
python scripts/reproduce_continuous_line.py --suite continuous_line_smoke
```

Run the continuous-corridor smoke check:

```bash
python scripts/reproduce_continuous_corridor.py --suite continuous_corridor_smoke
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

Run the continuous-line Bucket QR-MAX event-ablation suite:

```bash
python scripts/reproduce_continuous_line.py --suite bucket_event_ablation
```

Run the continuous-line algorithm comparison:

```bash
python scripts/reproduce_continuous_line.py --suite continuous_algorithm_comparison
```

Run the continuous-corridor Bucket QR-MAX event-ablation suite:

```bash
python scripts/reproduce_continuous_corridor.py --suite bucket_event_ablation
```

Run the continuous-corridor algorithm comparison:

```bash
python scripts/reproduce_continuous_corridor.py --suite continuous_corridor_algorithm_comparison
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

Keep committed outputs small: prefer aggregate CSVs, checksums, and plotting
inputs under `paper_results/`, not full raw logs.
