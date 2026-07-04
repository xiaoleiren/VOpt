from __future__ import annotations
import pandas as pd
from .utils import read_csv, write, ensure_results


def subject_summary() -> pd.DataFrame:
    df = read_csv('subject_summary.csv')
    total = pd.DataFrame([{
        'system': 'total', 'language': '',
        'loc': int(df['loc'].sum()),
        'modules': int(df['modules'].sum()),
        'verification_tasks': int(df['verification_tasks'].sum()),
        'log_source': ''
    }])
    return pd.concat([df, total], ignore_index=True)


def verifier_outcome() -> pd.DataFrame:
    df = read_csv('verifier_outcome_summary.csv')
    total = {c: '' for c in df.columns}
    total['system'] = 'total'
    for c in ['tasks','verified_fast','verified_precise','defects_precise','timeouts_fast','timeouts_precise','defects_fast','unknown_fast']:
        total[c] = int(df[c].sum())
    return pd.concat([df, pd.DataFrame([total])], ignore_index=True)


def robustness_summary() -> pd.DataFrame:
    ab = read_csv('feature_ablation.csv')
    lh = read_csv('limited_history.csv')
    tr = read_csv('cross_project_transfer.csv')
    rows = []
    for _, r in ab.iterrows():
        rows.append({'panel':'feature_ablation','setting':r['feature_set'],'vpb_4h':r['vpb_4h'],'ufn_percent':r['ufn_percent'],'fallback_rate_percent':''})
    for _, r in lh.iterrows():
        rows.append({'panel':'limited_history','setting':r['training_data'],'vpb_4h':r['vpb_4h'],'ufn_percent':r['ufn_percent'],'fallback_rate_percent':r['fallback_rate_percent']})
    for _, r in tr.iterrows():
        rows.append({'panel':'cross_project_transfer','setting':f"{r['train_system']}->{r['test_system']} ({int(r['test_tasks'])} tasks)",'vpb_4h':r['vpb_4h'],'ufn_percent':r['ufn_percent'],'fallback_rate_percent':''})
    return pd.DataFrame(rows)


def core_results() -> pd.DataFrame:
    return read_csv('core_results.csv')


def pareto() -> pd.DataFrame:
    return read_csv('pareto_front.csv')


def ufn_summary() -> pd.DataFrame:
    categories = read_csv('ufn_case_categories.csv')
    recovered = read_csv('fallback_recovery_breakdown.csv')
    rows = []
    for _, r in categories.iterrows():
        rows.append({'kind':'ufn_category','name':r['category'],'cases':int(r['verifyopt_ufn_cases'])})
    for _, r in recovered.iterrows():
        rows.append({'kind':'fallback_breakdown','name':r['reason'],'cases':int(r['cases'])})
    return pd.DataFrame(rows)


def main() -> None:
    ensure_results()
    tables = {
        'table_subject_summary.csv': subject_summary(),
        'table_verifier_outcome.csv': verifier_outcome(),
        'table_core_results.csv': core_results(),
        'table_pareto.csv': pareto(),
        'table_robustness.csv': robustness_summary(),
        'ufn_cases_summary.csv': ufn_summary(),
    }
    for name, df in tables.items():
        write(df, name)
        print(f'wrote results/generated/{name} ({len(df)} rows)')

if __name__ == '__main__':
    main()
