export type LingoMode = 'funky' | 'seedha'

export const COPY = {
  heroLine: {
    funky:
      'Spill your birth deets. We’ll hand back your cosmic resume — Lagna, grahas, dashas, no gatekeeping.',
    seedha:
      'Enter your birth details. Get a clear Vedic chart — Lagna, planets, dashas, in plain language.',
  },
  castCta: { funky: 'Cast my chart', seedha: 'Create my chart' },
  howCta: { funky: 'How it works', seedha: 'About the method' },
  castTitle: { funky: 'Cast your chart', seedha: 'Create your chart' },
  castLede: {
    funky: 'Three beats: who → when → where. Then we drop the diamond.',
    seedha: 'Three steps: name, birth time, place. Then your chart appears.',
  },
  readingSky: { funky: 'Reading the sky…', seedha: 'Calculating your chart…' },
  readingLede: {
    funky: 'Geocoding the place, spinning Lahiri math, lining up grahas.',
    seedha: 'Looking up your place, computing planetary positions.',
  },
  loadAmit: { funky: 'Load Amit sample', seedha: 'Load sample chart' },
  next: { funky: 'Next', seedha: 'Next' },
  back: { funky: 'Back', seedha: 'Back' },
  castIt: { funky: 'Cast it', seedha: 'Generate' },
  youTitle: { funky: 'You', seedha: 'Overview' },
  youLede: {
    funky: 'Tap a chip — full text parks in the drawer, not a wall of bullets.',
    seedha: 'Tap a chip to open details in the side panel.',
  },
  strengthChips: { funky: 'Strength chips', seedha: 'Key notes' },
  grahasTitle: { funky: 'Grahas on stage', seedha: 'Planets' },
  grahasLede: {
    funky: 'Click a glyph — details slide in. Numbers stay tucked until you ask.',
    seedha: 'Click a planet for details. Open the numbers table if you need exact degrees.',
  },
  housesTitle: { funky: 'Twelve rooms of the plot', seedha: 'Twelve houses' },
  housesLede: {
    funky: 'The diamond is the map. Click a room — the story waits in the drawer.',
    seedha: 'Interactive chart map. Click a house for its meaning.',
  },
  yogasTitle: { funky: 'Yoga check', seedha: 'Yogas' },
  yogasLede: {
    funky: 'Lit tiles are present combos. Dim tiles are misses. Tap any tile for the why.',
    seedha: 'Highlighted yogas are present. Tap any yoga for explanation.',
  },
  timingTitle: { funky: 'Timing — Vimshottari', seedha: 'Dasha timing' },
  timingLede: {
    funky: 'Scrub the seasons. Highlighted = now. Click a slice for the microclimate.',
    seedha: 'Browse dasha periods. Current period is highlighted. Click for details.',
  },
  askTitle: { funky: 'Ask the plot', seedha: 'Ask a question' },
  askLede: {
    funky: 'Big topic tiles first. Type a custom question if you want to go off-menu.',
    seedha: 'Choose a topic or type your own question.',
  },
  lexiconTitle: { funky: 'Lexicon — meet the cast', seedha: 'Reference library' },
  lexiconLede: {
    funky: 'Tap a tile for the deep cut. Browse like a gallery, not a textbook.',
    seedha: 'Browse rashis, nakshatras, houses, and planets. Tap for details.',
  },
  kdHint: {
    funky: 'Tap a house — grahas inside light up the story.',
    seedha: 'Tap a house to see planets and meaning.',
  },
  emptyTitle: { funky: 'No chart in the chamber', seedha: 'No chart yet' },
  emptyLede: {
    funky: 'Spill some birth deets first — then we can unpack your cosmic resume module by module.',
    seedha: 'Create a chart first, then explore each report section.',
  },
  shareCard: { funky: 'Download chart card', seedha: 'Download chart image' },
  showNumbers: { funky: 'Show numbers', seedha: 'Show table' },
  hideNumbers: { funky: 'Hide numbers', seedha: 'Hide table' },
} as const

export type CopyKey = keyof typeof COPY
