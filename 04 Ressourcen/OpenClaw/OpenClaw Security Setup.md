---
tags: [ressource, openclaw, security]
status: pausiert
---

# OpenClaw Security Setup (Cloudflare Tunnel)

**Status:** Pausiert — wird später umgesetzt.

## Ziel

OpenClaw absichern: Port nur auf localhost binden, Zugang nur über Cloudflare Tunnel, Docker-Sandbox, dmPolicy allowlist.

## Schritt 1: OpenClaw Installation finden

```bash
find /docker /opt /home -name "docker-compose.yml" 2>/dev/null | head -20
docker ps -a | grep -i openclaw
```

## Schritt 2: docker-compose.yml patchen

**Port auf localhost binden:**
```yaml
# Von:
ports:
  - "${PORT}:${PORT}"
# Zu:
ports:
  - "127.0.0.1:${PORT}:${PORT}"
```

**Docker Socket mounten (für Sandbox):**
```yaml
volumes:
  - openclaw_config:/home/node/.openclaw
  - openclaw_workspace:/home/node/openclaw
  - /var/run/docker.sock:/var/run/docker.sock
  - /home/linuxbrew/.linuxbrew:/home/linuxbrew/.linuxbrew
```

## Schritt 2.5: .env prüfen (KRITISCH)

```bash
grep GATEWAY_BIND /path/to/openclaw/.env
# Muss sein: OPENCLAW_GATEWAY_BIND=lan
# Falls fehlt: echo "OPENCLAW_GATEWAY_BIND=lan" >> .env
```

Ohne `lan` → 502-Fehler im Tunnel.

## Schritt 3: openclaw.json Security-Settings

```json
{
  "discovery": { "mdns": { "mode": "off" } },
  "logging": { "redactSensitive": "tools" },
  "channels": {
    "telegram": { "dmPolicy": "allowlist" }
  },
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "rw",
        "docker": { "network": "bridge" }
      }
    }
  },
  "tools": { "elevated": { "enabled": false } }
}
```

**WICHTIG:** `dmPolicy` nur für WhatsApp und Telegram — nicht Discord/Slack.

## Schritt 4: Cloudflare Tunnel installieren

```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o /tmp/cloudflared.deb
sudo dpkg -i /tmp/cloudflared.deb
sudo cloudflared service install ${TUNNEL_TOKEN}
sudo systemctl status cloudflared
```

## Schritt 4.5: Homebrew für Skills

```bash
apt-get install -y build-essential procps curl file git
useradd -m -s /bin/bash linuxbrew
sudo -u linuxbrew NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
chmod -R g+w /home/linuxbrew/.linuxbrew/
```

## Häufige Fehler

| Problem | Ursache | Fix |
|---|---|---|
| 502 Tunnel-Fehler | `OPENCLAW_GATEWAY_BIND` fehlt in .env | `echo "OPENCLAW_GATEWAY_BIND=lan" >> .env` |
| Dashboard fordert Pairing | Onboarding als root ausgeführt | `chown -R 1000:1000 /var/lib/docker/volumes/*_openclaw_config/_data/` |
| brew: command not found | Homebrew nicht gemountet | Volume-Mount in docker-compose.yml prüfen |
