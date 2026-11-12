"""Event model shared by every sorting algorithm and the UI.

Algorithms never talk to Streamlit. Instead they report what they do to a
*tracer*:

* ``Tracer``          - does nothing (used for benchmarks and plain sorting).
* ``RecordingTracer`` - stores an ``Event`` for each operation (used by the
                        visualizer, comparison mode and the race).

Because the algorithm code is identical in both cases, the numbers shown in the
UI come from the same code that is benchmarked and tested.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

COMPARE = "compare"
SWAP = "swap"
OVERWRITE = "overwrite"
PIVOT = "pivot"
SELECT = "select"          # current minimum in Selection Sort
KEY = "key"                # current key in Insertion Sort
MARK_SORTED = "mark_sorted"
COMPLETE = "complete"

EVENT_TYPES = (COMPARE, SWAP, OVERWRITE, PIVOT, SELECT, KEY, MARK_SORTED, COMPLETE)


@dataclass(frozen=True, slots=True)
class Event:
    """One step of an algorithm.

    Attributes:
        type: One of ``EVENT_TYPES``.
        indices: Array positions involved in the step.
        message: Plain-English explanation ("Why this step?").
        values: Values involved (compared values, or the new value of an overwrite).
        accesses: Number of main-array reads/writes this step costs.
        section: Part of the array being worked on as ``(lo, hi, mid)``, with ``hi``
            exclusive and ``mid`` set only by Merge Sort. ``None`` for other algorithms.
    """

    type: str
    indices: tuple[int, ...] = ()
    message: str = ""
    values: tuple[int, ...] = ()
    accesses: int = 0
    section: tuple[int, int, int | None] | None = None

    @property
    def label(self) -> str:
        """Short label used in the operation history."""
        idx = self.indices
        if self.type == COMPARE:
            return f"Compare {self.values[0]} and {self.values[1]}"
        if self.type == SWAP:
            return f"Swap {self.values[0]} and {self.values[1]}"
        if self.type == OVERWRITE:
            return f"Write {self.values[0]} to position {idx[0]}"
        if self.type == PIVOT:
            return f"Choose {self.values[0]} as the pivot"
        if self.type == SELECT:
            return f"{self.values[0]} is the new minimum"
        if self.type == KEY:
            return f"Pick {self.values[0]} as the key"
        if self.type == MARK_SORTED:
            if len(idx) == 1:
                return f"Position {idx[0]} is final"
            return f"{len(idx)} positions are final"
        return "Sorting complete"


class Tracer:
    """A tracer that ignores everything (zero bookkeeping)."""

    def compare(self, arr: Sequence[int], i: int, j: int, why: str) -> None: ...
    def compare_values(self, a: int, b: int, where: int, why: str) -> None: ...
    def swap(self, arr: Sequence[int], i: int, j: int, why: str) -> None: ...
    def overwrite(self, arr: Sequence[int], i: int, new: int, why: str) -> None: ...
    def pivot(self, arr: Sequence[int], i: int, why: str) -> None: ...
    def select(self, arr: Sequence[int], i: int, why: str) -> None: ...
    def key(self, arr: Sequence[int], i: int, why: str) -> None: ...
    def mark_sorted(self, arr: Sequence[int], indices: Iterable[int], why: str) -> None: ...
    def read(self, count: int) -> None: ...
    def begin_section(self, lo: int, hi: int, mid: int | None = None) -> None: ...
    def finish(self, arr: Sequence[int]) -> None: ...


class RecordingTracer(Tracer):
    """Stores one ``Event`` per reported operation.

    ``why`` strings may contain placeholders such as ``{a}``, ``{b}``, ``{v}``;
    they are filled in here, so algorithms only pass constant strings (cheap).
    """

    def __init__(self) -> None:
        self.events: list[Event] = []
        self._pending_reads = 0
        self._section: tuple[int, int, int | None] | None = None

    def _emit(self, kind: str, indices: tuple[int, ...], message: str,
              values: tuple[int, ...] = (), accesses: int = 0) -> None:
        total = accesses + self._pending_reads
        self._pending_reads = 0
        self.events.append(Event(kind, indices, message, values, total, self._section))

    def begin_section(self, lo, hi, mid=None):
        self._section = (lo, hi, mid)

    def compare(self, arr, i, j, why):
        a, b = arr[i], arr[j]
        self._emit(COMPARE, (i, j), f"Comparing {a} and {b} because {why.format(a=a, b=b)}.",
                   (a, b), 2)

    def compare_values(self, a, b, where, why):
        self._emit(COMPARE, (where,),
                   f"Comparing {a} and {b} because {why.format(a=a, b=b)}.", (a, b), 2)

    def swap(self, arr, i, j, why):
        a, b = arr[i], arr[j]
        text = why.format(a=a, b=b, i=i, j=j)
        self._emit(SWAP, (i, j), text[0].upper() + text[1:] + ".", (a, b), 4)

    def overwrite(self, arr, i, new, why):
        text = why.format(old=arr[i], new=new, i=i)
        self._emit(OVERWRITE, (i,), text[0].upper() + text[1:] + ".", (new,), 1)

    def pivot(self, arr, i, why):
        self._emit(PIVOT, (i,), why.format(v=arr[i], i=i) + ".", (arr[i],), 1)

    def select(self, arr, i, why):
        self._emit(SELECT, (i,), why.format(v=arr[i], i=i) + ".", (arr[i],), 1)

    def key(self, arr, i, why):
        self._emit(KEY, (i,), why.format(v=arr[i], i=i) + ".", (arr[i],), 1)

    def mark_sorted(self, arr, indices, why):
        idx = tuple(indices)
        if not idx:
            return
        text = why.format(v=arr[idx[0]]) if len(idx) == 1 else why
        self._emit(MARK_SORTED, idx, text + ".", tuple(arr[i] for i in idx))

    def read(self, count):
        self._pending_reads += count

    def finish(self, arr):
        self._emit(COMPLETE, (), "Sorting complete: every element is in its final position.")


def apply_event(event: Event, array: list[int]) -> None:
    """Replay the *data change* of an event on ``array`` (swap / overwrite only)."""
    if event.type == SWAP:
        i, j = event.indices
        array[i], array[j] = array[j], array[i]
    elif event.type == OVERWRITE:
        array[event.indices[0]] = event.values[0]
