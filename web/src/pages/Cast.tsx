import { type FormEvent, useCallback, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createChart } from '../api'
import { useChart } from '../ChartContext'
import { InkBurst } from '../components/InkBurst'
import { MagneticButton } from '../components/MagneticButton'
import { OrbitLoader } from '../components/OrbitLoader'
import { useLingo } from '../hooks/useLingo'

const AMIT = {
  name: 'Amit',
  date: '1998-05-20',
  time: '20:00',
  place: 'Sarni, Madhya Pradesh, India',
  time_unknown: false,
}

export function Cast() {
  const navigate = useNavigate()
  const { setReport } = useChart()
  const { t } = useLingo()
  const [step, setStep] = useState(0)
  const [name, setName] = useState('')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [place, setPlace] = useState('')
  const [timeUnknown, setTimeUnknown] = useState(false)
  const [loading, setLoading] = useState(false)
  const [burst, setBurst] = useState(false)
  const [error, setError] = useState<string | null>(null)

  function loadAmit() {
    setName(AMIT.name)
    setDate(AMIT.date)
    setTime(AMIT.time)
    setPlace(AMIT.place)
    setTimeUnknown(false)
    setError(null)
    setStep(2)
  }

  const goReport = useCallback(() => {
    navigate('/report/you')
  }, [navigate])

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (step < 2) {
      setStep((s) => s + 1)
      return
    }
    setError(null)
    setLoading(true)
    try {
      const report = await createChart({
        name: name.trim() || 'Friend',
        date,
        time: timeUnknown ? null : time || null,
        place: place.trim(),
        time_unknown: timeUnknown,
      })
      setReport(report)
      setLoading(false)
      setBurst(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Casting failed')
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="cast-loading page-enter">
        <OrbitLoader />
        <h1 className="section-title" style={{ marginBottom: 0 }}>
          {t('readingSky')}
        </h1>
        <p className="lede">{t('readingLede')}</p>
      </div>
    )
  }

  return (
    <section className="section wrap page-enter">
      <InkBurst active={burst} onDone={goReport} />
      <h1 className="section-title">{t('castTitle')}</h1>
      <p className="lede">{t('castLede')}</p>

      {error && <div className="error-banner">{error}</div>}

      <div className="cast-layout">
        <div>
          <div className="step-rail" role="tablist">
            {['Identity', 'When', 'Where'].map((label, i) => (
              <button
                key={label}
                type="button"
                role="tab"
                className={`${step === i ? 'active' : ''} ${i < step ? 'done' : ''}`}
                onClick={() => setStep(i)}
              >
                {i + 1}. {label}
              </button>
            ))}
          </div>

          <p style={{ marginBottom: '1rem' }}>
            <button type="button" className="btn btn-brass" onClick={loadAmit}>
              {t('loadAmit')}
            </button>
          </p>

          <form className="form-grid" onSubmit={onSubmit}>
            {step === 0 && (
              <div className="field">
                <label htmlFor="name">Name</label>
                <input
                  id="name"
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Who's the protagonist?"
                />
              </div>
            )}

            {step === 1 && (
              <>
                <div className="field">
                  <label htmlFor="date">Date of birth</label>
                  <input
                    id="date"
                    type="date"
                    required
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                  />
                </div>
                <div className="field">
                  <label htmlFor="time">Birth time</label>
                  <input
                    id="time"
                    type="time"
                    value={time}
                    disabled={timeUnknown}
                    onChange={(e) => setTime(e.target.value)}
                  />
                </div>
                <label className="check">
                  <input
                    type="checkbox"
                    checked={timeUnknown}
                    onChange={(e) => setTimeUnknown(e.target.checked)}
                  />
                  Time is a mystery (noon stand-in)
                </label>
              </>
            )}

            {step === 2 && (
              <div className="field">
                <label htmlFor="place">Place of birth</label>
                <input
                  id="place"
                  type="text"
                  required
                  value={place}
                  onChange={(e) => setPlace(e.target.value)}
                  placeholder="City, State, Country"
                />
              </div>
            )}

            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
              {step > 0 && (
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={() => setStep((s) => s - 1)}
                >
                  {t('back')}
                </button>
              )}
              <MagneticButton as="button" type="submit">
                {step < 2 ? t('next') : t('castIt')}
              </MagneticButton>
            </div>
          </form>
        </div>

        <div
          className="cast-art"
          style={{ backgroundImage: "url('/art/cast-ritual.png')" }}
          role="img"
          aria-label="Cast ritual illustration"
        />
      </div>
    </section>
  )
}
