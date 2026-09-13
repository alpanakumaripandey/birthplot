"""Plain-language summaries — optional LLM, always has a rule-based fallback."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Tuple

# OpenAI-compatible chat API (Token Harbor, OpenAI, Groq, OpenRouter, …)
_DEFAULT_BASE = "https://tokenharbor.ai/v1"
_DEFAULT_MODEL = "th-orchestra"


def _api_config() -> Tuple[str | None, str, str]:
    key = (
        os.environ.get("LLM_API_KEY")
        or os.environ.get("TOKENHARBOR_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    ).strip()
    base = (os.environ.get("LLM_BASE_URL") or _DEFAULT_BASE).rstrip("/")
    model = (os.environ.get("LLM_MODEL") or _DEFAULT_MODEL).strip()
    # Token Harbor keys need the Token Harbor base even if LLM_BASE_URL was unset.
    if key.startswith("thk_") and "LLM_BASE_URL" not in os.environ:
        base = "https://tokenharbor.ai/v1"
    return key or None, base, model


def _fmt_score(n: float) -> str:
    return str(int(n)) if n == int(n) else f"{n:.1f}"


def _rules_match_summary(report: Dict[str, Any]) -> str:
    """Short plain-English summary without any API."""
    a = report["person_a"]["name"]
    b = report["person_b"]["name"]
    total = report["total"]
    verdict = report["verdict"]

    parts: List[str] = [
        f"{a} and {b} scored {_fmt_score(float(total))} out of 36 on kundali matching — {verdict}.",
        (
            f"{a}'s Moon is in {report['person_a']['moon_rashi']} ({report['person_a']['moon_nakshatra']}); "
            f"{b}'s Moon is in {report['person_b']['moon_rashi']} ({report['person_b']['moon_nakshatra']})."
        ),
    ]

    strengths = report.get("strengths") or []
    if strengths:
        bits = ", ".join(s["title"] for s in strengths[:3])
        parts.append(f"What's working: {bits}.")

    watch = report.get("watchouts") or []
    if watch:
        bits = ", ".join(s["title"] for s in watch[:3])
        parts.append(f"Needs attention: {bits}.")

    parts.append(f"Manglik check: {report.get('manglik_note', 'Not checked')}.")

    plan = report.get("action_plan") or []
    if plan:
        parts.append(f"Practical next step: {plan[0]}")

    return " ".join(parts)


def _match_facts(report: Dict[str, Any]) -> str:
    """Compact facts for the LLM prompt."""
    lines = [
        f"Names: {report['person_a']['name']} (bride-side) & {report['person_b']['name']} (groom-side)",
        f"Score: {_fmt_score(float(report['total']))}/36 — {report['verdict']}",
        f"Moon A: {report['person_a']['moon_rashi']} / {report['person_a']['moon_nakshatra']}",
        f"Moon B: {report['person_b']['moon_rashi']} / {report['person_b']['moon_nakshatra']}",
        f"Manglik: {report.get('manglik_note', '')}",
    ]
    for label, key in (("Strong", "strengths"), ("Weak", "watchouts")):
        items = report.get(key) or []
        if items:
            lines.append(
                f"{label}: "
                + "; ".join(f"{s['title']} ({_fmt_score(float(s['score']))}/{s['max']})" for s in items)
            )
    for k in report.get("kootas") or []:
        if k.get("level") == "weak" and k.get("problem"):
            lines.append(f"{k['title']} issue: {k['problem']}")
    return "\n".join(lines)


def _call_llm(system: str, user: str, *, max_tokens: int = 220) -> str | None:
    api_key, base, model = _api_config()
    if not api_key:
        return None

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.4,
    }
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
        text = (text or "").strip()
        return text or None
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError, IndexError, TimeoutError):
        return None


_MATCH_SYSTEM = (
    "You explain Vedic kundali matching (Ashtakoota) in very simple English for non-astrologers. "
    "Use short sentences. No jargon without a one-line explanation. "
    "Cover: overall score, what is good, what to watch, Manglik, and one practical advice. "
    "Max 6 sentences. No bullet lists. Not medical or legal advice."
)


_ASK_SYSTEM = (
    "You are a friendly Vedic astrology guide for ordinary people. "
    "Answer using ONLY the chart facts and draft reading provided. "
    "Write in warm, normal everyday English — like explaining to a friend over tea. "
    "Structure: (1) one short opening that answers the question directly, "
    "(2) what the chart suggests about present, (3) what may come next, "
    "(4) one practical tip. "
    "Avoid house numbers, Sanskrit jargon, and markdown headings unless necessary. "
    "If you must mention a planet or dasha, explain it in plain words in the same sentence. "
    "Max 8 short sentences or 2 short paragraphs. "
    "Not medical, legal, or financial advice — guidance only."
)


def match_simple_summary(report: Dict[str, Any]) -> Tuple[str, str]:
    """
    Return (summary_text, source) where source is 'llm' or 'rules'.
    """
    facts = _match_facts(report)
    llm = _call_llm(
        _MATCH_SYSTEM,
        f"Write a simple marriage-match summary from these chart facts:\n\n{facts}",
    )
    if llm:
        return llm, "llm"
    return _rules_match_summary(report), "rules"


def _ask_chart_facts(
    chart: Any,
    timeline: Any,
    topic: str | None,
    question: str,
) -> str:
    """Compact chart + timing facts for Ask LLM."""
    moon = chart.planets["Moon"]
    lines = [
        f"Name: {chart.birth.name}",
        f"User question: {question.strip()}",
        f"Topic: {topic or 'unknown'}",
        f"Rising sign (Lagna): {chart.lagna.rashi_name}",
        f"Moon: {moon.info.rashi_name} / {moon.info.nakshatra_name} pada {moon.info.pada}",
    ]
    if timeline.current_mahadasha:
        m = timeline.current_mahadasha
        lines.append(
            f"Current long period (Mahadasha): {m.lord} until {m.end.strftime('%b %Y')}"
        )
    if timeline.current_antardasha:
        a = timeline.current_antardasha
        lines.append(
            f"Current chapter (Antardasha): {a.lord} "
            f"({a.start.strftime('%b %Y')}–{a.end.strftime('%b %Y')})"
        )
    # Planet house snapshot (short)
    bits = []
    for name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        pl = chart.planets[name]
        bits.append(f"{name} in house {pl.house} ({pl.info.rashi_name})")
    lines.append("Planets: " + "; ".join(bits))
    return "\n".join(lines)


def _rules_ask_summary(rule_answer: str, question: str, topic: str | None) -> str:
    """Tighten the rule-based answer into a shorter plain block if LLM is unavailable."""
    # Strip markdown headings / version tags for a cleaner fallback
    cleaned: List[str] = []
    for line in rule_answer.splitlines():
        s = line.strip()
        if not s:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        if s.startswith("(reading "):
            continue
        if s.startswith("#"):
            s = s.lstrip("#").strip()
        if s.startswith("•") or s.startswith("-") or s.startswith("*"):
            s = s.lstrip("•-* ").strip()
        cleaned.append(s)
    body = " ".join(p for p in cleaned if p)
    # Keep it readable — first ~900 chars at sentence boundary if very long
    if len(body) > 900:
        cut = body[:900]
        last = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
        if last > 400:
            body = cut[: last + 1]
        else:
            body = cut.rstrip() + "…"
    lead = f"About your question on {topic}: " if topic else ""
    return f"{lead}{body}".strip()


def ask_plain_answer(
    *,
    chart: Any,
    timeline: Any,
    question: str,
    topic: str | None,
    rule_answer: str,
) -> Tuple[str, str]:
    """
    Return (plain_answer, source) where source is 'llm' or 'rules'.
    Uses chart facts + the deterministic draft; LLM rewrites into everyday language.
    """
    if topic is None:
        # Keep help / unmatched topic responses as-is
        return rule_answer, "rules"

    facts = _ask_chart_facts(chart, timeline, topic, question)
    user = (
        f"Rewrite this chart reading as a clear answer to the user's question.\n\n"
        f"CHART FACTS:\n{facts}\n\n"
        f"DRAFT READING (facts to respect — rewrite, do not invent new predictions):\n"
        f"{rule_answer}\n\n"
        f"Write the final answer in normal language now."
    )
    llm = _call_llm(_ASK_SYSTEM, user, max_tokens=450)
    if llm:
        return llm, "llm"
    return _rules_ask_summary(rule_answer, question, topic), "rules"


_LIFE_SYSTEM = (
    "You are a Vedic life reader writing for ordinary people. "
    "Interpret the whole birth chart as Predictions for Past foundation, Present life, and Future outlook. "
    "Use ONLY the facts given — do not invent planets, dates, or events not supported by the facts. "
    "PURE everyday English. ZERO technical jargon: no house numbers, no Lagna, no Mahadasha names unless "
    "you translate them (e.g. say 'a long Jupiter chapter until 2027' not 'Jupiter Mahadasha'). "
    "No Sanskrit terms. No remedies. Write as confident, kind predictions. "
    "Output EXACTLY this format with the three markers:\n"
    "===HEADLINE===\n"
    "one short line\n"
    "===PAST===\n"
    "2-4 sentences: who they tend to be, work/money/love/home pattern from birth\n"
    "===PRESENT===\n"
    "2-4 sentences: what life feels like now — career, relationships, health tone, timing\n"
    "===FUTURE===\n"
    "2-4 sentences: what is coming — windows for work, love, and life changes\n"
)


def _life_chart_facts(
    chart: Any,
    timeline: Any,
    draft_past: str,
    draft_present: str,
    draft_future: str,
) -> str:
    moon = chart.planets["Moon"]
    lines = [
        f"Name: {chart.birth.name}",
        f"Rising sign: {chart.lagna.rashi_name}",
        f"Moon: {moon.info.rashi_name} / {moon.info.nakshatra_name}",
    ]
    for name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        pl = chart.planets[name]
        lines.append(f"{name}: {pl.info.rashi_name}, life-area house {pl.house}")
    if timeline.current_mahadasha:
        m = timeline.current_mahadasha
        lines.append(f"Long current chapter lord: {m.lord} until {m.end.strftime('%b %Y')}")
    if timeline.current_antardasha:
        a = timeline.current_antardasha
        lines.append(
            f"Current shorter chapter lord: {a.lord} "
            f"({a.start.strftime('%b %Y')}–{a.end.strftime('%b %Y')})"
        )
    lines.append("DRAFT PAST FACTS: " + draft_past)
    lines.append("DRAFT PRESENT FACTS: " + draft_present)
    lines.append("DRAFT FUTURE FACTS: " + draft_future)
    return "\n".join(lines)


def _parse_life_sections(text: str) -> Dict[str, str] | None:
    markers = ("HEADLINE", "PAST", "PRESENT", "FUTURE")
    found: Dict[str, str] = {}
    for i, name in enumerate(markers):
        start = text.find(f"==={name}===")
        if start < 0:
            return None
        start += len(f"==={name}===")
        end = len(text)
        for nxt in markers[i + 1 :]:
            pos = text.find(f"==={nxt}===", start)
            if pos >= 0:
                end = pos
                break
        found[name.lower()] = text[start:end].strip()
    if not all(found.get(k) for k in ("past", "present", "future")):
        return None
    return found


def _rules_life_predictive(
    chart: Any,
    draft_past: str,
    draft_present: str,
    draft_future: str,
) -> Tuple[str, List[str]]:
    """Plain predictive fallback without LLM."""
    name = chart.birth.name
    rising = chart.lagna.rashi_name
    moon = chart.planets["Moon"].info.rashi_name
    headline = f"{name}'s life path — past roots, present chapter, future windows"
    past = (
        f"{name} comes into life with a {rising} rising style and a {moon} emotional tone. "
        f"From birth the chart points to lasting patterns in work, money, partnership, and home. "
        f"{draft_past}"
    )
    # Soften jargon words in drafts
    for word, rep in (
        ("Mahadasha", "long life chapter"),
        ("Antardasha", "shorter chapter"),
        ("Lagna", "rising style"),
        ("10th", "career zone"),
        ("7th", "partnership zone"),
        ("2nd", "money zone"),
        ("4th", "home zone"),
        ("6th", "health/effort zone"),
        ("house", "life area"),
    ):
        past = past.replace(word, rep)
    present = draft_present
    future = draft_future
    for word, rep in (
        ("Mahadasha", "long chapter"),
        ("Antardasha", "shorter chapter"),
    ):
        present = present.replace(word, rep)
        future = future.replace(word, rep)
    present = (
        f"Right now, this is the active chapter of life. {present} "
        "Treat it as weather for decisions — your effort still steers the result."
    )
    future = (
        f"Looking ahead: {future} "
        "Stay open to timing, but keep building day by day."
    )
    return headline, [past, present, future]


def life_predictive_summary(
    *,
    chart: Any,
    timeline: Any,
    draft_past: str,
    draft_present: str,
    draft_future: str,
) -> Tuple[str, List[str], str]:
    """
    Return (headline, [past, present, future], source).
    LLM preferred; rules fallback always available.
    """
    facts = _life_chart_facts(chart, timeline, draft_past, draft_present, draft_future)
    llm = _call_llm(
        _LIFE_SYSTEM,
        f"Write the life prediction from these chart facts:\n\n{facts}",
        max_tokens=700,
    )
    if llm:
        parsed = _parse_life_sections(llm)
        if parsed:
            headline = parsed.get("headline") or f"{chart.birth.name} — life reading"
            return headline, [parsed["past"], parsed["present"], parsed["future"]], "llm"
        # LLM returned prose without markers — use as present-focused single block split
        paras = [p.strip() for p in llm.split("\n\n") if p.strip()]
        if len(paras) >= 3:
            return (
                f"{chart.birth.name} — life reading",
                paras[:3],
                "llm",
            )
    headline, insights = _rules_life_predictive(chart, draft_past, draft_present, draft_future)
    return headline, insights, "rules"
