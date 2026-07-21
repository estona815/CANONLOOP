# CANONLOOP

**One visual identity. Every format. No drift.**

## Inspiration

Generative media is fast, but identity drifts each time a team asks for another format. Masks,
wardrobe, logos, palette, and visual language change; successful and rejected runs lose their
history. Creative directors need a control system, not another one-shot prompt box.

## What it does

CANONLOOP turns a brief and authorized references into a versioned Visual Canon, plans a campaign,
routes outputs through continuity review, classifies drift, repairs only the failed constraint, and
packages approved assets with readable provenance. The guided SIX-LINE HALO demo includes a square
cover, vertical story, landscape banner, and poster. One synthetic fault fixture has a four-line
emblem instead of the required six; only that symbol rule is repaired.

## How it works

Eight bounded agents implement Intake, Canon Builder, Campaign Planner, Generation, Continuity
Critic, Repair, Provenance Archivist, and Release Packager. Each has typed contracts, allowed tools,
failure conditions, retry policy, traces, and a human-approval boundary. Approval combines score
thresholds with deterministic file, format, hash, manifest, and storage checks.

## How Genblaze is used

The backend pins Genblaze 0.3 packages. Automated integration executes a real Genblaze `Pipeline`
with a fallback model declaration and verifies its canonical manifest. A real two-iteration
`AgentLoop` creates parent-linked runs and stops after the repaired evaluation passes. Because this
submission was completed without provider API credentials, the provider is Genblaze
`MockProvider`; this is SDK-orchestration evidence and not a claim of external model inference.

## How Backblaze B2 is used

B2 is designed as the media system of record for references, canon versions, runs, rejected and
approved assets, evaluations, repairs, manifests, indexes, and release packages. The implemented
adapter uses the B2 S3-compatible API and verifies PUT → HEAD → GET → SHA-256. A Genblaze
`S3StorageBackend.for_backblaze` boundary is included. No B2 credentials were supplied, so no live
B2 operation was executed; the public Replay labels all object rows unverified.

## Production readiness

Replay is static-first and works without judge accounts or keys. Live work is bounded by prompt,
file, retry, concurrency, duration, and cost limits. Package generation excludes rejected assets and
validates archive paths. The app fails closed when credentials or evidence are missing.

## Security and provenance

Secrets are server-only. CORS, MIME, size, image decoding, traversal, prompt, timeout, retry, and
cost controls are documented and tested. All campaign media is fictional, project-specific,
AI-generated synthetic material with SHA-256 and rights metadata.

## Challenges

The hardest design problem was preserving an honest evidence boundary while still making the
failure-to-repair workflow reviewable without external credentials. Replay, Mock, and Live are
separate states in code, UI, tests, and documentation.

## Accomplishments

- Complete no-account guided continuity workflow
- Four approved synthetic formats plus one explicit fault fixture
- Typed eight-agent architecture and bounded repair loop
- Real Genblaze Pipeline, manifest verification, and AgentLoop no-key test
- B2 S3-compatible round-trip adapter with injected-client tests
- Safe package download, rights manifest, strict tests, and production build

## What we learned

Provenance is most useful when it is part of the product decision loop rather than a report added at
the end. Separating semantic critique from deterministic verification also prevents a model from
inventing upload success, hashes, or manifest validity.

## What's next

Run a production image provider through Genblaze, execute and preserve a scoped B2 round trip,
replace deterministic scores with multimodal critic evidence, and add authenticated multi-project
collaboration.

## Built with

Next.js, React, TypeScript, Zod, FastAPI, Pydantic, Genblaze, boto3, Pillow, Vitest, Pytest, and
Backblaze B2's S3-compatible API boundary.

## Testing instructions

Open the hosted URL and choose **Watch the Guided Demo**. Use the left step rail or **Run Guided
Demo** to inspect Brief → Visual Canon → Campaign Plan → Generation Runs → Continuity Review →
Repair Comparison → Approved Campaign → Provenance → B2 Storage. Download the campaign package.

## Limitations

No external generation-provider call and no authenticated B2 operation were executed. Continuity
scores are deterministic fixture evidence. These limitations are visible throughout the product.

