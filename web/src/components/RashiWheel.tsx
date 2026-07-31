type Props = { className?: string }

const SIGNS = [
  'Me', 'Vr', 'Mi', 'Ka', 'Si', 'Kn', 'Tu', 'Vs', 'Dh', 'Ma', 'Ku', 'Mn',
]

export function RashiWheel({ className = 'rashi-wheel' }: Props) {
  const r = 180
  const cx = 200
  const cy = 200
  return (
    <svg
      className={className}
      viewBox="0 0 400 400"
      aria-hidden="true"
      role="presentation"
    >
      <defs>
        <radialGradient id="wheelGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#2a9a93" stopOpacity="0.25" />
          <stop offset="70%" stopColor="#1f6f6a" stopOpacity="0.08" />
          <stop offset="100%" stopColor="#1a2428" stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle cx={cx} cy={cy} r={r} fill="url(#wheelGlow)" />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1a2428" strokeOpacity="0.35" strokeWidth="1.5" />
      <circle cx={cx} cy={cy} r={r * 0.72} fill="none" stroke="#b08d57" strokeOpacity="0.55" strokeWidth="1" />
      <circle cx={cx} cy={cy} r={r * 0.42} fill="none" stroke="#1f6f6a" strokeOpacity="0.45" strokeWidth="1" />
      {SIGNS.map((label, i) => {
        const a = ((i / 12) * Math.PI * 2) - Math.PI / 2
        const x2 = cx + Math.cos(a) * r
        const y2 = cy + Math.sin(a) * r
        const tx = cx + Math.cos(a + Math.PI / 12) * (r * 0.86)
        const ty = cy + Math.sin(a + Math.PI / 12) * (r * 0.86)
        return (
          <g key={label + i}>
            <line x1={cx} y1={cy} x2={x2} y2={y2} stroke="#1a2428" strokeOpacity="0.2" />
            <text
              x={tx}
              y={ty}
              textAnchor="middle"
              dominantBaseline="middle"
              fill="#1a2428"
              fillOpacity="0.55"
              fontSize="11"
              fontFamily="DM Sans, sans-serif"
            >
              {label}
            </text>
          </g>
        )
      })}
      <circle cx={cx} cy={cy} r="6" fill="#b08d57" />
    </svg>
  )
}
