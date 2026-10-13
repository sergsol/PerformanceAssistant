"""OpenAI client: request shape, retry on transient errors, no retry on 4xx."""

from __future__ import annotations

import httpx
import pytest

from app.services.llm import openai as openai_mod
from app.services.llm.openai import OpenAIClient


def _resp(status: int, body: dict) -> httpx.Response:
    return httpx.Response(status, json=body, request=httpx.Request("POST", openai_mod._URL))


OK = {"choices": [{"message": {"content": '{"ok": true}'}}]}


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(openai_mod.time, "sleep", lambda _s: None)


def test_returns_message_content_and_sends_json_mode(monkeypatch):
    seen = {}

    def fake_post(url, json, headers, timeout):
        seen.update(url=url, json=json, headers=headers)
        return _resp(200, OK)

    monkeypatch.setattr(httpx, "post", fake_post)
    out = OpenAIClient("sk-test", "gpt-test").complete_json("sys", "usr", 0.1)

    assert out == '{"ok": true}'
    assert seen["json"]["model"] == "gpt-test"
    assert seen["json"]["response_format"] == {"type": "json_object"}
    assert seen["json"]["messages"][0] == {"role": "system", "content": "sys"}
    assert seen["headers"]["Authorization"] == "Bearer sk-test"


def test_retries_transient_5xx_then_succeeds(monkeypatch):
    responses = iter([_resp(503, {"error": "busy"}), _resp(429, {"error": "rate"}), _resp(200, OK)])
    monkeypatch.setattr(httpx, "post", lambda *a, **k: next(responses))
    assert OpenAIClient("k").complete_json("s", "u") == '{"ok": true}'


def test_gives_up_after_max_retries(monkeypatch):
    calls = []

    def fake_post(*a, **k):
        calls.append(1)
        return _resp(503, {"error": "busy"})

    monkeypatch.setattr(httpx, "post", fake_post)
    with pytest.raises(httpx.HTTPStatusError):
        OpenAIClient("k", max_retries=2).complete_json("s", "u")
    assert len(calls) == 3


def test_does_not_retry_client_errors(monkeypatch):
    calls = []

    def fake_post(*a, **k):
        calls.append(1)
        return _resp(401, {"error": "bad key"})

    monkeypatch.setattr(httpx, "post", fake_post)
    with pytest.raises(httpx.HTTPStatusError):
        OpenAIClient("k").complete_json("s", "u")
    assert len(calls) == 1


def test_timeout_is_retried_then_raised(monkeypatch):
    def fake_post(*a, **k):
        raise httpx.ReadTimeout("slow")

    monkeypatch.setattr(httpx, "post", fake_post)
    with pytest.raises(httpx.ReadTimeout):
        OpenAIClient("k", max_retries=1).complete_json("s", "u")


def test_factory_selects_openai(monkeypatch):
    from app.services.llm import get_llm_client
    from app.settings import get_settings

    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-x")
    get_settings.cache_clear()
    try:
        assert isinstance(get_llm_client(), OpenAIClient)
    finally:
        monkeypatch.setenv("LLM_PROVIDER", "stub")
        get_settings.cache_clear()
