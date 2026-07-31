"""Build a Vedic kundli (D1) using whole-sign houses."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo

from kundli.ephemeris import (
    all_planet_longitudes,
    ascendant_longitude,
    datetime_to_julian_day,
    longitude_info,
    LongitudeInfo,
)
from kundli.geocode import GeoPlace, resolve_place


@dataclass
class PlanetPlacement:
    name: str
    info: LongitudeInfo
    house: int  # 1-12 whole-sign from Lagna


@dataclass
class HouseInfo:
    number: int
    rashi_index: int
    rashi_name: str
    planets: List[str] = field(default_factory=list)


@dataclass
class BirthInput:
    name: str
    birth_date: date
    birth_time: Optional[time]
    place_query: str
    time_unknown: bool = False


@dataclass
class KundliChart:
    birth: BirthInput
    place: GeoPlace
    local_dt: datetime
    utc_dt: datetime
    julian_day: float
    lagna: LongitudeInfo
    planets: Dict[str, PlanetPlacement]
    houses: List[HouseInfo]
    moon_nakshatra: str
    moon_pada: int

    @property
    def lagna_rashi(self) -> str:
        return self.lagna.rashi_name


def _whole_sign_house(planet_rashi: int, lagna_rashi: int) -> int:
    """House number 1-12 for whole-sign system."""
    return ((planet_rashi - lagna_rashi) % 12) + 1


def _local_datetime(birth: BirthInput, place: GeoPlace) -> datetime:
    tz = ZoneInfo(place.timezone)
    t = birth.birth_time or time(12, 0, 0)
    return datetime(
        birth.birth_date.year,
        birth.birth_date.month,
        birth.birth_date.day,
        t.hour,
        t.minute,
        t.second,
        tzinfo=tz,
    )


def build_chart(
    birth: BirthInput,
    place: Optional[GeoPlace] = None,
) -> KundliChart:
    """Compute full D1 kundli from birth details."""
    place = place or resolve_place(birth.place_query)
    local_dt = _local_datetime(birth, place)
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
    jd = datetime_to_julian_day(utc_dt)

    lagna = longitude_info(ascendant_longitude(jd, place.latitude, place.longitude))
    raw_planets = all_planet_longitudes(jd)

    planets: Dict[str, PlanetPlacement] = {}
    for name, info in raw_planets.items():
        house = _whole_sign_house(info.rashi_index, lagna.rashi_index)
        planets[name] = PlanetPlacement(name=name, info=info, house=house)

    # Build 12 houses
    from kundli.ephemeris import RASHI_NAMES

    houses: List[HouseInfo] = []
    for h in range(1, 13):
        rashi_idx = ((lagna.rashi_index - 1 + h - 1) % 12) + 1
        occupants = [
            p.name for p in planets.values() if p.house == h
        ]
        houses.append(
            HouseInfo(
                number=h,
                rashi_index=rashi_idx,
                rashi_name=RASHI_NAMES[rashi_idx - 1],
                planets=occupants,
            )
        )

    moon = planets["Moon"]
    return KundliChart(
        birth=birth,
        place=place,
        local_dt=local_dt,
        utc_dt=utc_dt,
        julian_day=jd,
        lagna=lagna,
        planets=planets,
        houses=houses,
        moon_nakshatra=moon.info.nakshatra_name,
        moon_pada=moon.info.pada,
    )
