import { type FormEvent, useState } from 'react'
import { askQuestion } from '../api'
import { ReportGate } from '../components/ReportGate'
import { TiltCard } from '../components/TiltCard'
import { useChart } from '../ChartContext'
import { useLingo } from '../hooks/useLingo'
import { useReveal } from '../hooks/useReveal'

const TOPICS: { id: string; icon: string }[] = [
  { id: 'career', icon: '↑' },
  { id: 'marriage', icon: '◇' },
  { id: 'money', icon: '◈' },
  { id: 'health', icon: '✚' },
  { id: 'education', icon: '☰' },
  { id: 'love', icon: '♡' },
  { id: 'foreign', icon: '◎' },
  { id: 'spirituality', icon: '✧' },
]

export function ReportAsk() {
  const { report, birthRequest } = useChart()
  const { t } = useLingo()
  const [q, setQ] = useState('career')
  const [answer, setAnswer] = useState<string | null>(null)
  const [topic, setTopic] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const revealRef = useReveal<HTMLDivElement>()

  async function run(question: string) {
    if (!birthRequest) return
    setLoading(true)
    setError(null)
    setQ(question)
    try {
      const res = await askQuestion(birthRequest, question)
      setAnswer(res.answer)
      setTopic(res.topic)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ask failed')
    } finally {
      setLoading(false)
    }
  }

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
                className={`topic-tile${topic === item.id || q === item.id ? ' active' : ''}`}
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
              <label htmlFor="q">Custom question</label>
              <textarea
                id="q"
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="career, marriage, money…"
              />
            </div>
            <button className="btn" type="submit" disabled={loading}>
              {loading ? 'Consulting the sky…' : 'Ask'}
            </button>
          </form>

          {answer && (
            <div className="ask-answer slide-in">
              {topic && (
                <p style={{ fontWeight: 600, color: 'var(--jade)' }}>Topic: {topic}</p>
              )}
              {answer}
            </div>
          )}
        </div>
      )}
    </ReportGate>
  )
}
