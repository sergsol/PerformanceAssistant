"""LLM provider factory. Chooses the client based on settings.llm_provider."""
from __future__ import annotations

from app.services.llm.base import LLMClient
from app.services.llm.gemini import GeminiClient
from app.services.llm.stub import StubClient
from app.settings import get_settings


def get_llm_client() -> LLMClient:
    s = get_settings()
    if s.llm_provider == "gemini":
        return GeminiClient(api_key=s.gemini_api_key, model=s.gemini_model)
    if s.llm_provider == "stub":
        return StubClient()
    # groq stub-out until implemented in Phase 3+
    if s.llm_provider == "groq":
        raise NotImplementedError("Groq client not yet implemented; use 'gemini' or 'stub'.")
    raise ValueError(f"Unknown llm_provider: {s.llm_provider}")
