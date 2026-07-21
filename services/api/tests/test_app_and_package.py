from io import BytesIO
from zipfile import ZipFile

from canonloop.app import app
from canonloop.packager import APPROVED_FILES, archive_names, build_campaign_package
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_discloses_no_live_claim() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["liveClaim"] is False


def test_replay_endpoint_discloses_unverified_b2() -> None:
    response = client.get("/api/replay")
    assert response.status_code == 200
    assert response.json()["disclosure"]["b2Verified"] is False


def test_agent_endpoint_lists_all_agents() -> None:
    assert len(client.get("/api/agents").json()) == 8


def test_package_contains_only_approved_media() -> None:
    payload = build_campaign_package()
    names = archive_names(payload)
    assert all(f"approved-assets/{filename}" in names for filename in APPROVED_FILES)
    assert "approved-assets/vertical-story-failed.png" not in names
    with ZipFile(BytesIO(payload)) as archive:
        assert "campaign-manifest.json" in archive.namelist()


def test_package_endpoint_returns_zip() -> None:
    response = client.get("/api/package")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
