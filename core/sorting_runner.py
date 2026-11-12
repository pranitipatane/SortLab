"""Runs algorithms and replays their events (the heart of the animation system).

Flow:  array -> run_algorithm() -> list[Event] -> PlaybackState.step() -> UI
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from algorithms import (bubble_sort, heap_sort, insertion_sort, merge_sort,
                        quick_sort, selection_sort)
from core.coach import Coaching, build_coaching, introduction
from core.events import (COMPARE, COMPLETE, KEY, MARK_SORTED, OVERWRITE, PIVOT, SELECT,
                         SWAP, Event, RecordingTracer, apply_event)
from core.statistics import Stats, summarize

SortFunction = Callable[..., list[int]]

ALGORITHMS: dict[str, SortFunction] = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}

# Visual states a bar can be in (see ui/visualizer.py for colours and patterns).
NORMAL, COMPARING, SWAPPING, OVERWRITING = "normal", "comparing", "swapping", "overwriting"
PIVOTING, SELECTED, KEYING, SORTED = "pivot", "selected", "key", "sorted"


@dataclass
class RunResult:
    """Everything produced by one full, recorded run of an algorithm."""

    algorithm: str
    events: list[Event]
    stats: Stats
    result: list[int]


def run_algorithm(name: str, data: list[int]) -> RunResult:
    """Run ``name`` on a copy of ``data`` and record every event."""
    tracer = RecordingTracer()
    result = ALGORITHMS[name](list(data), tracer)
    return RunResult(name, tracer.events, summarize(tracer.events), result)


class PlaybackState:
    """A cursor over an algorithm's event list.

    It keeps the *current* array, statistics and highlight markers, so moving
    forward by one event is O(1). Stored in ``st.session_state`` so a Streamlit
    rerun never restarts the sort by accident.
    """

    def __init__(self, algorithm: str, data: list[int]) -> None:
        self.algorithm = algorithm
        self.initial = list(data)
        run = run_algorithm(algorithm, data)
        self.events = run.events
        self.expected = run.result
        self._coaching: list[Coaching] | None = None    # written the first time it is shown
        self.reset()

    # --- state ---------------------------------------------------------
    def reset(self) -> None:
        """Rewind to the original, unsorted array."""
        self.array = list(self.initial)
        self.sorted_indices: set[int] = set()
        self.stats = Stats()
        self.index = 0
        self.pivot: int | None = None
        self.selected: int | None = None
        self.key: int | None = None
        self.last_event: Event | None = None

    @property
    def total(self) -> int:
        return len(self.events)

    @property
    def done(self) -> bool:
        return self.index >= self.total

    @property
    def progress(self) -> float:
        return 1.0 if self.total == 0 else self.index / self.total

    # --- stepping ------------------------------------------------------
    def step(self, count: int = 1) -> None:
        """Advance by up to ``count`` events."""
        events, start = self.events, self.index
        end = min(len(events), start + count)
        for position in range(start, end):
            self._apply(events[position])
        self.index = max(start, end)

    def finish(self) -> None:
        """Jump straight to the end."""
        self.step(self.total - self.index)

    def _apply(self, event: Event) -> None:
        apply_event(event, self.array)
        self.stats.apply(event)
        self.last_event = event
        kind = event.type
        if kind == SWAP:                      # markers travel with their value
            i, j = event.indices
            for name in ("pivot", "selected", "key"):
                pos = getattr(self, name)
                if pos == i:
                    setattr(self, name, j)
                elif pos == j:
                    setattr(self, name, i)
        elif kind == PIVOT:
            self.pivot = event.indices[0]
        elif kind == SELECT:
            self.selected = event.indices[0]
        elif kind == KEY:
            self.key = event.indices[0]
        elif kind == MARK_SORTED:
            self.sorted_indices.update(event.indices)
            self.pivot = self.selected = self.key = None
        elif kind == COMPLETE:
            self.sorted_indices = set(range(len(self.array)))
            self.pivot = self.selected = self.key = None

    # --- views for the UI -----------------------------------------------
    def bar_states(self) -> list[str]:
        """Visual state of every bar at the current step."""
        states = [SORTED if i in self.sorted_indices else NORMAL for i in range(len(self.array))]
        for pos, state in ((self.pivot, PIVOTING), (self.selected, SELECTED), (self.key, KEYING)):
            if pos is not None:
                states[pos] = state
        event = self.last_event
        if event is not None:
            active = {COMPARE: COMPARING, SWAP: SWAPPING, OVERWRITE: OVERWRITING}.get(event.type)
            if active:
                markers = (PIVOTING, SELECTED, KEYING)
                for i in event.indices:
                    if event.type == COMPARE and states[i] in markers:
                        continue          # keep the pivot / minimum / key visible while it is compared
                    states[i] = active
        return states

    def current_message(self) -> str:
        if self.last_event is None:
            return "Ready. Press Start race to begin."
        return self.last_event.message

    def current_coaching(self) -> Coaching:
        """The beginner explanation for the current step."""
        if self.last_event is None:
            return introduction(self.algorithm, self.total)
        if self._coaching is None:
            self._coaching = build_coaching(self.algorithm, self.events)
        return self._coaching[self.index - 1]

    def history(self, limit: int = 8) -> list[str]:
        """Last ``limit`` operations; the newest one is marked with an arrow."""
        start = max(0, self.index - limit)
        lines = [f"✓ {e.label}" for e in self.events[start:self.index]]
        if lines:
            lines[-1] = "→ " + lines[-1][2:]
        return lines
