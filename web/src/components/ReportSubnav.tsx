import { NavLink } from 'react-router-dom'
import { useLingo } from '../hooks/useLingo'
import type { CopyKey } from '../copy'

const LINKS: { to: string; key: CopyKey }[] = [
  { to: '/report/you', key: 'reportYou' },
  { to: '/report/grahas', key: 'reportGrahas' },
  { to: '/report/houses', key: 'reportHouses' },
  { to: '/report/yogas', key: 'reportYogas' },
  { to: '/report/timing', key: 'reportTiming' },
  { to: '/report/ask', key: 'reportAsk' },
]

export function ReportSubnav() {
  const { t } = useLingo()
  return (
    <nav className="report-subnav" aria-label="Report sections">
      {LINKS.map((l) => (
        <NavLink key={l.to} to={l.to}>
          {t(l.key)}
        </NavLink>
      ))}
    </nav>
  )
}
