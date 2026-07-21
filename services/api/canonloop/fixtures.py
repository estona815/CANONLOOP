import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from PIL import Image

from .models import (
    AssetBrief,
    AssetStatus,
    CampaignPlan,
    ContinuityEvaluation,
    Decision,
    DriftFinding,
    GeneratedAsset,
    GenerationRun,
    IdentityAnchor,
    ProjectBrief,
    RepairPlan,
    VisualCanon,
)
from .paths import MEDIA_ROOT

FIXTURE_TIME = datetime(2026, 7, 21, 9, 12, tzinfo=UTC)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _generated_asset(
    *, asset_id: str, run_id: str, filename: str, status: AssetStatus, key: str
) -> GeneratedAsset:
    path = MEDIA_ROOT / filename
    with Image.open(path) as image:
        width, height = image.size
    return GeneratedAsset(
        asset_id=asset_id,
        run_id=run_id,
        url=f"/media/{filename}",
        b2_object_key=key,
        mime_type="image/png",
        width=width,
        height=height,
        size_bytes=path.stat().st_size,
        sha256=_digest(path),
        thumbnail_url=f"/media/{filename}",
        provenance_uri=f"replay://manifests/{run_id}.json",
        status=status,
    )


def project_brief() -> ProjectBrief:
    return ProjectBrief(
        project_id="six-line-halo",
        title="CANONLOOP synthetic continuity demonstration",
        campaign_name="SIX-LINE HALO",
        audience="Creative directors and generative media production teams",
        objective="Deliver one coherent fictional launch campaign across four formats.",
        deliverables=["square cover", "vertical story", "landscape banner", "poster"],
        reference_assets=["square-cover.png", "workspace-concept.png"],
        brand_notes="Industrial night editorial imagery with a fully masked fictional performer.",
        prohibited_content=["real person", "third-party logo", "weapon", "exposed face"],
        budget=5.0,
        provider_preference="replay",
        rights_confirmed=True,
        created_at=FIXTURE_TIME,
    )


def visual_canon() -> VisualCanon:
    anchors = [
        ("mask", "identity", "Seamless dark metallic moth mask"),
        ("ear-light", "accessory", "Cyan light below the left ear"),
        ("jacket", "wardrobe", "Black asymmetric jacket"),
        ("emblem", "symbol", "Exactly six amber wing lines, three per side"),
        ("palette", "color", "Deep navy, cyan, and warm amber palette"),
    ]
    return VisualCanon(
        canon_id="canon-six-line-halo-v1",
        project_id="six-line-halo",
        identity_anchors=[
            IdentityAnchor(
                id=anchor_id,
                category=category,
                description=description,
                importance=0.95 if anchor_id == "emblem" else 0.9,
                source_asset_id="reference-001",
                visual_region="subject",
                verification_method="structured replay evidence",
                tolerance=0.05,
            )
            for anchor_id, category, description in anchors
        ],
        mutable_attributes=["crop", "pose", "negative space", "safe-area placement"],
        fixed_attributes=[description for _, _, description in anchors],
        color_palette=["#04101A", "#27D8F4", "#F3A516"],
        wardrobe_rules=["Black asymmetric jacket must remain visually dominant"],
        symbol_rules=["Emblem must contain exactly six wing lines"],
        lighting_rules=["Cyan rim light and warm amber emblem light"],
        style_rules=["Cinematic editorial photography", "Industrial night atmosphere"],
        composition_rules=["Face remains fully concealed"],
        forbidden_changes=["exposed face", "real logo", "weapon", "emblem line-count drift"],
        source_references=["reference-001", "reference-002"],
        confidence=0.94,
        user_approved=True,
        version=1,
    )


def campaign_plan() -> CampaignPlan:
    specs = [
        ("cover", "Square Cover", "1:1", (1536, 1536)),
        ("story", "Vertical Story", "9:16", (912, 1632)),
        ("banner", "Landscape Banner", "16:9", (1536, 864)),
        ("poster", "Poster", "2:3", (1024, 1536)),
    ]
    assets = [
        AssetBrief(
            asset_id=f"asset-{slug}",
            title=title,
            purpose=f"SIX-LINE HALO {title.lower()}",
            aspect_ratio=ratio,
            dimensions=dimensions,
            prompt="Fictional fully masked performer, preserve all approved Visual Canon anchors.",
            negative_prompt="No real person, logo, exposed face, weapon, or distorted emblem.",
            required_anchors=[anchor.id for anchor in visual_canon().identity_anchors],
            optional_elements=["industrial architecture", "light haze"],
            safe_areas=["Keep title area unobstructed"],
            priority=index + 1,
            retry_budget=2 if slug == "story" else 1,
        )
        for index, (slug, title, ratio, dimensions) in enumerate(specs)
    ]
    return CampaignPlan(
        plan_id="plan-six-line-halo-v1",
        project_id="six-line-halo",
        assets=assets,
        generation_order=[asset.asset_id for asset in assets],
        shared_prompt_prefix="SIX-LINE HALO canonical fictional performer.",
        global_negative_constraints=project_brief().prohibited_content,
        total_retry_budget=5,
        estimated_cost=None,
        status="approved",
    )


def generation_runs() -> list[GenerationRun]:
    specs = [
        (
            "run-005",
            None,
            "asset-cover",
            "square-cover.png",
            AssetStatus.APPROVED,
            "approved/square-cover.png",
        ),
        (
            "run-006",
            None,
            "asset-banner",
            "landscape-banner.png",
            AssetStatus.APPROVED,
            "approved/landscape-banner.png",
        ),
        (
            "run-007",
            None,
            "asset-story",
            "vertical-story-failed.png",
            AssetStatus.FAILED,
            "rejected/vertical-story/run-007.png",
        ),
        (
            "run-007r",
            "run-007",
            "asset-story",
            "vertical-story-repaired.png",
            AssetStatus.REPAIRED,
            "approved/vertical-story.png",
        ),
        (
            "run-008",
            None,
            "asset-poster",
            "poster.png",
            AssetStatus.APPROVED,
            "approved/poster.png",
        ),
    ]
    runs: list[GenerationRun] = []
    for run_id, parent_id, asset_id, filename, status, suffix in specs:
        generated = _generated_asset(
            asset_id=f"{asset_id}-{run_id}",
            run_id=run_id,
            filename=filename,
            status=status,
            key=f"projects/six-line-halo/{suffix}",
        )
        canonical_hash = hashlib.sha256(f"{run_id}:{generated.sha256}".encode()).hexdigest()
        runs.append(
            GenerationRun(
                run_id=run_id,
                parent_run_id=parent_id,
                project_id="six-line-halo",
                asset_id=asset_id,
                attempt=2 if parent_id else 1,
                provider="mock",
                model="canonloop-fixture-v1",
                prompt_version="fixture-v1",
                parameters={"mode": "replay", "faultInjection": run_id == "run-007"},
                started_at=FIXTURE_TIME,
                completed_at=FIXTURE_TIME,
                status=status,
                cost_estimate=0.0,
                assets=[generated],
                manifest_uri=f"replay://manifests/{run_id}.json",
                canonical_hash=canonical_hash,
                manifest_verified=True,
                storage_verified=False,
            )
        )
    return runs


def failed_evaluation() -> ContinuityEvaluation:
    finding = DriftFinding(
        type="symbol",
        severity="high",
        description="Emblem has 4 wing lines; canon requires 6.",
        expected="Six wing lines total, three per side",
        observed="Four wing lines total, two per side",
        affected_region="mask and halo emblem",
        related_anchor_id="emblem",
        repairable=True,
        evidence="Synthetic fault-injection fixture intentionally contains the four-line variant.",
    )
    return ContinuityEvaluation(
        evaluation_id="evaluation-run-007",
        run_id="run-007",
        canon_version=1,
        identity_score=0.91,
        style_score=0.88,
        palette_score=0.86,
        symbol_score=0.64,
        format_score=1.0,
        prohibited_elements=[],
        drift_findings=[finding],
        evidence=[finding.evidence],
        decision=Decision.REJECT,
        confidence=0.96,
        evaluator="canonloop-deterministic-fixture-v1",
        created_at=FIXTURE_TIME,
    )


def repair_plan() -> RepairPlan:
    return RepairPlan(
        repair_id="repair-run-007-v1",
        source_run_id="run-007",
        target_asset_id="asset-story",
        reasons=["Symbol score 0.64 is below the 0.90 approval threshold"],
        preserved_elements=["identity", "mask", "wardrobe", "palette", "lighting", "composition"],
        changed_instructions=["Render exactly six symmetric emblem wing lines"],
        prompt_patch="Change only emblem geometry: exactly three wing lines on each side.",
        provider_change=False,
        parameter_changes={},
        expected_improvement="Raise symbol compliance above 0.90 without changing passing anchors.",
        retry_number=1,
        requires_approval=False,
    )


def repaired_evaluation() -> ContinuityEvaluation:
    return ContinuityEvaluation(
        evaluation_id="evaluation-run-007r",
        run_id="run-007r",
        canon_version=1,
        identity_score=0.93,
        style_score=0.90,
        palette_score=0.89,
        symbol_score=0.94,
        format_score=1.0,
        prohibited_elements=[],
        drift_findings=[],
        evidence=[
            "Synthetic repaired fixture preserves the passing anchors and restores six lines."
        ],
        decision=Decision.APPROVE,
        confidence=0.95,
        evaluator="canonloop-deterministic-fixture-v1",
        created_at=FIXTURE_TIME,
    )


def replay_bundle() -> dict[str, Any]:
    return {
        "disclosure": {
            "mode": "replay",
            "liveProviderRun": False,
            "b2Verified": False,
            "claim": "Deterministic local fixture; not a live provider or B2 run.",
        },
        "brief": project_brief().model_dump(mode="json", by_alias=True),
        "canon": visual_canon().model_dump(mode="json", by_alias=True),
        "plan": campaign_plan().model_dump(mode="json", by_alias=True),
        "runs": [run.model_dump(mode="json", by_alias=True) for run in generation_runs()],
        "failedEvaluation": failed_evaluation().model_dump(mode="json", by_alias=True),
        "repairPlan": repair_plan().model_dump(mode="json", by_alias=True),
        "repairedEvaluation": repaired_evaluation().model_dump(mode="json", by_alias=True),
    }
