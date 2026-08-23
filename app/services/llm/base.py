"""Provider-agnostic LLM interface.

Everything downstream depends on this Protocol, not on a specific vendor SDK.
Swapping Gemini <-> Groq <-> a test stub is a one-line factory change.
"""
from __future__ import annotations

from typing import Protocol


class LLMClient(Protocol):
    def complete_json(self, system: str, user: str, temperature: float = 0.2) -> str:
        """Return the model's response as a JSON string.

        Implementations must instruct the model to return ONLY JSON (no prose,
        no markdown fences). The caller parses/validates against AssessResult.
        """
        ...
