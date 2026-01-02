import { useState, useEffect } from 'react'
import Header from './components/Header'
import SearchBar from './components/SearchBar'
import ContactsList from './components/ContactsList'
import CallPanel from './components/CallPanel'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`

export default function App() {
  const [contacts, setContacts] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [pbxStatus, setPbxStatus] = useState('disconnected')
  const [extension, setExtension] = useState(() => {
    // Carica l'interno dal localStorage
    return localStorage.getItem('userExtension') || ''
  })
  const [darkMode, setDarkMode] = useState(() => {
    // Carica il tema dal localStorage
    return localStorage.getItem('darkMode') === 'true'
  })

  useEffect(() => {
    // Fetch contacts from API
    fetchContacts()
    // Check PBX status
    checkPbxStatus()
    
    const statusInterval = setInterval(checkPbxStatus, 5000)
    return () => clearInterval(statusInterval)
  }, [])

  useEffect(() => {
    // Salva l'interno nel localStorage quando cambia
    if (extension) {
      localStorage.setItem('userExtension', extension)
    }
  }, [extension])

  useEffect(() => {
    // Salva il tema nel localStorage e applica la classe al body
    localStorage.setItem('darkMode', darkMode)
    if (darkMode) {
      document.body.classList.add('dark-mode')
    } else {
      document.body.classList.remove('dark-mode')
    }
  }, [darkMode])

  const fetchContacts = async () => {
    try {
      const response = await fetch(`${API_URL}/api/contacts`)
      if (response.ok) {
        const data = await response.json()
        setContacts(data)
      }
    } catch (error) {
      console.error('Failed to fetch contacts:', error)
    }
  }

  const checkPbxStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/status`)
      if (response.ok) {
        const data = await response.json()
        setPbxStatus(data.status || 'connected')
      } else {
        setPbxStatus('disconnected')
      }
    } catch (error) {
      setPbxStatus('disconnected')
    }
  }

  const filteredContacts = contacts.filter(contact =>
    contact.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    contact.number?.includes(searchTerm)
  )

  return (
    <div className="app">
      <Header pbxStatus={pbxStatus} darkMode={darkMode} onToggleDarkMode={() => setDarkMode(!darkMode)} />
      <main className="app-main">
        <SearchBar 
          searchTerm={searchTerm} 
          onSearchChange={setSearchTerm}
          extension={extension}
          onExtensionChange={setExtension}
        />
        <div className="app-content">
          <ContactsList 
            contacts={filteredContacts}
            extension={extension}
            apiUrl={API_URL}
          />
        </div>
      </main>
    </div>
  )
}
