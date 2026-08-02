"""Smoke tests for Ashtakoota matching."""

from __future__ import annotations

from datetime import date, time

from kundli.chart import BirthInput, build_chart
from kundli.geocode import GeoPlace
from kundli.matching import match_charts

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


def test_ashtakoota_mira_kabir():
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
    result = match_charts(a, b)
    assert result["version"] == "ashtakoota-v3"
    assert result["max"] == 36
    assert 0 <= result["total"] <= 36
    assert len(result["kootas"]) == 8
    assert sum(k["max"] for k in result["kootas"]) == 36
    assert result["person_a"]["name"] == "Mira"
    assert result["person_b"]["name"] == "Kabir"
    assert "moon_nakshatra" in result["person_a"]
    assert result["summary"]
    assert result["action_plan"]
    assert result["kootas"][0]["explanation"]
    assert result["kootas"][0]["title"]
    assert result["manglik_title"]
    weak = [k for k in result["kootas"] if k["level"] == "weak"]
    for k in weak:
        assert k.get("problem")
        assert k.get("solutions")
