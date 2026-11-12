"""Insertion Sort: grow a sorted section by inserting one key at a time.

This is the swap-based variant: the key moves left by adjacent swaps, which
makes every step easy to see in the visualization.
"""
from __future__ import annotations

from core.events import Tracer


def insertion_sort(data: list[int], tracer: Tracer | None = None) -> list[int]:
    """Return a new sorted list. ``data`` is not modified."""
    tracer = tracer or Tracer()
    arr = list(data)
    for i in range(1, len(arr)):
        j = i
        tracer.key(arr, j, "{v} is the current key; it will be inserted into the sorted section on its left")
        while j > 0:
            tracer.compare(arr, j - 1, j, "Insertion Sort checks whether the key must move further left")
            if arr[j - 1] > arr[j]:
                tracer.swap(arr, j - 1, j, "{b} is being moved left because it is smaller than {a}")
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                j -= 1
            else:
                break
    tracer.finish(arr)
    return arr
