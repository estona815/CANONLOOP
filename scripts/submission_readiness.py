from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "submission" / "submission-manifest.json"
DEADLINE = datetime(2026, 8, 3, 21, 0, tzinfo=UTC)


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def _public_url(value: object) -> bool:
    return isinstance(value, str) and bool(re.match(r"^https://[^\s]+$", value))


def evaluate() -> list[Check]:
    manifest = json.loads(MANIFEST_PATH.read_text())
    approved = [
        ROOT / "apps/web/public/media/square-cover.png",
        ROOT / "apps/web/public/media/vertical-story-repaired.png",
        ROOT / "apps/web/public/media/landscape-banner.png",
        ROOT / "apps/web/public/media/poster.png",
    ]
    required_docs = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "AI_DISCLOSURE.md",
        ROOT / "ASSET_MANIFEST.json",
        ROOT / "submission/devpost-description.md",
        ROOT / "submission/providers-and-models.md",
        ROOT / "submission/b2-and-genblaze-usage.md",
        ROOT / "submission/testing-instructions.md",
    ]
    return [
        Check("deadline", datetime.now(UTC) < DEADLINE, "Official deadline Aug 3, 2026 5 PM ET"),
        Check("working app URL", _public_url(manifest.get("appUrl")), str(manifest.get("appUrl"))),
        Check("repository URL", _public_url(manifest.get("repositoryUrl")), str(manifest.get("repositoryUrl"))),
        Check("public video URL", _public_url(manifest.get("videoUrl")), str(manifest.get("videoUrl"))),
        Check("four approved assets", all(path.is_file() for path in approved), f"{sum(path.is_file() for path in approved)}/4 present"),
        Check("rejected→repair fixture", (ROOT / "apps/web/public/media/vertical-story-failed.png").is_file(), "run-007 → run-007r"),
        Check("required documents", all(path.is_file() for path in required_docs), f"{sum(path.is_file() for path in required_docs)}/{len(required_docs)} present"),
        Check("real Genblaze Pipeline", manifest.get("genblazePipelineVerified") is True, "MockProvider integration evidence"),
        Check("real Genblaze AgentLoop", manifest.get("genblazeAgentLoopVerified") is True, "two iterations with parent linkage"),
        Check("live generation provider", manifest.get("liveProviderVerified") is True, "must be a real external provider run"),
        Check("Backblaze B2 round trip", manifest.get("b2Verified") is True, "requires real PUT/HEAD/GET/hash evidence"),
        Check("manifest hashes", bool(manifest.get("manifestHashes")), "canonical manifest evidence list"),
        Check("screenshots", len(manifest.get("screenshots", [])) >= 9, f"{len(manifest.get('screenshots', []))}/9 listed"),
    ]


def main() -> int:
    checks = evaluate()
    for check in checks:
        marker = "PASS" if check.passed else "FAIL"
        print(f"[{marker}] {check.name}: {check.detail}")
    ready = all(check.passed for check in checks)
    print("SUBMISSION_READY" if ready else "SUBMISSION_NOT_READY")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())

