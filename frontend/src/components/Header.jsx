import './Header.css'
import { Phone } from 'lucide-react'

export default function Header({ pbxStatus, darkMode, onToggleDarkMode }) {
  const statusColor = pbxStatus === 'connected' ? '#10b981' : '#ef4444'
  const statusText = pbxStatus === 'connected' ? 'Connesso' : 'Disconnesso'

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <Phone size={28} strokeWidth={2.5} />
          </div>
          <h1>Rubrica Telefonica</h1>
        </div>
        <div className="header-controls">
          <div className="status-indicator">
            <div className="status-dot" style={{ backgroundColor: statusColor }}></div>
            <span>{statusText}</span>
          </div>
          <button className="theme-toggle" onClick={onToggleDarkMode} title={darkMode ? 'Tema chiaro' : 'Tema scuro'}>
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
      </div>
    </header>
  )
}
