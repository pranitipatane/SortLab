"""Shared helpers for the algorithm tests."""
from __future__ import annotations

import random

from core.events import RecordingTracer, apply_event

CASES = {
    "empty": [],
    "one_element": [42],
    "sorted": [1, 2, 3, 4, 5, 6],
    "reverse": [9, 7, 5, 3, 1],
    "random": random.Random(7).sample(range(-500, 500), 60),
    "duplicates": [4, 2, 4, 1, 2, 4, 1, 1, 3],
    "all_equal": [5, 5, 5, 5],
    "negatives": [-3, 10, -20, 0, 7, -3, 15],
    "large_values": [10**12, -10**12, 999_999_999_999, 0, 10**9],
    "textbook": [5, 3, 8, 1, 2],
}


def check_sorts_correctly(func, data: list[int]) -> None:
    """The result is sorted, and the input list is left untouched."""
    original = list(data)
    result = func(data)
    assert result == sorted(original)          # built-in sort is allowed in tests only
    assert data == original
    assert result is not data


def check_events_replay(func, data: list[int]) -> None:
    """Replaying only swap/overwrite events on the input must produce the sorted output."""
    tracer = RecordingTracer()
    result = func(list(data), tracer)
    replay = list(data)
    for event in tracer.events:
        apply_event(event, replay)
    assert replay == result == sorted(data)
    assert tracer.events[-1].type == "complete"
    assert all(e.message for e in tracer.events)
