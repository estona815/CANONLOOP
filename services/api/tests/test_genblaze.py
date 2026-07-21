from canonloop.genblaze_integration import run_no_key_contract


def test_real_genblaze_pipeline_and_agent_loop_no_key() -> None:
    evidence = run_no_key_contract()
    assert evidence.core_version == "0.3.6"
    assert evidence.pipeline_completed
    assert evidence.pipeline_manifest_verified
    assert len(evidence.pipeline_canonical_hash) == 64
    assert evidence.agent_loop_passed
    assert evidence.agent_loop_iterations == 2
    assert evidence.parent_linked
    assert evidence.provider == "mock"
