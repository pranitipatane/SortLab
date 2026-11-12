"""Selection Sort: repeatedly select the smallest remaining element."""
from __future__ import annotations

from core.events import Tracer


def selection_sort(data: list[int], tracer: Tracer | None = None) -> list[int]:
    """Return a new sorted list. ``data`` is not modified."""
    tracer = tracer or Tracer()
    arr = list(data)
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        tracer.select(arr, min_idx, "{v} is currently the smallest value found in the unsorted section")
        for j in range(i + 1, n):
            tracer.compare(arr, j, min_idx, "Selection Sort looks for a value smaller than the current minimum")
            if arr[j] < arr[min_idx]:
                min_idx = j
                tracer.select(arr, min_idx, "{v} is the new smallest value found in the unsorted section")
        if min_idx != i:
            tracer.swap(arr, i, min_idx, "{b} is the smallest remaining value, so it is swapped into position {i}")
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        tracer.mark_sorted(arr, [i], "{v} has reached its final position")
    tracer.finish(arr)
    return arr
