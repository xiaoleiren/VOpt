from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from .utils import AGG, ensure_results


def main() -> None:
    df = pd.read_csv(AGG / 'pareto_front.csv')
    fig, ax = plt.subplots(figsize=(6, 3.5))
    columns = [
        ('fixed_fast','Fixed fast'),
        ('fixed_precise','Fixed precise'),
        ('rule_baseline','Rule baseline'),
        ('verifyopt','VerifyOpt'),
        ('verifyopt_fallback','VerifyOpt + fallback'),
    ]
    for col, label in columns:
        ax.plot(df['budget_h'], df[col], marker='o', label=label)
    ax.set_xlabel('CI budget (hours)')
    ax.set_ylabel('Verified properties within budget')
    ax.set_xscale('log', base=2)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = ensure_results() / 'pareto_front_demo.png'
    fig.savefig(out, dpi=200)
    print(f'wrote {out}')

if __name__ == '__main__':
    main()
