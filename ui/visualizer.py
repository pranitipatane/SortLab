"""Bar-chart rendering and the main Visualizer page."""
from __future__ import annotations

import streamlit as st
from matplotlib.figure import Figure
from matplotlib.patches import Patch

from core.sorting_runner import (ALGORITHMS, COMPARING, KEYING, NORMAL, OVERWRITING, PIVOTING,
                                 SELECTED, SORTED, SWAPPING, PlaybackState)
from ui.controls import SPEEDS, back_to_setup, ensure_playback, render_playback_bar
from ui.explanations import render_explanation
from ui.statistics_panel import render_step_panel

# state -> (colour, hatch pattern, legend text). Patterns keep states distinguishable
# without relying on colour alone. Active states follow the colour-blind-safe Okabe-Ito
# palette; the resting colour is a light tint of the app's blue accent so they stand out.
PREVIEW_BAR = "#1D5FD6"
PREVIEW_BACKGROUND = "#F6F7F9"
MAX_LABELLED_BARS = 40
STYLES: dict[str, tuple[str, str, str]] = {
    NORMAL: ("#9DB8E8", "", "Not final yet"),
    COMPARING: ("#E69F00", "//", "Comparing"),
    SWAPPING: ("#D55E00", "xx", "Swapping"),
    OVERWRITING: ("#AA4499", "\\\\", "Overwriting"),
    PIVOTING: ("#CC79A7", "**", "Pivot"),
    SELECTED: ("#F0E442", "oo", "Selected minimum"),
    KEYING: ("#0072B2", "..", "Current key"),
    SORTED: ("#009E73", "", "Sorted"),
}


def _is_dark() -> bool:
    """Best-effort theme detection (needs a recent Streamlit; falls back to light)."""
    try:
        return st.context.theme.type == "dark"
    except Exception:
        return False


def draw_array(array: list[int], states: list[str], title: str = "", height: float = 4.2,
               compact: bool = False) -> Figure:
    """Draw ``array`` as bars coloured by ``states``. Uses Figure directly (no pyplot state, no leaks)."""
    dark = _is_dark()
    background, text = ("#0E1117", "#FAFAFA") if dark else ("#FFFFFF", "#1F2933")
    if compact:
        background = PREVIEW_BACKGROUND
    fig = Figure(figsize=(10, height), facecolor=background)
    ax = fig.subplots()
    ax.set_facecolor(background)

    n = len(array)
    edge = "#EEEEEE" if dark else "#222222"
    if compact:                            # preview: one solid accent colour
        bars = ax.bar(range(n), array, width=0.85, color=PREVIEW_BAR, linewidth=0)
    else:
        styles = [STYLES[state] for state in states]
        bars = ax.bar(range(n), array, width=0.85, linewidth=0.6,
                      color=[color for color, _, _ in styles],
                      edgecolor=[edge if hatch else color for color, hatch, _ in styles])  # edge also draws the hatch
        for bar, (_, hatch, _) in zip(bars, styles):
            if hatch:
                bar.set_hatch(hatch)
    if n <= MAX_LABELLED_BARS:             # beyond this, the numbers would overlap
        ax.bar_label(bars, labels=list(map(str, array)), fontsize=max(9, 17 - n // 6), color=text, padding=2)
    if not compact:
        ax.axhline(0, color=text, linewidth=0.8)
    ax.set_xticks([])
    ax.tick_params(colors=text)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(text)
    ax.margins(y=0.12)
    if title:
        ax.set_title(title, color=text, fontsize=12)

    if compact:                            # preview: bars only, no axis or legend
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    else:
        used = set(states)
        handles = [Patch(facecolor=color, hatch=hatch, edgecolor=edge, label=label)
                   for state, (color, hatch, label) in STYLES.items() if state in used]
        ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=len(handles),
                  frameon=False, labelcolor=text, fontsize=9)
    fig.tight_layout()
    return fig


def _timer_delay() -> float | None:
    """Seconds between animation refreshes, or ``None`` while not playing."""
    ss = st.session_state
    return SPEEDS[ss["speed"]][0] if ss["playing"] else None


def _live_view(timer: float | None) -> None:
    """The part of the page that refreshes while playing (a Streamlit fragment).

    Chart, step panel and playback bar share one screen, so a learner can watch and
    read without scrolling. ``timer`` is the delay this fragment was started with.
    Only a full app rerun can change a fragment's timer, so one is requested when
    they differ.
    """
    ss = st.session_state
    pb: PlaybackState = ss["playback"]
    if _timer_delay() != timer:
        st.rerun()
    if ss["playing"]:
        pb.step(SPEEDS[ss["speed"]][1])
        if pb.done:
            ss["playing"] = False
            st.rerun()                     # full rerun so the timer stops

    chart, panel = st.columns([13, 7], gap="medium")
    with chart:
        st.pyplot(draw_array(pb.array, pb.bar_states(), height=4.8))
        st.progress(min(1.0, pb.progress))
    with panel:
        render_step_panel(pb)
    render_playback_bar(pb)


def render_visualizer_page() -> None:
    """Main page: live view, then the algorithm guide and complexity."""
    pb = ensure_playback()
    choice, change = st.columns([4, 1], vertical_alignment="bottom")
    choice.selectbox("Sorting algorithm", list(ALGORITHMS), key="algorithm", label_visibility="collapsed")
    change.button("← Change input", key="change_input", on_click=back_to_setup, width="stretch")

    delay = _timer_delay()
    st.fragment(run_every=delay)(_live_view)(delay)

    st.divider()
    render_explanation(pb.algorithm)
