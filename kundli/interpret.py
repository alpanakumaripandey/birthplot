"""Plain-language interpretations from chart + knowledge base."""

from __future__ import annotations

from typing import List

from kundli.chart import KundliChart
from kundli.dasha import DashaTimeline
from kundli.knowledge_loader import houses, nakshatras, planets, rashis
from kundli.yogas import YogaResult, detect_yogas


def lagna_blurb(chart: KundliChart) -> str:
    r = rashis()[str(chart.lagna.rashi_index)]
    return (
        f"Your Lagna (Ascendant) is {chart.lagna.rashi_name} ({r['sanskrit']}). "
        f"{r['summary']} "
        f"Rising degree: {chart.lagna.degree_in_rashi:.2f} deg in the sign."
    )


def moon_blurb(chart: KundliChart) -> str:
    moon = chart.planets["Moon"]
    r = rashis()[str(moon.info.rashi_index)]
    n = nakshatras()[str(moon.info.nakshatra_index)]
    return (
        f"Moon is in {moon.info.rashi_name} ({r['sanskrit']}), "
        f"nakshatra {moon.info.nakshatra_name} (pada {moon.info.pada}). "
        f"{n['summary']} Emotionally: {r['summary']}"
    )


def planet_lines(chart: KundliChart) -> List[str]:
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    kb = planets()
    lines = []
    for name in order:
        pl = chart.planets[name]
        meta = kb[name]
        retro = " (R)" if pl.info.retrograde else ""
        lines.append(
            f"{name}{retro}: {pl.info.rashi_name} | House {pl.house} | "
            f"{pl.info.nakshatra_name} pada {pl.info.pada} | "
            f"{pl.info.degree_in_rashi:.2f} deg - {meta['summary']}"
        )
    return lines


def house_lines(chart: KundliChart) -> List[str]:
    kb = houses()
    lines = []
    for h in chart.houses:
        meta = kb[str(h.number)]
        occ = ", ".join(h.planets) if h.planets else "empty"
        lines.append(
            f"House {h.number} ({meta['name']}) - {h.rashi_name}: [{occ}]. {meta['summary']}"
        )
    return lines


def strengths_summary(chart: KundliChart, yogas: List[YogaResult]) -> List[str]:
    notes: List[str] = []
    present = [y for y in yogas if y.present]
    if present:
        notes.append(
            "Notable combinations: " + ", ".join(y.name for y in present) + "."
        )

    # Simple focus: strongest occupied kendras / personal planets
    for house_num, label in [(1, "self/vitality"), (10, "career"), (7, "partnerships"), (5, "creativity")]:
        occ = chart.houses[house_num - 1].planets
        if occ:
            notes.append(f"House {house_num} ({label}) is active with: {', '.join(occ)}.")

    # Benefics vs challenging in Lagna
    lagna_planets = chart.houses[0].planets
    if lagna_planets:
        notes.append(
            f"Planets in Lagna shape first impressions and vitality: {', '.join(lagna_planets)}."
        )
    else:
        notes.append(
            f"Empty Lagna sign {chart.lagna.rashi_name} - personality colors more from Lagna lord and Moon."
        )

    notes.append(moon_blurb(chart))
    return notes


def dasha_summary(timeline: DashaTimeline) -> List[str]:
    lines = []
    bal = timeline.balance_at_birth
    lines.append(
        f"At birth, {bal['lord']} mahadasha had about {bal['years_remaining']:.2f} "
        f"of {bal['full_years']} years remaining (from Moon nakshatra balance)."
    )
    if timeline.current_mahadasha:
        m = timeline.current_mahadasha
        lines.append(
            f"Current Mahadasha: {m.lord} "
            f"({m.start.date().isoformat()} -> {m.end.date().isoformat()})."
        )
    if timeline.current_antardasha:
        a = timeline.current_antardasha
        lines.append(
            f"Current Antardasha: {a.lord} "
            f"({a.start.date().isoformat()} -> {a.end.date().isoformat()})."
        )
        kb = planets()
        lord = timeline.current_mahadasha.lord if timeline.current_mahadasha else ""
        sub = a.lord
        if lord in kb:
            lines.append(f"Mahadasha lord theme: {kb[lord]['summary']}")
        if sub in kb:
            lines.append(f"Antardasha lord theme: {kb[sub]['summary']}")
    return lines


def build_interpretation(chart: KundliChart, timeline: DashaTimeline) -> dict:
    yoga_list = detect_yogas(chart)
    return {
        "disclaimer": (
            "This report uses classical Jyotish computation for learning and reflective guidance. "
            "It is not medical, legal, financial, or destiny advice. For important life decisions, "
            "consult a qualified professional."
        ),
        "lagna": lagna_blurb(chart),
        "moon": moon_blurb(chart),
        "planets": planet_lines(chart),
        "houses": house_lines(chart),
        "yogas": yoga_list,
        "dasha": dasha_summary(timeline),
        "strengths": strengths_summary(chart, yoga_list),
    }
