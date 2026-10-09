from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    environment: str = "development"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000

    gemini_api_key: str = ""
    gemini_flash_model: str = "gemini-3.8-flash"
    gemini_pro_model: str = "gemini-3.1-pro-preview"

    hf_api_key: str = ""
    image_backend: str = "hf"  # hf | local_diffusers | demo
    hf_image_model: str = "stabilityai/stable-diffusion-xl-base-1.0"
    local_image_model: str = "runwayml/stable-diffusion-v1-5"
    image_width: int = 768
    image_height: int = 512
    image_steps: int = 20

    demo_mode: bool = False
    max_prompt_length: int = 2000

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"
