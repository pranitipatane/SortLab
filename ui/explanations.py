"""Algorithm explanations, code view and the Learn page."""
from __future__ import annotations

import inspect
import re
import sys

import numpy as np
import pandas as pd
import streamlit as st

from core.sorting_runner import ALGORITHMS
from data.algorithm_info import ALGORITHM_INFO
from ui.complexity_panel import render_matrix

SPEED_WORDS = {"O(n)": "Very fast", "O(n log n)": "Fast", "O(n²)": "Slow"}
_ANIMATION_LINE = re.compile(r"\s*(tracer\b|from )")
_TRACER_ARGUMENT = re.compile(r",\s*tracer(: Tracer( \| None = None)?)?")


def _yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def _guide_html(name: str) -> str:
    """Left column: what the algorithm does, its detailed steps, and when to use it."""
    info = ALGORITHM_INFO[name]
    steps = "".join(f'<li><span class="sl-learn-num">{number}</span><div>'
                    f'<div class="sl-learn-step">{title}</div><div class="sl-learn-detail">{detail}</div></div></li>'
                    for number, (title, detail) in enumerate(info["steps"], 1))
    return (f'<div class="sl-learn-title">{name}</div><div class="sl-learn-lead">{info["what"]}</div>'
            f'<div class="sl-learn-heading">How it works</div><ol class="sl-learn-steps">{steps}</ol>'
            f'<div class="sl-learn-use"><div class="sl-note-label">Use it when</div>'
            f'<div class="sl-learn-use-text">{info["use_case"]}</div></div>')


def _facts_html(name: str) -> str:
    """Right column: speed and memory in plain words, then strengths and weaknesses."""
    info = ALGORITHM_INFO[name]
    tiles = ""
    for label, key in (("Best case", "best"), ("Typical", "average"), ("Worst case", "worst")):
        word = SPEED_WORDS[info[key]]
        tone = "slow" if word == "Slow" else "fast"
        tiles += (f'<div class="sl-learn-tile"><div class="sl-stat-label">{label}</div>'
                  f'<div class="sl-learn-big">{info[key]}</div><div class="sl-speed-{tone}">{word}</div></div>')
    rows = (("Extra memory", info["memory"]), ("Sorts inside the original list", _yes_no(info["in_place"])),
            ("Keeps equal numbers in order", _yes_no(info["stable"])))
    facts = "".join(f"<div><span>{label}</span><strong>{value}</strong></div>" for label, value in rows)
    pros = "".join(f"<li>{item}</li>" for item in info["pros"])
    cons = "".join(f"<li>{item}</li>" for item in info["cons"])
    return (f'<div class="sl-learn-tiles">{tiles}</div><div class="sl-learn-note">{info["speed_note"]}</div>'
            f'<div class="sl-learn-rows">{facts}</div><div class="sl-learn-lists">'
            f'<div><div class="sl-learn-heading">Strengths</div><ul class="sl-learn-list sl-good">{pros}</ul></div>'
            f'<div><div class="sl-learn-heading">Weaknesses</div><ul class="sl-learn-list sl-bad">{cons}</ul></div></div>')


def render_explanation(name: str) -> None:
    """The guide under the player: guide and facts side by side, then code and comparison."""
    with st.container(key="learn_page"):
        guide, facts = st.columns([5, 6], gap="large")
        guide.markdown(_guide_html(name), unsafe_allow_html=True)
        facts.markdown(_facts_html(name), unsafe_allow_html=True)
    st.divider()
    _render_code(name)
    st.divider()
    render_matrix()


def readable_source(source: str) -> str:
    """Return an algorithm's source with the animation bookkeeping removed.

    The module docstring, imports, ``tracer`` lines and ``tracer`` arguments only exist
    for this app. The result is still valid Python that sorts correctly, which the tests check.
    """
    body = source.split('"""', 2)[2]
    lines = [_TRACER_ARGUMENT.sub("", line) for line in body.splitlines() if not _ANIMATION_LINE.match(line)]
    kept: list[str] = []                              # built bottom-up, so kept[-1] is the next line
    for line in reversed(lines):
        opens_block = line.split("#")[0].rstrip().endswith(":")
        following = next((other for other in reversed(kept) if other.strip()), "")
        indent = len(line) - len(line.lstrip())
        if opens_block and len(following) - len(following.lstrip()) <= indent:
            continue                                  # its only line was a tracer call
        kept.append(line)
    return "\n".join(reversed(kept)).strip()


@st.cache_data
def _python_code(name: str) -> str:
    """The real source file of the algorithm (not a copy), ready to read."""
    module = sys.modules[ALGORITHMS[name].__module__]
    return readable_source(inspect.getsource(module))


def _render_code(name: str) -> None:
    """The algorithm's code, always open, as Python or pseudocode."""
    heading, choice = st.columns([3, 1], vertical_alignment="center")
    heading.markdown('<div class="sl-learn-code-title">The code</div>', unsafe_allow_html=True)
    view = choice.segmented_control("Code view", ["Python", "Pseudocode"], default="Python", required=True,
                                    key="code_view", label_visibility="collapsed")
    if view == "Python":
        st.code(_python_code(name), language="python")
        st.caption("The real sorting code from this app, with the lines that drive the animation hidden.")
    else:
        st.code(ALGORITHM_INFO[name]["pseudocode"], language="text")


@st.cache_data
def _growth_table() -> pd.DataFrame:
    n = np.array([1, 2, 4, 8, 16, 32, 64, 128])
    return pd.DataFrame({"n": n, "n log₂ n": (n * np.log2(n)).round(0).astype(int), "n²": n ** 2}).set_index("n")


def render_learn_page() -> None:
    """Concept explanations for beginners."""
    st.header("Learn: Sorting Fundamentals")
    st.markdown("### What is sorting?")
    st.markdown("Sorting puts items in order, for example `[5, 3, 8, 1]` → `[1, 3, 5, 8]`.")
    st.markdown("### Why is sorting useful?")
    st.markdown("- Searching a sorted list is much faster (binary search: O(log n)).\n"
                "- It makes duplicates easy to find and data easy to read.\n"
                "- Many other algorithms assume their input is sorted.")
    st.markdown("### Comparison-based sorting")
    st.markdown("All six algorithms in SortLab decide the order by **comparing two values** (`a > b`). "
                "Any comparison-based sort needs Ω(n log n) comparisons in the worst case.")
    st.markdown("### Stable vs unstable")
    st.code("Records sorted by number:   (2,'A')  (1,'B')  (2,'C')\n"
            "Stable result:             (1,'B')  (2,'A')  (2,'C')   <- A stays before C\n"
            "Unstable (maybe):          (1,'B')  (2,'C')  (2,'A')   <- equal keys may swap", language="text")
    st.markdown("### In-place vs out-of-place")
    st.markdown("An **in-place** algorithm rearranges the original array using O(1) (or tiny) extra memory. "
                "An **out-of-place** algorithm, like Merge Sort, needs extra memory that grows with n.")
    st.markdown("### Time complexity and Big-O")
    st.markdown("Big-O describes how the number of steps *grows* as the input size n grows. "
                "The table shows why O(n log n) beats O(n²) for large inputs:")
    st.dataframe(_growth_table())
    st.markdown("### Space complexity")
    st.markdown("Space complexity counts the **extra** memory an algorithm needs, not the input itself.")
    st.markdown("### Best, average and worst case")
    st.code("Insertion Sort on [1, 2, 3, 4, 5]  -> best case    O(n)\n"
            "Insertion Sort on random data     -> average case O(n²)\n"
            "Insertion Sort on [5, 4, 3, 2, 1] -> worst case   O(n²)", language="text")
    st.markdown("### Comparison matrix")
    render_matrix()
