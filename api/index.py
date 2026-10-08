"""Vercel entrypoint — exposes the FastAPI app from backend/.

Vercel rewrites every request to /api/index and passes the original
path in the `__path` query parameter (see vercel.json); restore it here.
"""

import os
import sys
from urllib.parse import parse_qsl, urlencode

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app as _app  # noqa: E402


async def app(scope, receive, send):
    if scope["type"] == "http":
        params = parse_qsl(scope.get("query_string", b"").decode(), keep_blank_values=True)
        path = next((v for k, v in params if k == "__path"), None)
        if path is not None:
            path = "/" + path.lstrip("/")
            rest = urlencode([(k, v) for k, v in params if k != "__path"])
            scope = {**scope, "path": path, "raw_path": path.encode(), "query_string": rest.encode()}
    await _app(scope, receive, send)
