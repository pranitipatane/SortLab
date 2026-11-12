"""Tests for the setup-first Visualizer flow, run through the real Streamlit app."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from core.sorting_runner import run_algorithm
from ui.setup import _row_html

APP = str(Path(__file__).resolve().parent.parent / "app.py")


@pytest.fixture
def app() -> AppTest:
    """A freshly started app, sitting on the setup screen."""
    return AppTest.from_file(APP, default_timeout=30).run()


def click(app: AppTest, key: str) -> None:
    """Press the button with ``key`` and fail on any app exception."""
    app.button(key=key).click().run()
    assert not app.exception


def test_app_opens_on_setup_with_only_navigation_in_sidebar(app):
    assert not app.exception
    assert app.session_state["vis_view"] == "setup"
    assert len(app.sidebar.button) == 0
    assert len(app.sidebar.slider) == 0


def test_navigation_shows_an_icon_and_keeps_the_plain_page_name(app):
    navigation = app.sidebar.radio(key="page")
    assert navigation.options[0] == ":material/bar_chart: Visualizer"
    assert navigation.value == "Visualizer"


def test_default_array_has_twenty_values(app):
    assert len(app.session_state["array"]) == 20


def test_algorithm_card_selects_algorithm(app):
    click(app, "card_Quick Sort")
    assert app.session_state["algorithm"] == "Quick Sort"


def test_algorithm_rows_show_a_speed_badge():
    assert "O(n²) · Slow" in _row_html("Bubble Sort")
    assert "O(n log n) · Fast" in _row_html("Merge Sort")


def test_start_opens_player_and_plays_from_the_beginning(app):
    click(app, "begin_visualizing")
    assert app.session_state["vis_view"] == "play"
    assert app.session_state["playing"] is True
    assert app.button(key="pb_toggle").label == "Pause"


def test_pause_stops_playback(app):
    click(app, "begin_visualizing")
    click(app, "pb_toggle")
    assert app.session_state["playing"] is False


def test_start_over_rewinds_and_plays(app):
    click(app, "begin_visualizing")
    click(app, "pb_finish")
    assert app.session_state["playback"].done
    click(app, "pb_start_over")
    assert app.session_state["playing"] is True
    assert app.session_state["playback"].index <= 1


def test_step_labels_use_values_not_positions():
    events = run_algorithm("Bubble Sort", [3, 1, 2]).events
    assert events[0].label == "Compare 3 and 1"
    assert next(e for e in events if e.type == "swap").label == "Swap 3 and 1"


def test_change_input_keeps_array_and_stops_playback(app):
    array = list(app.session_state["array"])
    click(app, "begin_visualizing")
    click(app, "change_input")
    assert app.session_state["vis_view"] == "setup"
    assert app.session_state["playing"] is False
    assert app.session_state["array"] == array


def test_switching_to_custom_starts_from_the_current_array(app):
    array = list(app.session_state["array"])
    app.segmented_control(key="array_kind").set_value("Custom").run()
    assert not app.exception
    assert app.text_input(key="custom_text").value == ", ".join(str(v) for v in array)


def test_invalid_custom_input_stays_on_setup_and_shows_error(app):
    app.segmented_control(key="array_kind").set_value("Custom").run()
    app.text_input(key="custom_text").set_value("1, x").run()
    click(app, "begin_visualizing")
    assert app.session_state["vis_view"] == "setup"
    assert len(app.error) == 1


def test_valid_custom_input_is_what_gets_visualized(app):
    app.segmented_control(key="array_kind").set_value("Custom").run()
    app.text_input(key="custom_text").set_value("9, 4, 7").run()
    click(app, "begin_visualizing")
    assert app.session_state["playback"].initial == [9, 4, 7]


def test_custom_text_is_remembered_after_switching_away(app):
    app.segmented_control(key="array_kind").set_value("Custom").run()
    app.text_input(key="custom_text").set_value("9, 4, 7").run()
    app.segmented_control(key="array_kind").set_value("Sorted").run()
    app.segmented_control(key="array_kind").set_value("Custom").run()
    assert app.session_state["array"] == [9, 4, 7]


def test_race_page_has_its_own_input_and_speed(app):
    app.sidebar.radio(key="page").set_value("Algorithm Race").run()
    assert not app.exception
    app.segmented_control(key="array_kind").set_value("Sorted").run()
    assert not app.exception
    assert app.session_state["array"] == sorted(app.session_state["array"])
    assert app.select_slider(key="speed").value == "Normal"
