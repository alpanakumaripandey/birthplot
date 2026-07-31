import type { AskResponse, ChartRequest, FullReport } from './types'

/** Empty in local dev (Vite proxies /api). Set VITE_API_URL on Netlify/Cloudflare. */
const API_BASE = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, '') ?? ''

async function parseError(res: Response): Promise<string> {
  try {
    const data = await res.json()
    if (typeof data.detail === 'string') return data.detail
    return JSON.stringify(data.detail ?? data)
  } catch {
    return res.statusText || 'Request failed'
  }
}

export async function createChart(body: ChartRequest): Promise<FullReport> {
  const res = await fetch(`${API_BASE}/api/chart`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
}

export async function askQuestion(
  birth: ChartRequest,
  question: string,
): Promise<AskResponse> {
  const res = await fetch(`${API_BASE}/api/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...birth, question }),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json()
}

export async function fetchLexicon(kind: string): Promise<Record<string, unknown>> {
  const res = await fetch(`${API_BASE}/api/lexicon/${kind}`)
  if (!res.ok) throw new Error(await parseError(res))
  const data = await res.json()
  return data.items as Record<string, unknown>
}
