"""Vercel entrypoint — exposes the FastAPI app from backend/."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app  # noqa: E402,F401

_inner = app


async def app(scope, receive, send):  # noqa: F811  (temporary debug wrapper)
    if scope["type"] == "http" and b"__debug" in scope.get("query_string", b""):
        import json
        body = json.dumps({
            "path": scope.get("path"), "raw_path": str(scope.get("raw_path")),
            "root_path": scope.get("root_path"), "qs": scope.get("query_string", b"").decode(),
            "cwd": os.getcwd(), "frontend": os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "frontend")),
            "headers": {k.decode(): v.decode() for k, v in scope.get("headers", []) if b"forward" in k or b"vercel" in k or b"path" in k or b"url" in k},
        }).encode()
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": body})
        return
    await _inner(scope, receive, send)
