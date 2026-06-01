from news_intel.cli import build_parser


def test_parser_accepts_pipeline_commands():
    parser = build_parser()
    args = parser.parse_args(["run", "--date", "2026-06-01", "--skip-delivery"])
    assert args.command == "run"
    assert args.date == "2026-06-01"
    assert args.skip_delivery is True


def test_parser_accepts_individual_stage():
    parser = build_parser()
    args = parser.parse_args(["stage", "brief", "--date", "2026-06-01"])
    assert args.command == "stage"
    assert args.stage_name == "brief"
    assert args.date == "2026-06-01"


def test_run_order_is_stable():
    from news_intel.cli import PIPELINE_ORDER
    assert PIPELINE_ORDER == [
        "fetch",
        "ingest",
        "extract",
        "cluster",
        "investigate",
        "knowledge",
        "brief",
        "deliver",
        "site",
    ]


def test_extract_stage_fails_closed_for_empty_candidates():
    from news_intel.cli import extract_stage_exit_code

    assert extract_stage_exit_code(article_count=3, candidate_count=0) == 1
    assert extract_stage_exit_code(article_count=3, candidate_count=1) == 0
    assert extract_stage_exit_code(article_count=0, candidate_count=0) == 0


def test_stage_brief_writes_only_daily_brief(tmp_path, monkeypatch):
    import news_intel.cli as cli

    monkeypatch.setattr(cli, "ROOT", tmp_path)

    assert cli.stage_brief("2026-06-01") == 0
    assert (tmp_path / "brief" / "daily" / "2026-06-01.md").exists()
    assert not (tmp_path / "report" / "2026-06-01.md").exists()
