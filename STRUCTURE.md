# 📁 Project Structure

```
pbxdir/
│
├── 📚 DOCUMENTATION
│   ├── README.md              # Project overview and documentation index
│   ├── QUICKSTART.md          # ⭐ START HERE - Quick installation guide
│   ├── CONFIG.md              # Complete configuration guide
│   ├── API.md                 # REST API endpoints documentation
│   └── DEPLOYMENT.md          # Production deployment guide
│
├── 🏗️ BACKEND (Python/FastAPI)
│   ├── Dockerfile             # Backend container
│   ├── requirements.txt        # Python dependencies
│   ├── config.py              # Configuration (PBX_HOST, etc)
│   ├── main.py                # FastAPI main app
│   ├── pbx_manager.py         # AMI connection management
│   ├── contacts_manager.py    # Load contacts from JSON
│   └── numeri.json            # Contacts database (JSON)
│
├── 🎨 FRONTEND (React/Vite)
│   ├── Dockerfile             # Frontend container (multi-stage)
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite build tool config
│   ├── public/
│   │   └── index.html         # HTML template
│   └── src/
│       ├── main.jsx           # React entry point
│       ├── App.jsx            # Main component
│       ├── App.css            # App styles
│       ├── index.css          # Global styles + dark mode
│       └── components/        # React components
│           ├── Header.jsx/.css       # Header + theme toggle
│           ├── SearchBar.jsx/.css    # Search and internal input
│           └── ContactsList.jsx/.css # Contact list with call buttons
│
├── 🐳 INFRASTRUCTURE
│   ├── docker-compose.yml     # Container orchestration (backend + frontend)
   └── .gitignore             # Git ignore rules

```

## 📖 Which File to Read?

| Situation | File to read |
|-----------|--------------|
| **I'm new to this project** | 📍 [QUICKSTART.md](QUICKSTART.md) |
| **I need to install on a new server** | 📍 [QUICKSTART.md](QUICKSTART.md) |
| **I need to configure PBX/contacts** | [CONFIG.md](CONFIG.md) |
| **I need to integrate the APIs** | [API.md](API.md) |
| **I need to deploy to production** | [DEPLOYMENT.md](DEPLOYMENT.md) |
| **I want a project overview** | [README.md](README.md) |

## 🚀 Essential Commands

```bash
# Installation
docker compose up -d --build

# Stop
docker compose down

# Logs
docker compose logs -f

# Restart
docker compose restart
```

## 🔧 Important Files to Edit

1. **`backend/.env`** - PBX Configuration
   ```env
   PBX_HOST=192.168.1.1
   PBX_PORT=5038
   PBX_USERNAME=admin
   PBX_PASSWORD=manager
   ```

2. **`backend/numeri.json`** - Contacts
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

3. **`frontend/src/App.jsx`** - API URL
   ```javascript
   const API_URL = 'http://192.168.1.1:8000'  // Edit here if needed
   ```

## 📊 High-Level Architecture

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

## ✅ Setup Checklist

- [ ] Docker installed
- [ ] Repository cloned
- [ ] `backend/.env` created
- [ ] `docker compose up -d --build` executed
- [ ] `http://localhost:3000` accessible
- [ ] `/api/status` shows "connected"
- [ ] Contacts visible in list
- [ ] Test call successful

## 🎯 Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md)
2. Install the project on your server
3. Configure FreePBX credentials
4. Customize contacts
5. Test a phone call

---

**Questions?** Consult the appropriate `.md` file above!
