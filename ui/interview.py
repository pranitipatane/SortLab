"""Interview Mode: multiple-choice questions with a score."""
from __future__ import annotations

import random

import streamlit as st

from core.sorting_runner import ALGORITHMS
from data.questions import GENERAL, QUESTIONS

ROUND_SIZE = 10
ALL = "All algorithms"


def _build_round(topic: str) -> list[dict]:
    """Pick questions for a round and shuffle the answer options."""
    if topic == ALL:
        pool = list(QUESTIONS)
        chosen = random.sample(pool, min(ROUND_SIZE, len(pool)))
    else:
        specific = [q for q in QUESTIONS if q[0] == topic]
        general = [q for q in QUESTIONS if q[0] == GENERAL]
        chosen = specific + random.sample(general, min(ROUND_SIZE - len(specific), len(general)))
        random.shuffle(chosen)
    items = []
    for _, question, options, correct, explanation in chosen:
        order = list(range(len(options)))
        random.shuffle(order)
        items.append({"question": question, "options": [options[i] for i in order],
                      "answer": order.index(correct), "explanation": explanation})
    return items


def _start(topic: str) -> None:
    st.session_state["iv"] = {"items": _build_round(topic), "index": 0, "correct": 0,
                              "answered": 0, "submitted": False, "round": random.random()}


def _summary(correct: int, total: int) -> str:
    ratio = correct / total
    if ratio >= 0.9:
        return "Strong grasp of sorting fundamentals."
    if ratio >= 0.7:
        return "Good understanding, with a few topics worth reviewing."
    if ratio >= 0.5:
        return "Some gaps. Revisit the Learn page and the algorithm explanations."
    return "Keep practising. Try the visualizer and Learn page, then retry."


def render_interview_page() -> None:
    """Start screen, question flow and final score."""
    ss = st.session_state
    st.header("Interview Mode")
    iv = ss.get("iv")
    if iv is None:
        st.write("Answer multiple-choice questions like those asked in software-engineering interviews.")
        topic = st.selectbox("Topic", [ALL] + list(ALGORITHMS))
        st.button("Start interview", type="primary", on_click=_start, args=(topic,))
        return

    items, idx = iv["items"], iv["index"]
    total = len(items)
    c = st.columns(3)
    c[0].metric("Questions answered", f"{iv['answered']} / {total}")
    c[1].metric("Correct answers", iv["correct"])
    c[2].metric("Score", f"{iv['correct']} / {total}")

    if idx >= total:
        st.subheader("Interview Score")
        st.markdown(f"## {iv['correct']} / {total}")
        st.write(_summary(iv["correct"], total))
        st.button("Start a new interview", on_click=lambda: ss.pop("iv"))
        return

    item = items[idx]
    st.progress(idx / total, text=f"Question {idx + 1} of {total}")
    st.subheader(item["question"])
    choice = st.radio("Choose one answer", item["options"], index=None,
                      key=f"iv_{iv['round']}_{idx}", disabled=iv["submitted"])

    def submit() -> None:
        pick = st.session_state[f"iv_{iv['round']}_{idx}"]
        iv["submitted"] = True
        iv["answered"] += 1
        iv["correct"] += int(item["options"].index(pick) == item["answer"])

    def advance() -> None:
        iv["index"] += 1
        iv["submitted"] = False

    if not iv["submitted"]:
        st.button("Submit answer", on_click=submit, disabled=choice is None)
        return
    if item["options"].index(choice) == item["answer"]:
        st.success("Correct! " + item["explanation"])
    else:
        st.error(f"Not quite. Correct answer: **{item['options'][item['answer']]}**. {item['explanation']}")
    st.button("Next question" if idx + 1 < total else "See final score", on_click=advance)
