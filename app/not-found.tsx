export default function NotFound() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: '#0a0a0a', color: '#fff', fontFamily: 'DM Sans, sans-serif' }}>
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ fontSize: '4rem', fontFamily: 'Bebas Neue, sans-serif', letterSpacing: 2 }}>404</h1>
        <p style={{ opacity: 0.6 }}>Page not found</p>
        <a href="/" style={{ color: '#00e5ff', textDecoration: 'none', marginTop: 16, display: 'inline-block' }}>← Back to Control Center</a>
      </div>
    </div>
  )
}
