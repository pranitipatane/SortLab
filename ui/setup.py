"""Setup screen: choose an algorithm and an input before visualizing."""
from __future__ import annotations

import streamlit as st

from core.sorting_runner import ALGORITHMS, NORMAL
from data.algorithm_info import ALGORITHM_INFO
from ui.controls import CUSTOM, begin_visualizing, choose_algorithm, render_input_picker
from ui.explanations import SPEED_WORDS
from ui.visualizer import draw_array

TAGLINES: dict[str, str] = {
    "Bubble Sort": "Swaps neighbours in order",
    "Selection Sort": "Picks the smallest each pass",
    "Insertion Sort": "Grows a sorted section",
    "Merge Sort": "Divides, then merges",
    "Quick Sort": "Partitions around a pivot",
    "Heap Sort": "Pulls from a heap",
}


def _row_html(name: str) -> str:
    """Name, tagline and a badge with the average speed for one algorithm row."""
    average = ALGORITHM_INFO[name]["average"]
    word = SPEED_WORDS[average]
    return (f'<div class="sl-row"><div><div class="sl-row-name">{name}</div>'
            f'<div class="sl-row-tag">{TAGLINES[name]}</div></div>'
            f'<div class="sl-row-badge sl-row-badge-{word.lower()}">{average} · {word}</div></div>')


def _render_algorithm_list() -> None:
    """One clickable row per algorithm; the selected row is highlighted."""
    selected = st.session_state["algorithm"]
    with st.container(gap="xxsmall", key="algo_list"):
        for name in ALGORITHMS:
            key = "algo_row_selected" if name == selected else f"algo_row_{name.split()[0]}"
            with st.container(key=key):
                st.markdown(_row_html(name), unsafe_allow_html=True)
                st.button(f"Select {name}", key=f"card_{name}", on_click=choose_algorithm, args=(name,))


def _facts_html(name: str) -> str:
    """Average time, extra space and stability of the selected algorithm."""
    info = ALGORITHM_INFO[name]
    facts = (("Average time", info["average"]), ("Extra space", info["space"].rstrip("*")),
             ("Stable", "Yes" if info["stable"] else "No"))
    cells = "".join(f"<span>{label} <strong>{value}</strong></span>" for label, value in facts)
    return f'<div class="sl-facts">{cells}</div>'


def render_setup_page() -> None:
    """Algorithm list on the left; preview, input and Start on the right."""
    ss = st.session_state
    choose, configure = st.columns([5, 8], gap="large")

    with choose:
        st.header("New visualization", anchor=False)
        st.caption("Choose the algorithm you want to understand.")
        _render_algorithm_list()

    with configure:
        if not (ss["array_kind"] == CUSTOM and ss["custom_error"]):
            array = ss["array"]
            with st.container(key="setup_preview"):        # theme.py sizes this to the window
                st.pyplot(draw_array(array, [NORMAL] * len(array), height=6.4, compact=True))
        st.markdown(_facts_html(ss["algorithm"]), unsafe_allow_html=True)
        render_input_picker()
        st.button("Start visualizing", key="begin_visualizing", icon=":material/play_arrow:",
                  on_click=begin_visualizing, type="primary", width="stretch")
