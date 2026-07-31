# Deploy Birthplot (free)

Two services: **API on Render**, **UI on Netlify or Cloudflare Pages**.

Push this repo to GitHub first (private is fine).

## 1. API — Render

1. [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**, connect the repo  
   (uses `render.yaml`), **or** **Web Service** with:
   - **Root directory:** repo root
   - **Build:** `pip install -r requirements.txt && pip install .`
   - **Start:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Health check:** `/api/health`
2. Set env var **`CORS_ORIGINS`** after you have a UI URL, e.g.  
   `https://YOUR-SITE.netlify.app`  
   (comma-separated if you use more than one host; no trailing slash)
3. Copy the service URL, e.g. `https://birthplot-api.onrender.com`

Smoke test: open `https://YOUR-API.onrender.com/api/health` → `{"status":"ok",...}`.

**Note:** Free instances sleep. First chart after idle can take ~30–60s; Skyfield may also download `de421.bsp` (~17MB) once.

## 2a. UI — Netlify (pick this or 2b)

1. [Netlify](https://app.netlify.com) → **Add new site** → import repo
2. **Base directory:** `web`
3. **Build command:** `npm run build`
4. **Publish directory:** `dist`
5. Env var **`VITE_API_URL`** = your Render URL (no trailing slash)
6. Deploy, then put the Netlify URL into Render’s **`CORS_ORIGINS`** and redeploy/restart the API if needed

## 2b. UI — Cloudflare Pages

1. [Cloudflare Pages](https://pages.cloudflare.com) → create project from Git
2. **Root directory:** `web`
3. **Build command:** `npm run build`
4. **Build output:** `dist`
5. Env var **`VITE_API_URL`** = your Render URL
6. Deploy, then add the `*.pages.dev` (and custom domain) URL to **`CORS_ORIGINS`**

## Local still works

```bash
# API
uvicorn api.main:app --reload --port 8000

# UI — leave VITE_API_URL unset; Vite proxies /api
cd web && npm run dev
```

## Checklist if something fails

| Symptom | Fix |
|---------|-----|
| Browser CORS error | Add exact UI origin to `CORS_ORIGINS` on Render |
| UI calls localhost / wrong host | Set `VITE_API_URL` and **rebuild** the frontend (Vite inlines it at build time) |
| Deep links 404 | Confirm `_redirects` / Netlify `[[redirects]]` SPA rule |
| API 502 / slow first hit | Free sleep + cold start; wait and retry `/api/health` |
