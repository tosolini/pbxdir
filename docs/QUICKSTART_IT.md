# Quick Start - Rubrica Telefonica

Guida rapida per installare e eseguire la Rubrica Telefonica su un nuovo server.

## 📋 Prerequisiti

- **Docker**: versione 20.10+
- **Docker Compose**: versione 1.29+
- **Accesso FreePBX/Asterisk**: con AMI abilitato
- **Rete**: accesso alla PBX sulla porta 5038

## 🚀 Installazione (5 minuti)

### 1. Clona o copia il repository

```bash
# Se hai accesso git
git clone <repository-url> pbxdir
cd pbxdir

# Oppure copia i file manualmente
cd /path/to/pbxdir
```

### 2. Configura la connessione FreePBX

Crea o modifica `backend/.env`:

```bash
cat > backend/.env << 'EOF'
PBX_HOST=192.168.1.1
PBX_PORT=5038
PBX_USERNAME=admin
PBX_PASSWORD=manager
EOF
```

**Sostituisci i valori con i dati del tuo FreePBX:**
- `PBX_HOST`: IP o hostname della PBX
- `PBX_PORT`: Porta AMI (default 5038)
- `PBX_USERNAME`: Utente AMI configurato in FreePBX
- `PBX_PASSWORD`: Password utente AMI

### 3. Configura i contatti

Modifica `backend/numeri.json` con i tuoi contatti:

```json
[
  {
    "id": 0,
    "name": "Mario Rossi [Cellulare]",
    "number": "3391234567",
    "office": "0212345678",
    "shortInternal": "201",
    "email": "mario.rossi@company.com",
    "role": "Direttore",
    "department": "Direzione"
  }
]
```

**Campi**:
- `id`: Numero univoco
- `name`: Nome contatto (aggiungi tipo tra parentesi)
- `number`: Numero cellulare/principale
- `office`: Numero ufficio (opzionale)
- `shortInternal`: Interno centralino (opzionale)
- `email`: Email (cliccabile)
- `role`: Ruolo/Titolo
- `department`: Reparto

### 4. Avvia i container

```bash
# Da dentro la directory pbxdir
docker compose up -d --build

# Verifica che siano avviati
docker compose ps
```

Dovresti vedere:
```
NAME                   STATUS
pbx-backend           Up
pbx-frontend          Up
```

### 5. Verifica l'installazione

```bash
# Test backend
curl http://localhost:8000/api/health
# Dovrebbe rispondere: {"status":"ok"}

# Test contatti
curl http://localhost:8000/api/contacts | jq . | head -20

# Test connessione PBX
curl http://localhost:8000/api/status
# Dovrebbe mostrare lo stato AMI (connected/disconnected)
```

### 6. Accedi all'interfaccia

Apri il browser:
```
http://localhost:3000
```

## 🔧 Configurazione Avanzata

### Cambia IP/Porta Accesso

Modifica `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "8080:3000"  # Accesso su http://localhost:8080

  backend:
    ports:
      - "8001:8000"  # Accesso su http://localhost:8001
```

Poi riavvia:
```bash
docker compose down && docker compose up -d --build
```

### Rete Personalizzata

Se la PBX è su una rete diversa, modifica docker-compose.yml:

```yaml
services:
  backend:
    networks:
      - pbx_network

networks:
  pbx_network:
    driver: bridge
```

### Usa il tuo dominio

Modifica `frontend/src/App.jsx`:

```javascript
const API_URL = 'http://tuodominio.com:8000'  // o https
```

Poi ricostruisci:
```bash
docker compose down && docker compose up -d --build
```

## 🔐 Sicurezza in Produzione

### HTTPS per Frontend

Usa un reverse proxy (nginx/apache):

```nginx
server {
  listen 443 ssl;
  server_name rubrica.tuodominio.com;
  
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;
  
  location / {
    proxy_pass http://localhost:3000;
  }
}
```

### HTTPS per Backend

Aggiungi certificati a docker-compose.yml se necessario.

### Firewall

Apri solo le porte necessarie:

```bash
# Frontend (accesso da LAN/VPN)
sudo ufw allow from 192.168.1.0/24 to any port 3000

# Backend (accesso solo da frontend container, non esporre)
# Rimani sulla rete Docker interna
```

### Credenziali Sicure

Non committare `.env` in git:

```bash
echo "backend/.env" >> .gitignore
```

Usa secret management per produzione (Docker secrets, Vault, etc).

## 📊 Monitoring

### Leggi i log

```bash
# Tutti i servizi
docker compose logs

# Solo backend
docker compose logs backend -f

# Solo frontend
docker compose logs frontend -f

# Ultime 20 righe
docker compose logs --tail 20
```

### Verifica lo stato PBX

```bash
# Connessione PBX
curl http://localhost:8000/api/status

# Contatti caricati
curl http://localhost:8000/api/contacts | jq '. | length'
```

## 🆘 Troubleshooting

### Container non si avviano

```bash
# Vedi errori
docker compose logs

# Ricostruisci forzatamente
docker compose down
docker compose up -d --build

# Pulisci immagini non utilizzate
docker system prune -a
```

### Connessione PBX fallisce

1. Verifica `backend/.env`:
   ```bash
   cat backend/.env
   ```

2. Verifica raggiungibilità PBX:
   ```bash
   telnet 192.168.1.1 5038
   ```

3. Verifica credenziali in FreePBX:
   - Vedi: Admin → Settings → Asterisk Manager → Users

4. Abilita AMI se disabilitato:
   - Config file: `/etc/asterisk/manager.conf`
   - Riavvia Asterisk: `asterisk -r` → `core restart now`

### API non raggiungibile

```bash
# Verifica container in esecuzione
docker compose ps

# Verifica porta
netstat -tuln | grep 8000

# Se necessario, riavvia
docker compose restart backend
```

### Frontend non carica contatti

1. Verifica URL API in `src/App.jsx`
2. Controlla CORS in backend
3. Verifica `numeri.json` esiste in `backend/`
4. Leggi log: `docker compose logs backend`

## 🔄 Aggiornamenti

### Aggiorna contatti

1. Modifica `backend/numeri.json`
2. Non è necessario riavviare, i cambiamenti sono ricaricati
3. Ricarica il browser per vedere i nuovi contatti

### Aggiorna configurazione PBX

1. Modifica `backend/.env`
2. Riavvia backend:
   ```bash
   docker compose restart backend
   ```

### Aggiorna codice

```bash
# Pull ultimi cambiamenti
git pull origin main

# Ricostruisci
docker compose down && docker compose up -d --build
```

## 📦 Backup

### Salva i contatti

```bash
cp backend/numeri.json backup/numeri.json.$(date +%Y%m%d)
```

### Salva la configurazione

```bash
cp backend/.env backup/.env.$(date +%Y%m%d)
```

## 🛑 Arresto/Avvio

### Arresta i container

```bash
docker compose down
```

### Avvia i container

```bash
docker compose up -d
```

### Riavvia i container

```bash
docker compose restart
```

## 📚 Comandi Utili

```bash
# Status dettagliato
docker compose ps -a

# Logs in tempo reale
docker compose logs -f

# Esegui comando nel container
docker compose exec backend python -c "..."

# Accedi shell container
docker compose exec backend /bin/bash

# Ricostruisci singolo servizio
docker compose up -d --build backend
```

## 🎓 Prossimi Passi

1. **Test una chiamata**: Configura un interno, seleziona un contatto e clicca "Chiama"
2. **Personalizza tema**: Usa il toggle light/dark mode
3. **Aggiungi contatti**: Modifica `numeri.json` e ricarica browser
4. **Abilita HTTPS**: Configura reverse proxy per sicurezza

## 📞 Requisiti Asterisk/FreePBX

Verifiche di base sul server FreePBX:

```bash
# Accedi al server FreePBX via SSH

# Verifica Asterisk in esecuzione
systemctl status asterisk

# Verifica manager.conf
cat /etc/asterisk/manager.conf | grep -A 5 "admin"

# Riavvia Asterisk se necessario
asterisk -r
core restart now
exit
```

## ✅ Checklist Finale

- [ ] Docker e Docker Compose installati
- [ ] Repository clonato/copiato
- [ ] `.env` configurato con PBX corretta
- [ ] `numeri.json` popolato con contatti
- [ ] `docker compose up -d` eseguito con successo
- [ ] http://localhost:3000 raggiungibile
- [ ] `/api/status` mostra "connected"
- [ ] Contatti visibili nella lista
- [ ] Test una chiamata con successo
- [ ] Tema light/dark funziona
- [ ] Email cliccabili funzionano

## 🚀 Sei pronto!

Sei ora pronto a usare Rubrica Telefonica. Consulta [README.md](README.md) per documentazione completa.

Buon utilizzo! 📞
