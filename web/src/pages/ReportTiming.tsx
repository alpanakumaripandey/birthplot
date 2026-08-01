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

  const maha = report?.timeline.current_mahadasha
  const antar = report?.timeline.antardashas_in_current ?? []
  const praty = report?.timeline.pratyantars_in_current ?? []
  const mahas = report?.timeline.mahadashas ?? []

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">{t('timingTitle')}</h1>
          <p className="lede">{t('timingLede')}</p>

          {maha && (
            <div className="chip-row">
              <button
                type="button"
                className={`chip${picked?.start === maha.start ? ' active' : ''}`}
                onClick={() => setPicked(maha)}
              >
                <strong>
                  {t('timingNowMaha')}: {maha.lord}
                </strong>
                <span>
                  {maha.start.slice(0, 10)} → {maha.end.slice(0, 10)}
                </span>
              </button>
              {report.timeline.current_antardasha && (
                <button
                  type="button"
                  className={`chip${
                    picked?.start === report.timeline.current_antardasha.start
                      ? ' active'
                      : ''
                  }`}
                  onClick={() => setPicked(report.timeline.current_antardasha)}
                >
                  <strong>
                    {t('timingNowAntar')}: {report.timeline.current_antardasha.lord}
                  </strong>
                  <span>
                    {report.timeline.current_antardasha.start.slice(0, 10)} →{' '}
                    {report.timeline.current_antardasha.end.slice(0, 10)}
                  </span>
                </button>
              )}
            </div>
          )}

          {mahas.length > 0 ? (
            <TimelineScrubber
              label={t('timingMahaLabel')}
              periods={mahas}
              selectedStart={picked?.level === 'mahadasha' ? picked.start : null}
              onSelect={setPicked}
            />
          ) : (
            <p className="lede">{t('timingEmpty')}</p>
          )}

          {antar.length > 0 ? (
            <TimelineScrubber
              label={t('timingAntarLabel')}
              periods={antar}
              selectedStart={picked?.level === 'antardasha' ? picked.start : null}
              onSelect={setPicked}
            />
          ) : (
            <p className="lede">{t('timingEmptyAntar')}</p>
          )}

          {praty.length > 0 ? (
            <TimelineScrubber
              label={t('timingPratyLabel')}
              periods={praty}
              selectedStart={picked?.level === 'pratyantar' ? picked.start : null}
              onSelect={setPicked}
            />
          ) : null}

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
