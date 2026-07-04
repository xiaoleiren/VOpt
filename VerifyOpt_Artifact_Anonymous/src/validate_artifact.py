from __future__ import annotations
import re
import pandas as pd
from .utils import ROOT, AGG, ensure_results

FORBIDDEN_PATTERNS = [
    r'Wei\s+He', r'Xiaolei', r'Macau University', r'cellocapital', r'celloanalytics',
    r'/Users/', r'C:\\Users\\', r'\\home\\[^\n ]+', r'@hawk', r'@must'
]


def check_no_forbidden_text() -> list[str]:
    violations = []
    for path in ROOT.rglob('*'):
        if path.name == 'validate_artifact.py':
            continue
        if path.is_file() and path.suffix.lower() in {'.md','.py','.csv','.json','.jsonl','.txt','.tex','.cff'}:
            text = path.read_text(errors='ignore')
            for pat in FORBIDDEN_PATTERNS:
                if re.search(pat, text, flags=re.IGNORECASE):
                    violations.append(f'{path.relative_to(ROOT)} matches {pat}')
    return violations


def check_aggregates() -> list[str]:
    issues = []
    subjects = pd.read_csv(AGG / 'subject_summary.csv')
    if int(subjects['verification_tasks'].sum()) != 3343:
        issues.append('verification_tasks total is not 3343')
    if int(subjects['loc'].sum()) != 532900:
        issues.append('LOC total is not 532900')
    core = pd.read_csv(AGG / 'core_results.csv')
    row = core[core['policy'] == 'VerifyOpt + fallback'].iloc[0]
    if int(row['defects_found']) != 214:
        issues.append('VerifyOpt + fallback defects_found is not 214')
    if float(row['ufn_percent']) != 0.2:
        issues.append('VerifyOpt + fallback UFN is not 0.2')
    return issues


def main() -> None:
    issues = []
    issues.extend(check_no_forbidden_text())
    issues.extend(check_aggregates())
    report = ensure_results() / 'artifact_check_report.txt'
    if issues:
        report.write_text('FAILED\n' + '\n'.join(issues) + '\n')
        raise SystemExit(report.read_text())
    report.write_text('PASSED\nNo forbidden deanonymizing patterns found. Aggregate checks passed.\n')
    print(report.read_text())

if __name__ == '__main__':
    main()
