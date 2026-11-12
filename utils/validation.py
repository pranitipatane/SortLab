"""Safe parsing and validation of user input."""
from __future__ import annotations

import re
from dataclasses import dataclass

_SEPARATORS = re.compile(r"[,;\s]+")
_INTEGER = re.compile(r"[+-]?\d+")
_DECIMAL = re.compile(r"[+-]?\d*\.\d+")

MAX_CUSTOM_ELEMENTS = 100
MIN_CUSTOM_ELEMENTS = 2
MAX_ABS_VALUE = 1_000_000
MAX_BENCHMARK_SIZE = 1000
BENCHMARK_SIZE_OPTIONS = [10, 25, 50, 100, 250, 500, 1000]


@dataclass
class ParseResult:
    """Either ``values`` (success) or ``error`` (a friendly message)."""

    values: list[int] | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


def parse_custom_array(text: str | None) -> ParseResult:
    """Parse input such as ``"64, 12, 90, 34"`` into a list of integers."""
    if text is None or not text.strip():
        return ParseResult(error="❌ The input is empty. Please enter numbers separated by commas.")
    cleaned = text.strip().strip("[]").strip()
    tokens = [t for t in _SEPARATORS.split(cleaned) if t]
    if not tokens:
        return ParseResult(error="❌ Please enter numbers separated by commas.")
    if len(tokens) > MAX_CUSTOM_ELEMENTS:
        return ParseResult(error=f"❌ Too many elements ({len(tokens)}). The maximum is {MAX_CUSTOM_ELEMENTS}.")

    values: list[int] = []
    for token in tokens:
        if _INTEGER.fullmatch(token):
            value = int(token)
        elif _DECIMAL.fullmatch(token):
            return ParseResult(error=f"❌ '{token}' is a decimal. Please use whole numbers only.")
        else:
            return ParseResult(error=f"❌ '{token}' is not a number. Please enter numbers separated by commas.")
        if abs(value) > MAX_ABS_VALUE:
            return ParseResult(error=f"❌ {token} is too large. Values must be between "
                                     f"-{MAX_ABS_VALUE:,} and {MAX_ABS_VALUE:,}.")
        values.append(value)

    if len(values) < MIN_CUSTOM_ELEMENTS:
        return ParseResult(error=f"❌ Please enter at least {MIN_CUSTOM_ELEMENTS} numbers.")
    return ParseResult(values=values)


def validate_benchmark_sizes(sizes: list[int]) -> str | None:
    """Return an error message, or ``None`` if the sizes are acceptable."""
    if not sizes:
        return "❌ Please select at least one array size."
    for size in sizes:
        if not isinstance(size, int) or size < 1:
            return f"❌ Invalid size: {size}. Sizes must be positive whole numbers."
        if size > MAX_BENCHMARK_SIZE:
            return f"❌ Size {size} is too large. The maximum is {MAX_BENCHMARK_SIZE}."
    return None
