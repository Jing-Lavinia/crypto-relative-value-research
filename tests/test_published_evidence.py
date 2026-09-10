import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]


def test_published_attribution_reconciles():
    evidence = json.loads(
        (ROOT / "evidence" / "frozen_summary.json").read_text()
    )
    attribution = evidence["terminal"]["attribution_7bps_usd"]
    assert attribution["net_pnl"] == pytest.approx(
        attribution["market_pnl"]
        + attribution["funding_pnl"]
        - attribution["trading_cost"],
        abs=0.02,
    )


def test_readme_headlines_match_machine_readable_evidence():
    evidence = json.loads(
        (ROOT / "evidence" / "frozen_summary.json").read_text()
    )
    readme = (ROOT / "README.md").read_text()
    development = evidence["development"]["cost_scenarios"]["7bps"]
    terminal = evidence["terminal"]["cost_scenarios"]["7bps"]
    expected = {
        f"{development['total_return']:.2%}",
        f"{development['cagr']:.2%}",
        f"{development['sharpe']:.2f}",
        f"{development['maximum_drawdown']:.2%}",
        f"{terminal['total_return']:+.2%}",
    }
    assert all(value in readme for value in expected)


def test_all_published_cost_scenarios_match_readme():
    evidence = json.loads(
        (ROOT / "evidence" / "frozen_summary.json").read_text()
    )
    readme = (ROOT / "README.md").read_text()
    for section in ("development", "terminal"):
        for metrics in evidence[section]["cost_scenarios"].values():
            assert f"{metrics['total_return']:+.2%}" in readme or (
                section == "terminal"
                and abs(metrics["total_return"]) < 0.001
                and f"{metrics['total_return']:+.3%}" in readme
            )
            assert f"{metrics['sharpe']:.2f}" in readme
            assert f"{metrics['maximum_drawdown']:.2%}" in readme


def test_published_scale_and_governance_are_explicit():
    evidence = json.loads(
        (ROOT / "evidence" / "frozen_summary.json").read_text()
    )
    readme = (ROOT / "README.md").read_text()
    data_state = evidence["data_state"]
    assert f"{data_state['verified_official_objects']:,}" in readme
    assert f"{data_state['accepted_hourly_kline_rows']:,}" in readme
    assert evidence["development"]["promotion_mode"] == (
        "reviewed_practical_thresholds"
    )
    assert evidence["development"]["original_performance_gates_all_passed"] is False
