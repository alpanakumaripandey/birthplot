# Birthplot + Vedic Kundli

**Birthplot** is a local web UI for Indian Jyotish (Vedic) kundli. The same engine also runs as a terminal CLI.

## Features

- Sidereal zodiac with **Lahiri** ayanamsa (Skyfield / JPL ephemeris)
- **Whole-sign** houses, Lagna, 9 grahas (incl. Rahu/Ketu)
- Nakshatra + pada, yogas, Vimshottari dasha (maha / antar / pratyantar)
- Topic Q&A (career, marriage, health, money, ...)
- Funky multi-page site: Cast, Report modules, Lexicon, How
- CLI: interactive terminal reports

## Requirements

- Python 3.11+
- Node.js 18+ (for the website)
- Internet on first run (JPL `de421.bsp` ~17MB; place geocoding)

## Install

```bash
cd Astrology
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
pip install -e .

cd web
npm install
cd ..
```

## Run the website (local)

Two terminals from the project root:

```bash
# Terminal 1 — API
.\.venv\Scripts\uvicorn.exe api.main:app --reload --port 8000

# Terminal 2 — UI
cd web
npm run dev
```

Open **http://localhost:5173**

Vite proxies `/api` to the FastAPI server on port 8000.

## Free hosting

API on **Render** + UI on **Netlify** or **Cloudflare Pages**. Step-by-step: [DEPLOY.md](DEPLOY.md).

Demo: on **Cast**, click **Load Amit sample**, then **Cast it**.

### Website routes

| Path | Module |
|------|--------|
| `/` | Home hero |
| `/cast` | Birth form |
| `/report/you` … `/report/ask` | Report modules |
| `/lexicon` | Rashis, nakshatras, houses, grahas |
| `/how` | Method + disclaimer |

## Run the CLI

```bash
python -m kundli
```

Non-interactive:

```bash
python -m kundli --name "Ada" --date 1990-05-15 --time 14:30 --place "Mumbai, India" --save ada_kundli.txt -y --skip-qa
```

## Tests

```bash
pytest -q
```

## Notes

- Interpretations are **indicative** learning aids, not professional consultation.
- Chart JSON is stored in browser `sessionStorage` only (no database).
- Divisional charts (D9), matching, and deploy are out of scope for v1.
