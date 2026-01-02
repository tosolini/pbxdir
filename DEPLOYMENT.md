# Deployment

Guida per distribuire Rubrica Telefonica in ambienti diversi.

## Ambienti Supportati

- ✅ Development locale
- ✅ Server interno (stesso network di FreePBX)
- ✅ Cloud (AWS, Azure, DigitalOcean)
- ✅ Docker Swarm
- ✅ Kubernetes

## Development

```bash
# Clone repository
git clone <repo> pbxdir && cd pbxdir

# Configura .env
cat > backend/.env << 'EOF'
PBX_HOST=192.168.1.1
PBX_PORT=5038
PBX_USER=admin
PBX_PASSWORD=manager
EOF

# Avvia
docker compose up -d --build

# Accedi
open http://localhost:3000
```

---

## Server Interno (LAN/Intranet)

Deployment su server fisico nella stessa rete della PBX.

### Prerequisiti

- Server Linux (Ubuntu 20.04+, CentOS 7+)
- Docker 20.10+
- Docker Compose 1.29+
- Connessione di rete con FreePBX

### Installazione

```bash
# 1. Installa Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# 2. Clona repository
git clone <repo> /opt/pbxdir
cd /opt/pbxdir

# 3. Configura
sudo nano backend/.env
# PBX_HOST=<ip-pbx>
# PBX_PORT=5038
# PBX_USER=admin
# PBX_PASSWORD=manager

# 4. Avvia (come root o con sudo)
sudo docker compose up -d --build

# 5. Verifica
sudo docker compose ps
curl http://localhost:8000/api/status
```

### Accesso Intranet

**URL**: `http://<server-ip>:3000`

Accedi da qualsiasi PC sulla LAN.

### Auto-Start al Riavvio

```bash
# Crea systemd service
sudo tee /etc/systemd/system/pbxdir.service > /dev/null << 'EOF'
[Unit]
Description=Rubrica Telefonica
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/pbxdir
ExecStart=/usr/bin/docker-compose up -d --build
ExecStop=/usr/bin/docker-compose down
User=root

[Install]
WantedBy=multi-user.target
EOF

# Abilita
sudo systemctl daemon-reload
sudo systemctl enable pbxdir.service
sudo systemctl start pbxdir.service

# Verifica
sudo systemctl status pbxdir.service
```

---

## Cloud (AWS, Azure, DigitalOcean)

### Creazione Istanza

#### AWS EC2

1. Avvia istanza Ubuntu 20.04
2. Security Group:
   - Inbound: port 22 (SSH), 3000 (HTTP), 8000 (API opzionale)
   - Outbound: All (per raggiungere PBX)

#### DigitalOcean Droplet

1. Seleziona Ubuntu 20.04
2. Size: Basic ($4-6/mese)
3. Network: In stessa VPC della PBX

#### Azure

1. VM Linux (Ubuntu 20.04)
2. Inbound Rules: port 22, 3000
3. Subnet: In rete della PBX o con VPN

### Installazione Cloud

```bash
# SSH nel server
ssh ubuntu@<public-ip>

# Installa Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
sudo apt install docker-compose -y

# Clone e configura
git clone <repo> ~/pbxdir
cd ~/pbxdir
nano backend/.env

# Avvia
docker compose up -d --build

# Abilita firewall
sudo ufw allow 22/tcp
sudo ufw allow 3000/tcp
sudo ufw enable
```

---

## HTTPS (Produzione)

### Con Reverse Proxy (Nginx)

```bash
# Installa Nginx
sudo apt install nginx certbot python3-certbot-nginx -y

# Configura dominio
sudo nano /etc/nginx/sites-available/rubrica

server {
    listen 80;
    server_name rubrica.tuodominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Abilita
sudo ln -s /etc/nginx/sites-available/rubrica /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Ottieni certificato SSL
sudo certbot --nginx -d rubrica.tuodominio.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### Configurazione API HTTPS

Modifica `frontend/src/App.jsx`:

```javascript
const API_URL = 'https://rubrica.tuodominio.com:8000'
```

O esponi API tramite stesso dominio:

```nginx
location /api/ {
    proxy_pass http://localhost:8000/api/;
}
```

---

## Load Balancing

Per alta disponibilità con multipli server:

### Docker Swarm

```bash
# Inizializza swarm
docker swarm init

# Deploy come service
docker stack deploy -c docker-compose.yml pbx

# Scala replicas
docker service scale pbx_backend=3
docker service scale pbx_frontend=3
```

### Kubernetes

Crea `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pbxdir-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pbxdir-backend
  template:
    metadata:
      labels:
        app: pbxdir-backend
    spec:
      containers:
      - name: backend
        image: pbxdir-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: PBX_HOST
          valueFrom:
            configMapKeyRef:
              name: pbx-config
              key: host

---
apiVersion: v1
kind: Service
metadata:
  name: pbxdir-backend-service
spec:
  type: LoadBalancer
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: pbxdir-backend
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
kubectl get services
```

---

## Database Esterno (Opzionale)

Per archiviare contatti in database:

### PostgreSQL

```bash
# Aggiungi a docker-compose.yml
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: pbxdir
      POSTGRES_USER: pbx
      POSTGRES_PASSWORD: <secure-password>
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```python
# backend/main.py - SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://pbx:password@postgres:5432/pbxdir"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@app.get("/api/contacts")
async def get_contacts():
    db = SessionLocal()
    contacts = db.query(Contact).all()
    db.close()
    return contacts
```

---

## Monitoraggio

### Prometheus + Grafana

```bash
# Aggiungi a docker-compose.yml
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

Accedi a Grafana su `http://localhost:3001`

### ELK Stack (Logging)

```bash
# Elasticsearch
docker run -d --name elasticsearch -p 9200:9200 docker.elastic.co/elasticsearch/elasticsearch:8.0.0

# Kibana
docker run -d --name kibana -p 5601:5601 docker.elastic.co/kibana/kibana:8.0.0

# Logstash (opzionale)
docker run -d --name logstash -p 5000:5000 docker.elastic.co/logstash/logstash:8.0.0
```

---

## Backup & Recovery

### Backup Contatti

```bash
# Daily backup
0 2 * * * cp /opt/pbxdir/backend/numeri.json /backup/numeri.json.$(date +\%Y\%m\%d)

# AWS S3 Backup
aws s3 cp /opt/pbxdir/backend/numeri.json s3://my-bucket/backups/
```

### Restore

```bash
cp /backup/numeri.json.<date> /opt/pbxdir/backend/numeri.json
docker compose restart backend
```

---

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker image
        run: |
          docker build -t pbxdir-backend ./backend
          docker build -t pbxdir-frontend ./frontend
          
      - name: Deploy to server
        run: |
          ssh -i ${{ secrets.SSH_KEY }} ubuntu@${{ secrets.SERVER_IP }} << 'EOF'
            cd /opt/pbxdir
            git pull
            docker compose up -d --build
          EOF
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - docker build -t pbxdir-backend ./backend
    - docker build -t pbxdir-frontend ./frontend

deploy:
  stage: deploy
  script:
    - ssh ubuntu@prod.server "cd /opt/pbxdir && git pull && docker compose up -d --build"
```

---

## Scaling Orizzontale

### Multipli Server con Load Balancer

```
                    ┌─────────────┐
                    │ Load Balancer
                    │ (Nginx/HAProxy)
                    └────────┬────┘
           ┌────────────────┼────────────────┐
           │                │                │
      ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
      │ Server 1 │      │ Server 2 │      │ Server 3 │
      │ PBXDir   │      │ PBXDir   │      │ PBXDir   │
      └──────────┘      └──────────┘      └──────────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                       ┌────▼────┐
                       │  FreePBX │
                       └──────────┘
```

Load Balancer config (Nginx):

```nginx
upstream pbxdir_backend {
    server server1.internal:8000;
    server server2.internal:8000;
    server server3.internal:8000;
}

server {
    listen 80;
    server_name rubrica.internal;
    
    location / {
        proxy_pass http://pbxdir_backend;
    }
}
```

---

## Troubleshooting Deployment

### Container non si avvia

```bash
# Verifica logs
docker compose logs

# Pulisci e ricostruisci
docker compose down -v
docker compose up -d --build

# Verifica immagini
docker images
```

### Connessione PBX fallisce

```bash
# Verifica connectivity
docker exec pbx-backend ping 192.168.1.1
docker exec pbx-backend telnet 192.168.1.1:5038

# Verifica DNS
docker exec pbx-backend nslookup pbx.internal
```

### Port already in use

```bash
# Verifica porte
sudo lsof -i :3000
sudo lsof -i :8000

# Uccidi processo
sudo kill -9 <PID>

# Cambia porta in docker-compose.yml
```

---

## Best Practices

1. ✅ **Usa immagini versionate** (non `latest`)
2. ✅ **Separare secrets dai file di configurazione**
3. ✅ **Usa health checks** nei container
4. ✅ **Monitora log e metriche**
5. ✅ **Backup regolari** dei dati
6. ✅ **HTTPS in produzione**
7. ✅ **Segregazione di rete** (DMZ per API)
8. ✅ **Rate limiting** su endpoint pubblici
9. ✅ **Autenticazione e autorizzazione**
10. ✅ **Disaster recovery plan**

---

## Support

Per problemi di deployment:

1. Controlla logs: `docker compose logs -f`
2. Verifica configurazione: `cat backend/.env`
3. Test API: `curl http://localhost:8000/api/status`
4. Test connessione PBX: `telnet <pbx-ip> 5038`
5. Leggi [CONFIG.md](CONFIG.md) per dettagli
