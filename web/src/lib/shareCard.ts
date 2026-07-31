import type { FullReport } from '../types'

/** Render a shareable 1080x1350 chart card PNG and trigger download. */
export async function downloadChartCard(report: FullReport): Promise<void> {
  const W = 1080
  const H = 1350
  const canvas = document.createElement('canvas')
  canvas.width = W
  canvas.height = H
  const ctx = canvas.getContext('2d')
  if (!ctx) throw new Error('Canvas not available')

  // Background
  const grad = ctx.createLinearGradient(0, 0, W, H)
  grad.addColorStop(0, '#1a2a2e')
  grad.addColorStop(0.5, '#162226')
  grad.addColorStop(1, '#101a1d')
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, W, H)

  // Accent orbs
  ctx.fillStyle = 'rgba(61, 181, 173, 0.15)'
  ctx.beginPath()
  ctx.arc(180, 200, 220, 0, Math.PI * 2)
  ctx.fill()
  ctx.fillStyle = 'rgba(212, 176, 106, 0.12)'
  ctx.beginPath()
  ctx.arc(900, 1100, 280, 0, Math.PI * 2)
  ctx.fill()

  // Logo diamond
  ctx.strokeStyle = '#d4b06a'
  ctx.lineWidth = 4
  ctx.beginPath()
  ctx.moveTo(540, 80)
  ctx.lineTo(620, 160)
  ctx.lineTo(540, 240)
  ctx.lineTo(460, 160)
  ctx.closePath()
  ctx.stroke()
  ctx.fillStyle = '#3db5ad'
  ctx.beginPath()
  ctx.moveTo(540, 110)
  ctx.lineTo(590, 160)
  ctx.lineTo(540, 210)
  ctx.lineTo(490, 160)
  ctx.closePath()
  ctx.fill()

  ctx.fillStyle = '#e8f0f2'
  ctx.font = '700 64px Fraunces, Georgia, serif'
  ctx.textAlign = 'center'
  ctx.fillText('Birthplot', 540, 320)

  const name = report.chart.birth.name
  ctx.font = '600 52px Fraunces, Georgia, serif'
  ctx.fillStyle = '#d4b06a'
  ctx.fillText(name, 540, 420)

  ctx.fillStyle = '#a8bdc4'
  ctx.font = '400 28px DM Sans, sans-serif'
  ctx.fillText(report.chart.birth.birth_date, 540, 470)
  ctx.fillText(report.chart.place.display_name.slice(0, 48), 540, 510)

  // Info blocks
  const blocks = [
    ['Lagna', report.chart.lagna.rashi_name],
    ['Moon', `${report.chart.moon_nakshatra} · pada ${report.chart.moon_pada}`],
    [
      'Dasha',
      report.timeline.current_mahadasha
        ? `${report.timeline.current_mahadasha.lord}${
            report.timeline.current_antardasha
              ? `–${report.timeline.current_antardasha.lord}`
              : ''
          }`
        : '—',
    ],
  ]

  let y = 600
  for (const [label, value] of blocks) {
    ctx.fillStyle = 'rgba(61, 181, 173, 0.2)'
    roundRect(ctx, 120, y, 840, 110, 8)
    ctx.fill()
    ctx.fillStyle = '#5fd0c8'
    ctx.font = '600 24px DM Sans, sans-serif'
    ctx.textAlign = 'left'
    ctx.fillText(label.toUpperCase(), 160, y + 42)
    ctx.fillStyle = '#e8f0f2'
    ctx.font = '600 36px Fraunces, Georgia, serif'
    ctx.fillText(value, 160, y + 88)
    y += 140
  }

  // Diamond sketch
  ctx.strokeStyle = 'rgba(212, 176, 106, 0.55)'
  ctx.lineWidth = 2
  const cx = 540
  const cy = 1120
  const s = 90
  ctx.beginPath()
  ctx.moveTo(cx, cy - s)
  ctx.lineTo(cx + s, cy)
  ctx.lineTo(cx, cy + s)
  ctx.lineTo(cx - s, cy)
  ctx.closePath()
  ctx.stroke()
  ctx.beginPath()
  ctx.moveTo(cx - s, cy - s)
  ctx.lineTo(cx + s, cy - s)
  ctx.lineTo(cx + s, cy + s)
  ctx.lineTo(cx - s, cy + s)
  ctx.closePath()
  ctx.stroke()

  ctx.fillStyle = '#a8bdc4'
  ctx.font = '400 20px DM Sans, sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText('Lahiri · whole-sign · for learning', 540, 1300)

  const blob = await new Promise<Blob | null>((res) => canvas.toBlob(res, 'image/png'))
  if (!blob) throw new Error('PNG export failed')
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `birthplot_${name.replace(/\s+/g, '_')}.png`
  a.click()
  URL.revokeObjectURL(url)
}

function roundRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.arcTo(x + w, y, x + w, y + h, r)
  ctx.arcTo(x + w, y + h, x, y + h, r)
  ctx.arcTo(x, y + h, x, y, r)
  ctx.arcTo(x, y, x + w, y, r)
  ctx.closePath()
}
