import { type FormEvent, useCallback, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createChart } from '../api'
import { CAST_ART } from '../art'
import { useChart } from '../ChartContext'
import { InkBurst } from '../components/InkBurst'
import { MagneticButton } from '../components/MagneticButton'
import { OrbitLoader } from '../components/OrbitLoader'
import { useLingo } from '../hooks/useLingo'
import { useSound } from '../hooks/useSound'

type Demo = {
  name: string
  date: string
  time: string
  place: string
  time_unknown: boolean
}

const DEMOS: Demo[] = [
  {
    name: 'Mira',
    date: '1991-03-14',
    time: '09:42',
    place: 'Pune, Maharashtra, India',
    time_unknown: false,
  },
  {
    name: 'Kabir',
    date: '1987-11-02',
    time: '16:18',
    place: 'Jaipur, Rajasthan, India',
    time_unknown: false,
  },
  {
    name: 'Leela',
    date: '2001-07-29',
    time: '05:05',
    place: 'Kochi, Kerala, India',
    time_unknown: false,
  },
  {
    name: 'Arun',
    date: '1995-12-08',
    time: '21:30',
    place: 'Varanasi, Uttar Pradesh, India',
    time_unknown: false,
  },
]

function pickDemo(excludeName?: string): Demo {
  const pool = excludeName ? DEMOS.filter((d) => d.name !== excludeName) : DEMOS
  return pool[Math.floor(Math.random() * pool.length)] ?? DEMOS[0]
}

export function Cast() {
  const navigate = useNavigate()
  const { setReport } = useChart()
  const { t } = useLingo()
  const { play } = useSound()
  const [step, setStep] = useState(0)
  const [name, setName] = useState('')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [place, setPlace] = useState('')
  const [timeUnknown, setTimeUnknown] = useState(false)
  const [loading, setLoading] = useState(false)
  const [burst, setBurst] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [demoNote, setDemoNote] = useState<string | null>(null)

  const whoOk = name.trim().length > 0
  const whenOk = Boolean(date) && (timeUnknown || Boolean(time))
  const whereOk = place.trim().length > 0
  const stepOk = [whoOk, whenOk, whereOk]

  function loadDemo() {
    const demo = pickDemo(name)
    setName(demo.name)
    setDate(demo.date)
    setTime(demo.time)
    setPlace(demo.place)
    setTimeUnknown(demo.time_unknown)
    setError(null)
    setDemoNote(`Demo: ${demo.name}`)
    setStep(2)
  }

  function goStep(i: number) {
    if (i > step) {
      for (let s = 0; s < i; s++) {
        if (!stepOk[s]) {
          setError(t('castIncomplete'))
          setStep(s)
          return
        }
      }
    }
    setError(null)
    setStep(i)
  }

  const goReport = useCallback(() => {
    navigate('/report/you')
  }, [navigate])

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (step === 0) {
      if (!whoOk) {
        setError(t('castNeedName'))
        return
      }
      setError(null)
      setStep(1)
      return
    }
    if (step === 1) {
      if (!date) {
        setError(t('castNeedDate'))
        return
      }
      if (!timeUnknown && !time) {
        setError(t('castNeedTime'))
        return
      }
      setError(null)
      setStep(2)
      return
    }
    if (!whoOk || !whenOk || !whereOk) {
      setError(t('castIncomplete'))
      if (!whoOk) setStep(0)
      else if (!whenOk) setStep(1)
      return
    }
    setError(null)
    setLoading(true)
    try {
      const report = await createChart({
        name: name.trim(),
        date,
        time: timeUnknown ? null : time || null,
        place: place.trim(),
        time_unknown: timeUnknown || !time,
      })
      setReport(report)
      setLoading(false)
      setBurst(true)
      play('success')
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

  const stepLabels = [t('castStepWho'), t('castStepWhen'), t('castStepWhere')]

  return (
    <section className="section wrap page-enter">
      <InkBurst active={burst} onDone={goReport} />
      <h1 className="section-title">{t('castTitle')}</h1>
      <p className="lede">{t('castLede')}</p>

      {error && <div className="error-banner">{error}</div>}

      <div className="cast-layout">
        <div>
          <div className="step-rail" role="tablist" aria-label={t('castTitle')}>
            {stepLabels.map((label, i) => (
              <button
                key={label}
                type="button"
                role="tab"
                aria-selected={step === i}
                className={`${step === i ? 'active' : ''} ${stepOk[i] ? 'done' : ''}`}
                onClick={() => goStep(i)}
              >
                {i + 1}. {label}
              </button>
            ))}
          </div>

          <div className="sample-block">
            <button type="button" className="btn btn-brass" onClick={loadDemo}>
              {t('loadSample')}
            </button>
            {demoNote && (
              <p className="sample-caption">
                <strong>{demoNote}</strong> — {t('sampleCaption')}
              </p>
            )}
          </div>

          <form className="form-grid" onSubmit={onSubmit} noValidate>
            {step === 0 && (
              <div className="field">
                <label htmlFor="name">{t('castNameLabel')}</label>
                <input
                  id="name"
                  type="text"
                  required
                  value={name}
                  onChange={(e) => {
                    setName(e.target.value)
                    setDemoNote(null)
                  }}
                  placeholder={t('castNamePlaceholder')}
                />
              </div>
            )}

            {step === 1 && (
              <>
                <div className="field">
                  <label htmlFor="date">{t('castDateLabel')}</label>
                  <input
                    id="date"
                    type="date"
                    required
                    value={date}
                    onChange={(e) => {
                      setDate(e.target.value)
                      setDemoNote(null)
                    }}
                  />
                </div>
                <div className="field">
                  <label htmlFor="time">{t('castTimeLabel')}</label>
                  <input
                    id="time"
                    type="time"
                    required={!timeUnknown}
                    value={time}
                    disabled={timeUnknown}
                    onChange={(e) => {
                      setTime(e.target.value)
                      setDemoNote(null)
                    }}
                  />
                </div>
                <label className="check">
                  <input
                    type="checkbox"
                    checked={timeUnknown}
                    onChange={(e) => setTimeUnknown(e.target.checked)}
                  />
                  {t('castTimeMystery')}
                </label>
              </>
            )}

            {step === 2 && (
              <div className="field">
                <label htmlFor="place">{t('castPlaceLabel')}</label>
                <input
                  id="place"
                  type="text"
                  required
                  value={place}
                  onChange={(e) => {
                    setPlace(e.target.value)
                    setDemoNote(null)
                  }}
                  placeholder={t('castPlacePlaceholder')}
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
          style={{ backgroundImage: `url('${CAST_ART}')` }}
          role="img"
          aria-label="Cast ritual illustration"
        />
      </div>
    </section>
  )
}
