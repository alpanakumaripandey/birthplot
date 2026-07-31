type Props = {
  rashiIndex: number
  size?: number
  className?: string
}

const MARKS: Record<number, string> = {
  1: 'M16 6l4 10H12L16 6z M10 22h12', // Aries horn-ish
  2: 'M8 18c4-8 12-8 16 0M10 20h12', // Taurus
  3: 'M10 10h12M10 16h12M10 22h12', // Gemini
  4: 'M16 8c-6 4-6 12 0 16 6-4 6-12 0-16z', // Cancer
  5: 'M16 6v20M10 12h12', // Leo-ish
  6: 'M12 8h8v16h-8z M16 8v16', // Virgo-ish
  7: 'M8 22l8-16 8 16H8z', // Libra scales base
  8: 'M16 6c6 4 6 10 0 12-6 2-6 8 0 8', // Scorpio
  9: 'M10 24l6-18 6 18M12 16h8', // Sag
  10: 'M8 10h16v4H8zM12 14v10h8', // Cap
  11: 'M10 22c0-8 12-8 12 0M16 8v6', // Aqu
  12: 'M8 16c4-8 6-2 8 2s4 10 8 2', // Pisces
}

/** Abstract rashi marks (not letters). */
export function RashiGlyph({ rashiIndex, size = 28, className }: Props) {
  const d = MARKS[rashiIndex] ?? MARKS[1]
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      className={className}
      aria-hidden
    >
      <path d={d} fill="none" stroke="var(--jade)" strokeWidth="2" strokeLinecap="round" />
    </svg>
  )
}

export const RASHI_SHORT = [
  'Ar',
  'Ta',
  'Ge',
  'Cn',
  'Le',
  'Vi',
  'Li',
  'Sc',
  'Sg',
  'Cp',
  'Aq',
  'Pi',
]
