"""Session state, navigation, the shared input picker and the playback bar."""
from __future__ import annotations

import streamlit as st

from core.sorting_runner import PlaybackState
from utils.array_utils import DEFAULT_SIZE, DISTRIBUTIONS, MAX_SIZE, MIN_SIZE, generate_array
from utils.validation import parse_custom_array

PAGES = ["Visualizer", "Compare Algorithms", "Algorithm Race", "Benchmark", "Interview Mode", "Learn"]
PAGE_ICONS = {"Visualizer": "bar_chart", "Compare Algorithms": "compare_arrows", "Algorithm Race": "flag",
              "Benchmark": "speed", "Interview Mode": "chat_bubble", "Learn": "menu_book"}
BRAND_HTML = ('<div class="sl-brand"><div class="sl-logo"><span></span><span></span><span></span></div>'
              '<div><div class="sl-brand-name">SortLab</div>'
              '<div class="sl-brand-tag">Learn sorting step by step</div></div></div>')

# speed name -> (seconds between refreshes, operations applied per refresh)
SPEEDS: dict[str, tuple[float, int]] = {
    "Explain": (3.0, 1),               # long enough to read each step's reason
    "Slow": (0.8, 1),
    "Normal": (0.2, 1),
    "Fast": (0.05, 1),
    "Very Fast": (0.05, 10),
}

CUSTOM = "Custom"
INPUT_KINDS = [*DISTRIBUTIONS, CUSTOM]
_SHORT_KIND_LABELS = {"Reverse Sorted": "Reversed", "Nearly Sorted": "Nearly sorted", "Many Duplicates": "Duplicates"}

# The Visualizer page has two views: choose the input first, then watch it run.
VIEW_SETUP, VIEW_PLAY = "setup", "play"

# Widget-backed keys. Streamlit forgets a widget's value when the widget is not
# drawn (e.g. on another page), so we re-assign them on every run.
_WIDGET_KEYS = ("page", "array_size", "array_kind", "algorithm", "speed", "custom_text", "race_a", "race_b")


def init_session() -> None:
    """Create default session values once and keep widget values alive."""
    ss = st.session_state
    defaults = {"page": PAGES[0], "array_size": DEFAULT_SIZE, "array_kind": "Random",
                "algorithm": "Bubble Sort", "speed": "Normal", "custom_text": "",
                "custom_error": "", "playing": False, "race_a": "Bubble Sort",
                "race_b": "Quick Sort", "race_playing": False, "vis_view": VIEW_SETUP}
    for key, value in defaults.items():
        ss.setdefault(key, value)
    if "array" not in ss:
        ss["array"] = generate_array(ss["array_size"], ss["array_kind"])
    for key in _WIDGET_KEYS:
        ss[key] = ss[key]
    ensure_playback()


def ensure_playback() -> PlaybackState:
    """Keep exactly ONE PlaybackState; rebuild it only if algorithm or array changed."""
    ss = st.session_state
    signature = (ss["algorithm"], tuple(ss["array"]))
    if ss.get("playback_sig") != signature:
        ss["playback"] = PlaybackState(ss["algorithm"], ss["array"])
        ss["playback_sig"] = signature
        ss["playing"] = False          # changing algorithm/array always stops playback
    return ss["playback"]


# ---- input callbacks (run before the script reruns) ------------------------
def _regenerate() -> None:
    """Replace the array with a new generated one of the chosen size and type."""
    ss = st.session_state
    ss["array"] = generate_array(ss["array_size"], ss["array_kind"])
    ss["custom_error"] = ""
    ss["playing"] = False


def _apply_custom() -> None:
    """Use the typed numbers if they are valid; otherwise record a friendly error."""
    ss = st.session_state
    result = parse_custom_array(ss["custom_text"])
    if result.ok:
        ss["array"] = result.values
        ss["custom_error"] = ""
        ss["playing"] = False
    else:
        ss["custom_error"] = result.error


def _on_kind_change() -> None:
    """Switch input type. Custom starts from the current bars; typed text is remembered."""
    ss = st.session_state
    if ss["array_kind"] == CUSTOM:
        if not ss["custom_text"].strip():
            ss["custom_text"] = ", ".join(str(value) for value in ss["array"])
        _apply_custom()
    else:
        _regenerate()


def choose_algorithm(name: str) -> None:
    """Select the algorithm named on a setup card."""
    st.session_state["algorithm"] = name


# ---- moving between the two views ------------------------------------------
def begin_visualizing() -> None:
    """Leave setup and play from the first step, unless a custom input is invalid."""
    ss = st.session_state
    if ss["array_kind"] == CUSTOM:
        _apply_custom()
        if ss["custom_error"]:
            return                     # stay on setup; the error is shown there
    ensure_playback().reset()
    ss["playing"] = True
    ss["vis_view"] = VIEW_PLAY


def back_to_setup() -> None:
    """Stop playback and return to setup. The array and algorithm are kept."""
    ss = st.session_state
    ss["playing"] = False
    ss["vis_view"] = VIEW_SETUP


# ---- playback callbacks ----------------------------------------------------
def _toggle_play() -> None:
    """Play or pause. Does nothing once the sort has finished."""
    ss = st.session_state
    ss["playing"] = not ss["playing"] and not ss["playback"].done


def _step() -> None:
    """Pause and move forward exactly one operation."""
    st.session_state["playing"] = False
    st.session_state["playback"].step(1)


def _finish() -> None:
    """Pause and jump to the sorted result."""
    st.session_state["playing"] = False
    st.session_state["playback"].finish()


def _start_over() -> None:
    """Rewind and play again from the first step."""
    st.session_state["playback"].reset()
    st.session_state["playing"] = True


# ---- rendering -------------------------------------------------------------
def render_navigation() -> str:
    """Page selector in the sidebar; returns the chosen page."""
    st.sidebar.markdown(BRAND_HTML, unsafe_allow_html=True)
    st.sidebar.radio("Navigate", PAGES, key="page", label_visibility="collapsed", width="stretch",
                     format_func=lambda page: f":material/{PAGE_ICONS[page]}: {page}")
    return st.session_state["page"]


def render_input_picker() -> None:
    """Choose the input array. Shared by the Visualizer setup and the Race page."""
    ss = st.session_state
    st.segmented_control("Input type", INPUT_KINDS, key="array_kind", required=True,
                         format_func=lambda kind: _SHORT_KIND_LABELS.get(kind, kind),
                         on_change=_on_kind_change, width="stretch", wrap=True)
    if ss["array_kind"] == CUSTOM:
        st.text_input("Your numbers", key="custom_text", placeholder="64, 12, 90, 34, 7, 21",
                      on_change=_apply_custom,
                      help="Whole numbers separated by commas (2–100 values, negatives allowed).")
        if ss["custom_error"]:
            st.error(ss["custom_error"])
        else:
            st.caption(f"{len(ss['array'])} values")
    else:
        size, refresh = st.columns([3, 1], vertical_alignment="bottom")
        size.slider("Array size", MIN_SIZE, MAX_SIZE, key="array_size", on_change=_regenerate)
        refresh.button("New values", icon=":material/refresh:", on_click=_regenerate, width="stretch")


def render_playback_bar(pb: PlaybackState) -> None:
    """Video-player style controls, drawn directly under the chart."""
    ss = st.session_state
    started = 0 < pb.index < pb.total
    play_label = "Pause" if ss["playing"] else ("Resume" if started else "Play")
    play_icon = ":material/pause:" if ss["playing"] else ":material/play_arrow:"
    with st.container(key="playback_bar"):
        play, step, finish, again, speed = st.columns([1.2, 1, 1, 1.2, 2.6], vertical_alignment="bottom")
        play.button(play_label, key="pb_toggle", icon=play_icon, on_click=_toggle_play, disabled=pb.done,
                    type="primary", width="stretch")
        step.button("Step", key="pb_step", icon=":material/skip_next:", on_click=_step, disabled=pb.done,
                    width="stretch")
        finish.button("Finish", key="pb_finish", icon=":material/last_page:", on_click=_finish, disabled=pb.done,
                      width="stretch")
        again.button("Start over", key="pb_start_over", icon=":material/replay:", on_click=_start_over,
                     disabled=pb.index == 0, width="stretch")
        speed.select_slider("Speed", options=list(SPEEDS), key="speed",
                            help="Explain holds each step for about 3 seconds so you can read why it happened.")
