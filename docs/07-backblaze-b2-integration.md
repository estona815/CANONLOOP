# Backblaze B2 Integration

The adapter builds a Genblaze `S3StorageBackend.for_backblaze` only when a bucket-scoped key,
bucket, and region exist. The direct verification adapter performs PUT, HEAD, GET, and SHA-256
comparison with `s3v4`. Credentials are server-only. No keys were provided, so no B2 request was
made and all Replay object rows say unverified.

