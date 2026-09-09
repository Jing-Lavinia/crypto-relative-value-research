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

