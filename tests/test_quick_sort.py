"""Tests for quick_sort."""
import pytest

from algorithms.quick_sort import quick_sort
from core.events import RecordingTracer
from tests.common import CASES, check_events_replay, check_sorts_correctly


@pytest.mark.parametrize("name", list(CASES))
def test_sorts_correctly(name):
    check_sorts_correctly(quick_sort, CASES[name])


@pytest.mark.parametrize("name", list(CASES))
def test_events_replay_to_sorted_result(name):
    check_events_replay(quick_sort, CASES[name])


def test_textbook_example():
    assert quick_sort([5, 3, 8, 1, 2]) == [1, 2, 3, 5, 8]


def test_statistics_come_from_events():
    tracer = RecordingTracer()
    quick_sort([3, 1, 2], tracer)
    kinds = [e.type for e in tracer.events]
    assert "compare" in kinds and kinds[-1] == "complete"


def test_deep_sorted_input_does_not_hit_recursion_limit():
    data = list(range(1500))                      # worst case for a last-element pivot
    assert quick_sort(data) == data


def test_pivot_events_are_emitted():
    tracer = RecordingTracer()
    quick_sort([3, 1, 2, 5, 4], tracer)
    assert any(e.type == "pivot" for e in tracer.events)
