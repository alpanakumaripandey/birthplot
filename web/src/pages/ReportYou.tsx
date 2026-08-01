import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { askQuestion } from '../api'
import { GRAHA_ART, NAKSHATRA_SKY } from '../art'
import { DetailDrawer } from '../components/DetailDrawer'
import { KundliDiamond } from '../components/KundliDiamond'
import { LifeAreas } from '../components/LifeAreas'
import { MagneticButton } from '../components/MagneticButton'
import { MajorSummary } from '../components/MajorSummary'
import { PlanetGlyph } from '../components/PlanetGlyph'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useCountUp } from '../hooks/useCountUp'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import { downloadChartCard } from '../lib/shareCard'
import type { LifeArea } from '../types'

const LIFE_SPECS: {
  id: string
  label: string
  ask_topic: string
  planets: string[]
  houses: number[]
}[] = [
  {
    id: 'career',
    label: 'Career',
    ask_topic: 'career',
    planets: ['Sun', 'Saturn', 'Mercury', 'Mars'],
    houses: [10, 6, 2, 11],
  },
  {
    id: 'education',
    label: 'Education',
    ask_topic: 'education',
    planets: ['Mercury', 'Jupiter', 'Moon'],
    houses: [4, 5, 9],
  },
  {
    id: 'marriage',
    label: 'Relationship',
    ask_topic: 'marriage',
    planets: ['Venus', 'Jupiter', 'Moon'],
    houses: [7, 2, 8, 11],
  },
]

function formatLifeFull(raw: string): string {
  return raw
    .replace(/^##\s+/gm, '')
    .replace(/^#\s+/gm, '')
    .replace(/^\*\s+/gm, '• ')
    .replace(/^-\s+/gm, '• ')
}

function LifeReadingBody({ full }: { full: string }) {
  const text = formatLifeFull(full)
  const parts = text
    .split(/(?=^(?:Right now|Coming up|What this means(?: for you)?|Present|Ahead|Chart basis)\b)/im)
    .filter((p) => p.trim())
  if (parts.length <= 1) {
    return <pre className="life-drawer-full">{text}</pre>
  }
  return (
    <div className="life-reading">
      {parts.map((part) => {
        const lines = part.trim().split('\n')
        const title = lines[0]
        const body = lines.slice(1).join('\n').trim()
        const isSection =
          /^(Right now|Coming up|What this means(?: for you)?|Present|Ahead|Chart basis)/i.test(
            title,
          )
        return (
          <section key={title.slice(0, 48)} className="life-reading-section">
            {isSection ? <h3>{title}</h3> : <p className="life-reading-title">{title}</p>}
            {body ? <pre className="life-drawer-full">{body}</pre> : null}
          </section>
        )
      })}
    </div>
  )
}

function areaFromAsk(
  spec: (typeof LIFE_SPECS)[number],
  full: string,
  _reportHouses: { number: number; rashi_name: string; planets: string[] }[],
): LifeArea {
  const lines = formatLifeFull(full)
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
  const presentIdx = lines.findIndex((l) => /^Right now/i.test(l) || /^Present/i.test(l))
  const aheadIdx = lines.findIndex((l) => /^Coming up/i.test(l) || /^Ahead/i.test(l))
  const presentBlock =
    presentIdx >= 0
      ? lines.slice(presentIdx + 1, aheadIdx > presentIdx ? aheadIdx : presentIdx + 5)
      : lines.slice(1, 4)
  const aheadLine = aheadIdx >= 0 ? lines[aheadIdx + 1] : ''
  const blurb = [presentBlock.find((l) => /feel|stretch|steady|busy|alive|louder|softer/i.test(l)) ?? presentBlock[1] ?? presentBlock[0], aheadLine]
    .filter(Boolean)
    .join(' ')
  const headline =
    presentBlock.find((l) => /feel|stretch|steady|busy|alive/i.test(l))?.slice(0, 72) ??
    `Your ${spec.label.toLowerCase()} at a glance`
  return {
    id: spec.id,
    label: spec.label,
    ask_topic: spec.ask_topic,
    headline,
    blurb: blurb || lines[0] || spec.label,
    full,
    houses: spec.houses,
    planets: spec.planets,
  }
}

type Sel =
  | { kind: 'house'; house: number }
  | { kind: 'planet'; name: string }
  | { kind: 'strength'; text: string }
  | { kind: 'life'; area: LifeArea }
  | null

export function ReportYou() {
  const { report, setReport, birthRequest } = useChart()
  const { t } = useLingo()
  const [sel, setSel] = useState<Sel>(null)
  const [sharing, setSharing] = useState(false)
  const [shareError, setShareError] = useState<string | null>(null)
  const [lifeAreas, setLifeAreas] = useState<LifeArea[]>(
    () => report?.interpretation.life_areas ?? [],
  )
  const [lifeLoading, setLifeLoading] = useState(false)
  const revealRef = useReveal<HTMLDivElement>()

  useEffect(() => {
    const fromReport = report?.interpretation.life_areas
    const stale =
      !fromReport?.length ||
      fromReport.some(
        (a) =>
          /Timing window:|significators|mahadasha|antardasha|House \d+/i.test(a.full) ||
          !/friendly-v2|What this means for you/i.test(a.full),
      )
    if (fromReport?.length && !stale) {
      setLifeAreas(fromReport)
      return
    }
    if (!report || !birthRequest) {
      setLifeAreas(fromReport?.length ? fromReport : [])
      return
    }
    let alive = true
    setLifeLoading(true)
    Promise.all(
      LIFE_SPECS.map(async (spec) => {
        const res = await askQuestion(birthRequest, spec.ask_topic)
        return areaFromAsk(spec, res.answer, report.chart.houses)
      }),
    )
      .then((areas) => {
        if (!alive) return
        setLifeAreas(areas)
        setReport({
          ...report,
          interpretation: { ...report.interpretation, life_areas: areas },
        })
      })
      .catch(() => {
        if (alive) setLifeAreas(fromReport?.length ? fromReport : [])
      })
      .finally(() => {
        if (alive) setLifeLoading(false)
      })
    return () => {
      alive = false
    }
  }, [report, birthRequest, setReport])

  const deg = useCountUp(
    sel?.kind === 'planet' && report
      ? report.chart.planets[sel.name].info.degree_in_rashi
      : 0,
    sel?.kind === 'planet',
  )

  const drawer = useMemo(() => {
    if (!report || !sel) return null
    if (sel.kind === 'house') {
      const h = report.chart.houses[sel.house - 1]
      const line = report.interpretation.houses[sel.house - 1]
      return {
        title: `House ${h.number}`,
        subtitle: h.rashi_name,
        art: undefined as string | undefined,
        body: (
          <>
            <p>
              <strong>Planets:</strong> {h.planets.length ? h.planets.join(', ') : 'empty'}
            </p>
            <p>{line}</p>
          </>
        ),
      }
    }
    if (sel.kind === 'planet') {
      const pl = report.chart.planets[sel.name]
      const line = report.interpretation.planets.find((p) => p.startsWith(sel.name))
      return {
        title: sel.name,
        subtitle: `${pl.info.rashi_name} · House ${pl.house}`,
        art: GRAHA_ART[sel.name],
        body: (
          <>
            <PlanetGlyph name={sel.name} size={48} />
            <p>
              {pl.info.nakshatra_name} pada {pl.info.pada} · {deg.toFixed(2)}°
              {pl.info.retrograde ? ' · Retrograde' : ''}
            </p>
            <p>{line}</p>
          </>
        ),
      }
    }
    if (sel.kind === 'life') {
      const area = sel.area
      return {
        title: area.label,
        subtitle: area.headline,
        art: GRAHA_ART[area.planets[0]] as string | undefined,
        body: (
          <>
            <LifeReadingBody full={area.full} />
            <p style={{ marginTop: '1.25rem' }}>
              <Link className="btn" to={`/report/ask?topic=${encodeURIComponent(area.ask_topic)}`}>
                {t('lifeAreaAskMore')}
              </Link>
            </p>
          </>
        ),
      }
    }
    return {
      title: 'Focus note',
      subtitle: 'Strengths',
      art: undefined as string | undefined,
      body: <p>{sel.text}</p>,
    }
  }, [report, sel, deg, t])

  async function onShare() {
    if (!report) return
    setSharing(true)
    setShareError(null)
    try {
      await downloadChartCard(report)
    } catch (err) {
      setShareError(err instanceof Error ? err.message : t('shareFailed'))
    } finally {
      setSharing(false)
    }
  }

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef} className="you-page">
          <div
            className="you-hero-band"
            style={{ backgroundImage: `url('${NAKSHATRA_SKY}')` }}
            aria-hidden
          />

          <header className="you-header">
            <div>
              <p className="you-kicker">{t('youKicker')}</p>
              <h1 className="section-title you-title">
                {t('youTitle')} — {report.chart.birth.name}
              </h1>
              <p className="lede you-place">{report.chart.place.display_name}</p>
            </div>
            <MagneticButton as="button" onClick={() => void onShare()} disabled={sharing}>
              {sharing ? t('shareRendering') : t('shareCard')}
            </MagneticButton>
          </header>
          {shareError && <div className="error-banner">{shareError}</div>}

          <MajorSummary report={report} />

          {lifeLoading && !lifeAreas.length ? (
            <p className="lede life-areas-loading">{t('lifeAreasLoading')}</p>
          ) : (
            <LifeAreas areas={lifeAreas} onOpen={(area) => setSel({ kind: 'life', area })} />
          )}

          <div className="you-story-grid">
            <article className="you-story-card">
              <h2>{t('youLagnaStory')}</h2>
              <p>{report.interpretation.lagna}</p>
              <button
                type="button"
                className="chip"
                onClick={() => setSel({ kind: 'house', house: 1 })}
              >
                <strong>Lagna · {report.chart.lagna.rashi_name}</strong>
                <span>{t('youOpenLagna')}</span>
              </button>
            </article>
            <article
              className="you-story-card you-story-moon"
              style={{ backgroundImage: `url('${NAKSHATRA_SKY}')` }}
            >
              <h2>{t('youMoonStory')}</h2>
              <p>{report.interpretation.moon}</p>
              <button
                type="button"
                className="chip"
                onClick={() => setSel({ kind: 'planet', name: 'Moon' })}
              >
                <strong>
                  Moon · {report.chart.moon_nakshatra} p{report.chart.moon_pada}
                </strong>
                <span>{t('youOpenMoon')}</span>
              </button>
            </article>
          </div>

          <div className="visual-split you-map-split">
            <div className="you-diamond-wrap">
              <h2 className="you-section-label">{t('youMapTitle')}</h2>
              <KundliDiamond
                chart={report.chart}
                selected={sel?.kind === 'house' ? sel : null}
                onSelect={(s) => setSel(s)}
              />
            </div>
            <div>
              <h2 className="you-section-label">{t('strengthChips')}</h2>
              <p className="lede" style={{ fontSize: '0.95rem' }}>
                {t('youLede')}
              </p>
              <div className="chip-row">
                {report.interpretation.strengths.map((s) => (
                  <button
                    key={s.slice(0, 48)}
                    type="button"
                    className="chip"
                    onClick={() => setSel({ kind: 'strength', text: s })}
                  >
                    <strong>{s.split(/[.:]/)[0].slice(0, 42)}</strong>
                    <span>{t('youOpenNote')}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <DetailDrawer
            open={!!drawer}
            title={drawer?.title ?? ''}
            subtitle={drawer?.subtitle}
            art={drawer?.art}
            onClose={() => setSel(null)}
          >
            {drawer?.body}
          </DetailDrawer>
        </div>
      )}
    </ReportGate>
  )
}
