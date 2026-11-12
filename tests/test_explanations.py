"""Tests for the How it works tab: its content and the code it displays."""
import inspect
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from core.sorting_runner import ALGORITHMS
from data.algorithm_info import ALGORITHM_INFO
from tests.common import CASES
from ui.explanations import SPEED_WORDS, readable_source

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def shown_code(name: str) -> str:
    return readable_source(inspect.getsource(sys.modules[ALGORITHMS[name].__module__]))


@pytest.mark.parametrize("name", ALGORITHMS)
def test_every_algorithm_has_detailed_plain_content(name):
    info = ALGORITHM_INFO[name]
    assert info["what"] and info["speed_note"] and info["memory"] and info["use_case"]
    assert info["pros"] and info["cons"] and len(info["steps"]) >= 4
    assert all(title and detail for title, detail in info["steps"])
    assert {info["best"], info["average"], info["worst"]} <= set(SPEED_WORDS)


@pytest.mark.parametrize("name", ALGORITHMS)
def test_displayed_code_hides_the_animation(name):
    assert "tracer" not in shown_code(name).lower()
    assert "import" not in shown_code(name)


@pytest.mark.parametrize("name", ALGORITHMS)
@pytest.mark.parametrize("case", CASES)
def test_displayed_code_really_sorts(name, case):
    namespace: dict = {}
    exec(shown_code(name), namespace)
    assert namespace[ALGORITHMS[name].__name__](list(CASES[case])) == sorted(CASES[case])


def test_empty_block_is_removed_with_its_tracer_line():
    source = '"""Doc."""\ndef f(a, tracer):\n    if a:\n        tracer.mark(a)\n    return a\n'
    assert readable_source(source) == "def f(a):\n    return a"


@pytest.fixture
def player() -> AppTest:
    app = AppTest.from_file(APP, default_timeout=30).run()
    app.button(key="begin_visualizing").click().run()
    assert not app.exception
    return app


def test_guide_shows_code_and_comparison_without_tabs(player):
    assert len(player.tabs) == 0
    assert "def bubble_sort(data: list[int]) -> list[int]:" in player.code[0].value
    assert len(player.dataframe) == 1


def test_code_can_switch_to_pseudocode(player):
    player.segmented_control(key="code_view").set_value("Pseudocode").run()
    assert not player.exception
    assert player.code[0].value == ALGORITHM_INFO["Bubble Sort"]["pseudocode"]
