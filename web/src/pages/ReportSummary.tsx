import { Link } from 'react-router-dom'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'

export function ReportSummary() {
  const { report } = useChart()
  const { t } = useLingo()
  const revealRef = useReveal<HTMLDivElement>()
  const reading = (report?.interpretation.life_summary ?? []).find(
    (p) => p.version === 'jyotish-v2' && Array.isArray(p.insights) && p.insights.length > 0,
  )

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef} className="summary-page">
          <header className="summary-header">
            <h1 className="section-title">{t('summaryTitle')}</h1>
            <p className="lede">{t('summaryLede')}</p>
            <p className="summary-note">{t('summaryNote')}</p>
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
              <header className="summary-insight-head">
                <p className="summary-kicker">{reading.kicker}</p>
              </header>

              {reading.timing?.length ? (
                <div className="summary-timing-row" aria-label="Dasha windows">
                  {reading.timing.map((titem) => (
                    <span key={`${titem.label}-${titem.range}`} className="summary-chip">
                      <strong>{titem.label}</strong>
                      <span>{titem.range}</span>
                    </span>
                  ))}
                </div>
              ) : null}

              <div className="summary-insights summary-consult-body">
                {(reading.insights ?? []).map((para) => (
                  <p key={para.slice(0, 72)} className="summary-para">
                    {para}
                  </p>
                ))}
              </div>

              {reading.remedies?.length ? (
                <p className="summary-remedy-tags">
                  <span>{t('summaryRemedyFocus')}</span> {reading.remedies.join(' · ')}
                </p>
              ) : null}

              <p className="summary-insight-foot">
                <Link to="/report/ask">{t('summaryAskMore')}</Link>
              </p>
            </article>
          )}

          <p className="summary-foot">
            {t('summaryAskHint')}{' '}
            <Link to="/report/ask">{t('summaryAskLink')}</Link>
          </p>
        </div>
      )}
    </ReportGate>
  )
}
