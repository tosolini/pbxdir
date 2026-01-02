import { useState } from 'react'
import { Phone } from 'lucide-react'
import './ContactsList.css'

export default function ContactsList({ contacts, extension, apiUrl }) {
  const [calling, setCalling] = useState(null)

  const handleCall = async (phoneNumber, contactName, e) => {
    e.stopPropagation()
    
    if (!extension) {
      alert('Inserisci il tuo interno prima di effettuare una chiamata')
      return
    }

    setCalling(phoneNumber)
    try {
      const response = await fetch(`${apiUrl}/api/call`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          number: phoneNumber,
          extension: extension
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        alert(`Chiamata in corso verso ${contactName} (${phoneNumber})`)
      } else {
        alert(`Errore: ${data.detail || 'Impossibile effettuare la chiamata'}`)
      }
    } catch (error) {
      alert('Errore di connessione al server')
    } finally {
      setCalling(null)
    }
  }

  return (
    <div className="contacts-list-container">
      <h2>Contatti</h2>
      <div className="contacts-list">
        {contacts.length === 0 ? (
          <p className="empty-state">Nessun contatto trovato</p>
        ) : (
          contacts.map((contact) => (
            <div
              key={contact.id || contact.number}
              className="contact-item"
            >
              <div className="contact-info">
                <div className="contact-name">{contact.name || 'Sconosciuto'}</div>
                
                <div className="contact-phones">
                  {contact.number && (
                    <div className="phone-row">
                      <span className="phone-label">📞</span>
                      <span className="phone-number">{contact.number}</span>
                      <button 
                        className="call-button-inline"
                        onClick={(e) => handleCall(contact.number, contact.name, e)}
                        disabled={calling === contact.number}
                      >
                        <Phone size={14} />
                        {calling === contact.number ? 'Chiama...' : 'Chiama'}
                      </button>
                    </div>
                  )}
                  
                  {contact.office && (
                    <div className="phone-row">
                      <span className="phone-label">🏢</span>
                      <span className="phone-number">{contact.office}</span>
                      <button 
                        className="call-button-inline"
                        onClick={(e) => handleCall(contact.office, contact.name, e)}
                        disabled={calling === contact.office}
                      >
                        <Phone size={14} />
                        {calling === contact.office ? 'Chiama...' : 'Chiama'}
                      </button>
                    </div>
                  )}
                </div>
                
                {contact.email && (
                  <a href={`mailto:${contact.email}`} className="contact-email">
                    ✉️ {contact.email}
                  </a>
                )}
                {contact.role && (
                  <div className="contact-role">💼 {contact.role}</div>
                )}
                {contact.shortInternal && (
                  <div className="internal-row">
                    <span className="internal-label">📍 Interno: {contact.shortInternal}</span>
                    <button 
                      className="call-button-inline"
                      onClick={(e) => handleCall(contact.shortInternal, contact.name, e)}
                      disabled={calling === contact.shortInternal}
                    >
                      <Phone size={14} />
                      {calling === contact.shortInternal ? 'Chiama...' : 'Chiama'}
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
