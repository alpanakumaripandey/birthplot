import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { ChartProvider } from './ChartContext'
import { Shell } from './components/Shell'
import { PrefsProvider } from './hooks/usePrefs'
import { Cast } from './pages/Cast'
import { Home } from './pages/Home'
import { How } from './pages/How'
import { Lexicon } from './pages/Lexicon'
import { Match } from './pages/Match'
import { ReportAsk } from './pages/ReportAsk'
import { ReportGrahas } from './pages/ReportGrahas'
import { ReportHouses } from './pages/ReportHouses'
import { ReportIndex } from './pages/ReportIndex'
import { ReportSummary } from './pages/ReportSummary'
import { ReportTiming } from './pages/ReportTiming'
import { ReportYou } from './pages/ReportYou'
import { ReportYogas } from './pages/ReportYogas'
import { Settings } from './pages/Settings'

export default function App() {
  return (
    <PrefsProvider>
      <ChartProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<Shell />}>
              <Route index element={<Home />} />
              <Route path="cast" element={<Cast />} />
              <Route path="match" element={<Match />} />
              <Route path="report" element={<ReportIndex />} />
              <Route path="report/you" element={<ReportYou />} />
              <Route path="report/summary" element={<ReportSummary />} />
              <Route path="report/grahas" element={<ReportGrahas />} />
              <Route path="report/houses" element={<ReportHouses />} />
              <Route path="report/yogas" element={<ReportYogas />} />
              <Route path="report/timing" element={<ReportTiming />} />
              <Route path="report/ask" element={<ReportAsk />} />
              <Route path="lexicon" element={<Lexicon />} />
              <Route path="how" element={<How />} />
              <Route path="settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ChartProvider>
    </PrefsProvider>
  )
}
