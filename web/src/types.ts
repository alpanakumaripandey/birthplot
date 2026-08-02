export type LongitudeInfo = {
  longitude: number
  rashi_index: number
  rashi_name: string
  degree_in_rashi: number
  nakshatra_index: number
  nakshatra_name: string
  pada: number
  retrograde: boolean
}

export type PlanetPlacement = {
  name: string
  house: number
  info: LongitudeInfo
}

export type HouseInfo = {
  number: number
  rashi_index: number
  rashi_name: string
  planets: string[]
}

export type DashaPeriod = {
  lord: string
  start: string
  end: string
  level: string
}

export type ChartPayload = {
  birth: {
    name: string
    birth_date: string
    birth_time: string | null
    place_query: string
    time_unknown: boolean
  }
  place: {
    query: string
    display_name: string
    latitude: number
    longitude: number
    timezone: string
  }
  local_dt: string
  utc_dt: string
  lagna: LongitudeInfo
  planets: Record<string, PlanetPlacement>
  houses: HouseInfo[]
  moon_nakshatra: string
  moon_pada: number
}

export type YogaResult = {
  name: string
  present: boolean
  detail: string
  meaning: string
  kind?: 'classical' | 'note'
}

export type LifeArea = {
  id: string
  label: string
  ask_topic: string
  headline: string
  blurb: string
  full: string
  houses: number[]
  planets: string[]
}

export type LifeSummaryTiming = {
  label: string
  range: string
}

/** Narrative insight panel (new). Older FAQ-shaped items may still exist in saved charts. */
export type LifeSummaryItem = {
  id: string
  title?: string
  kicker?: string
  insights?: string[]
  timing?: LifeSummaryTiming[]
  ask_topic: string
  version?: string
  // legacy FAQ fields
  category?: string
  category_label?: string
  question?: string
  answer?: string
  timing_hint?: string
}

export type Interpretation = {
  disclaimer: string
  lagna: string
  moon: string
  planets: string[]
  houses: string[]
  yogas: YogaResult[]
  dasha: string[]
  strengths: string[]
  life_areas?: LifeArea[]
  life_summary?: LifeSummaryItem[]
}

export type Timeline = {
  balance_at_birth: {
    lord: string
    years_remaining: number
    full_years: number
  }
  mahadashas: DashaPeriod[]
  current_mahadasha: DashaPeriod | null
  current_antardasha: DashaPeriod | null
  antardashas_in_current: DashaPeriod[]
  pratyantars_in_current: DashaPeriod[]
}

export type FullReport = {
  chart: ChartPayload
  timeline: Timeline
  interpretation: Interpretation
}

export type ChartRequest = {
  name: string
  date: string
  time: string | null
  place: string
  time_unknown: boolean
}

export type AskResponse = {
  question: string
  topic: string | null
  answer: string
  help: string | null
}

export type MatchPersonSummary = {
  name: string
  moon_rashi: string
  moon_nakshatra: string
  moon_pada: number
  manglik: boolean
  manglik_detail: string
}

export type MatchKoota = {
  id: string
  name: string
  max: number
  score: number
  detail: string
  note: string
}

export type MatchReport = {
  version: string
  total: number
  max: number
  verdict: string
  kootas: MatchKoota[]
  person_a: MatchPersonSummary
  person_b: MatchPersonSummary
  manglik_note: string
  convention: string
}

export type MatchRequest = {
  person_a: ChartRequest
  person_b: ChartRequest
}
