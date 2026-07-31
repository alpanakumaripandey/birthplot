"""Topic Q&A: map user questions to houses/planets and answer in plain language."""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from kundli.chart import KundliChart
from kundli.dasha import DashaTimeline
from kundli.knowledge_loader import houses, planets, rashis, topics


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
    "relationship": "love",
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


def detect_topic(question: str) -> Optional[str]:
    q = question.lower().strip()
    if not q:
        return None
    topic_keys = list(topics().keys())
    # Direct key match
    for key in topic_keys:
        if re.search(rf"\b{re.escape(key)}\b", q):
            return key
    for alias, key in ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", q):
            return key
    # Fuzzy: any topic label word
    for key, meta in topics().items():
        label_words = re.findall(r"[a-z]+", meta["label"].lower())
        if any(w in q for w in label_words if len(w) > 3):
            return key
    return None


def list_topics_help() -> str:
    keys = sorted(topics().keys())
    return "Try topics: " + ", ".join(keys) + " (or words like job, spouse, abroad)."


def answer_topic(
    chart: KundliChart,
    timeline: DashaTimeline,
    topic_key: str,
) -> str:
    meta = topics()[topic_key]
    house_kb = houses()
    planet_kb = planets()
    rashi_kb = rashis()

    lines: List[str] = [
        f"## {meta['label']}",
        meta["intro"],
        "",
        "From your chart:",
    ]

    for hnum in meta["houses"]:
        h = chart.houses[hnum - 1]
        hmeta = house_kb[str(hnum)]
        occ = ", ".join(h.planets) if h.planets else "no planets (look to the sign lord for nuance)"
        lines.append(
            f"- House {hnum} ({hmeta['name']}) in {h.rashi_name}: {occ}. {hmeta['summary']}"
        )

    lines.append("")
    lines.append("Key planets for this topic:")
    for pname in meta["planets"]:
        pl = chart.planets[pname]
        pmeta = planet_kb[pname]
        rmeta = rashi_kb[str(pl.info.rashi_index)]
        lines.append(
            f"- {pname} in {pl.info.rashi_name} (house {pl.house}): {pmeta['summary']} "
            f"Sign flavor: {rmeta['summary']}"
        )

    # Dasha color
    if timeline.current_mahadasha and timeline.current_antardasha:
        m = timeline.current_mahadasha.lord
        a = timeline.current_antardasha.lord
        lines.append("")
        lines.append(
            f"Current period: {m}-{a} dasha. "
            f"If {m} or {a} rules or sits in the houses above, this topic may feel more active now."
        )
        relevant = set(meta["planets"]) | {
            chart.planets[p].name
            for p in chart.planets
            if chart.planets[p].house in meta["houses"]
        }
        hits = [x for x in (m, a) if x in relevant or x in meta["planets"]]
        if hits:
            lines.append(
                f"Overlap with this topic's planets/houses: {', '.join(hits)} - timing support is plausible."
            )
        else:
            lines.append(
                "Current dasha lords are not the primary significators here - results may come more steadily than suddenly."
            )

    lines.append("")
    lines.append(
        "Remember: Jyotish shows tendencies and timing colors, not fixed fate. Your choices still matter."
    )
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
