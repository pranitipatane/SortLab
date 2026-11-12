"""Static educational information about each algorithm.

``steps`` holds ``(what to do, more detail)`` pairs. Every detail follows the same example
list, 29, 10, 14, 37, 13, so a beginner can compare the algorithms on equal terms.
"""
from __future__ import annotations

import pandas as pd

ALGORITHM_INFO: dict[str, dict] = {
    "Bubble Sort": {
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "stable": True, "in_place": True,
        "what": "Compares neighbouring numbers and swaps any pair in the wrong order. "
                "After each pass, the biggest number left has moved to the end.",
        "steps": [
            ("Compare the first two neighbours.", "Start at the left. In 29, 10, 14, 37, 13 the first pair is 29 and 10."),
            ("Swap them if the left one is bigger.", "29 is bigger than 10, so they swap and the list becomes 10, 29, 14, 37, 13."),
            ("Move one place right and repeat.", "Next compare 29 and 14, then keep going. The biggest number gets carried "
                                                 "along, so 37 reaches the end of the list."),
            ("The biggest number is now finished.", "37 is in its final place, so the next pass stops one place earlier."),
            ("Stop when a pass makes no swaps.", "If nothing moved in a whole pass, every number is in order and there is "
                                                 "no need to keep checking."),
        ],
        "speed_note": "O(n²) means twice the numbers takes about four times the work. O(n) means the work only "
                      "doubles, which happens when the list is already sorted.",
        "memory": "Almost none, O(1)",
        "pros": ["Very simple to write and explain.", "Keeps equal numbers in their original order.",
                 "Notices a list is already sorted after one pass."],
        "cons": ["Slow on big lists, because it compares so many pairs.", "Makes far more swaps than Selection Sort."],
        "use_case": "You are learning sorting, or the list is tiny and almost sorted. It is rarely used in real programs.",
        "pseudocode": "for end from n-1 down to 1:\n    swapped = false\n    for i from 0 to end-1:\n"
                      "        if a[i] > a[i+1]:\n            swap a[i], a[i+1]\n            swapped = true\n"
                      "    if not swapped: stop",
    },
    "Selection Sort": {
        "best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "stable": False, "in_place": True,
        "what": "Finds the smallest number that is left and moves it to the front of the unsorted part.",
        "steps": [
            ("Assume the first unsorted number is the smallest.", "You have not checked the others yet, so this is only a "
                                                                  "starting guess. In 29, 10, 14, 37, 13 the guess is 29."),
            ("Check the rest and remember any smaller number.", "Look at each remaining number once. 10 beats 29, and nothing "
                                                                "after it beats 10, so 10 is the smallest."),
            ("Swap the smallest into the first unsorted spot.", "10 and 29 trade places, giving 10, 29, 14, 37, 13."),
            ("The sorted part grows by one. Repeat.", "10 is now final, so the next round starts at 29. Once every other number "
                                                      "is placed, the last one is automatically right."),
        ],
        "speed_note": "O(n²) means twice the numbers takes about four times the work.",
        "memory": "Almost none, O(1)",
        "pros": ["Very few swaps: at most one each round.", "Needs almost no extra memory.", "Easy to understand."],
        "cons": ["It checks every number, even in a sorted list.", "A long swap can jump over an equal number."],
        "use_case": "The list is small and moving numbers is expensive.",
        "pseudocode": "for i from 0 to n-2:\n    min = i\n    for j from i+1 to n-1:\n"
                      "        if a[j] < a[min]: min = j\n    swap a[i], a[min]",
    },
    "Insertion Sort": {
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "stable": True, "in_place": True,
        "what": "Builds a sorted group one number at a time, like sorting playing cards in your hand.",
        "steps": [
            ("Treat the first number as a sorted group.", "A single number is always in order. In 29, 10, 14, 37, 13 that "
                                                          "group is just 29."),
            ("Pick up the next number.", "Here that is 10. The number being placed is called the key."),
            ("Slide it left past every bigger number.", "29 is bigger than 10, so 10 moves in front of it, giving "
                                                        "10, 29, 14, 37, 13. It stops when the number on its left is not bigger."),
            ("The sorted group is now one longer. Repeat.", "10 and 29 are in order. 14 is next, and it only slides left past 29."),
        ],
        "speed_note": "O(n²) means twice the numbers takes about four times the work. O(n) means the work only "
                      "doubles, which happens when the list is already sorted.",
        "memory": "Almost none, O(1)",
        "pros": ["Very fast on nearly sorted lists.", "Keeps equal numbers in their original order.",
                 "Little extra work, so it does well on small lists."],
        "cons": ["Slow on big lists, especially ones in reverse order."],
        "use_case": "The list is small or nearly sorted. Faster sorts often use it for their small pieces.",
        "pseudocode": "for i from 1 to n-1:\n    j = i\n    while j > 0 and a[j-1] > a[j]:\n"
                      "        swap a[j-1], a[j]\n        j = j - 1",
    },
    "Merge Sort": {
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(n)",
        "stable": True, "in_place": False,
        "what": "Splits the list into smaller and smaller groups, then combines them back together in sorted order.",
        "steps": [
            ("Split the list into two halves.", "29, 10, 14, 37, 13 becomes 29, 10 and 14, 37, 13."),
            ("Keep splitting until each group has one number.", "A group of one number is already sorted, so this is where "
                                                                "the combining can start."),
            ("Combine groups by taking the smaller front number.", "To combine 10, 29 and 13, 14, 37, compare 10 and 13. "
                                                                   "10 goes first, then compare 29 and 13."),
            ("Copy any leftovers.", "When one group runs out, the other is already in order, so its remaining numbers go "
                                    "straight in. Here, 37 ends up last."),
            ("Keep combining until one list is left.", "Every combined group is sorted, so bigger and bigger groups can be "
                                                       "combined the same way until the whole list is done."),
        ],
        "speed_note": "O(n log n) means twice the numbers takes only a little more than twice the work, on every input.",
        "memory": "As much as the list, O(n)",
        "pros": ["Stays fast on every input.", "Keeps equal numbers in their original order.", "Its speed is easy to predict."],
        "cons": ["Needs extra memory as large as the list.", "All the copying adds some work."],
        "use_case": "The list is large and you need reliable speed, or equal items must keep their order.",
        "pseudocode": "merge_sort(a, lo, hi):\n    if hi - lo < 2: return\n    mid = (lo + hi) / 2\n"
                      "    merge_sort(a, lo, mid)\n    merge_sort(a, mid, hi)\n    merge(a, lo, mid, hi)",
    },
    "Quick Sort": {
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)", "space": "O(log n)*",
        "stable": False, "in_place": True,
        "what": "Picks one number as the pivot, moves smaller numbers to its left and the rest to its right, "
                "then does the same on each side.",
        "steps": [
            ("Choose a pivot.", "The pivot is the number everything else is compared with. This version uses the last "
                                "number, so in 29, 10, 14, 37, 13 the pivot is 13."),
            ("Compare every other number with the pivot.", "Each one is either smaller than 13 or not. Here only 10 is smaller."),
            ("Move the smaller numbers to the left.", "10 moves to the front, giving 10, 29, 14, 37, 13."),
            ("Put the pivot between the two sides.", "13 swaps with 29, giving 10, 13, 14, 37, 29. Now 13 is in its final place."),
            ("Repeat on each side.", "The left side is finished, because 10 is on its own. The right side, 14, 37, 29, "
                                     "gets its own pivot and the same treatment."),
        ],
        "speed_note": "O(n log n) means twice the numbers takes only a little more than twice the work. Poor pivots "
                      "can make it O(n²), which is about four times the work.",
        "memory": "A little, O(log n)",
        "pros": ["Very fast on most lists.", "Sorts inside the original list.", "Works well with how computers read memory."],
        "cons": ["Bad pivots make it slow, such as always using the last number on a sorted list.",
                 "A swap can change the order of equal numbers."],
        "use_case": "You need a fast general-purpose sort for a list in memory, with a good way to pick the pivot.",
        "pseudocode": "quick_sort(a, lo, hi):\n    while lo < hi:\n        p = partition(a, lo, hi)\n"
                      "        recurse on the smaller side, loop on the larger side\n\n"
                      "partition(a, lo, hi):\n    pivot = a[hi]; i = lo\n    for j from lo to hi-1:\n"
                      "        if a[j] < pivot: swap a[i], a[j]; i = i + 1\n    swap a[i], a[hi]\n    return i",
    },
    "Heap Sort": {
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(1)",
        "stable": False, "in_place": True,
        "what": "Arranges the numbers so the largest is always on top, then keeps moving the top number to the end.",
        "steps": [
            ("Picture the list as a tree.", "The first number is the top, and each number has up to two children. The bars "
                                            "stay in a row, but this is how Heap Sort sees them."),
            ("Build a max-heap.", "Swap numbers until every parent is at least as big as its children. "
                                  "29, 10, 14, 37, 13 becomes 37, 29, 14, 10, 13, with 37 on top."),
            ("Move the top number to the end.", "37 is the largest, so it swaps with the last number in the heap. "
                                                "37 is now final and leaves the heap."),
            ("Repair the heap.", "The number now on top, 13, is too small. It swaps with its bigger child, 29, until every "
                                 "parent is big enough again."),
            ("Repeat until one number is left.", "Each round places the next largest number. Repairing is quick because "
                                                 "the tree is short."),
        ],
        "speed_note": "O(n log n) means twice the numbers takes only a little more than twice the work, on every input.",
        "memory": "Almost none, O(1)",
        "pros": ["Stays fast on every input.", "Needs almost no extra memory."],
        "cons": ["A swap can change the order of equal numbers.", "Usually slower than Quick Sort in practice."],
        "use_case": "You need reliable speed and cannot spare extra memory.",
        "pseudocode": "build max-heap from a\nfor end from n-1 down to 1:\n    swap a[0], a[end]\n"
                      "    sift_down(a, 0, end)",
    },
}


def get_info(name: str) -> dict:
    """Return the information dictionary for an algorithm."""
    return ALGORITHM_INFO[name]


def complexity_dataframe() -> pd.DataFrame:
    """The comparison matrix used by the UI."""
    rows = []
    for name, info in ALGORITHM_INFO.items():
        rows.append({"Algorithm": name, "Best": info["best"], "Average": info["average"],
                     "Worst": info["worst"], "Space": info["space"],
                     "Stable": "Yes" if info["stable"] else "No",
                     "In-place": "Yes" if info["in_place"] else "No"})
    return pd.DataFrame(rows)
