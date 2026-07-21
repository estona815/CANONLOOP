import re
from io import BytesIO
from pathlib import PurePosixPath

from PIL import Image

MAX_IMAGE_BYTES = 12 * 1024 * 1024
MAX_PROMPT_CHARS = 6_000
ALLOWED_MIME = {"image/png", "image/jpeg", "image/webp"}
SAFE_SEGMENT = re.compile(r"^[a-zA-Z0-9._-]+$")


def safe_object_key(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("Unsafe object key")
    if any(not SAFE_SEGMENT.fullmatch(part) for part in path.parts):
        raise ValueError("Object key contains unsupported characters")
    return path.as_posix()


def validate_prompt(value: str) -> str:
    cleaned = value.strip()
    if not cleaned or len(cleaned) > MAX_PROMPT_CHARS:
        raise ValueError("Prompt length is outside the accepted range")
    return cleaned


def validate_image(payload: bytes, content_type: str) -> tuple[int, int]:
    if content_type not in ALLOWED_MIME:
        raise ValueError("Unsupported image content type")
    if not payload or len(payload) > MAX_IMAGE_BYTES:
        raise ValueError("Image size is outside the accepted range")
    try:
        with Image.open(BytesIO(payload)) as image:
            image.verify()
        with Image.open(BytesIO(payload)) as image:
            width, height = image.size
    except Exception as exc:
        raise ValueError("Invalid image payload") from exc
    if width < 64 or height < 64 or width * height > 40_000_000:
        raise ValueError("Image dimensions are outside the accepted range")
    return width, height
