import { useLingo } from '../hooks/useLingo'
import type { ChartPayload } from '../types'
import { PLANET_SHORT } from './PlanetGlyph'
import { RASHI_SHORT } from './RashiGlyph'

type Selection =
  | { kind: 'house'; house: number }
  | { kind: 'planet'; name: string }

type Props = {
  chart: ChartPayload
  selected?: Selection | null
  onSelect: (sel: Selection) => void
}

/** Label anchor points for houses 1-12 in a North-Indian style diamond. */
const HOUSE_POS: Record<number, { x: number; y: number }> = {
  1: { x: 200, y: 70 },
  2: { x: 310, y: 55 },
  3: { x: 345, y: 145 },
  4: { x: 345, y: 255 },
  5: { x: 310, y: 345 },
  6: { x: 200, y: 330 },
  7: { x: 200, y: 255 },
  8: { x: 90, y: 345 },
  9: { x: 55, y: 255 },
  10: { x: 55, y: 145 },
  11: { x: 90, y: 55 },
  12: { x: 200, y: 145 },
}

/** Clickable hit regions (approximate polygons) for each house. */
const HOUSE_HIT: Record<number, string> = {
  1: '200,20 280,100 200,180 120,100',
  2: '280,20 380,20 380,100 280,100',
  3: '300,100 380,100 380,200 300,200',
  4: '300,200 380,200 380,300 300,300',
  5: '280,300 380,300 380,380 280,380',
  6: '200,220 280,300 200,380 120,300',
  7: '200,180 280,260 200,340 120,260',
  8: '20,300 120,300 120,380 20,380',
  9: '20,200 100,200 100,300 20,300',
  10: '20,100 100,100 100,200 20,200',
  11: '20,20 120,20 120,100 20,100',
  12: '120,20 200,20 200,100 120,100',
}

export function KundliDiamond({ chart, selected, onSelect }: Props) {
  const { t } = useLingo()
  return (
    <div className="kundli-wrap">
      <svg
        className="kundli-diamond"
        viewBox="0 0 400 400"
        role="img"
        aria-label="North Indian style kundli chart. Click a house to inspect."
      >
        <defs>
          <linearGradient id="kdFill" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="var(--jade-bright)" stopOpacity="0.12" />
            <stop offset="100%" stopColor="var(--brass)" stopOpacity="0.1" />
          </linearGradient>
        </defs>

        <rect x="20" y="20" width="360" height="360" fill="url(#kdFill)" stroke="var(--ink)" strokeWidth="2" />
        <line x1="20" y1="20" x2="380" y2="380" stroke="var(--ink)" strokeWidth="1.5" strokeOpacity="0.55" />
        <line x1="380" y1="20" x2="20" y2="380" stroke="var(--ink)" strokeWidth="1.5" strokeOpacity="0.55" />
        <line x1="200" y1="20" x2="200" y2="380" stroke="var(--ink)" strokeWidth="1.2" strokeOpacity="0.4" />
        <line x1="20" y1="200" x2="380" y2="200" stroke="var(--ink)" strokeWidth="1.2" strokeOpacity="0.4" />
        <polygon
          className="kd-breathe"
          points="200,20 380,200 200,380 20,200"
          fill="none"
          stroke="var(--brass)"
          strokeWidth="1.5"
          strokeOpacity="0.7"
        />

        {chart.houses.map((h) => {
          const active =
            selected?.kind === 'house' && selected.house === h.number
          const pos = HOUSE_POS[h.number]
          const planets = h.planets.map((p) => PLANET_SHORT[p] ?? p.slice(0, 2)).join(' ')
          return (
            <g key={h.number}>
              <polygon
                points={HOUSE_HIT[h.number]}
                className={`kd-hit${active ? ' active' : ''}`}
                onClick={() => onSelect({ kind: 'house', house: h.number })}
                tabIndex={0}
                role="button"
                aria-label={`House ${h.number} ${h.rashi_name}`}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    onSelect({ kind: 'house', house: h.number })
                  }
                }}
              />
              <text
                x={pos.x}
                y={pos.y - 10}
                textAnchor="middle"
                className="kd-house-num"
                style={{ pointerEvents: 'none' }}
              >
                {h.number}
              </text>
              <text
                x={pos.x}
                y={pos.y + 6}
                textAnchor="middle"
                className="kd-rashi"
                style={{ pointerEvents: 'none' }}
              >
                {RASHI_SHORT[h.rashi_index - 1]}
              </text>
              <text
                x={pos.x}
                y={pos.y + 22}
                textAnchor="middle"
                className="kd-planets"
                style={{ pointerEvents: 'none' }}
              >
                {planets || '·'}
              </text>
            </g>
          )
        })}
      </svg>
      <p className="kd-hint">{t('kdHint')}</p>
    </div>
  )
}
