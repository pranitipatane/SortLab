"""Merge Sort: split in halves, sort each half, merge the two sorted halves."""
from __future__ import annotations

from core.events import Tracer


def merge_sort(data: list[int], tracer: Tracer | None = None) -> list[int]:
    """Return a new sorted list. ``data`` is not modified."""
    tracer = tracer or Tracer()
    arr = list(data)
    _sort(arr, 0, len(arr), tracer)
    tracer.finish(arr)
    return arr


def _sort(arr: list[int], lo: int, hi: int, tracer: Tracer) -> None:
    """Sort ``arr[lo:hi]`` (hi is exclusive)."""
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    _sort(arr, lo, mid, tracer)
    _sort(arr, mid, hi, tracer)
    _merge(arr, lo, mid, hi, tracer)


def _merge(arr: list[int], lo: int, mid: int, hi: int, tracer: Tracer) -> None:
    """Merge the sorted runs ``arr[lo:mid]`` and ``arr[mid:hi]``."""
    tracer.begin_section(lo, hi, mid)
    left, right = arr[lo:mid], arr[mid:hi]   # auxiliary copies (this is the O(n) extra space)
    tracer.read(hi - lo)
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        tracer.compare_values(left[i], right[j], k, "Merge Sort takes the smaller front value of the two sorted runs")
        if left[i] <= right[j]:              # <= keeps equal values in order (stable)
            tracer.overwrite(arr, k, left[i], "{new} (left run) is smaller or equal, so it is written to position {i}")
            arr[k] = left[i]
            i += 1
        else:
            tracer.overwrite(arr, k, right[j], "{new} (right run) is smaller, so it is written to position {i}")
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        tracer.overwrite(arr, k, left[i], "the right run is used up, so {new} is copied from the left run to position {i}")
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        tracer.overwrite(arr, k, right[j], "the left run is used up, so {new} is copied from the right run to position {i}")
        arr[k] = right[j]
        j += 1
        k += 1
