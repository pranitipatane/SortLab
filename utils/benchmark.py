"""Benchmarking with real algorithm executions (no animation involved)."""
from __future__ import annotations

import time
from typing import Callable, Sequence

import pandas as pd

from core.sorting_runner import ALGORITHMS
from utils.array_utils import generate_array

COLUMNS = ["Distribution", "Size", "Algorithm", "Time (ms)"]


def time_algorithm(func: Callable[[list[int]], list[int]], data: Sequence[int], repeats: int = 3) -> float:
    """Best-of-``repeats`` wall-clock time in milliseconds, using ``time.perf_counter()``."""
    best = float("inf")
    for _ in range(max(1, repeats)):
        sample = list(data)                  # every run gets its own copy of the same input
        start = time.perf_counter()
        func(sample)
        best = min(best, time.perf_counter() - start)
    return best * 1000.0


def run_benchmark(algorithms: Sequence[str], sizes: Sequence[int], distributions: Sequence[str],
                  repeats: int = 3, seed: int = 42,
                  on_progress: Callable[[float], None] | None = None) -> pd.DataFrame:
    """Time each algorithm on the *same* input for every (distribution, size) pair."""
    rows = []
    total = max(1, len(algorithms) * len(sizes) * len(distributions))
    done = 0
    for distribution in distributions:
        for size in sizes:
            data = generate_array(size, distribution, seed=seed, max_value=1000)
            for name in algorithms:
                rows.append({"Distribution": distribution, "Size": size, "Algorithm": name,
                             "Time (ms)": time_algorithm(ALGORITHMS[name], data, repeats)})
                done += 1
                if on_progress:
                    on_progress(done / total)
    return pd.DataFrame(rows, columns=COLUMNS)
