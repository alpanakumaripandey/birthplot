"""Planetary positions via Skyfield + Lahiri (Chitrapaksha) ayanamsa.

Uses JPL ephemeris (de421) for tropical longitudes, then converts to sidereal.
No native C extension required (works on Windows / Python 3.13 without MSVC).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Dict

from skyfield.api import Loader
from skyfield.framelib import ecliptic_frame

# Ephemeris cache beside the package (downloaded once)
_EPHEMERIS_DIR = Path(__file__).resolve().parent / ".ephemeris"
_EPHEMERIS_DIR.mkdir(parents=True, exist_ok=True)

RASHI_NAMES = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

NAKSHATRA_NAMES = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

NAKSHATRA_SPAN = 360.0 / 27.0  # 13°20'
PADA_SPAN = NAKSHATRA_SPAN / 4.0

# Skyfield body names for classical grahas
_PLANET_BODIES = {
    "Sun": "sun",
    "Moon": "moon",
    "Mercury": "mercury",
    "Venus": "venus",
    "Mars": "mars",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
}


@dataclass(frozen=True)
class LongitudeInfo:
    longitude: float
    rashi_index: int  # 1-12
    rashi_name: str
    degree_in_rashi: float
    nakshatra_index: int  # 1-27
    nakshatra_name: str
    pada: int  # 1-4
    retrograde: bool = False


def normalize_longitude(lon: float) -> float:
    return lon % 360.0


def datetime_to_julian_day(dt_utc: datetime) -> float:
    """Convert timezone-aware datetime to Julian Day (UT)."""
    if dt_utc.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    utc = dt_utc.astimezone(timezone.utc)
    # Skyfield timescale for consistent JD
    ts = _timescale()
    t = ts.utc(
        utc.year,
        utc.month,
        utc.day,
        utc.hour,
        utc.minute,
        utc.second + utc.microsecond / 1e6,
    )
    return float(t.ut1)


def lahiri_ayanamsa(jd_ut: float) -> float:
    """Lahiri (Chitrapaksha) ayanamsa in degrees (Indian Astronomical Ephemeris approx)."""
    t = (jd_ut - 2451545.0) / 36525.0
    return 23.85306 + 1.39722 * t + 0.00018 * t * t - 0.000005 * t * t * t


def longitude_info(longitude: float, retrograde: bool = False) -> LongitudeInfo:
    lon = normalize_longitude(longitude)
    rashi_index = int(lon // 30) + 1
    degree_in_rashi = lon % 30.0
    nak_index0 = int(lon // NAKSHATRA_SPAN)
    pada = int((lon % NAKSHATRA_SPAN) // PADA_SPAN) + 1
    return LongitudeInfo(
        longitude=lon,
        rashi_index=rashi_index,
        rashi_name=RASHI_NAMES[rashi_index - 1],
        degree_in_rashi=degree_in_rashi,
        nakshatra_index=nak_index0 + 1,
        nakshatra_name=NAKSHATRA_NAMES[nak_index0],
        pada=pada,
        retrograde=retrograde,
    )


@lru_cache(maxsize=1)
def _loader() -> Loader:
    return Loader(str(_EPHEMERIS_DIR))


@lru_cache(maxsize=1)
def _timescale():
    return _loader().timescale()


@lru_cache(maxsize=1)
def _ephemeris():
    load = _loader()
    return load("de421.bsp")


def _skyfield_time(dt_utc: datetime):
    utc = dt_utc.astimezone(timezone.utc)
    ts = _timescale()
    return ts.utc(
        utc.year,
        utc.month,
        utc.day,
        utc.hour,
        utc.minute,
        utc.second + utc.microsecond / 1e6,
    )


def _tropical_ecliptic_lon(body, t) -> float:
    """Geocentric tropical ecliptic longitude in degrees."""
    earth = _ephemeris()["earth"]
    astrometric = earth.at(t).observe(body)
    lat, lon, _ = astrometric.frame_latlon(ecliptic_frame)
    return normalize_longitude(lon.degrees)


def _ecliptic_lon_speed(body, t) -> tuple[float, float]:
    """Longitude and approx daily speed (deg/day) via finite difference."""
    lon0 = _tropical_ecliptic_lon(body, t)
    # +1 hour
    t2 = _timescale().ut1_jd(t.ut1 + 1.0 / 24.0)
    lon1 = _tropical_ecliptic_lon(body, t2)
    delta = (lon1 - lon0 + 180) % 360 - 180
    speed_per_day = delta * 24.0
    return lon0, speed_per_day


def mean_lunar_node_longitude(jd_ut: float) -> float:
    """Mean ascending node (Rahu) tropical longitude — Meeus-style approximation."""
    t = (jd_ut - 2451545.0) / 36525.0
    # Mean longitude of ascending node (degrees)
    omega = 125.04452 - 1934.136261 * t + 0.0020708 * t * t + t * t * t / 450000.0
    return normalize_longitude(omega)


def obliquity_of_ecliptic(jd_ut: float) -> float:
    """Mean obliquity of the ecliptic in degrees (IAU-ish)."""
    t = (jd_ut - 2451545.0) / 36525.0
    eps = (
        23.439291
        - 0.0130042 * t
        - 0.00000016 * t * t
        + 0.000000504 * t * t * t
    )
    return eps


def tropical_ascendant(jd_ut: float, lat: float, lon: float) -> float:
    """Tropical ascendant longitude (degrees) for lat/lon at JD UT."""
    # Greenwich mean sidereal time (hours) — Meeus
    t = (jd_ut - 2451545.0) / 36525.0
    gmst_deg = (
        280.46061837
        + 360.98564736629 * (jd_ut - 2451545.0)
        + 0.000387933 * t * t
        - t * t * t / 38710000.0
    )
    lst_deg = normalize_longitude(gmst_deg + lon)
    ramc = math.radians(lst_deg)
    phi = math.radians(lat)
    eps = math.radians(obliquity_of_ecliptic(jd_ut))

    # Ascendant formula
    y = -math.cos(ramc)
    x = math.sin(ramc) * math.cos(eps) + math.tan(phi) * math.sin(eps)
    asc = math.degrees(math.atan2(y, x))
    return normalize_longitude(asc)


def ascendant_longitude(jd_ut: float, lat: float, lon: float) -> float:
    """Sidereal (Lahiri) ascendant longitude."""
    tropical = tropical_ascendant(jd_ut, lat, lon)
    return normalize_longitude(tropical - lahiri_ayanamsa(jd_ut))


def all_planet_longitudes(jd_ut: float) -> Dict[str, LongitudeInfo]:
    """Sidereal longitudes for Sun–Saturn, Rahu, Ketu."""
    eph = _ephemeris()
    ts = _timescale()
    t = ts.ut1_jd(jd_ut)
    ayan = lahiri_ayanamsa(jd_ut)

    positions: Dict[str, LongitudeInfo] = {}
    for name, key in _PLANET_BODIES.items():
        body = eph[key]
        trop, speed = _ecliptic_lon_speed(body, t)
        sid = normalize_longitude(trop - ayan)
        positions[name] = longitude_info(sid, retrograde=speed < 0)

    # Rahu = mean node (mean node is retrograde by nature in tropical; mark R)
    rahu_trop = mean_lunar_node_longitude(jd_ut)
    rahu_sid = normalize_longitude(rahu_trop - ayan)
    positions["Rahu"] = longitude_info(rahu_sid, retrograde=True)

    ketu_sid = normalize_longitude(rahu_sid + 180.0)
    positions["Ketu"] = longitude_info(ketu_sid, retrograde=True)
    return positions


def planet_longitude_at(dt_utc: datetime, name: str) -> LongitudeInfo:
    jd = datetime_to_julian_day(dt_utc)
    return all_planet_longitudes(jd)[name]
