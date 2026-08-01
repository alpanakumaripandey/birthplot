import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

export type ThemeMode = 'day' | 'ratri'
export type MotionMode = 'drama' | 'calm'
export type LingoMode = 'funky' | 'seedha' | 'sick'

type Prefs = {
  theme: ThemeMode
  motion: MotionMode
  lingo: LingoMode
  setTheme: (t: ThemeMode) => void
  setMotion: (m: MotionMode) => void
  setLingo: (l: LingoMode) => void
  toggleTheme: () => void
  toggleMotion: () => void
  toggleLingo: () => void
}

const PrefsContext = createContext<Prefs | null>(null)

const KEYS = {
  theme: 'birthplot_theme',
  motion: 'birthplot_motion',
  lingo: 'birthplot_lingo',
} as const

function read<T extends string>(key: string, fallback: T, allowed: T[]): T {
  try {
    const v = localStorage.getItem(key) as T | null
    if (v && allowed.includes(v)) return v
  } catch {
    /* ignore */
  }
  return fallback
}

function applyAttrs(theme: ThemeMode, motion: MotionMode, lingo: LingoMode) {
  const root = document.documentElement
  root.setAttribute('data-theme', theme === 'ratri' ? 'ratri' : 'day')
  root.setAttribute('data-motion', motion)
  root.setAttribute('data-lingo', lingo)
}

function preferReducedMotion(): boolean {
  try {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches
  } catch {
    return false
  }
}

export function PrefsProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<ThemeMode>(() =>
    read(KEYS.theme, 'day', ['day', 'ratri']),
  )
  const [motion, setMotionState] = useState<MotionMode>(() =>
    read(
      KEYS.motion,
      preferReducedMotion() ? 'calm' : 'drama',
      ['drama', 'calm'],
    ),
  )
  const [lingo, setLingoState] = useState<LingoMode>(() =>
    read(KEYS.lingo, 'funky', ['funky', 'seedha', 'sick']),
  )

  useEffect(() => {
    applyAttrs(theme, motion, lingo)
  }, [theme, motion, lingo])

  const setTheme = useCallback((t: ThemeMode) => {
    setThemeState(t)
    localStorage.setItem(KEYS.theme, t)
  }, [])
  const setMotion = useCallback((m: MotionMode) => {
    setMotionState(m)
    localStorage.setItem(KEYS.motion, m)
  }, [])
  const setLingo = useCallback((l: LingoMode) => {
    setLingoState(l)
    localStorage.setItem(KEYS.lingo, l)
  }, [])

  const value = useMemo<Prefs>(
    () => ({
      theme,
      motion,
      lingo,
      setTheme,
      setMotion,
      setLingo,
      toggleTheme: () => setTheme(theme === 'ratri' ? 'day' : 'ratri'),
      toggleMotion: () => setMotion(motion === 'calm' ? 'drama' : 'calm'),
      toggleLingo: () =>
        setLingo(lingo === 'funky' ? 'sick' : lingo === 'sick' ? 'seedha' : 'funky'),
    }),
    [theme, motion, lingo, setTheme, setMotion, setLingo],
  )

  return (
    <PrefsContext.Provider value={value}>
      {children}
    </PrefsContext.Provider>
  )
}

export function usePrefs() {
  const ctx = useContext(PrefsContext)
  if (!ctx) throw new Error('usePrefs must be used within PrefsProvider')
  return ctx
}
