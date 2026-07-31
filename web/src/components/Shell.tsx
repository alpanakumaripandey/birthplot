import { NavLink, Outlet } from 'react-router-dom'
import { useState } from 'react'
import { useChart } from '../ChartContext'
import { usePrefs } from '../hooks/usePrefs'
import { LogoMark } from './LogoMark'
import { ShootingStars } from './ShootingStars'

export function Shell() {
  const [open, setOpen] = useState(false)
  const { report } = useChart()
  const { theme, motion, lingo, toggleTheme, toggleMotion, toggleLingo } = usePrefs()

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

        <div className="nav-toggles" aria-label="Preferences">
          <button
            type="button"
            className="pref-toggle"
            onClick={toggleTheme}
            title={theme === 'ratri' ? 'Day mode' : 'Ratri mode'}
            aria-pressed={theme === 'ratri'}
          >
            <span className={`pref-icon sun-moon${theme === 'ratri' ? ' is-moon' : ''}`}>
              <span className="pref-sun" />
              <span className="pref-moon" />
            </span>
            <span className="pref-label">{theme === 'ratri' ? 'Ratri' : 'Day'}</span>
          </button>
          <button
            type="button"
            className="pref-toggle"
            onClick={toggleLingo}
            title="Toggle lingo"
            aria-pressed={lingo === 'funky'}
          >
            <span className="pref-label">{lingo === 'funky' ? 'Funky' : 'Seedha'}</span>
          </button>
          <button
            type="button"
            className="pref-toggle"
            onClick={toggleMotion}
            title="Toggle motion"
            aria-pressed={motion === 'drama'}
          >
            <span className="pref-label">{motion === 'drama' ? 'Drama' : 'Calm'}</span>
          </button>
        </div>

        <button
          type="button"
          className="nav-toggle"
          aria-label="Menu"
          onClick={() => setOpen((v) => !v)}
        >
          Menu
        </button>
        <ul className={`nav-links${open ? ' open' : ''}`}>
          <li>
            <NavLink to="/cast" onClick={() => setOpen(false)}>
              Cast
            </NavLink>
          </li>
          <li>
            <NavLink
              to={report ? '/report/you' : '/report'}
              onClick={() => setOpen(false)}
            >
              Report
            </NavLink>
          </li>
          <li>
            <NavLink to="/lexicon" onClick={() => setOpen(false)}>
              Lexicon
            </NavLink>
          </li>
          <li>
            <NavLink to="/how" onClick={() => setOpen(false)}>
              How
            </NavLink>
          </li>
        </ul>
      </header>
      <main className="shell-main">
        <Outlet />
      </main>
      <footer className="site-footer">
        Birthplot · Jyotish for curious humans · Learning guidance, not destiny decrees
      </footer>
    </div>
  )
}

