---
tags: [signal-bot, automation, claude-daily, planned]
date: 2026-04-11
status: planned
depends-on: Parser Rebuild Phase A abgeschlossen + Phase B Review durchgeführt
---

# Claude Daily Reports — Automatisierte Opus-Analysen per Telegram

Drei Cron-gesteuerte Claude-Opus-Läufe die den Signal Bot täglich/wöchentlich beobachten und Reports an einen separaten Telegram-Bot schicken.

## Ziel

Dominic soll ohne Terminal sehen können:
- **Morgens vor Pre-Market**: Ist der Bot gesund? Kann er heute traden?
- **Nachts nach AH-Close**: Was ist heute passiert? Gab es Anomalien? Wie war die Delta zu Jacks echtem PnL?
- **Sonntags**: Was waren Muster dieser Woche? Was sollten wir anpassen?

Alle Reports über einen **separaten Bot** damit Signal Bot Alerts und Reports nicht im selben Chat-Thread kollidieren.

## Telegram-Channel

- **Bot Name:** Jacks analyse
- **Username:** @Jacksanalyse_bot
- **Bot ID:** 8781045760
- **Chat ID:** 781400898 (Dominic / Leo Löwenherz, gleicher Account wie `NOTIFY_CHAT_ID`)
- **Token:** liegt nur in `.env` (wird beim Build eingefügt, NIE in den Vault)
- **Smoke Test:** ✅ 2026-04-11, Delivery bestätigt

## Die drei Jobs

### 1. Morning Health Check — 09:30 CEST (Mo–Fr)
**Zweck:** ~15 Min vor US-Pre-Market. Alle Vor-Prüfungen bevor der Handelstag startet.

**Checks:**
- Systemd-Status: `signal-bot`, `signal-watchdog`, `ibgateway`
- `.heartbeat`-Alter (< 5 Min)
- IBKR-Verbindungstest via `ib_insync`: Account-Balance, offene Positionen aus IBKR, Drift-Abgleich zu `trades.db`
- `get_last_price("SPY")` — Pipeline-Test
- Stuck pending orders > 24h?
- Disk/RAM-Check auf VPS
- API-Budget vom Vortag
- **Parser Dry-Run** (kein echtes Probe-Signal): `parse_message("$TSLA entry 250")` → sauberer `ParsedSignal`?

**Output:** Kurzer Status-Report an @Jacksanalyse_bot. Grün bei OK, 🚨 + Details bei Fehler.

**Blockiert Evening Review bei kritischem Fehler.**

### 2. Evening Opus Review — 02:30 CEST (Di–Sa, nach AH-Close 02:00)
**Zweck:** Tiefe Analyse des abgeschlossenen Handelstags.

**Input-Daten (deterministisch gesammelt):**
- Alle heute geschlossenen Trades (Entry, Exit, PnL, Dauer, Slippage)
- Alle empfangenen Signale (geparst, ignoriert, Fehler)
- Bot-Errors/Warnings aus Log
- Signal-Latenz (Post→Order)
- SL/TP-Trigger-Verhalten
- Jacks eigene PnL-Aussagen (aus seinen Nachrichten) → Vergleich zu Bot-PnL

**Opus-Prompt:** "Du bist Trading-Analyst. Gegeben X,Y,Z — bewerte den Tag. Was lief gut, was schlecht, wo war die Delta zu Jack, welche Anomalien? Sei konkret, keine Floskeln."

**Output:**
- Kurze Telegram-Zusammenfassung (Ampel + 5–6 Zeilen Kern + Deep-Link)
- Volle Analyse als `/root/obsidian_vault/05 Daily Notes/Evening Reviews/YYYY-MM-DD.md`
- Obsidian Mobile Deep-Link in der Telegram-Nachricht

### 3. Weekend Deep Dive — Sonntag 18:00 CEST
**Zweck:** Wöchentliche Muster-Erkennung, Parameter-Drift-Check.

- Aggregation der 5–7 Evening Reviews der Woche
- PnL-Trend, Win-Rate, avg Hold-Time, Channel-Breakdown (wenn >1 aktiv)
- Parser-Qualität: wie viele `needs_review` wurden in der Woche generiert?
- Risk-Check: Drawdown, Kill-Switch-Trigger, Anomalien-Häufung
- **Empfehlungen** am Ende: was sollte diese Woche angepasst werden?

## Implementierungs-Plan (5 Schritte)

### Schritt 1 — Max-Plan-Check ✅ DONE
`claude -p "..."` läuft aus Shell ohne `ANTHROPIC_API_KEY`, nutzt `~/.claude/.credentials.json` (Max-Login), antwortet sauber.
**Konsequenz:** Alle drei Jobs laufen gegen Max-Kontingent, keine API-Abrechnung → faktisch 0€ zusätzlich solange im Usage-Limit.

### Schritt 2 — Separater Notifier
- Datei: `/root/signal_bot/scripts/daily_notifier.py`
- Dünner Telegram-Wrapper mit `TELEGRAM_DAILY_BOT_TOKEN` + `TELEGRAM_DAILY_CHAT_ID` aus neuer `.env`-Sektion
- Funktion: `send_daily_report(text, level="info"|"warn"|"critical")`

### Schritt 3 — `scripts/claude_daily.py` mit 3 Subcommands
```bash
python3 scripts/claude_daily.py morning
python3 scripts/claude_daily.py evening
python3 scripts/claude_daily.py weekly
```
- Jedes Subcommand: sammelt Daten deterministisch → `claude -p` mit kuratiertem Kontext → formatiert → `daily_notifier.send_daily_report()`
- **Cost-Cap pro Run** (Hard-Abort bei Überschreitung, nicht praktisch nötig im Max-Plan aber Safety-Net)
- **Morning-Lock**: Morning schreibt `/tmp/claude_daily_morning_ok` bei Erfolg; Evening liest das — bei Fehler flagged Evening explizit "Morning Check hatte Fehler X, Analyse ist potenziell unvollständig"

### Schritt 4 — systemd-Timer (nicht Cron)
- `signal-daily-morning.timer` → 09:30 Mo–Fr
- `signal-daily-evening.timer` → 02:30 Di–Sa
- `signal-daily-weekly.timer` → So 18:00
- Units in `/etc/systemd/system/`
- **Warum systemd statt Cron**: Logging via `journalctl`, Retry-Handling, Reboot-Überlebend, sauberes Error-Forwarding
- **`analyzer.py` Daily Digest 23:30 wird deaktiviert** um Dopplung zu vermeiden

### Schritt 5 — Test-Harness + Go-Live
- `python3 scripts/claude_daily.py morning --test` → dry-run, Nachricht kommt bei Dominic an
- Akzeptanz-Test: alle 3 Subcommands manuell einmal durchlaufen, Output prüfen
- Erst dann Timer scharfstellen

## Offene Entscheidungen (abgehakt vor Build)

- [x] **Opus für alles** (nicht Sonnet-Mix) — Dominic-Entscheidung 2026-04-11
- [x] **Max-Plan verifiziert** — Kosten faktisch 0€
- [x] **Separater Bot** — @Jacksanalyse_bot (frischer @BotFather Bot)
- [x] **Probe-Signal** = Parser-Dry-Run, nicht Listener-Injection
- [x] **Daily Digest 23:30 ersetzen**, nicht parallel laufen lassen
- [ ] Wann wird gebaut? → **NACH** Parser Rebuild Phase B abgeschlossen

## Abhängigkeiten

- **Warten auf:** [[Parser Rebuild — Stress Test Phase A]] → Phase B → Phase C → Phase D
- **Grund für Wartezeit:** Aktuell laufen Backtests die API-Budget + Context verbrauchen. Parallel ein neues Claude-calling-System zu bauen wäre chaotisch. Außerdem soll der ersetzte `analyzer.py` erst nach Bot-Restart mit neuem Parser aktiviert werden.

## Verwandte Notizen

- [[Signal Bot Live-Roadmap]] — Phase 2 (Paper-Profitabilität messen) profitiert direkt von den Daily Reports
- [[Signal Bot]] — Hauptprojekt-Notiz
- [[Parser Rebuild — Stress Test Phase A]] — aktuelle Blocker-Arbeit
