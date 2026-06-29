# Paper Results

Use this directory for small derived artifacts: aggregate CSVs, checksums, and
plotting inputs generated from raw OfficeWorld logs.

Raw `results/` logs are intentionally ignored by Git.

Included reference data:

- `table4_officeworld_15_configs.csv`: Table 4 values reported in the
  extended paper, "Training steps to reach the optimal policy compared with
  Value Iteration (VI)" for 15 OfficeWorld configurations.
- `table6_officeworld_steps.csv`: Table 6 values reported in the paper,
  "Average training steps to find a policy that produces results
  indistinguishable from VI optimal solution", mean over 10 random seeds.

Included figures:

- `figures/config_map0_exp0.png`: Configuration 1 (map0 exp0).
- `figures/config_map1_exp5.png`: Configuration 2 (map1 exp5).
- `figures/config_map4_exp6.png`: Configuration 3 (map4 exp6).
- `figures/map1.png`: Base OfficeWorld map1 used in the Table 4 sweep.
- `figures/map2.png`: Base OfficeWorld map2 used in the Table 4 sweep.
- `figures/map3.png`: Base OfficeWorld map3 used in the Table 4 sweep.
