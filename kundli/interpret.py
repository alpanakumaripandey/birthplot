"""Plain-language interpretations from chart + knowledge base."""

from __future__ import annotations

from typing import List

from kundli.chart import KundliChart
from kundli.dasha import DashaTimeline
from kundli.knowledge_loader import houses, nakshatras, planets, rashis
from kundli.life_summary import build_life_summary
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
    """Short, non-duplicative notes for chips / major summary."""
    notes: List[str] = []
    classical = [y for y in yogas if y.present and getattr(y, "kind", "classical") == "classical"]
    if classical:
        notes.append("Classical yogas on: " + ", ".join(y.name for y in classical) + ".")

    for house_num, label in [(1, "self"), (10, "career"), (7, "partners"), (5, "creativity")]:
        occ = chart.houses[house_num - 1].planets
        if occ:
            notes.append(f"H{house_num} ({label}): {', '.join(occ)}.")

    lagna_planets = chart.houses[0].planets
    if lagna_planets:
        notes.append(f"Lagna occupied by {', '.join(lagna_planets)}.")
    else:
        notes.append(f"Empty Lagna ({chart.lagna.rashi_name}) — lean on Lagna lord + Moon.")

    moon = chart.planets["Moon"]
    notes.append(
        f"Moon in {moon.info.rashi_name} / {chart.moon_nakshatra} p{chart.moon_pada} (H{moon.house})."
    )
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


def life_area_briefs(chart: KundliChart, timeline: DashaTimeline) -> List[dict]:
    """Career / education / relationship cards for the You report."""
    from kundli.qa import (
        answer_topic,
        _fmt_range,
        _topic_lords,
        _lord_hits_topic,
        _plain,
    )
    from kundli.knowledge_loader import topics

    specs = [
        ("career", "Career", "career"),
        ("education", "Education", "education"),
        ("marriage", "Relationship", "marriage"),
    ]
    out: List[dict] = []
    topic_kb = topics()
    for key, label, ask_topic in specs:
        meta = topic_kb[key]
        full = answer_topic(chart, timeline, key)
        relevant = _topic_lords(chart, meta)
        plain = _plain(key)

        if timeline.current_mahadasha and timeline.current_antardasha:
            m = timeline.current_mahadasha
            a = timeline.current_antardasha
            hits = [x for x in (m.lord, a.lord) if _lord_hits_topic(x, relevant, meta)]
            if hits:
                headline = f"Right now: an important stretch for {plain['short']}"
                present_bit = plain["active"].split(".")[0] + "."
            else:
                headline = f"Right now: a gentler stretch for {plain['short']}"
                present_bit = plain["quiet"].split(".")[0] + "."
            present_bit = f"{present_bit} This chapter runs through {a.end.strftime('%b %Y')}."
        else:
            headline = f"{plain.get('title_hint', label)} at a glance"
            present_bit = plain["about"]

        ahead_bit = plain["future_quiet"]
        if timeline.current_antardasha and timeline.antardashas_in_current:
            for antar in timeline.antardashas_in_current:
                if antar.start <= timeline.current_antardasha.start:
                    continue
                if _lord_hits_topic(antar.lord, relevant, meta):
                    ahead_bit = (
                        f"Coming up ({_fmt_range(antar)}): {plain['future_active']}"
                    )
                    break
            else:
                if timeline.current_mahadasha and timeline.mahadashas:
                    for maha in timeline.mahadashas:
                        if maha.start <= timeline.current_mahadasha.start:
                            continue
                        ahead_bit = (
                            f"From {maha.start.strftime('%b %Y')}: a longer new chapter begins."
                        )
                        break

        out.append(
            {
                "id": key,
                "label": label,
                "ask_topic": ask_topic,
                "headline": headline,
                "blurb": f"{present_bit} {ahead_bit}",
                "full": full,
                "houses": list(meta["houses"]),
                "planets": list(meta["planets"]),
            }
        )
    return out


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
        "life_areas": life_area_briefs(chart, timeline),
        "life_summary": build_life_summary(chart, timeline),
    }
