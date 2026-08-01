import { type FormEvent, useCallback, useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { askQuestion } from '../api'
import { ReportGate } from '../components/ReportGate'
import { TiltCard } from '../components/TiltCard'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'

const TOPICS: { id: string; icon: string }[] = [
  { id: 'career', icon: '↑' },
  { id: 'marriage', icon: '◇' },
  { id: 'love', icon: '♡' },
  { id: 'money', icon: '◈' },
  { id: 'health', icon: '✚' },
  { id: 'education', icon: '☰' },
  { id: 'children', icon: '✧' },
  { id: 'home', icon: '⌂' },
  { id: 'father', icon: '☉' },
  { id: 'mother', icon: '☾' },
  { id: 'foreign', icon: '◎' },
  { id: 'spirituality', icon: '✦' },
]

function formatAnswer(raw: string): string {
  return raw
    .replace(/^##\s+/gm, '')
    .replace(/^#\s+/gm, '')
    .replace(/^\*\s+/gm, '• ')
    .replace(/^-\s+/gm, '• ')
}

export function ReportAsk() {
  const { report, birthRequest } = useChart()
  const { t } = useLingo()
  const [searchParams] = useSearchParams()
  const [q, setQ] = useState('')
  const [answer, setAnswer] = useState<string | null>(null)
  const [help, setHelp] = useState<string | null>(null)
  const [topic, setTopic] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const revealRef = useReveal<HTMLDivElement>()

  const run = useCallback(
    async (question: string) => {
      if (!birthRequest) return
      const trimmed = question.trim()
      if (!trimmed) {
        setError(t('askNeedQuestion'))
        return
      }
      setLoading(true)
      setError(null)
      setAnswer(null)
      setHelp(null)
      setTopic(null)
      setQ(trimmed)
      try {
        const res = await askQuestion(birthRequest, trimmed)
        setAnswer(formatAnswer(res.answer))
        setTopic(res.topic)
        setHelp(res.help)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Ask failed')
      } finally {
        setLoading(false)
      }
    },
    [birthRequest, t],
  )

  useEffect(() => {
    const topicParam = searchParams.get('topic')
    if (topicParam && birthRequest) {
      void run(topicParam)
    }
  }, [searchParams, birthRequest, run])

  function onSubmit(e: FormEvent) {
    e.preventDefault()
    void run(q)
  }

  return (
    <ReportGate>
      {report && (
        <div ref={revealRef}>
          <h1 className="section-title">{t('askTitle')}</h1>
          <p className="lede">{t('askLede')}</p>

          <div className="topic-tiles">
            {TOPICS.map((item) => (
              <TiltCard
                key={item.id}
                className={`topic-tile${topic === item.id ? ' active' : ''}`}
                onClick={() => void run(item.id)}
                disabled={loading}
              >
                <span className="tt-icon">{item.icon}</span>
                {item.id}
              </TiltCard>
            ))}
          </div>

          {error && <div className="error-banner">{error}</div>}

          <form className="form-grid ask-box" onSubmit={onSubmit}>
            <div className="field">
              <label htmlFor="q">{t('askCustomLabel')}</label>
              <textarea
                id="q"
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder={t('askCustomPlaceholder')}
              />
            </div>
            <button className="btn" type="submit" disabled={loading}>
              {loading ? t('askLoading') : t('askSubmit')}
            </button>
          </form>

          {help && !topic && (
            <div className="warn-banner ask-help">
              <strong>{t('askHelpTitle')}</strong>
              <pre className="ask-help-pre">{help}</pre>
            </div>
          )}

          {answer && (
            <div className="ask-answer slide-in">
              {topic && (
                <p style={{ fontWeight: 600, color: 'var(--jade)' }}>
                  {t('askTopic')}: {topic}
                </p>
              )}
              {answer}
            </div>
          )}
        </div>
      )}
    </ReportGate>
  )
}
