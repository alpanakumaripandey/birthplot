import { useMemo, useState } from 'react'
import { GRAHA_ART } from '../art'
import { DetailDrawer } from '../components/DetailDrawer'
import { PlanetGlyph } from '../components/PlanetGlyph'
import { ReportGate } from '../components/ReportGate'
import { TimelineScrubber } from '../components/TimelineScrubber'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import type { DashaPeriod } from '../types'

export function ReportTiming() {
  const { report } = useChart()
  const { t } = useLingo()
  const [picked, setPicked] = useState<DashaPeriod | null>(null)
  const revealRef = useReveal<HTMLDivElement>()

  const theme = useMemo(() => {
    if (!report || !picked) return null
    const lines = report.interpretation.dasha
    const hit = lines.find((l) => l.toLowerCase().includes(picked.lord.toLowerCase()))
    return (
      hit ??
      `Period lord ${picked.lord} colors events through its house and karaka themes in your chart.`
    )
  }, [report, picked])

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">{t('timingTitle')}</h1>
          <p className="lede">{t('timingLede')}</p>

          <div className="chip-row">
            {report.interpretation.dasha.slice(0, 3).map((line) => (
              <div key={line.slice(0, 32)} className="chip" style={{ cursor: 'default' }}>
                <strong>{line.split(':')[0]}</strong>
                <span>{line.length > 80 ? `${line.slice(0, 80)}…` : line}</span>
              </div>
            ))}
          </div>

          <TimelineScrubber
            label="Antardashas in current mahadasha"
            periods={report.timeline.antardashas_in_current}
            selectedStart={picked?.level === 'antardasha' ? picked.start : null}
            onSelect={setPicked}
          />

          <TimelineScrubber
            label="Pratyantar strip"
            periods={report.timeline.pratyantars_in_current}
            selectedStart={picked?.level === 'pratyantar' ? picked.start : null}
            onSelect={setPicked}
          />

          <DetailDrawer
            open={!!picked}
            title={picked ? `${picked.lord} period` : ''}
            subtitle={
              picked
                ? `${picked.start.slice(0, 10)} → ${picked.end.slice(0, 10)} · ${picked.level}`
                : undefined
            }
            art={picked ? GRAHA_ART[picked.lord] : undefined}
            onClose={() => setPicked(null)}
          >
            {picked && (
              <>
                <PlanetGlyph name={picked.lord} size={48} />
                <p>{theme}</p>
              </>
            )}
          </DetailDrawer>
        </div>
      )}
    </ReportGate>
  )
}
