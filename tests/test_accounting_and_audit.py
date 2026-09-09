import json

import pytest

from perpetual_rv_demo.accounting import (
    aggregate_portfolio,
    aggregate_symbols,
    build_leg_ledger,
    reconcile,
)
from perpetual_rv_demo.audit import write_immutable_record


def _ledger():
    return build_leg_ledger(
        sleeve_by_pair={"p1": "a", "p2": "b"},
        previous={},
        current={
            ("p1", "AAA"): 100.0,
            ("p1", "BBB"): -100.0,
            ("p2", "AAA"): 50.0,
            ("p2", "CCC"): -50.0,
        },
        simple_returns={"AAA": 0.01, "BBB": 0.0, "CCC": 0.0},
        funding_rates={"AAA": 0.001, "BBB": 0.0, "CCC": 0.0},
        one_way_cost_bps=10.0,
    )


def test_shared_symbol_is_aggregated_once():
    symbols = aggregate_symbols(_ledger())
    aaa = next(row for row in symbols if row["symbol"] == "AAA")
    assert aaa["position_notional"] == 150.0
    assert aaa["market_pnl"] == 1.5


def test_market_funding_cost_and_net_reconcile():
    legs = _ledger()
    symbols = aggregate_symbols(legs)
    portfolio = aggregate_portfolio(symbols)
    assert reconcile(legs, symbols, portfolio)
    assert portfolio["net_pnl"] == pytest.approx(
        portfolio["market_pnl"]
        + portfolio["funding_pnl"]
        - portfolio["trading_cost"]
    )


def test_audit_record_cannot_be_overwritten(tmp_path):
    path = tmp_path / "run.json"
    write_immutable_record(path, {"run": "synthetic", "passed": True})
    record = json.loads(path.read_text())
    assert len(record["payload_sha256"]) == 64
    with pytest.raises(FileExistsError):
        write_immutable_record(path, {"run": "replacement"})

