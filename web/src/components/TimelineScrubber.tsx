import type { DashaPeriod } from '../types'

type Props = {
  periods: DashaPeriod[]
  selectedStart?: string | null
  onSelect: (p: DashaPeriod) => void
  label: string
}

function isNow(start: string, end: string) {
  const t = Date.now()
  return new Date(start).getTime() <= t && t < new Date(end).getTime()
}

function fmt(iso: string) {
  return iso.slice(0, 10)
}

export function TimelineScrubber({ periods, selectedStart, onSelect, label }: Props) {
  return (
    <div className="timeline-scrub">
      <div className="timeline-label">{label}</div>
      <div className="timeline-track" role="list">
        {periods.map((p) => {
          const now = isNow(p.start, p.end)
          const selected = selectedStart === p.start
          return (
            <button
              key={p.lord + p.start}
              type="button"
              role="listitem"
              className={`timeline-seg${now ? ' now' : ''}${selected ? ' selected' : ''}`}
              onClick={() => onSelect(p)}
            >
              <span className="seg-lord">{p.lord}</span>
              <span className="seg-dates">
                {fmt(p.start)} → {fmt(p.end)}
              </span>
              {now && (
                <>
                  <span className="seg-now">now</span>
                  <span className="seg-now-ping" aria-hidden />
                </>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
