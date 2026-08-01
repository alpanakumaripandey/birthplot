import { Navigate } from 'react-router-dom'
import { useChart } from '../ChartContext'
import { ReportGate } from '../components/ReportGate'

export function ReportIndex() {
  const { report } = useChart()
  if (report) return <Navigate to="/report/you" replace />
  return (
    <ReportGate>
      <div />
    </ReportGate>
  )
}
