import { Link } from 'react-router-dom'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import type { LifeSummaryItem } from '../types'

const LABELS = ['Past', 'Present', 'Future'] as const
const PREFERRED = ['life-llm-v1', 'jyotish-v3']

function pickReading(items: LifeSummaryItem[] | undefined): LifeSummaryItem | undefined {
  const list = items ?? []
  for (const ver of PREFERRED) {
    const hit = list.find(
      (p) => p.version === ver && Array.isArray(p.insights) && p.insights.length > 0,
    )
    if (hit) return hit
  }
  return list.find((p) => Array.isArray(p.insights) && p.insights.length > 0)
}

export function ReportSummary() {
  const { report } = useChart()
  const { t } = useLingo()
  const revealRef = useReveal<HTMLDivElement>()
  const reading = pickReading(report?.interpretation.life_summary)

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef} className="summary-page">
          <header className="summary-header">
            <h1 className="section-title">{t('summaryTitle')}</h1>
            <p className="lede">{t('summaryLede')}</p>
          </header>

          {!reading ? (
            <div className="empty-panel">
              <p>{t('summaryEmpty')}</p>
              <Link className="btn" to="/cast">
                {t('castCta')}
              </Link>
            </div>
          ) : (
            <article className="summary-consult">
              {reading.kicker || reading.simple_summary ? (
                <div className="match-simple-summary summary-hero-summary">
                  <div className="match-simple-head">
                    <h2>{t('summarySimpleTitle')}</h2>
                    {reading.simple_summary_source === 'llm' ||
                    reading.version === 'life-llm-v1' ? (
                      <span className="match-simple-badge">{t('summaryAiBadge')}</span>
                    ) : null}
                  </div>
                  <p>{reading.simple_summary || reading.kicker}</p>
                </div>
              ) : null}

              {reading.timing?.length ? (
                <div className="summary-timing-row" aria-label="Timing">
                  {reading.timing.map((titem) => (
                    <span key={`${titem.label}-${titem.range}`} className="summary-chip">
                      <strong>{titem.label}</strong>
                      <span>{titem.range}</span>
                    </span>
                  ))}
                </div>
              ) : null}

              <div className="summary-insights">
                {(reading.insights ?? []).map((para, i) => (
                  <div key={LABELS[i] ?? String(i)} className="summary-block">
                    <h2>{LABELS[i] ?? ''}</h2>
                    <p className="summary-para">{para}</p>
                  </div>
                ))}
              </div>
            </article>
          )}
        </div>
      )}
    </ReportGate>
  )
}
