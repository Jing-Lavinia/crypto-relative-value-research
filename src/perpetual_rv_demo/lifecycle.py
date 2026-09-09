from __future__ import annotations

from datetime import datetime
from typing import Iterable


def known_inactive_symbols(
    events: Iterable[dict], decision_time: datetime
) -> set[str]:
    """Return symbols whose exit requirement was known by the decision time."""
    return {
        str(event["symbol"])
        for event in events
        if event["announced_at"] <= decision_time
        and event["exit_at"] <= decision_time
    }


def flatten_known_inactive_pairs(
    targets: dict[tuple[str, str], float],
    events: Iterable[dict],
    decision_time: datetime,
) -> dict[tuple[str, str], float]:
    """Flatten an entire pair if either leg is known to be inactive."""
    inactive = known_inactive_symbols(events, decision_time)
    affected_pairs = {
        pair_id for pair_id, symbol in targets if symbol in inactive
    }
    return {
        key: (0.0 if key[0] in affected_pairs else notional)
        for key, notional in targets.items()
    }

