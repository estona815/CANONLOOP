# Architecture

Next.js renders the public Replay and creates a portable package. FastAPI exposes the typed fixture,
agent specs, package endpoint, and Genblaze evidence. Pydantic and Zod guard the Python/TypeScript
boundary. The optional storage adapter uses B2's S3-compatible endpoint with Signature V4.

