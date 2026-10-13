"""LLM client for Ollama/OpenAI-compatible endpoints."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """Environment-driven LLM settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_base_url: Optional[str] = None
    llm_model: str = "Qwen3-14b-32k:latest"
    llm_api_key: Optional[str] = None
    llm_stub: bool = False


def _resolve_base_url(settings: LLMSettings) -> Optional[str]:
    return (
        settings.llm_base_url
        or os.getenv("LLM_BASE_URL")
        or os.getenv("LLM_URL")
        or os.getenv("OLLAMA_API_BASE")
        or os.getenv("OLLAMA_BASE_URL")
        or os.getenv("OPENAI_API_BASE")
        or os.getenv("OPENAI_BASE_URL")
        or "http://localhost:11434/v1"
    )


def _resolve_model(settings: LLMSettings) -> str:
    return (
        os.getenv("LLM_MODEL")
        or os.getenv("OLLAMA_MODEL")
        or os.getenv("OPENAI_MODEL")
        or settings.llm_model
    )


def _resolve_api_key(settings: LLMSettings, base_url: Optional[str]) -> Optional[str]:
    key = (
        settings.llm_api_key
        or os.getenv("LLM_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("OLLAMA_API_KEY")
    )
    if key:
        return key
    if base_url and "localhost" in base_url:
        return "ollama"
    return None


def _use_stub(settings: LLMSettings) -> bool:
    flag = os.getenv("LLM_STUB", "0").lower()
    if flag in {"1", "true", "yes", "on"}:
        return True
    return bool(settings.llm_stub)


class LLMClient:
    """Simple LLM client supporting chat/generate and embeddings."""

    def __init__(self) -> None:
        self.settings = LLMSettings()
        self.base_url = _resolve_base_url(self.settings)
        self.model = _resolve_model(self.settings)
        self.api_key = _resolve_api_key(self.settings, self.base_url)
        self.stub = _use_stub(self.settings)
        self._client: Optional[OpenAI] = None

    def _get_client(self) -> OpenAI:
        if self._client is None:
            kwargs: Dict[str, Any] = {"api_key": self.api_key}
            if self.base_url:
                kwargs["base_url"] = self.base_url
            self._client = OpenAI(**kwargs)
        return self._client

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        if self.stub:
            last_user = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
            return f"[stubbed llm] {last_user[:400]}"

        client = self._get_client()
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            if tool_choice:
                kwargs["tool_choice"] = tool_choice
        if temperature is not None:
            kwargs["temperature"] = temperature
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        resp = client.chat.completions.create(**kwargs)
        # Object response
        if hasattr(resp, "choices") and resp.choices:
            msg = getattr(resp.choices[0], "message", None)
            if msg:
                return getattr(msg, "content", "") or ""
        # Dict fallback
        if isinstance(resp, dict):
            return resp.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
        return ""

    def generate(self, prompt: str) -> str:
        return self.chat(messages=[{"role": "user", "content": prompt}])

    def embeddings(self, inputs: List[str]) -> List[List[float]]:
        if self.stub:
            return [[0.0] * 8 for _ in inputs]
        client = self._get_client()
        resp = client.embeddings.create(model=self.model, input=inputs)
        if hasattr(resp, "data"):
            return [getattr(item, "embedding", []) for item in resp.data]
        if isinstance(resp, dict):
            return [d.get("embedding", []) for d in resp.get("data", [])]
        return []


_singleton: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    global _singleton
    if _singleton is None:
        _singleton = LLMClient()
    return _singleton


def chat(
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> str:
    return get_llm_client().chat(messages, tools=tools, tool_choice=tool_choice, temperature=temperature, max_tokens=max_tokens)


def get_embeddings(inputs: List[str]) -> List[List[float]]:
    return get_llm_client().embeddings(inputs)