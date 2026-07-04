# VerifyOpt Artifact (Anonymous)

This repository contains the reproducibility artifact for the ISSRE Industry Track submission.

The artifact is designed for anonymous review. It contains:

- aggregate data tables used to reproduce the paper's reported results;
- an anonymized, schema-compatible example feature/log dataset for exercising the scripts;
- scripts for computing VPB, UFN, timeout, fallback, ablation, limited-history, and transfer summaries;
- a lightweight budget-aware CI scheduling simulator;
- documentation for replacing the example data with the confidential full task-level logs.

## Confidentiality boundary

The original C/C++ source code, build configurations, proprietary module names, and raw company-internal logs cannot be disclosed. The repository therefore exposes the analysis layer: anonymized features, verifier outcomes, and aggregate result tables. All identifiers are anonymized as `system_a`, `system_b`, `system_c`, and `mod_XXXX`.

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python reproduce.py
```

Expected output files are generated under `results/generated/`:

- `table_subject_summary.csv`
- `table_verifier_outcome.csv`
- `table_core_results.csv`
- `table_pareto.csv`
- `table_robustness.csv`
- `ufn_cases_summary.csv`
- `artifact_check_report.txt`

The command should finish in a few seconds on a laptop.

## What is reproduced

The aggregate tables in `data/aggregate/` reproduce the paper-level numbers:

- 3 systems, 532.9 KLOC, 824 modules, 3,343 verification tasks;
- fast/precise verifier outcome summaries;
- VPB at 1, 2, 4, 8, 16, and 32 hours;
- core policy metrics: VPB, timeouts, false-positive triage, MTTAR, fallback rate, light-strategy tasks, UFN, and defects found;
- feature ablation, limited-history, and cross-project transfer results.

The task-level files under `data/example_anonymized/` are **schema-compatible anonymized examples** for exercising parsers and the scheduling simulator. They are not raw proprietary logs. To run the same scripts on the full private artifact, replace those files with the corresponding confidential exports following `data/schemas/`.

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── reproduce.py
├── data/
│   ├── aggregate/             # paper aggregate result tables
│   ├── example_anonymized/     # anonymized example task/log data
│   └── schemas/               # expected column schemas
├── src/
│   ├── compute_tables.py
│   ├── simulate_ci_scheduler.py
│   ├── train_selector.py
│   ├── validate_artifact.py
│   └── utils.py
├── docs/
│   ├── DATA_AVAILABILITY_SNIPPET.tex
│   ├── ANONYMIZATION.md
│   └── REPRODUCIBILITY_NOTES.md
└── results/generated/
```

## Data availability statement for the paper

A suggested LaTeX snippet is provided in `docs/DATA_AVAILABILITY_SNIPPET.tex`. Replace the placeholder `VerifyOpt-XXXX` with the anonymous.4open.science repository identifier before submission.

## License

The code is released under the MIT License. The anonymized aggregate data are released for review and reproduction of the paper results only.
