"""Tests for plain-language match summaries."""

from __future__ import annotations

from datetime import date, time

from kundli.chart import BirthInput, build_chart
from kundli.geocode import GeoPlace
from kundli.matching import match_charts
from kundli.simple_summary import match_simple_summary

PUNE = GeoPlace(
    query="Pune",
    display_name="Pune, Maharashtra, India",
    latitude=18.5204,
    longitude=73.8567,
    timezone="Asia/Kolkata",
)

JAIPUR = GeoPlace(
    query="Jaipur",
    display_name="Jaipur, Rajasthan, India",
    latitude=26.9124,
    longitude=75.7873,
    timezone="Asia/Kolkata",
)


def _demo_match() -> dict:
    a = build_chart(
        BirthInput(
            name="Mira",
            birth_date=date(1991, 3, 14),
            birth_time=time(9, 42),
            place_query="Pune",
            time_unknown=False,
        ),
        place=PUNE,
    )
    b = build_chart(
        BirthInput(
            name="Kabir",
            birth_date=date(1987, 11, 2),
            birth_time=time(16, 18),
            place_query="Jaipur",
            time_unknown=False,
        ),
        place=JAIPUR,
    )
    return match_charts(a, b)


def test_rules_simple_summary_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("TOKENHARBOR_API_KEY", raising=False)
    report = _demo_match()
    headline, sections, source = match_simple_summary(report)
    assert source == "rules"
    assert "Mira" in headline and "Kabir" in headline
    assert sections and len(sections) >= 5
    ids = [s["id"] for s in sections]
    assert "intro" in ids and "ahead" in ids and "manglik" in ids
    joined = " ".join(s["body"] for s in sections)
    assert "36" in joined
    assert len(joined) > 200
    for s in sections:
        assert len(s["body"]) > 40
