"""
Application configuration.
All environment variables and settings are managed here.
"""

import os


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    MODEL: str = "openai/gpt-oss-120b"
    REQUEST_TIMEOUT: float = 60.0
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7

    CORS_ORIGINS: list[str] = ["*"]
    FRONTEND_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")


settings = Settings()
