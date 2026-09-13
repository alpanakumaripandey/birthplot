"""One-shot local test: life summary with .env LLM key."""
from __future__ import annotations

import json
import os
import sys
from datetime import date, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Load .env like api.main does
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
from kundli.dasha import compute_vimshottari
from kundli.geocode import GeoPlace
from kundli.life_summary import build_life_summary
from kundli.simple_summary import _api_config, _call_llm

print("=== CONFIG ===")
key, base, model = _api_config()
print("key_set:", bool(key), "prefix:", (key[:8] + "…") if key else None)
print("base:", base)
print("model:", model)

print("\n=== RAW LLM PING ===")
ping = _call_llm(
    "Reply with exactly: OK",
    "Say OK",
    max_tokens=20,
)
print("ping:", repr(ping))

print("\n=== BUILD CHART + SUMMARY ===")
place = GeoPlace(
    query="Pune",
    display_name="Pune, Maharashtra, India",
    latitude=18.5204,
    longitude=73.8567,
    timezone="Asia/Kolkata",
)
chart = build_chart(
    BirthInput(
        name="Mira",
        birth_date=date(1991, 3, 14),
        birth_time=time(9, 42),
        place_query="Pune",
        time_unknown=False,
    ),
    place=place,
)
timeline = compute_vimshottari(chart)
item = build_life_summary(chart, timeline)[0]
print("version:", item["version"])
print("source:", item.get("simple_summary_source"))
print("headline:", item.get("simple_summary"))
secs = item.get("sections") or []
print("sections:", [(s["id"], len(s["body"])) for s in secs])
for s in secs:
    print(f"\n## {s['title']}")
    print(s["body"][:500])
