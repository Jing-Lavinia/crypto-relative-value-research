from __future__ import annotations

from datetime import datetime
from typing import Iterable


def eligible_symbols(
    observations: Iterable[dict],
    decision_time: datetime,
    *,
    minimum_listing_days: int,
    minimum_completeness: float,
    universe_size: int,
) -> list[str]:
    """Select a historical universe from records observable by the decision."""
    latest: dict[str, dict] = {}
    for row in observations:
        if row["observed_at"] > decision_time:
            continue
        symbol = str(row["symbol"])
        if symbol not in latest or row["observed_at"] > latest[symbol]["observed_at"]:
            latest[symbol] = row

    accepted = []
    for symbol, row in latest.items():
        listing_age = (decision_time - row["listed_at"]).days
        if listing_age < minimum_listing_days:
            continue
        if float(row["completeness"]) < minimum_completeness:
            continue
        accepted.append((symbol, float(row["trailing_quote_volume"])))
    accepted.sort(key=lambda item: (-item[1], item[0]))
    return [symbol for symbol, _ in accepted[:universe_size]]

