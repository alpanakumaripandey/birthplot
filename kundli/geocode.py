"""Place name → latitude, longitude, IANA timezone."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

_tf = TimezoneFinder()


@dataclass(frozen=True)
class GeoPlace:
    query: str
    display_name: str
    latitude: float
    longitude: float
    timezone: str


@lru_cache(maxsize=128)
def resolve_place(place: str) -> GeoPlace:
    """Geocode a city/place string. Raises ValueError if not found."""
    query = place.strip()
    if not query:
        raise ValueError("Place name is empty.")

    geolocator = Nominatim(user_agent="vedic-kundli-cli/0.1")
    try:
        location = geolocator.geocode(query, exactly_one=True, timeout=15)
    except (GeocoderTimedOut, GeocoderServiceError) as exc:
        raise ValueError(
            f"Could not look up place '{query}' (network/geocoder error: {exc}). "
            "Try again or use a clearer city name, e.g. 'Mumbai, India'."
        ) from exc

    if location is None:
        raise ValueError(
            f"Could not find place '{query}'. Try 'City, Country' (e.g. 'Delhi, India')."
        )

    lat = float(location.latitude)
    lon = float(location.longitude)
    tz = _tf.timezone_at(lat=lat, lng=lon)
    if not tz:
        # Fallback for rare ocean/edge cases
        tz = "UTC"

    return GeoPlace(
        query=query,
        display_name=location.address,
        latitude=lat,
        longitude=lon,
        timezone=tz,
    )
