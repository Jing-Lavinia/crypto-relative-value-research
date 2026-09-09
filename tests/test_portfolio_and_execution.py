from perpetual_rv_demo.execution import execute_whole_pairs
from perpetual_rv_demo.portfolio import apply_portfolio_constraints


def test_pair_cap_preserves_leg_proportions():
    targets = {("p1", "AAA"): 80.0, ("p1", "BBB"): -40.0}
    result = apply_portfolio_constraints(
        targets,
        equity=100.0,
        maximum_pair_gross=0.60,
        maximum_symbol_gross=1.0,
        maximum_total_gross=1.0,
        maximum_pairs_per_symbol=2,
    )
    assert result[("p1", "AAA")] == 40.0
    assert result[("p1", "BBB")] == -20.0


def test_symbol_overlap_limit_is_enforced():
    targets = {
        ("p1", "AAA"): 10.0,
        ("p1", "BBB"): -10.0,
        ("p2", "AAA"): 10.0,
        ("p2", "CCC"): -10.0,
    }
    result = apply_portfolio_constraints(
        targets,
        equity=100.0,
        maximum_pair_gross=1.0,
        maximum_symbol_gross=1.0,
        maximum_total_gross=2.0,
        maximum_pairs_per_symbol=1,
    )
    assert {pair_id for pair_id, _ in result} == {"p1"}


def test_zero_volume_carries_both_prior_legs():
    previous = {("p1", "AAA"): 20.0, ("p1", "BBB"): -20.0}
    targets = {("p1", "AAA"): 30.0, ("p1", "BBB"): -30.0}
    executed, blocked = execute_whole_pairs(
        targets, previous, {"AAA": 100.0, "BBB": 0.0}
    )
    assert executed == previous
    assert blocked == {"p1"}

