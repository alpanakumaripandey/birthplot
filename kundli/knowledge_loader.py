"""Load knowledge JSON files shipped with the package."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

_KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"


@lru_cache(maxsize=16)
def load_json(name: str) -> Dict[str, Any]:
    path = _KNOWLEDGE_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def rashis() -> Dict[str, Any]:
    return load_json("rashis.json")


def planets() -> Dict[str, Any]:
    return load_json("planets.json")


def nakshatras() -> Dict[str, Any]:
    return load_json("nakshatras.json")


def houses() -> Dict[str, Any]:
    return load_json("houses.json")


def topics() -> Dict[str, Any]:
    return load_json("topics.json")
