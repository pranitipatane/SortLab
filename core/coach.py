"""Beginner-friendly explanations for every step of a sort.

The algorithms report *what* they did as events. This module turns those events into
the coaching shown beside the chart: where we are, what just happened, and why it matters.

Each ``_bubble``-style function below walks the events of one algorithm and yields exactly
one ``Coaching`` per event. Pure Python, no Streamlit, so every sentence can be tested.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterator, Sequence

from core.events import COMPARE, KEY, MARK_SORTED, PIVOT, SELECT, SWAP, Event

WHY_LABEL = "Why do this?"
IDEA_LABEL = "The big idea"
TAKEAWAY_LABEL = "What to remember"

# The reason behind each algorithm. It stays on screen while the steps change, so a
# beginner can read it at their own pace.
IDEAS = {
    "Bubble Sort": "Each pass carries the largest remaining number to the far right, like a bubble "
                   "rising to the top. After the pass, that number never moves again.",
    "Selection Sort": "Each round finds the smallest number that is left and puts it next in line, "
                      "like picking the shortest person out of a group again and again.",
    "Insertion Sort": "It works like sorting playing cards in your hand: take the next card and "
                      "slide it left until it sits in the right place.",
    "Merge Sort": "Two short sorted groups are easy to combine: keep taking the smaller front number. "
                  "Merge Sort builds bigger and bigger sorted groups this way.",
    "Quick Sort": "Quick Sort splits the work around one number. Smaller numbers go left, the rest "
                  "go right, and each side becomes a smaller problem.",
    "Heap Sort": "Heap Sort first arranges the numbers like a family tree where every parent is at "
                 "least as big as its children. That puts the largest number at the top.",
}
HEAP_REMOVAL_IDEA = ("The largest number is always at the top of the heap. Move it to the end, "
                     "repair the heap, and repeat until every number is placed.")
TAKEAWAYS = {
    "Bubble Sort": "Bubble Sort is simple but slow on big lists because it compares so many pairs. "
                   "Try Nearly Sorted input to see it stop early.",
    "Selection Sort": "Selection Sort makes the same number of comparisons even if the list starts "
                      "sorted, but it uses very few swaps.",
    "Insertion Sort": "Insertion Sort is very fast on nearly sorted lists, because each number only "
                      "slides a short way.",
    "Merge Sort": "Merge Sort stays fast on any input, but it needs extra memory to hold the two "
                  "groups while it combines them.",
    "Quick Sort": "Quick Sort is usually very fast, but a bad pivot slows it down. Try Sorted input "
                  "here to see that happen.",
    "Heap Sort": "Heap Sort stays fast on any input and needs no extra memory, but equal numbers "
                 "can change their original order.",
}


@dataclass(frozen=True, slots=True)
class Coaching:
    """The explanation for one step.

    Attributes:
        context: Where we are, such as ``Pass 1 of 19, comparison 3``.
        title: What happened, in one short line.
        body: The plain-language reason for this particular step.
        note: The larger idea behind the step.
        note_label: Heading shown above ``note``.
    """

    context: str
    title: str
    body: str
    note: str
    note_label: str = WHY_LABEL


Steps = Iterator[Coaching]


def _numbers(count: int) -> str:
    """``1 number`` or ``5 numbers``."""
    return f"{count} number{'' if count == 1 else 's'}"


def _bubble(events: Sequence[Event]) -> Steps:
    idea = IDEAS["Bubble Sort"]
    total = sum(1 for e in events if e.type == COMPARE and e.indices[0] == 0)   # every pass starts at 0
    number = compared = 0
    just_finished_pass = False
    for event in events:
        where = f"Pass {number} of {total}, comparison {compared}"
        if event.type == COMPARE:
            just_finished_pass = False
            a, b = event.values
            if event.indices[0] == 0:
                number, compared = number + 1, 0
            compared += 1
            where = f"Pass {number} of {total}, comparison {compared}"
            if a > b:
                yield Coaching(where, f"{a} and {b} are in the wrong order",
                               f"The bigger number belongs on the right. {a} is bigger than {b}, "
                               "so Bubble Sort swaps them.", idea)
            elif a < b:
                yield Coaching(where, f"{a} and {b} are already in order",
                               "The smaller number is already on the left, so nothing moves. "
                               "Bubble Sort goes on to the next pair.", idea)
            else:
                yield Coaching(where, f"{a} and {b} are equal",
                               "Equal numbers do not need to change places, so nothing moves. "
                               "Bubble Sort goes on to the next pair.", idea)
        elif event.type == SWAP:
            a, b = event.values
            yield Coaching(where, f"Swap {a} and {b}",
                           f"{a} moves one place right and {b} moves one place left, so the "
                           "smaller number now comes first.", idea)
        elif just_finished_pass:                # a second mark means this pass made no swaps
            yield Coaching(f"Pass {number} of {total}, finished", "The rest is already sorted",
                           "That whole pass needed no swaps, so every number is in order and "
                           "Bubble Sort can stop early.", idea)
        else:
            just_finished_pass = True
            value = event.values[0]
            yield Coaching(f"Pass {number} of {total}, finished", f"{value} is in its final place",
                           f"No number still being sorted is bigger than {value}, so it will "
                           "never move again.", idea)


def _selection(events: Sequence[Event]) -> Steps:
    idea = IDEAS["Selection Sort"]
    total = sum(1 for e in events if e.type == MARK_SORTED)
    number, compared = 1, 0
    new_round = True
    for event in events:
        where = f"Round {number} of {total}"
        if event.type == SELECT:
            value = event.values[0]
            if new_round:
                new_round = False
                yield Coaching(where, f"Start with {value} as the smallest so far",
                               f"{value} is the first unsorted number, so it is the smallest seen "
                               "so far. Selection Sort will check every number to its right.", idea)
            else:
                yield Coaching(where, f"{value} is the new smallest",
                               f"Selection Sort remembers {value} and keeps looking, in case an "
                               "even smaller number is further along.", idea)
        elif event.type == COMPARE:
            compared += 1
            a, b = event.values
            where = f"{where}, comparison {compared} of {total - number + 1}"
            if a < b:
                yield Coaching(where, f"{a} is smaller than {b}",
                               f"{a} becomes the smallest number found so far this round.", idea)
            else:
                yield Coaching(where, f"{a} is not smaller than {b}",
                               f"{b} stays the smallest number found so far. Selection Sort moves "
                               "on to the next number.", idea)
        elif event.type == SWAP:
            a, b = event.values
            yield Coaching(where, f"Move {b} to the front of the unsorted part",
                           f"{b} is the smallest number left, so it trades places with {a}, which "
                           "was sitting in the spot it needs.", idea)
        else:
            value = event.values[0]
            yield Coaching(where, f"{value} is in its final place",
                           "Everything on its left is smaller or equal, and everything on its "
                           "right is bigger or equal, so it never moves again.", idea)
            number, compared, new_round = number + 1, 0, True


def _insertion(events: Sequence[Event]) -> Steps:
    idea = IDEAS["Insertion Sort"]
    total = sum(1 for e in events if e.type == KEY)
    number = 0
    for event in events:
        if event.type == KEY:
            number += 1
        where = f"Inserting number {number} of {total}"
        if event.type == KEY:
            value = event.values[0]
            yield Coaching(where, f"Pick up {value}",
                           f"Everything to the left of {value} is already sorted. Now {value} "
                           "slides left until it reaches its correct spot.", idea)
        elif event.type == COMPARE:
            a, b = event.values
            if a > b:
                yield Coaching(where, f"{a} is bigger than {b}",
                               f"{b} belongs before {a}, so {b} has to move left.", idea)
            else:
                yield Coaching(where, f"{b} has found its spot",
                               f"{a} is not bigger than {b}, so {b} can stop here. The numbers on "
                               "the left are still in order.", idea)
        else:
            a, b = event.values
            at_start = f" {b} is now at the very start, so there is nothing more to check." if event.indices[0] == 0 else ""
            yield Coaching(where, f"Slide {b} left past {a}",
                           f"{a} moves one place right to make room.{at_start}", idea)


def _merge(events: Sequence[Event]) -> Steps:
    idea = IDEAS["Merge Sort"]
    total = len({e.section for e in events})
    section = None
    number = left_taken = right_taken = 0
    previous = None
    for event in events:
        if event.section != section:
            section = event.section
            number, left_taken, right_taken = number + 1, 0, 0
        lo, hi, mid = section
        left_size, right_size = mid - lo, hi - mid
        where = f"Merge {number} of {total}: combining {left_size} and {right_size} numbers"
        if event.type == COMPARE:
            a, b = event.values
            if a == b:
                yield Coaching(where, f"{a} and {b} are equal",
                               "The front numbers of both groups match. The left one goes first, "
                               "so equal numbers keep their original order.", idea)
            else:
                yield Coaching(where, f"{min(a, b)} is smaller than {max(a, b)}",
                               "These are the front numbers of the left and right groups. "
                               "The smaller one goes next.", idea)
        elif previous is not None and previous.type == COMPARE:
            a, b = previous.values
            from_left = a <= b
            side = "left" if from_left else "right"
            left_taken += from_left
            right_taken += not from_left
            yield Coaching(where, f"Place {event.values[0]} next",
                           f"{event.values[0]} came from the {side} group. It takes the next spot "
                           f"in the combined group, and the {side} group moves on to its next number.", idea)
        else:
            from_left = left_taken < left_size
            side, other = ("left", "right") if from_left else ("right", "left")
            left_taken += from_left
            right_taken += not from_left
            yield Coaching(where, f"Copy {event.values[0]} over",
                           f"The {other} group has run out, and the {side} group is already in "
                           "order, so its remaining numbers can go straight in.", idea)
        previous = event


def _quick(events: Sequence[Event]) -> Steps:
    idea = IDEAS["Quick Sort"]
    total = sum(1 for e in events if e.type == PIVOT)
    number = checked = size = 0
    pivot_position = None
    for position, event in enumerate(events):
        where = f"Partition {number} of {total}, checked {checked} of {size}"
        if event.type == PIVOT:
            number, checked = number + 1, 0
            lo, hi, _ = event.section
            size, pivot_position = hi - lo - 1, event.indices[0]
            value = event.values[0]
            yield Coaching(f"Partition {number} of {total}", f"Use {value} as the pivot",
                           "The pivot is the number everything else gets compared against. "
                           f"This section has {_numbers(size)} to check.", idea)
        elif event.type == COMPARE:
            checked += 1
            where = f"Partition {number} of {total}, checked {checked} of {size}"
            a, pivot = event.values
            if a < pivot:
                following = events[position + 1] if position + 1 < len(events) else None
                will_move = (following is not None and following.type == SWAP
                             and following.indices[1] != pivot_position)
                ending = "so it will move there." if will_move else "and it is already there."
                yield Coaching(where, f"{a} is smaller than the pivot {pivot}",
                               f"{a} belongs with the smaller numbers on the left, {ending}", idea)
            else:
                yield Coaching(where, f"{a} is not smaller than the pivot {pivot}",
                               f"{a} can stay on the right side, so nothing moves.", idea)
        elif event.type == SWAP:
            a, b = event.values
            if event.indices[1] == pivot_position:
                yield Coaching(where, f"Put the pivot {b} between the two sides",
                               "Everything on its left is smaller, and everything on its right "
                               "is at least as big.", idea)
            else:
                yield Coaching(where, f"Move {b} to the smaller side",
                               f"{b} trades places with {a}, which is not smaller than the pivot. "
                               "The smaller numbers stay grouped on the left.", idea)
        elif pivot_position is not None:
            pivot_position = None
            yield Coaching(f"Partition {number} of {total}, finished",
                           f"{event.values[0]} is in its final place",
                           "The pivot never needs to move again. Quick Sort now repeats the same "
                           "job on the numbers on each side.", idea)
        else:
            yield Coaching("A section of one number", f"{event.values[0]} is on its own",
                           "A section with only one number is already sorted, so it is in its "
                           "final place.", idea)


def _heap(events: Sequence[Event]) -> Steps:
    total = sum(1 for e in events if e.type == MARK_SORTED)
    number = 0
    for position, event in enumerate(events):
        idea = HEAP_REMOVAL_IDEA if number else IDEAS["Heap Sort"]
        where = f"Round {number} of {total}: repairing the heap" if number else "Building the heap"
        if event.type == COMPARE and event.indices[0] < event.indices[1]:    # two children
            a, b = event.values
            title = f"Both children are {a}" if a == b else f"{max(a, b)} is the bigger child"
            yield Coaching(where, title,
                           "A parent has up to two children. Only the bigger one can safely move "
                           "up, so Heap Sort finds it first.", idea)
        elif event.type == COMPARE:                                          # child, then parent
            child, parent = event.values
            if child > parent:
                yield Coaching(where, f"Child {child} is bigger than parent {parent}",
                               "A parent must be at least as big as its children, so these two "
                               "need to swap.", idea)
            else:
                yield Coaching(where, f"Parent {parent} is big enough",
                               f"{parent} is at least as big as its child {child}, so this part of "
                               "the heap is fine and nothing moves.", idea)
        elif event.type == SWAP and position + 1 < len(events) and events[position + 1].type == MARK_SORTED:
            number += 1
            a, b = event.values
            yield Coaching(f"Round {number} of {total}: moving the largest",
                           f"Move the largest number, {a}, to the end",
                           f"{a} is at the top of the heap, so it is the biggest number left. It "
                           f"trades places with {b}, the last number in the heap.", HEAP_REMOVAL_IDEA)
        elif event.type == SWAP:
            parent, child = event.values
            yield Coaching(where, f"Swap {child} up and {parent} down",
                           f"{child} moves up to become the parent. {parent} moves down and may "
                           "need to keep going.", idea)
        else:
            yield Coaching(f"Round {number} of {total}: moving the largest",
                           f"{event.values[0]} is in its final place",
                           "It is now out of the heap and will never move again. The heap is one "
                           "number smaller.", HEAP_REMOVAL_IDEA)


_WRITERS: dict[str, Callable[[Sequence[Event]], Steps]] = {
    "Bubble Sort": _bubble,
    "Selection Sort": _selection,
    "Insertion Sort": _insertion,
    "Merge Sort": _merge,
    "Quick Sort": _quick,
    "Heap Sort": _heap,
}


def introduction(algorithm: str, total_steps: int) -> Coaching:
    """What the panel says before the first step."""
    return Coaching(f"{total_steps:,} steps to play", "Ready to start",
                    f"Press Play to watch {algorithm}, or Step to go one move at a time.",
                    IDEAS[algorithm], IDEA_LABEL)


def build_coaching(algorithm: str, events: Sequence[Event]) -> list[Coaching]:
    """Return one ``Coaching`` for each event, in the same order.

    Every run ends with exactly one ``complete`` event, which gets the closing message.
    """
    steps = list(_WRITERS[algorithm](events[:-1]))
    finished = Coaching("Finished", "All sorted", "Every number is now in its final place.",
                        TAKEAWAYS[algorithm], TAKEAWAY_LABEL)
    return steps + [finished]
