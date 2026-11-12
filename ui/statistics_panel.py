"""Side panel: a plain-language explanation of the current step, plus key counts."""
from __future__ import annotations

import streamlit as st

from core.sorting_runner import PlaybackState


def _stats_html(pb: PlaybackState) -> str:
    """Comparisons, the kind of move this algorithm makes, and overall position."""
    stats = pb.stats
    moves = ("Writes", stats.overwrites) if pb.algorithm == "Merge Sort" else ("Swaps", stats.swaps)
    counts = (("Comparisons", stats.comparisons), moves, (f"of {pb.total:,} steps", pb.index))
    cells = "".join(f'<div><div class="sl-stat-value">{value:,}</div><div class="sl-stat-label">{label}</div></div>'
                    for label, value in counts)
    return f'<div class="sl-stats">{cells}</div>'


def render_step_panel(pb: PlaybackState) -> None:
    """Everything needed to follow the animation, kept beside the chart."""
    coaching = pb.current_coaching()
    with st.container(border=True, key="step_panel"):
        st.markdown(f'<div class="sl-panel-label">{coaching.context}</div>'
                    f'<div class="sl-step-title">{coaching.title}</div>'
                    f'<div class="sl-step-body">{coaching.body}</div>'
                    f'<div class="sl-note"><div class="sl-note-label">{coaching.note_label}</div>'
                    f'<div class="sl-note-text">{coaching.note}</div></div>'
                    f'{_stats_html(pb)}', unsafe_allow_html=True)
