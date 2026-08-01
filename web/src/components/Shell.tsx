import { NavLink, Outlet } from 'react-router-dom'
import { useEffect, useRef, useState } from 'react'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { LogoMark } from './LogoMark'
import { ShootingStars } from './ShootingStars'

export function Shell() {
  const [open, setOpen] = useState(false)
  const { report } = useChart()
  const { t } = useLingo()
  const navRef = useRef<HTMLUListElement>(null)
  const btnRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpen(false)
        btnRef.current?.focus()
      }
    }
    const onPointer = (e: MouseEvent) => {
      const target = e.target as Node
      if (
        navRef.current &&
        !navRef.current.contains(target) &&
        btnRef.current &&
        !btnRef.current.contains(target)
      ) {
        setOpen(false)
      }
    }
    window.addEventListener('keydown', onKey)
    window.addEventListener('mousedown', onPointer)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('mousedown', onPointer)
    }
  }, [open])

  return (
    <div className="shell">
      <ShootingStars />
      <header className="site-nav">
        <NavLink to="/" className="brand" onClick={() => setOpen(false)}>
          <LogoMark size={26} />
          <span>
            Birth<em>plot</em>
          </span>
        </NavLink>

        <button
          ref={btnRef}
          type="button"
          className="nav-toggle"
          aria-label={t('navMenu')}
          aria-expanded={open}
          aria-controls="site-nav-links"
          onClick={() => setOpen((v) => !v)}
        >
          {t('navMenu')}
        </button>
        <ul
          id="site-nav-links"
          ref={navRef}
          className={`nav-links${open ? ' open' : ''}`}
        >
          <li>
            <NavLink to="/cast" onClick={() => setOpen(false)}>
              {t('navCast')}
            </NavLink>
          </li>
          <li>
            <NavLink
              to={report ? '/report/you' : '/report'}
              onClick={() => setOpen(false)}
            >
              {t('navReport')}
            </NavLink>
          </li>
          <li>
            <NavLink to="/lexicon" onClick={() => setOpen(false)}>
              {t('navLexicon')}
            </NavLink>
          </li>
          <li>
            <NavLink to="/how" onClick={() => setOpen(false)}>
              {t('navHow')}
            </NavLink>
          </li>
          <li>
            <NavLink to="/settings" onClick={() => setOpen(false)}>
              {t('navSettings')}
            </NavLink>
          </li>
        </ul>
      </header>
      <main className="shell-main">
        <Outlet />
      </main>
      <footer className="site-footer">{t('footer')}</footer>
    </div>
  )
}
