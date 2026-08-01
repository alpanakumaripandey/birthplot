import { Link } from 'react-router-dom'
import { GRAHA_ART, NAKSHATRA_SKY } from '../art'
import { useLingo } from '../hooks/useLingo'
import type { FullReport } from '../types'

type Props = {
  report: FullReport
}

export function MajorSummary({ report }: Props) {
  const { t } = useLingo()
  const { chart, timeline, interpretation } = report
  const maha = timeline.current_mahadasha
  const antar = timeline.current_antardasha
  const yogasOn = interpretation.yogas.filter(
    (y) => y.present && (y.kind ?? 'classical') === 'classical',
  )
  const topNotes = interpretation.strengths.slice(0, 4)

  const dashaLine = maha
    ? antar
      ? `${maha.lord} → ${antar.lord}`
      : maha.lord
    : '—'

  return (
    <section className="major-summary" aria-labelledby="major-summary-title">
      <div className="major-summary-head">
        <h2 id="major-summary-title">{t('majorTitle')}</h2>
        <p>{t('majorLede')}</p>
      </div>

      <div className="major-grid">
        <article className="major-card">
          <span className="major-kicker">{t('majorLagna')}</span>
          <strong>{chart.lagna.rashi_name}</strong>
          <span>
            {chart.lagna.degree_in_rashi.toFixed(1)}° ·{' '}
            {chart.birth.time_unknown ? t('majorTimeUnknown') : t('majorRising')}
          </span>
        </article>

        <article
          className="major-card major-card-art"
          style={{ backgroundImage: `url('${NAKSHATRA_SKY}')` }}
        >
          <span className="major-kicker">{t('majorMoon')}</span>
          <strong>
            {chart.moon_nakshatra} · pada {chart.moon_pada}
          </strong>
          <span>
            {chart.planets.Moon.info.rashi_name} · H{chart.planets.Moon.house}
          </span>
        </article>

        <Link to="/report/timing" className="major-card major-card-link">
          <span className="major-kicker">{t('majorDasha')}</span>
          <strong>{dashaLine}</strong>
          <span>
            {maha
              ? `${maha.start.slice(0, 10)} → ${maha.end.slice(0, 10)}`
              : t('majorDashaEmpty')}
          </span>
        </Link>

        <Link to="/report/yogas" className="major-card major-card-link">
          <span className="major-kicker">{t('majorYogas')}</span>
          <strong>
            {yogasOn.length
              ? yogasOn
                  .slice(0, 3)
                  .map((y) => y.name.replace(/ Yoga.*$/, ''))
                  .join(' · ')
              : t('majorYogasNone')}
          </strong>
          <span>
            {yogasOn.length
              ? t('majorYogasCount').replace('{n}', String(yogasOn.length))
              : t('majorYogasHint')}
          </span>
        </Link>
      </div>

      {topNotes.length > 0 && (
        <div className="major-notes">
          <h3>{t('majorNotes')}</h3>
          <ul>
            {topNotes.map((note) => (
              <li key={note.slice(0, 64)}>{note}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="major-graha-row" aria-hidden>
        {Object.keys(chart.planets)
          .slice(0, 9)
          .map((name) => (
            <img key={name} src={GRAHA_ART[name]} alt="" title={name} />
          ))}
      </div>
    </section>
  )
}
