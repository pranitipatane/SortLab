"""Algorithm Race page: two algorithms advance side by side, operation by operation."""
from __future__ import annotations

import streamlit as st

from core.sorting_runner import ALGORITHMS, PlaybackState
from ui.controls import SPEEDS, render_input_picker
from ui.visualizer import draw_array


def _new_race() -> None:
    ss = st.session_state
    ss["race"] = (PlaybackState(ss["race_a"], ss["array"]), PlaybackState(ss["race_b"], ss["array"]))
    ss["race_playing"] = False


def _toggle() -> None:
    st.session_state["race_playing"] = not st.session_state["race_playing"]


def _race_view() -> None:
    ss = st.session_state
    states: tuple[PlaybackState, PlaybackState] = ss["race"]
    if ss["race_playing"]:
        batch = SPEEDS[ss["speed"]][1]
        for pb in states:
            pb.step(batch)
        if all(pb.done for pb in states):
            ss["race_playing"] = False
            st.rerun()
    cols = st.columns(2)
    for col, pb in zip(cols, states):
        with col:
            st.pyplot(draw_array(pb.array, pb.bar_states(), pb.algorithm))
            st.progress(min(1.0, pb.progress), text=f"{round(pb.progress * 100)}% of {pb.total} operations")
            st.write(f"Comparisons: **{pb.stats.comparisons}** · Swaps: **{pb.stats.swaps}** · "
                     f"Overwrites: **{pb.stats.overwrites}**")
            st.write("✅ Finished" if pb.done else pb.current_message())


def render_race_page() -> None:
    """Choose two algorithms and race them on the current visualizer array."""
    ss = st.session_state
    st.header("Algorithm Race")
    st.caption("Both algorithms start from the same array and advance the same number of operations per tick. "
               "The race counts OPERATIONS, not seconds, so it is fair and independent of drawing speed. "
               "Use Benchmark mode for real timing.")
    names = list(ALGORITHMS)
    c1, c2 = st.columns(2)
    c1.selectbox("Left algorithm", names, key="race_a")
    c2.selectbox("Right algorithm", names, key="race_b")
    render_input_picker()
    st.select_slider("Animation speed", options=list(SPEEDS), key="speed")

    signature = (ss["race_a"], ss["race_b"], tuple(ss["array"]))
    if ss.get("race_sig") != signature:
        _new_race()
        ss["race_sig"] = signature
    states = ss["race"]

    b1, b2 = st.columns(2)
    b1.button("⏸ Pause" if ss["race_playing"] else "▶ Start race", on_click=_toggle,
              disabled=all(pb.done for pb in states), type="primary")
    b2.button("⟲ Reset race", on_click=_new_race)

    if ss["race_playing"]:
        st.fragment(run_every=SPEEDS[ss["speed"]][0])(_race_view)()
    else:
        st.fragment(_race_view)()
