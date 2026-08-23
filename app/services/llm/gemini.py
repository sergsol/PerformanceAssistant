"""Gemini client via the public REST API (httpx), so we avoid an extra SDK
dependency and keep the wrapper thin. Uses the free-tier Flash model by default.

Docs: https://ai.google.dev/api/generate-content
"""
from __future__ import annotations

import httpx

_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash") -> None:
        self._api_key = api_key
        self._model = model

    def complete_json(self, system: str, user: str, temperature: float = 0.2) -> str:
        url = f"{_BASE}/{self._model}:generateContent"
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {
                "temperature": temperature,
                # Ask Gemini to emit strict JSON.
                "responseMimeType": "application/json",
            },
        }
        resp = httpx.post(
            url,
            params={"key": self._api_key},
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        # candidates[0].content.parts[0].text — extract defensively.
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as exc:  # pragma: no cover - defensive
            raise RuntimeError(f"Unexpected Gemini response shape: {data}") from exc
