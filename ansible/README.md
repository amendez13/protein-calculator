# Ansible deployment

This folder contains playbooks/roles to deploy `protein-calculator` to a Linux VPS (Debian/Ubuntu).

## Prerequisites

- Ansible 2.14+ on your local machine
- SSH access to your VPS (key-based recommended)
- A Debian/Ubuntu VPS with `sudo` access

## Quick start

1. Create an inventory file from the example:

```bash
cp ansible/inventory.example.ini ansible/inventory.ini
```

2. Edit `ansible/inventory.ini` with your VPS host/user/key.

3. Deploy:

```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml
```

## Variables

You can set variables in your inventory (recommended) or pass `-e key=value`.

Common variables:

- `protein_calculator_repo_url` (default: `https://github.com/amendez13/protein-calculator.git`)
- `protein_calculator_repo_version` (default: `main`)
- `protein_calculator_app_dir` (default: `/opt/protein-calculator`)
- `protein_calculator_state_dir` (default: `/var/lib/protein-calculator`)
- `protein_calculator_database_url` (default: `sqlite+aiosqlite:////var/lib/protein-calculator/protein.db`)
- `protein_calculator_bind_host` (default: `127.0.0.1`)
- `protein_calculator_bind_port` (default: `8000`)
- `protein_calculator_debug` (default: `false`)
- `protein_calculator_enable_nginx` (default: `false`)
- `protein_calculator_nginx_server_name` (default: `_`)

Example (inventory):

```ini
[protein_calculator:vars]
protein_calculator_repo_version=main
protein_calculator_enable_nginx=true
protein_calculator_nginx_server_name=example.com
protein_calculator_bind_host=127.0.0.1
protein_calculator_bind_port=8000
```

## What it does

- Clones/updates the repo in `protein_calculator_app_dir`
- Creates a virtualenv in `protein_calculator_app_dir/venv` and installs `requirements.txt`
- Writes `/etc/protein-calculator.env` for runtime configuration
- Installs a systemd service `protein-calculator` and starts/enables it
- Optionally installs nginx and proxies HTTP to the app

## Notes

- TLS is intentionally not automated here. If you need HTTPS, add certificates and extend the nginx config.
- If the repo is private, you must provide credentials for the `git` checkout (e.g., deploy key/SSH URL).
