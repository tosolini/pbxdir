# Rubrica Telefonica - PBX Call Manager

Una moderna applicazione web per gestire chiamate VoIP tramite FreePBX/Asterisk. Consente di visualizzare contatti, effettuare chiamate attraverso Asterisk Manager Interface (AMI) e inviare email direttamente dai contatti.

## 📚 Documentazione

| File | Descrizione |
|------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | **INIZIO QUI** - Installazione e primo avvio (5 min) |
| [README.md](README.md) | Questo file - Overview del progetto |
| [CONFIG.md](CONFIG.md) | Guida configurazione completa |
| [API.md](API.md) | Documentazione REST API |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Guida per deployment in produzione |

**Per nuovi utenti**: Leggi [QUICKSTART.md](QUICKSTART.md) prima di tutto!

## 🎯 Caratteristiche

- **Interfaccia moderna e responsiva**: UI intuitiva con supporto light/dark mode
- **Gestione contatti**: Visualizza lista completa di contatti con multipli numeri e interni
- **Chiamate VoIP**: Integrazione diretta con FreePBX via AMI per originate call
- **Multipli numeri**: Supporto per cellulare, ufficio e numero centralino
- **Email cliccabili**: Apri il client di posta predefinito con un click
- **Interni callabili**: Chiama direttamente gli interni di altri dipendenti
- **Persistenza locale**: Salva automaticamente l'interno dell'utente in localStorage
- **Tema personalizzabile**: Toggle light/dark mode con persistenza

## 🏗️ Architettura

### Backend
- **Framework**: FastAPI con Uvicorn
- **Integrazione PBX**: pyst2 (Asterisk Manager Interface)
- **Python**: 3.11-slim
- **Endpoints API**:
  - `GET /api/health` - Health check
  - `GET /api/status` - Stato connessione AMI
  - `GET /api/contacts` - Lista contatti da numeri.json
  - `POST /api/call` - Originate call verso numero/interno

### Frontend
- **Framework**: React 18 con Vite
- **Build tool**: Node 18-alpine per build
- **Serving**: Python http.server
- **Dipendenze**: lucide-react per icone, axios per API

### Dati
- **Format**: JSON (numeri.json)
- **Campi contatto**:
  - `id`: identificativo univoco
  - `name`: nome contatto
  - `number`: numero cellulare/principale
  - `office`: numero ufficio (opzionale)
  - `shortInternal`: interno centralino (opzionale)
  - `email`: indirizzo email
  - `role`: ruolo/titolo
  - `department`: reparto

## 🚀 Quick Start

Vedi [QUICKSTART.md](QUICKSTART.md) per le istruzioni di installazione e deployment.

### Setup Rapido (2 minuti)

```bash
# 1. Clona repository
git clone <repo-url> pbxdir && cd pbxdir

# 2. Copia e configura file di esempio
cp backend/.env.example backend/.env
cp numeri.json.example numeri.json

# 3. Modifica backend/.env con le tue credenziali FreePBX
nano backend/.env

# 4. Modifica numeri.json con i tuoi contatti
nano numeri.json

# 5. Avvia
docker compose up -d --build

# 6. Accedi
open http://localhost:3000
```

**⚠️ IMPORTANTE**: Non committare mai i file `backend/.env` e `numeri.json` (contengono dati sensibili)!

## 📋 Configurazione Dettagliata

Per configurazione completa vedi [CONFIG.md](CONFIG.md).

### Environment Backend
Crea un file `.env` nella directory `backend/`:

```env
PBX_HOST=192.168.1.1
PBX_PORT=5038
PBX_USERNAME=admin
PBX_PASSWORD=manager
```

### Contatti
Modifica `backend/numeri.json` per aggiungere/modificare contatti:

```json
{
  "id": 0,
  "name": "Nome Cognome [Tipo]",
  "number": "33912345678",
  "office": "021234567",
  "shortInternal": "201",
  "email": "user@company.com",
  "role": "Ruolo",
  "department": "Reparto"
}
```

## 🔧 Uso

### Effettuare una chiamata
1. Inserisci il tuo interno nella barra di ricerca in alto
2. Seleziona un contatto dalla lista
3. Clicca su "Chiama" accanto al numero desiderato
4. La chiamata verrà instradata tramite FreePBX al tuo interno

### Inviare email
- Clicca su qualsiasi indirizzo email per aprire il client di posta predefinito

### Cambiare tema
- Clicca sull'icona sole/luna in alto a destra

## 📦 Struttura File

```
pbxdir/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configurazione
│   ├── pbx_manager.py       # Gestione AMI
│   ├── contacts_manager.py  # Gestione contatti
│   ├── numeri.json          # Database contatti
│   ├── requirements.txt      # Dipendenze Python
│   └── Dockerfile           # Container backend
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Component principale
│   │   ├── App.css          # Stili app
│   │   ├── index.css        # Stili globali + dark mode
│   │   ├── main.jsx         # Entry point
│   │   └── components/
│   │       ├── Header.jsx/.css
│   │       ├── SearchBar.jsx/.css
│   │       └── ContactsList.jsx/.css
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile           # Container frontend
│   └── public/index.html
├── docker-compose.yml       # Orchestrazione
└── README.md               # Questo file
```

## 🐳 Docker

L'applicazione è containerizzata con docker-compose per facile deployment.

```bash
# Avviare
docker compose up -d --build

# Fermare
docker compose down

# Log
docker compose logs -f
```

## 🌐 Accesso

Una volta in esecuzione:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔌 Requisiti FreePBX/Asterisk

- AMI abilitato sulla porta 5038
- Utente AMI con permessi per `originate`
- Numero esterno configurato sul sistema

## 📝 Note

- L'interno dell'utente viene salvato in localStorage
- Il tema (light/dark) viene salvato in localStorage
- Le email sono link mailto:// cliccabili
- Supporta contatti con multipli numeri (cellulare, ufficio, interno)

## 🤝 Supporto

Per problemi o domande, consulta i log:
```bash
docker compose logs backend  # Backend
docker compose logs frontend # Frontend
```

## 📄 Licenza

Proprietario
