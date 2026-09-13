"""Plain-language summaries — optional LLM, always has a rule-based fallback."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import re
from typing import Any, Dict, List, Tuple

# OpenAI-compatible chat API (Token Harbor, OpenAI, Groq, OpenRouter, …)
_DEFAULT_BASE = "https://tokenharbor.ai/v1"
# Free-tier default — paid models need Token Harbor balance
_DEFAULT_MODEL = "deepseek-v4-flash:free"


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


def _match_facts(report: Dict[str, Any]) -> str:
    """Compact facts for the Match deep-dive LLM."""
    lines = [
        f"Names: {report['person_a']['name']} (bride-side) & {report['person_b']['name']} (groom-side)",
        f"Score: {_fmt_score(float(report['total']))}/36 — {report['verdict']}",
        (
            f"Moon A ({report['person_a']['name']}): "
            f"{report['person_a']['moon_rashi']} / {report['person_a']['moon_nakshatra']} "
            f"pada {report['person_a'].get('moon_pada', '?')}"
        ),
        (
            f"Moon B ({report['person_b']['name']}): "
            f"{report['person_b']['moon_rashi']} / {report['person_b']['moon_nakshatra']} "
            f"pada {report['person_b'].get('moon_pada', '?')}"
        ),
        f"Manglik note: {report.get('manglik_note', '')}",
    ]
    if report.get("manglik_problem"):
        lines.append(f"Manglik issue: {report['manglik_problem']}")
    if report.get("manglik_solutions"):
        lines.append("Manglik practical notes: " + "; ".join(report["manglik_solutions"][:3]))
    for label, key in (("Strong gunas", "strengths"), ("Weak gunas", "watchouts")):
        items = report.get(key) or []
        if items:
            lines.append(
                f"{label}: "
                + "; ".join(
                    f"{s['title']} ({_fmt_score(float(s['score']))}/{s['max']})" for s in items
                )
            )
    for k in report.get("kootas") or []:
        bit = (
            f"{k.get('title') or k.get('name')}: "
            f"{_fmt_score(float(k['score']))}/{k['max']} ({k.get('level', 'ok')})"
        )
        if k.get("simple"):
            bit += f" — {k['simple']}"
        if k.get("problem"):
            bit += f" | issue: {k['problem']}"
        if k.get("solutions"):
            bit += " | tips: " + "; ".join(k["solutions"][:2])
        lines.append(bit)
    plan = report.get("action_plan") or []
    if plan:
        lines.append("Action ideas: " + "; ".join(plan[:4]))
    if report.get("summary"):
        lines.append(f"Engine one-liner: {report['summary']}")
    return "\n".join(lines)


def _call_llm(
    system: str,
    user: str,
    *,
    max_tokens: int = 220,
    timeout: int = 60,
) -> str | None:
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
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
        text = (text or "").strip()
        return text or None
    except urllib.error.HTTPError as exc:
        # Paid model with $0 balance — retry once on a free model
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            body = ""
        if exc.code == 402 and ":free" not in model:
            free = os.environ.get("LLM_FREE_MODEL", "deepseek-v4-flash:free").strip()
            if free and free != model:
                os.environ["LLM_MODEL"] = free
                return _call_llm(system, user, max_tokens=max_tokens, timeout=timeout)
        if os.environ.get("LLM_DEBUG"):
            print(f"LLM HTTP {exc.code}: {body[:200]}", flush=True)
        return None
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, IndexError, TimeoutError) as exc:
        if os.environ.get("LLM_DEBUG"):
            print(f"LLM call failed: {type(exc).__name__}: {exc}", flush=True)
        return None


_MATCH_SYSTEM = (
    "You write a comprehensive Vedic kundali-match deep dive in clear, normal English — "
    "warm, specific, and easy to read aloud. Sound like a thoughtful astrologer talking to a couple, "
    "not a textbook. "
    "Name both people, the score out of 36, and the verdict in the intro. "
    "You may name Moon signs and birth stars once, then explain what they mean for the relationship. "
    "Do NOT dump raw guna Sanskrit lists or house numbers. Explain issues in life language. "
    "Use ONLY the facts given — do not invent medical claims or exact wedding dates. "
    "No ritual remedies, no emoji, no bullet symbols. "
    "Each section: 2–3 full sentences. Finish EVERY section completely — especially AHEAD. "
    "Output EXACTLY these markers:\n"
    "===INTRO===\n"
    "Score, verdict, both Moons (+ stars), and overall relationship tone in plain words.\n"
    "===FIT===\n"
    "Emotional / mental chemistry — what already works between them (friendship, support, values).\n"
    "===DAILY===\n"
    "Day-to-day comfort, intimacy tone, temperament fit, and how they influence each other.\n"
    "===CHALLENGES===\n"
    "Where the chart asks for care — weak or mixed areas in everyday language, without scare tactics.\n"
    "===MANGLIK===\n"
    "Mars / Manglik check in plain words: what it means for this pair and how to take it practically.\n"
    "===AHEAD===\n"
    "Near- and mid-future outlook for the bond: what to build, when trust usually deepens, one clear next step.\n"
)

_MATCH_SECTION_ORDER = (
    ("intro", "INTRO", "At a glance"),
    ("fit", "FIT", "Emotional & mental fit"),
    ("daily", "DAILY", "Daily life & comfort"),
    ("challenges", "CHALLENGES", "Where to be careful"),
    ("manglik", "MANGLIK", "Mars energy"),
    ("ahead", "AHEAD", "What’s ahead together"),
)


def _normalize_match_markers(text: str) -> str:
    out = text
    for _, marker, _ in _MATCH_SECTION_ORDER:
        out = re.sub(
            rf"(?im)^\s*(?:===?\s*{marker}\s*===?|\*\*{marker}\*\*)\s*$",
            f"==={marker}===",
            out,
        )
        out = re.sub(rf"(?i)===\s*{marker}\s*===", f"==={marker}===", out)
    return out


def _parse_match_sections(text: str) -> Dict[str, str] | None:
    text = _normalize_match_markers(text)
    found: Dict[str, str] = {}
    for i, (sid, marker, _title) in enumerate(_MATCH_SECTION_ORDER):
        tag = f"==={marker}==="
        start = text.find(tag)
        if start < 0:
            return None
        start += len(tag)
        end = len(text)
        for _, nxt, _ in _MATCH_SECTION_ORDER[i + 1 :]:
            pos = text.find(f"==={nxt}===", start)
            if pos >= 0:
                end = pos
                break
        body = text[start:end].strip()
        body = re.sub(r"^[*#\-\d.]+\s*", "", body)
        if not body:
            return None
        found[sid] = body
    return found


def _match_sections_from_map(section_map: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {"id": sid, "title": title, "body": section_map[sid]}
        for sid, _marker, title in _MATCH_SECTION_ORDER
        if sid in section_map and section_map[sid].strip()
    ]


def _rules_match_sections(report: Dict[str, Any]) -> Tuple[str, List[Dict[str, str]]]:
    """Detailed structured Match reading without LLM."""
    a = report["person_a"]["name"]
    b = report["person_b"]["name"]
    total = _fmt_score(float(report["total"]))
    verdict = report["verdict"]
    strengths = report.get("strengths") or []
    watch = report.get("watchouts") or []
    plan = report.get("action_plan") or []

    strong_bits = (
        ", ".join(s["title"] for s in strengths[:4])
        if strengths
        else "everyday patience and clear talk more than luck alone"
    )
    weak_bits = (
        ", ".join(s["title"] for s in watch[:4])
        if watch
        else "no single guna in the weak band — still skim the okay areas"
    )
    tips = plan[0] if plan else "Talk through money, family, and timing before locking wedding plans."

    intro = (
        f"{a} and {b} score {total} out of 36 on kundali matching — “{verdict}”. "
        f"{a}’s Moon sits in {report['person_a']['moon_rashi']} "
        f"({report['person_a']['moon_nakshatra']}); "
        f"{b}’s Moon sits in {report['person_b']['moon_rashi']} "
        f"({report['person_b']['moon_nakshatra']}). "
        f"Together those Moons set the emotional weather of the relationship."
    )
    fit = (
        f"What already supports the bond: {strong_bits}. "
        f"These areas are natural gifts — keep them alive with appreciation, shared habits, "
        f"and honest check-ins rather than taking them for granted. "
        f"Mental friendship and mutual respect matter as much as romance for this pair."
    )
    daily = (
        f"Day to day, comfort grows when both people feel heard and neither has to win every argument. "
        f"Intimacy and temperament work best when routines stay kind and neither partner is rushed "
        f"into change they have not agreed to. Small habits — shared meals, fair chores, soft tone — "
        f"protect the match more than dramatic gestures."
    )
    challenges = (
        f"Where the chart asks for care: {weak_bits}. "
        f"Treat weak scores as homework, not a scare list — name the friction early, agree on boundaries, "
        f"and get a fuller consult if Nadi or Bhakoot is weak or the total feels low for your families."
    )
    manglik = (
        f"{report.get('manglik_note', 'Manglik check completed.')} "
        + (
            f"In plain words: {report['manglik_problem']} "
            if report.get("manglik_problem")
            else "No separate Mars clash stands out as a red flag for this pair. "
        )
        + "Use courage and pace wisely in the early married years; temper and haste are the real watch-outs."
    )
    ahead = (
        f"Looking ahead, this bond tends to deepen when both people choose realism over fantasy and "
        f"build trust through consistent behaviour — often more ease after the late twenties if the pair "
        f"is still young. Near term: {tips} "
        f"Strong gunas are gifts; weak gunas are the growth edge. Love still needs character, counselling "
        f"when stuck, and time — the chart is a weather report, not a verdict on worth."
    )
    section_map = {
        "intro": intro,
        "fit": fit,
        "daily": daily,
        "challenges": challenges,
        "manglik": manglik,
        "ahead": ahead,
    }
    headline = f"{a} & {b} — {total}/36 · {verdict}"
    return headline, _match_sections_from_map(section_map)


def _rules_match_summary(report: Dict[str, Any]) -> str:
    """Legacy one-block summary (joined intro + fit)."""
    _, sections = _rules_match_sections(report)
    return " ".join(s["body"] for s in sections[:2])


def match_simple_summary(report: Dict[str, Any]) -> Tuple[str, List[Dict[str, str]], str]:
    """
    Return (headline, sections[{id,title,body}], source).
    Structured match deep-dive: intro, fit, daily, challenges, manglik, ahead.
    """
    facts = _match_facts(report)
    user = f"Write the structured kundali-match deep-dive from these chart facts:\n\n{facts}"
    llm = _call_llm(_MATCH_SYSTEM, user, max_tokens=1400, timeout=100)
    if not llm:
        llm = _call_llm(_MATCH_SYSTEM, user, max_tokens=1200, timeout=100)
    if llm:
        parsed = _parse_match_sections(llm)
        if parsed:
            if len(parsed.get("ahead", "")) < 100:
                _, rules_secs = _rules_match_sections(report)
                rules_ahead = next((s["body"] for s in rules_secs if s["id"] == "ahead"), "")
                if rules_ahead:
                    parsed["ahead"] = (parsed.get("ahead", "").rstrip() + " " + rules_ahead).strip()
            a = report["person_a"]["name"]
            b = report["person_b"]["name"]
            headline = (
                f"{a} & {b} — {_fmt_score(float(report['total']))}/36 · {report['verdict']}"
            )
            first = parsed["intro"].split(".")[0].strip()
            if 20 < len(first) < 120:
                headline = first
            return headline, _match_sections_from_map(parsed), "llm"
    return (*_rules_match_sections(report), "rules")


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
    "You write a comprehensive Vedic birth-chart deep dive in clear, normal English — "
    "warm, specific, and easy to read aloud. Sound like a thoughtful astrologer talking to a friend, "
    "not a textbook and not a chatbot list. "
    "CRITICAL: Every chart is unique. Use the SPECIFIC rising, Moon, birth star, Sun, planet houses, "
    "career fields, partner tone, Manglik status, and timing from the facts. "
    "Do NOT reuse generic filler like 'steady effort beats shortcuts' or 'late twenties deepen love' "
    "unless the facts support that timing. "
    "You MUST state clearly whether the person is Manglik or not (Mars energy), and what that means "
    "in everyday words for marriage/temper — using the Manglik facts given. "
    "Name rising sign, Moon sign, birth star, and Sun sign in the intro. "
    "Do NOT dump long house-number lists; translate placements into life language. "
    "Timing: say 'until Aug 2035' or 'a longer Jupiter chapter from 2035' — never dump raw dasha strings. "
    "Use ONLY the facts given. No ritual remedies, no emoji, no markdown headings except the required markers. "
    "Each section: 2–3 full sentences. Finish EVERY section completely — especially FUTURE and MANGLIK. "
    "Output EXACTLY these markers with no extra labels:\n"
    "===INTRO===\n"
    "Rising, Moon (+ star), Sun — and the overall life tone. Mention one unique chart detail.\n"
    "===PERSONALITY===\n"
    "Emotional style from rising + Moon + birth-star summary; how they guard or share feelings.\n"
    "===CAREER===\n"
    "Use the given career fields and money/foreign notes from the facts — be specific to THIS chart.\n"
    "===RELATIONSHIPS===\n"
    "Partner qualities from the given 7th-sign tone and marriage notes — specific to THIS chart.\n"
    "===MANGLIK===\n"
    "State Manglik yes or no, Mars placement in plain words, and practical meaning for love/temper. "
    "If softened by Venus/Jupiter, say so.\n"
    "===NOW===\n"
    "Present life chapter from the timing facts — focus, opportunities, health watch if given.\n"
    "===FUTURE===\n"
    "Near- and mid-future for career, love, and direction with concrete timing from the facts.\n"
)


_SECTION_ORDER = (
    ("intro", "INTRO", "At a glance"),
    ("personality", "PERSONALITY", "Personality & mind"),
    ("career", "CAREER", "Career & wealth"),
    ("relationships", "RELATIONSHIPS", "Relationships & marriage"),
    ("manglik", "MANGLIK", "Manglik / Mars energy"),
    ("now", "NOW", "How life is going now"),
    ("future", "FUTURE", "What’s ahead"),
)

_HOUSE_PLAIN = {
    1: "self and body",
    2: "money and family voice",
    3: "siblings, courage, and short efforts",
    4: "home and emotional roots",
    5: "creativity, romance, and children themes",
    6: "work stress, rivals, and daily health",
    7: "marriage and one-to-one partnerships",
    8: "shared intensity, sudden change, and deep bonds",
    9: "luck, learning, and long journeys",
    10: "career and public reputation",
    11: "gains, networks, and goals",
    12: "foreign places, solitude, or hidden costs",
}


def _nak_summary(nak_name: str) -> str:
    try:
        from kundli.knowledge_loader import nakshatras

        for row in nakshatras().values():
            if row.get("name") == nak_name:
                return str(row.get("summary") or "").strip()
    except Exception:  # noqa: BLE001
        pass
    return ""


def _manglik_fact_lines(chart: Any) -> Tuple[bool, bool, str, List[str]]:
    """Return (is_manglik, mitigated, mars_plain, fact_lines)."""
    mars = chart.planets["Mars"]
    mars_h = mars.house
    is_m = mars_h in (1, 4, 7, 8, 12)
    venus_h = chart.planets["Venus"].house
    jup_h = chart.planets["Jupiter"].house
    h7_planets = chart.houses[6].planets
    mitigated = is_m and (
        venus_h in (1, 4, 5, 7, 9, 10)
        or jup_h in (1, 4, 7, 10)
        or "Venus" in h7_planets
        or "Jupiter" in h7_planets
    )
    where = _HOUSE_PLAIN.get(mars_h, f"house {mars_h}")
    mars_plain = f"Mars in {mars.info.rashi_name}, linked to {where}"
    lines = [
        f"Manglik status: {'YES' if is_m else 'NO'}",
        f"Mars detail: {mars_plain}",
        f"Manglik softened by Venus/Jupiter: {'yes' if mitigated else 'no'}",
    ]
    if is_m:
        lines.append(
            "Manglik meaning: higher heat in will, temper, and early married-life pace — "
            "needs cool-down habits, not panic."
        )
        if mitigated:
            lines.append(
                "Softening: Venus/Jupiter support reduces the harsh edge of Manglik for marriage tone."
            )
    else:
        lines.append(
            "Manglik meaning: Mars is not in a classic Manglik house — no Manglik flag for this chart."
        )
    return is_m, mitigated, mars_plain, lines


def _life_chart_facts(
    chart: Any,
    timeline: Any,
    draft_past: str,
    draft_present: str,
    draft_future: str,
) -> str:
    moon = chart.planets["Moon"]
    sun = chart.planets["Sun"]
    h7 = chart.houses[6]
    h10 = chart.houses[9]
    h12 = chart.houses[11]
    h2 = chart.houses[1]
    nak_sum = _nak_summary(moon.info.nakshatra_name)
    lines = [
        f"Name: {chart.birth.name}",
        f"Rising sign (Ascendant): {chart.lagna.rashi_name}",
        f"Moon sign: {moon.info.rashi_name}; birth star: {moon.info.nakshatra_name} pada {moon.info.pada}",
        f"Birth-star meaning: {nak_sum or 'use Moon sign tone'}",
        f"Sun sign: {sun.info.rashi_name}",
        f"10th-sign career tone: {_CAREER_TONE.get(h10.rashi_name, 'skilled work')}",
        f"Planets in career house (10th): {', '.join(h10.planets) if h10.planets else 'empty'}",
        f"7th-sign partner tone: {_PARTNER_TONE.get(h7.rashi_name, 'steady')}",
        f"Planets in marriage house (7th): {', '.join(h7.planets) if h7.planets else 'empty'}",
        f"Planets in money house (2nd): {', '.join(h2.planets) if h2.planets else 'empty'}",
        f"Planets in foreign/solitude house (12th): {', '.join(h12.planets) if h12.planets else 'empty'}",
        f"Rising style: {_RISING_TONE.get(chart.lagna.rashi_name, '')}",
        f"Moon feeling style: {_MOON_TONE.get(moon.info.rashi_name, '')}",
    ]
    _, _, _, mang_lines = _manglik_fact_lines(chart)
    lines.extend(mang_lines)
    for name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        pl = chart.planets[name]
        lines.append(
            f"{name}: {pl.info.rashi_name}, house {pl.house} ({_HOUSE_PLAIN.get(pl.house, '')})"
        )
    if timeline.current_mahadasha:
        m = timeline.current_mahadasha
        lines.append(
            f"Current long life chapter: planet {m.lord}, ends {m.end.strftime('%b %Y')}"
        )
    if timeline.current_antardasha:
        a = timeline.current_antardasha
        lines.append(
            f"Current shorter chapter: planet {a.lord}, "
            f"{a.start.strftime('%b %Y')} to {a.end.strftime('%b %Y')}"
        )
    if timeline.current_mahadasha:
        for m in timeline.mahadashas:
            if m.start > timeline.current_mahadasha.start:
                lines.append(
                    f"Next long life chapter: planet {m.lord}, "
                    f"{m.start.strftime('%b %Y')} to {m.end.strftime('%b %Y')}"
                )
                break
    lines.append("ENGINE NOTES (pattern): " + draft_past)
    lines.append("ENGINE NOTES (now): " + draft_present)
    lines.append("ENGINE NOTES (ahead): " + draft_future)
    return "\n".join(lines)


def _normalize_life_markers(text: str) -> str:
    """Accept ===INTRO===, === INTRO ===, or **INTRO** style markers."""
    out = text
    for _, marker, _ in _SECTION_ORDER:
        out = re.sub(
            rf"(?im)^\s*(?:===?\s*{marker}\s*===?|\*\*{marker}\*\*)\s*$",
            f"==={marker}===",
            out,
        )
        out = re.sub(
            rf"(?i)===\s*{marker}\s*===",
            f"==={marker}===",
            out,
        )
    return out


def _parse_life_sections(text: str) -> Dict[str, str] | None:
    text = _normalize_life_markers(text)
    found: Dict[str, str] = {}
    required = {sid for sid, _, _ in _SECTION_ORDER if sid != "manglik"}
    for i, (sid, marker, _title) in enumerate(_SECTION_ORDER):
        tag = f"==={marker}==="
        start = text.find(tag)
        if start < 0:
            if sid == "manglik":
                continue
            return None
        start += len(tag)
        end = len(text)
        for _, nxt, _ in _SECTION_ORDER[i + 1 :]:
            pos = text.find(f"==={nxt}===", start)
            if pos >= 0:
                end = pos
                break
        body = text[start:end].strip()
        body = re.sub(r"^[*#\-\d.]+\s*", "", body)
        if not body:
            if sid == "manglik":
                continue
            return None
        found[sid] = body
    if not required.issubset(found):
        return None
    return found


def _sections_from_map(section_map: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {"id": sid, "title": title, "body": section_map[sid]}
        for sid, _marker, title in _SECTION_ORDER
        if sid in section_map and section_map[sid].strip()
    ]


def _soft_jargon(text: str) -> str:
    out = text
    for word, rep in (
        ("Mahadasha", "long chapter"),
        ("Antardasha", "shorter chapter"),
        ("Lagna", "natural style"),
        ("nakshatra", "birth star"),
        ("rashi", "sign"),
        ("10th lord", "career guide"),
        ("7th lord", "partnership guide"),
        ("2nd lord", "money guide"),
        ("4th lord", "home guide"),
        ("6th lord", "health guide"),
        ("house", "part of life"),
    ):
        out = out.replace(word, rep)
    return out


# Lightweight tone maps (kept here to avoid circular import with life_summary)
_CAREER_TONE = {
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

_PARTNER_TONE = {
    "Aries": "direct and independent",
    "Taurus": "loyal and security-seeking",
    "Gemini": "talkative and mentally restless",
    "Cancer": "protective and home-centered",
    "Leo": "warm and needing appreciation",
    "Virgo": "careful and detail-minded",
    "Libra": "fair and companion-focused",
    "Scorpio": "intense and deeply loyal",
    "Sagittarius": "honest and freedom-loving",
    "Capricorn": "serious, pragmatic, and long-term oriented",
    "Aquarius": "friendly but needs space",
    "Pisces": "gentle and emotionally open",
}

_RISING_TONE = {
    "Aries": "bold, quick to act, and protective of your own path",
    "Taurus": "steady, sensory, and loyal once trust is earned",
    "Gemini": "curious, talkative, and mentally restless",
    "Cancer": "empathetic, intuitive, and protective of your inner circle",
    "Leo": "warm, proud, and naturally drawn to lead or perform",
    "Virgo": "careful, helpful, and detail-aware",
    "Libra": "fair-minded, people-aware, and drawn to harmony",
    "Scorpio": "intense, private, and deeply loyal",
    "Sagittarius": "open, honest, and hungry for growth",
    "Capricorn": "disciplined, ambitious, and quietly determined",
    "Aquarius": "independent, idea-driven, and a little unconventional",
    "Pisces": "sensitive, imaginative, and emotionally porous",
}

_MOON_TONE = {
    "Aries": "you feel first and decide fast",
    "Taurus": "you need comfort and stability before you open up",
    "Gemini": "you process feelings by talking and thinking them through",
    "Cancer": "emotions run deep and home/family matter a lot",
    "Leo": "you want warmth, recognition, and heartfelt loyalty",
    "Virgo": "you tidy feelings with analysis and practical care",
    "Libra": "you seek balance and dislike emotional chaos",
    "Scorpio": "feelings are private, intense, and all-or-nothing",
    "Sagittarius": "you need space and meaning, not clinging",
    "Capricorn": "you process emotions logically and rarely show vulnerability at once",
    "Aquarius": "you stay cool-headed and need mental freedom",
    "Pisces": "you absorb moods around you and feel things in waves",
}


def _plain_now_future(draft: str) -> str:
    """Turn engine timing notes into readable prose scraps."""
    out = _soft_jargon(draft)
    out = re.sub(r"\b\d+(st|nd|rd|th)\b", "", out)
    out = out.replace(";", ".")
    out = re.sub(r"\s{2,}", " ", out).strip(" .")
    return out


def _rules_life_sections(
    chart: Any,
    draft_past: str,
    draft_present: str,
    draft_future: str,
) -> Tuple[str, List[Dict[str, str]]]:
    """Structured plain reading without LLM — chart-specific, includes Manglik."""
    name = chart.birth.name
    rising = chart.lagna.rashi_name
    moon = chart.planets["Moon"]
    sun = chart.planets["Sun"]
    mars = chart.planets["Mars"]
    h7 = chart.houses[6]
    h10 = chart.houses[9]
    h12 = chart.houses[11]
    career = _CAREER_TONE.get(h10.rashi_name, "skilled, focused work")
    partner = _PARTNER_TONE.get(h7.rashi_name, "steady and sincere")
    rising_line = _RISING_TONE.get(rising, "shaped by your rising sign")
    moon_line = _MOON_TONE.get(moon.info.rashi_name, "your Moon colors how you feel")
    nak_sum = _nak_summary(moon.info.nakshatra_name)
    is_m, mitigated, mars_plain, _ = _manglik_fact_lines(chart)
    present = _plain_now_future(draft_present)
    future = _plain_now_future(draft_future)

    tenth_occ = (
        f" Right now the career area of the chart holds {', '.join(h10.planets)}, which colors how work shows up."
        if h10.planets
        else ""
    )
    seventh_occ = (
        f" The partnership area currently holds {', '.join(h7.planets)}, which shapes marriage chemistry."
        if h7.planets
        else ""
    )
    foreign = ""
    if h12.planets:
        foreign = (
            f" With {', '.join(h12.planets)} tied to foreign places or behind-the-scenes work, "
            f"gains can also come through remote setups, travel, or research away from the spotlight."
        )

    intro = (
        f"{name}, your chart has {rising} rising, Moon in {moon.info.rashi_name} "
        f"({moon.info.nakshatra_name}, pada {moon.info.pada}), and Sun in {sun.info.rashi_name}. "
        f"You are {'Manglik' if is_m else 'not Manglik'} "
        f"(Mars in {mars.info.rashi_name}, tied to {_HOUSE_PLAIN.get(mars.house, 'its house')}). "
        f"That mix sets a life tone that is personal to you — not a generic template."
    )
    personality = (
        f"With {rising} rising, you come across as {rising_line}. "
        f"Because your Moon sits in {moon.info.rashi_name}, {moon_line}. "
        + (
            f"Your birth star {moon.info.nakshatra_name} points to this: {nak_sum} "
            if nak_sum
            else f"{moon.info.nakshatra_name} flavors how your mind seeks peace and progress. "
        )
        + "You open up on your own timeline; trust and lived proof matter more than big emotional displays."
    )
    career_body = (
        f"Work that fits your chart leans toward {career}.{tenth_occ} "
        f"Money tends to grow when you own a clear skill and build reputation in that lane, "
        f"not only from quick wins.{foreign}"
    )
    relationships = (
        f"In partnership you are drawn to someone who is {partner}.{seventh_occ} "
        f"Marriage tone follows your chart's 7th-sign flavor — talk honestly about pace, family, and space "
        f"before locking big commitments. Emotional ease deepens when both people feel respected, not managed."
    )
    if is_m:
        manglik_body = (
            f"Yes — this chart is Manglik: {mars_plain}. "
            f"In everyday terms that often means more heat in will, courage, and temper, especially around "
            f"marriage timing and early married years. "
            + (
                "Venus/Jupiter support softens the edge, so the flag is real but not as harsh as textbooks scare. "
                if mitigated
                else "Cool-down habits and patient timing matter more than panic. "
            )
            + "Treat Manglik as a pace-and-temper note, not a verdict on your worth."
        )
    else:
        manglik_body = (
            f"No — this chart is not Manglik. {mars_plain}, which sits outside the classic Manglik houses "
            f"(self, home, marriage, intensity, or foreign/hidden zones). "
            f"Mars still gives drive, but you do not carry the classic Manglik marriage flag."
        )
    now = (
        f"In this chapter: {present}. "
        f"Use it to make concrete choices on work and relationships that match how your chart actually behaves."
    )
    ahead = (
        f"Looking ahead: {future}. "
        + (
            "If Manglik heat has felt loud, it usually eases with maturity and steadier partnership habits. "
            if is_m
            else ""
        )
        + "Keep building the skills your career lane rewards, and let love grow through consistent behaviour."
    )
    section_map = {
        "intro": intro,
        "personality": personality,
        "career": career_body,
        "relationships": relationships,
        "manglik": manglik_body,
        "now": now,
        "future": ahead,
    }
    _ = draft_past
    headline = f"{name} — {rising} rising · {'Manglik' if is_m else 'not Manglik'}"
    return headline, _sections_from_map(section_map)


def life_predictive_summary(
    *,
    chart: Any,
    timeline: Any,
    draft_past: str,
    draft_present: str,
    draft_future: str,
) -> Tuple[str, List[Dict[str, str]], str]:
    """
    Return (headline, sections[{id,title,body}], source).
    Structured deep-dive including Manglik.
    """
    facts = _life_chart_facts(chart, timeline, draft_past, draft_present, draft_future)
    user = "Write the structured life deep-dive from these chart facts:\n\n" + facts
    llm = _call_llm(_LIFE_SYSTEM, user, max_tokens=1700, timeout=100)
    if not llm:
        llm = _call_llm(_LIFE_SYSTEM, user, max_tokens=1500, timeout=100)
    if llm:
        parsed = _parse_life_sections(llm)
        if parsed:
            _, rules_secs = _rules_life_sections(
                chart, draft_past, draft_present, draft_future
            )
            rules_map = {s["id"]: s["body"] for s in rules_secs}
            if len(parsed.get("future", "")) < 120 and rules_map.get("future"):
                parsed["future"] = (
                    parsed.get("future", "").rstrip() + " " + rules_map["future"]
                ).strip()
            if "manglik" not in parsed or len(parsed.get("manglik", "")) < 60:
                parsed["manglik"] = rules_map.get("manglik", parsed.get("manglik", ""))
            mang_body = parsed.get("manglik", "")
            is_m, _, _, _ = _manglik_fact_lines(chart)
            if is_m and "not Manglik" in mang_body and "is Manglik" not in mang_body:
                parsed["manglik"] = rules_map["manglik"]
            if (not is_m) and re.search(r"\bYes\b.*\bManglik\b", mang_body, re.I):
                parsed["manglik"] = rules_map["manglik"]
            headline = (
                f"{chart.birth.name} — {chart.lagna.rashi_name} rising · "
                f"{'Manglik' if is_m else 'not Manglik'}"
            )
            first = parsed["intro"].split(".")[0].strip()
            if 20 < len(first) < 110:
                headline = first
            return headline, _sections_from_map(parsed), "llm"
    return (*_rules_life_sections(chart, draft_past, draft_present, draft_future), "rules")
