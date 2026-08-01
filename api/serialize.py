"""Serialize kundli dataclasses to JSON-friendly dicts."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from kundli.chart import BirthInput, KundliChart, build_chart
from kundli.dasha import (
    DASHA_ORDER,
    DASHA_YEARS,
    DashaPeriod,
    DashaTimeline,
    _add_years,
    compute_vimshottari,
)
from kundli.interpret import build_interpretation
from kundli.yogas import YogaResult


def _iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def _period(p: DashaPeriod) -> Dict[str, Any]:
    return {
        "lord": p.lord,
        "start": _iso(p.start),
        "end": _iso(p.end),
        "level": p.level,
    }


def pratyantars(antar: DashaPeriod) -> List[Dict[str, Any]]:
    """Pratyantardasha strips within an antardasha."""
    antar_years = (antar.end - antar.start).total_seconds() / (365.2425 * 86400)
    start_idx = DASHA_ORDER.index(antar.lord)
    out: List[Dict[str, Any]] = []
    cursor = antar.start
    for i in range(9):
        sub_lord = DASHA_ORDER[(start_idx + i) % 9]
        sub_years = antar_years * DASHA_YEARS[sub_lord] / 120.0
        end = _add_years(cursor, sub_years)
        if i == 8:
            end = antar.end
        out.append(
            {
                "lord": sub_lord,
                "start": _iso(cursor),
                "end": _iso(end),
                "level": "pratyantar",
            }
        )
        cursor = end
    return out


def serialize_longitude(info) -> Dict[str, Any]:
    return {
        "longitude": round(float(info.longitude), 4),
        "rashi_index": int(info.rashi_index),
        "rashi_name": info.rashi_name,
        "degree_in_rashi": round(float(info.degree_in_rashi), 4),
        "nakshatra_index": int(info.nakshatra_index),
        "nakshatra_name": info.nakshatra_name,
        "pada": int(info.pada),
        "retrograde": bool(info.retrograde),
    }


def serialize_chart(chart: KundliChart) -> Dict[str, Any]:
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    planets = {}
    for name in order:
        pl = chart.planets[name]
        planets[name] = {
            "name": name,
            "house": pl.house,
            "info": serialize_longitude(pl.info),
        }
    houses = [
        {
            "number": h.number,
            "rashi_index": h.rashi_index,
            "rashi_name": h.rashi_name,
            "planets": h.planets,
        }
        for h in chart.houses
    ]
    return {
        "birth": {
            "name": chart.birth.name,
            "birth_date": chart.birth.birth_date.isoformat(),
            "birth_time": None
            if chart.birth.time_unknown
            else (
                chart.birth.birth_time.strftime("%H:%M")
                if chart.birth.birth_time
                else None
            ),
            "place_query": chart.birth.place_query,
            "time_unknown": chart.birth.time_unknown,
        },
        "place": {
            "query": chart.place.query,
            "display_name": chart.place.display_name,
            "latitude": chart.place.latitude,
            "longitude": chart.place.longitude,
            "timezone": chart.place.timezone,
        },
        "local_dt": _iso(chart.local_dt),
        "utc_dt": _iso(chart.utc_dt),
        "lagna": serialize_longitude(chart.lagna),
        "planets": planets,
        "houses": houses,
        "moon_nakshatra": chart.moon_nakshatra,
        "moon_pada": chart.moon_pada,
    }


def serialize_yoga(y: YogaResult) -> Dict[str, Any]:
    return {
        "name": y.name,
        "present": y.present,
        "detail": y.detail,
        "meaning": y.meaning,
        "kind": getattr(y, "kind", "classical"),
    }


def serialize_timeline(tl: DashaTimeline) -> Dict[str, Any]:
    current_antar = tl.current_antardasha
    bal = tl.balance_at_birth
    return {
        "balance_at_birth": {
            "lord": bal["lord"],
            "years_remaining": float(bal["years_remaining"]),
            "full_years": float(bal["full_years"]),
        },
        "mahadashas": [_period(p) for p in tl.mahadashas],
        "current_mahadasha": _period(tl.current_mahadasha) if tl.current_mahadasha else None,
        "current_antardasha": _period(current_antar) if current_antar else None,
        "antardashas_in_current": [_period(p) for p in tl.antardashas_in_current],
        "pratyantars_in_current": pratyantars(current_antar) if current_antar else [],
    }


def serialize_interpretation(interp: dict) -> Dict[str, Any]:
    return {
        "disclaimer": interp["disclaimer"],
        "lagna": interp["lagna"],
        "moon": interp["moon"],
        "planets": interp["planets"],
        "houses": interp["houses"],
        "yogas": [serialize_yoga(y) for y in interp["yogas"]],
        "dasha": interp["dasha"],
        "strengths": interp["strengths"],
        "life_areas": interp.get("life_areas", []),
    }


def build_full_report(birth: BirthInput) -> Dict[str, Any]:
    chart = build_chart(birth)
    timeline = compute_vimshottari(chart)
    interpretation = build_interpretation(chart, timeline)
    return {
        "chart": serialize_chart(chart),
        "timeline": serialize_timeline(timeline),
        "interpretation": serialize_interpretation(interpretation),
    }
