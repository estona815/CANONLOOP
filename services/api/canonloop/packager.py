import json
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from .fixtures import replay_bundle
from .paths import MEDIA_ROOT
from .security import safe_object_key

APPROVED_FILES = (
    "square-cover.png",
    "vertical-story-repaired.png",
    "landscape-banner.png",
    "poster.png",
)


def build_campaign_package() -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        for filename in APPROVED_FILES:
            archive.writestr(
                safe_object_key(f"approved-assets/{filename}"), (MEDIA_ROOT / filename).read_bytes()
            )
        bundle = replay_bundle()
        archive.writestr("campaign-manifest.json", json.dumps(bundle, indent=2, ensure_ascii=False))
        archive.writestr(
            "README.txt",
            "CANONLOOP SIX-LINE HALO Replay package\n"
            "Synthetic fixture evidence. No live generation-provider or B2 verification claim.\n",
        )
    return buffer.getvalue()


def archive_names(payload: bytes) -> list[str]:
    with ZipFile(BytesIO(payload)) as archive:
        names = archive.namelist()
    for name in names:
        safe_object_key(name)
    return names
