---
tags: [ressource, openclaw, ollama]
status: pausiert
---

# OpenClaw → Ollama/Kimi K2.5 Migration

**Status:** Pausiert — wird später umgesetzt.

## Hintergrund

- VPS: Hostinger MK2, Linux, Docker Manager
- OpenClaw und Ollama laufen auf demselben Host
- Kimi K2.5 ist bereits in Ollama installiert (Ollama-Abo aktiv)
- **Problem:** Nach jedem Container-Neustart fällt OpenClaw auf NEXOS_API_KEY zurück
- **Ursache:** OLLAMA_API_KEY fehlt in der docker-compose.yml → nur die YAML ist persistent
- **Fix:** Beide Ollama-Variablen dauerhaft in die YAML eintragen

## Schritt 1: Ollama prüfen

```bash
curl -s http://127.0.0.1:11434/api/tags | grep kimi
```

Wenn `kimi-k2.5` erscheint → weiter. Sonst: `ollama pull kimi-k2.5:cloud`

## Schritt 2: Docker Compose YAML finden

```bash
find /docker /home /root -name "docker-compose.yml" 2>/dev/null
grep -l "openclaw" $(find /docker /home /root -name "docker-compose.yml" 2>/dev/null)
```

## Schritt 3: Umgebungsvariablen eintragen

Im `environment:`-Block des OpenClaw-Services hinzufügen:

```yaml
- OLLAMA_API_KEY=ollama-local
- OLLAMA_BASE_URL=http://127.0.0.1:11434
- OLLAMA_CONTEXT_LENGTH=64000
```

```bash
# Prüfen ob schon vorhanden:
grep -n "OLLAMA_API_KEY" /docker/<projektname>/docker-compose.yml

# Falls nicht, nach TELEGRAM_BOT_TOKEN einfügen:
sed -i '/TELEGRAM_BOT_TOKEN/a\      - OLLAMA_API_KEY=ollama-local\n      - OLLAMA_BASE_URL=http://127.0.0.1:11434\n      - OLLAMA_CONTEXT_LENGTH=64000' /docker/<projektname>/docker-compose.yml
```

## Schritt 4: Standardmodell setzen

```bash
docker exec $(docker ps --filter "name=openclaw" -q) \
  openclaw config set agents.defaults.model.primary "ollama/kimi-k2.5:cloud"
```

## Schritt 5: Container neu starten

```bash
cd $(find /docker -name "docker-compose.yml" -path "*openclaw*" | head -1 | xargs dirname)
docker compose down && docker compose up -d
sleep 5 && docker ps | grep openclaw
```

## Schritt 6: Verifizieren

```bash
docker exec $(docker ps --filter "name=openclaw" -q) openclaw models list

curl -s http://127.0.0.1:11434/api/chat \
  -d '{"model":"kimi-k2.5:cloud","messages":[{"role":"user","content":"Sag Hallo"}],"stream":false}' \
  | grep -o '"content":"[^"]*"'
```

---

## OpenClaw Absicherung (Cloudflare Tunnel)

Siehe [[OpenClaw Security Setup]]
