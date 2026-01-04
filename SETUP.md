# 🔧 Initial Setup After Clone

After cloning the repository, follow these steps:

## 1. Copy Example Files

```bash
# Copy backend configuration
cp backend/.env.example backend/.env

# Copy contacts database
cp numeri.json.example numeri.json
```

## 2. Configure FreePBX Credentials

Edit `backend/.env`:

```bash
nano backend/.env
```

Insert your values:

```env
PBX_HOST=<your-freepbx-ip>
PBX_PORT=5038
PBX_USERNAME=<ami-username>
PBX_PASSWORD=<ami-password>
```

## 3. Configure Contacts

Edit `numeri.json`:

```bash
nano numeri.json
```

Add your contacts following the example in `numeri.json.example`.

## 4. Start the Application

```bash
docker compose up -d --build
```

## 5. Verify Functionality

```bash
# Check containers
docker compose ps

# Check logs
docker compose logs -f

# Test API
curl http://localhost:8000/api/health
curl http://localhost:8000/api/contacts
```

## 6. Access the Interface

Open your browser at: **http://localhost:3000**

---

## ⚠️ Files NOT to Commit

These files contain sensitive data and are already in `.gitignore`:

- `backend/.env` - FreePBX credentials
- `numeri.json` - Contacts with emails and personal numbers

Always use the `.example` files as templates!

---

## 🔐 Security

For production:

1. Use strong passwords for AMI
2. Limit AMI access in FreePBX
3. Configure firewall for port 5038
4. Enable HTTPS (see [DEPLOYMENT.md](DEPLOYMENT.md))
5. Use secret management (not .env in plain text)

---

See [QUICKSTART.md](QUICKSTART.md) for complete guide.
