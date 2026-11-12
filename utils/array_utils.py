"""Array generation for the visualizer, comparison mode and benchmarks."""
from __future__ import annotations

import numpy as np

MIN_SIZE = 5
MAX_SIZE = 100
DEFAULT_SIZE = 20

DISTRIBUTIONS = ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted", "Many Duplicates"]


def generate_array(size: int, kind: str = "Random", seed: int | None = None,
                   max_value: int = 100) -> list[int]:
    """Create a list of ``size`` positive integers.

    Args:
        size: Number of elements (at least 1).
        kind: One of ``DISTRIBUTIONS``.
        seed: Optional seed for reproducible results.
        max_value: Largest value that can appear.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    if kind not in DISTRIBUTIONS:
        raise ValueError(f"unknown array type: {kind}")
    rng = np.random.default_rng(seed)
    max_value = max(max_value, size)
    candidates = np.arange(1, max_value + 1)

    if kind == "Many Duplicates":
        distinct = max(3, size // 5)
        pool = rng.choice(candidates, size=min(distinct, max_value), replace=False)
        return rng.choice(pool, size=size).tolist()

    values = rng.choice(candidates, size=size, replace=size > max_value)
    values = np.sort(values)                 # NumPy sort only builds test data, not a SortLab algorithm
    if kind == "Reverse Sorted":
        values = values[::-1]
    elif kind == "Nearly Sorted":            # np.sort returned a fresh, writable array
        for _ in range(max(1, size // 20)):  # a few random swaps
            a, b = rng.integers(0, size, size=2)
            values[a], values[b] = values[b], values[a]
    elif kind == "Random":
        values = rng.permutation(values)
    return values.tolist()                   # "Sorted" is returned as generated
