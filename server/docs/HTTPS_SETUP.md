# HTTPS setup (default install)

AISignX installs in **`https` deploy mode** by default. The Python app listens on **`http://127.0.0.1:5000`** (no TLS). **Caddy** terminates HTTPS on port **443** and obtains certificates automatically.

This gives browser-based displays a **secure context**, so the service worker can cache media for **offline playback**. Plain `http://` in a normal browser cannot do that (the Electron client is the exception on LAN HTTP).

---

## Quick setup after install

From the `server/` directory:

**Linux / macOS**

```bash
chmod +x scripts/setup_https.sh
./scripts/setup_https.sh --hostname signage.example.com
# or for local dev:
./scripts/setup_https.sh --hostname localhost

sudo caddy run --config deploy/Caddyfile
```

**Windows (run PowerShell as Administrator for port 443)**

```powershell
.\scripts\setup_https.ps1 -Hostname signage.example.com
caddy run --config deploy\Caddyfile
```

Start AISignX bound to localhost (install scripts use HTTPS config; run the app as usual):

```bash
# Linux — production-style
waitress-serve --host=127.0.0.1 --port=5000 app:app

# Dev
python app.py
```

Open the admin UI at **`https://YOUR_HOSTNAME/`** (not `:5000`).

---

## Certificate types

| Hostname | Certificate | Trusted in browsers? |
|----------|-------------|----------------------|
| Public domain (`signage.example.com`) | **Let's Encrypt** (free, auto via Caddy) | Yes |
| `localhost` | Caddy **internal** TLS | After one-time warning |
| LAN IP (`192.168.x.x`) | Caddy **internal** TLS | After one-time warning |

### Let's Encrypt requirements

- A **public DNS name** pointing to your server (A or AAAA record).
- Ports **80** and **443** reachable from the internet (for ACME HTTP challenge).
- Optional: set `AISIGNX_EMAIL=you@example.com` when running `setup_https.sh` for ACME account notices.

### LAN-only signage

Use a **real domain** with DNS → your public IP (or DuckDNS/no-ip) and port-forward 80/443, **or** use internal TLS and accept the browser warning once per display, **or** use the **Electron** or **Android** client on HTTP (they do not rely on the service worker).

---

## Production (Linux systemd)

```bash
sudo ./scripts/setup_https.sh --hostname signage.example.com --email admin@example.com --system
sudo systemctl enable --now caddy
```

Run AISignX under systemd or supervisor on `127.0.0.1:5000` only — do not expose port 5000 on the firewall.

---

## Config

Generated `config.py` uses:

```python
AISIGNX_DEPLOY_MODE = 'https'
```

Regenerate:

```bash
python generate_config.py --mode https --hostname signage.example.com --force
python generate_config.py --show
```

**HTTP is not supported** for clients or new installs. The Flask app may listen on `http://127.0.0.1:5000` locally behind Caddy only — do not point displays at port 5000.

---

## Client URLs

| Component | URL |
|-----------|-----|
| Admin / browser displays | `https://your-hostname/` |
| Electron / Android setup | `https://your-hostname` (no `:5000`) |
| Internal app (not for clients) | `http://127.0.0.1:5000` |

Downloaded setup files and enrollment JSON always use **https://**.

---

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Certificate fails | DNS, firewall 80/443, hostname matches `deploy/Caddyfile` |
| `connection refused` on 443 | Caddy running? `sudo caddy validate --config deploy/Caddyfile` |
| Login loops / wrong links | `AISIGNX_DEPLOY_MODE=https`, Caddy sends `X-Forwarded-Proto` (Caddy does by default) |
| Offline still fails in browser | Page must be `https://`, service worker registered (no red cache banner on display page) |

See also [SERVER_HTTP_ONLY_or_HTTPS_ONLY_Version2.md](SERVER_HTTP_ONLY_or_HTTPS_ONLY_Version2.md) and [DEPLOY_LINUX.md](DEPLOY_LINUX.md).
