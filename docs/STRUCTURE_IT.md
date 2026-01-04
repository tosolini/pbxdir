# 📁 Struttura Progetto

```
pbxdir/
│
├── 📚 DOCUMENTAZIONE
│   ├── README.md              # Overview progetto e indice documentazione
│   ├── QUICKSTART.md          # ⭐ INIZIO QUI - Guida installazione rapida
│   ├── CONFIG.md              # Guida configurazione completa
│   ├── API.md                 # Documentazione REST API endpoints
│   └── DEPLOYMENT.md          # Guida per deployment in produzione
│
├── 🏗️ BACKEND (Python/FastAPI)
│   ├── Dockerfile             # Container backend
│   ├── requirements.txt        # Dipendenze Python
│   ├── config.py              # Configurazione (PBX_HOST, ecc)
│   ├── main.py                # FastAPI app principale
│   ├── pbx_manager.py         # Gestione connessione AMI
│   ├── contacts_manager.py    # Caricamento contatti da JSON
│   └── numeri.json            # Database contatti (JSON)
│
├── 🎨 FRONTEND (React/Vite)
│   ├── Dockerfile             # Container frontend (multi-stage)
│   ├── package.json           # Dipendenze Node.js
│   ├── vite.config.js         # Config build tool Vite
│   ├── public/
│   │   └── index.html         # HTML template
│   └── src/
│       ├── main.jsx           # Entry point React
│       ├── App.jsx            # Component principale
│       ├── App.css            # Stili app
│       ├── index.css          # Stili globali + dark mode
│       └── components/        # Componenti React
│           ├── Header.jsx/.css       # Intestazione + toggle tema
│           ├── SearchBar.jsx/.css    # Search e input interno
│           └── ContactsList.jsx/.css # Lista contatti con pulsanti chiama
│
├── 🐳 INFRASTRUTTURA
│   ├── docker-compose.yml     # Orchestrazione container (backend + frontend)
   └── .gitignore             # File ignorati da git

```

## 📖 Quale File Leggere?

| Situazione | File da leggere |
|-----------|-----------------|
| **Sono nuovo al progetto** | 📍 [QUICKSTART.md](QUICKSTART.md) |
| **Devo installare su nuovo server** | 📍 [QUICKSTART.md](QUICKSTART.md) |
| **Devo configurare PBX/contatti** | [CONFIG.md](CONFIG.md) |
| **Devo integrare le API** | [API.md](API.md) |
| **Devo fare deployment in produzione** | [DEPLOYMENT.md](DEPLOYMENT.md) |
| **Voglio overview del progetto** | [README.md](README.md) |

## 🚀 Comandi Essenziali

```bash
# Installazione
docker compose up -d --build

# Stop
docker compose down

# Log
docker compose logs -f

# Riavvia
docker compose restart
```

## 🔧 File Importanti da Editare

1. **`backend/.env`** - Configurazione PBX
   ```env
   PBX_HOST=192.168.1.1
   PBX_PORT=5038
   PBX_USERNAME=admin
   PBX_PASSWORD=manager
   ```

2. **`backend/numeri.json`** - Contatti
   ```json
   [
     {
       "id": 0,
       "name": "Mario Rossi",
       "number": "3391234567",
       "email": "mario@company.com",
       ...
     }
   ]
   ```

3. **`frontend/src/App.jsx`** - URL API
   ```javascript
   const API_URL = 'http://192.168.1.1:8000'  // Modifica qui se necessario
   ```

## 📊 Architettura High-Level

```
┌─────────────────────────────────────────┐
│      🌐 Browser (http://localhost:3000) │
│          React + Vite UI                │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│    🔄 FastAPI Backend (port 8000)       │
│   - /api/contacts                       │
│   - /api/status                         │
│   - /api/call (originate)               │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│   📞 Asterisk Manager (port 5038)       │
│   FreePBX/Asterisk Server               │
│   - Originate call action               │
│   - Channel: SIP/{extension}            │
└─────────────────────────────────────────┘
```

## ✅ Checklist Setup

- [ ] Docker installato
- [ ] Repository clonato
- [ ] `backend/.env` creato
- [ ] `docker compose up -d --build` eseguito
- [ ] `http://localhost:3000` accessibile
- [ ] `/api/status` mostra "connected"
- [ ] Contatti visibili nella lista
- [ ] Test chiamata riuscito

## 🎯 Prossimi Passi

1. Leggi [QUICKSTART.md](QUICKSTART.md)
2. Installa il progetto sul tuo server
3. Configura le credenziali FreePBX
4. Personalizza i contatti
5. Effettua una prova di chiamata

---

**Domande?** Consulta il file `.md` appropriato sopra!
