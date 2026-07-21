# B2 and Genblaze Usage

## Verified locally

- Genblaze Core 0.3.6 `Pipeline` execution with `MockProvider`
- `fallback_models` recorded on the pipeline step
- canonical manifest creation and `Manifest.verify()` success
- asset SHA-256 included in the manifest
- two-iteration Genblaze `AgentLoop`
- second run contains a parent run identifier
- deterministic Replay with preserved run/evaluation/repair records

## Implemented but not externally verified

- `S3StorageBackend.for_backblaze` creation behind a credential gate
- B2 S3 Signature V4 client
- PUT with SHA-256 metadata
- HEAD size/metadata validation
- GET and downloaded SHA-256 comparison
- hierarchical keys for canon, runs, rejected, approved, and packages

## Evidence boundary

No external generation-provider credential or B2 key was supplied. Therefore there is no live
provider output, ObjectStorageSink transfer, B2 object, HEAD response, or B2 download result. The UI
and submission intentionally mark those items unverified.

