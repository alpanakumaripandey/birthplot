import { useMemo, useState } from 'react'
import { GRAHA_ART } from '../art'
import { DetailDrawer } from '../components/DetailDrawer'
import { GlyphGrid } from '../components/GlyphGrid'
import { PlanetGlyph, PLANET_ORDER } from '../components/PlanetGlyph'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useCountUp } from '../hooks/useCountUp'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'

export function ReportGrahas() {
  const { report } = useChart()
  const { t } = useLingo()
  const [selected, setSelected] = useState<string | null>(null)
  const [showNumbers, setShowNumbers] = useState(false)
  const revealRef = useReveal<HTMLDivElement>()
  const deg = useCountUp(
    selected && report ? report.chart.planets[selected].info.degree_in_rashi : 0,
    !!selected,
  )

  const drawer = useMemo(() => {
    if (!report || !selected) return null
    const pl = report.chart.planets[selected]
    const line = report.interpretation.planets.find((p) => p.startsWith(selected))
    return { pl, line }
  }, [report, selected])

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">{t('grahasTitle')}</h1>
          <p className="lede">{t('grahasLede')}</p>

          <GlyphGrid chart={report.chart} selected={selected} onSelect={setSelected} />

          <div className="numbers-toggle">
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => setShowNumbers((v) => !v)}
            >
              {showNumbers ? t('hideNumbers') : t('showNumbers')}
            </button>
          </div>

          {showNumbers && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Planet</th>
                  <th>Rashi</th>
                  <th>House</th>
                  <th>Nakshatra</th>
                  <th>Pada</th>
                  <th>Deg</th>
                  <th>R</th>
                </tr>
              </thead>
              <tbody>
                {PLANET_ORDER.map((name) => {
                  const pl = report.chart.planets[name]
                  return (
                    <tr key={name}>
                      <td>{name}</td>
                      <td>{pl.info.rashi_name}</td>
                      <td>{pl.house}</td>
                      <td>{pl.info.nakshatra_name}</td>
                      <td>{pl.info.pada}</td>
                      <td>{pl.info.degree_in_rashi.toFixed(2)}</td>
                      <td>{pl.info.retrograde ? 'R' : ''}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          )}

          <DetailDrawer
            open={!!drawer}
            title={selected ?? ''}
            subtitle={
              drawer
                ? `${drawer.pl.info.rashi_name} · House ${drawer.pl.house}`
                : undefined
            }
            art={selected ? GRAHA_ART[selected] : undefined}
            onClose={() => setSelected(null)}
          >
            {drawer && selected && (
              <>
                <PlanetGlyph name={selected} size={52} />
                <p>
                  {drawer.pl.info.nakshatra_name} · pada {drawer.pl.info.pada} ·{' '}
                  {deg.toFixed(2)}°
                  {drawer.pl.info.retrograde ? ' · Retrograde' : ''}
                </p>
                <p>{drawer.line}</p>
              </>
            )}
          </DetailDrawer>
        </div>
      )}
    </ReportGate>
  )
}
