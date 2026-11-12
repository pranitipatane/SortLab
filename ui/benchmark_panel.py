"""Benchmark page: real timings, no animation."""
from __future__ import annotations

import streamlit as st

from core.sorting_runner import ALGORITHMS
from utils.array_utils import DISTRIBUTIONS
from utils.benchmark import run_benchmark
from utils.validation import BENCHMARK_SIZE_OPTIONS, validate_benchmark_sizes


def render_benchmark_page() -> None:
    """Configure, run and display a benchmark."""
    ss = st.session_state
    st.header("Benchmark")
    st.caption("Each algorithm sorts a copy of the SAME input and is timed with time.perf_counter(). "
               "No animation or delays are included.")

    names = st.multiselect("Algorithms", list(ALGORITHMS), default=list(ALGORITHMS))
    sizes = st.multiselect("Array sizes", BENCHMARK_SIZE_OPTIONS, default=[10, 25, 50, 100, 250])
    dists = st.multiselect("Input distributions", DISTRIBUTIONS, default=DISTRIBUTIONS)
    repeats = st.slider("Repeats per measurement (best time is kept)", 1, 5, 3)

    if st.button("Run benchmark", type="primary"):
        error = validate_benchmark_sizes(sizes)
        if error:
            st.error(error)
        elif not names or not dists:
            st.error("❌ Please select at least one algorithm and one distribution.")
        else:
            bar = st.progress(0.0, text="Benchmarking…")
            ss["bench_df"] = run_benchmark(names, sizes, dists, repeats,
                                           on_progress=lambda p: bar.progress(p, text="Benchmarking…"))
            bar.empty()

    df = ss.get("bench_df")
    if df is None:
        st.info("Choose your settings and press **Run benchmark**. Sizes of 500+ can take several seconds "
                "for the O(n²) algorithms.")
        return

    import plotly.express as px            # imported here: it is slow to load and only this page needs it

    log_scale = st.checkbox("Logarithmic axes", value=True)
    present = set(df["Distribution"])
    for dist in [d for d in DISTRIBUTIONS if d in present]:
        part = df[df["Distribution"] == dist]
        st.subheader(dist)
        table = part.pivot(index="Size", columns="Algorithm", values="Time (ms)").round(4)
        st.dataframe(table)
        fig = px.line(part, x="Size", y="Time (ms)", color="Algorithm", markers=True,
                      log_x=log_scale, log_y=log_scale)
        st.plotly_chart(fig)

    st.warning("**Read these numbers carefully.** They depend on input size, input distribution, your hardware, "
               "the Python version and this specific implementation. No algorithm is always fastest. "
               "Every algorithm here reports to a do-nothing tracer, which adds a small constant cost per "
               "operation, so absolute times are larger than plain Python loops would be. "
               "Benchmark time is also NOT the animation time, which is dominated by deliberate delays and drawing.")
