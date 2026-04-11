---
tags: [signal-bot, parser, backtest, in-progress]
date: 2026-04-11
---

# Parser Rebuild — Step 9 Phase A (Stress Test)

> **Status:** Full Run läuft im Background · gestartet 14:30 UTC · PID 2808960
> **Log:** `/root/signal_bot/logs/backtest_phase_a.log`
> **DB:** `/root/signal_bot/data/backtest_results.db` (Table: `results`)
> **Skript:** `/root/signal_bot/scripts/backtest_phase_a.py`

## Smoke Test — ✅ DONE

- 50 Messages in 71s, Kosten **$0.24**, 0 Errors
- Stages: 22 blocker · 21 haiku · 1 sonnet · 6 opus
- 6 echte Entries sauber durch Opus: GWH, ELBM×2, OCGN, SLS, GNPX
- 1 Review-Flag (haiku_ambiguous) — normal, kein Bug

## Full Run — ✅ DONE (15:44 UTC)

- **2664 Messages** in **74 Min** · **$12.41** · **0 Errors**
- Stages: 783 blocker (29%) · 1503 haiku (56%) · 84 sonnet (3%) · 294 opus (11%)
- **273 echte Entries** durch Opus validiert (Verdict APPROVE/CORRECT)
- **47 Review-Flags** (1.8%)

### Top Review-Gründe
| Reason | Count | Bedeutung |
|---|---|---|
| `opus_reject_after_sonnet_entry` | 27 | Sonnet sagte Entry, Opus kippte → Phase B muss prüfen wer recht hat |
| `haiku_ambiguous` | 12 | Unklare Klassifikation |
| `disagree_old=entry_new=watchlist` | 2 | Alter Parser sagte Entry, neuer Watchlist |
| `low_conf_entry=*` | 3 | Entry mit conf < 0.7 |
| weitere disagreements | 3 | Randfälle |

### Blocker-Breakdown
- STATUS_UPDATE 257 · NO_SIGNAL 243 · WATCHLIST 196 · WATCH_ALERT 66 · CONDITIONAL_WATCH 43

### Backup-Artefakte im Vault
- **DB-Kopie:** `backtest_results_2026-04-11.db` (1.7 MB, vollständige Rohdaten aller 2714 Messages)
- **CSV Review-Queue:** `backtest_review_queue_2026-04-11.csv` (47 Rows)
- **MD Review-Queue:** `Parser Rebuild — Phase B Review Queue.md` (pro Reason gruppiert, zum direkten Annotieren)

## Wie man den Fortschritt prüft

```bash
# Log live
tail -f /root/signal_bot/logs/backtest_phase_a.log

# Prozess
ps -p 2808960

# Progress aus DB
python3 -c "import sqlite3; c=sqlite3.connect('/root/signal_bot/data/backtest_results.db'); \
  print(c.execute('SELECT COUNT(*), ROUND(SUM(cost_usd),2) FROM results').fetchone()); \
  [print(r) for r in c.execute('SELECT stage_reached, COUNT(*) FROM results GROUP BY stage_reached')]"
```

## Nach Abschluss — nächste Schritte

1. **Finalreport prüfen** (letzte ~20 Zeilen im Log) — Stage-Counts, Errors, Top-Review-Reasons
2. **Review-Queue generieren** für Phase B:
   - Alle `needs_review=1` Rows
   - Gruppiert nach `review_reason`, sortiert nach Impact
   - Export als CSV oder Markdown im Vault
3. **Phase B** — manuelle Annotation (`human_verdict`, `human_note`)
4. **Phase C** — IBKR historical bars für alle Entry-Kandidaten laden
5. **Phase D** — End-to-End-Simulation mit SL/TP-Parameter-Sweep (inkl. TP-Kalibrierung, siehe `project_tp_calibration.md` in memory)

## Bekannte Caveats

- DB-Tabelle heißt `results` (nicht `backtest_results`) — `PRIMARY KEY (message_id, channel_id)`
- `old_parser` Vergleich basiert auf 105 Rows aus `trades.db` signals-Tabelle (nur ein Teil der 2714 hat alten Parser durchlaufen)
- Bot läuft aktuell **noch mit altem Parser** — Restart erst nach abgeschlossener Phase D

## Kontext / Warum

Die alten SL-Defaults waren aus der Luft gegriffen; Flat-8%-SL wurde empirisch aus 17 Jack-Entries kalibriert. Gleicher Ansatz soll jetzt für TP-Regeln verwendet werden — Phase D Stress-Test mit Parameter-Sweep liefert die Grundlage.

---

## Phase A v2 — Vision-fähiger Parser (läuft)

**Motivation:** Während der Phase-B-Review von v1 ist aufgefallen dass Jack bei vielen Entries einen **Broker-Screenshot** postet (Webull/Schwab) und der Text darunter nur minimal ist. Der text-only v1-Parser hat diese Entries systematisch verpasst — msg 131 SLS war das konkrete Beispiel.

**Was sich in v2 geändert hat:**
- `scripts/backfill_media.py` hat **203 Fotos** aus Telegram heruntergeladen und **110 Image-only Messages** (leerer Text) neu in `raw_messages.db` eingefügt, die v1 nie gesehen hat
- `parser.py` erweitert: Multimodal Content Blocks (base64), alle 3 Stages lesen Bilder, Stage-1-Blocker wird bei anwesendem Bild übersprungen
- `parser_context.py` holt `parent_image_path` aus raw_messages (Reply-Kontext inkl. Parent-Bild)
- `scripts/backtest_phase_a.py` threaded `media_path` + `image_paths` durch alle Stages
- Schema: alte `results` Tabelle wurde zu **`results_v1`** umbenannt, neue `results` Tabelle wird frisch befüllt

**Final v2 (2026-04-11 18:12 UTC):**
- **2774 Messages** in **85 Min** · **$12.84** · **0 Errors**
- Stages: 739 blocker · 1676 haiku · 51 sonnet · 308 opus
- **49 Review-Flags** (vs v1: 47)
- Log: `/root/signal_bot/logs/backtest_phase_a_v2.log`

### v1 ↔ v2 Diff

| Metrik | v1 | v2 | Δ |
|---|---|---|---|
| Total Messages | 2714 | 2824 | +110 (Image-only) |
| **Echte Entries** | 283 | **311** | **+28** 🎯 |
| Exits | 136 | 150 | +14 |
| Updates | 792 | 986 | +194 |
| Watchlist | 580 | 578 | -2 |
| Sonnet-Stage | 85 | 52 | -33 (Haiku filtert besser) |
| Opus-Stage | 300 | 315 | +15 |
| Review-Flags | 47 | 49 | ≈ gleich, andere Fälle |

**Neu erkannte Entries (30):** msg 131 SLS (Broker-Screenshot), 4× RCKT ($4.00–4.48), 4× OCGN, IBRX, EEIQ, SYNX, MAMO, BATL, u.a.

**Verlorene Entries (6):** alle in v2 korrekter als `exit` (CETY, UOKA), `commentary` (SOPA, TPET, msg 4682) oder `extend` (BRLS) umklassifiziert — Bugfixes, keine Verluste.

**Netto: +22 echte Entries gewonnen, bessere Klassifikation.**

### v2 Review-Queue Top Reasons

- 31× `opus_reject_after_sonnet_entry` (+4 vs v1 — Opus wird strenger)
- 11× `haiku_ambiguous` (-1)
- 2× `disagree_old=entry_new=watchlist`
- 5× Einzelfälle

### Backups im Vault
- **DB-Kopie v2:** `backtest_results_v2_2026-04-11.db` (3.1 MB)
- **CSV Review-Queue v2:** `backtest_review_queue_v2_2026-04-11.csv` (49 Rows)
- **MD Review-Queue v2:** `Parser Rebuild — Phase B Review Queue v2.md` — bereit zur manuellen Annotation ab #1

**Vision-Verifikation vorab:**
- **msg 131 SLS**: v2-Parser extrahiert korrekt ticker=SLS, entry_low/high=3.45, expiry_time=pre_market, confidence=0.92 aus dem Broker-Screenshot. Opus APPROVE mit Reasoning "confirmed by broker screenshot"
- **msg 3469 ELBM**: v1 sagte "watchlist" (falsch), v2 sagt "entry" (richtig) — und das ohne Bild, d.h. die Prompt-Verbesserungen in Stage 2/3/4 helfen auch reinem Text

**Nach Abschluss:**
- v1↔v2 Diff erstellen (welche Flags weg, welche neu)
- Review-Queue v2 gruppiert nach `review_reason` als CSV/MD exportieren
- Phase-B manuelle Review startet ab Nachricht #1 der v2-Queue

## Phase 0 ergänzt: Media-Backfill — ✅ DONE

Vor v2 wurde `scripts/backfill_media.py` gebaut und durchgelaufen:
- 2873 Telegram-Messages gescannt
- 203 Photos heruntergeladen nach `/root/signal_bot/data/media/`
- 110 Image-only Messages neu in DB eingefügt (leerer Text, aber `has_media=1`)
- 18 MB total, 0 Errors
- Schema-Erweiterung: `raw_messages` hat jetzt `has_media`, `media_type`, `media_path` Spalten

---

*Wird nach Full-Run-Abschluss mit Ergebnissen erweitert.*
