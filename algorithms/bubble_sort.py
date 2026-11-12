"""Bubble Sort: repeatedly swap neighbouring elements that are out of order."""
from __future__ import annotations

from core.events import Tracer


def bubble_sort(data: list[int], tracer: Tracer | None = None) -> list[int]:
    """Return a new sorted list. ``data`` is not modified."""
    tracer = tracer or Tracer()
    arr = list(data)
    n = len(arr)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            tracer.compare(arr, i, i + 1, "Bubble Sort checks adjacent elements")
            if arr[i] > arr[i + 1]:
                tracer.swap(arr, i, i + 1, "{a} is greater than {b}, so the two values are swapped")
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        tracer.mark_sorted(arr, [end], "{v} has reached its final position")
        if not swapped:  # a pass without swaps means everything is in order
            tracer.mark_sorted(arr, range(end), "No swaps happened in this pass, so the rest is already sorted")
            break
    tracer.finish(arr)
    return arr
