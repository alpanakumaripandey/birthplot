"""Interactive Vedic Kundli CLI for non-experts."""

from __future__ import annotations

import sys
from datetime import date, datetime, time
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

# Avoid Windows cp1252 crashes on Unicode output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from kundli.chart import BirthInput, KundliChart, build_chart
from kundli.dasha import DashaTimeline, compute_vimshottari
from kundli.geocode import resolve_place
from kundli.interpret import build_interpretation
from kundli.qa import answer_question, list_topics_help

app = typer.Typer(
    add_completion=False,
    help="Interactive Vedic (Jyotish) kundli - plain-language answers in your terminal.",
    invoke_without_command=True,
)
console = Console(legacy_windows=False)


def _parse_date(raw: str) -> date:
    raw = raw.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ValueError("Use date like 1990-05-15 or 15-05-1990")


def _parse_time(raw: str) -> time:
    raw = raw.strip().lower().replace(".", ":")
    for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M%p"):
        try:
            return datetime.strptime(raw, fmt).time()
        except ValueError:
            continue
    raise ValueError("Use time like 14:30 or 2:30 PM")


def collect_birth_interactive(
    name: Optional[str] = None,
    birth_date: Optional[str] = None,
    birth_time: Optional[str] = None,
    place: Optional[str] = None,
    assume_yes: bool = False,
) -> BirthInput:
    console.print(
        Panel.fit(
            "[bold]Vedic Kundli[/bold]\n"
            "Answer a few simple questions. No astrology expertise needed.\n"
            "We use the Indian sidereal zodiac (Lahiri) and whole-sign houses.",
            border_style="cyan",
        )
    )

    name = name or Prompt.ask("Your name")
    while True:
        raw_date = birth_date or Prompt.ask("Date of birth", default="1990-01-15")
        try:
            d = _parse_date(raw_date)
            break
        except ValueError as exc:
            console.print(f"[red]{exc}[/red]")
            birth_date = None

    time_unknown = False
    t: Optional[time] = None
    if birth_time:
        if birth_time.strip().lower() in {"unknown", "?", "na", "n/a"}:
            time_unknown = True
            t = time(12, 0)
        else:
            t = _parse_time(birth_time)
    else:
        know_time = True if assume_yes else Confirm.ask(
            "Do you know your exact birth time?", default=True
        )
        if know_time:
            while True:
                raw_t = Prompt.ask("Birth time (24h or with AM/PM)", default="12:00")
                try:
                    t = _parse_time(raw_t)
                    break
                except ValueError as exc:
                    console.print(f"[red]{exc}[/red]")
        else:
            time_unknown = True
            t = time(12, 0)
            console.print(
                "[yellow]Using 12:00 noon as a placeholder. "
                "Lagna (rising sign) may be wrong without exact time; "
                "Moon sign and dasha are still useful.[/yellow]"
            )

    while True:
        place_q = place or Prompt.ask(
            "Place of birth (city, country)", default="Mumbai, India"
        )
        try:
            with console.status("Looking up location..."):
                geo = resolve_place(place_q)
            console.print(
                f"[green]Found:[/green] {geo.display_name}\n"
                f"  Lat {geo.latitude:.4f}, Lon {geo.longitude:.4f}, TZ {geo.timezone}"
            )
            if assume_yes or Confirm.ask("Use this location?", default=True):
                break
            place = None
        except ValueError as exc:
            console.print(f"[red]{exc}[/red]")
            place = None

    birth = BirthInput(
        name=name.strip() or "Friend",
        birth_date=d,
        birth_time=t,
        place_query=place_q,
        time_unknown=time_unknown,
    )
    console.print(
        f"\n[bold]Confirm:[/bold] {birth.name}, {birth.birth_date.isoformat()} "
        f"{birth.birth_time.strftime('%H:%M') if birth.birth_time else '?'} @ {place_q}"
    )
    if not assume_yes and not Confirm.ask("Generate kundli now?", default=True):
        raise typer.Exit(0)
    return birth


def _fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M %Z")


def render_report(
    chart: KundliChart,
    timeline: DashaTimeline,
    interpretation: dict,
) -> List[str]:
    """Render full report to console; return plain-text lines for optional save."""
    lines: List[str] = []

    def emit(text: str = "") -> None:
        lines.append(text)

    console.print()
    console.print(
        Panel(
            interpretation["disclaimer"],
            title="Disclaimer",
            border_style="dim",
        )
    )
    emit("DISCLAIMER")
    emit(interpretation["disclaimer"])
    emit("")

    # Birth summary
    summary = Table(title="Birth Summary", show_header=False, box=None)
    summary.add_row("Name", chart.birth.name)
    summary.add_row("Local birth", _fmt_dt(chart.local_dt))
    summary.add_row("UTC", _fmt_dt(chart.utc_dt))
    summary.add_row("Place", chart.place.display_name)
    summary.add_row(
        "Coords",
        f"{chart.place.latitude:.4f}, {chart.place.longitude:.4f} ({chart.place.timezone})",
    )
    if chart.birth.time_unknown:
        summary.add_row("Note", "Birth time approximate - Lagna uncertain")
    console.print(summary)
    emit("BIRTH SUMMARY")
    emit(f"Name: {chart.birth.name}")
    emit(f"Local: {_fmt_dt(chart.local_dt)}")
    emit(f"Place: {chart.place.display_name}")
    emit("")

    console.print(Panel(interpretation["lagna"], title="Lagna (Ascendant)", border_style="magenta"))
    emit("LAGNA")
    emit(interpretation["lagna"])
    emit("")

    console.print(Panel(interpretation["moon"], title="Moon & Nakshatra", border_style="blue"))
    emit("MOON")
    emit(interpretation["moon"])
    emit("")

    # Planets table
    pt = Table(title="Planetary Chart (Sidereal / Lahiri)", show_lines=False)
    pt.add_column("Planet")
    pt.add_column("Rashi")
    pt.add_column("House")
    pt.add_column("Nakshatra")
    pt.add_column("Pada")
    pt.add_column("Deg")
    pt.add_column("R")
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        pl = chart.planets[name]
        pt.add_row(
            name,
            pl.info.rashi_name,
            str(pl.house),
            pl.info.nakshatra_name,
            str(pl.info.pada),
            f"{pl.info.degree_in_rashi:.2f}",
            "R" if pl.info.retrograde else "",
        )
    console.print(pt)
    emit("PLANETS")
    for line in interpretation["planets"]:
        emit(line)
        console.print(f"  {line}")
    emit("")

    ht = Table(title="Houses (Whole Sign)", show_lines=False)
    ht.add_column("#", justify="right")
    ht.add_column("Theme")
    ht.add_column("Rashi")
    ht.add_column("Planets")
    from kundli.knowledge_loader import houses as houses_kb

    hkb = houses_kb()
    for h in chart.houses:
        ht.add_row(
            str(h.number),
            hkb[str(h.number)]["name"],
            h.rashi_name,
            ", ".join(h.planets) or "-",
        )
    console.print(ht)
    emit("HOUSES")
    for line in interpretation["houses"]:
        emit(line)
    emit("")

    # Yogas
    console.print(Text("Yogas (basic)", style="bold"))
    emit("YOGAS")
    for y in interpretation["yogas"]:
        mark = "[green]YES[/green]" if y.present else "[dim]no[/dim]"
        console.print(f"  {mark} [bold]{y.name}[/bold]: {y.detail}")
        console.print(f"      {y.meaning}")
        emit(f"{'YES' if y.present else 'no'} {y.name}: {y.detail}")
        emit(f"  {y.meaning}")
    emit("")

    # Dasha
    console.print(Panel("\n".join(interpretation["dasha"]), title="Vimshottari Dasha", border_style="green"))
    emit("DASHA")
    for line in interpretation["dasha"]:
        emit(line)
    emit("")

    if timeline.current_mahadasha and timeline.antardashas_in_current:
        dt = Table(title=f"Antardashas in {timeline.current_mahadasha.lord} Mahadasha")
        dt.add_column("Lord")
        dt.add_column("Start")
        dt.add_column("End")
        for a in timeline.antardashas_in_current:
            dt.add_row(a.lord, a.start.date().isoformat(), a.end.date().isoformat())
        console.print(dt)

    console.print(Panel("\n".join(interpretation["strengths"]), title="Strengths & Focus", border_style="yellow"))
    emit("STRENGTHS")
    for line in interpretation["strengths"]:
        emit(line)
    emit("")

    return lines


def qa_loop(chart: KundliChart, timeline: DashaTimeline, save_lines: List[str]) -> None:
    console.print()
    console.print(
        Panel(
            "Ask about life topics in plain words.\n"
            + list_topics_help()
            + "\nType [bold]quit[/bold] or [bold]exit[/bold] to finish.",
            title="Q&A Mode",
            border_style="cyan",
        )
    )
    while True:
        q = Prompt.ask("Your question", default="career")
        if q.strip().lower() in {"quit", "exit", "q", "done"}:
            break
        answer, key = answer_question(chart, timeline, q)
        console.print(Panel(answer, title=key or "Help", border_style="bright_blue"))
        save_lines.append("")
        save_lines.append(f"Q: {q}")
        save_lines.append(answer)


@app.callback()
def main(
    ctx: typer.Context,
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Person's name"),
    birth_date: Optional[str] = typer.Option(None, "--date", "-d", help="YYYY-MM-DD or DD-MM-YYYY"),
    birth_time: Optional[str] = typer.Option(None, "--time", "-t", help="HH:MM or 'unknown'"),
    place: Optional[str] = typer.Option(None, "--place", "-p", help="City, Country"),
    save: Optional[Path] = typer.Option(None, "--save", "-s", help="Save report to text file"),
    skip_qa: bool = typer.Option(False, "--skip-qa", help="Skip interactive Q&A"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Accept defaults / skip confirmations"),
) -> None:
    """Generate a full Vedic kundli report in the terminal."""
    if ctx.invoked_subcommand is not None:
        return

    birth = collect_birth_interactive(
        name, birth_date, birth_time, place, assume_yes=yes
    )

    with console.status("Computing kundli (Skyfield ephemeris)..."):
        place_obj = resolve_place(birth.place_query)
        chart = build_chart(birth, place=place_obj)
        timeline = compute_vimshottari(chart)
        interpretation = build_interpretation(chart, timeline)

    lines = render_report(chart, timeline, interpretation)

    if not skip_qa:
        qa_loop(chart, timeline, lines)

    out_path = save
    if out_path is None and not yes and Confirm.ask(
        "Save full report to a text file?", default=False
    ):
        default_name = f"kundli_{chart.birth.name.replace(' ', '_')}_{chart.birth.birth_date.isoformat()}.txt"
        out_path = Path(Prompt.ask("Filename", default=default_name))

    if out_path:
        out_path.write_text("\n".join(lines), encoding="utf-8")
        console.print(f"[green]Saved:[/green] {out_path.resolve()}")

    console.print("[bold]Done.[/bold] Run again anytime with: [cyan]python -m kundli[/cyan]")


if __name__ == "__main__":
    app()
