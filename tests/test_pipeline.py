from perpetual_rv_demo import run_synthetic_pipeline


def test_synthetic_pipeline_crosses_selected_control_boundary():
    result = run_synthetic_pipeline()
    assert result["execution_time"] > result["decision_time"]
    assert result["pair_legs"] == 4
    assert result["symbols"] == 4
    assert result["lifecycle_flattened_pairs"] == ["mr:AAA-BBB"]
    assert result["blocked_pairs"] == ["carry:CCC-DDD"]
    assert len(result["audit_payload_sha256"]) == 64
    assert result["reconciliation_passed"] is True
