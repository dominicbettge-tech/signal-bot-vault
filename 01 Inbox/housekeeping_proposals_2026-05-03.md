---
title: Knowledge Housekeeping Proposals
date: 2026-05-03
type: proposal
tags: [housekeeping, memory, wiki, propose-only]
prev_run: 2026-04-25
gap_days: 8
---

## Summary

- **346 Memory-Files** inventarisiert (∆ +0 seit 25.04. — kein File neu erstellt).
- **MEMORY.md mtime = 8.3 Tage alt** trotz massiver Aktivität in den letzten 8 Tagen (Stresstest-Framework, V1-V5 Tracking-Tools, Race-Day-Prep, parser_drop_detector, Telegram-Bundling). → **Größter Befund:** Drift zwischen CLAUDE.md (lebt) und MEMORY.md (eingefroren).
- **0 echte Orphan-Pins** (1 false-positive: `YYYY-MM-DD.md` ist Pattern aus REGEL 1-Beschreibung, kein Ref).
- **13 Tactical-Pins driften in 1-3 Tagen über 14d Stale-Threshold** — vorausschauender Pin-Removal-Vorschlag.
- **1 Duplicate-Cluster aus 25.04. noch ungelöst** (`feedback_review_format_v1/v2/v3`).
- **Cluster-Migration: vollständig.** Alle ≥3-File-Cluster sind via MOC-Refs erreichbar.

Kein File geändert. Manuelle Bestätigung nötig.

---

## Kategorie 0 — Memory-Activity-Gap (NEU, höchste Priorität)

**Befund:**
MEMORY.md wurde seit 2026-04-25 nicht mehr berührt (mtime 8.3d alt). In diesen 8 Tagen sind aber laut CLAUDE.md erhebliche Architekturentscheidungen + neue Subsysteme entstanden:

| Bereich | Datum | CLAUDE.md-Section | Status in Memory |
|---|---|---|---|
| Stresstest-Framework | 02.05. | "🧪 STRESSTEST-FRAMEWORK" | ❌ kein Memory-Eintrag |
| Stresstest Knowledge-System | 02.05. | "🧠 STRESSTEST KNOWLEDGE-SYSTEM" | ❌ kein Memory-Eintrag |
| Stresstest Pre-Flight-Update | 02.05. | "🧪 STRESSTEST WOCHENEND-UPDATE" | ❌ kein Memory-Eintrag |
| Race-Day-Session 03.05. | 03.05. | "📅 SESSION 2026-05-03" | ❌ kein Memory-Eintrag |
| Tracking-Tools V1-V5 | 03.05. | "Block II: Tracking-Tools V1-V5" | ❌ kein Memory-Eintrag |
| Telegram-Bundling α-2 | 03.05. | "Telegram-Bundling" | ❌ kein Memory-Eintrag |
| parser_drop_detector | 03.05. | erwähnt | ❌ kein Memory-Eintrag |
| LONG_ONLY_MODE | 28.04. | "🔒 Long-Only Mode" | ❌ kein Memory-Eintrag |
| CONDITIONAL_ENTRY | 28.04. | "Conditional-Entry-Architektur" | ❌ kein Memory-Eintrag |
| MAX-only Policy (RuntimeError-Lock) | 29.04. | "MAX-only Policy" | ❌ kein Memory-Eintrag |
| Bug #40 + #41 Fixes | 29.04. | "Bug #40 + #41 Fixes" | ❌ kein Memory-Eintrag |
| ENTRY_MODE=classic SL-Politik | 28.04. | "Order-Strategie + SL-Logik" | ❌ kein Memory-Eintrag |
| Skills-Routing (37 Skills installiert) | 28./29.04. | "🧠 Skills" | ❌ kein Memory-Eintrag |

**Vorschlag (kein Auto-Write):**
- 7-10 neue project-Memory-Files erstellen für die durable Architecture-Decisions (Stresstest-Framework, V1-V5 Tools, LONG_ONLY, CONDITIONAL_ENTRY, MAX-only Policy, ENTRY_MODE=classic).
- Pins in MEMORY.md hinzufügen — pro Subsystem 1 Pin (additiv).
- Alternativ: CLAUDE.md-Sections direkt in `00 Wiki/`-MOCs verlinken (REGEL 3 Wiki-First) und nur Tactical-Pin in MEMORY.md halten.

**Risiko ohne Aktion:** Bei nächster Compaction oder neuem Claude-Chat geht der durable Knowledge teilweise verloren — CLAUDE.md ist groß (>1500 Zeilen), Memory ist die schnellere Lookup-Schicht.

**Empfohlene Reihenfolge der Memory-Neuanlagen:**
1. `project_stresstest_framework_2026_05_02.md` — Pfad, Architektur, LOCKED-Decisions
2. `project_stresstest_knowledge_system_2026_05_02.md` — read_before_fix.sh Workflow
3. `project_tracking_tools_v1_v5_2026_05_03.md` — V1-V5 + Cron-Plan + Backlog
4. `project_telegram_bundling_alpha2_2026_05_03.md` — Architektur + Cron-Aktivierung
5. `project_long_only_mode_2026_04_28.md` — Defense-in-Depth, Sprach-Regel
6. `project_conditional_entry_2026_04_28.md` — Pattern, Time-Phrase-Parser, Confidence-Floor
7. `project_max_only_policy_2026_04_29.md` — RuntimeError-Lock in 3 Parsern, analyzer-Umstellung
8. `project_entry_mode_classic_sl_politik_2026_04_28.md` — Limit-Buy 1.06×, SL=fill×0.92
9. `feedback_short_is_ghost_not_short.md` — Sprach-Regel: negative Quantity = Artifact
10. `project_parser_drop_detector_2026_05_03.md` — Tool, Issue #66/#67/#68

---

## Kategorie 1 — Migrate-to-Wiki (0)

Keine neuen Migrationen nötig. Migration vom 25.04. bleibt vollständig.

---

## Kategorie 2 — Stale-Tactical (13 Pins, alle 11-13d alt, drift in 1-3 Tagen über 14d-Threshold)

Diese Tactical-Pins in MEMORY.md werden in 1-3 Tagen über 14d alt. Heute noch nicht akut, aber **vorausschauender Pin-Removal** empfohlen damit MEMORY.md weiter Headroom behält:

| Pin in MEMORY.md | Datum | Alter heute | >14d ab |
|---|---|---:|---|
| `BREAKOUT-ENTRY DEPLOYED 2026-04-21` | 21.04. | 12.4d | 05.05. |
| `CHART-VISION-SCANNER v1 shipped 2026-04-21` | 21.04. | 12.4d | 05.05. |
| `JACK-MISS-ANALYSIS 04-21/22` | 22.04. | 11.5d | 06.05. |
| `R18r PROD-WIRING 2026-04-22` | 22.04. | 11.5d | 06.05. |
| `PAPER-LEARNING-MODE 2026-04-22` | 22.04. | 11.5d | 06.05. |
| `FULL 6W-REPLAY 2026-04-22` | 22.04. | 11.5d | 06.05. |
| `DEDUP EMPTY-TICKER FIX 2026-04-22` | 22.04. | 11.5d | 06.05. |
| `CHAIN-INHERIT LIVE-DB 2026-04-22` | 22.04. | 11.5d | 06.05. |
| `USER-GATE-TRIO shipped 2026-04-20` | 20.04. | 13.4d | 04.05. |
| `ALT-B MISSED-TRADES-LOOP shipped 2026-04-20` | 20.04. | 13.4d | 04.05. |
| `BATCH-SIM 2026-04-20` | 20.04. | 13.4d | 04.05. |
| `CLONE-CANONICAL-GAP + FIX-20` | 20.04. | 13.4d | 04.05. |
| `SESSION-WRAP 2026-04-20 T9-17` | 20.04. | 13.4d | 04.05. |

**Vorschlag:**
- Pins in MEMORY.md belassen bis sie wirklich >14d sind (also stille Frist-Wache, kein Akut-Removal heute)
- Wenn >14d und keine Folgearbeit dranklebt: aus MEMORY.md entfernen (Detail-Files in `memory/` belassen — additiv-only)
- Falls die Tactical-Decisions noch hot sind (z.B. BREAKOUT-ENTRY läuft noch live): in passenden Wiki-MOC integrieren statt Pin verlieren

**Begründung:** Stale-Pins die noch im Index hängen blocken zukünftige neue Pins (200-Zeilen-Limit) und verwässern die Übersicht. Aber Race-Day morgen — heute keinen unnötigen Aufruhr.

---

## Kategorie 3 — Cluster-to-MOC (0)

Bestehende Cluster sind alle MOC-vermittelt. Neue Cluster ≥3 Files seit 25.04. **keine** entstanden — der `parser_v2_*`-Cluster (5 Files) und alle `kappi_p*`-Cluster sind unverändert.

---

## Kategorie 4 — Duplicate (1 Cluster, ÜBERTRAG aus 25.04.)

### Review-Format-Versionen (3 Files, immer noch ungelöst)

| File | Alter | Status | Vorschlag |
|---|---:|---|---|
| `feedback_review_format.md` | 19.7d | unverändert | Vermutlich obsolet — v3 prüfen |
| `feedback_review_format_v2.md` | 19.6d | unverändert | Vermutlich obsolet |
| `feedback_review_format_v3.md` | 18.7d | unverändert | Wahrscheinlich canonical |

**Status:** Identische Empfehlung wie 25.04. — User hat noch nicht entschieden. Re-vorschlag:
1. v1 + v2 + v3 nebeneinander lesen (10 Min)
2. v3 in `Review-Workflow-MOC.md` als canonical markieren
3. v1+v2 als "ältere Iteration archiviert" verlinken
4. Optional 1-Zeilen-Pin: `> ⚠️ **REVIEW-FORMAT v3** Canonical → feedback_review_format_v3.md`

---

## Kategorie 5 — Orphan-Pin (0 echte)

Sauber. 1 false-positive (`YYYY-MM-DD.md` aus REGEL 1-Beschreibungstext, kein echter Pin).

---

## Kategorie 6 — Übertragung aus 25.04. (Status-Update)

| Vorschlag aus 25.04. | Damals | Heute | Aktion empfohlen |
|---|---|---|---|
| Legacy-Phase-Files (P42/45/46) | 4 Files | unverändert | wie 25.04.: in Halt-Up MOC backlinken |
| Misc-Orphans (25 Files) | 25 Files | unverändert | wie 25.04.: in passende MOCs backlinken (low prio) |
| `memory_orphan_check.py` Wiki-Whitelist | offen | offen | minor — kein Akut-Bug |

---

## Empfohlene Reihenfolge

1. **POST-RACE-DAY (Di 05.05. abend):** Kategorie 0 angehen — die 10 fehlenden project-Memory-Files anlegen oder CLAUDE.md-Sections in MOCs aufnehmen. Größtes Drift-Risiko.
2. **Mi 06.05.:** Kategorie 2 — die 13 Tactical-Pins überprüfen (>14d) und entweder MOC-integrieren oder Pin entfernen.
3. **Wenn Lust:** Kategorie 4 — die 3 Review-Format-Files entscheiden (5-10 Min Lese-Aufgabe).
4. **Backlog:** Übertragene 25.04.-Vorschläge (Legacy-Phase, Misc-Orphans, Wiki-Whitelist) bleiben low-prio.

## Was NICHT zu tun ist

- ❌ Heute (Race-Day-Vorabend) keine Memory-Edits mehr — Code-Freeze gilt auch für Knowledge.
- ❌ Memory-Files löschen oder umbenennen (additiv-only, immer).
- ❌ Wiki-MOCs überschreiben.
- ❌ MEMORY.md-Pins gewaltsam neu sortieren — bestehende Reihenfolge respektieren.
- ❌ Kein Auto-Cron — manueller Aufruf bleibt.

## Nächster Run

Empfohlen: **Sa 10.05.** (1 Woche nach heute) — nach Race-Day Auswertung + nach voraussichtlich neuen Memory-Einträgen aus Kategorie 0.

Trigger-Conditions die einen früheren Run rechtfertigen:
- MEMORY.md erreicht ≥195 Zeilen
- Eine neue Build-Phase startet (z.B. neuer Loop-Module, Phase-3-Architektur)
- ≥10 neue project_*.md Files in einer Woche

---

## Health-Check

| Metrik | Wert | Status |
|---|---:|:---:|
| Memory-Files total | 346 | ✓ |
| MEMORY.md geschätzte Zeilen | ~155 (basierend auf Index-Counts) | ✓ Headroom |
| Echte Orphan-Pins | 0 | ✓ |
| Files >30d alt | 0 | ✓ |
| Stale-Tactical >14d | 0 (heute), 13 in 1-3 Tagen | ⚠ vorausschauend |
| MEMORY.md mtime | 8.3d | ⚠ Drift gegenüber CLAUDE.md |
| Duplicate-Cluster | 1 (übertragen aus 25.04.) | ⚠ unverändert |
| Wiki-MOCs aktiv | 19 | ✓ |

Gesamt-Bewertung: **Gesund mit 1 wichtigem Befund** (Kategorie 0 = Memory-Activity-Gap). Race-Day morgen — Empfehlung: heute nichts ändern, ab Di 05.05. die offenen Punkte angehen.
