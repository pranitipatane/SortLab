"""Quick Sort (Lomuto partition, last element as pivot).

The function recurses into the *smaller* partition and loops on the larger
one, so the recursion depth is at most O(log n) even on adversarial input
(sorted data still costs O(n^2) time, which is the point of the demo).
"""
from __future__ import annotations

from core.events import Tracer


def quick_sort(data: list[int], tracer: Tracer | None = None) -> list[int]:
    """Return a new sorted list. ``data`` is not modified."""
    tracer = tracer or Tracer()
    arr = list(data)
    _quick_sort(arr, 0, len(arr) - 1, tracer)
    tracer.finish(arr)
    return arr


def _quick_sort(arr: list[int], lo: int, hi: int, tracer: Tracer) -> None:
    while lo < hi:
        p = _partition(arr, lo, hi, tracer)
        if p - lo < hi - p:                  # recurse into the smaller side
            _quick_sort(arr, lo, p - 1, tracer)
            lo = p + 1
        else:
            _quick_sort(arr, p + 1, hi, tracer)
            hi = p - 1
    if lo == hi:
        tracer.mark_sorted(arr, [lo], "{v} is alone in its section, so it is in its final position")


def _partition(arr: list[int], lo: int, hi: int, tracer: Tracer) -> int:
    """Place the pivot (``arr[hi]``) in its final position and return that index."""
    pivot = arr[hi]
    tracer.begin_section(lo, hi + 1)
    tracer.pivot(arr, hi, "{v} is selected as the pivot")
    i = lo                                   # next slot for a value smaller than the pivot
    for j in range(lo, hi):
        tracer.compare(arr, j, hi, "Quick Sort compares every value with the pivot")
        if arr[j] < pivot:
            if i != j:
                tracer.swap(arr, i, j, "{b} is smaller than the pivot, so it moves into the left (smaller) section")
                arr[i], arr[j] = arr[j], arr[i]
            i += 1
    if i != hi:
        tracer.swap(arr, i, hi, "the pivot {b} is placed between the smaller and the larger values")
        arr[i], arr[hi] = arr[hi], arr[i]
    tracer.mark_sorted(arr, [i], "{v}, the pivot, is now in its final position")
    return i
