"""
LLM Service — handles all communication with the Groq API.
Swapping to another provider (OpenAI, Gemini, Ollama) only requires
changing this single file.
"""

import json
import re
import traceback
import httpx
from fastapi import HTTPException
from app.config import settings


def _clean_json(text: str) -> str:
    """Extract JSON from markdown code blocks if present."""
    match = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', text)
    if match:
        return match.group(1).strip()
    text = text.strip()
    if text.startswith('[') or text.startswith('{'):
        return text
    return text


async def complete(prompt: str, *, parse_json: bool = False):
    """
    Send a prompt to the LLM and return the response text.
    If parse_json=True, attempt to extract and parse JSON from the response.
    """
    payload = {
        "model": settings.MODEL,
        "messages": [
            {"role": "system", "content": "Detect the language of the user's input and respond in that same language."},
            {"role": "user", "content": prompt},
        ],
        "temperature": settings.TEMPERATURE,
        "max_tokens": settings.MAX_TOKENS,
    }

    text = ""
    try:
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.post(
                settings.GROQ_BASE_URL,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

        if response.status_code != 200:
            detail = response.text[:500]
            print(f"❌ LLM HTTP {response.status_code}: {detail}")
            raise HTTPException(status_code=502, detail=f"LLM error ({response.status_code}): {detail}")

        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()

        if parse_json:
            return json.loads(_clean_json(text))
        return text

    except json.JSONDecodeError as exc:
        print(f"❌ JSON parse error: {exc}\nRaw: {text[:500]}")
        raise HTTPException(status_code=502, detail="LLM returned invalid JSON")
    except HTTPException:
        raise
    except Exception as exc:
        print(f"❌ LLM error: {traceback.format_exc()}")
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}")
