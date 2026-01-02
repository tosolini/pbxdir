# API Reference

Documentazione completa degli endpoint REST disponibili.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

```http
GET /api/health
```

Verifica che il server è in esecuzione.

**Response:**
```json
{
  "status": "ok"
}
```

---

### Stato PBX

```http
GET /api/status
```

Verifica lo stato della connessione Asterisk Manager Interface (AMI).

**Response (Connesso):**
```json
{
  "status": "connected",
  "pbx_host": "192.168.1.1",
  "pbx_port": 5038
}
```

**Response (Disconnesso):**
```json
{
  "status": "disconnected",
  "pbx_host": "192.168.1.1",
  "pbx_port": 5038,
  "error": "Connection refused"
}
```

---

### Lista Contatti

```http
GET /api/contacts
```

Recupera la lista completa di contatti da `numeri.json`.

**Response:**
```json
[
  {
    "id": 0,
    "name": "Tizio [Cellulare]",
    "number": "333111111",
    "office": "043212345",
    "shortInternal": "",
    "email": "tizio.admin@company.com",
    "role": "Ufficio Amministrazione",
    "department": "Admin"
  },
  {
    "id": 1,
    "name": "Caio [Centralino]",
    "number": "021234567",
    "shortInternal": "201",
    "email": "caio.admin@company.com",
    "role": "Ufficio Amministrazione",
    "department": "Admin"
  }
]
```

**Query Parameters:**
- Nessuno

---

### Originate Call

```http
POST /api/call
```

Invia una richiesta di chiamata a Asterisk Manager Interface.

**Request Body:**
```json
{
  "number": "335123456",
  "extension": "233"
}
```

**Parameters:**
- `number` (string, required): Numero da chiamare
- `extension` (string, required): Interno del chiamante

**Response (Successo):**
```json
{
  "status": "success",
  "message": "Call originated successfully",
  "details": {
    "response": "Success",
    "message": "Originate successfully queued",
    "actionid": "admin1234567890"
  }
}
```

**Response (Errore):**
```json
{
  "status": "error",
  "detail": "Extension not configured in PBX"
}
```

**Codici HTTP:**
- `200`: Chiamata inviata con successo
- `400`: Parametri mancanti o non validi
- `503`: PBX non raggiungibile

---

## Esempi cURL

### Verifica Health

```bash
curl -X GET http://localhost:8000/api/health
```

### Verifica Stato PBX

```bash
curl -X GET http://localhost:8000/api/status
```

### Lista Contatti

```bash
curl -X GET http://localhost:8000/api/contacts | jq .
```

### Origina Chiamata

```bash
curl -X POST http://localhost:8000/api/call \
  -H "Content-Type: application/json" \
  -d '{
    "number": "335123456",
    "extension": "233"
  }'
```

---

## Documentazione Interattiva

Accedi a FastAPI Swagger UI:

```
http://localhost:8000/docs
```

Qui puoi testare direttamente gli endpoint.

---

## Error Handling

### Errori Comuni

| Errore | Causa | Soluzione |
|--------|-------|-----------|
| `Connection refused` | PBX non raggiungibile | Verifica indirizzo IP e porta |
| `Authentication failed` | Credenziali AMI errate | Verifica `.env` |
| `Extension not found` | Interno non configurato | Verifica interno in FreePBX |
| `Channel not available` | Formato canale errato | Usa `SIP/` o `PJSIP/` |

---

## Rate Limiting

Non è implementato rate limiting. In produzione considera di aggiungere:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/call")
@limiter.limit("10/minute")
async def originate_call(request: Request, call_data: CallData):
    ...
```

---

## CORS

CORS è abilitato per tutte le origini in development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Per produzione, restringi:

```python
allow_origins=[
    "https://rubrica.tuodominio.com",
    "http://localhost:3000"
],
```

---

## Versioning

API version: `v1`

Futuri cambiamenti potranno introdurre:
- `/api/v2/...` per backward compatibility

---

## Timeout

- Timeout connessione PBX: 10 secondi
- Timeout request HTTP: 30 secondi

Modificabili in `pbx_manager.py` se necessario.

---

## Autenticazione

Attualmente nessuna autenticazione è implementata. Per produzione aggiungi:

- JWT tokens
- API keys
- OAuth2

Esempio JWT:

```python
from fastapi_jwt_auth import AuthJWT

@app.post("/api/call")
async def originate_call(Authorize: AuthJWT = Depends(), ...):
    Authorize.jwt_required()
    ...
```
