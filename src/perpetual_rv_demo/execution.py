from __future__ import annotations

from collections import defaultdict


def execute_whole_pairs(
    targets: dict[tuple[str, str], float],
    previous: dict[tuple[str, str], float],
    executable_volume: dict[str, float],
) -> tuple[dict[tuple[str, str], float], set[str]]:
    """Carry a whole pair when either current or prior leg cannot execute."""
    pair_symbols: dict[str, set[str]] = defaultdict(set)
    for pair_id, symbol in set(targets) | set(previous):
        pair_symbols[pair_id].add(symbol)

    executed: dict[tuple[str, str], float] = {}
    blocked: set[str] = set()
    for pair_id, symbols in sorted(pair_symbols.items()):
        available = all(executable_volume.get(symbol, 0.0) > 0.0 for symbol in symbols)
        if not available:
            blocked.add(pair_id)
            for key, value in previous.items():
                if key[0] == pair_id:
                    executed[key] = value
            continue
        for symbol in symbols:
            key = (pair_id, symbol)
            executed[key] = float(targets.get(key, 0.0))
    return executed, blocked

