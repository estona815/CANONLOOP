# Providers and Models

| Purpose | Provider | Model | Genblaze adapter | Execution |
| --- | --- | --- | --- | --- |
| Replay pipeline contract | Genblaze MockProvider | `canonloop-fixture-v1` | `genblaze_core.testing.MockProvider` | Verified locally |
| Fallback declaration | Genblaze MockProvider | `canonloop-fixture-v2` | `fallback_models` | Contract verified |
| Demo campaign images | OpenAI built-in image generation | Product-integrated model | Not a Genblaze run | Generated during development |
| Optional live image | OpenAI API | `GENBLAZE_IMAGE_MODEL` | `genblaze_openai.DalleProvider` | Not configured/executed |
| Storage | Backblaze B2 | S3-compatible API | `genblaze_s3.S3StorageBackend` | Adapter ready; not verified |

No provider API key is required or used by the public Replay.

