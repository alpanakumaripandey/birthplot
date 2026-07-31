"""Vimshottari dasha (mahadasha / antardasha) from Moon nakshatra."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from kundli.chart import KundliChart
from kundli.ephemeris import NAKSHATRA_SPAN

# Order of Vimshottari lords starting from Ashwini (Ketu)
DASHA_ORDER = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
]

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

TOTAL_YEARS = 120
DAYS_PER_YEAR = 365.2425  # tropical-ish year length for dasha spans


@dataclass
class DashaPeriod:
    lord: str
    start: datetime
    end: datetime
    level: str  # "mahadasha" | "antardasha"

    @property
    def years(self) -> float:
        return (self.end - self.start).total_seconds() / (DAYS_PER_YEAR * 86400)


@dataclass
class DashaTimeline:
    balance_at_birth: dict  # lord, years_remaining
    mahadashas: List[DashaPeriod]
    current_mahadasha: Optional[DashaPeriod]
    current_antardasha: Optional[DashaPeriod]
    antardashas_in_current: List[DashaPeriod]


def _nakshatra_lord(nakshatra_index: int) -> str:
    """Nakshatra 1-27 → dasha lord (Ashwini=Ketu, cycles every 9)."""
    return DASHA_ORDER[(nakshatra_index - 1) % 9]


def _elapsed_in_nakshatra(moon_longitude: float) -> float:
    """Fraction 0-1 of Moon's progress through its current nakshatra."""
    return (moon_longitude % NAKSHATRA_SPAN) / NAKSHATRA_SPAN


def _add_years(dt: datetime, years: float) -> datetime:
    return dt + timedelta(days=years * DAYS_PER_YEAR)


def compute_vimshottari(chart: KundliChart, as_of: Optional[datetime] = None) -> DashaTimeline:
    """Compute mahadasha timeline and current antardasha."""
    moon = chart.planets["Moon"].info
    birth = chart.local_dt
    as_of = as_of or datetime.now(tz=birth.tzinfo)

    start_lord = _nakshatra_lord(moon.nakshatra_index)
    elapsed_frac = _elapsed_in_nakshatra(moon.longitude)
    full_years = DASHA_YEARS[start_lord]
    balance_years = full_years * (1.0 - elapsed_frac)

    # Build mahadasha sequence from birth
    mahas: List[DashaPeriod] = []
    cursor = birth
    lord_idx = DASHA_ORDER.index(start_lord)

    # First (partial) mahadasha
    first_end = _add_years(cursor, balance_years)
    mahas.append(DashaPeriod(start_lord, cursor, first_end, "mahadasha"))
    cursor = first_end

    # Full cycles until we cover ~120 years from birth
    covered = balance_years
    lord_idx = (lord_idx + 1) % 9
    while covered < TOTAL_YEARS + 5:
        lord = DASHA_ORDER[lord_idx]
        yrs = DASHA_YEARS[lord]
        end = _add_years(cursor, yrs)
        mahas.append(DashaPeriod(lord, cursor, end, "mahadasha"))
        cursor = end
        covered += yrs
        lord_idx = (lord_idx + 1) % 9

    current_maha = None
    for m in mahas:
        if m.start <= as_of < m.end:
            current_maha = m
            break
    if current_maha is None and mahas:
        # After last period or before first
        if as_of < mahas[0].start:
            current_maha = mahas[0]
        else:
            current_maha = mahas[-1]

    antars: List[DashaPeriod] = []
    current_antar = None
    if current_maha:
        antars = _antardashas(current_maha)
        for a in antars:
            if a.start <= as_of < a.end:
                current_antar = a
                break
        if current_antar is None and antars:
            current_antar = antars[-1] if as_of >= antars[-1].start else antars[0]

    return DashaTimeline(
        balance_at_birth={
            "lord": start_lord,
            "years_remaining": round(balance_years, 4),
            "full_years": full_years,
        },
        mahadashas=mahas[:12],  # first full cycle-ish for display
        current_mahadasha=current_maha,
        current_antardasha=current_antar,
        antardashas_in_current=antars,
    )


def _antardashas(maha: DashaPeriod) -> List[DashaPeriod]:
    """Antardashas within a mahadasha: each sub = maha_years * sub_years / 120."""
    maha_years = DASHA_YEARS[maha.lord]
    # For partial first dasha, scale by actual duration
    actual_years = (maha.end - maha.start).total_seconds() / (DAYS_PER_YEAR * 86400)
    scale = actual_years / maha_years if maha_years else 1.0

    start_idx = DASHA_ORDER.index(maha.lord)
    periods: List[DashaPeriod] = []
    cursor = maha.start
    for i in range(9):
        sub_lord = DASHA_ORDER[(start_idx + i) % 9]
        sub_years = (maha_years * DASHA_YEARS[sub_lord] / TOTAL_YEARS) * scale
        end = _add_years(cursor, sub_years)
        # Clamp last to maha.end for floating point
        if i == 8:
            end = maha.end
        periods.append(DashaPeriod(sub_lord, cursor, end, "antardasha"))
        cursor = end
    return periods
