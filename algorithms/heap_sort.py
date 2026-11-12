"""Heap Sort: build a max-heap, then repeatedly move the maximum to the end."""
from __future__ import annotations

from core.events import Tracer


def heap_sort(data: list[int], tracer: Tracer | None = None) -> list[int]:
    """Return a new sorted list. ``data`` is not modified."""
    tracer = tracer or Tracer()
    arr = list(data)
    n = len(arr)
    for start in range(n // 2 - 1, -1, -1):          # 1) build the max-heap
        _sift_down(arr, start, n, tracer)
    for end in range(n - 1, 0, -1):                  # 2) extract the maximum n-1 times
        tracer.swap(arr, 0, end, "{a} is the largest value in the heap, so it moves to position {j}")
        arr[0], arr[end] = arr[end], arr[0]
        tracer.mark_sorted(arr, [end], "{v} has reached its final position")
        _sift_down(arr, 0, end, tracer)
    tracer.finish(arr)
    return arr


def _sift_down(arr: list[int], root: int, size: int, tracer: Tracer) -> None:
    """Move ``arr[root]`` down until the max-heap property holds in ``arr[:size]``."""
    while True:
        left = 2 * root + 1
        if left >= size:
            return
        largest = left
        right = left + 1
        if right < size:
            tracer.compare(arr, left, right, "Heap Sort picks the larger of the two children")
            if arr[right] > arr[left]:
                largest = right
        tracer.compare(arr, largest, root, "the larger child is compared with its parent to keep the max-heap property")
        if arr[largest] > arr[root]:
            tracer.swap(arr, root, largest, "the child {b} is larger than its parent {a}, so they swap places")
            arr[root], arr[largest] = arr[largest], arr[root]
            root = largest
        else:
            return
