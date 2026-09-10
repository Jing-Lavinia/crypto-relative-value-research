from __future__ import annotations

from datetime import datetime
from typing import Iterable


def known_inactive_symbols(
    events: Iterable[dict], decision_time: datetime
) -> set[str]:
    """Return symbols with a delisting announcement known at decision time.

    A known announcement blocks new exposure even when the scheduled exit is
    still in the future. The execution layer determines when a held position
    can actually be flattened.
    """
    return {
        str(event["symbol"])
        for event in events
        if event["announced_at"] <= decision_time
    }


def flatten_known_inactive_pairs(
    targets: dict[tuple[str, str], float],
    events: Iterable[dict],
    decision_time: datetime,
) -> dict[tuple[str, str], float]:
    """Set both pair targets to zero after either leg's exit is announced."""
    inactive = known_inactive_symbols(events, decision_time)
    affected_pairs = {
        pair_id for pair_id, symbol in targets if symbol in inactive
    }
    return {
        key: (0.0 if key[0] in affected_pairs else notional)
        for key, notional in targets.items()
    }
