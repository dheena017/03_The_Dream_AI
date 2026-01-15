"""
LLM Client
Provides a minimal provider-agnostic interface to call an LLM.
Currently supports OpenAI via HTTP; falls back gracefully when not configured.
"""

import os
import json
import requests
from typing import Optional


class LLMClient:
    """Lightweight LLM client with simple safety checks."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def is_configured(self) -> bool:
        """Return True when the LLM is ready to be used."""
        if self.provider == "openai" and self.api_key:
            return True
        return False

    def generate_code(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 800) -> str:
        """Call the LLM and return generated code (plain text)."""
        if not self.is_configured():
            return "# LLM not configured. Set OPENAI_API_KEY to enable code generation."

        if self.provider == "openai":
            return self._call_openai(prompt, system_prompt, max_tokens)

        return "# Unsupported LLM provider configured."

    def _call_openai(self, prompt: str, system_prompt: Optional[str], max_tokens: int) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": max_tokens,
        }

        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
            resp.raise_for_status()
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as exc:  # pragma: no cover - network dependent
            return f"# LLM call failed: {exc}"
