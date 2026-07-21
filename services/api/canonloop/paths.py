from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
WEB_PUBLIC = REPOSITORY_ROOT / "apps" / "web" / "public"
MEDIA_ROOT = WEB_PUBLIC / "media"
FIXTURE_ROOT = REPOSITORY_ROOT / "data" / "fixtures"
OUTPUT_ROOT = REPOSITORY_ROOT / "output"
