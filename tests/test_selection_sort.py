"""Tests for selection_sort."""
import pytest

from algorithms.selection_sort import selection_sort
from core.events import RecordingTracer
from tests.common import CASES, check_events_replay, check_sorts_correctly


@pytest.mark.parametrize("name", list(CASES))
def test_sorts_correctly(name):
    check_sorts_correctly(selection_sort, CASES[name])


@pytest.mark.parametrize("name", list(CASES))
def test_events_replay_to_sorted_result(name):
    check_events_replay(selection_sort, CASES[name])


def test_textbook_example():
    assert selection_sort([5, 3, 8, 1, 2]) == [1, 2, 3, 5, 8]


def test_statistics_come_from_events():
    tracer = RecordingTracer()
    selection_sort([3, 1, 2], tracer)
    kinds = [e.type for e in tracer.events]
    assert "compare" in kinds and kinds[-1] == "complete"


def test_at_most_n_minus_one_swaps():
    tracer = RecordingTracer()
    selection_sort([9, 8, 7, 6, 5, 4, 3, 2, 1], tracer)
    assert sum(e.type == "swap" for e in tracer.events) <= 8
