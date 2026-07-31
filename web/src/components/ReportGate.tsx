import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { MagneticButton } from './MagneticButton'
import { ReportSubnav } from './ReportSubnav'

export function ReportGate({ children }: { children: React.ReactNode }) {
  const { report } = useChart()
  const { t } = useLingo()

  if (!report) {
    return (
      <div className="wrap empty-state page-enter">
        <h1 className="section-title">{t('emptyTitle')}</h1>
        <p className="lede">{t('emptyLede')}</p>
        <MagneticButton as="link" to="/cast">
          {t('castCta')}
        </MagneticButton>
      </div>
    )
  }

  const unknown = report.chart.birth.time_unknown

  return (
    <div className="wrap report-layout page-enter">
      <ReportSubnav />
      <div>
        {unknown && (
          <div className="warn-banner">
            Birth time was fuzzy — Lagna may be unreliable. Moon + dasha still help.
          </div>
        )}
        {children}
        <p style={{ marginTop: '2.5rem', fontSize: '0.85rem' }}>
          {report.interpretation.disclaimer}
        </p>
      </div>
    </div>
  )
}
