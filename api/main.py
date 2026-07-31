"""Birthplot FastAPI — local API over the kundli engine."""

from __future__ import annotations

import os
from datetime import date, datetime, time
from typing import Any, Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from kundli.chart import BirthInput, build_chart
from kundli.dasha import compute_vimshottari
from kundli.knowledge_loader import houses, nakshatras, planets, rashis, topics
from kundli.qa import answer_question, list_topics_help
from api.serialize import build_full_report

_LOCAL_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]


def _cors_origins() -> List[str]:
    """Localhost always allowed; add hosted UI origins via CORS_ORIGINS (comma-separated)."""
    extra = [
        o.strip().rstrip("/")
        for o in os.environ.get("CORS_ORIGINS", "").split(",")
        if o.strip()
    ]
    # Preserve order, drop dupes
    seen: set[str] = set()
    out: List[str] = []
    for origin in [*_LOCAL_ORIGINS, *extra]:
        if origin not in seen:
            seen.add(origin)
            out.append(origin)
    return out


app = FastAPI(title="Birthplot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChartRequest(BaseModel):
    name: str = Field(..., min_length=1)
    date: str = Field(..., description="YYYY-MM-DD")
    time: Optional[str] = Field(None, description="HH:MM or null if unknown")
    place: str = Field(..., min_length=1)
    time_unknown: bool = False


class AskRequest(BaseModel):
    name: str
    date: str
    time: Optional[str] = None
    place: str
    time_unknown: bool = False
    question: str = Field(..., min_length=1)


def _parse_birth(req: ChartRequest | AskRequest) -> BirthInput:
    try:
        d = date.fromisoformat(req.date.strip())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Date must be YYYY-MM-DD") from exc

    t: Optional[time] = None
    time_unknown = req.time_unknown
    raw_t = (req.time or "").strip()
    if time_unknown or raw_t.lower() in {"", "unknown", "?", "na", "n/a"}:
        time_unknown = True
        t = time(12, 0)
    else:
        for fmt in ("%H:%M", "%H:%M:%S"):
            try:
                t = datetime.strptime(raw_t, fmt).time()
                break
            except ValueError:
                continue
        if t is None:
            raise HTTPException(status_code=400, detail="Time must be HH:MM")

    return BirthInput(
        name=req.name.strip() or "Friend",
        birth_date=d,
        birth_time=t,
        place_query=req.place.strip(),
        time_unknown=time_unknown,
    )


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "brand": "Birthplot"}


@app.post("/api/chart")
def create_chart(body: ChartRequest) -> Dict[str, Any]:
    birth = _parse_birth(body)
    try:
        return build_full_report(birth)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Chart failed: {exc}") from exc


@app.post("/api/ask")
def ask(body: AskRequest) -> Dict[str, Any]:
    birth = _parse_birth(body)
    try:
        chart = build_chart(birth)
        timeline = compute_vimshottari(chart)
        answer, topic = answer_question(chart, timeline, body.question)
        return {
            "question": body.question,
            "topic": topic,
            "answer": answer,
            "help": list_topics_help() if topic is None else None,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Ask failed: {exc}") from exc


LexiconKind = Literal["rashis", "planets", "nakshatras", "houses", "topics"]


@app.get("/api/lexicon/{kind}")
def lexicon(kind: LexiconKind) -> Dict[str, Any]:
    loaders = {
        "rashis": rashis,
        "planets": planets,
        "nakshatras": nakshatras,
        "houses": houses,
        "topics": topics,
    }
    return {"kind": kind, "items": loaders[kind]()}
