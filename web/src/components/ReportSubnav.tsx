import { NavLink } from 'react-router-dom'

const LINKS = [
  { to: '/report/you', label: 'You' },
  { to: '/report/grahas', label: 'Grahas' },
  { to: '/report/houses', label: 'Houses' },
  { to: '/report/yogas', label: 'Yogas' },
  { to: '/report/timing', label: 'Timing' },
  { to: '/report/ask', label: 'Ask' },
]

export function ReportSubnav() {
  return (
    <nav className="report-subnav" aria-label="Report sections">
      {LINKS.map((l) => (
        <NavLink key={l.to} to={l.to}>
          {l.label}
        </NavLink>
      ))}
    </nav>
  )
}
