"""Ashtakoota (36-point) guna milan for marriage matching from Moon placements."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from kundli.chart import KundliChart

# Nakshatra index 1–27 → attribute tables (classical North-Indian Ashtakoota)

# Yoni animal per nakshatra (1-indexed via list position)
YONI: Tuple[str, ...] = (
    "Horse",
    "Elephant",
    "Sheep",
    "Serpent",
    "Serpent",
    "Dog",
    "Cat",
    "Sheep",
    "Cat",
    "Rat",
    "Rat",
    "Cow",
    "Buffalo",
    "Tiger",
    "Buffalo",
    "Tiger",
    "Deer",
    "Deer",
    "Dog",
    "Monkey",
    "Mongoose",
    "Monkey",
    "Lion",
    "Horse",
    "Lion",
    "Cow",
    "Elephant",
)

# Enemy yoni pairs (symmetric) — 0 points; same animal = 4; else 2
YONI_ENEMY = {
    frozenset({"Horse", "Buffalo"}),
    frozenset({"Elephant", "Lion"}),
    frozenset({"Sheep", "Monkey"}),
    frozenset({"Serpent", "Mongoose"}),
    frozenset({"Dog", "Deer"}),
    frozenset({"Cat", "Rat"}),
    frozenset({"Cow", "Tiger"}),
}

# Gana: D=Deva, M=Manushya, R=Rakshasa
GANA: Tuple[str, ...] = (
    "Deva",
    "Manushya",
    "Rakshasa",
    "Manushya",
    "Deva",
    "Manushya",
    "Deva",
    "Deva",
    "Rakshasa",
    "Rakshasa",
    "Manushya",
    "Manushya",
    "Deva",
    "Rakshasa",
    "Deva",
    "Rakshasa",
    "Deva",
    "Rakshasa",
    "Rakshasa",
    "Manushya",
    "Manushya",
    "Deva",
    "Rakshasa",
    "Rakshasa",
    "Manushya",
    "Manushya",
    "Deva",
)

# Nadi: Adi / Madhya / Antya
NADI: Tuple[str, ...] = (
    "Adi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Adi",
    "Adi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Adi",
    "Adi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Adi",
    "Adi",
    "Madhya",
    "Antya",
    "Antya",
    "Madhya",
    "Adi",
    "Adi",
    "Madhya",
    "Antya",
)

# Moon rashi → Varna rank (higher = Brahmin)
VARNA_RANK = {
    "Cancer": 4,
    "Scorpio": 4,
    "Pisces": 4,
    "Aries": 3,
    "Leo": 3,
    "Sagittarius": 3,
    "Taurus": 2,
    "Virgo": 2,
    "Capricorn": 2,
    "Gemini": 1,
    "Libra": 1,
    "Aquarius": 1,
}

VARNA_NAME = {4: "Brahmin", 3: "Kshatriya", 2: "Vaishya", 1: "Shudra"}

# Vashya class by Moon rashi
VASHYA_CLASS = {
    "Aries": "Chatushpada",
    "Taurus": "Chatushpada",
    "Gemini": "Manava",
    "Cancer": "Jalachara",
    "Leo": "Vanachara",
    "Virgo": "Manava",
    "Libra": "Manava",
    "Scorpio": "Keeta",
    "Sagittarius": "Chatushpada",
    "Capricorn": "Chatushpada",
    "Aquarius": "Manava",
    "Pisces": "Jalachara",
}

# Boy class → Girl class → points (max 2)
_VASHYA_SCORE: Dict[Tuple[str, str], float] = {
    ("Chatushpada", "Chatushpada"): 2,
    ("Chatushpada", "Manava"): 1,
    ("Chatushpada", "Jalachara"): 1,
    ("Chatushpada", "Vanachara"): 2,
    ("Chatushpada", "Keeta"): 1,
    ("Manava", "Chatushpada"): 1,
    ("Manava", "Manava"): 2,
    ("Manava", "Jalachara"): 1,
    ("Manava", "Vanachara"): 1,
    ("Manava", "Keeta"): 1,
    ("Jalachara", "Chatushpada"): 1.5,
    ("Jalachara", "Manava"): 1,
    ("Jalachara", "Jalachara"): 2,
    ("Jalachara", "Vanachara"): 1,
    ("Jalachara", "Keeta"): 1,
    ("Vanachara", "Chatushpada"): 0,
    ("Vanachara", "Manava"): 0,
    ("Vanachara", "Jalachara"): 0,
    ("Vanachara", "Vanachara"): 2,
    ("Vanachara", "Keeta"): 0,
    ("Keeta", "Chatushpada"): 1,
    ("Keeta", "Manava"): 1,
    ("Keeta", "Jalachara"): 1,
    ("Keeta", "Vanachara"): 0,
    ("Keeta", "Keeta"): 2,
}

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

# Natural friendship among Moon-sign lords for Graha Maitri
# Friends / Neutrals / Enemies (classical simplified)
_FRIENDS = {
    "Sun": {"Moon", "Mars", "Jupiter"},
    "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}
_ENEMIES = {
    "Sun": {"Venus", "Saturn"},
    "Moon": {"none"},
    "Mars": {"Mercury"},
    "Mercury": {"Moon"},
    "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"},
    "Saturn": {"Sun", "Moon", "Mars"},
}


def _moon(chart: KundliChart) -> Tuple[int, str, int, str]:
    """nak_index (1-27), nak_name, rashi_index (1-12), rashi_name."""
    m = chart.planets["Moon"]
    return (
        m.info.nakshatra_index,
        m.info.nakshatra_name,
        m.info.rashi_index,
        m.info.rashi_name,
    )


def _manglik(chart: KundliChart) -> Tuple[bool, str]:
    mars_h = chart.planets["Mars"].house
    yes = mars_h in (1, 4, 7, 8, 12)
    return yes, f"Mars in house {mars_h}"


def _varna(a_rashi: str, b_rashi: str) -> Tuple[float, str]:
    """A = bride-side, B = groom-side. Full point if groom varna >= bride."""
    ra, rb = VARNA_RANK[a_rashi], VARNA_RANK[b_rashi]
    score = 1.0 if rb >= ra else 0.0
    detail = f"{VARNA_NAME[ra]}–{VARNA_NAME[rb]}"
    return score, detail


def _vashya(a_rashi: str, b_rashi: str) -> Tuple[float, str]:
    ca, cb = VASHYA_CLASS[a_rashi], VASHYA_CLASS[b_rashi]
    # Classical table oriented boy→girl; use B as boy, A as girl
    score = float(_VASHYA_SCORE.get((cb, ca), 0))
    return score, f"{cb}–{ca}"


def _tara(a_nak: int, b_nak: int) -> Tuple[float, str]:
    """Count from bride (A) to groom (B)."""
    count = ((b_nak - a_nak) % 27) + 1
    rem = count % 9
    if rem == 0:
        rem = 9
    names = {
        1: "Janma",
        2: "Sampat",
        3: "Vipat",
        4: "Kshema",
        5: "Pratyak",
        6: "Sadhana",
        7: "Naidhana",
        8: "Mitra",
        9: "Ati-Mitra",
    }
    if rem in (1, 2, 4, 6, 8, 9):
        score = 3.0
    elif rem in (3, 5, 7):
        score = 1.5
    else:
        score = 0.0
    return score, f"{names[rem]} (#{count})"


def _yoni(a_nak: int, b_nak: int) -> Tuple[float, str]:
    ya, yb = YONI[a_nak - 1], YONI[b_nak - 1]
    pair = frozenset({ya, yb})
    if ya == yb:
        score = 4.0
    elif pair in YONI_ENEMY:
        score = 0.0
    else:
        score = 2.0
    return score, f"{ya}–{yb}"


def _graha_maitri(a_rashi: str, b_rashi: str) -> Tuple[float, str]:
    la, lb = SIGN_LORD[a_rashi], SIGN_LORD[b_rashi]
    if la == lb:
        score = 5.0
    elif lb in _FRIENDS.get(la, set()) and la in _FRIENDS.get(lb, set()):
        score = 5.0
    elif lb in _FRIENDS.get(la, set()) or la in _FRIENDS.get(lb, set()):
        score = 4.0
    elif lb in _ENEMIES.get(la, set()) or la in _ENEMIES.get(lb, set()):
        score = 0.5
    else:
        score = 3.0
    return score, f"{la}–{lb}"


def _gana(a_nak: int, b_nak: int) -> Tuple[float, str]:
    ga, gb = GANA[a_nak - 1], GANA[b_nak - 1]
    if ga == gb:
        score = 6.0
    elif {ga, gb} == {"Deva", "Manushya"}:
        score = 5.0
    elif {ga, gb} == {"Manushya", "Rakshasa"}:
        score = 1.0
    else:  # Deva–Rakshasa
        score = 0.0
    return score, f"{ga}–{gb}"


def _bhakoot(a_rashi_i: int, b_rashi_i: int) -> Tuple[float, str]:
    """Rashi indices 1–12. Zero for 2/12, 5/9, 6/8; else 7."""
    nth = ((b_rashi_i - a_rashi_i) % 12) + 1
    nth_rev = ((a_rashi_i - b_rashi_i) % 12) + 1
    if nth == 1:
        return 7.0, "same rashi"
    if {nth, nth_rev} in ({2, 12}, {5, 9}, {6, 8}):
        return 0.0, f"{nth}/{nth_rev} dosha"
    return 7.0, f"{nth}/{nth_rev}"


def _nadi(a_nak: int, b_nak: int) -> Tuple[float, str]:
    na, nb = NADI[a_nak - 1], NADI[b_nak - 1]
    if na == nb:
        return 0.0, f"same {na} (dosha)"
    return 8.0, f"{na}–{nb}"


def _level(score: float, max_pts: float) -> str:
    if max_pts <= 0:
        return "ok"
    ratio = score / max_pts
    if ratio >= 0.75:
        return "strong"
    if ratio >= 0.4:
        return "ok"
    return "weak"


def _pack(
    explanation: str,
    *,
    problem: str | None = None,
    solutions: List[str] | None = None,
) -> Dict[str, Any]:
    return {
        "explanation": explanation,
        "problem": problem,
        "solutions": solutions or [],
    }


def _varna_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Varna looks at the Moon-sign “outlook class” of each person ({detail}). "
        f"It hints whether {a} and {b} feel equal in values, dignity, and life seriousness — "
        "not caste in the social sense, but ego and worldview fit."
    )
    if score >= 1:
        return _pack(
            base
            + f" Here the bands support each other: neither is likely to feel chronically "
            f"looked down on or spiritually mismatched."
        )
    return _pack(
        base
        + " Here the bands differ, so one partner may push harder on status, ritual, "
        "career pride, or “how a household should look,” while the other wants a simpler pace.",
        problem=(
            "Risk of quiet superiority / inferiority feelings, or arguments about lifestyle "
            "standards, family image, and long-term goals."
        ),
        solutions=[
            "Write down three non‑negotiable values each (money, faith, career, family duty) and compare honestly before marriage talks harden.",
            "Agree that respect is equal even if habits differ — no mocking of education, job, or devotion style.",
            "Classical support: Thursday charity (chana / yellow cloth) and a short Guru mantra together once a week to soften ego friction.",
            "If families pressure status, set a united couple boundary early so outsiders cannot widen the gap.",
        ],
    )


def _vashya_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Vashya checks natural influence — who leads, who yields ({detail}). "
        f"It shows whether {a} and {b} can steer each other kindly or get stuck in control battles."
    )
    if score >= 2:
        return _pack(
            base + " Give-and-take looks easy: decisions can move without constant tug-of-war."
        )
    if score >= 1:
        return _pack(
            base
            + " Influence is mixed. Some topics will feel cooperative; others may need extra patience.",
            problem="Occasional power struggles around money, travel, or family decisions.",
            solutions=[
                "Split domains: one leads finances, the other leads home/social — review every 6 months.",
                "Use a simple rule: no big decision in anger; sleep on it, then decide together.",
                "Friday Venus-friendly habits (kind speech, shared pleasant routine) help soft influence.",
            ],
        )
    return _pack(
        base + " Control can feel uneven — one may dominate or the other resist by withdrawing.",
        problem="Chronic “who is the boss?” tension, silent stubbornness, or decisions made unilaterally.",
        solutions=[
            "Make a written decision map (house, money, in-laws, career moves) so power is explicit, not accidental.",
            "Practice “proposal + consent”: one proposes, the other must actively agree — no silent defaults.",
            "Classical support: Saturday seva or sesame charity for Saturn-style patience; cool Mars with Tuesday calm (no harsh speech).",
            "If fights escalate fast, use a counsellor or elder mediator for the first year of major choices.",
        ],
    )


def _tara_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Tara counts birth-star steps from {a} to {b} ({detail}). "
        "It speaks to luck timing, mutual support, and whether efforts feel blessed or blocked together."
    )
    if score >= 3:
        return _pack(
            base + " Supportive Tara: joint plans and day-to-day backing tend to land more smoothly."
        )
    if score >= 1.5:
        return _pack(
            base + " Mixed Tara: some seasons feel easy, some ask for more care — not a solo deal-breaker.",
            problem="Uneven luck windows — projects started together may stall in certain months.",
            solutions=[
                "Avoid forcing marriage dates, house buys, or business launches on rushed timelines; pick muhurta with a Jyotishi.",
                "Keep an emergency fund and shared calendar so “bad star weeks” don’t become money fights.",
                "Monday Moon care (rest, white food, calm night routine) for both partners during stress phases.",
            ],
        )
    return _pack(
        base + " Harder Tara (Vipat / Pratyak / Naidhana class): emotional timing and joint luck can feel off.",
        problem="Higher chance of mistimed decisions, feeling unsupported, or blame when plans fail.",
        solutions=[
            "Do not take major couple risks in haste; double-check health, money, and travel plans together.",
            "Build a weekly check-in: what felt supportive vs lonely — fix small gaps before they grow.",
            "Classical support: chant or listen to a short Moon / Durga stotra on Mondays; keep vows simple and kept.",
            "If marriage is near, ask a Jyotishi for Tara-aware muhurta and whether other strong gunas offset this.",
        ],
    )


def _yoni_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Yoni maps instinctive animal affinity from birth stars ({detail}). "
        f"It relates to private comfort, sexual pace, and how {a} and {b} seek closeness or space."
    )
    if score >= 4:
        return _pack(
            base + " Strong match: physical and instinctive comfort usually feels natural."
        )
    if score >= 2:
        return _pack(
            base + " Workable affinity: chemistry can grow with care; not a classical enemy pair.",
            problem="Desire or affection styles may differ (more touch vs more space).",
            solutions=[
                "Talk preferences early without shame — frequency, privacy, affection in public.",
                "Protect couple time weekly so friendship feeds intimacy.",
                "Friday shared pleasant routine (meal, walk, soft speech) supports Venus harmony.",
            ],
        )
    return _pack(
        base + " Enemy-style yoni: instincts can clash — chase vs withdraw, heat vs coolness.",
        problem="Frustration around intimacy, jealousy, or feeling “mismatched” in private life.",
        solutions=[
            "Treat intimacy as a skill: slow consent, clear asks, no score-keeping insults.",
            "If hurt repeats, seek a couples therapist — do not only rely on silence or pressure.",
            "Classical support: Friday Venus mantra / white sweets charity; avoid harsh red-coral self-prescription without guidance.",
            "Reduce porn/comparison habits that widen the gap; rebuild with shared affection rituals.",
        ],
    )


def _maitri_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Graha Maitri checks friendship between Moon-sign lords ({detail}). "
        f"It shows whether {a} and {b}’s minds naturally cooperate — moods, logic, and problem-solving."
    )
    if score >= 4:
        return _pack(
            base + " Friendly lords: you can usually understand each other’s thinking and repair after stress."
        )
    if score >= 3:
        return _pack(
            base + " Average mental friendship: workable if you stay curious and avoid mind-reading.",
            problem="Occasional misunderstanding when both assume the other “should just get it.”",
            solutions=[
                "Use “I feel / I need” sentences instead of accusations.",
                "Repeat back what you heard before answering in a fight.",
                "Wednesday Mercury habits: journaling, clear texts, no important talks while hungry/tired.",
            ],
        )
    return _pack(
        base + " Tense lords: minds may argue by default; small issues escalate into character attacks.",
        problem="Frequent misunderstandings, sarcasm, or feeling emotionally unread.",
        solutions=[
            "Hard rule: no name-calling; take a 20‑minute pause when volume rises.",
            "Write agreements (chores, money, visiting families) so memory fights drop.",
            "Classical support: Mercury/Jupiter charity (books, green gram, Thursday learning) to cool speech karma.",
            "Consider premarital counselling to learn a shared conflict language.",
        ],
    )


def _gana_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Gana is temperament from birth star — Deva (gentle/ideal), Manushya (practical), "
        f"Rakshasa (intense/direct) ({detail}). It shows default mood chemistry between {a} and {b}."
    )
    if score >= 5:
        return _pack(
            base + " Temperaments fit well — daily mood and pace usually feel familiar."
        )
    if score >= 1:
        return _pack(
            base + " Partial fit: one may want harmony while the other pushes for change or intensity.",
            problem="Different default speeds — rest vs drive, soft speech vs blunt honesty.",
            solutions=[
                "Name your types out loud (“I reset with quiet; you reset with action”) and design weekends accordingly.",
                "Protect sleep and meal timing — temperament clashes worsen with fatigue.",
                "Shared seva once a month softens ego and builds team feeling.",
            ],
        )
    return _pack(
        base + " Classical Deva–Rakshasa stretch: idealism vs intensity can feel like different planets.",
        problem="One feels the other is too soft or too harsh; home peace swings with mood.",
        solutions=[
            "Create house rules for tone: no contempt, no silent treatment longer than 24 hours.",
            "Channel intensity into gym, work, or creative goals — not into the partner.",
            "Classical support: Hanuman Chalisa / Mars-cooling on Tuesdays for harshness; soft Friday speech vows.",
            "If contempt appears early, pause marriage pressure and do structured counselling first.",
        ],
    )


def _bhakoot_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Bhakoot studies Moon-sign distance ({detail}). "
        "Harmonious pairs support love and household mood; 2/12, 5/9, or 6/8 links are classical stress patterns."
    )
    if score >= 7:
        return _pack(
            base
            + f" Harmonious for {a} and {b}: emotional weather usually supports bonding and home building."
        )
    return _pack(
        base
        + " This pair hits a Bhakoot dosha pattern — mood around family, money, or closeness can oscillate.",
        problem=(
            "Higher risk of emotional distance, family interference stress, or money-mood fights "
            "even when love is real."
        ),
        solutions=[
            "Keep finances transparent (shared sheet); money secrecy worsens Bhakoot stress.",
            "Limit triangle fights with in-laws — couple decides first, then informs families.",
            "Daily 10‑minute unplugged talk keeps emotional distance from becoming permanent.",
            "Classical support: Moon remedies (Monday fast/light diet if health allows, pearl only after consult) and a Jyotishi check for Bhakoot exceptions.",
            "Strengthen other life pillars (friendship, shared projects) so one bad mood week does not define the marriage.",
        ],
    )


def _nadi_copy(score: float, detail: str, a: str, b: str) -> Dict[str, Any]:
    base = (
        f"Nadi is the heaviest Ashtakoota factor ({detail}). "
        "Different Nadis are classically preferred for vitality and progeny themes; same Nadi is a major caution."
    )
    if score >= 8:
        return _pack(
            base
            + f" {a} and {b} have different Nadis — classical texts read this as clearer on the health/family axis."
        )
    return _pack(
        base
        + " Same Nadi is present. Traditional matching treats this as the strongest red flag in the 36‑point system.",
        problem=(
            "Classical concern for health stress, hereditary load, or challenges around children — "
            "not a medical diagnosis, but a serious traditional warning."
        ),
        solutions=[
            "Do not ignore this guna: consult a trusted Jyotishi for full D1/D9 review and any classical exceptions (e.g. other strong cancellations).",
            "Get practical medical/genetic counselling if you are planning children — astrology does not replace doctors.",
            "Prioritize sleep, shared health habits, and stress reduction as a couple project.",
            "Classical upaya often cited: Nadi-related charity, temple seva, and mantras under guidance — avoid random gemstone self-prescription.",
            "If families demand a “yes/no,” ask for a second independent chart reading before deciding.",
        ],
    )


_COPY = {
    "varna": _varna_copy,
    "vashya": _vashya_copy,
    "tara": _tara_copy,
    "yoni": _yoni_copy,
    "graha_maitri": _maitri_copy,
    "gana": _gana_copy,
    "bhakoot": _bhakoot_copy,
    "nadi": _nadi_copy,
}


def _verdict_pack(total: float, a: str, b: str, weak_n: int) -> Tuple[str, str, List[str]]:
    overall_solutions: List[str] = [
        "Read every weak guna below — score alone is not enough; the story is in the details.",
        "Decide together: marry / wait / seek deeper chart review — do not let relatives rush a low-clarity match.",
    ]
    if total >= 28:
        verdict, summary = (
            "Excellent match",
            f"{a} and {b} score in a strong classical range ({total:.0f}/36). "
            "Most life areas look supportive. Any weaker gunas are homework, not automatic rejection — "
            "still honour them so small cracks do not grow after marriage.",
        )
        overall_solutions = [
            "Protect the strengths with weekly appreciation and shared rituals.",
            "Still apply solutions listed under any Okay/Weak guna so pride does not skip maintenance.",
        ]
    elif total >= 24:
        verdict, summary = (
            "Very good match",
            f"{a} and {b} sit in a solid range ({total:.0f}/36). "
            "The bond has clear strengths. Focus effort on the weaker gunas so friction stays small.",
        )
    elif total >= 18:
        verdict, summary = (
            "Workable match",
            f"{a} and {b} land mid-range ({total:.0f}/36). Many couples thrive here with maturity. "
            f"There are {weak_n} weak guna(s) — treat those solutions as required conversation, not optional reading.",
        )
        overall_solutions.extend(
            [
                "Do a premarital counselling session focused on the watch-out list.",
                "Revisit this report together after 30 days of honest talks and see what improved.",
            ]
        )
    elif total >= 12:
        verdict, summary = (
            "Needs care",
            f"The score for {a} and {b} is on the lower side ({total:.0f}/36). Love can still be real, "
            f"but {weak_n} weak area(s) ask for patience, practical fixes, and preferably a full Jyotish consult "
            "before locking dates.",
        )
        overall_solutions.extend(
            [
                "Pause irreversible decisions until weak gunas and Manglik notes are addressed.",
                "Book an independent Jyotishi (not only family priest) for D9 and dasha context.",
            ]
        )
    else:
        verdict, summary = (
            "Low compatibility score",
            f"Classically, {a} and {b} score low ({total:.0f}/36). This is guidance, not a verdict on your worth. "
            "Take every weak guna and its solutions seriously; seek a fuller consult if marriage is near.",
        )
        overall_solutions.extend(
            [
                "Do not force muhurta or family pressure over unresolved Nadi/Bhakoot/Manglik issues.",
                "If you still choose each other, commit to counselling + health transparency + slow timelines.",
            ]
        )
    return verdict, summary, overall_solutions


GUNA_SIMPLE = {
    "varna": "In simple words: do your values, pride, and life outlook feel equal?",
    "vashya": "In simple words: can you influence each other kindly, without constant power fights?",
    "tara": "In simple words: do your birth stars support luck and teamwork together?",
    "yoni": "In simple words: do comfort, attraction, and private closeness feel natural?",
    "graha_maitri": "In simple words: do your minds understand each other and repair after stress?",
    "gana": "In simple words: do your basic temperaments (calm, practical, intense) fit day to day?",
    "bhakoot": "In simple words: does emotional weather at home and with family usually feel steady?",
    "nadi": "In simple words: does the traditional health-and-family axis look clear between you?",
}


def _full_overview(
    *,
    a: str,
    b: str,
    total: float,
    verdict: str,
    summary: str,
    a_rashi: str,
    a_nak: str,
    a_pada: int,
    b_rashi: str,
    b_nak: str,
    b_pada: int,
    strengths: List[Dict[str, Any]],
    weak: List[Dict[str, Any]],
    ok_issues: List[Dict[str, Any]],
    manglik_note: str,
    manglik_problem: str | None,
) -> Dict[str, Any]:
    """Plain-language full picture for the Match page."""
    what_it_is = (
        f"Kundali matching (Ashtakoota) compares {a} and {b} using mainly the Moon — "
        "the mind, habits, and emotional comfort of each person. There are eight gunas "
        "(qualities) adding up to 36 points. Think of it as a relationship weather report: "
        "it shows where nature helps, where effort is needed, and what to talk about before marriage. "
        "It does not replace love, character, counselling, or a doctor."
    )

    score_means = (
        f"Their score is {total:g} out of 36 — “{verdict}”. "
        f"{summary} "
        "As a rough guide: 28+ is traditionally excellent, 24–27 very good, 18–23 workable with effort, "
        "below 18 asks for extra care and often a second opinion."
    )

    moons = (
        f"{a}’s Moon sits in {a_rashi}, birth star {a_nak} (pada {a_pada}). "
        f"{b}’s Moon sits in {b_rashi}, birth star {b_nak} (pada {b_pada}). "
        "Almost every guna below is built from these two Moon placements."
    )

    if strengths:
        bits = "; ".join(
            f"{k['title']} scored {k['score']:g}/{k['max']}" for k in strengths
        )
        strong_para = (
            f"What already works in simple words: {bits}. "
            "These areas are natural supports — keep them alive with appreciation and shared habits."
        )
    else:
        strong_para = (
            "No guna landed in the top “strong” band. That does not cancel the match, "
            "but it means daily effort and clear talk matter more than luck."
        )

    if weak:
        bits = "; ".join(
            f"{k['title']} ({k['score']:g}/{k['max']})"
            + (f" — {k['problem']}" if k.get("problem") else "")
            for k in weak
        )
        weak_para = (
            f"Where the chart asks for care: {bits}. "
            "Each of these has practical solutions further down — treat them as a to-do list, not a scare list."
        )
    else:
        weak_para = (
            "No guna scored in the weak band. Still skim any “Okay” sections so small gaps do not grow later."
        )

    if ok_issues:
        mid = "; ".join(k["title"] for k in ok_issues)
        mid_para = (
            f"Mixed / okay areas that still deserve a talk: {mid}. "
            "They are not disasters, but small habits here prevent bigger fights."
        )
    else:
        mid_para = ""

    manglik_para = f"Separate Mars (Manglik) check: {manglik_note}"
    if manglik_problem:
        manglik_para += f" Issue in plain words: {manglik_problem}"

    bottom = (
        f"Bottom line for {a} and {b}: read the full picture — score, strengths, watch-outs, Manglik — "
        "then use the solutions. Strong gunas are gifts; weak gunas are homework. "
        "If Nadi or Bhakoot is weak, or the total is low, pause wedding pressure and get a fuller Jyotish consult."
    )

    paragraphs = [
        what_it_is,
        score_means,
        moons,
        strong_para,
        weak_para,
    ]
    if mid_para:
        paragraphs.append(mid_para)
    paragraphs.extend([manglik_para, bottom])

    guide = [
        {"id": kid, "title": title, "simple": GUNA_SIMPLE[kid]}
        for kid, title in (
            ("varna", "Values & outlook"),
            ("vashya", "Influence & give-and-take"),
            ("tara", "Timing & mutual support"),
            ("yoni", "Comfort & intimacy"),
            ("graha_maitri", "Mental friendship"),
            ("gana", "Temperament fit"),
            ("bhakoot", "Emotional harmony"),
            ("nadi", "Health & family axis"),
        )
    ]

    return {"paragraphs": paragraphs, "guna_guide": guide}

def _manglik_pack(
    mang_a: bool,
    mang_b: bool,
    detail_a: str,
    detail_b: str,
    a: str,
    b: str,
) -> Tuple[str, str, str | None, List[str]]:
    """title, one-line note, problem|None, solutions."""
    if mang_a and mang_b:
        return (
            "Both show Manglik",
            f"Both Manglik — often treated as balancing ({a}: {detail_a}; {b}: {detail_b}).",
            "Energy and courage can run high; temper and haste may spike in early marriage years if untrained.",
            [
                "Promise a “cool-down” rule: no final decisions during anger; walk first.",
                "Channel Mars into sport, disciplined work, or service — not into winning every argument.",
                "Classical support often cited: Hanuman Chalisa on Tuesdays, masoor/jaggery charity, "
                "and red coral only after a qualified Jyotishi checks the full chart.",
                "Delay impulsive wedding logistics; pick muhurta with Mars dignity in mind.",
            ],
        )
    if not mang_a and not mang_b:
        return (
            "No Manglik flag",
            f"Neither {a} nor {b} is Manglik on the classic Mars houses.",
            None,
            [],
        )
    who = a if mang_a else b
    det = detail_a if mang_a else detail_b
    other = b if mang_a else a
    return (
        "Manglik on one side",
        f"Only {who} is Manglik ({det}); {other} is not.",
        "Traditional concern for friction, delay, or temper imbalance — not an automatic ban.",
        [
            f"Discuss openly: how {who} handles anger and haste, and how {other} needs safety.",
            "Ask a Jyotishi whether Venus/Jupiter placements cancel or soften Manglik for this chart.",
            "Classical upaya often used: Kumbh vivah / symbolic Mars pacification only under guidance; "
            "Tuesday Hanuman practice; avoid self-prescribing strong Mars gems.",
            "Prefer a slightly later, calmer wedding timeline if families agree — haste worsens Mars stories.",
            "Premarital counselling on conflict styles is practical medicine alongside any ritual.",
        ],
    )


def match_charts(person_a: KundliChart, person_b: KundliChart) -> Dict[str, Any]:
    """
    Ashtakoota from Moon. Person A = bride-side, Person B = groom-side
    for Varna / Tara / Vashya orientation (classical convention).
    """
    a_nak, a_nak_name, a_ri, a_rashi = _moon(person_a)
    b_nak, b_nak_name, b_ri, b_rashi = _moon(person_b)
    a_name = person_a.birth.name
    b_name = person_b.birth.name

    scored: List[Tuple[str, str, float, Tuple[float, str]]] = [
        ("varna", "Varna", 1, _varna(a_rashi, b_rashi)),
        ("vashya", "Vashya", 2, _vashya(a_rashi, b_rashi)),
        ("tara", "Tara", 3, _tara(a_nak, b_nak)),
        ("yoni", "Yoni", 4, _yoni(a_nak, b_nak)),
        ("graha_maitri", "Graha Maitri", 5, _graha_maitri(a_rashi, b_rashi)),
        ("gana", "Gana", 6, _gana(a_nak, b_nak)),
        ("bhakoot", "Bhakoot", 7, _bhakoot(a_ri, b_ri)),
        ("nadi", "Nadi", 8, _nadi(a_nak, b_nak)),
    ]

    titles = {
        "varna": "Values & outlook",
        "vashya": "Influence & give-and-take",
        "tara": "Timing & mutual support",
        "yoni": "Comfort & intimacy",
        "graha_maitri": "Mental friendship",
        "gana": "Temperament fit",
        "bhakoot": "Emotional harmony",
        "nadi": "Health & family axis",
    }

    kootas: List[Dict[str, Any]] = []
    for kid, name, max_pts, (score, detail) in scored:
        level = _level(score, max_pts)
        copy = _COPY[kid](score, detail, a_name, b_name)
        kootas.append(
            {
                "id": kid,
                "name": name,
                "title": titles[kid],
                "max": max_pts,
                "score": score,
                "level": level,
                "detail": detail,
                "simple": GUNA_SIMPLE[kid],
                "explanation": copy["explanation"],
                "problem": copy.get("problem"),
                "solutions": copy.get("solutions") or [],
            }
        )

    total = sum(float(k["score"]) for k in kootas)
    max_total = 36.0
    weak = [k for k in kootas if k["level"] == "weak"]
    ok_issues = [k for k in kootas if k["level"] == "ok" and k.get("problem")]
    strengths = [k for k in kootas if k["level"] == "strong"]

    verdict, summary, overall_solutions = _verdict_pack(total, a_name, b_name, len(weak))

    mang_a, mang_a_d = _manglik(person_a)
    mang_b, mang_b_d = _manglik(person_b)
    manglik_title, manglik_note, manglik_problem, manglik_solutions = _manglik_pack(
        mang_a, mang_b, mang_a_d, mang_b_d, a_name, b_name
    )

    overview = _full_overview(
        a=a_name,
        b=b_name,
        total=total,
        verdict=verdict,
        summary=summary,
        a_rashi=a_rashi,
        a_nak=a_nak_name,
        a_pada=person_a.moon_pada,
        b_rashi=b_rashi,
        b_nak=b_nak_name,
        b_pada=person_b.moon_pada,
        strengths=strengths,
        weak=weak,
        ok_issues=ok_issues,
        manglik_note=manglik_note,
        manglik_problem=manglik_problem,
    )

    action_plan: List[str] = list(overall_solutions)
    for k in weak + ok_issues:
        for sol in k["solutions"][:2]:
            if sol not in action_plan:
                action_plan.append(sol)
    for sol in manglik_solutions[:2]:
        if sol not in action_plan:
            action_plan.append(sol)

    return {
        "version": "ashtakoota-v4",
        "total": total,
        "max": max_total,
        "verdict": verdict,
        "summary": summary,
        "overview": overview["paragraphs"],
        "guna_guide": overview["guna_guide"],
        "action_plan": action_plan[:8],
        "strengths": [
            {"name": k["name"], "title": k["title"], "score": k["score"], "max": k["max"]}
            for k in strengths
        ],
        "watchouts": [
            {
                "name": k["name"],
                "title": k["title"],
                "score": k["score"],
                "max": k["max"],
                "problem": k.get("problem"),
            }
            for k in weak
        ],
        "kootas": kootas,
        "person_a": {
            "name": a_name,
            "moon_rashi": a_rashi,
            "moon_nakshatra": a_nak_name,
            "moon_pada": person_a.moon_pada,
            "manglik": mang_a,
            "manglik_detail": mang_a_d,
        },
        "person_b": {
            "name": b_name,
            "moon_rashi": b_rashi,
            "moon_nakshatra": b_nak_name,
            "moon_pada": person_b.moon_pada,
            "manglik": mang_b,
            "manglik_detail": mang_b_d,
        },
        "manglik_title": manglik_title,
        "manglik_note": manglik_note,
        "manglik_problem": manglik_problem,
        "manglik_solutions": manglik_solutions,
        "convention": "",
    }
