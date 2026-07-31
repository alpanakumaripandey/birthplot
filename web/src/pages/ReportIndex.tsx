import { Navigate } from 'react-router-dom'
import { useChart } from '../ChartContext'

export function ReportIndex() {
  const { report } = useChart()
  if (report) return <Navigate to="/report/you" replace />
  return <Navigate to="/cast" replace />
}
