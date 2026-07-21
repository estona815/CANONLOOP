import hashlib
from dataclasses import dataclass
from typing import Any, Protocol, cast

import boto3  # type: ignore[import-untyped]
from botocore.config import Config  # type: ignore[import-untyped]
from genblaze_s3 import S3StorageBackend

from .config import Settings
from .security import safe_object_key


class S3Client(Protocol):
    def put_object(self, **kwargs: Any) -> dict[str, Any]: ...

    def head_object(self, **kwargs: Any) -> dict[str, Any]: ...

    def get_object(self, **kwargs: Any) -> dict[str, Any]: ...


@dataclass(frozen=True)
class RoundTripReport:
    object_key: str
    sha256: str
    size_bytes: int
    content_type: str
    head_verified: bool
    download_verified: bool


def build_genblaze_b2_backend(settings: Settings) -> S3StorageBackend:
    if not settings.b2_configured:
        raise RuntimeError("B2 is not configured")
    assert settings.b2_bucket and settings.b2_key_id and settings.b2_app_key
    return S3StorageBackend.for_backblaze(
        settings.b2_bucket,
        key_id=settings.b2_key_id,
        app_key=settings.b2_app_key,
        region=settings.b2_region,
    )


def build_b2_client(settings: Settings) -> S3Client:
    if not settings.b2_configured:
        raise RuntimeError("B2 is not configured")
    assert settings.b2_region and settings.b2_key_id and settings.b2_app_key
    endpoint = f"https://s3.{settings.b2_region}.backblazeb2.com"
    return cast(
        S3Client,
        boto3.client(
            "s3",
            endpoint_url=endpoint,
            region_name=settings.b2_region,
            aws_access_key_id=settings.b2_key_id,
            aws_secret_access_key=settings.b2_app_key,
            config=Config(
                signature_version="s3v4", retries={"max_attempts": 2, "mode": "standard"}
            ),
        ),
    )


class B2Archive:
    def __init__(self, client: S3Client, bucket: str) -> None:
        self._client = client
        self._bucket = bucket

    def put_head_get_verify(self, key: str, payload: bytes, content_type: str) -> RoundTripReport:
        safe_key = safe_object_key(key)
        digest = hashlib.sha256(payload).hexdigest()
        self._client.put_object(
            Bucket=self._bucket,
            Key=safe_key,
            Body=payload,
            ContentType=content_type,
            Metadata={"sha256": digest, "source": "canonloop"},
        )
        head = self._client.head_object(Bucket=self._bucket, Key=safe_key)
        response = self._client.get_object(Bucket=self._bucket, Key=safe_key)
        downloaded = response["Body"].read()
        downloaded_digest = hashlib.sha256(downloaded).hexdigest()
        metadata = {str(key).lower(): str(value) for key, value in head.get("Metadata", {}).items()}
        return RoundTripReport(
            object_key=safe_key,
            sha256=digest,
            size_bytes=len(payload),
            content_type=content_type,
            head_verified=head.get("ContentLength") == len(payload)
            and metadata.get("sha256") == digest,
            download_verified=downloaded_digest == digest,
        )
