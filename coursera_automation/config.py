"""Configuration settings for Coursera Playwright automation."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings and runtime credentials."""

    login_url: str = os.getenv(
        "COURSERA_LOGIN_URL", "https://www.coursera.org"
    )
    course_url: str = os.getenv(
        "COURSERA_COURSE_URL",
        "https://www.coursera.org/specializations/generative-ai-for-software-developers",
    )
    email: str = os.getenv("COURSERA_EMAIL", "24bai70310@cuchd.in")
    password: str = os.getenv("COURSERA_PASSWORD", "Lakshya.24AI")
    headless: bool = os.getenv("COURSERA_HEADLESS", "false").lower() == "true"
    timeout_ms: int = int(os.getenv("COURSERA_TIMEOUT_MS", "30000"))
    max_items: int = int(os.getenv("COURSERA_MAX_ITEMS", "25"))
    nvidia_api_key: str = os.getenv(
        "NVIDIA_API_KEY",
        "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",
    )
    nvidia_base_url: str = os.getenv(
        "NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"
    )
    nvidia_model: str = os.getenv("NVIDIA_MODEL", "z-ai/glm-5.3")


config = Settings()
