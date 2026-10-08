"""
Application configuration.
All environment variables and settings are managed here.
"""

import os


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    # Tried in order; on an error the next model is used.
    MODELS: list[str] = [
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b",
        "meta-llama/llama-4-scout-17b-16e-instruct",
    ]
    MODEL: str = MODELS[0]
    REQUEST_TIMEOUT: float = 60.0
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7

    CORS_ORIGINS: list[str] = ["*"]
    FRONTEND_DIR: str = "../frontend"


settings = Settings()
