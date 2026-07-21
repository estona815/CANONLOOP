import pytest
from canonloop.agents import (
    AGENT_SPECS,
    CampaignPlannerAgent,
    CanonBuilderAgent,
    ContinuityCriticAgent,
    GenerationAgent,
    IntakeAgent,
    ProvenanceArchivistAgent,
    ReleasePackagerAgent,
    RepairAgent,
)
from canonloop.models import Decision


def test_eight_agents_have_operational_specs() -> None:
    assert len(AGENT_SPECS) == 8
    assert all(spec.allowed_tools and spec.failure_conditions for spec in AGENT_SPECS)


def test_intake_requires_rights() -> None:
    with pytest.raises(PermissionError):
        IntakeAgent().run({"rightsConfirmed": False})


def test_full_agent_vertical_slice() -> None:
    brief = IntakeAgent().run({"rightsConfirmed": True})
    canon = CanonBuilderAgent().run(brief)
    plan = CampaignPlannerAgent().run(canon)
    runs = GenerationAgent().run(plan)
    failed = next(run for run in runs if run.run_id == "run-007")
    evaluation = ContinuityCriticAgent().run(failed)
    repair = RepairAgent().run(evaluation)
    index = ProvenanceArchivistAgent().run(runs)
    package = ReleasePackagerAgent().run(runs)
    assert evaluation.decision == Decision.REJECT
    assert repair.source_run_id == "run-007"
    assert len(index) == 5
    assert len(package.approved_asset_ids) == 4
