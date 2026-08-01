import { useEffect, useState } from 'react'
import { useLingo } from '../hooks/useLingo'
import { usePrefs } from '../hooks/usePrefs'

const FUNKY = [
  'janam ka full thali',
  'sky ka screenshot, no filter',
  'dashas decoded, drama optional',
  'no gatekeeping, only grahas',
  'Lagna pe plot twist',
  'Hinglish Jyotish, high clarity',
]

const SICK = [
  "it's giving cosmic resume",
  'sky screenshot, no filter',
  'dashas decoded, lowkey fire',
  'no gatekeep, only grahas',
  'Lagna plot twist unlocked',
  'main character Jyotish',
]

const PLAIN = [
  'your Vedic birth chart',
  'a clear sky snapshot',
  'timing periods, explained',
  'plain-language Jyotish',
  'Lagna, houses, grahas',
  'learn the method, explore freely',
]

export function TaglineTicker() {
  const { mode } = useLingo()
  const { motion } = usePrefs()
  const lines = mode === 'funky' ? FUNKY : mode === 'sick' ? SICK : PLAIN
  const [i, setI] = useState(0)

  useEffect(() => {
    setI(0)
  }, [mode])

  useEffect(() => {
    if (motion === 'calm') return
    const ms = motion === 'drama' ? 2800 : 4000
    const id = window.setInterval(() => setI((n) => (n + 1) % lines.length), ms)
    return () => window.clearInterval(id)
  }, [lines.length, mode, motion])

  return (
    <div className="tagline-ticker" aria-live="polite">
      {lines.map((line, idx) => (
        <span key={`${mode}-${line}`} className={`ticker-line${idx === i ? ' active' : ''}`}>
          {line}
        </span>
      ))}
    </div>
  )
}
