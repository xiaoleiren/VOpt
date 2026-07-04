# Reproducibility notes

The paper's aggregate results are reproduced from CSV files in `data/aggregate/`. The full proprietary task-level logs cannot be released, but the schemas and a small anonymized example are provided to show how the analysis pipeline operates.

## Metrics

- VPB: verified properties within a strict wall-clock budget.
- UFN: unsafe false-negative rate on the subset of light-strategy tasks for which a precise reference result is conclusive.
- MTTAR: machine-side mean time to actionable result; asynchronous human review latency is reported separately.

## CI scheduler model

The simulator models eight parallel workers with budget-aware dispatch. Diagnostic retries are admitted only when the remaining wall-clock budget can accommodate the retry cap. Otherwise the task is routed to an asynchronous ticket and not counted toward VPB.
