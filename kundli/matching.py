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


def _explain_varna(score: float, detail: str, a: str, b: str) -> str:
    if score >= 1:
        return (
            f"{a} and {b} sit in compatible life-outlook bands ({detail}). "
            "Ego and values usually line up without one person feeling looked down on."
        )
    return (
        f"Outlook bands differ ({detail}). One partner may expect more status or "
        "spiritual seriousness than the other — talk early about lifestyle and goals."
    )


def _explain_vashya(score: float, detail: str, a: str, b: str) -> str:
    if score >= 2:
        return (
            f"Natural give-and-take looks smooth ({detail}). "
            f"{a} and {b} can influence each other without constant power struggles."
        )
    if score >= 1:
        return (
            f"Influence is mixed ({detail}). Some days one leads easily; other days "
            "you may need extra patience around decisions."
        )
    return (
        f"Control dynamics can feel uneven ({detail}). "
        "Agree who decides what, so small issues do not turn into tug-of-war."
    )


def _explain_tara(score: float, detail: str, a: str, b: str) -> str:
    if score >= 3:
        return (
            f"Birth-star timing is supportive ({detail}). "
            f"Day-to-day luck and mutual support between {a} and {b} tend to flow better."
        )
    if score >= 1.5:
        return (
            f"Birth-star link is mixed ({detail}). "
            "Some phases feel easy, some need more care — not a deal-breaker on its own."
        )
    return (
        f"Birth-star count is a harder Tara ({detail}). "
        "Plan big moves together carefully; emotional timing may feel off more often."
    )


def _explain_yoni(score: float, detail: str, a: str, b: str) -> str:
    if score >= 4:
        return (
            f"Instinct and intimacy style match closely ({detail}). "
            f"Physical comfort and private chemistry between {a} and {b} usually feel natural."
        )
    if score >= 2:
        return (
            f"Intimate style is workable ({detail}). "
            "Attraction can grow with care; neither is a natural enemy pattern."
        )
    return (
        f"Instinct styles clash ({detail}). "
        "You may need more conscious effort around closeness, space, and sexual comfort."
    )


def _explain_maitri(score: float, detail: str, a: str, b: str) -> str:
    if score >= 4:
        return (
            f"Mind-sign rulers are friendly ({detail}). "
            f"{a} and {b} can understand each other’s moods and think as a team."
        )
    if score >= 3:
        return (
            f"Mental friendship is average ({detail}). "
            "Communication works if you stay curious and avoid assuming the worst."
        )
    return (
        f"Mind-sign rulers are tense ({detail}). "
        "Misunderstandings may come faster — slow down arguments and clarify feelings."
    )


def _explain_gana(score: float, detail: str, a: str, b: str) -> str:
    if score >= 5:
        return (
            f"Temperaments fit well ({detail}). "
            f"Basic nature — calm, practical, or intense — sits comfortably between {a} and {b}."
        )
    if score >= 1:
        return (
            f"Temperaments are only partly aligned ({detail}). "
            "One may want peace while the other pushes harder — name the difference early."
        )
    return (
        f"Temperaments pull in opposite directions ({detail}). "
        "Expect different default moods; shared routines and respect matter a lot here."
    )


def _explain_bhakoot(score: float, detail: str, a: str, b: str) -> str:
    if score >= 7:
        return (
            f"Moon-sign pair is harmonious ({detail}). "
            f"Emotional weather between {a} and {b} tends to support love and home life."
        )
    return (
        f"Moon signs form a classical Bhakoot stress pair ({detail}). "
        "Family, money mood, or emotional distance can flare — stay honest about needs."
    )


def _explain_nadi(score: float, detail: str, a: str, b: str) -> str:
    if score >= 8:
        return (
            f"Health–family axis is clear ({detail}). "
            "Classical texts see different Nadis as better for vitality and children themes."
        )
    return (
        f"Same Nadi shows here ({detail}). "
        "Traditional matching treats this as the heaviest caution — discuss health, "
        "family planning, and get a second opinion from a trusted Jyotishi if needed."
    )


def _verdict_pack(total: float, a: str, b: str) -> Tuple[str, str]:
    if total >= 28:
        return (
            "Excellent match",
            f"{a} and {b} score in a strong classical range. Most life areas look supportive; "
            "use the weaker gunas below as gentle homework, not red flags.",
        )
    if total >= 24:
        return (
            "Very good match",
            f"{a} and {b} sit in a solid range. The bond has clear strengths; "
            "pay attention to any weak gunas so small frictions do not pile up.",
        )
    if total >= 18:
        return (
            "Workable match",
            f"{a} and {b} land in a middle range — many couples live well here with effort. "
            "Read the weak points carefully and talk them through before big decisions.",
        )
    if total >= 12:
        return (
            "Needs care",
            f"The score for {a} and {b} is on the lower side. Strengths still exist, "
            "but several areas ask for patience, counseling, or a deeper chart review.",
        )
    return (
        "Low compatibility score",
        f"Classically, {a} and {b} score low on Ashtakoota. This is guidance, not a verdict "
        "on love — still, take the weak gunas seriously and seek a fuller consult if marriage is near.",
    )


def _manglik_pack(
    mang_a: bool,
    mang_b: bool,
    detail_a: str,
    detail_b: str,
    a: str,
    b: str,
) -> Tuple[str, str]:
    """title, explanation."""
    if mang_a and mang_b:
        return (
            "Both show Manglik",
            f"{a} ({detail_a}) and {b} ({detail_b}) both have Mars in a Manglik house. "
            "Many traditions treat two Manglik partners as balancing each other. "
            "Still watch temper and haste in the early years of marriage.",
        )
    if not mang_a and not mang_b:
        return (
            "No Manglik flag",
            f"Neither {a} nor {b} has Mars in the classic Manglik houses (1, 4, 7, 8, or 12). "
            "This separate check looks clear alongside the 36-point score.",
        )
    who = a if mang_a else b
    det = detail_a if mang_a else detail_b
    other = b if mang_a else a
    return (
        "Manglik on one side",
        f"{who} shows Manglik ({det}); {other} does not. "
        "Older matching often asks for extra care, remedies, or delayed marriage timing. "
        "Treat this as a conversation point, not an automatic no.",
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

    raw: List[Tuple[str, str, float, Tuple[float, str], Any]] = [
        ("varna", "Varna", 1, _varna(a_rashi, b_rashi), _explain_varna),
        ("vashya", "Vashya", 2, _vashya(a_rashi, b_rashi), _explain_vashya),
        ("tara", "Tara", 3, _tara(a_nak, b_nak), _explain_tara),
        ("yoni", "Yoni", 4, _yoni(a_nak, b_nak), _explain_yoni),
        ("graha_maitri", "Graha Maitri", 5, _graha_maitri(a_rashi, b_rashi), _explain_maitri),
        ("gana", "Gana", 6, _gana(a_nak, b_nak), _explain_gana),
        ("bhakoot", "Bhakoot", 7, _bhakoot(a_ri, b_ri), _explain_bhakoot),
        ("nadi", "Nadi", 8, _nadi(a_nak, b_nak), _explain_nadi),
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
    for kid, name, max_pts, (score, detail), explainer in raw:
        level = _level(score, max_pts)
        kootas.append(
            {
                "id": kid,
                "name": name,
                "title": titles[kid],
                "max": max_pts,
                "score": score,
                "level": level,
                "detail": detail,
                "explanation": explainer(score, detail, a_name, b_name),
            }
        )

    total = sum(float(k["score"]) for k in kootas)
    max_total = 36.0
    verdict, summary = _verdict_pack(total, a_name, b_name)

    strengths = [k for k in kootas if k["level"] == "strong"]
    watch = [k for k in kootas if k["level"] == "weak"]

    mang_a, mang_a_d = _manglik(person_a)
    mang_b, mang_b_d = _manglik(person_b)
    manglik_title, manglik_note = _manglik_pack(
        mang_a, mang_b, mang_a_d, mang_b_d, a_name, b_name
    )

    # Keep old field for any cached clients
    manglik_note_short = manglik_note

    return {
        "version": "ashtakoota-v2",
        "total": total,
        "max": max_total,
        "verdict": verdict,
        "summary": summary,
        "strengths": [
            {"name": k["name"], "title": k["title"], "score": k["score"], "max": k["max"]}
            for k in strengths
        ],
        "watchouts": [
            {"name": k["name"], "title": k["title"], "score": k["score"], "max": k["max"]}
            for k in watch
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
        "manglik_note": manglik_note_short,
        "convention": (
            f"Person A ({a_name}) is read as bride-side and Person B ({b_name}) as groom-side "
            "for classical Varna, Vashya, and Tara rules. Score is educational guidance — "
            "not a medical, legal, or destiny decree."
        ),
    }
