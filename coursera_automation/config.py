"""Configuration settings for Coursera Playwright automation."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings and runtime credentials."""

    login_url: str = os.getenv(
        "COURSERA_LOGIN_URL", "https://www.coursera.org/#authMode=login"
    )
    course_url: str = os.getenv(
        "COURSERA_COURSE_URL",
        "https://www.coursera.org/specializations/generative-ai-for-software-developers",
    )
    email: str = os.getenv("COURSERA_EMAIL", "24bai70310@cuchd.in")
    password: str = os.getenv("COURSERA_PASSWORD", "Lakshya.24AI")
    headless: bool = os.getenv("COURSERA_HEADLESS", "false").lower() == "true"
    timeout_ms: int = int(os.getenv("COURSERA_TIMEOUT_MS", "30000"))


config = Settings()
