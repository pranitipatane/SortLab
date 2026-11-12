"""The table comparing the complexity of every algorithm."""
from __future__ import annotations

import streamlit as st

from data.algorithm_info import complexity_dataframe


@st.cache_data
def _matrix():
    return complexity_dataframe()


def render_matrix() -> None:
    """Algorithm comparison matrix."""
    st.markdown("**Algorithm comparison matrix**")
    st.dataframe(_matrix(), hide_index=True)
    st.caption("* Quick Sort's space is its recursion stack: O(log n) with balanced partitions "
               "(and with this project's smaller-side-first recursion); a naive version can reach O(n). "
               "Best case for Bubble/Insertion Sort assumes the early-exit check / already sorted input.")
