from __future__ import annotations

import json
import os
import shlex
import subprocess
import urllib.request


def parse_json_object(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"LLM did not return JSON object: {text[:200]}")
    return json.loads(text[start : end + 1])


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
        return parse_json_object(text)


class CommandJSONClient:
    def __init__(
        self,
        *,
        command: str | list[str] | None = None,
        input_mode: str | None = None,
        timeout: int | None = None,
        cwd: str | None = None,
    ):
        command = command or os.environ.get("LLM_COMMAND", "")
        if isinstance(command, str):
            self.command = shlex.split(command)
        else:
            self.command = command
        if not self.command:
            raise RuntimeError("LLM_COMMAND is required when LLM_PROVIDER=command")
        self.input_mode = input_mode or os.environ.get("LLM_COMMAND_INPUT", "argv")
        if self.input_mode not in {"argv", "stdin"}:
            raise RuntimeError("LLM_COMMAND_INPUT must be one of: argv, stdin")
        self.timeout = timeout or int(os.environ.get("LLM_COMMAND_TIMEOUT", "120"))
        self.cwd = cwd

    def complete_json(self, prompt: str) -> dict:
        args = list(self.command)
        stdin = None
        if self.input_mode == "argv":
            args.append(prompt)
        else:
            stdin = prompt

        try:
            result = subprocess.run(
                args,
                input=stdin,
                text=True,
                capture_output=True,
                timeout=self.timeout,
                check=False,
                cwd=self.cwd,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"LLM command timed out after {self.timeout}s: {self.command[0]}") from exc
        except FileNotFoundError as exc:
            raise RuntimeError(f"LLM command not found: {self.command[0]}") from exc

        if result.returncode != 0:
            stderr = result.stderr.strip()[:500]
            stdout = result.stdout.strip()[:500]
            detail = stderr or stdout or f"exit code {result.returncode}"
            raise RuntimeError(f"LLM command failed: {detail}")
        return parse_json_object(result.stdout)


def build_llm_client(*, model: str | None = None):
    provider = os.environ.get("LLM_PROVIDER", "openai").strip().lower()
    if provider in {"openai", "openai-compatible", "api"}:
        return OpenAICompatibleClient(model=model)
    if provider in {"command", "agent", "local-command"}:
        return CommandJSONClient()
    raise RuntimeError(f"unsupported LLM_PROVIDER: {provider}")
