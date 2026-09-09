from __future__ import annotations

from collections import Counter, defaultdict


def apply_portfolio_constraints(
    targets: dict[tuple[str, str], float],
    *,
    equity: float,
    maximum_pair_gross: float,
    maximum_symbol_gross: float,
    maximum_total_gross: float,
    maximum_pairs_per_symbol: int,
) -> dict[tuple[str, str], float]:
    """Apply deterministic limits while preserving pair-leg proportions."""
    if equity <= 0:
        raise ValueError("equity must be positive")

    pair_symbols: dict[str, set[str]] = defaultdict(set)
    for pair_id, symbol in targets:
        pair_symbols[pair_id].add(symbol)

    accepted: set[str] = set()
    usage: Counter[str] = Counter()
    for pair_id in sorted(pair_symbols):
        symbols = pair_symbols[pair_id]
        if all(usage[symbol] < maximum_pairs_per_symbol for symbol in symbols):
            accepted.add(pair_id)
            usage.update(symbols)

    constrained = {
        key: float(value)
        for key, value in targets.items()
        if key[0] in accepted
    }

    for pair_id in sorted(accepted):
        keys = [key for key in constrained if key[0] == pair_id]
        gross = sum(abs(constrained[key]) for key in keys)
        limit = equity * maximum_pair_gross
        scale = min(1.0, limit / gross) if gross else 0.0
        for key in keys:
            constrained[key] *= scale

    for _ in range(10):
        symbol_gross: dict[str, float] = defaultdict(float)
        for (_, symbol), value in constrained.items():
            symbol_gross[symbol] += abs(value)
        scales = {
            symbol: min(1.0, equity * maximum_symbol_gross / gross)
            if gross else 0.0
            for symbol, gross in symbol_gross.items()
        }
        if all(scale >= 1.0 - 1e-12 for scale in scales.values()):
            break
        for key in constrained:
            constrained[key] *= scales[key[1]]

    total_gross = sum(abs(value) for value in constrained.values())
    total_limit = equity * maximum_total_gross
    if total_gross > total_limit:
        scale = total_limit / total_gross
        constrained = {key: value * scale for key, value in constrained.items()}
    return constrained

