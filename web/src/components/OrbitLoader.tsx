import { useEffect, useState } from 'react'
import { useLingo } from '../hooks/useLingo'

const FUNKY_STATUS = [
  'bribing Saturn for cooperation…',
  "counting Moon's padas…",
  'asking Rahu to sit still…',
  'geocoding the hometown vibes…',
  'spinning Lahiri like a DJ…',
]

const PLAIN_STATUS = [
  'Computing Saturn factors…',
  'Resolving Moon nakshatra…',
  'Calculating lunar nodes…',
  'Looking up birth place…',
  'Applying Lahiri ayanamsa…',
]

/** Orbiting planets loader for Cast screen. */
export function OrbitLoader() {
  const { mode } = useLingo()
  const lines = mode === 'funky' ? FUNKY_STATUS : PLAIN_STATUS
  const [i, setI] = useState(0)

  useEffect(() => {
    const id = window.setInterval(() => setI((n) => (n + 1) % lines.length), 1800)
    return () => window.clearInterval(id)
  }, [lines.length])

  return (
    <div className="orbit-loader">
      <svg viewBox="0 0 200 200" className="orbit-svg" aria-hidden>
        <circle cx="100" cy="100" r="28" fill="var(--jade)" opacity="0.85" />
        <circle cx="100" cy="100" r="8" fill="var(--brass-hot)" />
        <g className="orbit-ring orbit-ring-a">
          <circle cx="100" cy="100" r="55" fill="none" stroke="var(--line)" strokeWidth="1" />
          <circle className="orbit-planet" cx="155" cy="100" r="6" fill="var(--brass)" />
          <path
            className="orbit-trail"
            d="M155 100 A55 55 0 0 0 138 55"
            fill="none"
            stroke="var(--brass)"
            strokeWidth="2"
            strokeOpacity="0.45"
          />
        </g>
        <g className="orbit-ring orbit-ring-b">
          <circle cx="100" cy="100" r="75" fill="none" stroke="var(--line)" strokeWidth="1" />
          <circle className="orbit-planet" cx="100" cy="25" r="5" fill="var(--jade-bright)" />
        </g>
        <g className="orbit-ring orbit-ring-c">
          <circle cx="100" cy="100" r="92" fill="none" stroke="var(--line)" strokeWidth="1" />
          <circle className="orbit-planet" cx="40" cy="140" r="4.5" fill="var(--brass-hot)" />
        </g>
      </svg>
      <p className="orbit-status">{lines[i]}</p>
    </div>
  )
}
