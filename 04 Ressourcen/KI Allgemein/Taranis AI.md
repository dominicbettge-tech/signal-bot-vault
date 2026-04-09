# Taranis AI

> OSINT-Tool mit AI-Unterstützung für News-Aggregation und Situationsanalyse.

## Links
- GitHub: https://github.com/taranis-ai/taranis-ai
- Docs: https://taranis.ai/docs/

## Status: PAUSIERT (2026-04-09)

Images gelöscht, Dateien unter `/root/taranis/` noch vorhanden. Neustart erst nach Klärung der Ressourcenfrage.

## Problem: Nicht nutzbar auf aktuellem Server

**VPS:** Hostinger MK2 — 7.8 GB RAM, kein Swap

Die drei AI-Bots benötigen zusammen ~40 GB Disk und schätzungsweise 6-10 GB RAM im Betrieb:

| Bot | Image-Größe | RAM (ca.) |
|---|---|---|
| `taranis-natural-language-processing` | 15.4 GB | 2-4 GB |
| `taranis-summarize-bot` | 13.4 GB | 2-4 GB |
| `taranis-story-clustering` | 12.8 GB | 2-3 GB |

Beim ersten Start (alle Container gleichzeitig) brach der Server zusammen: Load Average stieg auf **68**, Terminal nicht mehr bedienbar.

Taranis **ohne** AI-Bots (nur Core + Frontend + Collector) wäre technisch möglich (~500 MB RAM), aber dann fehlt der Hauptnutzen.

## Optionen

- [ ] **Option A:** Server-Upgrade auf 16 GB RAM (Hostinger ~$15-20/month mehr)
- [ ] **Option B:** Taranis ohne AI-Bots betreiben — nur als News-RSS-Aggregator für den Binance Bot
- [ ] **Option C:** Taranis auf separatem Server oder Cloud-Instanz

## Installation (2026-04-09)

Installiert via:
```bash
curl -fsSL https://taranis.ai/install.sh | bash
```

**Problem beim Install:** Installer lief aus `/root/signal_bot/` → hat das Signal Bot `.env` überschrieben.
**Fix:** Signal Bot `.env` aus `.env.bak.1775760768` wiederhergestellt. Taranis-Dateien nach `/root/taranis/` verschoben.

**Port:** 8090 (statt Default 8080 — belegt durch Signal Bot Dashboard)

## Dateien

| Datei | Pfad |
|---|---|
| compose.yml | `/root/taranis/compose.yml` |
| .env | `/root/taranis/.env` |

## Zugang (wenn aktiv)

- URL: http://187.124.166.210:8090
- Admin: `admin` / `admin` ← **ändern!**

## Verwaltung

```bash
# Starten
cd /root/taranis && docker compose up -d

# Stoppen
cd /root/taranis && docker compose down

# Status
docker ps --filter "name=taranis"

# Logs
docker logs taranis-core-1 -f
```

## Nächste Schritte (offen)

- [ ] Entscheidung: Option A, B oder C?
- [ ] Use Case klären: für Binance Bot News-Layer nutzen?
- [ ] Admin-Passwort ändern (nach Neuinstall via UI)
