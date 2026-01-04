# Configuration

Configuration guide for Phone Directory.

## Environment Variables

### Backend

Create `backend/.env`:

```env
PBX_HOST=192.168.1.1
PBX_PORT=5038
PBX_USERNAME=admin
PBX_PASSWORD=manager
```

#### Available Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PBX_HOST` | 192.168.1.1 | PBX IP address or hostname |
| `PBX_PORT` | 5038 | Asterisk Manager port |
| `PBX_USERNAME` | admin | AMI username |
| `PBX_PASSWORD` | manager | AMI password |

### Frontend

Backend URL configured in `src/App.jsx`:

```javascript
const API_URL = 'http://192.168.1.1:8000'
```

To modify, edit the file and rebuild:

```bash
# Edit
nano frontend/src/App.jsx

# Rebuild
docker compose down && docker compose up -d --build
```

---

## Contacts (numeri.json)

### Structure

```json
[
  {
    "id": 0,
    "name": "Name [Type]",
    "number": "3351234567",
    "office": "021345678",
    "shortInternal": "101",
    "email": "user@company.com",
    "role": "Role",
    "department": "Department"
  }
]
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | number | ✅ | Unique contact ID |
| `name` | string | ✅ | Display name (add type in []) |
| `number` | string | ✅ | Main number (mobile) |
| `office` | string | ❌ | Office number |
| `shortInternal` | string | ❌ | Switchboard extension |
| `email` | string | ❌ | Email address (clickable) |
| `role` | string | ❌ | Role/Title |
| `department` | string | ❌ | Department |

### Examples

**Simple contact (mobile only):**

```json
{
  "id": 5,
  "name": "John Smith",
  "number": "33351234567",
  "email": "john.smith@company.com",
  "role": "Technician",
  "department": "IT"
}
```

**Complete contact (multiple numbers):**

```json
{
  "id": 0,
  "name": "Jane Doe [Mobile]",
  "number": "33512345679",
  "office": "0431234455677",
  "shortInternal": "201",
  "email": "jane@company.com",
  "role": "Director",
  "department": "Administration"
}
```

**Internal contact (extension only):**

```json
{
  "id": 20,
  "name": "Technical Support [Internal]",
  "shortInternal": "999",
  "email": "support@company.com",
  "role": "Help Desk",
  "department": "IT"
}
```

### Adding Contacts

1. Edit `backend/numeri.json`
2. Add new entry to the array
3. Reload browser (no restart needed)

```bash
# Edit
nano backend/numeri.json

# Validate JSON
jq . backend/numeri.json

# Save (Ctrl+X, Y, Enter in nano)
```

---

## FreePBX/Asterisk

### AMI User Configuration

1. Log in to FreePBX as admin
2. Go to: **Admin → Settings → Asterisk Manager → Users**
3. Create new user:
   - **Username**: admin
   - **Secret**: manager
   - **Read Permissions**: Enable all
   - **Write Permissions**: originate

4. Save and apply

### External Number Configuration

To receive external calls correctly:

1. Go to: **Admin → Connectivity → Trunk**
2. Configure trunk with the same external number
3. Verify in: **Admin → Settings → Advanced Settings → Outbound Caller ID**

### Verify Manager

```bash
# Access Asterisk server
ssh asterisk-server

# Connect to Asterisk CLI
asterisk -r

# Verify manager status
manager list

# Verify user permissions
manager list connected

# Exit
exit
exit
```

---

## Docker Compose

### Network Configuration

To change access port, modify `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "3000:3000"    # Change to "8080:3000" for access on port 8080

  backend:
    ports:
      - "8000:8000"    # Change to "8001:8000" for access on port 8001
```

Then restart:

```bash
docker compose down && docker compose up -d --build
```

### Environment Variables in Container

To add variables, modify `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - PBX_HOST=192.168.1.1
      - PBX_PORT=5038
      - PBX_USERNAME=admin
      - PBX_PASSWORD=manager
```

---

## Python Backend

### Dependencies

File: `backend/requirements.txt`

```
FastAPI==0.104.1
Uvicorn==0.24.0
pyst2==0.5.1
python-dotenv==1.0.0
pydantic-settings==2.0.0
```

To add dependencies:

1. Edit `requirements.txt`
2. Add new line
3. Rebuild: `docker compose up -d --build backend`

### Configuration Variables

File: `backend/config.py`

```python
class Settings(BaseSettings):
    PBX_HOST: str = "192.168.1.1"
    PBX_PORT: int = 5038
    PBX_USERNAME: str = "admin"
    PBX_PASSWORD: str = "manager"
    
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

Change for a new instance.

### Vite Configuration

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

## Themes

### Dark Mode

Enabled via UI toggle. Saved in localStorage with key `darkMode`.

To force dark mode:

```javascript
// In App.jsx
const [darkMode, setDarkMode] = useState(() => true)  // Force true
```

### Dark Theme Colors

Defined in `src/index.css`:

```css
body.dark-mode {
  background-color: #0f172a;
  color: #e2e8f0;
}
```

Modify to customize colors.

---

## Local Persistence

### localStorage

The app saves in localStorage:

| Key | Value | Description |
|-----|-------|-------------|
| `userExtension` | string | User extension |
| `darkMode` | boolean | Preferred theme |

To clear (browser console):

```javascript
localStorage.removeItem('userExtension')
localStorage.removeItem('darkMode')
```

---

## SSL Certificates (Production)

For HTTPS, generate certificates:

```bash
# Self-signed (development)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Let's Encrypt (production)
sudo certbot certonly --standalone -d directory.yourdomain.com
```

Then configure reverse proxy (nginx/apache) with HTTPS.

---

## Logging

### Backend

Logs available via Docker:

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

## Security

### Credentials

**NEVER** commit `.env` to git:

```bash
echo "backend/.env" >> .gitignore
```

### Firewall

Open only necessary ports:

```bash
sudo ufw allow 3000/tcp  # Frontend
sudo ufw allow 8000/tcp  # Backend (if externally accessible)
```

### CORS

Restrict in production (`main.py`):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://directory.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Troubleshooting

### PBX won't connect

1. Verify `.env`:
   ```bash
   cat backend/.env
   ```

2. Verify reachability:
   ```bash
   telnet 192.168.1.1 5038
   ```

3. Verify credentials in FreePBX

4. Read logs:
   ```bash
   docker compose logs backend
   ```

### Contacts not loading

1. Validate JSON:
   ```bash
   jq . backend/numeri.json
   ```

2. Verify API:
   ```bash
   curl http://localhost:8000/api/contacts
   ```

3. Check browser console (F12)

### Theme doesn't persist

Clear localStorage:

```javascript
// Browser console
localStorage.clear()
location.reload()
```

---

## Reset Configuration

To reset everything to defaults:

```bash
# Remove container and volumes
docker compose down -v

# Restore default .env
cp backend/.env.example backend/.env  # If exists

# Restart
docker compose up -d --build
```
