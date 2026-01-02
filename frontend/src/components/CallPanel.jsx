import { useState } from 'react'
import './CallPanel.css'

export default function CallPanel({ selectedContact, apiUrl, extension }) {
  const [isLoading, setIsLoading] = useState(false)

  const handleCall = async () => {
    if (!selectedContact) return
    
    if (!extension || extension.trim() === '') {
      alert('Inserisci il tuo numero interno nella barra in alto')
      return
    }
    
    setIsLoading(true)
    try {
      const response = await fetch(
        `${apiUrl}/call`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            number: selectedContact.number,
            extension: extension.trim()
          })
        }
      )
      
      const data = await response.json()
      
      if (response.ok && data.status === 'success') {
        alert(`Chiamata avviata dal tuo interno ${extension} verso ${selectedContact.name || selectedContact.number}`)
      } else {
        alert(`Errore: ${data.message || 'Chiamata non riuscita'}`)
      }
    } catch (error) {
      alert('Errore durante la chiamata')
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="call-panel">
      <h2>Gestione Chiamate</h2>

      {selectedContact ? (
        <div className="call-info">
          <div className="selected-contact">
            <p className="contact-label">Contatto selezionato:</p>
            <p className="contact-name">{selectedContact.name || 'Sconosciuto'}</p>
            <div className="contact-details">
              <div className="detail-item">
                <span className="detail-icon">📞</span>
                <span className="contact-number">{selectedContact.number}</span>
              </div>
              {selectedContact.email && (
                <div className="detail-item">
                  <span className="detail-icon">✉️</span>
                  <span className="contact-email">{selectedContact.email}</span>
                </div>
              )}
              {selectedContact.shortInternal && (
                <div className="detail-item">
                  <span className="detail-icon">📍</span>
                  <span className="contact-internal">Interno: {selectedContact.shortInternal}</span>
                </div>
              )}
              {selectedContact.role && (
                <div className="detail-item">
                  <span className="detail-icon">💼</span>
                  <span className="contact-role">{selectedContact.role}</span>
                </div>
              )}
            </div>
          </div>
          <button 
            className="call-button" 
            onClick={handleCall}
            disabled={isLoading || !extension}
          >
            {isLoading ? '⏳ Chiamata...' : '☎️ Chiama'}
          </button>
        </div>
      ) : (
        <p className="no-selection">Seleziona un contatto per effettuare una chiamata</p>
      )}
    </div>
  )
}
