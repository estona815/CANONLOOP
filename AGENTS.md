# CANONLOOP repository instructions

- Preserve user work and keep changes reviewable.
- Never read, print, log, or commit credentials. Only `.env.example` may be committed.
- Keep Backblaze B2 and generation-provider secrets server-side.
- Use synthetic or explicitly authorized media only.
- Do not upload, deploy, publish, push, or submit without explicit user approval.
- Never label mock or replay evidence as a live Genblaze/B2 run.
- Write generated audio only to `output/audio/` and preserve original media.
- Keep Python code in `services/api`, web code in `apps/web`, and contracts in `packages/contracts`.
- Run relevant lint, typecheck, unit, integration, build, and readiness checks before handoff.
- Do not skip or delete failing tests to make a check pass.

