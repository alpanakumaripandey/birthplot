import { useRef, type CSSProperties, type MouseEvent, type ReactNode } from 'react'

type Props = {
  children: ReactNode
  className?: string
  onClick?: () => void
  as?: 'button' | 'div' | 'article'
  disabled?: boolean
}

/** 3D tilt toward cursor — disabled when data-motion=calm. */
export function TiltCard({
  children,
  className = '',
  onClick,
  as = 'button',
  disabled,
}: Props) {
  const ref = useRef<HTMLElement | null>(null)

  function onMove(e: MouseEvent) {
    const el = ref.current
    if (!el) return
    if (document.documentElement.getAttribute('data-motion') === 'calm') return
    const r = el.getBoundingClientRect()
    const x = (e.clientX - r.left) / r.width - 0.5
    const y = (e.clientY - r.top) / r.height - 0.5
    el.style.setProperty('--tilt-x', `${(-y * 8).toFixed(2)}deg`)
    el.style.setProperty('--tilt-y', `${(x * 10).toFixed(2)}deg`)
    el.style.setProperty('--glint-x', `${(x + 0.5) * 100}%`)
    el.style.setProperty('--glint-y', `${(y + 0.5) * 100}%`)
  }

  function onLeave() {
    const el = ref.current
    if (!el) return
    el.style.setProperty('--tilt-x', '0deg')
    el.style.setProperty('--tilt-y', '0deg')
  }

  const style = {
    '--tilt-x': '0deg',
    '--tilt-y': '0deg',
    '--glint-x': '50%',
    '--glint-y': '50%',
  } as CSSProperties

  const props = {
    ref: ref as never,
    className: `tilt-card ${className}`,
    style,
    onMouseMove: onMove,
    onMouseLeave: onLeave,
    onClick,
  }

  if (as === 'article') return <article {...props}>{children}</article>
  if (as === 'div') return <div {...props}>{children}</div>
  return (
    <button type="button" disabled={disabled} {...props}>
      {children}
    </button>
  )
}
