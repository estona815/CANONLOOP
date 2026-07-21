from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator
from pydantic.alias_generators import to_camel


class Contract(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


class Decision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


class AssetStatus(StrEnum):
    PLANNED = "planned"
    GENERATED = "generated"
    FAILED = "failed"
    REPAIRED = "repaired"
    APPROVED = "approved"


class IdentityAnchor(Contract):
    id: str
    category: str
    description: str
    importance: float = Field(ge=0, le=1)
    source_asset_id: str
    visual_region: str
    verification_method: str
    tolerance: float = Field(ge=0, le=1)


class ProjectBrief(Contract):
    project_id: str
    title: str
    campaign_name: str
    audience: str
    objective: str
    deliverables: list[str] = Field(min_length=1, max_length=8)
    reference_assets: list[str] = Field(min_length=1, max_length=8)
    brand_notes: str
    prohibited_content: list[str]
    budget: float = Field(gt=0, le=100)
    provider_preference: str
    rights_confirmed: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class VisualCanon(Contract):
    canon_id: str
    project_id: str
    identity_anchors: list[IdentityAnchor] = Field(min_length=1)
    mutable_attributes: list[str]
    fixed_attributes: list[str] = Field(min_length=1)
    color_palette: list[str] = Field(min_length=3)
    wardrobe_rules: list[str]
    symbol_rules: list[str]
    lighting_rules: list[str]
    style_rules: list[str]
    composition_rules: list[str]
    forbidden_changes: list[str]
    source_references: list[str]
    confidence: float = Field(ge=0, le=1)
    user_approved: bool
    version: int = Field(ge=1)


class AssetBrief(Contract):
    asset_id: str
    title: str
    purpose: str
    modality: str = "image"
    aspect_ratio: str
    dimensions: tuple[int, int]
    prompt: str = Field(min_length=1, max_length=6_000)
    negative_prompt: str
    required_anchors: list[str]
    optional_elements: list[str]
    safe_areas: list[str]
    priority: int = Field(ge=1, le=8)
    retry_budget: int = Field(ge=0, le=2)
    status: AssetStatus = AssetStatus.PLANNED


class CampaignPlan(Contract):
    plan_id: str
    project_id: str
    assets: list[AssetBrief] = Field(min_length=1, max_length=8)
    generation_order: list[str]
    shared_prompt_prefix: str
    global_negative_constraints: list[str]
    total_retry_budget: int = Field(ge=0, le=16)
    estimated_cost: float | None = Field(default=None, ge=0)
    status: str


class GeneratedAsset(Contract):
    asset_id: str
    run_id: str
    url: str
    b2_object_key: str
    mime_type: str
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    size_bytes: int = Field(gt=0)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    thumbnail_url: str
    provenance_uri: str
    status: AssetStatus


class GenerationRun(Contract):
    run_id: str
    parent_run_id: str | None = None
    project_id: str
    asset_id: str
    attempt: int = Field(ge=1, le=3)
    provider: str
    model: str
    prompt_version: str
    parameters: dict[str, Any]
    started_at: datetime
    completed_at: datetime
    status: AssetStatus
    cost_estimate: float | None = Field(default=None, ge=0)
    assets: list[GeneratedAsset] = Field(min_length=1)
    manifest_uri: str
    canonical_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    manifest_verified: bool
    storage_verified: bool
    error: str | None = None


class DriftFinding(Contract):
    type: str
    severity: str
    description: str
    expected: str
    observed: str
    affected_region: str
    related_anchor_id: str
    repairable: bool
    evidence: str


class ContinuityEvaluation(Contract):
    evaluation_id: str
    run_id: str
    canon_version: int
    identity_score: float = Field(ge=0, le=1)
    style_score: float = Field(ge=0, le=1)
    palette_score: float = Field(ge=0, le=1)
    symbol_score: float = Field(ge=0, le=1)
    format_score: float = Field(ge=0, le=1)
    prohibited_elements: list[str]
    drift_findings: list[DriftFinding]
    evidence: list[str]
    decision: Decision
    confidence: float = Field(ge=0, le=1)
    evaluator: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def approval_requires_thresholds(self) -> "ContinuityEvaluation":
        if self.decision == Decision.APPROVE:
            passed = (
                self.identity_score >= 0.85
                and self.style_score >= 0.80
                and self.palette_score >= 0.80
                and self.symbol_score >= 0.90
                and self.format_score == 1.0
                and not self.prohibited_elements
            )
            if not passed:
                raise ValueError("Approved evaluations must meet all continuity thresholds")
        return self


class RepairPlan(Contract):
    repair_id: str
    source_run_id: str
    target_asset_id: str
    reasons: list[str]
    preserved_elements: list[str]
    changed_instructions: list[str]
    prompt_patch: str
    provider_change: bool
    parameter_changes: dict[str, Any]
    expected_improvement: str
    retry_number: int = Field(ge=1, le=2)
    requires_approval: bool


class AgentTraceEvent(Contract):
    trace_id: str
    project_id: str
    agent: str
    stage: str
    input_summary: str
    output_summary: str
    tool: str
    run_id: str | None = None
    duration_ms: int = Field(ge=0)
    cost: float | None = Field(default=None, ge=0)
    result: str
    error: str | None = None
    fallback_used: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CampaignPackage(Contract):
    package_id: str
    project_id: str
    approved_asset_ids: list[str] = Field(min_length=1)
    rejected_asset_ids: list[str]
    canon_version: int
    manifest_index: list[str]
    continuity_report: str
    provenance_report: str
    zip_uri: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class HealthResponse(Contract):
    status: str
    mode: str
    provider_configured: bool
    b2_configured: bool
    live_claim: bool = False


class PublicUrl(Contract):
    url: HttpUrl
