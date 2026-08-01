"""Basic classical yoga detection for beginner-friendly reports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from kundli.chart import KundliChart


@dataclass
class YogaResult:
    name: str
    present: bool
    detail: str
    meaning: str
    kind: str = "classical"  # "classical" | "note"


def detect_yogas(chart: KundliChart) -> List[YogaResult]:
    results: List[YogaResult] = []
    p = chart.planets

    # Budhaditya: Sun + Mercury same house/sign
    same_sun_merc = p["Sun"].house == p["Mercury"].house
    results.append(
        YogaResult(
            name="Budhaditya Yoga",
            present=same_sun_merc,
            detail=(
                f"Sun and Mercury together in house {p['Sun'].house} ({p['Sun'].info.rashi_name})."
                if same_sun_merc
                else "Sun and Mercury are not together."
            ),
            meaning="Often linked with sharp intellect, articulate speech, and learning ability.",
            kind="classical",
        )
    )

    # Gaja Kesari: Jupiter in kendra from Moon (1,4,7,10)
    moon_h = p["Moon"].house
    jup_h = p["Jupiter"].house
    from_moon = ((jup_h - moon_h) % 12) + 1
    gaja = from_moon in (1, 4, 7, 10)
    results.append(
        YogaResult(
            name="Gaja Kesari Yoga",
            present=gaja,
            detail=(
                f"Jupiter is in the {from_moon}th from Moon (house {jup_h} from Lagna)."
                if gaja
                else f"Jupiter is in the {from_moon}th from Moon - not a kendra."
            ),
            meaning="Classically associated with reputation, wisdom, and respectable standing.",
            kind="classical",
        )
    )

    # Chandra-Mangala: Moon + Mars together
    chandra_mangala = p["Moon"].house == p["Mars"].house
    results.append(
        YogaResult(
            name="Chandra-Mangala Yoga",
            present=chandra_mangala,
            detail=(
                f"Moon and Mars share house {p['Moon'].house}."
                if chandra_mangala
                else "Moon and Mars are separate."
            ),
            meaning="Can indicate drive in earning and a forceful emotional/working style.",
            kind="classical",
        )
    )

    # Raja yoga hint: lords of kendras/trikonas together (simplified: benefics in kendras)
    kendra_houses = {1, 4, 7, 10}
    trikona = {1, 5, 9}
    benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
    benefics_in_kendra = [b for b in benefics if p[b].house in kendra_houses]
    results.append(
        YogaResult(
            name="Benefics in Kendras",
            present=len(benefics_in_kendra) >= 2,
            detail=(
                f"Benefics in angular houses: {', '.join(benefics_in_kendra) or 'none'}."
            ),
            meaning="Supportive planets in angles often ease life direction, home, partnership, and career pillars.",
            kind="note",
        )
    )

    # Viparita Raja hint: planets in dusthanas
    dusthana = {6, 8, 12}
    in_dusthana = [name for name, pl in p.items() if pl.house in dusthana]
    results.append(
        YogaResult(
            name="Planets in Dusthanas (6/8/12)",
            present=len(in_dusthana) >= 2,
            detail=f"In 6/8/12: {', '.join(in_dusthana) or 'none'}.",
            meaning="Not always negative - can show growth through service, research, or letting go; context matters.",
            kind="note",
        )
    )

    # Kemadruma (simplified)
    neighbors = set()
    for name, pl in p.items():
        if name in ("Moon", "Sun"):
            continue
        rel = ((pl.house - moon_h) % 12) + 1
        if rel in (2, 12):
            neighbors.add(name)
    with_moon = [n for n, pl in p.items() if n != "Moon" and pl.house == moon_h]
    kemadruma = len(neighbors) == 0 and len(with_moon) == 0
    results.append(
        YogaResult(
            name="Kemadruma Yoga (simplified)",
            present=kemadruma,
            detail=(
                "Moon has no companions and no planets in 2nd/12th from it."
                if kemadruma
                else f"Moon support nearby: with={with_moon or 'none'}, 2nd/12th={sorted(neighbors) or 'none'}."
            ),
            meaning="If present, classical texts warn of mental loneliness; many cancellations exist - take lightly.",
            kind="classical",
        )
    )

    in_trikona = [n for n, pl in p.items() if pl.house in trikona]
    results.append(
        YogaResult(
            name="Planets in Trikonas (1/5/9)",
            present=len(in_trikona) >= 2,
            detail=f"In dharma trikonas: {', '.join(in_trikona) or 'none'}.",
            meaning="Activity in 1/5/9 often highlights purpose, creativity, and fortune themes.",
            kind="note",
        )
    )

    return results
