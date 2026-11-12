# Code Guide, Phase 1: Setup-First Visualizer

## What changed for the user

Before, the chart was on screen immediately and 13 controls sat in the sidebar. Now the Visualizer has two views:

1. **Setup:** choose an algorithm, choose the input, see a preview, press **Start visualizing**.
2. **Play:** the chart with a step panel beside it and player controls under both, all on one screen so a learner can watch and read without scrolling.

The sidebar now holds only page navigation.

## Approach

The Visualizer stays one page and remembers which view it is on in `st.session_state["vis_view"]`, either `"setup"` or `"play"`. `app.py` reads that value and draws the matching screen.

| Alternative considered | Why it was not used |
|---|---|
| A separate "Setup" page in the navigation | Users could land on the player with nothing chosen |
| A multi-step wizard | More clicks for someone who only wants to try another algorithm |
| Keeping playback buttons outside the fragment | They could not sit directly under the chart and step panel |

## Flow

```text
app.py -> init_session() -> vis_view?
             |                |
             |                +-- "setup" -> render_setup_page()
             |                |                rows -> choose_algorithm()
             |                |                render_input_picker()
             |                |                Start -> begin_visualizing() -> vis_view = "play"
             |                |
             |                +-- "play"  -> render_visualizer_page()
             |                                 algorithm dropdown, Change input -> back_to_setup()
             |                                 fragment _live_view(timer)
             |                                   chart + render_step_panel(), then render_playback_bar()
```

## Key idea: the timer check

A Streamlit fragment reruns on its own timer, and only a full app rerun can start, stop or change that timer. The playback bar is inside the fragment, so pressing Pause reruns only the fragment and the old timer keeps going.

`_live_view(timer)` solves this. It receives the delay it was started with and compares it to `_timer_delay()`, the delay it should have now. If they differ, it calls `st.rerun()` to restart the page with the right timer.

## Key idea: the coach is separate from the algorithms

The panel beside the chart teaches a beginner what each step means. Algorithms stay small: they only report events. `core/coach.py` reads those events and writes the explanation for each one.

```text
algorithm -> events -> build_coaching() -> one Coaching per event
                                             context  "Pass 1 of 19, comparison 2"
                                             title    "99 and 47 are in the wrong order"
                                             body     the reason for this exact step
                                             note     the larger idea behind the algorithm
```

| Alternative considered | Why it was not used |
|---|---|
| Longer `why` text inside each algorithm | A compare runs before the algorithm decides, so it cannot yet say "swap" or "leave them" |
| Passing pass numbers through every tracer call | Bubble, Selection, Insertion and Heap can work it out from the events |
| Writing the text during playback | Pressing Finish would format every step for nothing |

Merge and Quick Sort work on one section at a time, and events alone cannot show which. They call `tracer.begin_section(...)`, and the recorder stores that section on later events. It adds no animation step.

`PlaybackState` builds the coaching the first time it is shown, so the Race page never pays for it.

## Key idea: the guide under the player

The player is followed by one page with no tabs: guide and facts, then the code, then the table comparing all six algorithms. The guide reads everything from `ALGORITHM_INFO` in `data/algorithm_info.py`. Each entry in `steps` is a pair: the instruction, then more detail. All six algorithms use the same example list, 29, 10, 14, 37, 13, so they can be compared directly.

The code is always open below the guide. The real algorithm files contain `tracer` lines that only drive the animation, so `readable_source` removes them from the display. It reads the real file every time, so the page cannot drift out of date. A test runs the displayed code on every test array to prove it still sorts.

## Function reference

| Function | File | Purpose | Inputs | Output / effect | Example |
|---|---|---|---|---|---|
| `render_setup_page` | `ui/setup.py` | Draws the setup screen | Session state | Algorithm list, preview, picker, Start button | Opening the app |
| `_render_algorithm_list` | `ui/setup.py` | Draws six clickable rows | Session state | Selected row is highlighted | Quick Sort row turns blue |
| `_row_html` | `ui/setup.py` | Contents of one row | `name: str` | HTML string | Name, tagline, speed badge such as `O(n²) · Slow` |
| `_facts_html` | `ui/setup.py` | Facts under the preview | `name: str` | HTML string | Time, space, stable |
| `choose_algorithm` | `ui/controls.py` | Selects an algorithm | `name: str` | Sets `algorithm` | `"Heap Sort"` |
| `render_input_picker` | `ui/controls.py` | Shared input controls | Session state | Type choice plus size or text box | Used by Setup and Race |
| `_on_kind_change` | `ui/controls.py` | Handles an input type change | Session state | New array, or custom numbers | Custom prefilled from current bars |
| `_apply_custom` | `ui/controls.py` | Validates typed numbers | `custom_text` | Sets `array` or `custom_error` | `"1, x"` gives an error |
| `_regenerate` | `ui/controls.py` | Makes a new array | Size and type | Sets `array`, clears error | 20 Random values |
| `begin_visualizing` | `ui/controls.py` | Leaves setup and plays | Session state | Rewinds, `playing=True`, `vis_view="play"` | Stays on setup if input is invalid |
| `back_to_setup` | `ui/controls.py` | Returns to setup | Session state | `playing=False`, `vis_view="setup"` | Array is kept |
| `_toggle_play` | `ui/controls.py` | Play or pause | Session state | Flips `playing` | Stays off when finished |
| `render_playback_bar` | `ui/controls.py` | Player controls | `pb: PlaybackState` | Buttons and speed | Label shows Play, Pause or Resume |
| `_start_over` | `ui/controls.py` | Replays from the start | Session state | Rewinds, `playing=True` | Replaces Restart and Reset |
| `render_step_panel` | `ui/statistics_panel.py` | Panel beside the chart | `pb: PlaybackState` | Coaching text and counts | "Swap 68 and 52" |
| `_stats_html` | `ui/statistics_panel.py` | Counts row | `pb: PlaybackState` | HTML string | Shows Writes for Merge Sort, Swaps for the rest |
| `build_coaching` | `core/coach.py` | Writes all explanations | `algorithm: str`, `events` | `list[Coaching]`, one per event | Bubble Sort's first step |
| `introduction` | `core/coach.py` | Text before the first step | `algorithm: str`, `total_steps: int` | `Coaching` | "Ready to start" |
| `_bubble`, `_selection`, `_insertion`, `_merge`, `_quick`, `_heap` | `core/coach.py` | Text for one algorithm | `events` | Yields one `Coaching` per event | Tracks passes or sections |
| `current_coaching` | `core/sorting_runner.py` | Explanation for the current step | None | `Coaching` | Builds the list once |
| `begin_section` | `core/events.py` | Records the part being sorted | `lo`, `hi`, optional `mid` | Stored on later events | Merge and Quick Sort |
| `render_explanation` | `ui/explanations.py` | Draws the guide | `name: str` | Guide, facts, code and comparison table | `"Heap Sort"` |
| `_guide_html` | `ui/explanations.py` | Left column | `name: str` | HTML string | Summary, detailed steps, Use it when |
| `_facts_html` | `ui/explanations.py` | Right column | `name: str` | HTML string | Speed tiles, memory, strengths, weaknesses |
| `readable_source` | `ui/explanations.py` | Hides animation code | `source: str` | Valid Python as `str` | Removes `tracer.compare(...)` lines |
| `_render_code` | `ui/explanations.py` | The code section | `name: str` | Python or pseudocode | Chosen with the `code_view` control |
| `Event.label` | `core/events.py` | Short step text | The event | `str` using values | `"Compare 3 and 1"` |
| `_timer_delay` | `ui/visualizer.py` | Delay needed right now | Session state | `float`, or `None` when paused | Normal gives `0.2` |
| `_live_view` | `ui/visualizer.py` | Chart, bar, explanation | `timer: float or None` | Advances and draws | Restarts page if timer is wrong |
| `draw_array` | `ui/visualizer.py` | Draws the bars | `array`, `states`, `title`, `height`, `compact` | Matplotlib `Figure` | Preview uses `height=6.4, compact=True` |

## Design system: Clean Studio

One neutral background, one blue accent (`#1D5FD6`), and colour only where it means something. Use Streamlit's own options first, and CSS only for what they cannot do.

| Where | What it controls |
|---|---|
| `.streamlit/config.toml` | Page, text and border colours, light sidebar, Figtree font, corner radius, minimal toolbar |
| `width="stretch"` on buttons | Equal-width buttons |
| `st.segmented_control` | The input type selector; `required=True` means one is always chosen, and `wrap=True` keeps every option visible instead of scrolling |
| `ui/theme.py` | Sidebar navigation, heading size, algorithm rows, facts line |
| `TAGLINES` in `ui/setup.py` | Each algorithm's short description |

**Fitting the setup screen to the window:** Python cannot read the browser's window size, so `ui/theme.py` does it with CSS. `clamp(smallest, ideal, largest)` sizes the preview and the spacing of the algorithm rows from `100vh`, the window height, so both columns grow and shrink together. Each row stops growing at `4.5rem` so it does not look stretched, and any spare height goes into the gaps between rows. The preview uses `object-fit: contain`, which scales the picture without stretching the numbers.

**Sidebar:** the navigation is still a Streamlit radio, so the selected page stays in `st.session_state["page"]` as a plain name such as `"Visualizer"`. `format_func` only changes what is displayed, adding an icon from `PAGE_ICONS`. CSS hides the radio circles and stretches each option across the sidebar. `BRAND_HTML` builds the logo from three small bars.

**Clickable rows:** each row is a keyed container holding HTML and a real Streamlit button. The CSS makes the button invisible and stretches it across the row, so a click anywhere selects that algorithm while keyboard focus and tests still use a real button.

Bars show their value above them up to `MAX_LABELLED_BARS` (40 bars); beyond that the numbers would overlap. The app is fixed to its light theme because the palette is designed around it.

## Tests

`tests/test_setup_flow.py` drives the real app with Streamlit's `AppTest`. It covers opening on setup, card selection, starting, pausing, Change input, custom input (valid, invalid, remembered) and the Race page controls.

`tests/test_coach.py` checks that every event in every test array gets a complete explanation, and checks the exact wording on small arrays for all six algorithms.

`tests/test_explanations.py` checks each algorithm's page content, that the animation code is hidden, that the displayed code really sorts, and that the page has no tabs.

`AppTest` does not fire fragment timers, so the animation's timing still needs a check in the browser.

## Try it yourself

1. In `ui/controls.py`, add a `"Very Slow": (1.5, 1)` entry to `SPEEDS`. Where does it appear, and why did you not need to edit the slider?
2. Change the `[5, 8]` column ratio in `render_setup_page` to `[1, 1]`. What happens to the chart, and why does the original ratio suit this screen better?
3. Temporarily delete the `if _timer_delay() != timer` check in `_live_view`, then press Pause during playback. Explain what you see.
4. Change `begin_visualizing` so it sets `playing` to `False`. How does the first screen after setup change?
5. Add a test that pressing **Finish** leaves `playback.array` sorted.
6. Rewrite one sentence in `_bubble` in `core/coach.py`. Which test fails, and what is that test protecting?
7. On paper, follow `_quick` through `[1, 3, 2]`. Why does the message for `1` say it is already in place?
8. In `readable_source`, remove the check that skips empty blocks. Which algorithm's displayed code breaks, and why?
9. Remove the `tracer.begin_section` call from `_merge` in `algorithms/merge_sort.py`. Why does the coach crash, and why do the sorting tests for Merge Sort still pass?
