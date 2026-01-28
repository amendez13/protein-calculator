# Deployment Guide

This is a minimal guide for deploying `protein-calculator` on a Linux VPS. It assumes a single-node setup with a SQLite database file.

## Requirements

- Linux VPS (Ubuntu/Debian are common)
- Python 3.10+
- A reverse proxy (optional but recommended)

## Install and Run (Ansible)

This repo includes Ansible playbooks under `ansible/`.

Quick start:

```bash
cp ansible/inventory.example.ini ansible/inventory.ini
ansible-playbook -i ansible/inventory.ini ansible/site.yml
```

To enable nginx, set `protein_calculator_enable_nginx=true` in your inventory (and configure `protein_calculator_nginx_server_name`).

## Install and Run (manual)

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv git

git clone https://github.com/amendez13/protein-calculator.git
cd protein-calculator

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export PROTEIN_DATABASE_URL="sqlite+aiosqlite:////var/lib/protein-calculator/protein.db"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## systemd Service

1. Create a directory for the DB:
```bash
sudo mkdir -p /var/lib/protein-calculator
sudo chown -R $USER:$USER /var/lib/protein-calculator
```

2. Create an env file (example):
```bash
sudo tee /etc/protein-calculator.env >/dev/null <<'EOF'
PROTEIN_DATABASE_URL=sqlite+aiosqlite:////var/lib/protein-calculator/protein.db
PROTEIN_DEBUG=false
EOF
```

3. Create a systemd unit:
```bash
sudo tee /etc/systemd/system/protein-calculator.service >/dev/null <<'EOF'
[Unit]
Description=Protein Calculator (FastAPI)
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/protein-calculator
EnvironmentFile=/etc/protein-calculator.env
ExecStart=/opt/protein-calculator/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
```

4. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now protein-calculator
sudo systemctl status protein-calculator
```

## Reverse Proxy (nginx)

Example server block (HTTP only; add TLS separately):

```nginx
server {
  listen 80;
  server_name example.com;

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

## Tailscale (optional)

If you prefer private access:
- Install Tailscale on the VPS and your client device.
- Bind uvicorn to `127.0.0.1` and access the service through the VPS’s Tailscale IP.

## Backups

SQLite is a single file. Back up the path you configured in `PROTEIN_DATABASE_URL` (e.g. `/var/lib/protein-calculator/protein.db`).
