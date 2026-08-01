import { Link } from 'react-router-dom'
import { ELEMENT_ART, GRAHA_ART } from '../art'
import { TiltCard } from './TiltCard'
import { useLingo } from '../hooks/useLingo'
import type { LifeArea } from '../types'

const AREA_ART: Record<string, string> = {
  career: ELEMENT_ART.Fire,
  education: ELEMENT_ART.Air,
  marriage: ELEMENT_ART.Water,
}

type Props = {
  areas: LifeArea[]
  onOpen: (area: LifeArea) => void
}

export function LifeAreas({ areas, onOpen }: Props) {
  const { t } = useLingo()

  if (!areas.length) return null

  return (
    <section className="life-areas" aria-labelledby="life-areas-title">
      <div className="life-areas-head">
        <h2 id="life-areas-title">{t('lifeAreasTitle')}</h2>
        <p>{t('lifeAreasLede')}</p>
      </div>
      <div className="life-areas-grid">
        {areas.map((area) => (
          <TiltCard
            key={area.id}
            className="life-area-card"
            onClick={() => onOpen(area)}
          >
            <div
              className="life-area-art"
              style={{ backgroundImage: `url('${AREA_ART[area.id] ?? ELEMENT_ART.Earth}')` }}
              aria-hidden
            />
            <div className="life-area-body">
              <span className="life-area-kicker">{area.label}</span>
              <strong className="life-area-headline">{area.headline}</strong>
              <p className="life-area-blurb">{area.blurb}</p>
              <div className="life-area-planets" aria-hidden>
                {area.planets.slice(0, 4).map((p) => (
                  <img key={p} src={GRAHA_ART[p]} alt="" title={p} />
                ))}
              </div>
              <span className="life-area-cta">{t('lifeAreaOpen')}</span>
            </div>
          </TiltCard>
        ))}
      </div>
      <p className="life-areas-foot">
        {t('lifeAreasAskHint')}{' '}
        <Link to="/report/ask">{t('lifeAreasAskLink')}</Link>
      </p>
    </section>
  )
}
