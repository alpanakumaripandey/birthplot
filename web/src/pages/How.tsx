import { useState } from 'react'
import { ELEMENT_ART, GRAHA_ART, GRAHA_NAMES, HOW_STEP_ART, HOW_WHEEL } from '../art'
import { HOW_BEGINNER, HOW_SHORT } from '../copy'
import { MagneticButton } from '../components/MagneticButton'
import { useLingo } from '../hooks/useLingo'
import { usePrefs } from '../hooks/usePrefs'

type Track = 'short' | 'beginner'

function renderBody(text: string) {
  return text.split('\n\n').map((block, i) => {
    const lines = block.split('\n')
    return (
      <p key={i} className="how-chapter-p">
        {lines.map((line, j) => {
          const parts = line.split(/(\*\*.+?\*\*)/g)
          return (
            <span key={j}>
              {j > 0 && <br />}
              {parts.map((part, k) =>
                part.startsWith('**') && part.endsWith('**') ? (
                  <strong key={k}>{part.slice(2, -2)}</strong>
                ) : (
                  <span key={k}>{part.replace(/^- /, '• ')}</span>
                ),
              )}
            </span>
          )
        })}
      </p>
    )
  })
}

export function How() {
  const { t } = useLingo()
  const { lingo } = usePrefs()
  const [track, setTrack] = useState<Track>('short')
  const [openId, setOpenId] = useState<string | null>(HOW_SHORT[0].id)
  const [chapter, setChapter] = useState(0)

  const beginner = HOW_BEGINNER[chapter]
  const beginnerArt = HOW_STEP_ART[beginner.art]

  return (
    <section className="section wrap page-enter how-page">
      <div
        className="page-art-band how-hero-band"
        style={{ backgroundImage: `url('${HOW_WHEEL}')` }}
        aria-hidden
      />

      <div className="how-graha-strip" aria-hidden>
        {GRAHA_NAMES.map((name) => (
          <img key={name} src={GRAHA_ART[name]} alt="" className="how-graha-dot" title={name} />
        ))}
      </div>

      <h1 className="section-title">{t('howTitle')}</h1>
      <p className="lede">{t('howLede')}</p>

      <div className="how-track-bar" role="tablist" aria-label="Explanation length">
        <button
          type="button"
          role="tab"
          aria-selected={track === 'short'}
          className={track === 'short' ? 'active' : ''}
          onClick={() => setTrack('short')}
        >
          {t('howTrackShort')}
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={track === 'beginner'}
          className={track === 'beginner' ? 'active' : ''}
          onClick={() => setTrack('beginner')}
        >
          {t('howTrackBeginner')}
        </button>
      </div>
      <p className="how-track-hint">{t('howTrackHint')}</p>

      {track === 'short' && (
        <div className="how-short-grid">
          {HOW_SHORT.map((card) => {
            const open = openId === card.id
            return (
              <button
                key={card.id}
                type="button"
                className={`how-short-card${open ? ' open' : ''}`}
                onClick={() => setOpenId(open ? null : card.id)}
                aria-expanded={open}
              >
                <span
                  className="how-short-art"
                  style={{ backgroundImage: `url('${HOW_STEP_ART[card.art]}')` }}
                />
                <span className="how-short-body">
                  <strong>{card.title[lingo]}</strong>
                  <span>{card.blurb[lingo]}</span>
                  {open && <span className="how-short-more">{card.more[lingo]}</span>}
                </span>
              </button>
            )
          })}
        </div>
      )}

      {track === 'beginner' && (
        <div className="how-beginner">
          <div className="how-beginner-visual">
            <div
              className="how-beginner-art"
              style={{ backgroundImage: `url('${beginnerArt}')` }}
              role="img"
              aria-label={beginner.title[lingo]}
            />
            <div className="how-element-row" aria-hidden>
              {(Object.keys(ELEMENT_ART) as (keyof typeof ELEMENT_ART)[]).map((el) => (
                <img key={el} src={ELEMENT_ART[el]} alt="" title={el} />
              ))}
            </div>
          </div>
          <div className="how-beginner-copy">
            <p className="how-chapter-meta">
              {t('howChapterOf')} {chapter + 1} / {HOW_BEGINNER.length}
            </p>
            <h2 className="how-chapter-title">{beginner.title[lingo]}</h2>
            <div className="how-chapter-body">{renderBody(beginner.body[lingo])}</div>
            <div className="how-chapter-nav">
              <button
                type="button"
                className="btn btn-ghost"
                disabled={chapter === 0}
                onClick={() => setChapter((c) => Math.max(0, c - 1))}
              >
                {t('howPrev')}
              </button>
              <button
                type="button"
                className="btn"
                disabled={chapter >= HOW_BEGINNER.length - 1}
                onClick={() => setChapter((c) => Math.min(HOW_BEGINNER.length - 1, c + 1))}
              >
                {t('howNextChapter')}
              </button>
            </div>
            <div className="how-chapter-dots" role="tablist" aria-label="Chapters">
              {HOW_BEGINNER.map((c, i) => (
                <button
                  key={c.id}
                  type="button"
                  className={i === chapter ? 'active' : ''}
                  aria-label={`${t('howChapterOf')} ${i + 1}`}
                  onClick={() => setChapter(i)}
                />
              ))}
            </div>
          </div>
        </div>
      )}

      <h2 className="how-disclaimer-title">{t('howDisclaimerTitle')}</h2>
      <p className="how-disclaimer">{t('howDisclaimer')}</p>
      <p style={{ marginTop: '1.5rem' }}>
        <MagneticButton as="link" to="/cast">
          {t('castCta')}
        </MagneticButton>
      </p>
    </section>
  )
}
