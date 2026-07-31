import { useMemo, useState } from 'react'
import { ELEMENT_ART, RASHI_ELEMENT } from '../art'
import { DetailDrawer } from '../components/DetailDrawer'
import { KundliDiamond } from '../components/KundliDiamond'
import { RashiGlyph } from '../components/RashiGlyph'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'

type Sel = { kind: 'house'; house: number } | null

export function ReportHouses() {
  const { report } = useChart()
  const { t } = useLingo()
  const [sel, setSel] = useState<Sel>(null)
  const revealRef = useReveal<HTMLDivElement>()

  const drawer = useMemo(() => {
    if (!report || !sel) return null
    const h = report.chart.houses[sel.house - 1]
    const line = report.interpretation.houses[sel.house - 1]
    const el = RASHI_ELEMENT[h.rashi_index]
    return { h, line, art: ELEMENT_ART[el] }
  }, [report, sel])

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">{t('housesTitle')}</h1>
          <p className="lede">{t('housesLede')}</p>

          <div className="visual-split">
            <KundliDiamond
              chart={report.chart}
              selected={sel}
              onSelect={(s) => setSel(s.kind === 'house' ? s : null)}
            />
            <div className="chip-row" style={{ flexDirection: 'column', alignItems: 'stretch' }}>
              {report.chart.houses.map((h) => (
                <button
                  key={h.number}
                  type="button"
                  className={`chip${sel?.house === h.number ? ' active' : ''}`}
                  onClick={() => setSel({ kind: 'house', house: h.number })}
                >
                  <strong>
                    H{h.number} · {h.rashi_name}
                  </strong>
                  <span>{h.planets.length ? h.planets.join(', ') : 'empty room'}</span>
                </button>
              ))}
            </div>
          </div>

          <DetailDrawer
            open={!!drawer}
            title={drawer ? `House ${drawer.h.number}` : ''}
            subtitle={drawer?.h.rashi_name}
            art={drawer?.art}
            onClose={() => setSel(null)}
          >
            {drawer && (
              <>
                <RashiGlyph rashiIndex={drawer.h.rashi_index} size={40} />
                <p>
                  <strong>Occupants:</strong>{' '}
                  {drawer.h.planets.length ? drawer.h.planets.join(', ') : 'none'}
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
