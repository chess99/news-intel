from __future__ import annotations

import json
import os
import urllib.request


class OpenAICompatibleClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_host: str | None = None,
        model: str | None = None,
    ):
        self.api_key = api_key or os.environ.get("LLM_API_KEY") or os.environ.get("MINIMAX_API_KEY", "")
        self.api_host = (api_host or os.environ.get("LLM_API_HOST", "https://api.minimaxi.com")).rstrip("/")
        self.model = model or os.environ.get("LLM_MODEL", "MiniMax-M2.7")

    def complete_json(self, prompt: str) -> dict:
        payload = json.dumps(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 1200,
            }
        ).encode()
        req = urllib.request.Request(
            f"{self.api_host}/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read())
        text = data["choices"][0]["message"]["content"]
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end < start:
            raise ValueError(f"LLM did not return JSON object: {text[:200]}")
        return json.loads(text[start : end + 1])
