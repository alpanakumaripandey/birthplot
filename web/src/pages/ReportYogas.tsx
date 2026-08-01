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

  const classical = report?.interpretation.yogas.filter(
    (y) => (y.kind ?? 'classical') === 'classical',
  )
  const notes = report?.interpretation.yogas.filter((y) => y.kind === 'note')

  function tile(y: YogaResult) {
    return (
      <TiltCard
        key={y.name}
        className={`yoga-tile ${y.present ? 'lit' : 'dim'}`}
        onClick={() => setYoga(y)}
      >
        <div className="yt-flag">
          {y.present ? t('yogaPresent') : t('yogaQuiet')}
          {y.kind === 'note' ? ` · ${t('yogaNote')}` : ''}
        </div>
        <strong>{y.name}</strong>
      </TiltCard>
    )
  }

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">{t('yogasTitle')}</h1>
          <p className="lede">{t('yogasLede')}</p>

          <h2 className="how-chapter-title" style={{ fontSize: '1.25rem' }}>
            {t('yogaClassical')}
          </h2>
          <div className="yoga-grid">{classical?.map(tile)}</div>

          <h2 className="how-chapter-title" style={{ fontSize: '1.25rem', marginTop: '1.5rem' }}>
            {t('yogaNotes')}
          </h2>
          <p className="lede" style={{ fontSize: '0.92rem' }}>
            {t('yogaNotesLede')}
          </p>
          <div className="yoga-grid">{notes?.map(tile)}</div>

          <DetailDrawer
            open={!!yoga}
            title={yoga?.name ?? ''}
            subtitle={
              yoga?.present
                ? yoga.kind === 'note'
                  ? t('yogaNoteActive')
                  : t('yogaPresentFull')
                : t('yogaQuietFull')
            }
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
