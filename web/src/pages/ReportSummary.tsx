import { Link } from 'react-router-dom'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'

const LABELS = ['Past', 'Present', 'Future'] as const

export function ReportSummary() {
  const { report } = useChart()
  const { t } = useLingo()
  const revealRef = useReveal<HTMLDivElement>()
  const reading = (report?.interpretation.life_summary ?? []).find(
    (p) => p.version === 'jyotish-v3' && Array.isArray(p.insights) && p.insights.length > 0,
  )

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef} className="summary-page">
          <header className="summary-header">
            <h1 className="section-title">{t('summaryTitle')}</h1>
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

