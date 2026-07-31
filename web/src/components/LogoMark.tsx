type Props = {
  size?: number
  className?: string
  animated?: boolean
}

/** Birthplot diamond-in-orbit mark — draws on load, spins on hover. */
export function LogoMark({ size = 28, className = '', animated = true }: Props) {
  return (
    <svg
      className={`logo-mark${animated ? ' logo-mark--animated' : ''} ${className}`}
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      aria-hidden
    >
      <polygon
        className="logo-outer"
        points="32,8 56,32 32,56 8,32"
        stroke="var(--brass)"
        strokeWidth="2.5"
        fill="none"
      />
      <polygon
        className="logo-inner"
        points="32,18 46,32 32,46 18,32"
        fill="var(--jade)"
        opacity="0.9"
      />
      <circle cx="32" cy="32" r="3.5" fill="var(--brass-hot)" />
      <g className="logo-orbit">
        <circle cx="32" cy="8" r="2.4" fill="var(--jade-bright)" />
        <circle cx="56" cy="32" r="2.4" fill="var(--jade-bright)" />
        <circle cx="32" cy="56" r="2.4" fill="var(--jade-bright)" />
        <circle cx="8" cy="32" r="2.4" fill="var(--jade-bright)" />
      </g>
    </svg>
  )
}
