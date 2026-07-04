from __future__ import annotations
import subprocess
import sys

COMMANDS = [
    [sys.executable, '-m', 'src.compute_tables'],
    [sys.executable, '-m', 'src.simulate_ci_scheduler'],
    [sys.executable, '-m', 'src.train_selector'],
    [sys.executable, '-m', 'src.plot_pareto'],
    [sys.executable, '-m', 'src.validate_artifact'],
]

for cmd in COMMANDS:
    print('$ ' + ' '.join(cmd))
    subprocess.check_call(cmd)
print('Artifact reproduction completed successfully.')
