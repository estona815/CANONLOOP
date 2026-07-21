from io import BytesIO
from typing import Any

import pytest
from canonloop.b2_archive import B2Archive, build_genblaze_b2_backend
from canonloop.config import Settings


class FakeS3Client:
    def __init__(self) -> None:
        self.payload = b""
        self.metadata: dict[str, str] = {}

    def put_object(self, **kwargs: Any) -> dict[str, Any]:
        self.payload = kwargs["Body"]
        self.metadata = kwargs["Metadata"]
        return {"ETag": "fixture"}

    def head_object(self, **kwargs: Any) -> dict[str, Any]:
        return {"ContentLength": len(self.payload), "Metadata": self.metadata}

    def get_object(self, **kwargs: Any) -> dict[str, Any]:
        return {"Body": BytesIO(self.payload)}


def test_b2_round_trip_contract_with_fake_client() -> None:
    report = B2Archive(FakeS3Client(), "canonloop-fixture").put_head_get_verify(
        "projects/test/manifest.json", b"fixture", "application/json"
    )
    assert report.head_verified and report.download_verified


def test_genblaze_b2_backend_fails_closed_without_keys() -> None:
    with pytest.raises(RuntimeError, match="not configured"):
        build_genblaze_b2_backend(Settings(_env_file=None))
