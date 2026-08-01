/** Art path helpers for Birthplot image library. */

export const GRAHA_ART: Record<string, string> = {
  Sun: '/art/graha-sun.png',
  Moon: '/art/graha-moon.png',
  Mars: '/art/graha-mars.png',
  Mercury: '/art/graha-mercury.png',
  Jupiter: '/art/graha-jupiter.png',
  Venus: '/art/graha-venus.png',
  Saturn: '/art/graha-saturn.png',
  Rahu: '/art/graha-rahu.png',
  Ketu: '/art/graha-ketu.png',
}

export const ELEMENT_ART = {
  Fire: '/art/element-fire.png',
  Earth: '/art/element-earth.png',
  Air: '/art/element-air.png',
  Water: '/art/element-water.png',
} as const

/** Rashi index 1-12 → element */
export const RASHI_ELEMENT: Record<number, keyof typeof ELEMENT_ART> = {
  1: 'Fire',
  2: 'Earth',
  3: 'Air',
  4: 'Water',
  5: 'Fire',
  6: 'Earth',
  7: 'Air',
  8: 'Water',
  9: 'Fire',
  10: 'Earth',
  11: 'Air',
  12: 'Water',
}

export const NAKSHATRA_SKY = '/art/nakshatra-sky.png'
export const HERO_DAY = '/art/hero-mist.png'
export const HERO_DAY_GLOW = '/art/hero-day-glow.png'
export const HERO_RATRI = '/art/hero-ratri.png'
export const CAST_ART = '/art/cast-ritual.png'
export const HOW_WHEEL = '/art/wheel-atmosphere.png'
export const LEXICON_MOSAIC = '/art/lexicon-mosaic.png'

export const HOW_STEP_ART = {
  birth: '/art/how-birth.png',
  sky: '/art/how-sky.png',
  lagna: '/art/how-lagna.png',
  grahas: '/art/how-grahas.png',
  dasha: '/art/how-dasha.png',
} as const

export const GRAHA_NAMES = Object.keys(GRAHA_ART)
