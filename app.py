"""SortLab: Interactive Sorting Algorithm Visualizer.

Run with:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="SortLab", page_icon="📊", layout="wide")

from ui.benchmark_panel import render_benchmark_page  # noqa: E402
from ui.compare_mode import render_compare_page  # noqa: E402
from ui.controls import VIEW_SETUP, init_session, render_navigation  # noqa: E402
from ui.explanations import render_learn_page  # noqa: E402
from ui.interview import render_interview_page  # noqa: E402
from ui.race import render_race_page  # noqa: E402
from ui.setup import render_setup_page  # noqa: E402
from ui.theme import CSS  # noqa: E402
from ui.visualizer import render_visualizer_page  # noqa: E402


def main() -> None:
    """Route to the selected page."""
    st.markdown(CSS, unsafe_allow_html=True)
    init_session()
    page = render_navigation()

    if page != "Visualizer":
        st.session_state["playing"] = False       # never leave a hidden animation running
    if page != "Algorithm Race":
        st.session_state["race_playing"] = False

    if page == "Visualizer":
        if st.session_state["vis_view"] == VIEW_SETUP:
            render_setup_page()
        else:
            render_visualizer_page()
    elif page == "Compare Algorithms":
        render_compare_page()
    elif page == "Algorithm Race":
        render_race_page()
    elif page == "Benchmark":
        render_benchmark_page()
    elif page == "Interview Mode":
        render_interview_page()
    else:
        render_learn_page()


main()
