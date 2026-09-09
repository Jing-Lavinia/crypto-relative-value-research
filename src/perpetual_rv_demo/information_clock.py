from __future__ import annotations

from bisect import bisect_right
from datetime import datetime
from typing import Iterable


def next_open_after(decision_time: datetime, market_opens: Iterable[datetime]) -> datetime:
    """Return the first market open strictly after a decision timestamp."""
    ordered = sorted(set(market_opens))
    index = bisect_right(ordered, decision_time)
    if index >= len(ordered):
        raise ValueError("no eligible market open after decision time")
    execution_time = ordered[index]
    if execution_time <= decision_time:
        raise AssertionError("execution must be strictly after the decision")
    return execution_time


def history_available_at(rows: Iterable[dict], decision_time: datetime) -> list[dict]:
    """Restrict arbitrary timestamped rows to the information set at a decision."""
    return [row for row in rows if row["timestamp"] <= decision_time]

