from news_intel.delivery import delivery_payload


def test_delivery_payload_contains_title_and_body():
    payload = delivery_payload("2026-06-01", "# Personal Tech Radar · 2026-06-01\n\nBody")
    assert payload["title"] == "Personal Tech Radar · 2026-06-01"
    assert payload["body"].startswith("# Personal Tech Radar")
