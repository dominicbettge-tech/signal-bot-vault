---
tags: [inbox, ops, autonomy, housekeeper]
date: 2026-04-25
---

# Autonomy-Setup 2026-04-25

Auto-Memory + wöchentlicher Knowledge-Housekeeper-Cron eingerichtet, voll autonom durch alle 3 Phasen, alle Constraints eingehalten (Bot/Kairos nicht angefasst, existing Crontab nur additiv erweitert).

## Was gemacht wurde

### Phase 1 — Auto-Memory
- **Backup:** `/root/.claude/settings.json.bak.2026-04-25` (2585 Bytes)
- **Befund:** `autoMemoryEnabled` war BEREITS auf `true` gesetzt (Zeile 92 der bestehenden settings.json). jq-Set lief idempotent, alle 8 Top-Level-Keys erhalten (`autoCompactWindow`, `autoMemoryEnabled`, `effortLevel`, `enabledPlugins`, `env`, `hooks`, `permissions`, `skipDangerousModePermissionPrompt`).
- **Verify:** `jq '.autoMemoryEnabled' /root/.claude/settings.json` → `true` ✓
- **Auto-Dream (v2.1.83+):** NICHT automatisch aktiviert (Plan-Vorgabe). Manuell togglebar via `/memory` in einer Session.

### Phase 2 — Housekeeper-Cron
- **Crontab-Backup:** `/root/crontab.bak.2026-04-25` (23 Lines)
- **Wrapper-Script:** `/root/scripts/run_housekeeper.sh` (executable, 362 Bytes)
- **Cron-Eintrag (additiv):** `0 18 * * 0 /root/scripts/run_housekeeper.sh` — Sonntag 18:00 Europe/Berlin
- **Diff vs Backup:** nur 3 neue Lines am Ende (Leerzeile + Comment + Cron), keine bestehende Zeile geändert
- **Existing Crons unverändert:** OpenClaw memory-backup (*/30), watchdog (*/10), status_writer (*/5), Signal-Bot Analyzer (Daily 21:30 + Weekly So 17:00), check_api_and_resume (*/30), obsidian_github_sync (23:00), Wochenendprojekt-Reminder (Sa 07:00), Testcenter Phase B (23:15), Codex queue-loop (*/2h), tsl_monitor_cron (23:30), shadow_replay (23:45), paper_gate_monitor (23:40), kairos_daily_report (22:30) — alle 22 originalen Einträge intakt.

### Phase 2e — Trockentest
- Manueller Lauf: `/root/scripts/run_housekeeper.sh`
- **Laufzeit:** 12:30:24 → 12:34:06 = 3min 42s
- **Exit:** 0
- **Output:** `/root/obsidian_vault/01 Inbox/housekeeper_2026-04-25.md` (442 Bytes, 5 Lines, sinnvoller Inhalt: 346 Files geprüft, 0 stale Pins, 0 Dangling, MEMORY.md 188/200, 3 echte Vorschläge)
- **Bonus:** Skill hat zusätzlich `housekeeping_proposals_2026-04-25.md` erstellt (7752 Bytes, ausführliche Vorschlagsliste)
- **Log:** `/root/scripts/housekeeper_runs.log` zeigt sauber `starting` + `done, exit=0`
- **Errors:** keine

## Wo liegen Backups

| Backup | Pfad | Bytes |
|---|---|---|
| settings.json | `/root/.claude/settings.json.bak.2026-04-25` | 2585 |
| crontab | `/root/crontab.bak.2026-04-25` | 2715 (23 Lines) |

## Rollback-Befehle

**Auto-Memory deaktivieren (jq-Inplace):**
```bash
jq '.autoMemoryEnabled = false' /root/.claude/settings.json > /tmp/s.tmp && mv /tmp/s.tmp /root/.claude/settings.json
```
Oder Backup zurück:
```bash
cp /root/.claude/settings.json.bak.2026-04-25 /root/.claude/settings.json
```

**Cron-Eintrag entfernen:**
```bash
crontab /root/crontab.bak.2026-04-25
```

**Wrapper-Script entfernen:**
```bash
rm /root/scripts/run_housekeeper.sh
# Optional: Log und /root/scripts auch wegräumen
rm -f /root/scripts/housekeeper_runs.log
rmdir /root/scripts  # nur falls leer
```

**Output-Files aufräumen (optional):**
```bash
rm "/root/obsidian_vault/01 Inbox/housekeeper_2026-04-25.md"
rm "/root/obsidian_vault/01 Inbox/housekeeping_proposals_2026-04-25.md"
```

## Was der User prüfen soll

- **Sonntag 26.04.2026 ~18:05 CET:** prüfen ob `/root/scripts/housekeeper_runs.log` einen neuen Lauf-Block zeigt (`starting` + `done`).
- **Montag 27.04.2026 morgens:** prüfen ob `/root/obsidian_vault/01 Inbox/housekeeper_2026-04-26.md` existiert mit sinnvollem Inhalt.
- Falls Lauf fehlschlägt: Log-File `/root/scripts/housekeeper_runs.log` zeigt stderr-Zeilen vom claude-Call.
- **Auto-Memory:** ab dieser Session sollten neue Memory-Files automatisch ohne explizite Bestätigung geschrieben werden (vorher schon aktiv gewesen, daher kein Verhaltens-Sprung erwartet).

## Constraints — Status

| # | Constraint | Status |
|---|---|---|
| 1 | Bot + kairos.daemon nicht stoppen/restartn | ✓ Beide PIDs (1378055/1378062) unangetastet, Kairos-Heartbeat 12:24 frisch |
| 2 | Existing Crontab nur additiv | ✓ Diff zeigt nur 3 neue Lines am Ende |
| 3 | Backup vor jeder Änderung | ✓ settings.json + crontab gesichert |
| 4 | Bei Unklarheit STOP | ✓ einzige Auffälligkeit (autoMemoryEnabled war schon true) im Report dokumentiert |
| 5 | IS_SANDBOX=1 für headless claude | ✓ im Wrapper-Script gesetzt |
| 6 | cd /root/signal_bot vor claude-Call | ✓ im Wrapper-Script gesetzt |

## Final Deliverables (alle vorhanden)

1. ✓ `/root/.claude/settings.json` (autoMemoryEnabled: true)
2. ✓ `/root/.claude/settings.json.bak.2026-04-25`
3. ✓ `/root/scripts/run_housekeeper.sh` (executable)
4. ✓ `/root/scripts/housekeeper_runs.log` (mit Trockentest-Eintrag)
5. ✓ `/root/crontab.bak.2026-04-25`
6. ✓ Aktualisierte crontab mit Sonntag-18:00-Eintrag (`crontab -l | grep run_housekeeper` zeigt Eintrag)
7. ✓ `/root/obsidian_vault/01 Inbox/housekeeper_2026-04-25.md` (Trockentest-Output)
8. ✓ Dieser Report
