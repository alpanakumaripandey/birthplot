"""Life Summary: visible life insights from chart + dasha (not a FAQ)."""

from __future__ import annotations

from datetime import datetime
from typing import List, Set, Tuple

from kundli.chart import KundliChart
from kundli.dasha import DashaPeriod, DashaTimeline, _antardashas
from kundli.knowledge_loader import topics

SIGN_CAREER = {
    "Aries": "leadership, sports, engineering starts, defense, entrepreneurship, or roles that need courage",
    "Taurus": "finance, banking, food, design, beauty, real estate, or steady skilled craft",
    "Gemini": "writing, media, sales, teaching, tech support, marketing, or multi-skill roles",
    "Cancer": "care, hospitality, HR, counseling, home/property, education support, or public service",
    "Leo": "creative direction, performance, brand work, politics, teaching with presence, or management",
    "Virgo": "analytics, health services, editing, accounting, quality control, or detailed specialist work",
    "Libra": "law, design, diplomacy, consulting, partnerships, fashion, or client-facing roles",
    "Scorpio": "research, psychology, investigation, surgery-adjacent fields, finance depth, or crisis work",
    "Sagittarius": "teaching, publishing, travel, law, coaching, higher education, or international work",
    "Capricorn": "management, government, engineering, operations, long-term strategy, or corporate structure",
    "Aquarius": "technology, innovation, networks, social impact, aviation/tech products, or unconventional careers",
    "Pisces": "arts, healing, film, spirituality-adjacent work, charity, design, or imaginative service",
}

SIGN_STYLE = {
    "Aries": "direct and ready to begin",
    "Taurus": "steady and loyal once trust is there",
    "Gemini": "curious and needs mental connection",
    "Cancer": "caring, protective, and home-oriented",
    "Leo": "warm-hearted and wanting appreciation",
    "Virgo": "careful, helpful, and detail-minded",
    "Libra": "fair, diplomatic, and partnership-oriented",
    "Scorpio": "deep, private, and intensely loyal",
    "Sagittarius": "honest, open, and big-picture",
    "Capricorn": "serious, responsible, and long-term focused",
    "Aquarius": "independent and needs space inside closeness",
    "Pisces": "gentle, imaginative, and emotionally tuned",
}

PLANET_FEEL = {
    "Sun": "visibility and leadership",
    "Moon": "emotional safety and care",
    "Mars": "drive and decisive action",
    "Mercury": "communication and skill-building",
    "Jupiter": "growth, guidance, and good support",
    "Venus": "harmony, love, and ease with people",
    "Saturn": "patience, duty, and slow solid results",
    "Rahu": "ambition, foreign or unconventional paths",
    "Ketu": "release, focus, and looking inward",
}


def _fmt(p: DashaPeriod) -> str:
    return f"{p.start.strftime('%b %Y')} to {p.end.strftime('%b %Y')}"


def _topic_lords(chart: KundliChart, topic_key: str) -> Set[str]:
    meta = topics()[topic_key]
    return set(meta["planets"]) | {
        name for name, pl in chart.planets.items() if pl.house in meta["houses"]
    }


def _hits(lord: str, relevant: Set[str], topic_key: str) -> bool:
    meta = topics()[topic_key]
    return lord in relevant or lord in meta["planets"]


def _now(timeline: DashaTimeline) -> datetime:
    if timeline.current_antardasha:
        return datetime.now(tz=timeline.current_antardasha.start.tzinfo)
    if timeline.current_mahadasha:
        return datetime.now(tz=timeline.current_mahadasha.start.tzinfo)
    return datetime.now()


def _windows_for(
    chart: KundliChart,
    timeline: DashaTimeline,
    topic_key: str,
    limit: int = 3,
) -> List[Tuple[str, str]]:
    relevant = _topic_lords(chart, topic_key)
    now = _now(timeline)
    out: List[Tuple[str, str]] = []

    if timeline.current_mahadasha and timeline.current_antardasha:
        m, a = timeline.current_mahadasha, timeline.current_antardasha
        if _hits(m.lord, relevant, topic_key) or _hits(a.lord, relevant, topic_key):
            out.append(("Open now", _fmt(a)))

        for antar in timeline.antardashas_in_current:
            if antar.start <= a.start or antar.end <= now:
                continue
            if _hits(antar.lord, relevant, topic_key):
                out.append(("Coming soon", _fmt(antar)))
            if len(out) >= limit:
                return out[:limit]

    if timeline.current_mahadasha and timeline.mahadashas:
        for maha in timeline.mahadashas:
            if maha.start <= timeline.current_mahadasha.start:
                continue
            if _hits(maha.lord, relevant, topic_key):
                out.append(("Longer chapter", _fmt(maha)))
            else:
                for antar in _antardashas(maha)[:4]:
                    if _hits(antar.lord, relevant, topic_key):
                        out.append(("Later window", _fmt(antar)))
                        break
            if len(out) >= limit:
                break

    return out[:limit]


def _timing_line(windows: List[Tuple[str, str]], quiet: str) -> str:
    if not windows:
        return quiet
    bits = [f"{label.lower()} ({rng})" for label, rng in windows]
    if len(bits) == 1:
        return f"A clear timing window shows up {bits[0]}."
    return "Timing windows that stand out: " + "; ".join(bits) + "."


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
    }


def build_life_summary(chart: KundliChart, timeline: DashaTimeline) -> List[dict]:
    """Three insight panels: career/money, love, life path — narrative, not FAQ."""
    h10 = chart.houses[9]
    h7 = chart.houses[6]
    h5 = chart.houses[4]
    h6 = chart.houses[5]
    h11 = chart.houses[10]
    h9 = chart.houses[8]
    h12 = chart.houses[11]
    venus = chart.planets["Venus"]
    jupiter = chart.planets["Jupiter"]
    saturn = chart.planets["Saturn"]
    rahu = chart.planets["Rahu"]
    mars = chart.planets["Mars"]

    career_field = SIGN_CAREER.get(h10.rashi_name, "roles that match your steady strengths")
    partner_style = SIGN_STYLE.get(h7.rashi_name, "selective about closeness")
    lagna_style = SIGN_STYLE.get(chart.lagna.rashi_name, "your own pace")

    career_wins = _windows_for(chart, timeline, "career")
    money_wins = _windows_for(chart, timeline, "money")
    marriage_wins = _windows_for(chart, timeline, "marriage")
    love_wins = _windows_for(chart, timeline, "love")
    foreign_wins = _windows_for(chart, timeline, "foreign")
    health_wins = _windows_for(chart, timeline, "health")
    child_wins = _windows_for(chart, timeline, "children")

    career_planets = set(h10.planets) | set(h6.planets) | set(h11.planets)
    business_lean = bool(career_planets & {"Mars", "Sun", "Rahu", "Mercury"})
    job_lean = bool(career_planets & {"Saturn", "Moon", "Jupiter"}) or not career_planets
    abroad_lean = (
        rahu.house in (9, 12, 7, 3)
        or bool(h12.planets)
        or bool({"Rahu", "Moon", "Venus"} & set(h9.planets))
    )
    romance_lean = venus.house in (5, 7) or "Venus" in h5.planets or "Moon" in h5.planets
    traditional_lean = jupiter.house in (7, 9) or saturn.house in (7, 2) or "Jupiter" in h7.planets
    heavy = False
    if timeline.current_mahadasha and timeline.current_antardasha:
        heavy = timeline.current_mahadasha.lord in {"Saturn", "Rahu", "Ketu"} or (
            timeline.current_antardasha.lord in {"Saturn", "Rahu", "Ketu"}
        )

    # --- Career & Finance panel ---
    if business_lean and not job_lean:
        path_line = (
            "Visible lean: more self-driven paths — business, freelancing, or high-ownership roles — "
            "fit better than a purely quiet desk track."
        )
    elif business_lean and job_lean:
        path_line = (
            "Visible lean: both employment and enterprise can work. A hybrid (stable role + side build) "
            "is often the smartest bridge."
        )
    else:
        path_line = (
            "Visible lean: steady employment and growing inside a system first. "
            "Business can wait until skills, savings, and a clear niche are ready."
        )

    if abroad_lean:
        abroad_line = (
            "Foreign study, remote global work, or living abroad shows up as a realistic theme — "
            + _timing_line(foreign_wins, "keep skills and documents ready for when a clean door opens.")
        )
    else:
        abroad_line = (
            "Abroad is possible but not the loudest theme. Short programs, remote clients, "
            "or a later move may fit better than forcing an immediate relocation."
        )

    career_timing = [{"label": label, "range": rng} for label, rng in (career_wins or money_wins)[:3]]
    career_kicker = (
        f"Work gifts lean toward {career_field.split(',')[0].strip()}"
        + (f" · timing {career_wins[0][1]}" if career_wins else "")
    )

    career_insights = [
        (
            f"What stands out for career: your natural talents point toward {career_field}. "
            f"The tone feels shaped by {h10.rashi_name}"
            + (
                f", with {', '.join(h10.planets)} adding extra color in that space."
                if h10.planets
                else "."
            )
        ),
        (
            "On growth and moves: "
            + _timing_line(
                career_wins,
                "near-term career energy looks steadier than dramatic — prepare quietly, then move when an offer is clear.",
            )
            + " Those windows are useful for promotions, role changes, or a careful job switch."
        ),
        path_line,
        abroad_line,
        (
            "On money: "
            + _timing_line(
                money_wins,
                "this stretch favors budgeting and skill-led income over sudden windfalls.",
            )
            + f" Gains themes sit in {h11.rashi_name}"
            + (
                f" with {', '.join(h11.planets)} — choose income streams that match that tone."
                if h11.planets
                else " — one reliable stream before adding risk."
            )
            + " For stocks or property, treat timing as a weather hint only: slow compounding and savings first, not speculation."
        ),
    ]

    # --- Love & Marriage panel ---
    partner_wins = marriage_wins or love_wins
    if romance_lean and not traditional_lean:
        path_love = (
            "The chart leans toward choice-led / love-led partnership — personal connection matters a lot."
        )
    elif romance_lean and traditional_lean:
        path_love = (
            "Both paths can work: love may start the story, while family blessing or formal steps still matter."
        )
    elif traditional_lean:
        path_love = (
            "There is a lean toward traditional or family-supported paths, though a love match can still work "
            "when values and timing align."
        )
    else:
        path_love = "Either love or arranged routes can work — shared values and timing matter more than the label."

    love_kicker = (
        f"Partnership style: {partner_style}"
        + (f" · window {partner_wins[0][1]}" if partner_wins else "")
    )
    love_insights = [
        (
            f"What stands out in relationships: you tend to show up as {partner_style}. "
            f"Close bonds ask for trust, fairness, and everyday give-and-take"
            + (
                f" — with {', '.join(h7.planets)} active in that space."
                if h7.planets
                else "."
            )
        ),
        (
            "On meeting someone or moving toward commitment: charts show supportive windows, not a fixed wedding date. "
            + _timing_line(
                partner_wins,
                "the next clearer partnership chapter may arrive with a later timing shift — date with intention, not pressure.",
            )
        ),
        path_love,
        (
            f"A repeating pattern often mirrors Venus ({PLANET_FEEL['Venus']}, house {venus.house}) "
            f"and Mars ({PLANET_FEEL['Mars']}, house {mars.house}): wanting closeness while also needing space, "
            f"or swinging between idealizing and testing trust. The pattern softens when needs are named early "
            f"and partners are chosen for actions that match their words."
        ),
        (
            "When conflict loops: one issue at a time, no scorekeeping, and a weekly check-in. "
            f"Plain talk ({PLANET_FEEL['Mercury']}) plus warm repair ({PLANET_FEEL['Venus']}) cools most storms faster than winning the argument."
        ),
    ]
    love_timing = [{"label": label, "range": rng} for label, rng in partner_wins[:3]]

    # --- Life path / health / family ---
    shift_windows: List[Tuple[str, str]] = []
    if timeline.current_antardasha and timeline.antardashas_in_current:
        for a in timeline.antardashas_in_current:
            if a.start > timeline.current_antardasha.start:
                shift_windows.append(("Next shorter chapter", _fmt(a)))
                if len(shift_windows) >= 2:
                    break
    if not shift_windows and timeline.current_mahadasha and timeline.mahadashas:
        for m in timeline.mahadashas:
            if m.start > timeline.current_mahadasha.start:
                shift_windows.append(("Next longer chapter", _fmt(m)))
                break

    life_kicker = (
        f"Life tone: {lagna_style}"
        + (" · a heavier chapter asking for patience" if heavy else " · build and clarify")
    )
    life_insights = [
        (
            f"Soul-path sketch: live more as {chart.lagna.rashi_name} energy ({lagna_style}), "
            f"offer the world your {h10.rashi_name}-toned work gifts, and grow through "
            f"{PLANET_FEEL.get('Ketu', 'inner focus')}. Purpose feels quieter when you serve and keep promises; "
            f"louder when you chase only status."
        ),
        (
            (
                "Why life can feel heavy now: this chapter asks for patience, release, or a rethink of old goals — "
                "not proof that you failed. "
                if heavy
                else "Even in a milder chapter, life feels heavy when rest and meaning run low. "
            )
            + (
                f"Current flavor mixes {PLANET_FEEL.get(timeline.current_mahadasha.lord, 'mixed')} "
                f"with {PLANET_FEEL.get(timeline.current_antardasha.lord, 'mixed')} "
                f"({_fmt(timeline.current_antardasha)}). "
                if timeline.current_mahadasha and timeline.current_antardasha
                else ""
            )
            + _timing_line(
                shift_windows,
                "The tone usually softens as the next shorter chapter begins — protect sleep, support, and one clear goal.",
            )
        ),
        (
            "Health themes to watch (reflective, not medical): "
            f"routine and recovery around {h6.rashi_name}"
            + (
                f" with {', '.join(h6.planets)}"
                if h6.planets
                else ""
            )
            + f". Guard {PLANET_FEEL['Moon']} — mood and rest — and don’t ignore small warning signs. "
            + _timing_line(health_wins, "Keep checkups and gentle movement steady year-round.")
        ),
        (
            "Children / family growth: supportive windows can appear, but conception is never guaranteed by a chart — "
            "pair this with medical guidance. "
            + _timing_line(
                child_wins,
                "Near-term children timing looks quieter; health and partnership readiness come first.",
            )
            + f" Creativity and children themes sit in {h5.rashi_name}"
            + (f" with {', '.join(h5.planets)}." if h5.planets else ".")
        ),
    ]
    life_timing = [
        {"label": label, "range": rng}
        for label, rng in (shift_windows + health_wins + child_wins)[:3]
    ]

    return [
        _panel(
            id="career",
            title="Career & Finance",
            kicker=career_kicker,
            insights=career_insights,
            timing=career_timing,
            ask_topic="career",
        ),
        _panel(
            id="love",
            title="Love & Relationships",
            kicker=love_kicker,
            insights=love_insights,
            timing=love_timing,
            ask_topic="marriage",
        ),
        _panel(
            id="life",
            title="Life Path, Health & Family",
            kicker=life_kicker,
            insights=life_insights,
            timing=life_timing,
            ask_topic="spirituality",
        ),
    ]
