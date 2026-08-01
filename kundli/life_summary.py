"""Life Summary in classical Jyotish voice: dasha windows, doshas, upaya."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Sequence, Set, Tuple

from kundli.chart import HouseInfo, KundliChart
from kundli.dasha import DashaPeriod, DashaTimeline, _antardashas

CONTENT_VERSION = "jyotish-v2"

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

HOUSE_NAME = {
    1: "Lagna (self/body)",
    2: "2nd (wealth/speech/family)",
    3: "3rd (courage/effort)",
    4: "4th (home/mother/peace)",
    5: "5th (children/intelligence)",
    6: "6th (health/enemies/service)",
    7: "7th (marriage/partnership)",
    8: "8th (longevity/sudden change)",
    9: "9th (luck/dharma/father)",
    10: "10th (career/status)",
    11: "11th (gains/networks)",
    12: "12th (loss/foreign/moksha)",
}

CAREER_BY_SIGN = {
    "Aries": "initiative-led work — engineering, defense, entrepreneurship, leadership",
    "Taurus": "steady wealth crafts — finance, banking, design, real estate, luxury trade",
    "Gemini": "information work — writing, media, sales, teaching, tech communication",
    "Cancer": "care-and-people work — HR, hospitality, counseling, property, public service",
    "Leo": "visible authority — management, brand, performance, education leadership",
    "Virgo": "precision work — analytics, health services, accounting, quality systems",
    "Libra": "balance roles — law, consulting, design, diplomacy, partnerships",
    "Scorpio": "depth work — research, investigation, crisis finance, transformative fields",
    "Sagittarius": "guidance paths — teaching, publishing, law, coaching, higher learning",
    "Capricorn": "structure work — operations, government, engineering, corporate hierarchy",
    "Aquarius": "systems/tech — innovation, networks, unconventional or social-tech careers",
    "Pisces": "imaginative service — arts, healing, film, charity, compassionate craft",
}

HEALTH_BY_SIGN = {
    "Aries": "head heat, haste injuries, inflammatory flares",
    "Taurus": "throat/thyroid, food-rest imbalance",
    "Gemini": "nerves, lungs, mental overstimulation",
    "Cancer": "digestion, chest, mood-linked appetite",
    "Leo": "heart strain, heat, upper-back tension",
    "Virgo": "gut assimilation, worry loops",
    "Libra": "kidneys, lumbar fatigue, work–rest imbalance",
    "Scorpio": "hidden stress, reproductive/elimination sensitivity",
    "Sagittarius": "hips, liver load, overextension",
    "Capricorn": "bones/joints, fatigue from duty",
    "Aquarius": "circulation, ankles, irregular routine",
    "Pisces": "feet, sleep debt, immune dips from emotion",
}

# Classical-lite upaya (educational; not medical/financial advice)
UPAYA: Dict[str, Dict[str, str]] = {
    "Sun": {
        "mantra": "Offer Surya namaskar or chant Om Suryaya Namah with sunrise discipline",
        "charity": "Donate wheat, copper, or help a father-figure / authority in need on Sundays",
        "gemstone": "Ruby (Manik) only after proper consultation — linked to vitality and status",
    },
    "Moon": {
        "mantra": "Chant Om Chandraya Namah; keep a calm night routine and Monday white/pearl discipline",
        "charity": "Donate milk, rice, or white clothes; care for maternal figures on Mondays",
        "gemstone": "Pearl (Moti) for emotional steadiness — only if Moon is a functional benefic for you",
    },
    "Mars": {
        "mantra": "Hanuman Chalisa or Om Mangalaya Namah on Tuesdays to cool Manglik friction",
        "charity": "Donate red lentils (masoor), jaggery, or blood-donation if medically fit",
        "gemstone": "Red coral (Moonga) for Mars — use only under a qualified Jyotishi’s guidance",
    },
    "Mercury": {
        "mantra": "Om Budhaya Namah; journaling and clear speech practice on Wednesdays",
        "charity": "Donate green gram, books, or support a student’s learning",
        "gemstone": "Emerald (Panna) for Mercury — only when Mercury supports your lagna",
    },
    "Jupiter": {
        "mantra": "Om Gurave Namah or Guru mantra on Thursdays; seek a living teacher’s blessing",
        "charity": "Donate chana dal, turmeric, yellow cloth, or support a teacher/temple on Thursday",
        "gemstone": "Yellow sapphire (Pukhraj) for Jupiter — classic expansion stone, consult before wearing",
    },
    "Venus": {
        "mantra": "Om Shukraya Namah; keep relationship speech clean on Fridays",
        "charity": "Donate white sweets, sugar, or support women’s welfare / arts on Fridays",
        "gemstone": "Diamond or white sapphire for Venus — harmony stone, not a shortcut to marriage",
    },
    "Saturn": {
        "mantra": "Om Sham Shanicharaya Namah; patience vows and Saturday seva",
        "charity": "Donate sesame oil, black cloth, or serve elders/workers on Saturdays",
        "gemstone": "Blue sapphire (Neelam) is strong medicine — never self-prescribe for Saturn",
    },
    "Rahu": {
        "mantra": "Durga / Om Raam Rahave Namah; avoid impulsive ‘quick money’ fantasies",
        "charity": "Donate mustard oil, blankets, or help someone with foreign/tech hardship",
        "gemstone": "Hessonite (Gomed) for Rahu — only after careful chart check",
    },
    "Ketu": {
        "mantra": "Om Ketave Namah or Ganapati; practice detachment from empty status",
        "charity": "Donate multi-colored blankets, dog food, or support spiritual learning",
        "gemstone": "Cat’s eye (Lehsunia) for Ketu — specialist stone, use carefully",
    },
}

PLANET_KARMA = {
    "Sun": "authority, father karma, and how you claim dignity",
    "Moon": "mind, mother karma, and emotional debts",
    "Mars": "aggression, siblings, and courage debts",
    "Mercury": "speech, trade, and learning contracts",
    "Jupiter": "dharma, teachers, and grace you must honor",
    "Venus": "relationships, pleasure, and fairness in love",
    "Saturn": "duty, delay, and long unpaid karmic invoices",
    "Rahu": "unfinished worldly hunger and foreign/unusual paths",
    "Ketu": "past-life skill and the need to release ego",
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


def _houses_ruled(chart: KundliChart, planet: str) -> List[int]:
    return [h.number for h in chart.houses if SIGN_LORD[h.rashi_name] == planet]


def _ruled_phrase(chart: KundliChart, planet: str) -> str:
    ruled = _houses_ruled(chart, planet)
    if not ruled:
        return f"{planet} does not lord any house from this Lagna (nodes)"
    bits = [HOUSE_NAME[n] for n in ruled]
    return f"{planet} rules your " + " and ".join(bits)


def _occ(h: HouseInfo) -> str:
    return ", ".join(h.planets) if h.planets else "no grahas sitting (lord carries result)"


def _age_at(chart: KundliChart, when: datetime) -> int:
    b = chart.birth.birth_date
    return when.year - b.year - ((when.month, when.day) < (b.month, b.day))


def _now(timeline: DashaTimeline) -> datetime:
    ref = timeline.current_antardasha or timeline.current_mahadasha
    if ref and ref.start.tzinfo:
        return datetime.now(tz=ref.start.tzinfo)
    return datetime.now()


def _manglik(chart: KundliChart) -> Tuple[bool, str, bool]:
    """Classical Manglik: Mars in 1/4/7/8/12. Mitigation: Venus with 7th or Jupiter aspect-like kendra support."""
    mars_h = chart.planets["Mars"].house
    present = mars_h in (1, 4, 7, 8, 12)
    detail = f"Mars sits in house {mars_h} ({chart.planets['Mars'].info.rashi_name})"
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
            scored.append((a.start, f"{m.lord}–{a.lord} (current)", _fmt(a), s + 10))
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


def _upaya_inline(planets: Sequence[str]) -> str:
    bits: List[str] = []
    for p in planets:
        u = UPAYA.get(p)
        if not u:
            continue
        bits.append(
            f"For {p}: mantra — {u['mantra']}; charity — {u['charity']}; "
            f"gemstone note — {u['gemstone']}"
        )
    if not bits:
        return ""
    return (
        "To balance these energies, stay with one remedy lane for 40–90 days. "
        + " ".join(bits)
        + " Remedies support karma hygiene; they are not medical, legal, or financial advice."
    )


def build_life_summary(chart: KundliChart, timeline: DashaTimeline) -> List[dict]:
    """One continuous Jyotish consult-style reading (not separate section cards)."""
    h2, h4, h6, h7, h10 = (_house(chart, n) for n in (2, 4, 6, 7, 10))
    lord10, lord10_h, lord10_sign = _lord_placement(chart, 10)
    lord2, lord2_h, lord2_sign = _lord_placement(chart, 2)
    lord7, lord7_h, lord7_sign = _lord_placement(chart, 7)
    lord4, lord4_h, lord4_sign = _lord_placement(chart, 4)
    lord6, lord6_h, lord6_sign = _lord_placement(chart, 6)

    maha = timeline.current_mahadasha
    antar = timeline.current_antardasha
    now = _now(timeline)
    age = _age_at(chart, now)
    manglik, manglik_detail, mitigated = _manglik(chart)

    if maha and antar:
        opening = (
            f"Your kundli is read here as a karma blueprint — past-life debts and future destiny "
            f"moving through operational time windows, not as a personality quiz. "
            f"You are currently running {maha.lord} Mahadasha until {_fmt_end(maha)}, "
            f"with {antar.lord} Antardasha active ({_fmt(antar)}). "
            f"{_ruled_phrase(chart, maha.lord)}. "
            f"This stretch activates karma around {PLANET_KARMA.get(maha.lord, maha.lord)}, "
            f"with the shorter chapter coloring {PLANET_KARMA.get(antar.lord, antar.lord)}."
        )
    else:
        opening = (
            "Your kundli is read here as a karma blueprint — past-life debts and future destiny "
            "through house lords and grahas. A precise birth time sharpens Mahadasha windows."
        )

    golden = False
    golden_why = ""
    if maha:
        ruled = _houses_ruled(chart, maha.lord)
        if set(ruled) & {2, 9, 10, 11}:
            golden = True
            hit = [HOUSE_NAME[n] for n in ruled if n in (2, 9, 10, 11)]
            golden_why = f"because {maha.lord} rules " + " and ".join(hit)
        elif maha.lord in h10.planets:
            golden = True
            golden_why = f"because {maha.lord} sits in your 10th house of career"
        elif antar and antar.lord in h10.planets:
            golden = True
            golden_why = f"because {antar.lord} Antardasha lights grahas in your 10th"

    rahu_warn = (
        (maha and maha.lord == "Rahu")
        or (antar and antar.lord == "Rahu")
        or chart.planets["Rahu"].house in (2, 6, 8, 10, 11, 12)
    )

    career = (
        f"Regarding career and wealth (10th and 2nd houses): the 10th is {h10.rashi_name} "
        f"with {_occ(h10)}; 10th lord {lord10} sits in house {lord10_h} ({lord10_sign}). "
        f"The work field this points to is {CAREER_BY_SIGN[h10.rashi_name]}. "
        f"The 2nd house of resources is {h2.rashi_name}; 2nd lord {lord2} is in house {lord2_h} "
        f"({lord2_sign}). "
        + (
            f"Because of the current dasha, this is a golden window to build, launch, or ask for growth "
            f"{golden_why} — use it for structured business or career moves, not speculation. "
            if golden
            else "In this dasha, prefer steady duty and timed asks over sudden leaps. "
        )
        + (
            "Watch Rahu’s hunger for shortcuts: it can create illusions of quick money; "
            "verify every offer twice before you commit. "
            if rahu_warn
            else "Keep income plans transparent and slow enough to stay clean. "
        )
    )

    love = (
        f"When analyzing love and family (7th and 4th houses): the 7th is {h7.rashi_name} "
        f"({_occ(h7)}); 7th lord {lord7} sits in house {lord7_h} ({lord7_sign}). "
        f"The 4th of home/peace is {h4.rashi_name}; 4th lord {lord4} is in house {lord4_h} "
        f"({lord4_sign}). "
        + (
            f"Your chart shows Manglik Dosha — {manglik_detail} — which classical texts link with "
            f"friction or delay around marriage. "
            if manglik
            else f"Basic Manglik Dosha (Mars in 1/4/7/8/12) is not indicated ({manglik_detail}). "
        )
        + (
            "However, benefic Venus/Jupiter support mitigates the severity; still do Kundali matching "
            "before commitment. "
            if manglik and mitigated
            else (
                "Without a clear Venus/Jupiter cushion, take matching and timing seriously. "
                if manglik
                else "Even so, gun milan / dosha balance with a partner’s chart remains essential. "
            )
        )
        + (
            f"Mars matures around age 28; you are {age} now"
            + (
                ", so mitigation by maturity is already available. "
                if age >= 28
                else " — patience until that maturity helps reduce heat. "
            )
        )
    )

    weak: List[str] = []
    for name in ("Saturn", "Mars", "Rahu", "Ketu", "Sun"):
        if chart.planets[name].house in (6, 8, 12) or name == lord6:
            weak.append(name)
    if not weak:
        weak = [lord6, "Moon"]

    health = (
        f"For health and daily struggles (6th house): the 6th is {h6.rashi_name} with {_occ(h6)}; "
        f"6th lord {lord6} sits in house {lord6_h} ({lord6_sign}). "
        f"Themes to watch in the body-mind field include {HEALTH_BY_SIGN[h6.rashi_name]}. "
        f"Pressure grahas in this story: {', '.join(weak)}. "
        f"When the running dasha lords touch the 6th/8th axis, old conflict or fatigue karma can surface "
        f"for clearing — treat it as a repair window, not punishment. "
        f"Spiritual blockage often shows first as skipped rest, bitter speech, or abandoned seva."
    )

    remedy_planets: List[str] = []
    for p in ([maha.lord, antar.lord] if maha and antar else []) + (
        ["Mars", "Venus"] if manglik else ["Venus", lord7]
    ) + weak:
        if p not in remedy_planets:
            remedy_planets.append(p)
    remedy_planets = remedy_planets[:3]

    closing = (
        "Ultimately this is a predictive, time-bound map: less about why you feel a certain way, "
        "more about when events tend to manifest and how to spiritually steady the field. "
        + _upaya_inline(remedy_planets)
    )

    timing: List[dict] = []
    if maha and antar:
        timing.append({"label": f"{maha.lord}–{antar.lord} now", "range": _fmt(antar)})
        timing.append({"label": f"{maha.lord} Mahadasha", "range": _fmt(maha)})
    for lab, rng in _windows(chart, timeline, _keys_for_houses(chart, (10, 7, 6), ()), limit=2):
        if not any(t["range"] == rng for t in timing):
            timing.append({"label": lab, "range": rng})

    kicker = (
        (f"{maha.lord} Mahadasha until {_fmt_end(maha)}" if maha else "Dasha pending precise time")
        + (" · golden career window" if golden else "")
        + (" · Manglik noted" if manglik else "")
    )

    return [
        {
            "id": "consult",
            "title": "Jyotish consult summary",
            "kicker": kicker,
            "insights": [opening, career, love, health, closing],
            "timing": timing[:4],
            "ask_topic": "career",
            "remedies": remedy_planets,
            "version": CONTENT_VERSION,
        }
    ]
