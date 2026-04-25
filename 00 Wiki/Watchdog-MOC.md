---
title: Watchdog
type: moc
tags: [watchdog, observability, signal-bot, systemd, safety]
created: 2026-04-25
updated: 2026-04-25
---

## Summary

**Watchdog** ist die Observability-Schicht des [[Signal-Bot-MOC|Signal-Bots]] — separater systemd-Service `signal-watchdog`, der alle 60s Bot+IBGateway+Kairos+Positionen prüft und kritische Alerts via Telegram pusht. Architektur-Trennung: **Bot=Execution, Watchdog=Observability, Kairos=Intelligence** — Watchdog hat KEINE DB-Writes, KEINE IBKR-Calls, liest nur. Observability-Triade (`.heartbeat` + `.position_heartbeat` + `.kairos_heartbeat`) seit 2026-04-24 vollständig. Stand 2026-04-25: nach Restart-Storm (06:39-06:41) 3 Bug-Fixes pending (timeout 30s→120s, Restart-Lock, restart_all.sh + signal-kairos).

## Aktueller Stand (2026-04-25)

- **Service:** `signal-watchdog.service` ACTIVE
- **Code:** `/root/signal_bot/watchdog.py`
- **Check-Interval:** 60s
- **Heartbeats:** main.py (`.heartbeat` 120s max-age) + position_monitor (`.position_heartbeat` 60s) + kairos (`.kairos_heartbeat` 600s)
- **Critical-Keywords:** `HARD-DD CRITICAL`, `GHOST POSITION`, `ORPHAN DB TRADE`, `Kairos-Service DOWN`, `Position-Monitor FAILED`
- **Pending-Fixes:** restart-timeout 30→120s, restart-lock, signal-kairos in restart_all.sh

## Komponenten

### Heartbeat-Triade

| File | Writer | Max-Age | Purpose |
|---|---|---|---|
| `.heartbeat` | `main.py` | 120s | Bot-Loop alive |
| `.position_heartbeat` | `position_monitor._check_all_positions()` | 60s | TSL/TP-Loop alive (5s-Cycle × 12 Grace) |
| `.kairos_heartbeat` | `kairos/daemon.py:_write_heartbeat_file()` | 600s | Kairos-Daemon alive (atomic via tmp+os.replace) |

### Check-Funktionen (run_checks)

| Check | Was |
|---|---|
| 1. Bot-Service | `systemctl is-active signal-bot` |
| 2. IBGateway | `systemctl is-active ibgateway` |
| 3. Bot-Heartbeat | `.heartbeat` mtime |
| 4. Position-Monitor-Heartbeat | `.position_heartbeat` mtime |
| 5. Kairos-Service | `is-active signal-kairos` (Guard: nur wenn Service existiert) |
| 6. Kairos-Heartbeat | `.kairos_heartbeat` mtime |
| 7. Daily-DD Circuit-Breaker | `SUM(realized_pnl)` heute, WARN 80%/CRITICAL 100% von `MAX_BANKROLL_USD × MAX_DAILY_LOSS_PERCENT` |
| 8. Ghost-Positions | `kairos_output/ghost_snapshot.json` read-only, alert auf GHOST+ORPHAN_DB |
| 9. Stuck-Pending-Orders | DB-Query auf pending > N min |
| 10. SL-Missing | DB-Query Positionen ohne SL |

### Was Watchdog NICHT tut (bewusst)

- **Keine IBKR-Calls** — Ghost-Detection nur über Snapshot-File (Kairos/Bot schreibt, Watchdog liest)
- **Keine DB-Writes** — read-only auf `trades.db`, `kairos_output/*`
- **Keine Auto-Closes** — SL-Missing nur Alert (Auto-Close würde Positionen wipen während Bot SL setzt)
- **Kein config.py-Import** — `.env` direkt lesen (vermeidet circular imports)

## Hardening-Historie

| Datum | Phase | Änderung |
|---|---|---|
| 2026-04-17 | DD Circuit-Breaker | `check_daily_drawdown()` WARN 80%/CRIT 100%, Heartbeat 300→120s |
| 2026-04-17 ~15:32 | Position-Monitor-Heartbeat | `.position_heartbeat` File + Check, schließt Silent-Freeze-Lücke |
| 2026-04-24 | Blueprint-Alignment | +Kairos-Service-Check + Kairos-Heartbeat + Ghost-Snapshot-Read |
| 2026-04-25 06:39-06:41 | Restart-Storm-RCA | 3 Bugs identifiziert (timeout/lock/restart_all.sh) |

## Restart-Storm 2026-04-25 (RCA)

**Was:** 6 Telegram-Alerts (FAILED→OK alternierend) zwischen 06:39 und 06:41 CEST.

**Race:** User-Restart kollidierte mit Watchdog-Auto-Restart, weil Bot-Shutdown ~90s dauert (Telethon-Disconnect) aber Watchdog-Restart-Timeout nur 30s.

**Bug-Liste (pending fixes):**

1. **`watchdog.py:561-562`** — `restart_bot()` subprocess-timeout=30s zu kurz. Fix: 120s ODER pre-check `systemctl is-failed signal-bot`.
2. **`watchdog.py:559` is_bot_running()-Race** — User-Stop sieht Watchdog innerhalb 60s als "down" und startet eigenen Restart parallel. Fix: User-Restart-Lock-File `/var/run/signal-bot.restart.lock` das `restart_all.sh` setzt + Watchdog respektiert.
3. **`scripts/restart_all.sh:13`** — `SERVICES=(signal-bot signal-watchdog)` — **Kairos fehlt**. Fix: `SERVICES=(signal-bot signal-watchdog signal-kairos)` ODER bewusste Trennung dokumentieren.
4. **Sekundär:** Ghost-Snapshot war 14h stale (16:01 24.04 → 06:41 25.04), Watchdog 4× alerted, kein Self-Heal. Snapshot-Writer im Bot-Prozess hat Exception verschluckt. Restart hat zufällig gefixt.

## Critical-Lessons

- **Monitor-Errors NIE ignorieren** (2026-04-24): `pos.unrealizedPNL` crashte Heartbeat 7h42m, SL/TP effektiv tot bis Watchdog-Alert. Jeder Loop-Error ist kritisch.
- **Snapshot-Freshness ≠ Detection-Korrektheit**: Stale-Alerts heißen Writer kaputt, nicht Detection.
- **`feedback_never_dismiss_monitor_errors.md`** REGEL: jeder Monitor-Error ist pre-Alert.

## Konfiguration (env)

```
MAX_BANKROLL_USD=10000
MAX_DAILY_LOSS_PERCENT=10  # → Limit $1000/Tag (User: bewusst hoch)
MAX_HEARTBEAT_AGE=120
MAX_POSITION_HEARTBEAT_AGE=60
MAX_KAIROS_HEARTBEAT_AGE=600
MAX_GHOST_SNAPSHOT_AGE=1800
```

## Bedienung

```bash
systemctl status signal-watchdog       # State prüfen
systemctl restart signal-watchdog      # Restart
journalctl -u signal-watchdog -f       # Live-Logs
bash scripts/restart_all.sh restart    # Atomic Bot+Watchdog (+Kairos pending)
```

## Memory-Detail-Files

- `/root/.claude/projects/-root-signal-bot/memory/project_watchdog_hardening_2026_04_17.md` — DD-Circuit-Breaker + Position-Monitor-Heartbeat
- `/root/.claude/projects/-root-signal-bot/memory/project_watchdog_blueprint_alignment_2026_04_24.md` — Kairos-Integration, Observability-Triade
- `/root/.claude/projects/-root-signal-bot/memory/project_watchdog_restart_storm_2026_04_25.md` — Restart-Storm RCA + 3 Bug-Fixes pending
- `/root/.claude/projects/-root-signal-bot/memory/feedback_never_dismiss_monitor_errors.md` — REGEL: Monitor-Errors nie ignorieren

## Related

- [[Signal-Bot-MOC]] — bewachter Service
- [[Kairos-MOC]] — bewachter Service (Kairos-Daemon)
- [[Hermes-Gateway]] — paralleler Service-Stack
- [[IBKR-Paper-Trading]] — Backend, indirekt überwacht (über ibgateway-systemd)
