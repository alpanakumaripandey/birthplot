import { useRef } from 'react'
import { MagneticButton } from '../components/MagneticButton'
import { RashiWheel } from '../components/RashiWheel'
import { TaglineTicker } from '../components/TaglineTicker'
import { useLingo } from '../hooks/useLingo'
import { usePrefs } from '../hooks/usePrefs'
import { HERO_DAY, HERO_RATRI } from '../art'

export function Home() {
  const { t } = useLingo()
  const { theme, motion } = usePrefs()
  const artRef = useRef<HTMLDivElement>(null)
  const wheelRef = useRef<HTMLDivElement>(null)

  function onMove(e: React.MouseEvent) {
    if (motion === 'calm') return
    const x = (e.clientX / window.innerWidth - 0.5) * 2
    const y = (e.clientY / window.innerHeight - 0.5) * 2
    if (artRef.current) {
      artRef.current.style.transform = `translate(${x * -12}px, ${y * -8}px) scale(1.05)`
    }
    if (wheelRef.current) {
      wheelRef.current.style.transform = `translate(${x * 18}px, ${y * 12}px)`
    }
  }

  return (
    <section className="hero wrap page-enter has-art" onMouseMove={onMove}>
      <div
        ref={artRef}
        className="hero-art hero-parallax-layer"
        style={{ backgroundImage: `url('${theme === 'ratri' ? HERO_RATRI : HERO_DAY}')` }}
        aria-hidden
      />
      <div ref={wheelRef} className="hero-parallax-layer" style={{ position: 'absolute', inset: 0, zIndex: 1, pointerEvents: 'none' }}>
        <RashiWheel />
      </div>
      <div className="hero-copy">
        <h1 className="hero-brand">
          Birth<em>plot</em>
        </h1>
        <TaglineTicker />
        <p className="hero-line">{t('heroLine')}</p>
        <div className="hero-actions">
          <MagneticButton as="link" to="/cast">
            {t('castCta')}
          </MagneticButton>
          <MagneticButton as="link" to="/how" className="btn-ghost" magnetic={false}>
            {t('howCta')}
          </MagneticButton>
        </div>
      </div>
    </section>
  )
}
