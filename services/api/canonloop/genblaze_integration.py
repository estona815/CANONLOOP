from dataclasses import dataclass
from pathlib import Path

from genblaze_core import (
    AgentContext,
    AgentLoop,
    Asset,
    EvaluationResult,
    Modality,
    Pipeline,
    PipelineResult,
)
from genblaze_core.testing import MockProvider

from .paths import MEDIA_ROOT


@dataclass(frozen=True)
class GenblazeEvidence:
    core_version: str
    pipeline_completed: bool
    pipeline_manifest_verified: bool
    pipeline_canonical_hash: str
    agent_loop_passed: bool
    agent_loop_iterations: int
    parent_linked: bool
    provider: str
    model: str
    disclosure: str


def _asset(path: Path) -> Asset:
    import hashlib

    return Asset(
        url=path.resolve().as_uri(),
        media_type="image/png",
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        size_bytes=path.stat().st_size,
    )


class _RepairEvaluator:
    def evaluate(self, result: PipelineResult) -> EvaluationResult:
        run = result.run
        repaired = run.parent_run_id is not None
        return EvaluationResult(
            passed=repaired,
            score=0.94 if repaired else 0.64,
            feedback="Emblem repaired to six lines"
            if repaired
            else "Repair emblem from four to six lines",
            metadata={"constraint": "symbol", "deterministicFixture": True},
        )


def run_no_key_contract() -> GenblazeEvidence:
    from genblaze_core import __version__ as core_version

    cover = _asset(MEDIA_ROOT / "square-cover.png")
    provider = MockProvider(assets=[cover], cost_usd=0.0)
    pipeline = (
        Pipeline("canonloop-no-key-contract", project_id="six-line-halo")
        .step(
            provider,
            model="canonloop-fixture-v1",
            fallback_models=["canonloop-fixture-v2"],
            prompt="Synthetic SIX-LINE HALO fixture; no external provider call.",
            modality=Modality.IMAGE,
        )
        .run(raise_on_failure=True, timeout=10)
    )

    story = _asset(MEDIA_ROOT / "vertical-story-repaired.png")

    def pipeline_factory(context: AgentContext) -> Pipeline:
        candidate = Pipeline("canonloop-repair-loop", project_id="six-line-halo")
        if context.prior_results:
            candidate = candidate.from_result(context.prior_results[-1])
        prompt = (
            "Render exactly six emblem wing lines"
            if context.iteration
            else "Synthetic four-line fault"
        )
        return candidate.step(
            MockProvider(assets=[story], cost_usd=0.0),
            model="canonloop-fixture-v1",
            prompt=prompt,
            modality=Modality.IMAGE,
        )

    loop_result = AgentLoop(pipeline_factory, _RepairEvaluator(), max_iterations=2).run(
        raise_on_failure=True,
        timeout=10,
    )
    return GenblazeEvidence(
        core_version=core_version,
        pipeline_completed=pipeline.run.status == "completed",
        pipeline_manifest_verified=pipeline.manifest.verify(),
        pipeline_canonical_hash=pipeline.manifest.canonical_hash,
        agent_loop_passed=loop_result.passed,
        agent_loop_iterations=len(loop_result.iterations),
        parent_linked=loop_result.final.run.parent_run_id is not None,
        provider=pipeline.run.steps[0].provider,
        model=pipeline.run.steps[0].model,
        disclosure=(
            "Real Genblaze Pipeline and AgentLoop with MockProvider; "
            "no live generation or B2 claim."
        ),
    )
