"""Life summary LLM / rules predictive reading."""

from __future__ import annotations

from datetime import date, time

from kundli.chart import BirthInput, build_chart
from kundli.dasha import compute_vimshottari
from kundli.geocode import GeoPlace
from kundli.life_summary import build_life_summary

PUNE = GeoPlace(
    query="Pune",
    display_name="Pune, Maharashtra, India",
    latitude=18.5204,
    longitude=73.8567,
    timezone="Asia/Kolkata",
)


def test_life_summary_rules_when_no_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("TOKENHARBOR_API_KEY", raising=False)

    chart = build_chart(
        BirthInput(
            name="Mira",
            birth_date=date(1991, 3, 14),
            birth_time=time(9, 42),
            place_query="Pune",
            time_unknown=False,
        ),
        place=PUNE,
    )
    timeline = compute_vimshottari(chart)
    out = build_life_summary(chart, timeline)
    assert len(out) == 1
    item = out[0]
    assert item["version"] == "life-llm-v4"
    assert item["sections"] and len(item["sections"]) >= 5
    assert item["simple_summary"]
    assert item["simple_summary_source"] in ("llm", "rules")
    assert item["simple_summary_source"] == "rules"
    ids = [s["id"] for s in item["sections"]]
    assert "personality" in ids and "future" in ids and "now" in ids
    for s in item["sections"]:
        assert len(s["body"]) > 40
    # Rules path should stay clear (no raw dasha labels)
    joined = " ".join(s["body"] for s in item["sections"])
    assert "Mahadasha" not in joined
    assert "Antardasha" not in joined
