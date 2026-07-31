import { useEffect, useState } from 'react'
import { fetchLexicon } from '../api'
import {
  ELEMENT_ART,
  GRAHA_ART,
  NAKSHATRA_SKY,
  RASHI_ELEMENT,
} from '../art'
import { PlanetGlyph } from '../components/PlanetGlyph'
import { RashiGlyph } from '../components/RashiGlyph'
import { TiltCard } from '../components/TiltCard'
import { useLingo } from '../hooks/useLingo'

const KINDS = [
  { id: 'rashis', label: 'Rashis' },
  { id: 'nakshatras', label: 'Nakshatras' },
  { id: 'houses', label: 'Houses' },
  { id: 'planets', label: 'Grahas' },
  { id: 'topics', label: 'Topics' },
] as const

type Kind = (typeof KINDS)[number]['id']

export function Lexicon() {
  const { t } = useLingo()
  const [kind, setKind] = useState<Kind>('rashis')
  const [items, setItems] = useState<Record<string, Record<string, unknown>> | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState('')
  const [openKey, setOpenKey] = useState<string | null>(null)

  useEffect(() => {
    let alive = true
    setItems(null)
    setError(null)
    setOpenKey(null)
    fetchLexicon(kind)
      .then((data) => {
        if (alive) setItems(data as Record<string, Record<string, unknown>>)
      })
      .catch((err) => {
        if (alive) setError(err instanceof Error ? err.message : 'Load failed')
      })
    return () => {
      alive = false
    }
  }, [kind])

  const entries = items
    ? Object.entries(items).filter(([key, val]) => {
        const blob = `${key} ${JSON.stringify(val)}`.toLowerCase()
        return blob.includes(filter.toLowerCase())
      })
    : []

  const open = openKey && items ? items[openKey] : null

  function tileArt(key: string): string | undefined {
    if (kind === 'planets') return GRAHA_ART[key]
    if (kind === 'rashis') {
      const el = RASHI_ELEMENT[Number(key)]
      return el ? ELEMENT_ART[el] : undefined
    }
    if (kind === 'nakshatras') return NAKSHATRA_SKY
    return undefined
  }

  return (
    <section className="section wrap page-enter">
      <div
        className="lex-mosaic-hero"
        style={{
          backgroundImage:
            kind === 'nakshatras'
              ? `url('${NAKSHATRA_SKY}')`
              : "url('/art/lexicon-mosaic.png')",
        }}
        aria-hidden
      />
      <h1 className="section-title">{t('lexiconTitle')}</h1>
      <p className="lede">{t('lexiconLede')}</p>

      <div className="lex-tabs">
        {KINDS.map((k) => (
          <button
            key={k.id}
            type="button"
            className={kind === k.id ? 'active' : ''}
            onClick={() => setKind(k.id)}
          >
            {k.label}
          </button>
        ))}
      </div>

      <div className="field" style={{ maxWidth: '20rem', marginBottom: '1.5rem' }}>
        <label htmlFor="filter">Filter</label>
        <input
          id="filter"
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Search…"
        />
      </div>

      {error && <div className="error-banner">{error}</div>}
      {!items && !error && <p>Loading the library…</p>}

      <div className="lex-grid">
        {entries.map(([key, val]) => {
          const title =
            (val.name as string) ||
            (val.label as string) ||
            (val.sanskrit as string) ||
            key
          const summary =
            (val.summary as string) ||
            (val.intro as string) ||
            (val.karaka as string) ||
            ''
          const rashiIdx = kind === 'rashis' ? Number(key) : NaN
          const art = tileArt(key)
          return (
            <TiltCard
              key={key}
              as="article"
              className={`lex-item${art ? ' art-card' : ''}`}
              onClick={() => setOpenKey(key)}
            >
              {art && (
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    backgroundImage: `url('${art}')`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    opacity: 0.35,
                    pointerEvents: 'none',
                  }}
                />
              )}
              {kind === 'rashis' && !Number.isNaN(rashiIdx) && (
                <RashiGlyph rashiIndex={rashiIdx} size={32} />
              )}
              {kind === 'planets' && <PlanetGlyph name={key} size={32} />}
              <h3>{title}</h3>
              <p style={{ margin: 0, fontSize: '0.85rem', opacity: 0.7 }}>#{key}</p>
              {summary && (
                <p style={{ marginTop: '0.5rem' }}>
                  {summary.length > 90 ? `${summary.slice(0, 90)}…` : summary}
                </p>
              )}
            </TiltCard>
          )
        })}
      </div>

      {open && openKey && (
        <div className="lex-overlay" onClick={() => setOpenKey(null)} role="presentation">
          <div
            className="lex-overlay-panel"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal
          >
            {tileArt(openKey) && (
              <div
                className="drawer-art-band"
                style={{ backgroundImage: `url('${tileArt(openKey)}')`, margin: '0 0 1rem' }}
              />
            )}
            <h2 style={{ fontFamily: 'var(--font-display)', marginTop: 0 }}>
              {(open.name as string) ||
                (open.label as string) ||
                (open.sanskrit as string) ||
                openKey}
            </h2>
            {kind === 'rashis' && <RashiGlyph rashiIndex={Number(openKey)} size={48} />}
            {kind === 'planets' && <PlanetGlyph name={openKey} size={48} />}
            <div style={{ marginTop: '1rem', color: 'var(--ink-soft)' }}>
              {Object.entries(open).map(([k, v]) => (
                <p key={k} style={{ marginBottom: '0.65rem' }}>
                  <strong style={{ color: 'var(--ink)' }}>{k}:</strong>{' '}
                  {typeof v === 'string' || typeof v === 'number' || typeof v === 'boolean'
                    ? String(v)
                    : Array.isArray(v)
                      ? v.join(', ')
                      : JSON.stringify(v)}
                </p>
              ))}
            </div>
            <button type="button" className="btn" onClick={() => setOpenKey(null)}>
              Close
            </button>
          </div>
        </div>
      )}
    </section>
  )
}
