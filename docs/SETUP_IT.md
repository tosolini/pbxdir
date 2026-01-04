# 🔧 Setup Iniziale dopo Clone

Dopo aver clonato il repository, segui questi passi:

## 1. Copia File di Esempio

```bash
# Copia configurazione backend
cp backend/.env.example backend/.env

# Copia database contatti
cp numeri.json.example numeri.json
```

## 2. Configura Credenziali FreePBX

Modifica `backend/.env`:

```bash
nano backend/.env
```

Inserisci i tuoi valori:

```env
PBX_HOST=<ip-del-tuo-freepbx>
PBX_PORT=5038
PBX_USERNAME=<username-ami>
PBX_PASSWORD=<password-ami>
```

## 3. Configura Contatti

Modifica `numeri.json`:

```bash
nano numeri.json
```

Aggiungi i tuoi contatti seguendo l'esempio in `numeri.json.example`.

## 4. Avvia l'Applicazione

```bash
docker compose up -d --build
```

## 5. Verifica Funzionamento

```bash
# Controlla container
docker compose ps

# Controlla log
docker compose logs -f

# Test API
curl http://localhost:8000/api/health
curl http://localhost:8000/api/contacts
```

## 6. Accedi all'Interfaccia

Apri il browser su: **http://localhost:3000**

---

## ⚠️ File da NON Committare

Questi file contengono dati sensibili e sono già nel `.gitignore`:

- `backend/.env` - Credenziali FreePBX
- `numeri.json` - Contatti con email e numeri personali

Usa sempre i file `.example` come template!

---

## 🔐 Sicurezza

Per produzione:

1. Usa password robuste per AMI
2. Limita accesso AMI in FreePBX
3. Configura firewall per porta 5038
4. Abilita HTTPS (vedi [DEPLOYMENT.md](DEPLOYMENT.md))
5. Usa secret management (non .env in plain text)

---

Vedi [QUICKSTART.md](QUICKSTART.md) per guida completa.
