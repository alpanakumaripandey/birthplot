import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { createChart } from '../api'
import { ReportGate } from '../components/ReportGate'
import { OrbitLoader } from '../components/OrbitLoader'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import type { LifeSummaryItem } from '../types'

const CURRENT = 'life-llm-v4'

function pickReading(items: LifeSummaryItem[] | undefined): LifeSummaryItem | undefined {
  const list = items ?? []
  const preferred = list.find((p) => {
    if (p.version !== CURRENT) return false
    if (p.sections && p.sections.length > 0) return true
    return Array.isArray(p.insights) && p.insights.length > 0
  })
  if (preferred) return preferred
  return list.find(
    (p) =>
      (p.sections && p.sections.length > 0) ||
      (Array.isArray(p.insights) && p.insights.length > 0),
  )
}

export function ReportSummary() {
  const { report, setReport, birthRequest } = useChart()
  const { t } = useLingo()
  const revealRef = useReveal<HTMLDivElement>()
  const reading = pickReading(report?.interpretation.life_summary)
  const needsFresh = !reading || reading.version !== CURRENT
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const tried = useRef(false)

  useEffect(() => {
    if (!birthRequest || !needsFresh || tried.current) return
    tried.current = true
    let cancelled = false
    setLoading(true)
    setError(null)
    void createChart(birthRequest)
      .then((fresh) => {
        if (cancelled) return
        setReport(fresh)
      })
      .catch((err) => {
        if (cancelled) return
        setError(err instanceof Error ? err.message : 'Could not load summary')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [birthRequest, needsFresh, setReport])

  const freshReading = pickReading(report?.interpretation.life_summary)
  const showReading =
    freshReading && freshReading.version === CURRENT ? freshReading : undefined

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef} className="summary-page">
          <header className="summary-header">
            <h1 className="section-title">{t('summaryTitle')}</h1>
            <p className="lede">{t('summaryLede')}</p>
          </header>

          {error && <div className="error-banner">{error}</div>}

          {loading || (needsFresh && !showReading && !error) ? (
            <div className="cast-loading" style={{ padding: '2rem 0' }}>
              <OrbitLoader />
              <p className="lede" style={{ marginBottom: 0 }}>
                {t('summaryLoading')}
              </p>
            </div>
          ) : !showReading ? (
            <div className="empty-panel">
              <p>{t('summaryEmpty')}</p>
              <button
                type="button"
                className="btn"
                onClick={() => {
                  tried.current = false
                  setError(null)
                  if (birthRequest) {
                    tried.current = true
                    setLoading(true)
                    void createChart(birthRequest)
                      .then(setReport)
                      .catch((err) =>
                        setError(err instanceof Error ? err.message : 'Could not load summary'),
                      )
                      .finally(() => setLoading(false))
                  }
                }}
              >
                {t('summaryRetry')}
              </button>
              <p style={{ marginTop: '1rem' }}>
                <Link to="/cast">{t('castCta')}</Link>
              </p>
            </div>
          ) : (
            <article className="summary-consult summary-story">
              <div className="match-simple-head">
                <h2 className="summary-story-title">
                  {showReading.simple_summary || showReading.kicker || t('summarySimpleTitle')}
                </h2>
                {showReading.simple_summary_source === 'llm' ? (
                  <span className="match-simple-badge">{t('summaryAiBadge')}</span>
                ) : null}
              </div>

              {showReading.sections && showReading.sections.length > 0 ? (
                <div className="summary-deep-sections">
                  {showReading.sections.map((sec, idx) => (
                    <section key={sec.id} className="summary-deep-block">
                      <h3>
                        <span className="summary-deep-num">{idx + 1}</span>
                        {sec.title}
                      </h3>
                      {sec.body.split(/\n\n+/).map((block) => (
                        <p key={block.slice(0, 56)} className="summary-para">
                          {block}
                        </p>
                      ))}
                    </section>
                  ))}
                </div>
              ) : (
                <div className="summary-story-body">
                  {(showReading.insights ?? []).map((para) =>
                    para.split(/\n\n+/).map((block) => (
                      <p key={block.slice(0, 48)} className="summary-para">
                        {block}
                      </p>
                    )),
                  )}
                </div>
              )}
            </article>
          )}
        </div>
      )}
    </ReportGate>
  )
}
