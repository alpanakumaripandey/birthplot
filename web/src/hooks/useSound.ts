import { useCallback } from 'react'
import { playSfx, type SfxName } from '../lib/sfx'
import { usePrefs } from './usePrefs'

export function useSound() {
  const { sound, motion } = usePrefs()
  const enabled = sound && motion !== 'calm'

  const play = useCallback((name: SfxName) => playSfx(name, enabled), [enabled])

  return { play, enabled }
}
