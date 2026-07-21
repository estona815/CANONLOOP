import pytest
from canonloop.fixtures import (
    campaign_plan,
    failed_evaluation,
    generation_runs,
    project_brief,
    repair_plan,
    repaired_evaluation,
    visual_canon,
)
from canonloop.models import ContinuityEvaluation, Decision
from pydantic import ValidationError


def test_project_brief_contract() -> None:
    assert project_brief().rights_confirmed is True


def test_visual_canon_has_five_anchors() -> None:
    assert len(visual_canon().identity_anchors) == 5


def test_campaign_plan_has_four_formats() -> None:
    assert len(campaign_plan().assets) == 4


def test_generation_runs_include_parent_link() -> None:
    repaired = next(run for run in generation_runs() if run.run_id == "run-007r")
    assert repaired.parent_run_id == "run-007"


def test_failed_evaluation_is_rejected() -> None:
    assert failed_evaluation().decision == Decision.REJECT


def test_repaired_evaluation_meets_thresholds() -> None:
    evaluation = repaired_evaluation()
    assert evaluation.decision == Decision.APPROVE
    assert evaluation.symbol_score >= 0.9


def test_invalid_approval_is_rejected() -> None:
    payload = repaired_evaluation().model_dump()
    payload["symbol_score"] = 0.3
    with pytest.raises(ValidationError):
        ContinuityEvaluation.model_validate(payload)


def test_repair_plan_is_bounded() -> None:
    assert repair_plan().retry_number <= 2
