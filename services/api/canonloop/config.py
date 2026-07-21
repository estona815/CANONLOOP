from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunMode(StrEnum):
    REPLAY = "replay"
    MOCK = "mock"
    LIVE = "live"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    canonloop_mode: RunMode = RunMode.REPLAY
    canonloop_allowed_origins: str = "http://localhost:3000"
    canonloop_api_origin: str = "http://localhost:8000"
    canonloop_max_estimated_cost_usd: float = Field(default=5.0, gt=0, le=100)
    canonloop_max_concurrent_jobs: int = Field(default=2, ge=1, le=4)
    genblaze_provider: str = "openai"
    genblaze_image_model: str = "gpt-image-1"
    genblaze_fallback_model: str = "dall-e-3"
    genblaze_max_retries: int = Field(default=2, ge=0, le=2)
    genblaze_timeout_seconds: int = Field(default=180, ge=10, le=600)
    openai_api_key: str | None = None
    gmi_api_key: str | None = None
    b2_bucket: str | None = None
    b2_region: str | None = None
    b2_key_id: str | None = None
    b2_app_key: str | None = None

    @property
    def allowed_origins(self) -> list[str]:
        return [
            value.strip() for value in self.canonloop_allowed_origins.split(",") if value.strip()
        ]

    @property
    def b2_configured(self) -> bool:
        return all((self.b2_bucket, self.b2_region, self.b2_key_id, self.b2_app_key))

    @property
    def provider_configured(self) -> bool:
        return bool(self.openai_api_key or self.gmi_api_key)


settings = Settings()
