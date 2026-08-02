import { type FormEvent, useState } from 'react'
import { matchCharts } from '../api'
import { OrbitLoader } from '../components/OrbitLoader'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'
import { useSound } from '../hooks/useSound'
import type { ChartRequest, MatchKoota, MatchReport } from '../types'

type PersonForm = {
  name: string
  date: string
  time: string
  place: string
  time_unknown: boolean
}

const EMPTY: PersonForm = {
  name: '',
  date: '',
  time: '',
  place: '',
  time_unknown: false,
}

const DEMO_A: PersonForm = {
  name: 'Mira',
  date: '1991-03-14',
  time: '09:42',
  place: 'Pune, Maharashtra, India',
  time_unknown: false,
}

const DEMO_B: PersonForm = {
  name: 'Kabir',
  date: '1987-11-02',
  time: '16:18',
  place: 'Jaipur, Rajasthan, India',
  time_unknown: false,
}

function toRequest(p: PersonForm): ChartRequest {
  return {
    name: p.name.trim(),
    date: p.date,
    time: p.time_unknown ? null : p.time || null,
    place: p.place.trim(),
    time_unknown: p.time_unknown || !p.time,
  }
}

function personOk(p: PersonForm): boolean {
  return (
    p.name.trim().length > 0 &&
    Boolean(p.date) &&
    p.place.trim().length > 0 &&
    (p.time_unknown || Boolean(p.time))
  )
}

function fmtScore(n: number): string {
  return n % 1 === 0 ? String(n) : n.toFixed(1)
}

function levelLabel(
  level: MatchKoota['level'],
  t: (key: 'matchLevelStrong' | 'matchLevelOk' | 'matchLevelWeak') => string,
): string {
  if (level === 'strong') return t('matchLevelStrong')
  if (level === 'weak') return t('matchLevelWeak')
  return t('matchLevelOk')
}

function PersonFields({
  id,
  label,
  value,
  onChange,
}: {
  id: string
  label: string
  value: PersonForm
  onChange: (next: PersonForm) => void
}) {
  const { t } = useLingo()
  return (
    <fieldset className="match-person">
      <legend>{label}</legend>
      <div className="form-grid">
        <div className="field">
          <label htmlFor={`${id}-name`}>{t('castNameLabel')}</label>
          <input
            id={`${id}-name`}
            type="text"
            value={value.name}
            placeholder={t('castNamePlaceholder')}
            onChange={(e) => onChange({ ...value, name: e.target.value })}
            autoComplete="name"
          />
        </div>
        <div className="field">
          <label htmlFor={`${id}-date`}>{t('castDateLabel')}</label>
          <input
            id={`${id}-date`}
            type="date"
            value={value.date}
            onChange={(e) => onChange({ ...value, date: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor={`${id}-time`}>{t('castTimeLabel')}</label>
          <input
            id={`${id}-time`}
            type="time"
            value={value.time}
            disabled={value.time_unknown}
            onChange={(e) => onChange({ ...value, time: e.target.value })}
          />
        </div>
        <label className="check">
          <input
            type="checkbox"
            checked={value.time_unknown}
            onChange={(e) =>
              onChange({
                ...value,
                time_unknown: e.target.checked,
                time: e.target.checked ? '' : value.time,
              })
            }
          />
          {t('castTimeMystery')}
        </label>
        <div className="field">
          <label htmlFor={`${id}-place`}>{t('castPlaceLabel')}</label>
          <input
            id={`${id}-place`}
            type="text"
            value={value.place}
            placeholder={t('castPlacePlaceholder')}
            onChange={(e) => onChange({ ...value, place: e.target.value })}
            autoComplete="off"
          />
        </div>
      </div>
    </fieldset>
  )
}

function MoonLine({ person }: { person: MatchReport['person_a'] }) {
  const { t } = useLingo()
  return (
    <p className="match-moon">
      <strong>{person.name}</strong> — {t('matchMoonLine')} {person.moon_rashi} /{' '}
      {person.moon_nakshatra} (pada {person.moon_pada})
    </p>
  )
}

export function Match() {
  const { t } = useLingo()
  const { play } = useSound()
  const revealRef = useReveal<HTMLDivElement>()
  const [a, setA] = useState<PersonForm>(EMPTY)
  const [b, setB] = useState<PersonForm>(EMPTY)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<MatchReport | null>(null)

  function loadDemo() {
    setA(DEMO_A)
    setB(DEMO_B)
    setError(null)
    setResult(null)
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (!personOk(a) || !personOk(b)) {
      setError(t('matchNeedBoth'))
      return
    }
    setError(null)
    setLoading(true)
    try {
      const report = await matchCharts({
        person_a: toRequest(a),
        person_b: toRequest(b),
      })
      setResult(report)
      play('success')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Match failed')
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="cast-loading page-enter">
        <OrbitLoader />
        <h1 className="section-title" style={{ marginBottom: 0 }}>
          {t('matchReading')}
        </h1>
      </div>
    )
  }

  return (
    <section ref={revealRef} className="section wrap page-enter match-page">
      <h1 className="section-title">{t('matchTitle')}</h1>
      {!result && <p className="lede">{t('matchLede')}</p>}

      {error && <div className="error-banner">{error}</div>}

      {!result ? (
        <form className="match-form" onSubmit={onSubmit}>
          <div className="match-duo">
            <PersonFields id="person-a" label={t('matchPersonA')} value={a} onChange={setA} />
            <PersonFields id="person-b" label={t('matchPersonB')} value={b} onChange={setB} />
          </div>
          <div className="match-actions">
            <button type="button" className="btn btn-brass" onClick={loadDemo}>
              {t('matchLoadDemo')}
            </button>
            <button type="submit" className="btn">
              {t('matchSubmit')}
            </button>
          </div>
        </form>
      ) : (
        <div className="match-result">
          <div className="match-score-hero">
            <p className="match-score-label">{t('matchScoreLabel')}</p>
            <p className="match-score-num">
              {fmtScore(result.total)}
              <span> / {result.max}</span>
            </p>
            <p className="match-verdict">{result.verdict}</p>
            {result.summary ? <p className="match-summary">{result.summary}</p> : null}
          </div>

          <div className="match-pair-moons">
            <MoonLine person={result.person_a} />
            <MoonLine person={result.person_b} />
          </div>

          {result.action_plan && result.action_plan.length > 0 ? (
            <div className="match-action-plan">
              <h2>{t('matchActionPlan')}</h2>
              <ol>
                {result.action_plan.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ol>
            </div>
          ) : null}

          {(result.strengths?.length || result.watchouts?.length) ? (
            <div className="match-highlights">
              {result.strengths && result.strengths.length > 0 ? (
                <div>
                  <h2>{t('matchStrengths')}</h2>
                  <ul>
                    {result.strengths.map((s) => (
                      <li key={s.name}>
                        <strong>{s.title}</strong> ({s.name}) — {fmtScore(s.score)}/{s.max}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
              {result.watchouts && result.watchouts.length > 0 ? (
                <div>
                  <h2>{t('matchWatchouts')}</h2>
                  <ul>
                    {result.watchouts.map((s) => (
                      <li key={s.name}>
                        <strong>{s.title}</strong> ({s.name}) — {fmtScore(s.score)}/{s.max}
                        {s.problem ? <span className="match-watch-problem"> — {s.problem}</span> : null}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
          ) : null}

          <h2 className="match-breakdown-title">{t('matchBreakdown')}</h2>
          <ul className="match-koota-list">
            {result.kootas.map((k) => (
              <li key={k.id} className={`match-koota match-koota--${k.level ?? 'ok'}`}>
                <div className="match-koota-head">
                  <div>
                    <strong>{k.title ?? k.name}</strong>
                    <span className="match-koota-classic">{k.name} · {k.detail}</span>
                  </div>
                  <div className="match-koota-meta">
                    <span className={`match-level match-level--${k.level ?? 'ok'}`}>
                      {levelLabel(k.level, t)}
                    </span>
                    <span>
                      {fmtScore(k.score)} / {k.max}
                    </span>
                  </div>
                </div>
                <div className="match-koota-bar" aria-hidden>
                  <span style={{ width: `${Math.min(100, (k.score / k.max) * 100)}%` }} />
                </div>
                <p className="match-koota-detail">
                  {k.explanation ?? k.note ?? k.detail}
                </p>
                {k.problem ? (
                  <div className="match-issue">
                    <h3>{t('matchProblem')}</h3>
                    <p>{k.problem}</p>
                  </div>
                ) : null}
                {k.solutions && k.solutions.length > 0 ? (
                  <div className="match-solutions">
                    <h3>{t('matchSolutions')}</h3>
                    <ul>
                      {k.solutions.map((sol) => (
                        <li key={sol}>{sol}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </li>
            ))}
          </ul>

          <div className="match-manglik">
            <h2>{result.manglik_title ?? t('matchManglik')}</h2>
            <p>{result.manglik_note}</p>
            {result.manglik_problem ? (
              <div className="match-issue">
                <h3>{t('matchProblem')}</h3>
                <p>{result.manglik_problem}</p>
              </div>
            ) : null}
            {result.manglik_solutions && result.manglik_solutions.length > 0 ? (
              <div className="match-solutions">
                <h3>{t('matchSolutions')}</h3>
                <ul>
                  {result.manglik_solutions.map((sol) => (
                    <li key={sol}>{sol}</li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>

          <p className="match-convention">{result.convention}</p>

          <button
            type="button"
            className="btn"
            onClick={() => {
              setResult(null)
              play('tap')
            }}
          >
            {t('matchAgain')}
          </button>
        </div>
      )}
    </section>
  )
}
