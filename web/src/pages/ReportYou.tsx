import { useMemo, useState } from 'react'
import { GRAHA_ART, NAKSHATRA_SKY } from '../art'
import { DetailDrawer } from '../components/DetailDrawer'
import { KundliDiamond } from '../components/KundliDiamond'
import { MagneticButton } from '../components/MagneticButton'
import { PlanetGlyph } from '../components/PlanetGlyph'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useCountUp } from '../hooks/useCountUp'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import { downloadChartCard } from '../lib/shareCard'

type Sel =
  | { kind: 'house'; house: number }
  | { kind: 'planet'; name: string }
  | { kind: 'strength'; text: string }
  | null

export function ReportYou() {
  const { report } = useChart()
  const { t } = useLingo()
  const [sel, setSel] = useState<Sel>(null)
  const [sharing, setSharing] = useState(false)
  const revealRef = useReveal<HTMLDivElement>()

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
    return {
      title: 'Focus note',
      subtitle: 'Strengths',
      art: undefined as string | undefined,
      body: <p>{sel.text}</p>,
    }
  }, [report, sel, deg])

  async function onShare() {
    if (!report) return
    setSharing(true)
    try {
      await downloadChartCard(report)
    } finally {
      setSharing(false)
    }
  }

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">
            {t('youTitle')} — {report.chart.birth.name}
          </h1>
          <p className="lede">{report.chart.place.display_name}</p>

          <MagneticButton as="button" onClick={() => void onShare()} disabled={sharing}>
            {sharing ? 'Rendering…' : t('shareCard')}
          </MagneticButton>

          <div className="chip-row" style={{ marginTop: '1rem' }}>
            <button
              type="button"
              className={`chip${sel?.kind === 'house' && sel.house === 1 ? ' active' : ''}`}
              onClick={() => setSel({ kind: 'house', house: 1 })}
            >
              <strong>Lagna · {report.chart.lagna.rashi_name}</strong>
              <span>Rising sign</span>
            </button>
            <button
              type="button"
              className={`chip art-card${sel?.kind === 'planet' && sel.name === 'Moon' ? ' active' : ''}`}
              style={{ backgroundImage: `url('${NAKSHATRA_SKY}')` }}
              onClick={() => setSel({ kind: 'planet', name: 'Moon' })}
            >
              <strong>Moon · {report.chart.moon_nakshatra}</strong>
              <span>Pada {report.chart.moon_pada}</span>
            </button>
          </div>

          <div className="visual-split" style={{ marginTop: '1.25rem' }}>
            <KundliDiamond
              chart={report.chart}
              selected={sel?.kind === 'house' ? sel : null}
              onSelect={(s) => setSel(s)}
            />
            <div>
              <h2 style={{ fontFamily: 'var(--font-display)', marginTop: 0 }}>
                {t('strengthChips')}
              </h2>
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
                    <span>Open note</span>
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
