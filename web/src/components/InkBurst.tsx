import { useEffect, useState, type CSSProperties } from 'react'

type Props = {
  active: boolean
  onDone?: () => void
}

/** One-shot jade/brass ink burst overlay (~800ms). */
export function InkBurst({ active, onDone }: Props) {
  const [show, setShow] = useState(false)

  useEffect(() => {
    if (!active) return
    setShow(true)
    const t = window.setTimeout(() => {
      setShow(false)
      onDone?.()
    }, 850)
    return () => window.clearTimeout(t)
  }, [active, onDone])

  if (!show) return null

  const dots = Array.from({ length: 18 }, (_, i) => i)

  return (
    <div className="ink-burst" aria-hidden>
      <svg viewBox="0 0 200 200" className="ink-burst-svg">
        {dots.map((i) => {
          const a = (i / dots.length) * Math.PI * 2
          const x = 100 + Math.cos(a) * 70
          const y = 100 + Math.sin(a) * 70
          return (
            <circle
              key={i}
              className="ink-dot"
              cx="100"
              cy="100"
              r={i % 3 === 0 ? 5 : 3}
              fill={i % 2 === 0 ? 'var(--jade-bright)' : 'var(--brass)'}
              style={
                {
                  '--tx': `${x - 100}px`,
                  '--ty': `${y - 100}px`,
                  animationDelay: `${i * 18}ms`,
                } as CSSProperties
              }
            />
          )
        })}
        <circle className="ink-ring" cx="100" cy="100" r="8" fill="none" stroke="var(--brass)" />
      </svg>
    </div>
  )
}
