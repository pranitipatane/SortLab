"""Tests for the beginner explanations shown beside the chart."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from core.coach import IDEAS, TAKEAWAYS, build_coaching
from core.sorting_runner import ALGORITHMS, PlaybackState, run_algorithm
from tests.common import CASES

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def coach(algorithm: str, data: list[int]):
    return build_coaching(algorithm, run_algorithm(algorithm, data).events)


def titles(algorithm: str, data: list[int]) -> list[str]:
    return [step.title for step in coach(algorithm, data)]


@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("case", CASES)
def test_every_event_gets_a_complete_explanation(algorithm, case):
    events = run_algorithm(algorithm, CASES[case]).events
    steps = build_coaching(algorithm, events)
    assert len(steps) == len(events)
    for step in steps:
        for text in (step.context, step.title, step.body, step.note, step.note_label):
            assert text and "{" not in text and "None" not in text


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_every_algorithm_has_an_idea_and_a_takeaway(algorithm):
    assert IDEAS[algorithm] and TAKEAWAYS[algorithm]


def test_bubble_sort_steps():
    steps = coach("Bubble Sort", [3, 1, 2])
    assert [s.title for s in steps] == [
        "3 and 1 are in the wrong order", "Swap 3 and 1", "3 and 2 are in the wrong order", "Swap 3 and 2",
        "3 is in its final place", "1 and 2 are already in order", "2 is in its final place",
        "The rest is already sorted", "All sorted"]
    assert steps[0].context == "Pass 1 of 2, comparison 1"
    assert steps[5].context == "Pass 2 of 2, comparison 1"


def test_bubble_sort_explains_equal_values():
    assert titles("Bubble Sort", [2, 2])[0] == "2 and 2 are equal"


def test_selection_sort_steps():
    steps = coach("Selection Sort", [2, 1])
    assert [s.title for s in steps] == [
        "Start with 2 as the smallest so far", "1 is smaller than 2", "1 is the new smallest",
        "Move 1 to the front of the unsorted part", "1 is in its final place", "All sorted"]
    assert steps[1].context == "Round 1 of 1, comparison 1 of 1"


def test_insertion_sort_steps():
    steps = coach("Insertion Sort", [2, 1])
    assert [s.title for s in steps] == ["Pick up 1", "2 is bigger than 1", "Slide 1 left past 2", "All sorted"]
    assert steps[0].context == "Inserting number 1 of 1"
    assert "very start" in steps[2].body
    assert titles("Insertion Sort", [1, 2])[1] == "2 has found its spot"


def test_merge_sort_steps_and_groups():
    steps = coach("Merge Sort", [3, 1])
    assert [s.title for s in steps] == ["1 is smaller than 3", "Place 1 next", "Copy 3 over", "All sorted"]
    assert steps[0].context == "Merge 1 of 1: combining 1 and 1 numbers"
    assert "from the right group" in steps[1].body
    assert steps[2].body.startswith("The right group has run out")


def test_quick_sort_steps():
    steps = coach("Quick Sort", [3, 1, 2])
    assert [s.title for s in steps] == [
        "Use 2 as the pivot", "3 is not smaller than the pivot 2", "1 is smaller than the pivot 2",
        "Move 1 to the smaller side", "Put the pivot 2 between the two sides", "2 is in its final place",
        "3 is on its own", "1 is on its own", "All sorted"]
    assert steps[1].context == "Partition 1 of 1, checked 1 of 2"
    assert steps[2].body.endswith("so it will move there.")


def test_quick_sort_says_when_a_small_value_is_already_in_place():
    assert coach("Quick Sort", [1, 3, 2])[1].body.endswith("and it is already there.")


def test_heap_sort_steps_and_phases():
    steps = coach("Heap Sort", [1, 3, 2])
    assert [s.title for s in steps] == [
        "3 is the bigger child", "Child 3 is bigger than parent 1", "Swap 3 up and 1 down",
        "Move the largest number, 3, to the end", "3 is in its final place", "Parent 2 is big enough",
        "Move the largest number, 2, to the end", "2 is in its final place", "All sorted"]
    assert steps[0].context == "Building the heap"
    assert steps[3].context == "Round 1 of 2: moving the largest"
    assert steps[5].context == "Round 1 of 2: repairing the heap"


def test_panel_follows_playback_from_introduction_to_takeaway():
    state = PlaybackState("Bubble Sort", [3, 1, 2])
    assert state.current_coaching().title == "Ready to start"
    assert state.current_coaching().note_label == "The big idea"
    state.step()
    assert state.current_coaching().title == "3 and 1 are in the wrong order"
    state.finish()
    assert state.current_coaching().title == "All sorted"
    assert state.current_coaching().note_label == "What to remember"
    state.reset()
    assert state.current_coaching().title == "Ready to start"


def test_step_panel_shows_the_coaching_in_the_app():
    app = AppTest.from_file(APP, default_timeout=30).run()
    app.button(key="begin_visualizing").click().run()
    assert not app.exception
    assert any("Why do this?" in block.value for block in app.markdown)
