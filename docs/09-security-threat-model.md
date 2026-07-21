# Security Threat Model

Protected assets include provider keys, B2 keys, generated media, manifests, hashes, and package
contents. Controls cover server-only secrets, CORS allowlists, MIME and image decoding, upload size,
prompt length, object-key traversal, ZIP traversal, timeouts, retry and concurrency caps, cost
confirmation, error redaction, and accurate Replay/Live labels. Metadata is data, never instruction.

