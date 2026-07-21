# Genblaze Integration

Pinned packages: `genblaze-core 0.3.6`, `genblaze-cli 0.3.4`, `genblaze-s3 0.3.5`, and
`genblaze-openai 0.3.2`. `run_no_key_contract()` executes an authentic `Pipeline`, sets a fallback
model, verifies the canonical manifest, then executes a two-iteration `AgentLoop` whose second run
has a `parent_run_id`. The provider is Genblaze `MockProvider`; no external inference is claimed.

