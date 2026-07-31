import { useEffect, useState } from 'react'
import { useLingo } from '../hooks/useLingo'

const FUNKY = [
  'your cosmic resume',
  'sky ka screenshot',
  'dashas, decoded',
  'no gatekeeping, only grahas',
]

const PLAIN = [
  'your Vedic birth chart',
  'a clear sky snapshot',
  'timing periods, explained',
  'plain-language Jyotish',
]

export function TaglineTicker() {
  const { mode } = useLingo()
  const lines = mode === 'funky' ? FUNKY : PLAIN
  const [i, setI] = useState(0)

  useEffect(() => {
    const calm =
      typeof document !== 'undefined' &&
      document.documentElement.getAttribute('data-motion') === 'calm'
    if (calm) return
    const id = window.setInterval(() => setI((n) => (n + 1) % lines.length), 4000)
    return () => window.clearInterval(id)
  }, [lines.length])

  return (
    <div className="tagline-ticker" aria-live="polite">
      {lines.map((line, idx) => (
        <span key={line} className={`ticker-line${idx === i ? ' active' : ''}`}>
          {line}
        </span>
      ))}
    </div>
  )
}
