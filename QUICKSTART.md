# Quick Start - Phone Directory

Quick guide to install and run Phone Directory on a new server.

## 📋 Prerequisites

- **Docker**: version 20.10+
- **Docker Compose**: version 1.29+
- **FreePBX/Asterisk access**: with AMI enabled
- **Network**: access to PBX on port 5038

## 🚀 Installation (5 minutes)

### 1. Clone or copy the repository

```bash
# If you have git access
git clone <repository-url> pbxdir
cd pbxdir

# Or copy files manually
cd /path/to/pbxdir
```

### 2. Configure FreePBX connection

Create or modify `backend/.env`:

```bash
cat > backend/.env << 'EOF'
PBX_HOST=192.168.1.1
PBX_PORT=5038
PBX_USERNAME=admin
PBX_PASSWORD=manager
EOF
```

**Replace values with your FreePBX data:**
- `PBX_HOST`: IP or hostname of the PBX
- `PBX_PORT`: AMI port (default 5038)
- `PBX_USERNAME`: AMI user configured in FreePBX
- `PBX_PASSWORD`: AMI user password

### 3. Configure contacts

Modify `backend/numeri.json` with your contacts:

```json
[
  {
    "id": 0,
    "name": "John Smith [Mobile]",
    "number": "3391234567",
    "office": "0212345678",
    "shortInternal": "201",
    "email": "john.smith@company.com",
    "role": "Director",
    "department": "Management"
  }
]
```

**Fields**:
- `id`: Unique number
- `name`: Contact name (add type in brackets)
- `number`: Mobile/main number
- `office`: Office number (optional)
- `shortInternal`: Switchboard extension (optional)
- `email`: Email (clickable)
- `role`: Role/Title
- `department`: Department

### 4. Start the containers

```bash
# From inside the pbxdir directory
docker compose up -d --build

# Verify they are running
docker compose ps
```

You should see:
```
NAME                   STATUS
pbx-backend           Up
pbx-frontend          Up
```

### 5. Verify the installation

```bash
# Test backend
curl http://localhost:8000/api/health
# Should respond: {"status":"ok"}

# Test contacts
curl http://localhost:8000/api/contacts | jq . | head -20

# Test PBX connection
curl http://localhost:8000/api/status
# Should show AMI status (connected/disconnected)
```

### 6. Access the interface

Open your browser:
```
http://localhost:3000
```

## 🔧 Advanced Configuration

### Change IP/Port Access

Modify `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "8080:3000"  # Access at http://localhost:8080

  backend:
    ports:
      - "8001:8000"  # Access at http://localhost:8001
```

Then restart:
```bash
docker compose down && docker compose up -d --build
```

### Custom Network

If the PBX is on a different network, modify docker-compose.yml:

```yaml
services:
  backend:
    networks:
      - pbx_network

networks:
  pbx_network:
    driver: bridge
```

### Use your own domain

Modify `frontend/src/App.jsx`:

```javascript
const API_URL = 'http://yourdomain.com:8000'  // or https
```

Then rebuild:
```bash
docker compose down && docker compose up -d --build
```

## 🔐 Security in Production

### HTTPS for Frontend

Use a reverse proxy (nginx/apache):

```nginx
server {
  listen 443 ssl;
  server_name directory.yourdomain.com;
  
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;
  
  location / {
    proxy_pass http://localhost:3000;
  }
}
```

### HTTPS for Backend

Add certificates to docker-compose.yml if necessary.

### Firewall

Open only necessary ports:

```bash
# Frontend (access from LAN/VPN)
sudo ufw allow from 192.168.1.0/24 to any port 3000

# Backend (access only from frontend container, don't expose)
# Stay on Docker internal network
```

### Secure Credentials

Don't commit `.env` to git:

```bash
echo "backend/.env" >> .gitignore
```

Use secret management for production (Docker secrets, Vault, etc).

## 📊 Monitoring

### Read the logs

```bash
# All services
docker compose logs

# Backend only
docker compose logs backend -f

# Frontend only
docker compose logs frontend -f

# Last 20 lines
docker compose logs --tail 20
```

### Check PBX status

```bash
# PBX connection
curl http://localhost:8000/api/status

# Contacts loaded
curl http://localhost:8000/api/contacts | jq '. | length'
```

## 🆘 Troubleshooting

### Containers won't start

```bash
# See errors
docker compose logs

# Force rebuild
docker compose down
docker compose up -d --build

# Clean unused images
docker system prune -a
```

### PBX connection fails

1. Verify `backend/.env`:
   ```bash
   cat backend/.env
   ```

2. Verify PBX reachability:
   ```bash
   telnet 192.168.1.1 5038
   ```

3. Verify credentials in FreePBX:
   - Go to: Admin → Settings → Asterisk Manager → Users

4. Enable AMI if disabled:
   - Config file: `/etc/asterisk/manager.conf`
   - Restart Asterisk: `asterisk -r` → `core restart now`

### API not reachable

```bash
# Verify running containers
docker compose ps

# Verify port
netstat -tuln | grep 8000

# If needed, restart
docker compose restart backend
```

### Frontend won't load contacts

1. Verify API URL in `src/App.jsx`
2. Check CORS in backend
3. Verify `numeri.json` exists in `backend/`
4. Read logs: `docker compose logs backend`

## 🔄 Updates

### Update contacts

1. Modify `backend/numeri.json`
2. No restart necessary, changes are reloaded
3. Reload browser to see new contacts

### Update PBX configuration

1. Modify `backend/.env`
2. Restart backend:
   ```bash
   docker compose restart backend
   ```

### Update code

```bash
# Pull latest changes
git pull origin main

# Rebuild
docker compose down && docker compose up -d --build
```

## 📦 Backup

### Save contacts

```bash
cp backend/numeri.json backup/numeri.json.$(date +%Y%m%d)
```

### Save configuration

```bash
cp backend/.env backup/.env.$(date +%Y%m%d)
```

## 🛑 Stop/Start

### Stop containers

```bash
docker compose down
```

### Start containers

```bash
docker compose up -d
```

### Restart containers

```bash
docker compose restart
```

## 📚 Useful Commands

```bash
# Detailed status
docker compose ps -a

# Real-time logs
docker compose logs -f

# Execute command in container
docker compose exec backend python -c "..."

# Access container shell
docker compose exec backend /bin/bash

# Rebuild single service
docker compose up -d --build backend
```

## 🎓 Next Steps

1. **Test a call**: Configure an extension, select a contact and click "Call"
2. **Customize theme**: Use the light/dark mode toggle
3. **Add contacts**: Modify `numeri.json` and reload browser
4. **Enable HTTPS**: Configure reverse proxy for security

## 📞 Asterisk/FreePBX Requirements

Basic checks on FreePBX server:

```bash
# SSH to FreePBX server

# Verify Asterisk is running
systemctl status asterisk

# Verify manager.conf
cat /etc/asterisk/manager.conf | grep -A 5 "admin"

# Restart Asterisk if needed
asterisk -r
core restart now
exit
```

## ✅ Final Checklist

- [ ] Docker and Docker Compose installed
- [ ] Repository cloned/copied
- [ ] `.env` configured with correct PBX
- [ ] `numeri.json` populated with contacts
- [ ] `docker compose up -d` executed successfully
- [ ] http://localhost:3000 is accessible
- [ ] `/api/status` shows "connected"
- [ ] Contacts visible in list
- [ ] Test a call successfully
- [ ] Light/dark theme works
- [ ] Clickable emails work

## 🚀 You're ready!

You are now ready to use Phone Directory. Consult [README.md](README.md) for complete documentation.

Enjoy! 📞
