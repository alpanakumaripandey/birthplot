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


def _verdict(total: float) -> str:
    if total >= 28:
        return "Excellent"
    if total >= 24:
        return "Very good"
    if total >= 18:
        return "Acceptable"
    if total >= 12:
        return "Needs care"
    return "Low"


def match_charts(person_a: KundliChart, person_b: KundliChart) -> Dict[str, Any]:
    """
    Ashtakoota from Moon. Person A = bride-side, Person B = groom-side
    for Varna / Tara / Vashya orientation (classical convention).
    """
    a_nak, a_nak_name, a_ri, a_rashi = _moon(person_a)
    b_nak, b_nak_name, b_ri, b_rashi = _moon(person_b)

    kootas: List[Dict[str, Any]] = []

    def add(name: str, max_pts: float, fn_result: Tuple[float, str], blurb: str) -> None:
        score, detail = fn_result
        kootas.append(
            {
                "id": name.lower().replace(" ", "_"),
                "name": name,
                "max": max_pts,
                "score": score,
                "detail": detail,
                "note": blurb,
            }
        )

    add("Varna", 1, _varna(a_rashi, b_rashi), "Spiritual / ego temperament class from Moon sign.")
    add("Vashya", 2, _vashya(a_rashi, b_rashi), "Mutual influence and natural control dynamic.")
    add("Tara", 3, _tara(a_nak, b_nak), "Birth-star compatibility counted A → B.")
    add("Yoni", 4, _yoni(a_nak, b_nak), "Intimate / instinctive animal affinity.")
    add("Graha Maitri", 5, _graha_maitri(a_rashi, b_rashi), "Moon-sign lords' friendship.")
    add("Gana", 6, _gana(a_nak, b_nak), "Temperament: Deva / Manushya / Rakshasa.")
    add("Bhakoot", 7, _bhakoot(a_ri, b_ri), "Moon-sign pair harmony (2/12, 5/9, 6/8 checked).")
    add("Nadi", 8, _nadi(a_nak, b_nak), "Health / progeny axis — same Nadi is a dosha.")

    total = sum(float(k["score"]) for k in kootas)
    max_total = 36.0

    mang_a, mang_a_d = _manglik(person_a)
    mang_b, mang_b_d = _manglik(person_b)
    if mang_a == mang_b:
        manglik_note = (
            "Both Manglik — often considered balancing."
            if mang_a
            else "Neither Manglik."
        )
    else:
        manglik_note = (
            f"Manglik mismatch — A: {'yes' if mang_a else 'no'} ({mang_a_d}); "
            f"B: {'yes' if mang_b else 'no'} ({mang_b_d})."
        )

    return {
        "version": "ashtakoota-v1",
        "total": total,
        "max": max_total,
        "verdict": _verdict(total),
        "kootas": kootas,
        "person_a": {
            "name": person_a.birth.name,
            "moon_rashi": a_rashi,
            "moon_nakshatra": a_nak_name,
            "moon_pada": person_a.moon_pada,
            "manglik": mang_a,
            "manglik_detail": mang_a_d,
        },
        "person_b": {
            "name": person_b.birth.name,
            "moon_rashi": b_rashi,
            "moon_nakshatra": b_nak_name,
            "moon_pada": person_b.moon_pada,
            "manglik": mang_b,
            "manglik_detail": mang_b_d,
        },
        "manglik_note": manglik_note,
        "convention": "Ashtakoota treats Person A as bride-side and Person B as groom-side for Varna, Vashya, and Tara.",
    }
