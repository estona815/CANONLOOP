from dataclasses import dataclass
from typing import Generic, TypeVar

from .fixtures import (
    campaign_plan,
    failed_evaluation,
    generation_runs,
    project_brief,
    repair_plan,
    repaired_evaluation,
    visual_canon,
)
from .models import (
    CampaignPackage,
    CampaignPlan,
    ContinuityEvaluation,
    Decision,
    GenerationRun,
    ProjectBrief,
    RepairPlan,
    VisualCanon,
)

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


@dataclass(frozen=True)
class AgentSpec:
    name: str
    input_contract: str
    output_contract: str
    allowed_tools: tuple[str, ...]
    failure_conditions: tuple[str, ...]
    retry_policy: str
    approval_boundary: str


class BoundedAgent(Generic[InputT, OutputT]):
    spec: AgentSpec

    def run(self, value: InputT) -> OutputT:
        raise NotImplementedError


class IntakeAgent(BoundedAgent[dict[str, object], ProjectBrief]):
    spec = AgentSpec(
        "Intake",
        "RawBrief",
        "ProjectBrief",
        ("schema-validator",),
        ("rights not confirmed",),
        "no automatic retry",
        "rights confirmation",
    )

    def run(self, value: dict[str, object]) -> ProjectBrief:
        brief = project_brief()
        if not value.get("rightsConfirmed", brief.rights_confirmed):
            raise PermissionError("Reference rights must be confirmed")
        return brief


class CanonBuilderAgent(BoundedAgent[ProjectBrief, VisualCanon]):
    spec = AgentSpec(
        "Canon Builder",
        "ProjectBrief",
        "VisualCanon",
        ("reference-reader", "schema-validator"),
        ("no usable references",),
        "one clarification",
        "human canon approval",
    )

    def run(self, value: ProjectBrief) -> VisualCanon:
        if not value.reference_assets:
            raise ValueError("At least one reference is required")
        return visual_canon()


class CampaignPlannerAgent(BoundedAgent[VisualCanon, CampaignPlan]):
    spec = AgentSpec(
        "Campaign Planner",
        "VisualCanon",
        "CampaignPlan",
        ("cost-estimator",),
        ("budget exceeded",),
        "one bounded re-plan",
        "plan approval",
    )

    def run(self, value: VisualCanon) -> CampaignPlan:
        if not value.user_approved:
            raise PermissionError("Visual Canon must be approved")
        return campaign_plan()


class GenerationAgent(BoundedAgent[CampaignPlan, list[GenerationRun]]):
    spec = AgentSpec(
        "Generation",
        "CampaignPlan",
        "GenerationRun[]",
        ("genblaze-pipeline", "provider", "sink"),
        ("cost cap", "provider timeout", "missing manifest"),
        "two attempts per asset",
        "live cost confirmation",
    )

    def run(self, value: CampaignPlan) -> list[GenerationRun]:
        if value.total_retry_budget > 16:
            raise ValueError("Retry budget exceeds policy")
        return generation_runs()


class ContinuityCriticAgent(BoundedAgent[GenerationRun, ContinuityEvaluation]):
    spec = AgentSpec(
        "Continuity Critic",
        "GenerationRun",
        "ContinuityEvaluation",
        ("deterministic-checks", "critic"),
        ("missing asset", "invalid manifest"),
        "no score retry",
        "human override",
    )

    def run(self, value: GenerationRun) -> ContinuityEvaluation:
        return repaired_evaluation() if value.parent_run_id else failed_evaluation()


class RepairAgent(BoundedAgent[ContinuityEvaluation, RepairPlan]):
    spec = AgentSpec(
        "Repair",
        "ContinuityEvaluation",
        "RepairPlan",
        ("prompt-patcher",),
        ("non-repairable finding", "retry exhausted"),
        "maximum two repairs",
        "third failure requires human",
    )

    def run(self, value: ContinuityEvaluation) -> RepairPlan:
        if value.decision != Decision.REJECT or not all(
            finding.repairable for finding in value.drift_findings
        ):
            raise ValueError("Evaluation does not permit automatic repair")
        return repair_plan()


class ProvenanceArchivistAgent(BoundedAgent[list[GenerationRun], list[str]]):
    spec = AgentSpec(
        "Provenance Archivist",
        "GenerationRun[]",
        "ManifestIndex",
        ("manifest-verifier", "b2-adapter"),
        ("hash mismatch", "storage failure"),
        "one storage retry",
        "never claim unverified storage",
    )

    def run(self, value: list[GenerationRun]) -> list[str]:
        return [run.manifest_uri for run in value if run.manifest_verified]


class ReleasePackagerAgent(BoundedAgent[list[GenerationRun], CampaignPackage]):
    spec = AgentSpec(
        "Release Packager",
        "GenerationRun[]",
        "CampaignPackage",
        ("zip-packager",),
        ("rejected asset in release", "unsafe archive path"),
        "no retry after validation error",
        "approved assets only",
    )

    def run(self, value: list[GenerationRun]) -> CampaignPackage:
        approved = [run.asset_id for run in value if run.status.value in {"approved", "repaired"}]
        rejected = [run.asset_id for run in value if run.status.value == "failed"]
        return CampaignPackage(
            package_id="package-six-line-halo-v1",
            project_id="six-line-halo",
            approved_asset_ids=approved,
            rejected_asset_ids=rejected,
            canon_version=1,
            manifest_index=[run.manifest_uri for run in value],
            continuity_report="continuity-report.json",
            provenance_report="provenance-report.json",
            zip_uri="/api/package",
        )


AGENT_SPECS = [
    IntakeAgent.spec,
    CanonBuilderAgent.spec,
    CampaignPlannerAgent.spec,
    GenerationAgent.spec,
    ContinuityCriticAgent.spec,
    RepairAgent.spec,
    ProvenanceArchivistAgent.spec,
    ReleasePackagerAgent.spec,
]
