"""Statistics computed from events (never hard-coded)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from core.events import COMPARE, OVERWRITE, SWAP, Event


@dataclass
class Stats:
    """Running counters. One *operation* = one event."""

    comparisons: int = 0
    swaps: int = 0
    overwrites: int = 0
    accesses: int = 0     # reads/writes of the main array
    operations: int = 0

    def apply(self, event: Event) -> None:
        """Update the counters with one event."""
        self.operations += 1
        self.accesses += event.accesses
        if event.type == COMPARE:
            self.comparisons += 1
        elif event.type == SWAP:
            self.swaps += 1
        elif event.type == OVERWRITE:
            self.overwrites += 1


def summarize(events: Iterable[Event]) -> Stats:
    """Totals for a whole event list."""
    stats = Stats()
    for event in events:
        stats.apply(event)
    return stats
