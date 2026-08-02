export type LingoMode = 'funky' | 'seedha' | 'sick'

type Tone = { funky: string; seedha: string; sick: string }

export const COPY = {
  navCast: { funky: 'Cast', seedha: 'Cast', sick: 'Cast' },
  navMatch: { funky: 'Milan', seedha: 'Match', sick: 'Match' },
  navReport: { funky: 'Report', seedha: 'Report', sick: 'Recap' },
  navLexicon: { funky: 'Lexicon', seedha: 'Lexicon', sick: 'Glossary' },
  navHow: { funky: 'Kaise?', seedha: 'How', sick: 'Explain' },
  navSettings: { funky: 'Settings', seedha: 'Settings', sick: 'Prefs' },
  navMenu: { funky: 'Menu', seedha: 'Menu', sick: 'Menu' },
  footer: {
    funky: 'Birthplot · Jyotish with swag · Guidance, not god-mode destiny',
    seedha: 'Birthplot · Jyotish for curious humans · Learning guidance, not destiny decrees',
    sick: 'Birthplot · Jyotish that actually slaps · Vibes, not destiny decrees fr',
  },

  heroLine: {
    funky:
      'Drop your janam deets. We serve the full thali — Lagna, grahas, dashas, zero gatekeeping, full masala.',
    seedha:
      'Enter your birth details. Get a clear Vedic chart — Lagna, planets, dashas, in plain language.',
    sick:
      'Drop the birth deets. We cook the whole chart — Lagna, grahas, dashas. Main-character energy, no gatekeep.',
  },
  castCta: { funky: 'Cast mera chart', seedha: 'Create my chart', sick: 'Lock my chart' },
  howCta: { funky: 'Ye kaise chalta hai?', seedha: 'About the method', sick: 'How it even works' },
  castTitle: { funky: 'Chart pe chadh jao', seedha: 'Create your chart', sick: 'Build your chart' },
  castLede: {
    funky: 'Teen scene: kaun → kab → kahan. Phir diamond drops. Drama optional.',
    seedha: 'Three steps: name, birth time, place. Then your chart appears.',
    sick: 'Three beats: who → when → where. Then the diamond hits. Lowkey cinematic.',
  },
  castStepWho: { funky: 'Kaun', seedha: 'Identity', sick: 'Who' },
  castStepWhen: { funky: 'Kab', seedha: 'When', sick: 'When' },
  castStepWhere: { funky: 'Kahan', seedha: 'Where', sick: 'Where' },
  castNameLabel: { funky: 'Naam / alias', seedha: 'Name', sick: 'Name / alias' },
  castNamePlaceholder: {
    funky: 'Protagonist ka naam?',
    seedha: 'Your name',
    sick: "Main character's name?",
  },
  castDateLabel: { funky: 'Janam date', seedha: 'Date of birth', sick: 'Birth date' },
  castTimeLabel: {
    funky: 'Exact time (agar pata hai)',
    seedha: 'Birth time',
    sick: 'Birth time (if you got it)',
  },
  castTimeMystery: {
    funky: 'Time mystery hai — noon pe stand-in maar denge',
    seedha: 'Time unknown (noon stand-in)',
    sick: "Time's a mystery — we run noon + flag it",
  },
  castPlaceLabel: { funky: 'Janam jagah', seedha: 'Place of birth', sick: 'Birth place' },
  castPlacePlaceholder: {
    funky: 'City, State, Country — jitna accurate, utna tasty',
    seedha: 'City, State, Country',
    sick: 'City, State, Country — more exact = more fire',
  },
  readingSky: {
    funky: 'Sky padh rahe hain…',
    seedha: 'Calculating your chart…',
    sick: 'Reading the sky rn…',
  },
  readingLede: {
    funky: 'Place geocode, Lahiri spin, graha lineup — thoda wait, cosmic chai brewing.',
    seedha: 'Looking up your place, computing planetary positions.',
    sick: 'Geocoding the spot, spinning Lahiri math, lining grahas. Hold — chart loading.',
  },
  loadSample: {
    funky: 'Random sample maar do',
    seedha: 'Try a sample chart',
    sick: 'Hit me with a random demo',
  },
  sampleCaption: {
    funky: 'Demo banda/bandi only — Tera chart nahi. Dubara click = naya random.',
    seedha: 'Demo only — a fictional sample, not your chart. Click again for another.',
    sick: 'Demo NPC only — not you. Tap again for a new random.',
  },
  next: { funky: 'Aage', seedha: 'Next', sick: 'Next' },
  back: { funky: 'Peeche', seedha: 'Back', sick: 'Back' },
  castIt: { funky: 'Cast karo!', seedha: 'Generate', sick: 'Send it' },
  youTitle: { funky: 'Tu / You', seedha: 'Overview', sick: 'You' },
  youLede: {
    funky: 'Chip pe tap — pura scene drawer mein. Wall of text? Nah.',
    seedha: 'Tap a chip to open details in the side panel.',
    sick: 'Tap a chip — full lore slides in. No wall of text arc.',
  },
  youKicker: {
    funky: 'Tera cosmic resume',
    seedha: 'Your chart overview',
    sick: 'Your cosmic resume',
  },
  youLagnaStory: {
    funky: 'Lagna ki kahani',
    seedha: 'Lagna story',
    sick: 'Lagna story',
  },
  youMoonStory: {
    funky: 'Moon ki vibe',
    seedha: 'Moon story',
    sick: 'Moon vibe',
  },
  youOpenLagna: {
    funky: 'Diamond pe open',
    seedha: 'Open Lagna house',
    sick: 'Open Lagna',
  },
  youOpenMoon: {
    funky: 'Moon detail',
    seedha: 'Open Moon',
    sick: 'Open Moon',
  },
  youOpenNote: {
    funky: 'Note kholo',
    seedha: 'Open note',
    sick: 'Open note',
  },
  youMapTitle: {
    funky: 'Kundli map',
    seedha: 'Chart map',
    sick: 'Chart map',
  },
  lifeAreasTitle: {
    funky: 'Life areas — career, padhai, rishta',
    seedha: 'Life areas — career, education, relationship',
    sick: 'Life areas — career, school, relationship',
  },
  lifeAreasLede: {
    funky: 'Teen bade themes pe quick read. Card tap = full dive. Ask pe aur gehra.',
    seedha: 'Quick reads for three big life themes. Tap a card for the full note, or continue in Ask.',
    sick: 'Three big themes, fast. Tap a card to dive; Ask for more heat.',
  },
  lifeAreaOpen: {
    funky: 'Full reading kholo →',
    seedha: 'Open full reading →',
    sick: 'Open full reading →',
  },
  lifeAreaAskMore: {
    funky: 'Ask mein aur poochho',
    seedha: 'Ask more on this topic',
    sick: 'Ask more on this',
  },
  lifeAreasAskHint: {
    funky: 'Custom sawaal?',
    seedha: 'Want a custom question?',
    sick: 'Custom question?',
  },
  lifeAreasAskLink: {
    funky: 'Ask section pe jao',
    seedha: 'Go to Ask',
    sick: 'Jump to Ask',
  },
  lifeAreasLoading: {
    funky: 'Career / padhai / rishta cards aa rahe hain…',
    seedha: 'Loading career, education, and relationship cards…',
    sick: 'Loading life-area cards…',
  },
  majorTitle: {
    funky: 'Badi baatein — major highlights',
    seedha: 'Major highlights',
    sick: 'Major hits — chart at a glance',
  },
  majorLede: {
    funky: 'Cast ke baad pehle ye padho — Lagna, Moon, dasha, yogas, key notes.',
    seedha: 'Start here after casting — Lagna, Moon, current dasha, yogas, and key notes.',
    sick: 'Read this first after cast — Lagna, Moon, dasha, yogas, key notes.',
  },
  majorLagna: { funky: 'Lagna', seedha: 'Lagna', sick: 'Lagna' },
  majorMoon: { funky: 'Moon nakshatra', seedha: 'Moon nakshatra', sick: 'Moon nakshatra' },
  majorDasha: { funky: 'Abhi ki dasha', seedha: 'Current dasha', sick: 'Current dasha' },
  majorYogas: { funky: 'Yogas on', seedha: 'Yogas present', sick: 'Yogas on' },
  majorRising: { funky: 'Rising sign', seedha: 'Rising sign', sick: 'Rising sign' },
  majorTimeUnknown: {
    funky: 'Time unknown — Lagna soft-read',
    seedha: 'Time unknown — treat Lagna carefully',
    sick: 'Time unknown — go easy on Lagna takes',
  },
  majorDashaEmpty: {
    funky: 'Dasha strip loading nahi hua',
    seedha: 'No current dasha available',
    sick: 'No current dasha locked',
  },
  majorYogasNone: {
    funky: 'Koi lit yoga nahi is pass',
    seedha: 'No classical yogas flagged',
    sick: 'No lit yogas this pass',
  },
  majorYogasCount: {
    funky: '{n} lit — Yoga check pe full list',
    seedha: '{n} present — see Yogas for details',
    sick: '{n} lit — open Yogas for the full list',
  },
  majorYogasHint: {
    funky: 'Yoga tab mein deep cut',
    seedha: 'Check the Yogas tab for the full scan',
    sick: 'Yogas tab has the full scan',
  },
  majorNotes: {
    funky: 'Key notes (strength pass)',
    seedha: 'Key notes',
    sick: 'Key notes (strength pass)',
  },
  strengthChips: { funky: 'Strength ke chips', seedha: 'Key notes', sick: 'Strength chips' },
  grahasTitle: { funky: 'Grahas on stage, baby', seedha: 'Planets', sick: 'Grahas on deck' },
  grahasLede: {
    funky: 'Glyph pe click — details slide in. Numbers tab tak hide jab tak tu na maange.',
    seedha: 'Click a planet for details. Open the numbers table if you need exact degrees.',
    sick: 'Click a glyph — details slide. Numbers stay tucked till you ask.',
  },
  housesTitle: { funky: 'Barah kamre, ek plot', seedha: 'Twelve houses', sick: 'Twelve plot rooms' },
  housesLede: {
    funky: 'Diamond = map. Room pe click — story drawer mein wait kar rahi hai.',
    seedha: 'Interactive chart map. Click a house for its meaning.',
    sick: 'Diamond = map. Tap a room — story waits in the drawer.',
  },
  yogasTitle: { funky: 'Yoga check, lit or dim', seedha: 'Yogas', sick: 'Yoga check' },
  yogasLede: {
    funky: 'Lit = combo on. Dim = miss. Tap for the “kyun?”',
    seedha: 'Highlighted yogas are present. Tap any yoga for explanation.',
    sick: 'Lit tiles = combo landed. Dim = miss. Tap for the why.',
  },
  timingTitle: {
    funky: 'Timing — Vimshottari weather',
    seedha: 'Dasha timing',
    sick: 'Timing — Vimshottari seasons',
  },
  timingLede: {
    funky: 'Seasons scrub karo. Highlighted = abhi. Slice pe click = microclimate.',
    seedha: 'Browse dasha periods. Current period is highlighted. Click for details.',
    sick: 'Scrub the seasons. Highlighted = now. Tap a slice for the microclimate.',
  },
  askTitle: { funky: 'Plot se poochho', seedha: 'Ask a question', sick: 'Ask the plot' },
  askLede: {
    funky: 'Bade topic tiles pehle. Custom sawaal? Type maar, off-menu chalo.',
    seedha: 'Choose a topic or type your own question.',
    sick: 'Big topic tiles first. Custom Q? Type it — go off-menu.',
  },
  lexiconTitle: {
    funky: 'Lexicon — cast se milo',
    seedha: 'Reference library',
    sick: 'Lexicon — meet the cast',
  },
  lexiconLede: {
    funky: 'Tile tap = deep cut. Gallery vibe, textbook vibe nahi.',
    seedha: 'Browse rashis, nakshatras, houses, and planets. Tap for details.',
    sick: 'Tap a tile for the deep cut. Gallery vibes, not textbook vibes.',
  },
  kdHint: {
    funky: 'House pe tap — andar ke grahas story light up karte hain.',
    seedha: 'Tap a house to see planets and meaning.',
    sick: 'Tap a house — grahas inside light the story.',
  },
  emptyTitle: {
    funky: 'Chamber khali hai, boss',
    seedha: 'No chart yet',
    sick: 'No chart in the chamber',
  },
  emptyLede: {
    funky: 'Pehle janam deets daalo — phir module-by-module cosmic resume unpack.',
    seedha: 'Create a chart first, then explore each report section.',
    sick: 'Drop birth deets first — then we unpack the cosmic resume module by module.',
  },
  shareCard: {
    funky: 'Chart card download',
    seedha: 'Download chart image',
    sick: 'Download chart card',
  },
  shareRendering: {
    funky: 'Render ho raha…',
    seedha: 'Rendering…',
    sick: 'Rendering…',
  },
  shareFailed: {
    funky: 'Share card fail — try again',
    seedha: 'Could not download chart card',
    sick: 'Share card failed — try again',
  },
  clearChart: {
    funky: 'Naya cast / clear',
    seedha: 'Clear chart',
    sick: 'Clear chart',
  },
  timeUnknownWarn: {
    funky: 'Time fuzzy tha — Lagna soft-read. Moon + dasha still solid.',
    seedha: 'Birth time was unknown — treat Lagna carefully. Moon and dasha still help.',
    sick: 'Time was fuzzy — go easy on Lagna takes. Moon + dasha still land.',
  },
  castIncomplete: {
    funky: 'Pehle saare steps bharo — kaun, kab, kahan.',
    seedha: 'Complete name, date/time, and place first.',
    sick: 'Finish who / when / where before casting.',
  },
  castNeedName: {
    funky: 'Naam chahiye, boss.',
    seedha: 'Please enter a name.',
    sick: 'Need a name first.',
  },
  castNeedDate: {
    funky: 'Date daalo.',
    seedha: 'Please enter a birth date.',
    sick: 'Drop a birth date.',
  },
  castNeedTime: {
    funky: 'Time daalo ya mystery checkbox tick karo.',
    seedha: 'Enter birth time or mark time unknown.',
    sick: 'Add a time or mark it unknown.',
  },
  askCustomLabel: {
    funky: 'Custom sawaal',
    seedha: 'Custom question',
    sick: 'Custom question',
  },
  askCustomPlaceholder: {
    funky: 'career, marriage, money… ya apna sentence',
    seedha: 'career, marriage, money… or your own question',
    sick: 'career, marriage, money… or type your own',
  },
  askLoading: {
    funky: 'Sky se pooch rahe…',
    seedha: 'Consulting the sky…',
    sick: 'Asking the sky…',
  },
  askSubmit: { funky: 'Poochho', seedha: 'Ask', sick: 'Ask' },
  askTopic: { funky: 'Topic', seedha: 'Topic', sick: 'Topic' },
  askHelpTitle: {
    funky: 'Topic match nahi — try ye themes:',
    seedha: 'Could not map that — try one of these themes:',
    sick: 'No topic lock — try one of these:',
  },
  askNeedQuestion: {
    funky: 'Kuch toh poochho.',
    seedha: 'Enter a question or pick a topic.',
    sick: 'Type something or tap a topic.',
  },
  timingNowMaha: { funky: 'Abhi maha', seedha: 'Current maha', sick: 'Current maha' },
  timingNowAntar: { funky: 'Abhi antar', seedha: 'Current antar', sick: 'Current antar' },
  timingMahaLabel: {
    funky: 'Mahadasha strip',
    seedha: 'Mahadashas',
    sick: 'Mahadasha strip',
  },
  timingAntarLabel: {
    funky: 'Antardashas in current maha',
    seedha: 'Antardashas in current mahadasha',
    sick: 'Antars in current maha',
  },
  timingPratyLabel: {
    funky: 'Pratyantar strip',
    seedha: 'Pratyantar strip',
    sick: 'Pratyantar strip',
  },
  timingEmpty: {
    funky: 'Maha strip empty — chart refresh try karo.',
    seedha: 'No mahadasha periods available.',
    sick: 'No mahadasha strip loaded.',
  },
  timingEmptyAntar: {
    funky: 'Antar list empty for current maha.',
    seedha: 'No antardashas in the current mahadasha.',
    sick: 'No antars in the current maha.',
  },
  yogaPresent: { funky: 'Lit', seedha: 'Present', sick: 'Lit' },
  yogaQuiet: { funky: 'Dim', seedha: 'Quiet', sick: 'Dim' },
  yogaNote: { funky: 'note', seedha: 'note', sick: 'note' },
  yogaClassical: {
    funky: 'Classical yogas',
    seedha: 'Classical yogas',
    sick: 'Classical yogas',
  },
  yogaNotes: {
    funky: 'Chart notes (occupancy)',
    seedha: 'Chart notes',
    sick: 'Chart notes (occupancy)',
  },
  yogaNotesLede: {
    funky: 'Ye classical yoga nahi — pattern flags for study.',
    seedha: 'These are occupancy notes, not classical yogas.',
    sick: 'Occupancy flags for study — not classical yogas.',
  },
  yogaPresentFull: {
    funky: 'Is chart mein present',
    seedha: 'Present in this chart',
    sick: 'Present in this chart',
  },
  yogaNoteActive: {
    funky: 'Note flag on',
    seedha: 'Chart note active',
    sick: 'Note flag on',
  },
  yogaQuietFull: {
    funky: 'Yahan active nahi',
    seedha: 'Not active here',
    sick: 'Not active here',
  },
  lexFilter: { funky: 'Filter', seedha: 'Filter', sick: 'Filter' },
  lexLoading: {
    funky: 'Library load ho rahi…',
    seedha: 'Loading the library…',
    sick: 'Loading the library…',
  },
  lexEmpty: {
    funky: 'Koi match nahi — filter soft karo.',
    seedha: 'No matches for that filter.',
    sick: 'No matches — loosen the filter.',
  },
  lexClose: { funky: 'Band karo', seedha: 'Close', sick: 'Close' },
  showNumbers: { funky: 'Numbers dikhao', seedha: 'Show table', sick: 'Show numbers' },
  hideNumbers: { funky: 'Numbers chhupao', seedha: 'Hide table', sick: 'Hide numbers' },

  reportYou: { funky: 'Tu', seedha: 'You', sick: 'You' },
  reportSummary: { funky: 'Summary', seedha: 'Summary', sick: 'Summary' },
  reportGrahas: { funky: 'Grahas', seedha: 'Grahas', sick: 'Grahas' },
  reportHouses: { funky: 'Kamre', seedha: 'Houses', sick: 'Houses' },
  reportYogas: { funky: 'Yogas', seedha: 'Yogas', sick: 'Yogas' },
  reportTiming: { funky: 'Timing', seedha: 'Timing', sick: 'Timing' },
  reportAsk: { funky: 'Poochho', seedha: 'Ask', sick: 'Ask' },

  summaryTitle: {
    funky: 'Past · Present · Future',
    seedha: 'Past · Present · Future',
    sick: 'Past · Present · Future',
  },
  summaryLede: {
    funky: 'Chart foundation, current dasha, upcoming windows.',
    seedha: 'Chart foundation, current dasha, upcoming windows.',
    sick: 'Chart foundation, current dasha, upcoming windows.',
  },
  summaryNote: {
    funky: '',
    seedha: '',
    sick: '',
  },
  summaryEmpty: {
    funky: 'Chart dubara cast karo for this summary.',
    seedha: 'Re-cast your chart to load this summary.',
    sick: 'Re-cast to load this summary.',
  },
  summaryRemedyFocus: {
    funky: '',
    seedha: '',
    sick: '',
  },
  summaryOpen: {
    funky: 'Poora padho →',
    seedha: 'Read more →',
    sick: 'Open →',
  },
  summaryAskHint: {
    funky: 'Aur detail chahiye?',
    seedha: 'Want a deeper dive?',
    sick: 'Want more heat on a topic?',
  },
  summaryAskLink: {
    funky: 'Ask pe jao',
    seedha: 'Go to Ask',
    sick: 'Jump to Ask',
  },
  summaryAskMore: {
    funky: 'Is theme pe Ask kholo →',
    seedha: 'Explore this theme in Ask →',
    sick: 'Take this theme to Ask →',
  },

  matchTitle: {
    funky: 'Kundali milan — do janam, ek score',
    seedha: 'Kundali matching',
    sick: 'Kundali match — two charts, one score',
  },
  matchLede: {
    funky:
      'Do logon ke Moon charts → 36 guna. Score ke saath plain English: kya strong hai, kahan sochna hai.',
    seedha:
      'Compare two birth charts with Ashtakoota (36 points). The result explains each guna in plain language.',
    sick:
      'Two Moons, 36 gunas — then we translate the score so anyone gets what’s strong and what needs talk.',
  },
  matchPersonA: { funky: 'Person A (bride-side)', seedha: 'Person A (bride-side)', sick: 'Person A (bride-side)' },
  matchPersonB: { funky: 'Person B (groom-side)', seedha: 'Person B (groom-side)', sick: 'Person B (groom-side)' },
  matchSubmit: { funky: 'Milan chalao', seedha: 'Match charts', sick: 'Run the match' },
  matchLoadDemo: { funky: 'Demo jodi', seedha: 'Load demo pair', sick: 'Load demo pair' },
  matchReading: {
    funky: 'Dono kundli milayi ja rahi hai…',
    seedha: 'Matching both charts…',
    sick: 'Cross-checking both skies…',
  },
  matchScoreLabel: { funky: 'Guna score', seedha: 'Guna score', sick: 'Guna score' },
  matchBreakdown: {
    funky: 'Har guna — detail + solution',
    seedha: 'Each guna: detail & solutions',
    sick: 'Guna by guna — detail + fixes',
  },
  matchStrengths: { funky: 'Strong areas', seedha: 'Strengths', sick: 'What’s strong' },
  matchWatchouts: { funky: 'Dhyan dena', seedha: 'Watch-outs', sick: 'Talk these through' },
  matchActionPlan: {
    funky: 'Pehle ye karo',
    seedha: 'What to do next',
    sick: 'Do this next',
  },
  matchOverview: {
    funky: 'Poori picture — seedhi baat',
    seedha: 'Full summary in simple words',
    sick: 'The whole picture — plain English',
  },
  matchOverviewHint: {
    funky: 'Pehle ye padho — score ke peeche poori kahani.',
    seedha: 'Read this first — what the whole match means in everyday language.',
    sick: 'Read this first — the whole match in plain talk.',
  },
  matchGunaGuide: {
    funky: 'Har guna kya poochhta hai',
    seedha: 'What each guna asks',
    sick: 'What each guna is asking',
  },
  matchProblem: { funky: 'Issue', seedha: 'The issue', sick: 'The issue' },
  matchSolutions: { funky: 'Solutions', seedha: 'Solutions', sick: 'Fixes' },
  matchManglik: { funky: 'Manglik check', seedha: 'Manglik check', sick: 'Manglik check' },
  matchMoonLine: { funky: 'Moon', seedha: 'Moon', sick: 'Moon' },
  matchLevelStrong: { funky: 'Strong', seedha: 'Strong', sick: 'Strong' },
  matchLevelOk: { funky: 'Okay', seedha: 'Okay', sick: 'Okay' },
  matchLevelWeak: { funky: 'Weak', seedha: 'Weak', sick: 'Weak' },
  matchAgain: { funky: 'Naya milan', seedha: 'Match again', sick: 'Match again' },
  matchNeedBoth: {
    funky: 'Dono sides ke naam, date, place chahiye.',
    seedha: 'Name, date, and place are required for both people.',
    sick: 'Need name, date, and place for both people.',
  },

  settingsTitle: {
    funky: 'Settings — apna vibe set karo',
    seedha: 'Settings',
    sick: 'Prefs — lock your vibe',
  },
  settingsLede: {
    funky: 'Theme, lingo, motion — teen dials. Jo vibe chahiye, wahi lock.',
    seedha: 'Choose theme, language tone, and motion preference.',
    sick: 'Theme, lingo, motion — three dials. Pick what hits.',
  },
  settingsTheme: { funky: 'Theme', seedha: 'Theme', sick: 'Theme' },
  settingsThemeHint: {
    funky: 'Din ka parchment glow ya Raat ka ink — pick your arena.',
    seedha: 'Day (warm parchment) or Ratri (dark night).',
    sick: 'Day parchment glow or Ratri ink night — pick your arena.',
  },
  themeDay: { funky: 'Day', seedha: 'Day', sick: 'Day' },
  themeDayBlurb: {
    funky: 'Warm paper, brass spark, monsoon ink — morning chai energy.',
    seedha: 'Warm parchment and clear contrast for daytime reading.',
    sick: 'Warm paper, brass spark — soft daylight main-character glow.',
  },
  themeRatri: { funky: 'Ratri', seedha: 'Ratri', sick: 'Ratri' },
  themeRatriBlurb: {
    funky: 'Deep teal night, brass stars — late-night scroll mode.',
    seedha: 'Dark night theme with soft teal and brass accents.',
    sick: 'Deep teal night, brass stars — late-night scroll mode.',
  },
  settingsLingo: { funky: 'Lingo', seedha: 'Language tone', sick: 'Lingo' },
  settingsLingoHint: {
    funky: 'Funky = Hinglish chaos. Sick = GenZ cool. Seedha = calm classroom.',
    seedha: 'Funky is playful Hinglish. Sick is GenZ English. Seedha is plain.',
    sick: 'Funky = Hinglish chaos. Sick = GenZ cool. Seedha = clean classroom.',
  },
  lingoFunky: { funky: 'Funky', seedha: 'Funky', sick: 'Funky' },
  lingoFunkyBlurb: {
    funky: 'Deets, thali, masala, “cast karo” — full desi internet voice.',
    seedha: 'Playful Hinglish and street-smart phrasing.',
    sick: 'Hinglish chaos with heart — thali, masala, cast karo.',
  },
  lingoSick: { funky: 'Sick', seedha: 'Sick', sick: 'Sick' },
  lingoSickBlurb: {
    funky: 'GenZ cool English — slaps, locked in, main character, no cap.',
    seedha: 'Modern GenZ English — casual, sharp, internet-native.',
    sick: 'GenZ cool — it’s giving chart, lowkey fire, no cap.',
  },
  lingoSeedha: { funky: 'Seedha', seedha: 'Seedha', sick: 'Seedha' },
  lingoSeedhaBlurb: {
    funky: 'Seedha bola toh: clean English, low slang, high clarity.',
    seedha: 'Clear, straightforward English for focused reading.',
    sick: 'Clean English, low slang, high clarity. Soft reset.',
  },
  settingsMotion: { funky: 'Motion', seedha: 'Motion', sick: 'Motion' },
  settingsMotionHint: {
    funky: 'Drama = wheels spin hard, chips float. Calm = chill, less floaty.',
    seedha: 'Drama enables strong animations. Calm reduces motion.',
    sick: 'Drama = max motion cinema. Calm = soft mode, less spin.',
  },
  motionDrama: { funky: 'Drama', seedha: 'Drama', sick: 'Drama' },
  motionDramaBlurb: {
    funky: 'Faster orbits, parallax punch, streak rain — cinema mode on.',
    seedha: 'Stronger motion: parallax, orbits, streaks, floating chips.',
    sick: 'Parallax punch, orbit heat, streak rain — cinema mode unlocked.',
  },
  motionCalm: { funky: 'Calm', seedha: 'Calm', sick: 'Calm' },
  motionCalmBlurb: {
    funky: 'Motion ko chill mode — focus pe content, less spin.',
    seedha: 'Reduced motion for a quieter reading experience.',
    sick: 'Chill motion — content first, less float.',
  },
  settingsSound: { funky: 'Sound', seedha: 'Sound', sick: 'Sound' },
  settingsSoundHint: {
    funky: 'Soft taps & cast chimes. Off = silence.',
    seedha: 'Soft UI sounds on cast, drawers, and toggles. Off mutes them.',
    sick: 'Soft taps and cast chimes — flip off for silence.',
  },
  soundOn: { funky: 'On', seedha: 'On', sick: 'On' },
  soundOnBlurb: {
    funky: 'Tiny brass/jade tones when you cast or open drawers.',
    seedha: 'Play soft feedback sounds for key actions.',
    sick: 'Soft tones on cast, drawers, toggles.',
  },
  soundOff: { funky: 'Off', seedha: 'Off', sick: 'Off' },
  soundOffBlurb: {
    funky: 'No beeps. Pure visual.',
    seedha: 'Mute all UI sounds.',
    sick: 'Silence mode.',
  },

  howTitle: {
    funky: 'Birthplot ka jugad',
    seedha: 'How Birthplot works',
    sick: 'How Birthplot even works',
  },
  howLede: {
    funky:
      'Crystal ball? Nah. Janam deets + classical Jyotish math + ek chart jo poke karne layak ho.',
    seedha:
      'Classical Vedic calculation from your birth details, then a clear interactive chart to explore.',
    sick:
      'No crystal-ball arc. Birth deets + classical Jyotish math + a chart you can actually poke.',
  },
  howTrackShort: { funky: 'Short & spicy', seedha: 'Short', sick: 'Short & spicy' },
  howTrackBeginner: {
    funky: 'Beginner slow-walk',
    seedha: 'Beginner',
    sick: 'Beginner slow-walk',
  },
  howTrackHint: {
    funky: 'Short = five taps mein vibe. Beginner = picture-wali class, no rush.',
    seedha: 'Short = quick overview. Beginner = detailed step-by-step.',
    sick: 'Short = five taps of vibe. Beginner = picture class, no rush.',
  },
  howDisclaimerTitle: {
    funky: 'Seedha baat / Disclaimer',
    seedha: 'Disclaimer',
    sick: 'Real talk / Disclaimer',
  },
  howDisclaimer: {
    funky:
      'Classical Jyotish math for learning + reflection. Medical / legal / money / destiny decree? Not this app. Big life calls = real pro. Tera effort still writes the plot.',
    seedha:
      'This report uses classical Jyotish computation for learning and reflective guidance. It is not medical, legal, financial, or destiny advice. For important life decisions, consult a qualified professional.',
    sick:
      'Classical Jyotish for learning + reflection. Not medical, legal, money, or destiny decrees. Big life calls = real pro. Your choices still write the plot.',
  },
  howPrev: { funky: 'Peeche chapter', seedha: 'Previous', sick: 'Prev chapter' },
  howNextChapter: { funky: 'Agla chapter', seedha: 'Next chapter', sick: 'Next chapter' },
  howChapterOf: { funky: 'Chapter', seedha: 'Chapter', sick: 'Chapter' },
} as const satisfies Record<string, Tone>

export type CopyKey = keyof typeof COPY

/** Short-track expandable cards. */
export const HOW_SHORT = [
  {
    id: 'birth',
    art: 'birth' as const,
    title: { funky: 'Janam deets', seedha: 'Birth details', sick: 'Birth deets' },
    blurb: {
      funky: 'Naam, date, time, jagah — sky photo ke four coordinates.',
      seedha: 'Name, date, time, and place locate the sky at your birth.',
      sick: 'Name, date, time, place — four coords for your sky photo.',
    },
    more: {
      funky:
        'Time/place galat = Lagna shift possible. Time mystery? Noon stand-in + flag. No drama hidden.',
      seedha:
        'Accurate time and place matter because the sky moves. If time is unknown, noon is used and marked.',
      sick:
        'Wrong time/place can shift Lagna. Time mystery? We run noon + flag it. No hidden sauce.',
    },
  },
  {
    id: 'sky',
    art: 'sky' as const,
    title: { funky: 'Sky ka hisaab', seedha: 'Sky calculation', sick: 'Sky math' },
    blurb: {
      funky: 'Sidereal + Lahiri — desi sky map, Western newspaper wala nahi.',
      seedha: 'Sidereal zodiac with Lahiri ayanamsa — the Indian standard map.',
      sick: 'Sidereal + Lahiri — desi sky map, not the Western newspaper one.',
    },
    more: {
      funky:
        'Planets sidereal frame mein, phir whole-sign houses Lagna se. Clean jugad.',
      seedha:
        'Planets are placed in the sidereal zodiac, then whole-sign houses are counted from the rising sign.',
      sick:
        'Planets land in the sidereal frame, then whole-sign houses stack from Lagna. Clean build.',
    },
  },
  {
    id: 'lagna',
    art: 'lagna' as const,
    title: {
      funky: 'Lagna + barah kamre',
      seedha: 'Lagna and houses',
      sick: 'Lagna + twelve rooms',
    },
    blurb: {
      funky: 'Lagna = rising sign = house 1. Baaki gyarah rooms line mein.',
      seedha: 'Lagna is the rising sign (house 1). Houses 2–12 follow in order.',
      sick: 'Lagna = rising sign = house 1. The other eleven rooms follow.',
    },
    more: {
      funky:
        'Whole-sign = har house ek full rashi. Beginner-friendly, bahut schools ka classic.',
      seedha:
        'Each house is one full sign (whole-sign system), which is clear for learning.',
      sick:
        'Whole-sign = each house is one full rashi. Beginner-friendly, classic in a lot of schools.',
    },
  },
  {
    id: 'grahas',
    art: 'grahas' as const,
    title: {
      funky: 'Nau grahas, full cast',
      seedha: 'Nine planets',
      sick: 'Nine grahas, full cast',
    },
    blurb: {
      funky: 'Sun se Saturn + Rahu-Ketu — har ek ka ghar reserved.',
      seedha: 'Sun–Saturn plus Rahu and Ketu, each placed in a house and sign.',
      sick: 'Sun through Saturn + Rahu/Ketu — each gets a seat.',
    },
    more: {
      funky:
        'Report mein glyphs tap. Yogas = pattern check, fate handcuff nahi.',
      seedha:
        'Explore each planet in the report. Yogas flag classical combinations for study.',
      sick:
        'Tap glyphs in the report. Yogas = pattern check, not fate handcuffs.',
    },
  },
  {
    id: 'dasha',
    art: 'dasha' as const,
    title: {
      funky: 'Dasha = season playlist',
      seedha: 'Dasha timing',
      sick: 'Dasha = season playlist',
    },
    blurb: {
      funky: 'Vimshottari: Moon nakshatra se life ke seasons.',
      seedha: 'Vimshottari dashas are life periods seeded from the Moon’s nakshatra.',
      sick: 'Vimshottari: life seasons seeded from Moon nakshatra.',
    },
    more: {
      funky:
        'Maha → antar → pratyantar. Timeline scrub; “abhi” highlight. Weather map, jail sentence nahi.',
      seedha:
        'Browse mahadasha, antardasha, and pratyantar. Current period is highlighted for orientation.',
      sick:
        'Maha → antar → pratyantar. Scrub the timeline; “now” is lit. Weather map, not a prison sentence.',
    },
  },
] as const

/** Beginner long chapters. */
export const HOW_BEGINNER = [
  {
    id: 'birth',
    art: 'birth' as const,
    title: {
      funky: 'Kaun / kab / kahan — kyun poochte hain',
      seedha: 'Why name, time, and place matter',
      sick: 'Who / when / where — why we even ask',
    },
    body: {
      funky: `Kundli = ek moment ka sky freeze-frame on Earth.

**Kaun** bas story label hai — math ko letters se matlab nahi, report ko hai.

**Kab** (date + clock) decide karta hai sky ka kaunsa slice up tha. Earth ghoomti hai; ~har do ghante naya sign east pe rise hota hai. Woh rising sign = **Lagna** — poora house map flip.

**Kahan** (city / coords) local horizon set karta hai. Same clock Mumbai vs Delhi Lagna ko cusp pe nudge kar sakta hai. Hum place geocode karke lat/long se calculate karte hain.

Time fuzzy hai? Bolo. Noon stand-in + time-unknown flag — taaki Lagna-sensitive claims pe over-read na ho.`,
      seedha: `A kundli is a snapshot of the sky for one birth moment at one place.

The **name** labels the report. The **date and time** decide which sky was present — the rising sign (Lagna) changes roughly every two hours. The **place** sets the local horizon; we look up coordinates and calculate from there.

If time is unknown, noon is used and the chart is marked so Lagna-sensitive conclusions are treated carefully.`,
      sick: `A kundli is a freeze-frame of the sky for one moment on Earth.

**Who** is just your story label — the math does not care about the letters, the report does.

**When** (date + clock) locks which sky slice was up. Earth spins; about every two hours a new sign rises east. That rising sign is **Lagna** — and it flips the whole house map.

**Where** (city / coords) sets the local horizon. Same clock in Mumbai vs Delhi can nudge Lagna near a cusp. We geocode your place, then calculate with lat/long.

Time fuzzy? Say so. Noon stand-in + time-unknown flag so you don’t over-read Lagna-sensitive claims.`,
    },
  },
  {
    id: 'sky',
    art: 'sky' as const,
    title: {
      funky: 'Sidereal sky, Lahiri yardstick',
      seedha: 'Sidereal zodiac and Lahiri',
      sick: 'Sidereal sky, Lahiri yardstick',
    },
    body: {
      funky: `Western pop often **tropical** (seasons) use karta hai. Classical Indian Jyotish = **sidereal** — star field se tied.

Dono frames centuries mein drift hue. Gap = **ayanamsa**. Birthplot = **Lahiri (Chitrapaksha)** — desi standard.

Jab hum “Moon in Taurus” bolte hain, sidereal Taurus matlab — newspaper tropical column zaroori nahi.

Flow: longitudes → rashi → nakshatra → pada. Ye stack dignity, yogas, dasha seed feed karta hai.`,
      seedha: `Birthplot uses the **sidereal** zodiac (star-based), not the tropical season-based map common in Western pop astrology.

The offset between them is the **ayanamsa**. We use **Lahiri**, the usual Indian standard.

Planets are placed in signs (rashis) and lunar mansions (nakshatras). Those placements feed strength notes, yogas, and dasha timing.`,
      sick: `Western pop often runs **tropical** (seasons). Classical Indian Jyotish runs **sidereal** — tied to the star field.

Those frames drifted for centuries. The gap is the **ayanamsa**. Birthplot uses **Lahiri (Chitrapaksha)** — the desi standard.

When we say “Moon in Taurus,” we mean sidereal Taurus — not necessarily the newspaper tropical column.

Flow: longitudes → rashi → nakshatra → pada. That stack feeds dignity, yogas, and dasha seeding.`,
    },
  },
  {
    id: 'lagna',
    art: 'lagna' as const,
    title: {
      funky: 'Lagna = ghar 1, phir gyarah rooms',
      seedha: 'Lagna and the twelve houses',
      sick: 'Lagna = house 1, then eleven rooms',
    },
    body: {
      funky: `**Lagna** = birth pe east horizon pe rising rashi. **Whole-sign** system mein woh poori sign = House 1. Agli = House 2, ghoomte raho.

Barah kamre ki story:
- 1 self / body tone
- 2 resources
- 3 courage / siblings / skills
- 4 home / roots
- 5 creativity / kids / romance sparks
- 6 work / health friction
- 7 partners
- 8 depth / change
- 9 dharma / long roads
- 10 career skyline
- 11 gains / networks
- 12 retreat / losses / far shores

Interactive diamond wahi map hai. Room tap; andar baithe grahas us life area pe bolte hain.`,
      seedha: `**Lagna** is the rising sign at birth. With **whole-sign** houses, that full sign is house 1; the following signs are houses 2–12 in order.

Houses describe life areas (self, money, home, partnership, career, and so on). Planets in a house color that topic. The diamond chart lets you tap each house to read it.`,
      sick: `**Lagna** is the rashi rising on the eastern horizon at birth. In our **whole-sign** system, that whole sign becomes House 1. Next sign = House 2, and so on.

Think twelve rooms in a story:
- 1 self / body tone
- 2 resources
- 3 courage / siblings / skills
- 4 home / roots
- 5 creativity / kids / romance sparks
- 6 work / health friction
- 7 partners
- 8 depth / change
- 9 dharma / long roads
- 10 career skyline
- 11 gains / networks
- 12 retreat / losses / far shores

The interactive diamond is that map. Tap a room; grahas inside speak to that life area.`,
    },
  },
  {
    id: 'grahas',
    art: 'grahas' as const,
    title: {
      funky: 'Nau grahas se milo',
      seedha: 'The nine grahas',
      sick: 'Meet the nine grahas',
    },
    body: {
      funky: `Jyotish ke **nau grahas** (graspers / influencers):

- **Sun** — vitality, authority, father themes  
- **Moon** — mind, mother, daily feel weather  
- **Mars** — drive, heat, conflict skill  
- **Mercury** — speech, trade, wit  
- **Jupiter** — growth, wisdom, grace  
- **Venus** — pleasure, arts, bonds  
- **Saturn** — time, duty, pressure that builds bone  
- **Rahu** — hunger, foreign stretch, obsession edge  
- **Ketu** — release, insight, past-thread detach  

Har ek rashi + house mein baitha. Dignity, aspects, yogas = pattern language — tools, handcuffs nahi. Report tiles poke karo, whole swallow mat.`,
      seedha: `Nine grahas are used: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu.

Each has a sign and house placement. Strength notes and yogas describe classical patterns for study. Explore them in the report; treat readings as guidance for reflection, not fixed fate.`,
      sick: `Jyotish tracks **nine grahas** (graspers / influencers):

- **Sun** — vitality, authority, father themes  
- **Moon** — mind, mother, daily feel weather  
- **Mars** — drive, heat, conflict skill  
- **Mercury** — speech, trade, wit  
- **Jupiter** — growth, wisdom, grace  
- **Venus** — pleasure, arts, bonds  
- **Saturn** — time, duty, pressure that builds bone  
- **Rahu** — hunger, foreign stretch, obsession edge  
- **Ketu** — release, insight, past-thread detach  

Each sits in a rashi and a house. Dignity, aspects, yogas = pattern language — tools, not handcuffs. Poke the report tiles; don’t swallow whole.`,
    },
  },
  {
    id: 'dasha',
    art: 'dasha' as const,
    title: {
      funky: 'Vimshottari — timing ka plot twist',
      seedha: 'Vimshottari dasha timing',
      sick: 'Vimshottari — the timing plot twist',
    },
    body: {
      funky: `**Vimshottari** = 120-year dasha scheme, Moon ke **nakshatra** se seed. Life = planetary seasons ki playlist:

1. **Mahadasha** — lamba weather system  
2. **Antardasha** — uske andar ka chapter  
3. **Pratyantar** — short scene  

Birthplot timeline scrubable hai. Highlighted slice = “abhi.”

Timing = forecast. Prison sentence nahi. Effort + context still plot likhte hain.`,
      seedha: `**Vimshottari** timing is seeded from the Moon’s nakshatra at birth. It divides life into planetary periods: mahadasha (long), antardasha (medium), and pratyantar (short).

The timing page highlights the current period. Use it as a map of seasons, not as a fixed prediction of destiny.`,
      sick: `**Vimshottari** is a 120-year dasha scheme seeded from the Moon’s **nakshatra** at birth. Life unfolds as planetary seasons:

1. **Mahadasha** — the long weather system  
2. **Antardasha** — the chapter inside it  
3. **Pratyantar** — the short scene  

Birthplot draws a scrubable timeline. Highlighted slice = “now.”

Read timing like a forecast — useful for orientation, useless as a prison sentence. Effort + context still write the plot.`,
    },
  },
] as const
