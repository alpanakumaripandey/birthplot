import { COPY, type CopyKey } from '../copy'
import { usePrefs } from './usePrefs'

export function useLingo() {
  const { lingo } = usePrefs()
  const t = (key: CopyKey) => COPY[key][lingo]
  return { mode: lingo, t }
}
