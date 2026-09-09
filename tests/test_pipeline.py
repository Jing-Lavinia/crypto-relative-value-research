from perpetual_rv_demo import run_synthetic_pipeline


def test_synthetic_pipeline_crosses_full_control_boundary():
    result = run_synthetic_pipeline()
    assert result["execution_time"] > result["decision_time"]
    assert result["pair_legs"] == 4
    assert result["symbols"] == 4
    assert result["reconciliation_passed"] is True

