"""Tests for utilities, statistics, playback and benchmarking."""
import re
from pathlib import Path

import pytest

from core.sorting_runner import ALGORITHMS, PlaybackState, run_algorithm
from core.statistics import summarize
from utils.array_utils import DISTRIBUTIONS, generate_array
from utils.benchmark import run_benchmark
from utils.validation import parse_custom_array, validate_benchmark_sizes


# ---- validation --------------------------------------------------------
def test_parse_valid_input():
    result = parse_custom_array("64, 12, 90, 34, 7, 21")
    assert result.ok and result.values == [64, 12, 90, 34, 7, 21]


def test_parse_negative_and_brackets():
    assert parse_custom_array("[-5, 3, 0]").values == [-5, 3, 0]


@pytest.mark.parametrize("text", ["", "   ", None, "a, b", "1, 2, x", "1.5, 2", "5", "1, 99999999"])
def test_parse_rejects_bad_input(text):
    result = parse_custom_array(text)
    assert not result.ok and result.error.startswith("❌")


def test_parse_too_many_elements():
    assert not parse_custom_array(",".join(["1"] * 101)).ok


def test_benchmark_size_validation():
    assert validate_benchmark_sizes([10, 100]) is None
    assert validate_benchmark_sizes([]) is not None
    assert validate_benchmark_sizes([0]) is not None
    assert validate_benchmark_sizes([5000]) is not None


# ---- array generation --------------------------------------------------
@pytest.mark.parametrize("kind", DISTRIBUTIONS)
def test_generate_array_sizes(kind):
    for size in (1, 5, 30, 100):
        assert len(generate_array(size, kind, seed=1)) == size


def test_generate_array_shapes():
    assert generate_array(20, "Sorted", seed=3) == sorted(generate_array(20, "Sorted", seed=3))
    reverse = generate_array(20, "Reverse Sorted", seed=3)
    assert reverse == sorted(reverse, reverse=True)
    assert len(set(generate_array(50, "Many Duplicates", seed=3))) < 50
    assert generate_array(30, seed=5) == generate_array(30, seed=5)


def test_generate_array_rejects_bad_arguments():
    with pytest.raises(ValueError):
        generate_array(0)
    with pytest.raises(ValueError):
        generate_array(5, "Nope")


# ---- runner / statistics / playback -----------------------------------
@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_run_algorithm_matches_expected(name):
    data = generate_array(40, "Random", seed=11)
    run = run_algorithm(name, data)
    assert run.result == sorted(data)
    assert run.stats.operations == len(run.events)
    assert run.stats.comparisons > 0


def test_bubble_sort_known_counts():
    run = run_algorithm("Bubble Sort", [3, 2, 1])
    assert (run.stats.comparisons, run.stats.swaps) == (3, 3)


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_playback_reaches_sorted_state(name):
    data = generate_array(25, "Nearly Sorted", seed=2)
    state = PlaybackState(name, data)
    assert state.array == data and state.index == 0
    state.step(3)
    assert state.index <= 3
    state.finish()
    assert state.done and state.array == sorted(data)
    assert state.sorted_indices == set(range(len(data)))
    assert state.stats.comparisons == summarize(state.events).comparisons
    state.reset()
    assert state.array == data and state.index == 0 and state.stats.operations == 0


def test_playback_history_and_messages():
    state = PlaybackState("Bubble Sort", [3, 1, 2])
    assert "Ready" in state.current_message()
    state.step(2)
    assert len(state.history()) == 2 and state.history()[-1].startswith("→")
    assert "Comparing 3 and 1" in state.events[0].message


def test_playback_handles_tiny_arrays():
    for data in ([], [1]):
        state = PlaybackState("Quick Sort", data)
        state.finish()
        assert state.done and state.array == data


# ---- benchmark ---------------------------------------------------------
def test_benchmark_returns_real_measurements():
    df = run_benchmark(["Bubble Sort", "Merge Sort"], [10, 50], ["Random", "Sorted"], repeats=1)
    assert len(df) == 2 * 2 * 2
    assert (df["Time (ms)"] > 0).all()
    assert set(df["Distribution"]) == {"Random", "Sorted"}


# ---- source-code rules -------------------------------------------------
def test_algorithms_do_not_use_builtin_sorting():
    for path in Path(__file__).resolve().parent.parent.joinpath("algorithms").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert not re.search(r"(?<![\w.])sorted\(", source), path.name
        assert not re.search(r"\.sort\(", source), path.name
