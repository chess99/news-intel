import sys

import pytest

from news_intel.llm import CommandJSONClient, build_llm_client, parse_json_object


def test_parse_json_object_extracts_object_from_text():
    assert parse_json_object("prefix {\"ok\": true} suffix") == {"ok": True}


def test_parse_json_object_rejects_missing_json():
    with pytest.raises(ValueError, match="did not return JSON object"):
        parse_json_object("no json here")


def test_command_json_client_passes_prompt_as_argv():
    client = CommandJSONClient(
        command=[
            sys.executable,
            "-c",
            "import json, sys; print(json.dumps({'prompt': sys.argv[1]}))",
        ],
        input_mode="argv",
        timeout=5,
    )

    assert client.complete_json("hello") == {"prompt": "hello"}


def test_command_json_client_passes_prompt_as_stdin():
    client = CommandJSONClient(
        command=[
            sys.executable,
            "-c",
            "import json, sys; print(json.dumps({'prompt': sys.stdin.read()}))",
        ],
        input_mode="stdin",
        timeout=5,
    )

    assert client.complete_json("hello") == {"prompt": "hello"}


def test_command_json_client_reports_non_zero_exit():
    client = CommandJSONClient(
        command=[
            sys.executable,
            "-c",
            "import sys; print('bad command', file=sys.stderr); raise SystemExit(2)",
        ],
        timeout=5,
    )

    with pytest.raises(RuntimeError, match="bad command"):
        client.complete_json("hello")


def test_build_llm_client_selects_command_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "command")
    monkeypatch.setenv("LLM_COMMAND", f"{sys.executable} -c \"print('{{\\\"ok\\\": true}}')\"")

    client = build_llm_client()

    assert isinstance(client, CommandJSONClient)
