import './SearchBar.css'

export default function SearchBar({ searchTerm, onSearchChange, extension, onExtensionChange }) {
  return (
    <div className="search-bar">
      <div className="search-input-container">
        <input
          type="text"
          placeholder="Cerca contatti per nome o numero..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="search-input"
        />
      </div>
      
      <div className="extension-input-container">
        <label htmlFor="extension">Il tuo interno:</label>
        <input
          id="extension"
          type="text"
          placeholder="es. 233"
          value={extension}
          onChange={(e) => onExtensionChange(e.target.value)}
          className="extension-input"
        />
      </div>
    </div>
  )
}
