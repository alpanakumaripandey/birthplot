"""One-shot local test: match deep-dive with .env LLM key."""
from __future__ import annotations

import os
import sys
from datetime import date, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

env_path = ROOT / ".env"
if env_path.is_file():
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val

from kundli.chart import BirthInput, build_chart
from kundli.geocode import GeoPlace
from kundli.matching import match_charts
from kundli.simple_summary import match_simple_summary

PUNE = GeoPlace(
    query="Pune",
    display_name="Pune, Maharashtra, India",
    latitude=18.5204,
    longitude=73.8567,
    timezone="Asia/Kolkata",
)
JAIPUR = GeoPlace(
    query="Jaipur",
    display_name="Jaipur, Rajasthan, India",
    latitude=26.9124,
    longitude=75.7873,
    timezone="Asia/Kolkata",
)

a = build_chart(
    BirthInput(
        name="Mira",
        birth_date=date(1991, 3, 14),
        birth_time=time(9, 42),
        place_query="Pune",
        time_unknown=False,
    ),
    place=PUNE,
)
b = build_chart(
    BirthInput(
        name="Kabir",
        birth_date=date(1987, 11, 2),
        birth_time=time(16, 18),
        place_query="Jaipur",
        time_unknown=False,
    ),
    place=JAIPUR,
)
report = match_charts(a, b)
headline, sections, source = match_simple_summary(report)
print("version:", report["version"])
print("source:", source)
print("headline:", headline)
print("sections:", [(s["id"], len(s["body"])) for s in sections])
for s in sections:
    print(f"\n## {s['title']}")
    print(s["body"][:450])
