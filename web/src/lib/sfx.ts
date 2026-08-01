/** Soft synthesized UI sounds (Web Audio) — no binary assets required. */

export type SfxName = 'tap' | 'cast' | 'drawer' | 'success' | 'toggle'

let ctx: AudioContext | null = null

function getCtx(): AudioContext | null {
  if (typeof window === 'undefined') return null
  try {
    if (!ctx) ctx = new AudioContext()
    if (ctx.state === 'suspended') void ctx.resume()
    return ctx
  } catch {
    return null
  }
}

function tone(
  audio: AudioContext,
  {
    freq,
    dur = 0.12,
    type = 'sine',
    gain = 0.04,
    delay = 0,
    slideTo,
  }: {
    freq: number
    dur?: number
    type?: OscillatorType
    gain?: number
    delay?: number
    slideTo?: number
  },
) {
  const t0 = audio.currentTime + delay
  const osc = audio.createOscillator()
  const g = audio.createGain()
  osc.type = type
  osc.frequency.setValueAtTime(freq, t0)
  if (slideTo != null) {
    osc.frequency.exponentialRampToValueAtTime(Math.max(1, slideTo), t0 + dur)
  }
  g.gain.setValueAtTime(0.0001, t0)
  g.gain.exponentialRampToValueAtTime(gain, t0 + 0.015)
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur)
  osc.connect(g)
  g.connect(audio.destination)
  osc.start(t0)
  osc.stop(t0 + dur + 0.02)
}

const PLAYERS: Record<SfxName, (a: AudioContext) => void> = {
  tap: (a) => tone(a, { freq: 520, dur: 0.06, gain: 0.025, type: 'triangle' }),
  toggle: (a) => {
    tone(a, { freq: 380, dur: 0.07, gain: 0.03, type: 'sine' })
    tone(a, { freq: 520, dur: 0.08, gain: 0.025, delay: 0.05, type: 'sine' })
  },
  drawer: (a) => tone(a, { freq: 240, dur: 0.14, gain: 0.03, slideTo: 160, type: 'sine' }),
  cast: (a) => {
    tone(a, { freq: 220, dur: 0.18, gain: 0.035, type: 'sine' })
    tone(a, { freq: 330, dur: 0.2, gain: 0.03, delay: 0.08, type: 'triangle' })
    tone(a, { freq: 440, dur: 0.22, gain: 0.025, delay: 0.16, type: 'sine' })
  },
  success: (a) => {
    tone(a, { freq: 392, dur: 0.12, gain: 0.035, type: 'triangle' })
    tone(a, { freq: 523, dur: 0.16, gain: 0.03, delay: 0.1, type: 'sine' })
    tone(a, { freq: 659, dur: 0.2, gain: 0.028, delay: 0.2, type: 'sine' })
  },
}

export function playSfx(name: SfxName, enabled: boolean) {
  if (!enabled) return
  const audio = getCtx()
  if (!audio) return
  try {
    PLAYERS[name](audio)
  } catch {
    /* ignore autoplay / context errors */
  }
}
