"""Life summary LLM / rules predictive reading."""

from __future__ import annotations

from datetime import date, time

from kundli.chart import BirthInput, build_chart
from kundli.dasha import compute_vimshottari
from kundli.geocode import GeoPlace
from kundli.life_summary import build_life_summary
from kundli.simple_summary import _manglik_fact_lines

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
    assert item["version"] == "life-llm-v5"
    assert item["sections"] and len(item["sections"]) >= 6
    assert item["simple_summary"]
    assert item["simple_summary_source"] == "rules"
    ids = [s["id"] for s in item["sections"]]
    assert "personality" in ids and "future" in ids and "now" in ids
    assert "manglik" in ids
    for s in item["sections"]:
        assert len(s["body"]) > 40
    joined = " ".join(s["body"] for s in item["sections"])
    assert "Mahadasha" not in joined
    assert "Antardasha" not in joined
    is_m, _, _, _ = _manglik_fact_lines(chart)
    if is_m:
        assert "this chart is Manglik" in joined
    else:
        assert "is not Manglik" in joined or "not Manglik" in joined


def test_two_charts_differ_and_state_manglik(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("TOKENHARBOR_API_KEY", raising=False)

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
    sa = build_life_summary(a, compute_vimshottari(a))[0]
    sb = build_life_summary(b, compute_vimshottari(b))[0]
    career_a = next(s["body"] for s in sa["sections"] if s["id"] == "career")
    career_b = next(s["body"] for s in sb["sections"] if s["id"] == "career")
    assert career_a != career_b
    mang_a = next(s["body"] for s in sa["sections"] if s["id"] == "manglik")
    mang_b = next(s["body"] for s in sb["sections"] if s["id"] == "manglik")
    assert "Manglik" in mang_a and "Manglik" in mang_b
    assert a.lagna.rashi_name in sa["simple_summary"] or a.lagna.rashi_name in next(
        s["body"] for s in sa["sections"] if s["id"] == "intro"
    )
