---
title: Knowledge Housekeeping Proposals
date: 2026-04-25
type: proposal
tags: [housekeeping, memory, wiki, propose-only]
---

## Summary

- **346 Memory-Files** inventarisiert, **MEMORY.md 188/200 Zeilen** (12 Zeilen Headroom).
- **0 echte Dangling-Refs** (17 false-positives sind externe Wiki-MOCs in `00 Wiki/`).
- **0 stale Tactical-Pins** (alle aktuellen Pins <14d alt — kein Pin-Removal nötig).
- **142 Orphan-Files** im Memory aber nicht direkt in MEMORY.md verlinkt. **120+ davon sind erwartet** (durch heutige MOC-Migration via Wiki-Refs erreichbar) — kein Akut-Handlungsbedarf.
- **3 echte Vorschläge** unten: 1× Duplicate-Cluster, 1× Legacy-Phase-Files, 1× Misc-Review-Hinweis.
- Kein File geändert. Manuelle Bestätigung nötig.

---

## Kategorie 1 — Migrate-to-Wiki (0)

Heutige Migration (`MEMORY_proposed_2026-04-25.md` → MEMORY.md) hat alle 7 großen Cluster bereits durch Wiki-MOC-Refs ersetzt. Nichts mehr zu migrieren.

| Status | MOC | Files-im-Cluster |
|---|---|---|
| ✅ Done | Kairos-MOC.md | 18 (alle 04-23/04-24) |
| ✅ Done | Parser-V2-MOC.md | 4 (alle 04-24) |
| ✅ Done | Auto-Research-MOC.md | 13 (Round 17c-18r) |
| ✅ Done | KAPPI-MOC.md | 27 (P1-P8) |
| ✅ Done | Watchdog-MOC.md | 2 |
| ✅ Done | Review-Workflow-MOC.md | 38 |
| ✅ Done | Testcenter-MOC.md | 11 |

---

## Kategorie 2 — Stale-Tactical (0)

Kein Tactical-Pin in MEMORY.md älter als 14 Tage. Frühester Pin: `BATCH-SIM 2026-04-20` = 5d alt. Re-Check empfohlen am **2026-05-05** (in 10 Tagen).

---

## Kategorie 3 — Cluster-to-MOC (0)

Alle 7 großen Cluster heute schon migriert. Keine neuen Cluster ≥3 Files seit der Migration entstanden.

---

## Kategorie 4 — Duplicate (1 Cluster)

### Review-Format-Versionen (3 Files, alle 11+ Tage alt)

| File | Alter | Vorschlag |
|---|---:|---|
| `feedback_review_format.md` | 11.9d | Vermutlich obsolet — nur falls v3 nicht alle Inhalte abdeckt |
| `feedback_review_format_v2.md` | 11.7d | Vermutlich obsolet |
| `feedback_review_format_v3.md` | 10.9d | Wahrscheinlich canonical |

**Empfehlung:**
1. v1 + v2 + v3 nebeneinander lesen, prüfen ob v3 alle Inhalte schluckt
2. Wenn ja: v1 + v2 in `Review-Workflow-MOC.md` als "ältere Iteration archiviert" erwähnen, Memory-Files belassen (additiv-only)
3. Optional: einen Pointer-Pin in MEMORY.md hinzufügen: `> ⚠️ **REVIEW-FORMAT v3** Canonical → feedback_review_format_v3.md` (1 Zeile)

**Begründung:** 3 Files mit gleichem Topic, kein einziger ist im Index direkt gepinnt — User schiebt hier gerade durch MOC-Layer hindurch, aber das aktuell gültige Format ist nicht offensichtlich.

---

## Kategorie 5 — Orphan-Pin (0 echt)

Erweiterte Regex-Suche: 0 echte Dangling-Pins. Die 17 vom alten `memory_orphan_check.py` gemeldeten "Dangling" sind externe Wiki-MOCs (`Kairos-MOC.md`, `Halt-Up-Pattern.md` etc.), die in `00 Wiki/` leben — false-positive.

**Sub-Vorschlag (Tooling):**
- `scripts/memory_orphan_check.py` ergänzen um Whitelist `WIKI_MOC_REFS = {"Kairos-MOC.md", ...}` oder Path-Heuristik (`00 Wiki/`-prefix erkennen) — sonst meldet das Tool Dauerrauschen.
- Aber: kleine Sache, kein Akut-Bug.

---

## Kategorie 6 — Legacy-Phase Files (NEU, 4 Files)

Files mit alter Phase-Numerierung (`project_42_*`, `project_45_*`, `project_46_*`), 6.8d alt — wahrscheinlich aus prä-MOC-Phase und nicht mit-migriert:

| File | Alter | Topic |
|---|---:|---|
| `project_42_46_implementation_design.md` | 6.8d | Phase 42/46 Design |
| `project_42_staggered_entry_foundation.md` | 6.8d | Staggered-Entry-Basis |
| `project_45_extend_scope_closed.md` | 6.8d | Scope-Extension geschlossen |
| `project_46_halt_up_hybrid_foundation.md` | 6.8d | Halt-Up-Hybrid-Basis |

**Vorschlag:**
- 4 Files lesen, prüfen ob Inhalt in `Halt-Up-Pattern.md` MOC + `staggered_entry`/`halt_up`-Strategie-Specs schon abgedeckt ist
- Wenn ja: als "completed phases" in MOCs verlinken, Memory-Files belassen
- Wenn nein: einzelner Pin hinzufügen oder Inhalte in passenden Wiki-MOC integrieren

---

## Kategorie 7 — Misc-Orphans (NEU, 25 Files)

Files in der "misc"-Kategorie, die nicht direkt im aktuellen MEMORY.md-Index erscheinen aber thematisch zu bestehenden MOCs gehören könnten:

| File | Alter | Mögliches MOC-Ziel |
|---|---:|---|
| `project_alt_b_execution_2026_04_21.md` | 4.2d | Loop-Orchestrator (Alt-B Missed-Trades) |
| `project_alt_c_paused_2026_04_21.md` | 4.2d | Signal-Bot-MOC (Alt-C Roadmap) |
| `project_bot_knowledge_integration.md` | 10.7d | Signal-Bot-MOC |
| `project_c14_winner_validated.md` | 3.9d | Auto-Research-MOC |
| `project_chart_ocr_range_validator.md` | 7.6d | Parser-MOC oder eigenes Chart-MOC |
| `project_chart_pattern_learner.md` | 7.6d | Parser-MOC oder Chart-MOC |
| `project_entry_comparison_pipeline_2026_04_23.md` | 1.6d | Kairos-MOC |
| `project_hauptprojekt_2_auto_research_loop.md` | 3.8d | Auto-Research-MOC |
| `project_jack_edge_audit_2026_04_16.md` | 7.7d | Jack-Sparo MOC |
| `project_karpathy_build_baseline_2026_04_22.md` | 3.2d | Karpathy-LLM-Wiki |
| `project_module_hybrid_review_2026_04_17.md` | 8.6d | Review-Workflow-MOC |
| `project_param_sweep_uncap_tp_2026_04_18.md` | 6.6d | KAPPI-MOC |
| `project_parser_api_credits_failed_2026_04_22.md` | 2.8d | Parser-MOC (V1) |
| `project_polygon_backfill_tickers_24.md` | 6.9d | Signal-Bot-MOC (Daten-Pipeline) |
| `project_post_backfill_sims_2026_04_18.md` | 6.9d | Auto-Research-MOC |
| `project_post_review_build_queue.md` | 6.9d | Review-Workflow-MOC |
| `project_priority_review_before_testcenter.md` | 7.6d | Review-Workflow-MOC |
| `project_profit_pipeline_2026_04_16.md` | 8.7d | Signal-Bot-MOC |
| `project_review_pending_tickers.md` | 10.7d | Review-Workflow-MOC (Runtime-State) |
| `project_round2_autonomous_2026_04_18.md` | 6.6d | Review-Workflow-MOC |
| `project_rule_engine_architecture.md` | 10.7d | Karpathy-LLM-Wiki / Auto-Research-MOC |
| `project_rule_hypotheses.md` | 5.6d | Auto-Research-MOC |
| `project_simulation_results.md` | 11.8d | Auto-Research-MOC |
| `project_slippage_mitigation_options.md` | 13.2d | KAPPI-MOC oder Halt-Up-Pattern |
| `project_upper_range_stagger_design_2026_04_22.md` | 3.2d | Halt-Up-Pattern oder Staggered-Entry |

**Vorschlag:**
- 25 Files in passenden MOCs als "Detail-Refs" verlinken (1 Backlink pro File)
- Memory-Files unangetastet lassen — sie sind durch zukünftige MOC-Backlinks erreichbar
- Optional: `project_review_pending_tickers.md` (10.7d) ist Runtime-State und sollte vermutlich aktualisiert/abgeräumt werden — User-Entscheidung

---

## Empfohlene Reihenfolge

1. **Kategorie 4 (Duplicate)** — `feedback_review_format_v1/v2/v3` lesen, canonical-Pin in MEMORY.md (1 Zeile, +1 LoC)
2. **Kategorie 6 (Legacy-Phase)** — 4 P42-46-Files in `Halt-Up-Pattern.md` MOC backlinken
3. **Kategorie 7 (Misc-Orphans)** — 25 Files in passende MOCs backlinken (low priority, kein Akut-Bedarf)
4. **Sub-Tool-Fix** — `memory_orphan_check.py` Wiki-MOC-Whitelist (3 Zeilen Code, optional)

## Was NICHT zu tun ist

- Kein Memory-File löschen
- Kein bestehender MEMORY.md-Pin verändern
- Keine Wiki-MOCs überschreiben
- Kein Auto-Cron — nächste manuelle Iteration in **7 Tagen (2026-05-02)** oder bei MEMORY.md ≥195 Zeilen

## Migration-Status (Kontext)

Heutige Memory-Konsolidierung ist **erfolgreich abgeschlossen**. Vor 2026-04-25:
- 7 Cluster mit 60+ Pins direkt in MEMORY.md (Kairos 18, Review-Workflow 24, etc.)

Nach 2026-04-25:
- 14 MOC-Refs (2 pro Cluster: Wiki-MOC + LATEST-Detail), Cluster-Bloat eliminiert.
- 188/200 Zeilen — gesundes Polster.

Dieser Housekeeping-Pass bestätigt: kein Drift, kein Akut-Restmüll. Nächster Run wenn neue Build-Phase startet (z.B. Parser_V3, neuer Loop) oder MEMORY.md wieder ≥195 Zeilen erreicht.
