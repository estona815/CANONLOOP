from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .agents import AGENT_SPECS
from .config import settings
from .fixtures import replay_bundle
from .genblaze_integration import run_no_key_contract
from .models import HealthResponse
from .packager import build_campaign_package

app = FastAPI(title="CANONLOOP API", version="0.1.0", docs_url="/api/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Content-Type", "X-Canonloop-Live-Confirm"],
)


@app.get("/health", response_model=HealthResponse, response_model_by_alias=True)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        mode=settings.canonloop_mode.value,
        provider_configured=settings.provider_configured,
        b2_configured=settings.b2_configured,
        live_claim=False,
    )


@app.get("/api/replay")
def get_replay() -> dict[str, object]:
    return replay_bundle()


@app.get("/api/agents")
def get_agents() -> list[dict[str, object]]:
    return [
        {
            "name": spec.name,
            "inputContract": spec.input_contract,
            "outputContract": spec.output_contract,
            "allowedTools": spec.allowed_tools,
            "failureConditions": spec.failure_conditions,
            "retryPolicy": spec.retry_policy,
            "approvalBoundary": spec.approval_boundary,
        }
        for spec in AGENT_SPECS
    ]


@app.get("/api/genblaze/no-key-evidence")
def get_genblaze_evidence() -> dict[str, object]:
    return run_no_key_contract().__dict__


@app.get("/api/package")
def download_package() -> Response:
    return Response(
        build_campaign_package(),
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="canonloop-six-line-halo.zip"',
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )
