from datetime import datetime, timedelta, timezone

import pytest

from perpetual_rv_demo.information_clock import history_available_at, next_open_after
from perpetual_rv_demo.lifecycle import flatten_known_inactive_pairs
from perpetual_rv_demo.universe import eligible_symbols


def test_decision_uses_only_available_history():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = [
        {"timestamp": now - timedelta(hours=1), "value": 1},
        {"timestamp": now + timedelta(hours=1), "value": 999},
    ]
    assert history_available_at(rows, now) == [rows[0]]


def test_signal_executes_strictly_after_decision():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert next_open_after(now, [now, now + timedelta(hours=1)]) > now


def test_missing_future_open_is_rejected():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        next_open_after(now, [now])


def test_known_delisting_flattens_both_pair_legs():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    targets = {("p1", "AAA"): 10.0, ("p1", "BBB"): -10.0}
    events = [
        {
            "symbol": "AAA",
            "announced_at": now - timedelta(days=1),
            "exit_at": now,
        }
    ]
    assert set(flatten_known_inactive_pairs(targets, events, now).values()) == {
        0.0
    }


def test_future_observation_does_not_change_past_universe():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    base = [
        {
            "symbol": "AAA",
            "listed_at": now - timedelta(days=365),
            "observed_at": now,
            "trailing_quote_volume": 10.0,
            "completeness": 1.0,
        },
        {
            "symbol": "BBB",
            "listed_at": now - timedelta(days=365),
            "observed_at": now,
            "trailing_quote_volume": 9.0,
            "completeness": 1.0,
        },
    ]
    future = {
        "symbol": "BBB",
        "listed_at": now - timedelta(days=365),
        "observed_at": now + timedelta(days=1),
        "trailing_quote_volume": 999.0,
        "completeness": 1.0,
    }
    kwargs = {
        "minimum_listing_days": 180,
        "minimum_completeness": 0.995,
        "universe_size": 1,
    }
    assert eligible_symbols(base, now, **kwargs) == eligible_symbols(
        base + [future], now, **kwargs
    )


def test_listing_age_and_completeness_are_enforced():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = [
        {
            "symbol": "OLD",
            "listed_at": now - timedelta(days=365),
            "observed_at": now,
            "trailing_quote_volume": 10.0,
            "completeness": 1.0,
        },
        {
            "symbol": "NEW",
            "listed_at": now - timedelta(days=10),
            "observed_at": now,
            "trailing_quote_volume": 100.0,
            "completeness": 1.0,
        },
        {
            "symbol": "GAP",
            "listed_at": now - timedelta(days=365),
            "observed_at": now,
            "trailing_quote_volume": 200.0,
            "completeness": 0.90,
        },
    ]
    assert eligible_symbols(
        rows,
        now,
        minimum_listing_days=180,
        minimum_completeness=0.995,
        universe_size=5,
    ) == ["OLD"]
