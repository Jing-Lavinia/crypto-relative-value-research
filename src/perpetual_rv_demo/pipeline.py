from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .audit import stable_hash
from .accounting import (
    aggregate_portfolio,
    aggregate_symbols,
    build_leg_ledger,
    reconcile,
)
from .execution import execute_whole_pairs
from .information_clock import next_open_after
from .lifecycle import flatten_known_inactive_pairs
from .portfolio import apply_portfolio_constraints
from .signal_interfaces import synthetic_signal_provider
from .universe import eligible_symbols


def run_synthetic_pipeline() -> dict:
    """Run a small example through the selected public control boundary."""
    utc = timezone.utc
    decision_time = datetime(2026, 1, 5, 12, tzinfo=utc)
    market_opens = [decision_time, decision_time + timedelta(hours=1)]
    execution_time = next_open_after(decision_time, market_opens)

    observations = [
        {
            "symbol": symbol,
            "listed_at": decision_time - timedelta(days=365),
            "observed_at": decision_time,
            "trailing_quote_volume": volume,
            "completeness": 1.0,
        }
        for symbol, volume in {
            "AAA": 500.0,
            "BBB": 400.0,
            "CCC": 300.0,
            "DDD": 200.0,
            "EEE": 100.0,
        }.items()
    ]
    eligible = set(
        eligible_symbols(
            observations,
            decision_time,
            minimum_listing_days=180,
            minimum_completeness=0.995,
            universe_size=4,
        )
    )
    sleeves, raw_targets = synthetic_signal_provider(eligible, decision_time)
    events = [
        {
            "symbol": "AAA",
            "announced_at": decision_time - timedelta(days=1),
            "exit_at": decision_time + timedelta(days=1),
        }
    ]
    lifecycle_targets = flatten_known_inactive_pairs(
        raw_targets, events, decision_time
    )
    constrained = apply_portfolio_constraints(
        lifecycle_targets,
        equity=1_000_000.0,
        maximum_pair_gross=0.20,
        maximum_symbol_gross=0.15,
        maximum_total_gross=0.60,
        maximum_pairs_per_symbol=2,
    )
    previous = {
        ("mr:AAA-BBB", "AAA"): 60_000.0,
        ("mr:AAA-BBB", "BBB"): -60_000.0,
        ("carry:CCC-DDD", "CCC"): 50_000.0,
        ("carry:CCC-DDD", "DDD"): -50_000.0,
    }
    positions, blocked = execute_whole_pairs(
        constrained,
        previous=previous,
        executable_volume={
            "AAA": 10.0,
            "BBB": 8.0,
            "CCC": 12.0,
            "DDD": 0.0,
        },
    )
    legs = build_leg_ledger(
        sleeve_by_pair=sleeves,
        previous=previous,
        current=positions,
        simple_returns={
            "AAA": 0.004,
            "BBB": 0.001,
            "CCC": -0.001,
            "DDD": 0.002,
        },
        funding_rates={
            "AAA": 0.0,
            "BBB": 0.0,
            "CCC": -0.0002,
            "DDD": 0.0003,
        },
        one_way_cost_bps=7.0,
    )
    symbols = aggregate_symbols(legs)
    portfolio = aggregate_portfolio(symbols)
    passed = reconcile(legs, symbols, portfolio)
    flattened_pairs = sorted(
        {
            pair_id
            for (pair_id, symbol), target in raw_targets.items()
            if target != lifecycle_targets[(pair_id, symbol)]
        }
    )
    result = {
        "decision_time": decision_time.isoformat(),
        "execution_time": execution_time.isoformat(),
        "blocked_pairs": sorted(blocked),
        "lifecycle_flattened_pairs": flattened_pairs,
        "eligible_symbols": sorted(eligible),
        "pair_legs": len(legs),
        "symbols": len(symbols),
        "portfolio": portfolio,
        "reconciliation_passed": passed,
    }
    return {**result, "audit_payload_sha256": stable_hash(result)}
