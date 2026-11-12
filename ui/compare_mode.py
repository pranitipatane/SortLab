"""Compare Algorithms page: same input, real statistics."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from core.sorting_runner import ALGORITHMS, run_algorithm
from utils.validation import parse_custom_array


@st.cache_data(show_spinner=False)
def compare(data: tuple[int, ...], names: tuple[str, ...]) -> pd.DataFrame:
    """Run each algorithm on the same data and collect statistics from the events."""
    rows = []
    for name in names:
        run = run_algorithm(name, list(data))
        s = run.stats
        rows.append({"Algorithm": name, "Comparisons": s.comparisons, "Swaps": s.swaps,
                     "Overwrites": s.overwrites, "Array accesses": s.accesses,
                     "Operations": s.operations})
    return pd.DataFrame(rows)


def render_compare_page() -> None:
    """Select algorithms, choose an input, show the results table and chart."""
    st.header("Compare Algorithms")
    st.caption("Every selected algorithm sorts the SAME initial array. All numbers are counted while the real code runs.")

    names = st.multiselect("Algorithms to compare", list(ALGORITHMS), default=list(ALGORITHMS)[:3])
    source = st.radio("Input array", ["Current visualizer array", "Enter my own"], horizontal=True)
    data: list[int] | None = st.session_state["array"]
    if source == "Enter my own":
        text = st.text_input("Array", value="64, 12, 90, 34, 7, 21", key="compare_text")
        result = parse_custom_array(text)
        if result.ok:
            data = result.values
        else:
            data = None
            st.error(result.error)
    if data is None:
        return
    if not names:
        st.warning("Please select at least one algorithm.")
        return

    st.markdown("**Initial array**")
    st.code(str(data), language="text")
    table = compare(tuple(data), tuple(names))
    st.dataframe(table, hide_index=True)
    import plotly.express as px            # imported here: it is slow to load and only this page needs it

    melted = table.melt(id_vars="Algorithm", value_vars=["Comparisons", "Swaps", "Overwrites"],
                        var_name="Metric", value_name="Count")
    st.plotly_chart(px.bar(melted, x="Algorithm", y="Count", color="Metric", barmode="group"))
    st.caption("An 'operation' is one recorded event (compare, swap, overwrite, pivot/selection marker, "
               "sorted marker, completion). Different algorithms record different kinds of steps, "
               "so operation counts show work, not speed.")
