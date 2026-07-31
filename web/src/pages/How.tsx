export function How() {
  return (
    <section className="section wrap page-enter">
      <div
        className="page-art-band"
        style={{ backgroundImage: "url('/art/wheel-atmosphere.png')" }}
        aria-hidden
      />
      <h1 className="section-title">How Birthplot works</h1>
      <p className="lede">
        Classical Jyotish math, local machine, no cloud crystal ball. Here’s the method, straight.
      </p>

      <h2 style={{ fontFamily: 'var(--font-display)' }}>The stack under the hood</h2>
      <ul className="blurb-list">
        <li>
          <strong>Sidereal zodiac + Lahiri ayanamsa</strong> — Indian standard offset from tropical positions.
        </li>
        <li>
          <strong>Whole-sign houses</strong> — House 1 is your Lagna rashi; the rest follow in order. Clean for beginners.
        </li>
        <li>
          <strong>Nine grahas</strong> — Sun through Saturn plus Rahu/Ketu. Positions via Skyfield (JPL) + node math.
        </li>
        <li>
          <strong>Vimshottari dasha</strong> — Seeded from Moon nakshatra; mahadasha, antardasha, pratyantar strips.
        </li>
        <li>
          <strong>Interactive diamond</strong> — North-Indian style map you can tap; details live in the drawer.
        </li>
      </ul>

      <h2 style={{ fontFamily: 'var(--font-display)', marginTop: '2rem' }}>Disclaimer</h2>
      <p>
        This report uses classical Jyotish computation for learning and reflective guidance. It is not
        medical, legal, financial, or destiny advice. For important life decisions, consult a qualified
        professional. Your choices still write the plot.
      </p>

      <h2 style={{ fontFamily: 'var(--font-display)', marginTop: '2rem' }}>Run it local</h2>
      <p>
        API on port 8000, Vite on 5173. Chart JSON lives in your browser sessionStorage until you cast again.
      </p>
    </section>
  )
}
