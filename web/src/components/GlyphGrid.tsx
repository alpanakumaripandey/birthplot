import { GRAHA_ART } from '../art'
import type { ChartPayload } from '../types'
import { PLANET_ORDER, PlanetGlyph } from './PlanetGlyph'
import { TiltCard } from './TiltCard'

type Props = {
  chart: ChartPayload
  selected?: string | null
  onSelect: (name: string) => void
}

export function GlyphGrid({ chart, selected, onSelect }: Props) {
  return (
    <div className="glyph-grid">
      {PLANET_ORDER.map((name) => {
        const pl = chart.planets[name]
        const active = selected === name
        return (
          <TiltCard
            key={name}
            className={`glyph-tile has-art${active ? ' active' : ''}`}
            onClick={() => onSelect(name)}
          >
            <div
              className="glyph-art-bg"
              style={{
                position: 'absolute',
                inset: 0,
                backgroundImage: `url('${GRAHA_ART[name]}')`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                opacity: 0.35,
                pointerEvents: 'none',
              }}
            />
            <span className="glyph-wiggle" style={{ display: 'grid' }}>
              <PlanetGlyph name={name} size={36} lit />
            </span>
            <strong>{name}</strong>
            <span>
              {pl.info.rashi_name} · H{pl.house}
            </span>
            {pl.info.retrograde && <em className="retro-tag">R</em>}
          </TiltCard>
        )
      })}
    </div>
  )
}
