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
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
        text = (text or "").strip()
        return text or None
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError, IndexError):
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
