"""Topic Q&A: plain-language, explanatory answers (minimal jargon)."""

from __future__ import annotations

import re
from datetime import datetime
from typing import List, Optional, Set, Tuple

from kundli.chart import KundliChart
from kundli.dasha import DashaPeriod, DashaTimeline
from kundli.knowledge_loader import topics


# Extra aliases → topic keys
ALIASES = {
    "job": "career",
    "work": "career",
    "profession": "career",
    "business": "career",
    "spouse": "marriage",
    "wedding": "marriage",
    "married": "marriage",
    "marry": "marriage",
    "partner": "marriage",
    "relationship": "marriage",
    "romance": "love",
    "dating": "love",
    "wealth": "money",
    "finance": "money",
    "income": "money",
    "rich": "money",
    "study": "education",
    "college": "education",
    "learning": "education",
    "kids": "children",
    "child": "children",
    "baby": "children",
    "family": "home",
    "property": "home",
    "house": "home",
    "spiritual": "spirituality",
    "meditation": "spirituality",
    "moksha": "spirituality",
    "abroad": "foreign",
    "travel": "foreign",
    "visa": "foreign",
    "dad": "father",
    "mom": "mother",
    "illness": "health",
    "disease": "health",
    "body": "health",
}

# Bump when copy shape changes — UI refreshes stale saved readings
CONTENT_VERSION = "friendly-v2"

PLANET_PLAIN = {
    "Sun": "confidence and being seen",
    "Moon": "feelings, comfort, and emotional safety",
    "Mars": "drive and taking action",
    "Mercury": "talking things through and clear thinking",
    "Jupiter": "growth, support, and good guidance",
    "Venus": "warmth, affection, and ease with people",
    "Saturn": "patience, commitment, and slow steady effort",
    "Rahu": "wanting more and trying a new path",
    "Ketu": "releasing old patterns and looking inward",
}

SIGN_PLAIN = {
    "Aries": "direct and ready to begin",
    "Taurus": "steady and loyal once trust is there",
    "Gemini": "curious, talkative, and needs mental connection",
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

# Rich user-facing copy per topic
TOPIC_PLAIN = {
    "career": {
        "short": "work and career",
        "title_hint": "Your work life",
        "about": (
            "This is about how you show up at work: the kind of roles that suit you, "
            "how you earn respect, and what helps your effort turn into progress."
        ),
        "style_lead": "In work, you naturally come across as",
        "active": (
            "This period can feel more active for career. You may notice stronger push around "
            "job choices, visibility, responsibility, or deciding what you want next. "
            "It is a useful time to update your goals, speak up about your work, and say yes "
            "to opportunities that match where you want to grow."
        ),
        "quiet": (
            "This period looks steadier for career — less sudden drama, more quiet building. "
            "Focus on skills, finishing projects, and small consistent steps. Big leaps can wait; "
            "solid foundations now make the next chapter easier."
        ),
        "do_now": (
            "Practical tip: write down one work win you want in the next 6–12 months, "
            "and one habit that supports it each week."
        ),
        "future_active": (
            "Career energy may rise again — new roles, recognition, interviews, "
            "or a clearer sense of direction."
        ),
        "future_quiet": (
            "Career may stay in a build-quietly mode. Keep learning and networking gently."
        ),
        "wrap": (
            "Think of this as a weather report for work: useful for planning, "
            "not a fixed script. Your effort still shapes the outcome."
        ),
    },
    "education": {
        "short": "learning and studies",
        "title_hint": "Your learning path",
        "about": (
            "This is about how you learn best — focus, curiosity, teachers, exams, "
            "courses, and the subjects that keep your mind awake."
        ),
        "style_lead": "As a learner, you naturally come across as",
        "active": (
            "Learning can feel more alive now. You may feel drawn to a course, exam prep, "
            "writing, research, or picking up a skill that stretches you. Momentum comes more "
            "easily when you study in short focused blocks instead of waiting for a perfect mood."
        ),
        "quiet": (
            "Study energy is quieter right now. That does not mean stop — it means go gentle. "
            "Review what you already know, keep a light routine, and avoid stacking pressure. "
            "Small daily practice beats rare marathon sessions."
        ),
        "do_now": (
            "Practical tip: choose one topic to improve this month and give it 25 focused minutes "
            "most days."
        ),
        "future_active": (
            "A clearer window for courses, exams, certifications, or serious study may open."
        ),
        "future_quiet": (
            "Learning may stay in the background for a while — stay curious without forcing intensity."
        ),
        "wrap": (
            "Use these notes to plan your study rhythm. Consistency matters more than pressure."
        ),
    },
    "marriage": {
        "short": "relationships and partnership",
        "title_hint": "Your relationship life",
        "about": (
            "This is about close one-to-one bonds: marriage, committed partnership, "
            "and how you share life with someone else — trust, fairness, affection, "
            "and the everyday give-and-take of being a team."
        ),
        "style_lead": "In close relationships, you naturally come across as",
        "active": (
            "Relationship topics can feel louder in this chapter. You may notice more "
            "conversations about the future, stronger feelings about closeness, or a clearer "
            "sense of what you need from a partner. If you are single, you might meet people "
            "who matter more, or finally feel ready to date with intention. If you are already "
            "with someone, honesty and shared decisions may come to the front."
        ),
        "quiet": (
            "Relationship energy looks softer right now — less pressure for big announcements, "
            "more room for small kindness. This is a good stretch for listening, repairing small "
            "hurts, and building trust without forcing a milestone. Quiet seasons still shape "
            "lasting bonds."
        ),
        "do_now": (
            "Practical tip: have one honest conversation this week about what makes you feel "
            "safe and appreciated — or journal it first if you are not ready to say it aloud."
        ),
        "future_active": (
            "Connection themes may heat up — dating with more seriousness, commitment talks, "
            "family discussions, or healing an important bond."
        ),
        "future_quiet": (
            "Partnership may stay gentler ahead. Keep communication simple, kind, and regular."
        ),
        "wrap": (
            "A good relationship grows from how you show up day by day. Use timing as support, "
            "not as pressure to rush or wait forever."
        ),
    },
    "love": {
        "short": "love and romance",
        "title_hint": "Your romantic life",
        "about": (
            "This is about attraction, warmth, playfulness, and emotional chemistry — "
            "the spark side of love, whether you are dating or deepening an existing bond."
        ),
        "style_lead": "In romance, you naturally come across as",
        "active": (
            "Romance can feel more noticeable now — flirtation, dating energy, or a spark "
            "returning in a current relationship. Follow what feels genuine; skip pressure to perform."
        ),
        "quiet": (
            "Romance is softer now. Friendship, comfort, and emotional safety matter more "
            "than grand gestures. That quieter care can still deepen love."
        ),
        "do_now": "Practical tip: do one small warm gesture this week with no agenda attached.",
        "future_active": "A warmer romantic chapter may open — more meetings, more chemistry, more heart.",
        "future_quiet": "Love themes stay low-key ahead. Keep your heart open without rushing.",
        "wrap": "Romance works best when it feels natural. Let timing help; do not let it hurry you.",
    },
    "money": {
        "short": "money",
        "title_hint": "Your money life",
        "about": "This is about income, spending habits, savings, and how money supports your real life.",
        "style_lead": "With money, you naturally tend to be",
        "active": (
            "Money may ask for more attention now — income shifts, spending choices, "
            "or a chance to grow resources. Review numbers calmly before big commitments."
        ),
        "quiet": (
            "Finances look steadier. Stick to simple plans and avoid all-or-nothing bets. "
            "Quiet money seasons are good for cleaning up habits."
        ),
        "do_now": "Practical tip: track spending for two weeks and name one money goal for this year.",
        "future_active": "A clearer window for income changes or money decisions may arrive.",
        "future_quiet": "Money stays in a build-slowly mode ahead.",
        "wrap": "Steady habits beat dramatic swings. Plan first, then act.",
    },
    "health": {
        "short": "health and energy",
        "title_hint": "Your energy and wellbeing",
        "about": "This is about daily vitality — sleep, stress, routine, and how you care for your body.",
        "style_lead": "With energy and health, you naturally lean",
        "active": (
            "Wellbeing may need more care now. Sleep, stress, food, and movement matter more. "
            "Treat small warning signs early rather than pushing through."
        ),
        "quiet": (
            "Energy looks steadier. Keep simple routines and protect rest. "
            "Prevention now saves drama later."
        ),
        "do_now": "Practical tip: protect one non-negotiable rest or movement habit this week.",
        "future_active": "A stretch focused on recovery and body-care may come.",
        "future_quiet": "Energy looks more even ahead if basics stay steady.",
        "wrap": "Your body keeps the score. Small daily care is the real long game.",
    },
}


def detect_topic(question: str) -> Optional[str]:
    q = question.lower().strip()
    if not q:
        return None
    topic_keys = list(topics().keys())
    for key in topic_keys:
        if re.search(rf"\b{re.escape(key)}\b", q):
            return key
    for alias, key in ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", q):
            return key
    for key, meta in topics().items():
        label_words = re.findall(r"[a-z]+", meta["label"].lower())
        if any(w in q for w in label_words if len(w) > 3):
            return key
    return None


def list_topics_help() -> str:
    keys = sorted(topics().keys())
    return "Try topics: " + ", ".join(keys) + " (or words like job, spouse, abroad)."


def _fmt_range(p: DashaPeriod) -> str:
    return f"{p.start.strftime('%b %Y')} to {p.end.strftime('%b %Y')}"


def _topic_lords(chart: KundliChart, meta: dict) -> Set[str]:
    return set(meta["planets"]) | {
        name for name, pl in chart.planets.items() if pl.house in meta["houses"]
    }


def _lord_hits_topic(lord: str, relevant: Set[str], meta: dict) -> bool:
    return lord in relevant or lord in meta["planets"]


def _plain(topic_key: str) -> dict:
    if topic_key in TOPIC_PLAIN:
        return TOPIC_PLAIN[topic_key]
    meta = topics()[topic_key]
    short = meta["label"].split("&")[0].strip().lower()
    return {
        "short": short,
        "title_hint": f"Your {short}",
        "about": f"This is a simple read on {short} in your life.",
        "style_lead": "In this part of life, you naturally come across as",
        "active": f"This part of life may feel more noticeable right now. Pay attention to what keeps coming up.",
        "quiet": f"This part of life looks steadier right now. Small steps beat big leaps.",
        "do_now": "Practical tip: name one small action you can take this week.",
        "future_active": f"A clearer chapter for {short} may open ahead.",
        "future_quiet": f"{short.capitalize()} may stay quieter ahead — keep going gently.",
        "wrap": "Use this as guidance for reflection, not a fixed fate.",
    }


def _style_paragraph(chart: KundliChart, meta: dict, plain: dict) -> str:
    primary = meta["houses"][0]
    h = chart.houses[primary - 1]
    sign_bit = SIGN_PLAIN.get(h.rashi_name, "unique in its own way")
    lead = plain["style_lead"]
    if h.planets:
        flavors = [PLANET_PLAIN.get(p, p.lower()) for p in h.planets[:2]]
        if len(flavors) == 1:
            extra = f" You also carry a strong pull toward {flavors[0]}."
        else:
            extra = f" You also carry a strong pull toward {flavors[0]}, mixed with {flavors[1]}."
        return f"{lead} {sign_bit}.{extra}"
    return (
        f"{lead} {sign_bit}. Even when this area looks quiet from the outside, "
        f"that tone still shapes how you connect and choose."
    )


def _a(phrase: str) -> str:
    """Choose a/an for a phrase starting with a vowel sound (simple heuristic)."""
    first = phrase.lstrip().lower()
    return "an" if first[:1] in "aeiou" else "a"


def _support_paragraph(chart: KundliChart, meta: dict) -> str:
    bits: List[str] = []
    for pname in meta["planets"][:3]:
        pl = chart.planets[pname]
        flavor = PLANET_PLAIN.get(pname, pname.lower())
        sign_bit = SIGN_PLAIN.get(pl.info.rashi_name, "mixed")
        bits.append(f"{flavor} — {_a(sign_bit)} {sign_bit} tone")
    if not bits:
        return ""
    if len(bits) == 1:
        return f"A big support theme for you is {bits[0]}."
    if len(bits) == 2:
        return f"Two big support themes for you are {bits[0]}; and {bits[1]}."
    return (
        f"Three themes that keep showing up for you:\n"
        f"• {bits[0]}\n"
        f"• {bits[1]}\n"
        f"• {bits[2]}\n"
        f"Together they color how this area of life feels day to day."
    )


def _present_lines(
    chart: KundliChart,
    timeline: DashaTimeline,
    topic_key: str,
    meta: dict,
    relevant: Set[str],
) -> List[str]:
    plain = _plain(topic_key)
    lines: List[str] = [
        "## Right now",
        "",
        plain["about"],
        "",
        _style_paragraph(chart, meta, plain),
        "",
        _support_paragraph(chart, meta),
        "",
    ]

    if timeline.current_mahadasha and timeline.current_antardasha:
        m = timeline.current_mahadasha
        a = timeline.current_antardasha
        hits = [x for x in (m.lord, a.lord) if _lord_hits_topic(x, relevant, meta)]
        lines.append(
            f"Where you are in time: from {_fmt_range(a)}, inside a longer life chapter "
            f"that runs through {m.end.strftime('%b %Y')}."
        )
        lines.append("")
        if hits:
            why = " and ".join(PLANET_PLAIN.get(h, h.lower()) for h in hits)
            lines.append(plain["active"])
            lines.append("")
            lines.append(
                f"Why this may feel stronger now: this chapter puts more attention on {why}. "
                f"That does not force an outcome — it simply turns the volume up on these themes."
            )
        else:
            lines.append(plain["quiet"])
        lines.append("")
        lines.append(plain["do_now"])
    else:
        lines.append(
            "Timing gets clearer with an exact birth time. Even so, your natural style above still applies."
        )
        lines.append("")
        lines.append(plain["do_now"])
    return lines


def _ahead_lines(
    timeline: DashaTimeline,
    topic_key: str,
    meta: dict,
    relevant: Set[str],
    as_of: Optional[datetime] = None,
) -> List[str]:
    plain = _plain(topic_key)
    lines: List[str] = ["", "## Coming up", ""]
    now = as_of or datetime.now()
    if timeline.current_antardasha and timeline.current_antardasha.start.tzinfo:
        now = now.replace(tzinfo=timeline.current_antardasha.start.tzinfo)
    elif timeline.current_mahadasha and timeline.current_mahadasha.start.tzinfo:
        now = now.replace(tzinfo=timeline.current_mahadasha.start.tzinfo)

    upcoming: List[str] = []

    if timeline.current_antardasha and timeline.antardashas_in_current:
        for antar in timeline.antardashas_in_current:
            if antar.start <= timeline.current_antardasha.start:
                continue
            if antar.end <= now:
                continue
            if _lord_hits_topic(antar.lord, relevant, meta):
                flavor = PLANET_PLAIN.get(antar.lord, antar.lord.lower())
                upcoming.append(
                    f"Around {_fmt_range(antar)}, themes of {flavor} may rise. "
                    f"{plain['future_active']}"
                )
            if len(upcoming) >= 2:
                break

    if timeline.current_mahadasha and timeline.mahadashas:
        for maha in timeline.mahadashas:
            if maha.start <= timeline.current_mahadasha.start:
                continue
            flavor = PLANET_PLAIN.get(maha.lord, maha.lord.lower())
            start = maha.start.strftime("%b %Y")
            end = maha.end.strftime("%b %Y")
            if _lord_hits_topic(maha.lord, relevant, meta):
                upcoming.append(
                    f"From {start} to {end}, a longer chapter begins that leans on {flavor}. "
                    f"{plain['future_active']}"
                )
            else:
                upcoming.append(
                    f"From {start} to {end}, a longer chapter begins with more emphasis on {flavor}. "
                    f"{plain['future_quiet']}"
                )
            break

    if upcoming:
        lines.append("Here is what the next chapters may feel like:")
        lines.append("")
        lines.extend(f"• {u}" for u in upcoming[:3])
    else:
        lines.append(plain["future_quiet"])
    return lines


def _simple_wrap(chart: KundliChart, topic_key: str, meta: dict) -> List[str]:
    plain = _plain(topic_key)
    primary = meta["houses"][0]
    h = chart.houses[primary - 1]
    sign_bit = SIGN_PLAIN.get(h.rashi_name, "your own")
    return [
        "",
        "## What this means for you",
        "",
        f"{plain['title_hint']}: your baseline style is {sign_bit}.",
        "",
        plain["wrap"],
        "",
        "These are tendencies and timing colors, not fixed fate. Your choices still matter.",
    ]


def answer_topic(
    chart: KundliChart,
    timeline: DashaTimeline,
    topic_key: str,
) -> str:
    meta = topics()[topic_key]
    relevant = _topic_lords(chart, meta)

    lines: List[str] = [
        f"# {meta['label']}",
        f"(reading {CONTENT_VERSION})",
        "",
        *_present_lines(chart, timeline, topic_key, meta, relevant),
        *_ahead_lines(timeline, topic_key, meta, relevant),
        *_simple_wrap(chart, topic_key, meta),
    ]
    return "\n".join(lines)


def answer_question(
    chart: KundliChart,
    timeline: DashaTimeline,
    question: str,
) -> Tuple[str, Optional[str]]:
    """Return (answer_text, topic_key_or_none)."""
    key = detect_topic(question)
    if not key:
        return (
            "I could not map that to a topic yet.\n" + list_topics_help(),
            None,
        )
    return answer_topic(chart, timeline, key), key
