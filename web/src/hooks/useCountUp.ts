import { useEffect, useState } from 'react'

/** Tick a number from 0 to target when `active`. */
export function useCountUp(target: number, active: boolean, ms = 600) {
  const [value, setValue] = useState(0)
  useEffect(() => {
    if (!active) {
      setValue(0)
      return
    }
    const start = performance.now()
    let raf = 0
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / ms)
      const eased = 1 - (1 - t) ** 3
      setValue(target * eased)
      if (t < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [target, active, ms])
  return value
}
