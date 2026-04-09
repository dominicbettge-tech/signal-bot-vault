# Taranis AI

> OSINT-Tool mit AI-Unterstützung für News-Aggregation und Situationsanalyse.

## Links
- GitHub: https://github.com/taranis-ai/taranis-ai
- Docs: https://taranis.ai/docs/

## Installation (2026-04-09)

Installiert auf VPS Hostinger MK2 (187.124.166.210) via:
```bash
curl -fsSL https://taranis.ai/install.sh | bash
```

**Problem:** Installer lief aus `/root/signal_bot/` → hat das Signal Bot `.env` überschrieben.  
**Fix:** Signal Bot `.env` aus `.env.bak.1775760768` wiederhergestellt. Taranis-Dateien nach `/root/taranis/` verschoben.

## Konfiguration

| Datei | Pfad |
|---|---|
| compose.yml | `/root/taranis/compose.yml` |
| .env | `/root/taranis/.env` |

**Port:** 8090 (statt Default 8080 — belegt durch Signal Bot Dashboard)

## Zugang

- URL: http://187.124.166.210:8090
- Admin: `admin` / `admin` ← **ändern!**

## Services (Docker)

| Container | Aufgabe |
|---|---|
| taranis-ingress-1 | Nginx Reverse Proxy (Port 8090) |
| taranis-frontend-1 | Flask/HTMX UI |
| taranis-core-1 | Backend/REST API |
| taranis-workers-1 | Celery Worker |
| taranis-collector-1 | News-Quellen Collector |
| taranis-nlp_bot-1 | NLP-Analyse Bot |
| taranis-summary_bot-1 | Zusammenfassungs-Bot |
| taranis-story_bot-1 | Story-Aggregations-Bot |
| taranis-database-1 | PostgreSQL |
| taranis-rabbitmq-1 | Message Broker |

## Verwaltung

```bash
# Status
docker ps --filter "name=taranis"

# Starten / Stoppen
cd /root/taranis && docker compose up -d
cd /root/taranis && docker compose down

# Logs
docker logs taranis-core-1 -f
```

## Passwort ändern

In `/root/taranis/.env`:
```
PRE_SEED_PASSWORD_ADMIN=neues_passwort
```
Dann: `docker compose down && docker compose up -d`  
(nur beim ersten Start wirksam — bei bestehender DB via UI ändern)

## Nächste Schritte

- [ ] Default Sources laden: http://187.124.166.210:8090/config/sources → "load default sources"
- [ ] Admin-Passwort ändern
- [ ] Use Case klären: für Signal Bot Kontext nutzen?
