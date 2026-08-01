import { useRef, type MouseEvent, type ReactNode } from 'react'
import { Link } from 'react-router-dom'

type Common = {
  children: ReactNode
  className?: string
  magnetic?: boolean
}

type BtnProps = Common & {
  as?: 'button'
  type?: 'button' | 'submit'
  disabled?: boolean
  onClick?: () => void
}

type LinkProps = Common & {
  as: 'link'
  to: string
  onClick?: () => void
}

type Props = BtnProps | LinkProps

/** Primary CTA with optional magnetic pull toward cursor. */
export function MagneticButton(props: Props) {
  const ref = useRef<HTMLElement | null>(null)

  function onMove(e: MouseEvent) {
    if (props.magnetic === false) return
    if (document.documentElement.getAttribute('data-motion') === 'calm') return
    const el = ref.current
    if (!el) return
    const r = el.getBoundingClientRect()
    const cx = r.left + r.width / 2
    const cy = r.top + r.height / 2
    const dx = e.clientX - cx
    const dy = e.clientY - cy
    const dist = Math.hypot(dx, dy)
    if (dist > 80) {
      el.style.transform = ''
      return
    }
    const pull = 1 - dist / 80
    el.style.transform = `translate(${dx * 0.18 * pull}px, ${dy * 0.18 * pull}px)`
  }

  function onLeave() {
    if (ref.current) ref.current.style.transform = ''
  }

  const cls = `btn magnetic-btn ${props.className ?? ''}`

  if (props.as === 'link') {
    return (
      <Link
        ref={ref as never}
        to={props.to}
        className={cls}
        onClick={props.onClick}
        onMouseMove={onMove}
        onMouseLeave={onLeave}
      >
        {props.children}
      </Link>
    )
  }

  return (
    <button
      ref={ref as never}
      type={props.type ?? 'button'}
      className={cls}
      disabled={props.disabled}
      onClick={props.onClick}
      onMouseMove={onMove}
      onMouseLeave={onLeave}
    >
      {props.children}
    </button>
  )
}
