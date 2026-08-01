"""Life Summary: straight past / present / future facts from D1 + dasha."""

from __future__ import annotations

from datetime import datetime
from typing import List, Sequence, Set, Tuple

from kundli.chart import HouseInfo, KundliChart
from kundli.dasha import DashaPeriod, DashaTimeline, _antardashas

CONTENT_VERSION = "jyotish-v3"

SIGN_LORD = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

CAREER_BY_SIGN = {
    "Aries": "leadership, engineering, defense, or startups",
    "Taurus": "finance, banking, design, or real estate",
    "Gemini": "writing, media, sales, teaching, or tech communication",
    "Cancer": "care, HR, hospitality, counseling, or property",
    "Leo": "management, brand, performance, or education leadership",
    "Virgo": "analytics, health services, accounting, or quality work",
    "Libra": "law, consulting, design, diplomacy, or partnerships",
    "Scorpio": "research, investigation, depth finance, or crisis work",
    "Sagittarius": "teaching, publishing, law, coaching, or higher learning",
    "Capricorn": "operations, government, engineering, or corporate structure",
    "Aquarius": "technology, networks, innovation, or social systems",
    "Pisces": "arts, healing, film, charity, or imaginative service",
}

PARTNER_BY_SIGN = {
    "Aries": "direct and independent",
    "Taurus": "loyal and security-seeking",
    "Gemini": "talkative and mentally restless",
    "Cancer": "protective and home-centered",
    "Leo": "warm and needing appreciation",
    "Virgo": "careful and detail-minded",
    "Libra": "fair and companion-focused",
    "Scorpio": "intense and deeply loyal",
    "Sagittarius": "honest and freedom-loving",
    "Capricorn": "serious and long-term oriented",
    "Aquarius": "friendly but needs space",
    "Pisces": "gentle and emotionally open",
}

HEALTH_BY_SIGN = {
    "Aries": "head strain, haste injuries",
    "Taurus": "throat, food and rest habits",
    "Gemini": "nerves, lungs, overthinking fatigue",
    "Cancer": "digestion, mood-linked appetite",
    "Leo": "heart strain, heat, upper-back tension",
    "Virgo": "gut, worry loops",
    "Libra": "kidneys, lower back, work–rest balance",
    "Scorpio": "hidden stress, reproductive/elimination sensitivity",
    "Sagittarius": "hips, liver load, overextension",
    "Capricorn": "bones, joints, duty fatigue",
    "Aquarius": "circulation, ankles, irregular routine",
    "Pisces": "feet, sleep debt, immune dips",
}


def _fmt(p: DashaPeriod) -> str:
    return f"{p.start.strftime('%b %Y')}–{p.end.strftime('%b %Y')}"


def _fmt_end(p: DashaPeriod) -> str:
    return p.end.strftime("%b %Y")


def _house(chart: KundliChart, num: int) -> HouseInfo:
    return chart.houses[num - 1]


def _lord_of_house(chart: KundliChart, house_num: int) -> str:
    return SIGN_LORD[_house(chart, house_num).rashi_name]


def _lord_placement(chart: KundliChart, house_num: int) -> Tuple[str, int, str]:
    lord = _lord_of_house(chart, house_num)
    pl = chart.planets[lord]
    return lord, pl.house, pl.info.rashi_name


def _occ(h: HouseInfo) -> str:
    return ", ".join(h.planets) if h.planets else "empty"


def _now(timeline: DashaTimeline) -> datetime:
    ref = timeline.current_antardasha or timeline.current_mahadasha
    if ref and ref.start.tzinfo:
        return datetime.now(tz=ref.start.tzinfo)
    return datetime.now()


def _age_at(chart: KundliChart, when: datetime) -> int:
    b = chart.birth.birth_date
    return when.year - b.year - ((when.month, when.day) < (b.month, b.day))


def _manglik(chart: KundliChart) -> Tuple[bool, str, bool]:
    mars_h = chart.planets["Mars"].house
    present = mars_h in (1, 4, 7, 8, 12)
    detail = f"Mars in house {mars_h} ({chart.planets['Mars'].info.rashi_name})"
    venus_h = chart.planets["Venus"].house
    jup_h = chart.planets["Jupiter"].house
    mitigated = present and (
        venus_h in (1, 4, 5, 7, 9, 10)
        or jup_h in (1, 4, 7, 10)
        or "Venus" in _house(chart, 7).planets
        or "Jupiter" in _house(chart, 7).planets
    )
    return present, detail, mitigated


def _keys_for_houses(chart: KundliChart, houses: Sequence[int], extras: Sequence[str] = ()) -> Set[str]:
    keys: Set[str] = set(extras)
    for h in houses:
        lord, _, _ = _lord_placement(chart, h)
        keys.add(lord)
        keys.update(_house(chart, h).planets)
    return keys


def _windows(
    chart: KundliChart,
    timeline: DashaTimeline,
    keys: Set[str],
    *,
    limit: int = 3,
) -> List[Tuple[str, str]]:
    now = _now(timeline)
    scored: List[Tuple[datetime, str, str, int]] = []

    if timeline.current_mahadasha and timeline.current_antardasha:
        m, a = timeline.current_mahadasha, timeline.current_antardasha
        s = (2 if a.lord in keys else 0) + (2 if m.lord in keys else 0)
        if s:
            scored.append((a.start, f"{m.lord}–{a.lord}", _fmt(a), s + 10))
        for antar in timeline.antardashas_in_current:
            if antar.start <= a.start or antar.end <= now:
                continue
            if antar.lord in keys:
                scored.append((antar.start, f"{m.lord}–{antar.lord}", _fmt(antar), 6))

    if timeline.current_mahadasha:
        for maha in timeline.mahadashas:
            if maha.start <= timeline.current_mahadasha.start:
                continue
            if maha.lord in keys:
                scored.append((maha.start, f"{maha.lord} Mahadasha", _fmt(maha), 4))
            else:
                for antar in _antardashas(maha):
                    if antar.end <= now:
                        continue
                    if antar.lord in keys:
                        scored.append((antar.start, f"{maha.lord}–{antar.lord}", _fmt(antar), 3))
                        break
            if len(scored) >= limit + 2:
                break

    scored.sort(key=lambda t: (-t[3], t[0]))
    out: List[Tuple[str, str]] = []
    seen = set()
    for _, label, rng, _ in scored:
        if (label, rng) in seen:
            continue
        seen.add((label, rng))
        out.append((label, rng))
        if len(out) >= limit:
            break
    return out


def _next_maha(timeline: DashaTimeline) -> DashaPeriod | None:
    if not timeline.current_mahadasha:
        return None
    for m in timeline.mahadashas:
        if m.start > timeline.current_mahadasha.start:
            return m
    return None


def build_life_summary(chart: KundliChart, timeline: DashaTimeline) -> List[dict]:
    """Straight past / present / future life facts — no remedies, no meta."""
    h1 = _house(chart, 1)
    h6 = _house(chart, 6)
    h7 = _house(chart, 7)
    h10 = _house(chart, 10)

    lord10, lord10_h, lord10_sign = _lord_placement(chart, 10)
    lord2, lord2_h, lord2_sign = _lord_placement(chart, 2)
    lord7, lord7_h, lord7_sign = _lord_placement(chart, 7)
    lord4, lord4_h, lord4_sign = _lord_placement(chart, 4)
    lord6, lord6_h, lord6_sign = _lord_placement(chart, 6)

    maha = timeline.current_mahadasha
    antar = timeline.current_antardasha
    next_m = _next_maha(timeline)
    now = _now(timeline)
    age = _age_at(chart, now)
    manglik, manglik_detail, mitigated = _manglik(chart)

    career_wins = _windows(chart, timeline, _keys_for_houses(chart, (10, 2, 11), ("Sun", "Saturn")))
    love_wins = _windows(chart, timeline, _keys_for_houses(chart, (7, 4), ("Venus", "Jupiter", "Mars")))
    cur_rng = _fmt(antar) if antar else ""
    future_career = [w for w in career_wins if w[1] != cur_rng]
    future_love = [w for w in love_wins if w[1] != cur_rng]

    past = (
        f"Rising {h1.rashi_name}. "
        f"Career: 10th in {h10.rashi_name} ({_occ(h10)}), 10th lord {lord10} in house {lord10_h} "
        f"({lord10_sign}) — {CAREER_BY_SIGN[h10.rashi_name]}. "
        f"Money: 2nd lord {lord2} in house {lord2_h} ({lord2_sign}). "
        f"Marriage: 7th in {h7.rashi_name} ({_occ(h7)}), partner tone {PARTNER_BY_SIGN[h7.rashi_name]}; "
        f"7th lord {lord7} in house {lord7_h} ({lord7_sign}). "
        f"Home: 4th lord {lord4} in house {lord4_h} ({lord4_sign}). "
        + (
            f"Manglik yes ({manglik_detail})"
            + (" — Venus/Jupiter softens it." if mitigated else ".")
            if manglik
            else f"Manglik no ({manglik_detail})."
        )
        + f" Health: 6th lord {lord6} in house {lord6_h} ({lord6_sign}); "
        f"watch {HEALTH_BY_SIGN[h6.rashi_name]}."
    )

    if maha and antar:
        c_keys = _keys_for_houses(chart, (10, 2, 11))
        l_keys = _keys_for_houses(chart, (7, 4), ("Venus", "Jupiter"))
        career_now = (
            "Career and money are in an active window"
            if maha.lord in c_keys or antar.lord in c_keys or maha.lord in h10.planets or antar.lord in h10.planets
            else "Career and money are in a steadier window"
        )
        love_now = (
            "Relationship themes are active"
            if maha.lord in l_keys or antar.lord in l_keys
            else "Relationship pace is quieter"
        )
        present = (
            f"Age {age}. {maha.lord} Mahadasha until {_fmt_end(maha)}; "
            f"{antar.lord} Antardasha {_fmt(antar)}. "
            f"{career_now}. {love_now}. "
            f"Health watch: {HEALTH_BY_SIGN[h6.rashi_name]}."
        )
    else:
        present = f"Age {age}. Need precise birth time for the current dasha clock."

    future_bits: List[str] = []
    if next_m:
        future_bits.append(f"Next Mahadasha {next_m.lord} {_fmt(next_m)}")
    if future_career:
        future_bits.append(
            "Career/money: " + "; ".join(f"{lab} {rng}" for lab, rng in future_career[:2])
        )
    if future_love:
        future_bits.append(
            "Marriage/home: " + "; ".join(f"{lab} {rng}" for lab, rng in future_love[:2])
        )
    if manglik and age < 28:
        future_bits.append("Manglik heat eases after age 28")
    future = ". ".join(future_bits) + "." if future_bits else "No stronger near window listed."

    timing: List[dict] = []
    if maha and antar:
        timing.append({"label": "Now", "range": f"{maha.lord}–{antar.lord} · {_fmt(antar)}"})
    if next_m:
        timing.append({"label": "Next", "range": f"{next_m.lord} · {_fmt(next_m)}"})
    seen_rng = {t["range"] for t in timing}
    for lab, rng in future_career[:1] + future_love[:1]:
        if rng in seen_rng:
            continue
        timing.append({"label": lab, "range": rng})
        seen_rng.add(rng)

    kicker = (
        f"{maha.lord}–{antar.lord} · to {_fmt_end(maha)}"
        if maha and antar
        else "Past · Present · Future"
    )

    return [
        {
            "id": "life",
            "title": "Life summary",
            "kicker": kicker,
            "insights": [past, present, future],
            "timing": timing[:4],
            "ask_topic": "career",
            "version": CONTENT_VERSION,
        }
    ]
