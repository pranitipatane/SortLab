# SortLab

**Interactive Sorting Algorithm Visualizer — Understand Sorting Algorithms Step by Step**

## Overview

SortLab is a Python + Streamlit learning tool that shows how six classic sorting algorithms work, step by step,
and why their performance differs. It needs no JavaScript, React or Node.js.

## Features

- Setup screen first (algorithm cards, one input picker, live preview), then the visualization with player-style
  controls under the chart
- Animated bar chart with distinct states (normal, comparing, swapping, overwriting, pivot, selected minimum,
  current key, sorted). Every state has a colour **and** a pattern, and a text description.
- Random / Sorted / Reverse Sorted / Nearly Sorted / Many Duplicates arrays, size 5-100
- Custom array input with friendly validation (negatives allowed)
- Play, Pause, Resume, Step, Finish, Start over and five speed settings, including Explain for reading each step
- Live statistics: comparisons, swaps, array accesses, overwrites, operations, progress
- **Why this step?** plain-English explanation for every operation, plus an operation history
- View the real Python implementation and pseudocode
- Complexity information and comparison matrix
- Compare Algorithms (same input, real counts), Algorithm Race (side by side), Benchmark (real timings
  across input distributions), Interview Mode (multiple choice + score), Learn page

## Supported Algorithms

Bubble Sort, Selection Sort, Insertion Sort (swap-based variant), Merge Sort, Quick Sort (Lomuto partition,
last-element pivot, recursion into the smaller side first), Heap Sort. All are written by hand; none use
`sorted()` or `.sort()` (a test enforces this).




## Project Structure

```text
sortlab/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/config.toml
├── algorithms/   bubble_sort.py selection_sort.py insertion_sort.py merge_sort.py quick_sort.py heap_sort.py
├── core/         events.py sorting_runner.py statistics.py
├── data/         algorithm_info.py questions.py
├── utils/        array_utils.py benchmark.py validation.py
├── ui/           setup.py visualizer.py controls.py statistics_panel.py complexity_panel.py explanations.py
│                 compare_mode.py race.py benchmark_panel.py interview.py
├── docs/         code-guide/
├── tests/        one test file per algorithm + test_utils.py + test_setup_flow.py + common.py
└── screenshots/  (add home.png, visualization.png, comparison.png)
```

## Installation

```bash
python -m venv venv
```

Windows: `venv\Scripts\activate`  ·  macOS/Linux: `source venv/bin/activate`

```bash
pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
```

## Testing

```bash
pytest
```

## Screenshots

Add your own after running the app: `screenshots/home.png`, `screenshots/visualization.png`,
`screenshots/comparison.png`.

## Technologies

Python 3.11+, Streamlit (>= 1.67, used for fragments, segmented controls and stretch-width buttons), NumPy, Pandas, Matplotlib, Plotly, pytest.


