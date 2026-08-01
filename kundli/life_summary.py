"""Life Summary: plain-language answers to common life questions from chart + dasha."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Set, Tuple

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

PLANET_FEEL = {
    "Sun": "visibility and leadership",
    "Moon": "emotional safety and care",
    "Mars": "drive and decisive action",
    "Mercury": "communication and skill-building",
    "Jupiter": "growth, guidance, and good support",
    "Venus": "harmony, love, and ease with people",
    "Saturn": "patience, duty, and slow solid results",
    "Rahu": "ambition, foreign/new paths, and bigger appetite for change",
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
    """Return [(label, range_text), ...] favorable-ish windows for a topic."""
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
            # Peek antars in next maha for nearer windows
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


def _window_sentence(windows: List[Tuple[str, str]], soft: str) -> str:
    if not windows:
        return soft
    bits = [f"{label.lower()} ({rng})" for label, rng in windows]
    if len(bits) == 1:
        return f"A useful timing window is {bits[0]}."
    return "Useful timing windows: " + "; ".join(bits) + "."


def _item(
    *,
    id: str,
    category: str,
    category_label: str,
    question: str,
    answer: str,
    ask_topic: str,
    timing_hint: str = "",
) -> dict:
    return {
        "id": id,
        "category": category,
        "category_label": category_label,
        "question": question,
        "answer": answer,
        "ask_topic": ask_topic,
        "timing_hint": timing_hint,
    }


def build_life_summary(chart: KundliChart, timeline: DashaTimeline) -> List[dict]:
    """FAQ-style summary answers for the Report Summary page."""
    h10 = chart.houses[9]
    h7 = chart.houses[6]
    h5 = chart.houses[4]
    h6 = chart.houses[5]
    h11 = chart.houses[10]
    h12 = chart.houses[11]
    h9 = chart.houses[8]
    venus = chart.planets["Venus"]
    jupiter = chart.planets["Jupiter"]
    saturn = chart.planets["Saturn"]
    rahu = chart.planets["Rahu"]
    sun = chart.planets["Sun"]
    mercury = chart.planets["Mercury"]
    mars = chart.planets["Mars"]

    career_field = SIGN_CAREER.get(h10.rashi_name, "roles that match your steady strengths")
    career_wins = _windows_for(chart, timeline, "career")
    money_wins = _windows_for(chart, timeline, "money")
    marriage_wins = _windows_for(chart, timeline, "marriage")
    love_wins = _windows_for(chart, timeline, "love")
    foreign_wins = _windows_for(chart, timeline, "foreign")
    health_wins = _windows_for(chart, timeline, "health")
    child_wins = _windows_for(chart, timeline, "children")
    spirit_wins = _windows_for(chart, timeline, "spirituality")

    career_hint = career_wins[0][1] if career_wins else ""
    marriage_hint = marriage_wins[0][1] if marriage_wins else ""
    money_hint = money_wins[0][1] if money_wins else ""

    # Business vs job: Mars/Sun/Saturn/Rahu in career houses lean entrepreneurial vs stable
    career_planets = set(h10.planets) | set(h6.planets) | set(h11.planets)
    business_lean = bool(career_planets & {"Mars", "Sun", "Rahu", "Mercury"})
    job_lean = bool(career_planets & {"Saturn", "Moon", "Jupiter"}) or not career_planets

    # Love vs arranged lean: Venus/5th freer romance; Jupiter/Saturn/7th more traditional framing
    romance_lean = venus.house in (5, 7) or "Venus" in h5.planets or "Moon" in h5.planets
    traditional_lean = jupiter.house in (7, 9) or saturn.house in (7, 2) or "Jupiter" in h7.planets

    # Abroad lean
    abroad_lean = (
        rahu.house in (9, 12, 7, 3)
        or bool(h12.planets)
        or bool({"Rahu", "Moon", "Venus"} & set(h9.planets))
    )

    # Heavy cycle: Saturn/Rahu current
    heavy = False
    if timeline.current_mahadasha and timeline.current_antardasha:
        heavy = timeline.current_mahadasha.lord in {"Saturn", "Rahu", "Ketu"} or (
            timeline.current_antardasha.lord in {"Saturn", "Rahu", "Ketu"}
        )

    items: List[dict] = []

    # --- Career & Finance ---
    items.append(
        _item(
            id="career-field",
            category="career",
            category_label="Career & Finance",
            question="What career field best aligns with my natural talents?",
            answer=(
                f"Your work style points toward {career_field}. "
                f"The tone of your career house feels shaped by {h10.rashi_name}"
                + (
                    f", with {', '.join(h10.planets)} adding extra color."
                    if h10.planets
                    else ", with quieter support from the sign itself."
                )
                + f" Roles that use {PLANET_FEEL.get(sun.name, 'confidence')} and "
                f"{PLANET_FEEL.get(mercury.name, 'clear thinking')} tend to fit you better than forced paths."
            ),
            ask_topic="career",
        )
    )
    items.append(
        _item(
            id="career-promotion",
            category="career",
            category_label="Career & Finance",
            question="When is a favorable time to switch jobs or ask for a promotion?",
            answer=(
                "Jyotish cannot promise a promotion date — it shows when career momentum is more supportive. "
                + _window_sentence(
                    career_wins,
                    "Near-term career timing looks steadier than dramatic; prepare quietly and move when a clear offer appears.",
                )
                + " Before asking, line up proof of your impact and one clear ask."
            ),
            ask_topic="career",
            timing_hint=career_hint,
        )
    )
    items.append(
        _item(
            id="career-business",
            category="career",
            category_label="Career & Finance",
            question="Should I start my own business or stick to employment?",
            answer=(
                (
                    "Your chart leans a bit more toward initiative and self-driven paths — business, freelancing, "
                    "or a high-ownership role inside a company can fit, especially if you like building something."
                    if business_lean and not job_lean
                    else (
                        "Your chart supports both, with a slight lean toward entrepreneurial or high-agency roles. "
                        "A hybrid (job + side project) can be a wise bridge."
                        if business_lean and job_lean
                        else "Your chart leans toward steady employment, structure, and growing inside a system first. "
                        "Business can still work later once skills, savings, and a niche are solid."
                    )
                )
                + " Decide with cash runway and one customer need — not only excitement."
            ),
            ask_topic="career",
        )
    )
    items.append(
        _item(
            id="career-abroad",
            category="career",
            category_label="Career & Finance",
            question="Do I have strong alignments for studying or working abroad?",
            answer=(
                (
                    "Yes — foreign study, remote global work, or living abroad shows up as a realistic theme in your chart. "
                    if abroad_lean
                    else "Abroad is possible, but your chart does not shout it as the main path. Short programs, remote clients, "
                    "or later relocation may fit better than forcing an immediate move. "
                )
                + _window_sentence(
                    foreign_wins,
                    "Keep documents and skills ready so you can move when a clean opportunity appears.",
                )
            ),
            ask_topic="foreign",
            timing_hint=foreign_wins[0][1] if foreign_wins else "",
        )
    )
    items.append(
        _item(
            id="money-struggle",
            category="career",
            category_label="Career & Finance",
            question="When will my current financial struggles ease?",
            answer=(
                "Money chapters ease in waves, not overnight. "
                + _window_sentence(
                    money_wins,
                    "The near term looks better for budgeting and skill-building than sudden windfalls.",
                )
                + f" Your gains house sits in {h11.rashi_name}"
                + (
                    f" with {', '.join(h11.planets)} — focus on income streams that match that tone."
                    if h11.planets
                    else " — focus on one reliable income stream before adding risk."
                )
            ),
            ask_topic="money",
            timing_hint=money_hint,
        )
    )
    items.append(
        _item(
            id="money-invest",
            category="career",
            category_label="Career & Finance",
            question="What are better periods for me to invest in stocks or real estate?",
            answer=(
                "This is educational timing color, not financial advice. "
                + _window_sentence(
                    money_wins,
                    "Prefer long-term SIPs and learning over timing the market right now.",
                )
                + (
                    f" Saturn’s patience theme ({PLANET_FEEL['Saturn']}) suggests slow compounding beats speculation."
                    if saturn.house in (2, 8, 11, 10)
                    else " Keep emergency savings first; invest only money you can leave untouched for years."
                )
            ),
            ask_topic="money",
            timing_hint=money_hint,
        )
    )

    # --- Love & Marriage ---
    items.append(
        _item(
            id="marriage-when",
            category="love",
            category_label="Love & Marriage",
            question="When might I meet a life partner or move toward marriage?",
            answer=(
                "Charts show favorable windows for commitment — not a guaranteed wedding date. "
                + _window_sentence(
                    marriage_wins or love_wins,
                    "The next clearer partnership chapter may arrive with a later timing shift; keep dating intentional, not desperate.",
                )
                + f" Your partnership style feels shaped by {h7.rashi_name}"
                + (
                    f", with {', '.join(h7.planets)} active in that space."
                    if h7.planets
                    else "."
                )
            ),
            ask_topic="marriage",
            timing_hint=marriage_hint or (love_wins[0][1] if love_wins else ""),
        )
    )
    items.append(
        _item(
            id="marriage-compat",
            category="love",
            category_label="Love & Marriage",
            question="Am I structurally compatible with a serious partner?",
            answer=(
                f"You tend to need a partner who respects that you are "
                f"{'warm and relationship-oriented' if venus.house in (1, 4, 5, 7, 10) else 'selective about closeness'}"
                f", with emotional safety around {PLANET_FEEL['Moon']}. "
                f"Compatibility grows when both people share fairness, humor, and clear talk — "
                f"your chart rewards honesty more than perfect matching on paper. "
                f"For a named partner, cast both charts together in a full matching session; "
                f"this summary speaks to your side of the bond."
            ),
            ask_topic="marriage",
        )
    )
    items.append(
        _item(
            id="marriage-path",
            category="love",
            category_label="Love & Marriage",
            question="Does my chart lean toward love marriage or arranged marriage?",
            answer=(
                (
                    "Your chart leans more toward love / choice-led partnership — attraction and personal connection matter a lot."
                    if romance_lean and not traditional_lean
                    else (
                        "Your chart can support either path. Love may start the story; family blessing or formal steps may still matter."
                        if romance_lean and traditional_lean
                        else (
                            "Your chart leans a bit more toward traditional or family-supported paths, "
                            "though a love match can still work if values and timing align."
                            if traditional_lean
                            else "Either path can work — what matters more is shared values and timing, not the label."
                        )
                    )
                )
                + " Choose the route that keeps dignity for everyone involved."
            ),
            ask_topic="marriage",
        )
    )
    items.append(
        _item(
            id="marriage-pattern",
            category="love",
            category_label="Love & Marriage",
            question="Why might my relationships repeat the same pattern?",
            answer=(
                f"Repeating patterns often mirror what you seek and what you fear. "
                f"With Venus emphasizing {PLANET_FEEL['Venus']} from house {venus.house}, "
                f"and Mars showing {PLANET_FEEL['Mars']} from house {mars.house}, "
                f"you may swing between wanting closeness and needing space — or between idealizing and testing trust. "
                f"The pattern softens when you name your need early, slow the rush, and pick partners whose actions match their words."
            ),
            ask_topic="love",
        )
    )
    items.append(
        _item(
            id="marriage-conflict",
            category="love",
            category_label="Love & Marriage",
            question="How can I ease ongoing conflicts in my marriage or partnership?",
            answer=(
                "Conflict cools with structure: one issue at a time, no scorekeeping, and a weekly check-in. "
                f"Your chart responds well to {PLANET_FEEL['Mercury']} — say the need plainly — "
                f"and {PLANET_FEEL['Venus']} — repair with warmth after hard talks. "
                "If fights loop on the same wound, pause the topic for 24 hours, then return with one request each. "
                "For deep stuck conflict, a counselor plus kind timing beats winning the argument."
            ),
            ask_topic="marriage",
        )
    )

    # --- Life path, health, family ---
    items.append(
        _item(
            id="life-purpose",
            category="life",
            category_label="Life Path, Health & Family",
            question="What is my true soul purpose or karmic path in this lifetime?",
            answer=(
                f"A simple reading of purpose: grow through {PLANET_FEEL.get(chart.planets['Ketu'].name, 'inner focus')} "
                f"while offering the world your {h10.rashi_name}-toned work gifts ({career_field}). "
                f"Your rising sign {chart.lagna.rashi_name} asks you to live more as that energy — "
                f"not as someone else’s script. Purpose feels quieter when you serve, learn, and keep promises; "
                f"it feels louder when you chase only status."
            ),
            ask_topic="spirituality",
            timing_hint=spirit_wins[0][1] if spirit_wins else "",
        )
    )
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

    items.append(
        _item(
            id="life-heavy",
            category="life",
            category_label="Life Path, Health & Family",
            question="Why does life feel heavy right now, and when might this cycle shift?",
            answer=(
                (
                    "This chapter can feel heavier because timing is asking for patience, release, or a rethink of old goals — "
                    "not because you failed. "
                    if heavy
                    else "Even outside a classic ‘heavy’ chapter, stress piles up when rest and meaning run low. "
                )
                + (
                    f"Current chapter flavor: {PLANET_FEEL.get(timeline.current_mahadasha.lord, 'mixed')} "
                    f"with {PLANET_FEEL.get(timeline.current_antardasha.lord, 'mixed')} in the shorter window "
                    f"({_fmt(timeline.current_antardasha)}). "
                    if timeline.current_mahadasha and timeline.current_antardasha
                    else ""
                )
                + _window_sentence(
                    shift_windows,
                    "The tone usually softens as the next shorter chapter begins — keep basics (sleep, support, one goal).",
                )
            ),
            ask_topic="spirituality",
        )
    )
    items.append(
        _item(
            id="health-watch",
            category="life",
            category_label="Life Path, Health & Family",
            question="What health themes should I watch out for?",
            answer=(
                "This is reflective guidance, not a diagnosis. "
                f"Your vitality house themes sit around {h6.rashi_name}"
                + (
                    f" with {', '.join(h6.planets)} — so stress, routine, and recovery deserve attention."
                    if h6.planets
                    else " — so daily routine, digestion/stress balance, and sleep deserve attention."
                )
                + f" Protect {PLANET_FEEL['Moon']} (rest and mood) and avoid ignoring small warning signs. "
                + _window_sentence(
                    health_wins,
                    "Keep checkups and gentle exercise steady year-round.",
                )
            ),
            ask_topic="health",
            timing_hint=health_wins[0][1] if health_wins else "",
        )
    )
    items.append(
        _item(
            id="children-when",
            category="life",
            category_label="Life Path, Health & Family",
            question="When might conception or children themes become more supported?",
            answer=(
                "Charts can suggest supportive windows for children themes — they cannot promise conception. "
                "Please combine this with medical guidance. "
                + _window_sentence(
                    child_wins,
                    "Near-term children timing looks quieter; focus on health and partnership readiness first.",
                )
                + f" Your creativity/children house sits in {h5.rashi_name}"
                + (
                    f" with {', '.join(h5.planets)}."
                    if h5.planets
                    else "."
                )
                + f" Jupiter’s growth theme from house {jupiter.house} also colors this story."
            ),
            ask_topic="children",
            timing_hint=child_wins[0][1] if child_wins else "",
        )
    )

    return items
