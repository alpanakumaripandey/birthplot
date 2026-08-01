"""Life Summary in classical Jyotish voice: dasha windows, doshas, upaya."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Sequence, Set, Tuple

from kundli.chart import HouseInfo, KundliChart
from kundli.dasha import DashaPeriod, DashaTimeline, _antardashas

CONTENT_VERSION = "jyotish-v1"

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


def _upaya_block(planets: Sequence[str]) -> str:
    lines = ["Upaya (remedies) — pick one lane and stay consistent for 40–90 days:"]
    for p in planets:
        u = UPAYA.get(p)
        if not u:
            continue
        lines.append(f"• {p}: Mantra — {u['mantra']}. Charity — {u['charity']}. Gemstone — {u['gemstone']}.")
    lines.append(
        "Remedies support karma hygiene; they do not replace medical, legal, or financial advice."
    )
    return " ".join(lines) if len(lines) == 1 else "\n".join(lines)


def _panel(
    *,
    id: str,
    title: str,
    kicker: str,
    insights: List[str],
    timing: List[dict],
    ask_topic: str,
    remedies: List[str],
) -> dict:
    return {
        "id": id,
        "title": title,
        "kicker": kicker,
        "insights": insights,
        "timing": timing,
        "ask_topic": ask_topic,
        "remedies": remedies,
        "version": CONTENT_VERSION,
    }


def build_life_summary(chart: KundliChart, timeline: DashaTimeline) -> List[dict]:
    """Predictive Jyotish summary: when windows open + how to balance them."""
    h2, h4, h6, h7, h9, h10 = (_house(chart, n) for n in (2, 4, 6, 7, 9, 10))
    lord10, lord10_h, lord10_sign = _lord_placement(chart, 10)
    lord2, lord2_h, lord2_sign = _lord_placement(chart, 2)
    lord7, lord7_h, lord7_sign = _lord_placement(chart, 7)
    lord4, lord4_h, lord4_sign = _lord_placement(chart, 4)
    lord6, lord6_h, lord6_sign = _lord_placement(chart, 6)

    maha = timeline.current_mahadasha
    antar = timeline.current_antardasha
    now = _now(timeline)
    age = _age_at(chart, now)

    dasha_line = "Dasha timing needs a precise birth time for sharper windows."
    karma_dasha = ""
    if maha and antar:
        dasha_line = (
            f"You are currently running {maha.lord} Mahadasha until {_fmt_end(maha)}, "
            f"with {antar.lord} Antardasha active ({_fmt(antar)})."
        )
        karma_dasha = (
            f"This period activates karma around {PLANET_KARMA.get(maha.lord, maha.lord)} "
            f"and the shorter {PLANET_KARMA.get(antar.lord, antar.lord)}."
        )

    # --- Career & Wealth ---
    career_keys = _keys_for_houses(chart, (10, 2, 11, 6), ("Sun", "Saturn", "Mercury", "Mars", "Jupiter"))
    career_wins = _windows(chart, timeline, career_keys)
    golden = False
    golden_why = ""
    if maha:
        ruled = _houses_ruled(chart, maha.lord)
        if set(ruled) & {2, 9, 10, 11}:
            golden = True
            hit = [HOUSE_NAME[n] for n in ruled if n in (2, 9, 10, 11)]
            golden_why = f"because {maha.lord} rules " + " and ".join(hit)
        elif maha.lord in _house(chart, 10).planets:
            golden = True
            golden_why = f"because {maha.lord} currently sits in your 10th house of career"
        elif antar and antar.lord in _house(chart, 10).planets:
            golden = True
            golden_why = f"because {antar.lord} Antardasha activates grahas in your 10th"

    career_insights = [
        (
            f"{dasha_line} {_ruled_phrase(chart, maha.lord) if maha else ''}. "
            + (
                f"This is a golden operational window for career/wealth moves {golden_why}. "
                if golden
                else "Results in this stretch come more through duty and timed effort than shortcuts. "
            )
            + karma_dasha
        ).strip(),
        (
            f"10th house is {h10.rashi_name} with {_occ(h10)}. "
            f"10th lord {lord10} sits in house {lord10_h} ({lord10_sign}). "
            f"Field blueprint: {CAREER_BY_SIGN[h10.rashi_name]}. "
            f"2nd house (wealth) is {h2.rashi_name}; 2nd lord {lord2} is in house {lord2_h} ({lord2_sign})."
        ),
        (
            (
                f"Because {maha.lord} currently times your chart"
                + (
                    f" and rules luck/career houses ({', '.join(HOUSE_NAME[n] for n in _houses_ruled(chart, maha.lord) if n in (2, 9, 10, 11))})"
                    if maha and any(n in (2, 9, 10, 11) for n in _houses_ruled(chart, maha.lord))
                    else ""
                )
                + ", prefer launching, promotion asks, or structured business building inside this Mahadasha — "
                "not gambling on ‘quick money’."
                if maha
                else "Build career through skill proof and timed asks."
            )
            + (
                f" Watch Rahu themes ({PLANET_KARMA['Rahu']}) if Rahu is dasha-linked or occupies dusthana/career houses — "
                "illusions of overnight wealth rise then."
                if (maha and maha.lord == "Rahu")
                or (antar and antar.lord == "Rahu")
                or chart.planets["Rahu"].house in (2, 6, 8, 10, 11, 12)
                else ""
            )
        ),
        _upaya_block(
            [
                *(
                    [maha.lord, antar.lord]
                    if maha and antar
                    else [lord10, lord2]
                ),
            ][:2]
        ),
    ]

    # --- Love & Family ---
    manglik, manglik_detail, mitigated = _manglik(chart)
    love_keys = _keys_for_houses(chart, (7, 4, 2, 5), ("Venus", "Jupiter", "Moon", "Mars"))
    love_wins = _windows(chart, timeline, love_keys)
    mars_mature = age >= 28
    love_insights = [
        (
            f"{dasha_line} For marriage/home, track Venus, 7th lord {lord7}, and 4th lord {lord4}. "
            f"7th is {h7.rashi_name} ({_occ(h7)}); 7th lord {lord7} in house {lord7_h} ({lord7_sign}). "
            f"4th is {h4.rashi_name}; 4th lord {lord4} in house {lord4_h} ({lord4_sign})."
        ),
        (
            (
                f"Manglik Dosha note: {manglik_detail} — classical texts link Mars in 1/4/7/8/12 with friction or delay in marriage. "
                if manglik
                else f"Manglik Dosha: not indicated by the basic Mars-in-1/4/7/8/12 rule ({manglik_detail}). "
            )
            + (
                "Benefic Venus/Jupiter support mitigates severity — still prefer Kundali matching before commitment. "
                if manglik and mitigated
                else (
                    "Without clear Venus/Jupiter cushion, take matching and timing seriously. "
                    if manglik
                    else "Still match charts for gun milan / dosha balance before marriage decisions. "
                )
            )
            + (
                f"Mars energy softens after maturity (~age 28); you are {age} now"
                + (" — mitigation window is open." if mars_mature else " — patience until Mars matures helps.")
            )
        ),
        (
            "Operational windows for commitment talks, engagement, or home decisions: "
            + (
                "; ".join(f"{lab} ({rng})" for lab, rng in love_wins)
                if love_wins
                else "no strong near dasha hit — prepare emotionally and financially first"
            )
            + ". This is a time map, not a fixed wedding date."
        ),
        _upaya_block(["Mars", "Venus"] if manglik else ["Venus", lord7]),
    ]

    # --- Health & struggles ---
    health_keys = _keys_for_houses(chart, (1, 6, 8), ("Sun", "Moon", "Mars", "Saturn"))
    health_wins = _windows(chart, timeline, health_keys)
    weak = []
    for name in ("Saturn", "Mars", "Rahu", "Ketu", "Sun"):
        if chart.planets[name].house in (6, 8, 12) or name == lord6:
            weak.append(name)
    if not weak:
        weak = [lord6, "Moon"]

    health_insights = [
        (
            f"6th house (disease/service/struggle) is {h6.rashi_name} with {_occ(h6)}. "
            f"6th lord {lord6} sits in house {lord6_h} ({lord6_sign}). "
            f"Physical watch-themes from sign lore: {HEALTH_BY_SIGN[h6.rashi_name]}. "
            f"Planetary pressure points: {', '.join(weak)}."
        ),
        (
            f"{dasha_line} "
            + (
                f"When {antar.lord if antar else 'the antardasha lord'} or {maha.lord if maha else 'mahadasha lord'} "
                f"touches the 6th/8th axis, old health or workplace conflict karma can surface for clearing — "
                "treat it as a repair window, not punishment."
            )
        ),
        (
            "Supportive health-timing (for routines, checkups, recovery vows): "
            + (
                "; ".join(f"{lab} ({rng})" for lab, rng in health_wins)
                if health_wins
                else "keep year-round discipline; no sharp dasha spike listed"
            )
            + ". Spiritual blockage often shows as ignored rest, bitter speech, or skipped seva — fix those first."
        ),
        _upaya_block(weak[:2]),
    ]

    # --- Destiny / karma overview kicker shared ---
    career_kicker = (
        f"{maha.lord if maha else '—'} Mahadasha"
        + (f" until {_fmt_end(maha)}" if maha else "")
        + (" · golden career window" if golden else " · duty-first window")
    )
    love_kicker = (
        ("Manglik present" if manglik else "Manglik clear (basic rule)")
        + (" · mitigated" if manglik and mitigated else "")
        + (f" · age {age}")
    )
    health_kicker = f"6th lord {lord6} in house {lord6_h} · watch {HEALTH_BY_SIGN[h6.rashi_name].split(',')[0]}"

    return [
        _panel(
            id="career",
            title="Career, Wealth & Karma Windows",
            kicker=career_kicker,
            insights=career_insights,
            timing=[{"label": lab, "range": rng} for lab, rng in career_wins],
            ask_topic="career",
            remedies=[maha.lord, antar.lord] if maha and antar else [lord10, lord2],
        ),
        _panel(
            id="love",
            title="Marriage, Home & Dosha Notes",
            kicker=love_kicker,
            insights=love_insights,
            timing=[{"label": lab, "range": rng} for lab, rng in love_wins],
            ask_topic="marriage",
            remedies=["Mars", "Venus"] if manglik else ["Venus", lord7],
        ),
        _panel(
            id="life",
            title="Health, Struggle & Upaya",
            kicker=health_kicker,
            insights=health_insights,
            timing=[{"label": lab, "range": rng} for lab, rng in health_wins],
            ask_topic="health",
            remedies=weak[:2],
        ),
    ]
