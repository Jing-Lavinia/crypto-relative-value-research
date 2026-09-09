from __future__ import annotations

from datetime import datetime
from typing import Callable


TargetMap = dict[tuple[str, str], float]
SignalProvider = Callable[[set[str], datetime], tuple[dict[str, str], TargetMap]]


def synthetic_signal_provider(
    eligible: set[str], decision_time: datetime
) -> tuple[dict[str, str], TargetMap]:
    """Return deterministic targets while keeping empirical signals private."""
    del decision_time
    required = {"AAA", "BBB", "CCC", "DDD"}
    if not required.issubset(eligible):
        return {}, {}
    sleeves = {
        "mr:AAA-BBB": "mean_reversion",
        "carry:CCC-DDD": "funding_carry",
    }
    targets = {
        ("mr:AAA-BBB", "AAA"): 80_000.0,
        ("mr:AAA-BBB", "BBB"): -80_000.0,
        ("carry:CCC-DDD", "CCC"): 70_000.0,
        ("carry:CCC-DDD", "DDD"): -70_000.0,
    }
    return sleeves, targets

