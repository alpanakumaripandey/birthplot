import { useEffect, type ReactNode } from 'react'

type Props = {
  open: boolean
  title: string
  subtitle?: string
  art?: string
  onClose: () => void
  children: ReactNode
}

export function DetailDrawer({ open, title, subtitle, art, onClose, children }: Props) {
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  return (
    <>
      <div
        className={`drawer-backdrop${open ? ' open' : ''}`}
        onClick={onClose}
        aria-hidden={!open}
      />
      <aside
        className={`detail-drawer${open ? ' open' : ''}`}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        aria-hidden={!open}
      >
        <div className="drawer-head">
          <div>
            <h2>{title}</h2>
            {subtitle && <p className="drawer-sub">{subtitle}</p>}
          </div>
          <button type="button" className="drawer-close" onClick={onClose} aria-label="Close">
            Close
          </button>
        </div>
        <div className="drawer-body">
          {art && <div className="drawer-art-band" style={{ backgroundImage: `url('${art}')` }} />}
          {children}
        </div>
      </aside>
    </>
  )
}
