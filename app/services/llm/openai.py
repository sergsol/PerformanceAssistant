"""OpenAI Chat Completions client (plain httpx, no SDK dependency).

Uses JSON mode so the response is a strict JSON object. Retries transient
failures (429 / 5xx / timeouts) a couple of times before giving up.
"""

from __future__ import annotations

import time

import httpx

_URL = "https://api.openai.com/v1/chat/completions"
_RETRY_STATUSES = {429, 500, 502, 503, 504}


class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", max_retries: int = 2) -> None:
        self._api_key = api_key
        self._model = model
        self._max_retries = max_retries

    def complete_json(self, system: str, user: str, temperature: float = 0.2) -> str:
        payload = {
            "model": self._model,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        headers = {"Authorization": f"Bearer {self._api_key}"}

        for attempt in range(self._max_retries + 1):
            last_attempt = attempt == self._max_retries
            try:
                resp = httpx.post(_URL, json=payload, headers=headers, timeout=60)
            except httpx.TimeoutException:
                if last_attempt:
                    raise
                time.sleep(2**attempt)
                continue
            if resp.status_code in _RETRY_STATUSES and not last_attempt:
                time.sleep(2**attempt)
                continue
            resp.raise_for_status()
            data = resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as exc:  # pragma: no cover - defensive
                raise RuntimeError(f"Unexpected OpenAI response shape: {data}") from exc
        raise RuntimeError("unreachable")  # pragma: no cover
