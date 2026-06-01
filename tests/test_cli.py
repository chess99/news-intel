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
