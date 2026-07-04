from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
AGG = DATA / 'aggregate'
RESULTS = ROOT / 'results' / 'generated'


def ensure_results() -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    return RESULTS


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(AGG / name)


def write(df: pd.DataFrame, name: str) -> None:
    out = ensure_results() / name
    df.to_csv(out, index=False)
