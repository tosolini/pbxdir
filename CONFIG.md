# Configurazione

Guida di configurazione per Rubrica Telefonica.

## Environment Variables

### Backend

Crea `backend/.env`:

```env
PBX_HOST=10.0.0.2
PBX_PORT=5038
PBX_USER=click2dial
PBX_PASSWORD=admin
```

#### Variabili Disponibili

| Variable | Default | Descrizione |
|----------|---------|-------------|
| `PBX_HOST` | 10.0.0.2 | Indirizzo IP o hostname della PBX |
| `PBX_PORT` | 5038 | Porta Asterisk Manager |
| `PBX_USER` | click2dial | Username AMI |
| `PBX_PASSWORD` | admin | Password AMI |

### Frontend

URL backend configurato in `src/App.jsx`:

```javascript
const API_URL = 'http://10.0.110.2:8000'
```

Per modificare, edita il file e ricostruisci:

```bash
# Modifica
nano frontend/src/App.jsx

# Ricostruisci
docker compose down && docker compose up -d --build
```

---

## Contatti (numeri.json)

### Struttura

```json
[
  {
    "id": 0,
    "name": "Nome [Tipo]",
    "number": "3391234567",
    "office": "0212345678",
    "shortInternal": "201",
    "email": "user@company.com",
    "role": "Ruolo",
    "department": "Reparto"
  }
]
```

### Campi

| Campo | Tipo | Obbligatorio | Descrizione |
|-------|------|--------------|-------------|
| `id` | number | ✅ | ID univoco contatto |
| `name` | string | ✅ | Nome visualizzato (aggiungi tipo in []) |
| `number` | string | ✅ | Numero principale (cellulare) |
| `office` | string | ❌ | Numero ufficio |
| `shortInternal` | string | ❌ | Interno centralino |
| `email` | string | ❌ | Indirizzo email (cliccabile) |
| `role` | string | ❌ | Ruolo/Titolo |
| `department` | string | ❌ | Reparto |

### Esempi

**Contatto semplice (solo cellulare):**

```json
{
  "id": 5,
  "name": "Mario Rossi",
  "number": "3391234567",
  "email": "mario.rossi@company.com",
  "role": "Tecnico",
  "department": "IT"
}
```

**Contatto completo (multipli numeri):**

```json
{
  "id": 0,
  "name": "Elena Bianchi [Cellulare]",
  "number": "3391609864",
  "office": "043212345",
  "shortInternal": "201",
  "email": "elena@company.com",
  "role": "Direttore",
  "department": "Amministrazione"
}
```

**Contatto interno (solo interno):**

```json
{
  "id": 20,
  "name": "Supporto Tecnico [Interno]",
  "shortInternal": "999",
  "email": "support@company.com",
  "role": "Help Desk",
  "department": "IT"
}
```

### Aggiunta Contatti

1. Modifica `backend/numeri.json`
2. Aggiungi nuova voce nell'array
3. Ricarica il browser (no restart necessario)

```bash
# Modifica
nano backend/numeri.json

# Valida JSON
jq . backend/numeri.json

# Salva (Ctrl+X, Y, Enter in nano)
```

---

## FreePBX/Asterisk

### Configurazione Utente AMI

1. Accedi a FreePBX come admin
2. Vai a: **Admin → Settings → Asterisk Manager → Users**
3. Crea nuovo utente:
   - **Username**: click2dial
   - **Secret**: admin
   - **Read Permissions**: Attiva tutte
   - **Write Permissions**: originate

4. Salva e applica

### Configurazione Numero Esterno

Per ricevere chiamate esterne correttamente:

1. Vai a: **Admin → Connectivity → Trunk**
2. Configura il trunk con lo stesso numero esterno
3. Verifica in: **Admin → Settings → Advanced Settings → Outbound Caller ID**

### Verifica Manager

```bash
# Accedi al server Asterisk
ssh asterisk-server

# Connettiti a Asterisk CLI
asterisk -r

# Verifica manager status
manager list

# Verifica permessi utente
manager list connected

# Esci
exit
exit
```

---

## Docker Compose

### Configurazione di Rete

Per cambiare porta di accesso, modifica `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "3000:3000"    # Cambia a "8080:3000" per accesso su porta 8080

  backend:
    ports:
      - "8000:8000"    # Cambia a "8001:8000" per accesso su porta 8001
```

Poi riavvia:

```bash
docker compose down && docker compose up -d --build
```

### Variabili Ambiente nel Container

Per aggiungere variabili, modifica `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - PBX_HOST=10.0.0.2
      - PBX_PORT=5038
      - PBX_USER=click2dial
      - PBX_PASSWORD=admin
```

---

## Python Backend

### Dipendenze

File: `backend/requirements.txt`

```
FastAPI==0.104.1
Uvicorn==0.24.0
pyst2==0.5.1
python-dotenv==1.0.0
pydantic-settings==2.0.0
```

Per aggiungere dipendenze:

1. Edita `requirements.txt`
2. Aggiungi nuova linea
3. Ricostruisci: `docker compose up -d --build backend`

### Variabili Configurazione

File: `backend/config.py`

```python
class Settings(BaseSettings):
    PBX_HOST: str = "10.0.0.2"
    PBX_PORT: int = 5038
    PBX_USER: str = "click2dial"
    PBX_PASSWORD: str = "admin"
    
    class Config:
        env_file = ".env"
        extra = "ignore"
```

---

## Frontend React

### Environment

File: `frontend/src/App.jsx`

```javascript
const API_URL = 'http://10.0.110.2:8000'
```

Cambia per una nuova istanza.

### Configurazione Vite

File: `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,  // Port dev server
  }
})
```

---

## Temi

### Dark Mode

Abilitato tramite toggle UI. Salvato in localStorage con chiave `darkMode`.

Per forzare dark mode:

```javascript
// In App.jsx
const [darkMode, setDarkMode] = useState(() => true)  // Forza true
```

### Colori Tema Scuro

Definiti in `src/index.css`:

```css
body.dark-mode {
  background-color: #0f172a;
  color: #e2e8f0;
}
```

Modifica per personalizzare colori.

---

## Persistenza Locale

### localStorage

L'app salva in localStorage:

| Chiave | Valore | Descrizione |
|--------|--------|-------------|
| `userExtension` | string | Interno utente |
| `darkMode` | boolean | Tema preferito |

Per pulire (console browser):

```javascript
localStorage.removeItem('userExtension')
localStorage.removeItem('darkMode')
```

---

## Certificati SSL (Produzione)

Per HTTPS, genera certificati:

```bash
# Self-signed (sviluppo)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Let's Encrypt (produzione)
sudo certbot certonly --standalone -d rubrica.tuodominio.com
```

Poi configura reverse proxy (nginx/apache) con HTTPS.

---

## Logging

### Backend

Logs disponibili tramite Docker:

```bash
docker compose logs backend -f
```

Log level in `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR
```

### Frontend

Browser console (F12):

```javascript
// Add in App.jsx for debugging
console.log('Extension:', extension)
console.log('PBX Status:', pbxStatus)
```

---

## Sicurezza

### Credenziali

**MAI** committare `.env` in git:

```bash
echo "backend/.env" >> .gitignore
```

### Firewall

Apri solo porte necessarie:

```bash
sudo ufw allow 3000/tcp  # Frontend
sudo ufw allow 8000/tcp  # Backend (se accessibile esternamente)
```

### CORS

Restringi in produzione (`main.py`):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rubrica.tuodominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Troubleshooting

### PBX non si connette

1. Verifica `.env`:
   ```bash
   cat backend/.env
   ```

2. Verifica raggiungibilità:
   ```bash
   telnet 10.0.0.2 5038
   ```

3. Verifica credenziali in FreePBX

4. Leggi logs:
   ```bash
   docker compose logs backend
   ```

### Contatti non caricano

1. Valida JSON:
   ```bash
   jq . backend/numeri.json
   ```

2. Verifica API:
   ```bash
   curl http://localhost:8000/api/contacts
   ```

3. Controlla browser console (F12)

### Tema non persiste

Svuota localStorage:

```javascript
// Console browser
localStorage.clear()
location.reload()
```

---

## Reset Configurazione

Per resettare tutto ai defaults:

```bash
# Rimuovi container e volumi
docker compose down -v

# Ripristina .env di default
cp backend/.env.example backend/.env  # Se esiste

# Riavvia
docker compose up -d --build
```
