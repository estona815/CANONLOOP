from io import BytesIO

import pytest
from canonloop.security import safe_object_key, validate_image, validate_prompt
from PIL import Image


def test_safe_object_key_accepts_hierarchy() -> None:
    assert (
        safe_object_key("projects/demo/runs/run-1/manifest.json")
        == "projects/demo/runs/run-1/manifest.json"
    )


def test_safe_object_key_rejects_traversal() -> None:
    with pytest.raises(ValueError):
        safe_object_key("../secret.env")


def test_prompt_length_guard() -> None:
    with pytest.raises(ValueError):
        validate_prompt("x" * 6_001)


def test_image_validation() -> None:
    buffer = BytesIO()
    Image.new("RGB", (64, 64), "navy").save(buffer, format="PNG")
    assert validate_image(buffer.getvalue(), "image/png") == (64, 64)
