import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { DetailDrawer } from '../components/DetailDrawer'
import { ReportGate } from '../components/ReportGate'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import type { LifeSummaryItem } from '../types'

const CATEGORY_ORDER = ['career', 'love', 'life'] as const

export function ReportSummary() {
  const { report } = useChart()
  const { t } = useLingo()
  const revealRef = useReveal<HTMLDivElement>()
  const [open, setOpen] = useState<LifeSummaryItem | null>(null)

  const grouped = useMemo(() => {
    const items = report?.interpretation.life_summary ?? []
    return CATEGORY_ORDER.map((cat) => ({
      id: cat,
      label: items.find((i) => i.category === cat)?.category_label ?? cat,
      items: items.filter((i) => i.category === cat),
    })).filter((g) => g.items.length)
  }, [report])

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef} className="summary-page">
          <header className="summary-header">
            <h1 className="section-title">{t('summaryTitle')}</h1>
            <p className="lede">{t('summaryLede')}</p>
            <p className="summary-note">{t('summaryNote')}</p>
          </header>

          {!grouped.length ? (
            <div className="empty-panel">
              <p>{t('summaryEmpty')}</p>
              <Link className="btn" to="/cast">
                {t('castCta')}
              </Link>
            </div>
          ) : (
            grouped.map((group) => (
              <section key={group.id} className="summary-group" aria-labelledby={`sum-${group.id}`}>
                <h2 id={`sum-${group.id}`}>{group.label}</h2>
                <div className="summary-list">
                  {group.items.map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      className="summary-card"
                      onClick={() => setOpen(item)}
                    >
                      <span className="summary-q">{item.question}</span>
                      {item.timing_hint ? (
                        <span className="summary-timing">{item.timing_hint}</span>
                      ) : null}
                      <span className="summary-preview">
                        {item.answer.slice(0, 140)}
                        {item.answer.length > 140 ? '…' : ''}
                      </span>
                      <span className="summary-cta">{t('summaryOpen')}</span>
                    </button>
                  ))}
                </div>
              </section>
            ))
          )}

          <p className="summary-foot">
            {t('summaryAskHint')}{' '}
            <Link to="/report/ask">{t('summaryAskLink')}</Link>
          </p>

          <DetailDrawer
            open={!!open}
            title={open?.question ?? ''}
            subtitle={open?.timing_hint || open?.category_label}
            onClose={() => setOpen(null)}
          >
            {open && (
              <>
                <p className="summary-drawer-answer">{open.answer}</p>
                <p style={{ marginTop: '1.25rem' }}>
                  <Link
                    className="btn"
                    to={`/report/ask?topic=${encodeURIComponent(open.ask_topic)}`}
                  >
                    {t('summaryAskMore')}
                  </Link>
                </p>
              </>
            )}
          </DetailDrawer>
        </div>
      )}
    </ReportGate>
  )
}
