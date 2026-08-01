import { usePrefs, type LingoMode, type MotionMode, type ThemeMode } from '../hooks/usePrefs'
import { useLingo } from '../hooks/useLingo'
import { useSound } from '../hooks/useSound'

type RowProps<T extends string> = {
  label: string
  hint: string
  value: T
  options: { id: T; title: string; blurb: string }[]
  onChange: (v: T) => void
}

function SettingRow<T extends string>({ label, hint, value, options, onChange }: RowProps<T>) {
  return (
    <div className="settings-row">
      <div className="settings-row-head">
        <h2>{label}</h2>
        <p>{hint}</p>
      </div>
      <div className="settings-options" role="radiogroup" aria-label={label}>
        {options.map((opt) => (
          <button
            key={opt.id}
            type="button"
            role="radio"
            aria-checked={value === opt.id}
            className={`settings-option${value === opt.id ? ' active' : ''}`}
            onClick={() => onChange(opt.id)}
          >
            <strong>{opt.title}</strong>
            <span>{opt.blurb}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

export function Settings() {
  const { t } = useLingo()
  const { theme, setTheme, lingo, setLingo, motion, setMotion, sound, setSound } = usePrefs()
  const { play } = useSound()

  return (
    <section className="section wrap page-enter settings-page">
      <h1 className="section-title">{t('settingsTitle')}</h1>
      <p className="lede">{t('settingsLede')}</p>

      <SettingRow<ThemeMode>
        label={t('settingsTheme')}
        hint={t('settingsThemeHint')}
        value={theme}
        onChange={(v) => {
          setTheme(v)
          play('toggle')
        }}
        options={[
          {
            id: 'day',
            title: t('themeDay'),
            blurb: t('themeDayBlurb'),
          },
          {
            id: 'ratri',
            title: t('themeRatri'),
            blurb: t('themeRatriBlurb'),
          },
        ]}
      />

      <SettingRow<LingoMode>
        label={t('settingsLingo')}
        hint={t('settingsLingoHint')}
        value={lingo}
        onChange={(v) => {
          setLingo(v)
          play('toggle')
        }}
        options={[
          {
            id: 'funky',
            title: t('lingoFunky'),
            blurb: t('lingoFunkyBlurb'),
          },
          {
            id: 'sick',
            title: t('lingoSick'),
            blurb: t('lingoSickBlurb'),
          },
          {
            id: 'seedha',
            title: t('lingoSeedha'),
            blurb: t('lingoSeedhaBlurb'),
          },
        ]}
      />

      <SettingRow<MotionMode>
        label={t('settingsMotion')}
        hint={t('settingsMotionHint')}
        value={motion}
        onChange={(v) => {
          setMotion(v)
          play('toggle')
        }}
        options={[
          {
            id: 'drama',
            title: t('motionDrama'),
            blurb: t('motionDramaBlurb'),
          },
          {
            id: 'calm',
            title: t('motionCalm'),
            blurb: t('motionCalmBlurb'),
          },
        ]}
      />

      <SettingRow<'on' | 'off'>
        label={t('settingsSound')}
        hint={t('settingsSoundHint')}
        value={sound ? 'on' : 'off'}
        onChange={(v) => {
          setSound(v === 'on')
          if (v === 'on') play('toggle')
        }}
        options={[
          {
            id: 'on',
            title: t('soundOn'),
            blurb: t('soundOnBlurb'),
          },
          {
            id: 'off',
            title: t('soundOff'),
            blurb: t('soundOffBlurb'),
          },
        ]}
      />
    </section>
  )
}
