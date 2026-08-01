"""Life Summary: deterministic insights from whole-sign D1 + Vimshottari timing."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Sequence, Set, Tuple

from kundli.chart import HouseInfo, KundliChart
from kundli.dasha import DashaPeriod, DashaTimeline, _antardashas

# Classical sign lords (sidereal / whole-sign)
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

# Primary career fields from 10th-house sign (single primary + secondary)
CAREER_BY_SIGN = {
    "Aries": ("leadership / engineering / defense / startups", "roles that need initiative"),
    "Taurus": ("finance / banking / design / real estate", "steady skilled or luxury-linked work"),
    "Gemini": ("writing / media / sales / teaching / tech communication", "multi-skill information work"),
    "Cancer": ("care / HR / hospitality / counseling / property", "people-and-home linked service"),
    "Leo": ("management / brand / performance / education leadership", "visible authority roles"),
    "Virgo": ("analytics / health services / accounting / quality work", "detail and systems roles"),
    "Libra": ("law / consulting / design / partnerships / diplomacy", "client and balance roles"),
    "Scorpio": ("research / investigation / depth finance / crisis work", "transformative specialist roles"),
    "Sagittarius": ("teaching / publishing / law / coaching / travel", "guidance and higher-learning roles"),
    "Capricorn": ("operations / government / engineering / corporate structure", "long-horizon management"),
    "Aquarius": ("technology / networks / innovation / social systems", "unconventional or tech-forward work"),
    "Pisces": ("arts / healing / film / care / imaginative service", "creative or compassionate work"),
}

PARTNER_BY_SIGN = {
    "Aries": "direct, independent, and quick to decide",
    "Taurus": "loyal, steady, and security-seeking",
    "Gemini": "talkative, curious, and mentally restless",
    "Cancer": "protective, emotional, and home-centered",
    "Leo": "warm, proud, and needing appreciation",
    "Virgo": "careful, helpful, and critical when stressed",
    "Libra": "fair, companion-focused, and harmony-seeking",
    "Scorpio": "intense, private, and deeply loyal",
    "Sagittarius": "honest, expansive, and freedom-loving",
    "Capricorn": "serious, duty-bound, and long-term oriented",
    "Aquarius": "friendly yet independent, needing space",
    "Pisces": "gentle, idealizing, and emotionally porous",
}

HEALTH_BY_SIGN = {
    "Aries": "head, stress from overdrive, inflammation from haste",
    "Taurus": "throat, thyroid, habits around food and rest",
    "Gemini": "nerves, lungs, overthinking fatigue",
    "Cancer": "digestion, chest, mood-linked appetite",
    "Leo": "heart strain from overwork, heat, back tension",
    "Virgo": "gut, assimilation, worry loops",
    "Libra": "kidneys, lower back, balance of work/rest",
    "Scorpio": "reproductive/elimination system, buried stress",
    "Sagittarius": "hips, liver load, overextension",
    "Capricorn": "bones, joints, chronic fatigue from duty",
    "Aquarius": "circulation, ankles, irregular routines",
    "Pisces": "feet, sleep, immune dips from emotional load",
}

CONTENT_VERSION = "deterministic-v1"


def _fmt(p: DashaPeriod) -> str:
    return f"{p.start.strftime('%b %Y')}–{p.end.strftime('%b %Y')}"


def _house(chart: KundliChart, num: int) -> HouseInfo:
    return chart.houses[num - 1]


def _lord_of_house(chart: KundliChart, house_num: int) -> str:
    return SIGN_LORD[_house(chart, house_num).rashi_name]


def _lord_placement(chart: KundliChart, house_num: int) -> Tuple[str, int, str]:
    lord = _lord_of_house(chart, house_num)
    pl = chart.planets[lord]
    return lord, pl.house, pl.info.rashi_name


def _occ_text(h: HouseInfo) -> str:
    if h.planets:
        return ", ".join(h.planets)
    return "empty (sign lord carries the result)"


def _now(timeline: DashaTimeline) -> datetime:
    ref = timeline.current_antardasha or timeline.current_mahadasha
    if ref and ref.start.tzinfo:
        return datetime.now(tz=ref.start.tzinfo)
    return datetime.now()


def _score_period(lord: str, keys: Set[str]) -> int:
    """Higher = more relevant. Exact key match beats nothing."""
    if lord in keys:
        return 2
    return 0


def _windows(
    chart: KundliChart,
    timeline: DashaTimeline,
    keys: Set[str],
    *,
    limit: int = 3,
) -> List[Tuple[str, str, int]]:
    """
    Deterministic timing list: (label, range, score).
    Prefer current/ upcoming antars whose lord is in keys, then mahadashas.
    Sorted by start time within same priority band.
    """
    now = _now(timeline)
    scored: List[Tuple[datetime, str, str, int]] = []

    if timeline.current_mahadasha and timeline.current_antardasha:
        a = timeline.current_antardasha
        s = _score_period(a.lord, keys) + _score_period(timeline.current_mahadasha.lord, keys)
        if s:
            scored.append((a.start, "Current", _fmt(a), s + 10))

        for antar in timeline.antardashas_in_current:
            if antar.start <= a.start or antar.end <= now:
                continue
            s = _score_period(antar.lord, keys)
            if s:
                scored.append((antar.start, "Next", _fmt(antar), s + 5))

    if timeline.current_mahadasha:
        for maha in timeline.mahadashas:
            if maha.start <= timeline.current_mahadasha.start:
                continue
            s = _score_period(maha.lord, keys)
            if s:
                scored.append((maha.start, "Major chapter", _fmt(maha), s))
            # First matching antar inside next maha
            for antar in _antardashas(maha):
                if antar.end <= now:
                    continue
                s2 = _score_period(antar.lord, keys)
                if s2 and not s:
                    scored.append((antar.start, "Later", _fmt(antar), s2))
                    break
            if len([x for x in scored if x[1] == "Major chapter"]) >= 2:
                break

    scored.sort(key=lambda t: (-t[3], t[0]))
    out: List[Tuple[str, str, int]] = []
    seen = set()
    for _, label, rng, sc in scored:
        key = (label, rng)
        if key in seen:
            continue
        seen.add(key)
        out.append((label, rng, sc))
        if len(out) >= limit:
            break
    return out


def _keys_career(chart: KundliChart) -> Set[str]:
    lord10, _, _ = _lord_placement(chart, 10)
    return {"Sun", "Saturn", "Mercury", "Mars", lord10} | set(_house(chart, 10).planets) | set(
        _house(chart, 6).planets
    )


def _keys_money(chart: KundliChart) -> Set[str]:
    lord2, _, _ = _lord_placement(chart, 2)
    lord11, _, _ = _lord_placement(chart, 11)
    return {"Jupiter", "Venus", "Mercury", lord2, lord11} | set(_house(chart, 2).planets) | set(
        _house(chart, 11).planets
    )


def _keys_marriage(chart: KundliChart) -> Set[str]:
    lord7, _, _ = _lord_placement(chart, 7)
    return {"Venus", "Jupiter", "Moon", lord7} | set(_house(chart, 7).planets)


def _keys_foreign(chart: KundliChart) -> Set[str]:
    lord9, _, _ = _lord_placement(chart, 9)
    lord12, _, _ = _lord_placement(chart, 12)
    return {"Rahu", lord9, lord12} | set(_house(chart, 9).planets) | set(_house(chart, 12).planets)


def _keys_health(chart: KundliChart) -> Set[str]:
    lord1, _, _ = _lord_placement(chart, 1)
    lord6, _, _ = _lord_placement(chart, 6)
    return {"Sun", "Moon", "Mars", "Saturn", lord1, lord6} | set(_house(chart, 6).planets)


def _keys_children(chart: KundliChart) -> Set[str]:
    lord5, _, _ = _lord_placement(chart, 5)
    return {"Jupiter", "Moon", lord5} | set(_house(chart, 5).planets)


def _timing_chips(windows: Sequence[Tuple[str, str, int]]) -> List[dict]:
    return [{"label": label, "range": rng} for label, rng, _ in windows]


def _timing_sentence(windows: Sequence[Tuple[str, str, int]], idle: str) -> str:
    if not windows:
        return idle
    parts = [f"{label} ({rng})" for label, rng, _ in windows]
    if len(parts) == 1:
        return f"Primary timing: {parts[0]}."
    return "Primary timing: " + "; ".join(parts) + "."


def _business_score(chart: KundliChart) -> Tuple[int, int]:
    """Return (business_score, job_score) from fixed placements."""
    biz = 0
    job = 0
    for hnum in (10, 6, 11, 3, 7):
        for p in _house(chart, hnum).planets:
            if p in {"Mars", "Sun", "Rahu", "Mercury"}:
                biz += 2
            if p in {"Saturn", "Moon", "Jupiter"}:
                job += 2
    for hnum in (10, 1, 2):
        lord, house, _ = _lord_placement(chart, hnum)
        if lord in {"Mars", "Sun", "Rahu", "Mercury"} and house in (1, 3, 10, 11):
            biz += 1
        if lord in {"Saturn", "Moon", "Jupiter"} and house in (2, 6, 10, 11):
            job += 1
    # Empty 10th still relies on lord
    if not _house(chart, 10).planets:
        lord, house, _ = _lord_placement(chart, 10)
        if lord in {"Saturn", "Jupiter", "Moon"}:
            job += 2
        if lord in {"Mars", "Sun", "Mercury", "Rahu"}:
            biz += 2
        if house in (6, 10, 11):
            job += 1
            biz += 1
    return biz, job


def _abroad_score(chart: KundliChart) -> int:
    score = 0
    rahu = chart.planets["Rahu"]
    if rahu.house in (3, 7, 9, 12):
        score += 3
    if rahu.house in (1, 10, 11):
        score += 1
    for hnum in (9, 12):
        if _house(chart, hnum).planets:
            score += 1
        lord, house, _ = _lord_placement(chart, hnum)
        if house in (3, 7, 9, 12) or lord == "Rahu":
            score += 2
    if "Rahu" in _house(chart, 9).planets or "Rahu" in _house(chart, 12).planets:
        score += 2
    return score


def _romance_scores(chart: KundliChart) -> Tuple[int, int]:
    love = 0
    arranged = 0
    venus = chart.planets["Venus"]
    jupiter = chart.planets["Jupiter"]
    saturn = chart.planets["Saturn"]
    if venus.house in (1, 5, 7, 9, 11):
        love += 2
    if "Venus" in _house(chart, 5).planets or "Moon" in _house(chart, 5).planets:
        love += 2
    if "Mars" in _house(chart, 5).planets:
        love += 1
    if jupiter.house in (7, 2, 9, 11):
        arranged += 2
    if saturn.house in (7, 2, 11):
        arranged += 2
    if "Jupiter" in _house(chart, 7).planets:
        arranged += 2
    if "Saturn" in _house(chart, 7).planets:
        arranged += 1
    lord7, house7, _ = _lord_placement(chart, 7)
    if lord7 == "Venus" or house7 in (5, 7):
        love += 1
    if lord7 in {"Jupiter", "Saturn"} or house7 in (2, 9, 10):
        arranged += 1
    return love, arranged


def _panel(
    *,
    id: str,
    title: str,
    kicker: str,
    insights: List[str],
    timing: List[dict],
    ask_topic: str,
) -> dict:
    return {
        "id": id,
        "title": title,
        "kicker": kicker,
        "insights": insights,
        "timing": timing,
        "ask_topic": ask_topic,
        "version": CONTENT_VERSION,
    }


def build_life_summary(chart: KundliChart, timeline: DashaTimeline) -> List[dict]:
    """Three deterministic insight panels grounded in house/lord/dasha facts."""
    h1 = _house(chart, 1)
    h2 = _house(chart, 2)
    h5 = _house(chart, 5)
    h6 = _house(chart, 6)
    h7 = _house(chart, 7)
    h9 = _house(chart, 9)
    h10 = _house(chart, 10)
    h11 = _house(chart, 11)
    h12 = _house(chart, 12)

    lord10, lord10_house, lord10_sign = _lord_placement(chart, 10)
    lord7, lord7_house, lord7_sign = _lord_placement(chart, 7)
    lord2, lord2_house, lord2_sign = _lord_placement(chart, 2)
    lord11, lord11_house, lord11_sign = _lord_placement(chart, 11)
    lord5, lord5_house, lord5_sign = _lord_placement(chart, 5)
    lord6, lord6_house, lord6_sign = _lord_placement(chart, 6)

    career_primary, career_secondary = CAREER_BY_SIGN[h10.rashi_name]
    partner_style = PARTNER_BY_SIGN[h7.rashi_name]
    health_theme = HEALTH_BY_SIGN[h6.rashi_name]
    lagna_style = PARTNER_BY_SIGN[h1.rashi_name]

    career_wins = _windows(chart, timeline, _keys_career(chart))
    money_wins = _windows(chart, timeline, _keys_money(chart))
    marriage_wins = _windows(chart, timeline, _keys_marriage(chart))
    foreign_wins = _windows(chart, timeline, _keys_foreign(chart))
    health_wins = _windows(chart, timeline, _keys_health(chart))
    child_wins = _windows(chart, timeline, _keys_children(chart))

    biz, job = _business_score(chart)
    if biz > job + 1:
        path_line = (
            f"Work structure score: business/self-led {biz} vs employment {job}. "
            f"Verdict: prefer entrepreneurship, freelancing, or a high-ownership role."
        )
    elif job > biz + 1:
        path_line = (
            f"Work structure score: employment {job} vs business/self-led {biz}. "
            f"Verdict: prefer stable employment and grow inside a system first; business later if skills and capital are ready."
        )
    else:
        path_line = (
            f"Work structure score: employment {job} and business/self-led {biz} are close. "
            f"Verdict: a hybrid path (job + owned project) fits best until one side clearly outperforms."
        )

    abroad = _abroad_score(chart)
    if abroad >= 5:
        abroad_line = (
            f"Foreign score: {abroad}/10 (strong). Study, remote global work, or relocation is a supported theme. "
            + _timing_sentence(foreign_wins, "Keep documents ready; act when a concrete offer appears.")
        )
    elif abroad >= 3:
        abroad_line = (
            f"Foreign score: {abroad}/10 (moderate). Short programs, remote clients, or a later move are more likely than an immediate permanent shift. "
            + _timing_sentence(foreign_wins, "Build skills that travel well.")
        )
    else:
        abroad_line = (
            f"Foreign score: {abroad}/10 (low–mild). Local/remote growth is primary; abroad is optional, not required."
        )

    love_s, arr_s = _romance_scores(chart)
    if love_s > arr_s + 1:
        path_love = (
            f"Partnership path score: love/choice-led {love_s} vs traditional/family-supported {arr_s}. "
            f"Verdict: personal choice and mutual attraction lead; formal steps follow."
        )
    elif arr_s > love_s + 1:
        path_love = (
            f"Partnership path score: traditional/family-supported {arr_s} vs love/choice-led {love_s}. "
            f"Verdict: family-supported or formally introduced paths are stronger; love matches still work if values align."
        )
    else:
        path_love = (
            f"Partnership path score: love/choice-led {love_s} and traditional/family-supported {arr_s} are balanced. "
            f"Verdict: either route works; shared values and timing decide."
        )

    heavy = False
    cur_line = ""
    if timeline.current_mahadasha and timeline.current_antardasha:
        m, a = timeline.current_mahadasha, timeline.current_antardasha
        heavy = m.lord in {"Saturn", "Rahu", "Ketu"} or a.lord in {"Saturn", "Rahu", "Ketu"}
        cur_line = (
            f"Current dasha: {m.lord}–{a.lord} ({_fmt(a)}; mahadasha through {m.end.strftime('%b %Y')})."
        )

    shift_windows: List[Tuple[str, str, int]] = []
    if timeline.current_antardasha and timeline.antardashas_in_current:
        for antar in timeline.antardashas_in_current:
            if antar.start > timeline.current_antardasha.start:
                shift_windows.append(("Next antardasha", _fmt(antar), 1))
                if len(shift_windows) >= 2:
                    break
    if not shift_windows and timeline.current_mahadasha:
        for maha in timeline.mahadashas:
            if maha.start > timeline.current_mahadasha.start:
                shift_windows.append(("Next mahadasha", _fmt(maha), 1))
                break

    venus = chart.planets["Venus"]
    mars = chart.planets["Mars"]
    jupiter = chart.planets["Jupiter"]

    # --- Career panel ---
    career_insights = [
        (
            f"10th house (career) is {h10.rashi_name}; occupants: {_occ_text(h10)}. "
            f"10th lord is {lord10} in house {lord10_house} ({lord10_sign}). "
            f"Primary field fit: {career_primary}. Secondary fit: {career_secondary}."
        ),
        (
            _timing_sentence(
                career_wins,
                "No strong career dasha hit in the near list — prepare quietly; move when a concrete offer appears.",
            )
            + " Use those windows for promotion talks, role change, or a planned job switch."
        ),
        path_line,
        abroad_line,
        (
            f"2nd house (resources) is {h2.rashi_name}; 11th house (gains) is {h11.rashi_name}. "
            f"2nd lord {lord2} sits in house {lord2_house} ({lord2_sign}); "
            f"11th lord {lord11} sits in house {lord11_house} ({lord11_sign}). "
            + _timing_sentence(
                money_wins,
                "Money timing is quiet near-term — favor skill income and budgeting over speculative bets.",
            )
            + " Investing windows are educational timing only, not financial advice."
        ),
    ]
    career_kicker = f"{career_primary}" + (
        f" · {career_wins[0][1]}" if career_wins else f" · 10th lord {lord10} in house {lord10_house}"
    )

    # --- Love panel ---
    love_insights = [
        (
            f"7th house (partnership) is {h7.rashi_name}; occupants: {_occ_text(h7)}. "
            f"7th lord is {lord7} in house {lord7_house} ({lord7_sign}). "
            f"Venus is in house {venus.house} ({venus.info.rashi_name}). "
            f"Relationship style: {partner_style}."
        ),
        (
            _timing_sentence(
                marriage_wins,
                "No strong marriage significator dasha in the near list — focus on readiness and clear standards.",
            )
            + " These are commitment-support windows, not a fixed wedding date."
        ),
        path_love,
        (
            f"Pattern markers: Venus in house {venus.house}, Mars in house {mars.house}. "
            + (
                "Venus/Mars axis across personal houses can repeat push–pull closeness cycles; name needs early and test consistency."
                if {venus.house, mars.house} & {1, 5, 7, 8, 12}
                else "Keep attraction (Venus) and assertion (Mars) in separate conversations so desire does not turn into conflict."
            )
        ),
        (
            "Conflict method that fits this chart: one issue, plain request, repair afterward. "
            f"Mercury skills and Venus repair matter more here than winning the argument."
        ),
    ]
    love_kicker = f"{partner_style}" + (
        f" · {marriage_wins[0][1]}" if marriage_wins else f" · 7th lord {lord7} in house {lord7_house}"
    )

    # --- Life panel ---
    life_insights = [
        (
            f"Lagna is {h1.rashi_name} ({lagna_style}). "
            f"Purpose sketch: live the Lagna tone, deliver 10th-house work ({career_primary}), "
            f"and refine through Ketu’s house {chart.planets['Ketu'].house} "
            f"({chart.planets['Ketu'].info.rashi_name}) — release what is finished, keep what is skill."
        ),
        (
            (cur_line + " " if cur_line else "")
            + (
                "This counts as a heavier chapter (Saturn/Rahu/Ketu active) — expect patience work, pruning, or restructuring rather than easy expansion. "
                if heavy
                else "This is not a classic heavy dasha chapter — heaviness now is more likely lifestyle or unmet needs than a fixed doom cycle. "
            )
            + _timing_sentence(
                shift_windows,
                "Watch the next dasha change for a tone shift.",
            )
        ),
        (
            f"6th house (health/routine) is {h6.rashi_name}; occupants: {_occ_text(h6)}. "
            f"6th lord {lord6} is in house {lord6_house} ({lord6_sign}). "
            f"Watch themes: {health_theme}. "
            + _timing_sentence(health_wins, "Keep baseline checkups and sleep non-negotiable.")
            + " Reflective guidance only — not a medical diagnosis."
        ),
        (
            f"5th house (children/creativity) is {h5.rashi_name}; occupants: {_occ_text(h5)}. "
            f"5th lord {lord5} is in house {lord5_house} ({lord5_sign}). "
            f"Jupiter is in house {jupiter.house} ({jupiter.info.rashi_name}). "
            + _timing_sentence(
                child_wins,
                "Children timing is quiet near-term — prioritize health and relationship readiness.",
            )
            + " Supportive windows only; combine with medical guidance for conception."
        ),
    ]
    life_kicker = (
        f"Lagna {h1.rashi_name}"
        + (" · heavy chapter" if heavy else " · building chapter")
        + (f" · {shift_windows[0][1]}" if shift_windows else "")
    )

    return [
        _panel(
            id="career",
            title="Career & Finance",
            kicker=career_kicker,
            insights=career_insights,
            timing=_timing_chips(career_wins or money_wins),
            ask_topic="career",
        ),
        _panel(
            id="love",
            title="Love & Relationships",
            kicker=love_kicker,
            insights=love_insights,
            timing=_timing_chips(marriage_wins),
            ask_topic="marriage",
        ),
        _panel(
            id="life",
            title="Life Path, Health & Family",
            kicker=life_kicker,
            insights=life_insights,
            timing=_timing_chips(shift_windows[:1] + health_wins[:1] + child_wins[:1]),
            ask_topic="spirituality",
        ),
    ]
