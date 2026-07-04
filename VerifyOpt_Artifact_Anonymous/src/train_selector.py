from __future__ import annotations
import math
import pandas as pd
from .utils import ROOT, ensure_results

FEATURES = [
    'loc','cyclomatic_complexity','loop_count','pointer_use','fan_in','fan_out',
    'recursion','switch_density','macro_expansion_size','changed_code_size',
    'criticality_flag','previous_runtime_s','previous_timeout','previous_warning_count',
    'previous_confirmed_warning_ratio','previous_human_escalation'
]


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, x))))


def score(row: pd.Series) -> float:
    """Small transparent selector used only for artifact smoke testing.

    The paper used XGBoost; this lightweight implementation keeps the public
    artifact dependency-free while exercising the same feature columns and
    producing deterministic predictions.
    """
    z = 2.0
    z -= 0.0012 * row['loc']
    z -= 0.08 * row['cyclomatic_complexity']
    z -= 0.11 * row['loop_count']
    z -= 0.35 * row['pointer_use']
    z -= 0.00008 * row['macro_expansion_size']
    z -= 0.55 * row['criticality_flag']
    z -= 0.80 * row['previous_timeout']
    z -= 0.05 * row['previous_warning_count']
    z += 0.02 * max(0.0, 10.0 - row['previous_runtime_s'])
    return sigmoid(z)


def main() -> None:
    df = pd.read_csv(ROOT / 'data' / 'example_anonymized' / 'task_features.csv')
    df['label_light'] = df['fast_status'].isin(['verified','defect']).astype(int)
    test = df[df['split'] == 'test'].copy()
    test['p_light'] = test.apply(score, axis=1)
    test['pred_light'] = (test['p_light'] >= 0.5).astype(int)
    acc = (test['pred_light'] == test['label_light']).mean()
    out = ensure_results() / 'selector_training_demo.txt'
    out.write_text(
        'model=transparent_dependency_free_smoke_test\n'
        'note=The paper used XGBoost; this script validates schema and feature flow without requiring xgboost.\n'
        f'example_test_accuracy={acc:.4f}\n'
        f'rows_test={len(test)}\n'
    )
    print(out.read_text())

if __name__ == '__main__':
    main()
