import { useState } from 'react'
import { DetailDrawer } from '../components/DetailDrawer'
import { ReportGate } from '../components/ReportGate'
import { TiltCard } from '../components/TiltCard'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import type { YogaResult } from '../types'

export function ReportYogas() {
  const { report } = useChart()
  const { t } = useLingo()
  const [yoga, setYoga] = useState<YogaResult | null>(null)
  const revealRef = useReveal<HTMLDivElement>()

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">{t('yogasTitle')}</h1>
          <p className="lede">{t('yogasLede')}</p>

          <div className="yoga-grid">
            {report.interpretation.yogas.map((y) => (
              <TiltCard
                key={y.name}
                className={`yoga-tile ${y.present ? 'lit' : 'dim'}`}
                onClick={() => setYoga(y)}
              >
                <div className="yt-flag">{y.present ? 'Present' : 'Quiet'}</div>
                <strong>{y.name}</strong>
              </TiltCard>
            ))}
          </div>

          <DetailDrawer
            open={!!yoga}
            title={yoga?.name ?? ''}
            subtitle={yoga?.present ? 'Present in this chart' : 'Not active here'}
            onClose={() => setYoga(null)}
          >
            {yoga && (
              <>
                <p>{yoga.detail}</p>
                <p>{yoga.meaning}</p>
              </>
            )}
          </DetailDrawer>
        </div>
      )}
    </ReportGate>
  )
}
