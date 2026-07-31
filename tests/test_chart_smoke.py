"""Smoke tests for chart + dasha with a known sample birth (offline coords)."""

from __future__ import annotations

from datetime import date, time

import pytest

from kundli.chart import BirthInput, build_chart
from kundli.dasha import DASHA_ORDER, DASHA_YEARS, compute_vimshottari
from kundli.ephemeris import longitude_info, normalize_longitude
from kundli.geocode import GeoPlace
from kundli.interpret import build_interpretation
from kundli.qa import answer_question, detect_topic
from kundli.yogas import detect_yogas

# Mumbai approx — avoid network in unit tests
MUMBAI = GeoPlace(
    query="Mumbai, India",
    display_name="Mumbai, Maharashtra, India",
    latitude=19.0760,
    longitude=72.8777,
    timezone="Asia/Kolkata",
)


@pytest.fixture
def sample_chart():
    birth = BirthInput(
        name="Test Person",
        birth_date=date(1990, 5, 15),
        birth_time=time(14, 30),
        place_query="Mumbai, India",
        time_unknown=False,
    )
    return build_chart(birth, place=MUMBAI)


def test_longitude_info_boundaries():
    info = longitude_info(0.0)
    assert info.rashi_name == "Aries"
    assert info.nakshatra_name == "Ashwini"
    assert info.pada == 1

    info2 = longitude_info(29.999)
    assert info2.rashi_name == "Aries"

    info3 = longitude_info(30.0)
    assert info3.rashi_name == "Taurus"


def test_normalize_longitude():
    assert normalize_longitude(370) == 10
    assert normalize_longitude(-10) == 350


def test_chart_has_nine_planets(sample_chart):
    expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    assert set(sample_chart.planets) == expected
    assert 1 <= sample_chart.lagna.rashi_index <= 12
    assert len(sample_chart.houses) == 12
    # Whole-sign: every planet house 1-12
    for pl in sample_chart.planets.values():
        assert 1 <= pl.house <= 12
    # Ketu opposite Rahu
    rahu = sample_chart.planets["Rahu"].info.longitude
    ketu = sample_chart.planets["Ketu"].info.longitude
    diff = abs((ketu - rahu) % 360 - 180)
    assert diff < 0.01 or abs(diff - 360) < 0.01 or diff < 1.0


def test_rahu_ketu_opposition(sample_chart):
    r = sample_chart.planets["Rahu"].info.longitude
    k = sample_chart.planets["Ketu"].info.longitude
    sep = (k - r) % 360
    assert abs(sep - 180) < 0.5


def test_vimshottari_balance(sample_chart):
    timeline = compute_vimshottari(sample_chart)
    assert timeline.balance_at_birth["lord"] in DASHA_ORDER
    assert 0 < timeline.balance_at_birth["years_remaining"] <= 20
    assert timeline.current_mahadasha is not None
    assert timeline.current_antardasha is not None
    assert len(timeline.antardashas_in_current) == 9
    # Antardashas nest inside mahadasha
    m = timeline.current_mahadasha
    for a in timeline.antardashas_in_current:
        assert a.start >= m.start
        assert a.end <= m.end + __import__("datetime").timedelta(seconds=2)


def test_dasha_years_sum():
    assert sum(DASHA_YEARS.values()) == 120


def test_yogas_and_interpretation(sample_chart):
    yogas = detect_yogas(sample_chart)
    assert len(yogas) >= 5
    timeline = compute_vimshottari(sample_chart)
    interp = build_interpretation(sample_chart, timeline)
    assert "lagna" in interp
    assert len(interp["planets"]) == 9
    assert len(interp["houses"]) == 12


def test_qa_topics(sample_chart):
    assert detect_topic("Tell me about my career") == "career"
    assert detect_topic("Will I get married?") == "marriage"
    assert detect_topic("xyzabc") is None
    timeline = compute_vimshottari(sample_chart)
    text, key = answer_question(sample_chart, timeline, "money and wealth")
    assert key == "money"
    assert "House" in text
