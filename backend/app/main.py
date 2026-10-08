"""
Application factory — creates and configures the FastAPI app.
Registers middleware, routes, and static file serving.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import health, quiz, explain, flashcards, chat


def create_app() -> FastAPI:
    app = FastAPI(title="Study Helper API")

    # ── Middleware ───────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routes ──────────────────────────────────────────
    app.include_router(health.router)
    app.include_router(quiz.router)
    app.include_router(explain.router)
    app.include_router(flashcards.router)
    app.include_router(chat.router)

    # ── Static frontend ────────────────────────────────
    app.mount("/", StaticFiles(directory=settings.FRONTEND_DIR, html=True), name="frontend")

    return app


app = create_app()
