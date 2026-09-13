"""Tests for Ask plain-language answers (rules fallback)."""

from __future__ import annotations

from datetime import date, time

from kundli.chart import BirthInput, build_chart
from kundli.dasha import compute_vimshottari
from kundli.geocode import GeoPlace
from kundli.qa import answer_question
from kundli.simple_summary import ask_plain_answer

PUNE = GeoPlace(
    query="Pune",
    display_name="Pune, Maharashtra, India",
    latitude=18.5204,
    longitude=73.8567,
    timezone="Asia/Kolkata",
)


def test_ask_plain_rules_fallback(monkeypatch):
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
    rule, topic = answer_question(chart, timeline, "Tell me about my career")
    assert topic == "career"
    text, source = ask_plain_answer(
        chart=chart,
        timeline=timeline,
        question="Tell me about my career",
        topic=topic,
        rule_answer=rule,
    )
    assert source == "rules"
    assert len(text) > 40
    assert "(reading " not in text
