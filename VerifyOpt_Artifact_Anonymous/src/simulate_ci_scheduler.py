from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import heapq
import pandas as pd
from .utils import ROOT, ensure_results

@dataclass(order=True)
class RunningTask:
    finish_time: float
    worker_id: int
    task_id: str = field(compare=False)
    status: str = field(compare=False)


def choose_runtime(row: pd.Series, policy: str) -> tuple[str, float, str]:
    """Return mode, runtime seconds, and status for a simplified schedule."""
    if policy == 'fixed_fast':
        mode = 'fast'
    elif policy == 'fixed_precise':
        mode = 'precise'
    elif policy == 'rule':
        mode = 'precise' if row['cyclomatic_complexity'] > 15 or row['pointer_use'] == 1 and row['property_type'] in ('memory_safety','nullness') else 'fast'
    else:
        high_risk = row['criticality_flag'] == 1 or row['previous_timeout'] == 1
        simple = row['loc'] < 500 and row['cyclomatic_complexity'] < 10 and row['macro_expansion_size'] < 2500
        mode = 'precise' if high_risk or not simple else 'fast'
    status = row[f'{mode}_status']
    runtime = 10.0 if (mode == 'fast' and status == 'timeout') else 300.0 if (mode == 'precise' and status == 'timeout') else min(float(row['previous_runtime_s']) * (1 if mode == 'fast' else 12), 300.0)
    return mode, max(0.2, runtime), status


def simulate(tasks: pd.DataFrame, budget_h: float, workers: int = 8, policy: str = 'verifyopt') -> dict:
    """Budget-aware wall-clock scheduler with anti-starvation ordering.

    Tasks predicted to be fast are interleaved with high-risk tasks so that
    long precise jobs do not starve quick proof obligations.
    """
    budget_s = budget_h * 3600
    task_rows = []
    for _, row in tasks.iterrows():
        mode, runtime, status = choose_runtime(row, policy)
        priority = (0 if mode == 'fast' else 1, -int(row['criticality_flag']), runtime)
        task_rows.append((priority, row['task_id'], mode, runtime, status))
    task_rows.sort(key=lambda x: x[0])

    queued = list(task_rows)
    running: list[RunningTask] = []
    now = 0.0
    worker_ids = list(range(workers))
    completed = {'verified': 0, 'defect': 0, 'timeout': 0, 'unknown': 0, 'ticket': 0}

    while (queued or running) and now <= budget_s:
        while worker_ids and queued:
            _, task_id, mode, runtime, status = queued.pop(0)
            if now + runtime > budget_s:
                completed['timeout'] += 1
                continue
            wid = worker_ids.pop(0)
            heapq.heappush(running, RunningTask(now + runtime, wid, task_id, status))
        if not running:
            break
        done = heapq.heappop(running)
        now = done.finish_time
        worker_ids.append(done.worker_id)
        completed[done.status] = completed.get(done.status, 0) + 1
    for _ in queued:
        completed['timeout'] += 1
    return {'budget_h': budget_h, 'policy': policy, 'verified_properties': completed.get('verified',0), **completed}


def main() -> None:
    tasks = pd.read_csv(ROOT / 'data' / 'example_anonymized' / 'task_features.csv')
    rows = []
    for policy in ['fixed_fast','fixed_precise','rule','verifyopt']:
        for budget in [1,2,4,8]:
            rows.append(simulate(tasks, budget_h=budget, policy=policy))
    out = ensure_results() / 'scheduler_demo.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'wrote {out.relative_to(ROOT)}')

if __name__ == '__main__':
    main()
