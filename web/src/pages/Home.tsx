import { lazy, Suspense, useRef, useState } from 'react'
import { ELEMENT_ART, GRAHA_ART, GRAHA_NAMES, HERO_DAY, HERO_RATRI, LOOP_GIF } from '../art'
import { MagneticButton } from '../components/MagneticButton'
import { RashiWheel } from '../components/RashiWheel'
import { TaglineTicker } from '../components/TaglineTicker'
import { useLingo } from '../hooks/useLingo'
import { usePrefs } from '../hooks/usePrefs'
import { useSound } from '../hooks/useSound'

const Starfield3D = lazy(() =>
  import('../components/Starfield3D').then((m) => ({ default: m.Starfield3D })),
)

export function Home() {
  const { t } = useLingo()
  const { theme, motion } = usePrefs()
  const { play } = useSound()
  const artRef = useRef<HTMLDivElement>(null)
  const wheelRef = useRef<HTMLDivElement>(null)
  const [hot, setHot] = useState<string | null>(null)

  function onMove(e: React.MouseEvent) {
    if (motion === 'calm') return
    const x = (e.clientX / window.innerWidth - 0.5) * 2
    const y = (e.clientY / window.innerHeight - 0.5) * 2
    if (artRef.current) {
      artRef.current.style.transform = `translate(${x * -22}px, ${y * -14}px) scale(1.08)`
    }
    if (wheelRef.current) {
      wheelRef.current.style.transform = `translate(${x * 18}px, ${y * 14}px) rotate(${x * 3}deg)`
    }
  }

  return (
    <section className="hero wrap page-enter has-art" onMouseMove={onMove}>
      {motion === 'drama' && (
        <Suspense fallback={null}>
          <Starfield3D />
        </Suspense>
      )}
      <div
        ref={artRef}
        className="hero-art hero-parallax-layer"
        style={{ backgroundImage: `url('${theme === 'ratri' ? HERO_RATRI : HERO_DAY}')` }}
        aria-hidden
      />
      {motion === 'drama' && (
        <img className="hero-gif-sky" src={LOOP_GIF.nakshatra} alt="" aria-hidden />
      )}
      <div ref={wheelRef} className="hero-wheel-layer" aria-hidden>
        <RashiWheel />
        {motion === 'drama' && (
          <img className="hero-gif-orbit" src={LOOP_GIF.orbit} alt="" aria-hidden />
        )}
      </div>
      <div className="hero-copy">
        <h1 className="hero-brand">
          Birth<em>plot</em>
        </h1>
        <TaglineTicker />
        <p className="hero-line">{t('heroLine')}</p>
        <div className="hero-actions">
          <MagneticButton as="link" to="/cast" onClick={() => play('tap')}>
            {t('castCta')}
          </MagneticButton>
          <MagneticButton as="link" to="/how" className="btn-ghost" magnetic={false}>
            {t('howCta')}
          </MagneticButton>
        </div>

        <div className="hero-graha-orbit" aria-label="Graha gallery">
          {GRAHA_NAMES.map((name, i) => (
            <button
              key={name}
              type="button"
              className={`hero-graha-chip${hot === name ? ' hot' : ''}`}
              style={{ ['--i' as string]: i }}
              onMouseEnter={() => setHot(name)}
              onMouseLeave={() => setHot(null)}
              onFocus={() => setHot(name)}
              onBlur={() => setHot(null)}
              onClick={() => play('tap')}
              title={name}
            >
              <img src={GRAHA_ART[name]} alt={name} />
            </button>
          ))}
        </div>
        {hot && <p className="hero-graha-label">{hot}</p>}

        <div className="hero-elements" aria-hidden>
          {(Object.keys(ELEMENT_ART) as (keyof typeof ELEMENT_ART)[]).map((el) => (
            <span key={el} className="hero-element-pill" title={el}>
              <img src={ELEMENT_ART[el]} alt="" />
            </span>
          ))}
        </div>
      </div>
    </section>
  )
}
