from pathlib import Path

import pytest

from news_intel.delivery import brief_path, delivery_payload, require_feishu_config
from scripts import send_report


def test_delivery_payload_contains_title_and_body():
    payload = delivery_payload("2026-06-01", "# Personal Tech Radar · 2026-06-01\n\nBody")
    assert payload["title"] == "Personal Tech Radar · 2026-06-01"
    assert payload["body"].startswith("# Personal Tech Radar")


def test_brief_path_is_only_daily_delivery_artifact():
    assert brief_path(Path("/repo"), "2026-06-01") == Path("/repo/brief/daily/2026-06-01.md")


def test_require_feishu_config_lists_missing_env(monkeypatch):
    for name in ["FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_CHAT_ID"]:
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(RuntimeError, match="FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_CHAT_ID"):
        require_feishu_config()


def test_require_feishu_config_reads_env(monkeypatch):
    monkeypatch.setenv("FEISHU_APP_ID", "app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")
    monkeypatch.setenv("FEISHU_CHAT_ID", "chat")

    assert require_feishu_config() == {
        "FEISHU_APP_ID": "app",
        "FEISHU_APP_SECRET": "secret",
        "FEISHU_CHAT_ID": "chat",
    }


def test_send_report_dry_run_validates_payload(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(send_report, "ROOT", tmp_path)
    monkeypatch.setenv("FEISHU_APP_ID", "app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret")
    monkeypatch.setenv("FEISHU_CHAT_ID", "chat")
    path = tmp_path / "brief" / "daily" / "2026-06-01.md"
    path.parent.mkdir(parents=True)
    path.write_text("# Personal Tech Radar · 2026-06-01\n\nBody", encoding="utf-8")

    assert send_report.main(["--dry-run", "2026-06-01"]) == 0

    assert "dry-run ok" in capsys.readouterr().out
