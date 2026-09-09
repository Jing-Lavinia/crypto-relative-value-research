from __future__ import annotations

from collections import defaultdict
from math import isclose


def build_leg_ledger(
    *,
    sleeve_by_pair: dict[str, str],
    previous: dict[tuple[str, str], float],
    current: dict[tuple[str, str], float],
    simple_returns: dict[str, float],
    funding_rates: dict[str, float],
    one_way_cost_bps: float,
) -> list[dict]:
    """Calculate one-period market, funding, cost, and net P&L by pair leg."""
    rows: list[dict] = []
    for pair_id, symbol in sorted(set(previous) | set(current)):
        prior_notional = float(previous.get((pair_id, symbol), 0.0))
        current_notional = float(current.get((pair_id, symbol), 0.0))
        traded_notional = abs(current_notional - prior_notional)
        market_pnl = current_notional * float(simple_returns.get(symbol, 0.0))
        funding_pnl = -current_notional * float(funding_rates.get(symbol, 0.0))
        trading_cost = traded_notional * float(one_way_cost_bps) / 10_000.0
        rows.append(
            {
                "sleeve": sleeve_by_pair[pair_id],
                "pair_id": pair_id,
                "symbol": symbol,
                "position_notional": current_notional,
                "market_pnl": market_pnl,
                "funding_pnl": funding_pnl,
                "trading_cost": trading_cost,
                "net_pnl": market_pnl + funding_pnl - trading_cost,
            }
        )
    return rows


def aggregate_symbols(leg_rows: list[dict]) -> list[dict]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in leg_rows:
        symbol = row["symbol"]
        for field in (
            "position_notional",
            "market_pnl",
            "funding_pnl",
            "trading_cost",
            "net_pnl",
        ):
            totals[symbol][field] += float(row[field])
    return [
        {"symbol": symbol, **dict(values)}
        for symbol, values in sorted(totals.items())
    ]


def aggregate_portfolio(symbol_rows: list[dict]) -> dict[str, float]:
    fields = ("market_pnl", "funding_pnl", "trading_cost", "net_pnl")
    return {
        field: sum(float(row[field]) for row in symbol_rows)
        for field in fields
    }


def reconcile(leg_rows: list[dict], symbol_rows: list[dict], portfolio: dict) -> bool:
    leg_total = sum(float(row["net_pnl"]) for row in leg_rows)
    symbol_total = sum(float(row["net_pnl"]) for row in symbol_rows)
    expected = (
        float(portfolio["market_pnl"])
        + float(portfolio["funding_pnl"])
        - float(portfolio["trading_cost"])
    )
    return (
        isclose(leg_total, symbol_total, abs_tol=1e-8)
        and isclose(symbol_total, float(portfolio["net_pnl"]), abs_tol=1e-8)
        and isclose(float(portfolio["net_pnl"]), expected, abs_tol=1e-8)
    )

