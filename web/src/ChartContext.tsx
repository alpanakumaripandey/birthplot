import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import type { ChartRequest, FullReport } from './types'

const STORAGE_KEY = 'birthplot_report_v1'

type ChartContextValue = {
  report: FullReport | null
  setReport: (r: FullReport | null) => void
  birthRequest: ChartRequest | null
  clear: () => void
}

const ChartContext = createContext<ChartContextValue | null>(null)

function loadStored(): FullReport | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as FullReport
  } catch {
    return null
  }
}

export function ChartProvider({ children }: { children: ReactNode }) {
  const [report, setReportState] = useState<FullReport | null>(() => loadStored())

  const setReport = useCallback((r: FullReport | null) => {
    setReportState(r)
    if (r) sessionStorage.setItem(STORAGE_KEY, JSON.stringify(r))
    else sessionStorage.removeItem(STORAGE_KEY)
  }, [])

  const clear = useCallback(() => setReport(null), [setReport])

  const birthRequest: ChartRequest | null = useMemo(() => {
    if (!report) return null
    const b = report.chart.birth
    return {
      name: b.name,
      date: b.birth_date,
      time: b.time_unknown ? null : b.birth_time,
      place: b.place_query,
      time_unknown: b.time_unknown,
    }
  }, [report])

  const value = useMemo(
    () => ({ report, setReport, birthRequest, clear }),
    [report, setReport, birthRequest, clear],
  )

  return <ChartContext.Provider value={value}>{children}</ChartContext.Provider>
}

export function useChart() {
  const ctx = useContext(ChartContext)
  if (!ctx) throw new Error('useChart must be used within ChartProvider')
  return ctx
}
