"""Tests for bubble_sort."""
import pytest

from algorithms.bubble_sort import bubble_sort
from core.events import RecordingTracer
from tests.common import CASES, check_events_replay, check_sorts_correctly


@pytest.mark.parametrize("name", list(CASES))
def test_sorts_correctly(name):
    check_sorts_correctly(bubble_sort, CASES[name])


@pytest.mark.parametrize("name", list(CASES))
def test_events_replay_to_sorted_result(name):
    check_events_replay(bubble_sort, CASES[name])


def test_textbook_example():
    assert bubble_sort([5, 3, 8, 1, 2]) == [1, 2, 3, 5, 8]


def test_statistics_come_from_events():
    tracer = RecordingTracer()
    bubble_sort([3, 1, 2], tracer)
    kinds = [e.type for e in tracer.events]
    assert "compare" in kinds and kinds[-1] == "complete"


def test_sorted_input_takes_one_pass():
    tracer = RecordingTracer()
    bubble_sort(list(range(10)), tracer)
    assert sum(e.type == "compare" for e in tracer.events) == 9   # O(n) best case
    assert not any(e.type == "swap" for e in tracer.events)
