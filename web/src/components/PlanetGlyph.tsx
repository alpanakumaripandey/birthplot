const SIZE = 28

type Props = {
  name: string
  size?: number
  lit?: boolean
  className?: string
}

/** Minimal classical-style planet glyphs (inline SVG). */
export function PlanetGlyph({ name, size = SIZE, lit = true, className }: Props) {
  const stroke = lit ? 'var(--jade)' : 'var(--ink-soft)'
  const fill = lit ? 'var(--brass)' : 'transparent'
  const opacity = lit ? 1 : 0.45
  const common = {
    width: size,
    height: size,
    viewBox: '0 0 32 32',
    fill: 'none',
    className,
    style: { opacity },
    'aria-hidden': true as const,
  }

  switch (name) {
    case 'Sun':
      return (
        <svg {...common}>
          <circle cx="16" cy="16" r="6" stroke={stroke} strokeWidth="2" fill={fill} />
          {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => {
            const r = (deg * Math.PI) / 180
            return (
              <line
                key={deg}
                x1={16 + Math.cos(r) * 9}
                y1={16 + Math.sin(r) * 9}
                x2={16 + Math.cos(r) * 13}
                y2={16 + Math.sin(r) * 13}
                stroke={stroke}
                strokeWidth="2"
              />
            )
          })}
        </svg>
      )
    case 'Moon':
      return (
        <svg {...common}>
          <path
            d="M20 8a9 9 0 1 0 0 16 7 7 0 1 1 0-16z"
            stroke={stroke}
            strokeWidth="2"
            fill={fill}
          />
        </svg>
      )
    case 'Mars':
      return (
        <svg {...common}>
          <circle cx="13" cy="19" r="7" stroke={stroke} strokeWidth="2" />
          <path d="M18 14l8-8M26 6h-6M26 6v6" stroke={stroke} strokeWidth="2" />
        </svg>
      )
    case 'Mercury':
      return (
        <svg {...common}>
          <circle cx="16" cy="14" r="6" stroke={stroke} strokeWidth="2" />
          <path d="M16 20v7M12 27h8M10 8c2-3 10-3 12 0" stroke={stroke} strokeWidth="2" />
        </svg>
      )
    case 'Jupiter':
      return (
        <svg {...common}>
          <path d="M10 8h12M18 8v16M10 24h10" stroke={stroke} strokeWidth="2.2" />
          <path d="M8 14h10" stroke={stroke} strokeWidth="2.2" />
        </svg>
      )
    case 'Venus':
      return (
        <svg {...common}>
          <circle cx="16" cy="12" r="6" stroke={stroke} strokeWidth="2" />
          <path d="M16 18v9M12 23h8" stroke={stroke} strokeWidth="2" />
        </svg>
      )
    case 'Saturn':
      return (
        <svg {...common}>
          <path d="M18 6v14M12 20h12" stroke={stroke} strokeWidth="2.2" />
          <path d="M14 10c4-4 10 0 6 5" stroke={stroke} strokeWidth="2" />
          <circle cx="18" cy="24" r="2.5" fill={stroke} />
        </svg>
      )
    case 'Rahu':
      return (
        <svg {...common}>
          <path
            d="M6 20c4-10 16-10 20 0M8 18c3-2 13-2 16 0"
            stroke={stroke}
            strokeWidth="2"
          />
          <circle cx="10" cy="20" r="3" stroke={stroke} strokeWidth="2" fill={fill} />
          <circle cx="22" cy="20" r="3" stroke={stroke} strokeWidth="2" fill={fill} />
        </svg>
      )
    case 'Ketu':
      return (
        <svg {...common}>
          <path d="M16 6l3 10H13L16 6z" stroke={stroke} strokeWidth="2" fill={fill} />
          <path d="M16 16c-6 2-8 8-2 10 6 0 8-6 2-10z" stroke={stroke} strokeWidth="2" />
        </svg>
      )
    default:
      return (
        <svg {...common}>
          <circle cx="16" cy="16" r="8" stroke={stroke} strokeWidth="2" />
          <text x="16" y="20" textAnchor="middle" fontSize="10" fill={stroke}>
            ?
          </text>
        </svg>
      )
  }
}

export const PLANET_ORDER = [
  'Sun',
  'Moon',
  'Mars',
  'Mercury',
  'Jupiter',
  'Venus',
  'Saturn',
  'Rahu',
  'Ketu',
] as const

export const PLANET_SHORT: Record<string, string> = {
  Sun: 'Su',
  Moon: 'Mo',
  Mars: 'Ma',
  Mercury: 'Me',
  Jupiter: 'Ju',
  Venus: 'Ve',
  Saturn: 'Sa',
  Rahu: 'Ra',
  Ketu: 'Ke',
}
