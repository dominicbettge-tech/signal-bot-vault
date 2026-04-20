---
title: Wiki Index
type: index
updated: 2026-04-20
---

# Wiki Index

Liste aller LLM-generierten Wiki-Pages in `00 Wiki/`. Wird bei jedem `ingest` regeneriert.

## MOCs (Map of Content — orphan-resolving)

- [[Signal-Bot-MOC]] — Map aller 50+ Signal-Bot-Notizen (Sim, Audit, Core-Docs)
- [[Parser-MOC]] — Parser-Review-Queues, Analyses, Implementation-Plans
- [[Ticker-Klassifikator-MOC]] — Phase-1/2 Klassifikator-Notizen

## Entities & Tools

- [[Jack-Sparo]] — Signal-Quelle (person)
- [[IBKR-Paper-Trading]] — Ausführungs-Backend (tool)
- [[Hermes-Gateway]] — Telegram-Front-End für claude-home (tool)

## Patterns

- [[Halt-Up-Pattern]] — validated Edge, Core-Strategy (n=53/37, +39.38% / +14.05pp vs Jack-Hold)
- [[Karpathy-LLM-Wiki]] — das Wiki-Pattern selbst (meta)

## Concepts (Research-Ingests)

- [[Chase-AI-Insights]] — Claude-Code-Feature-Audit aus 40 YT-Videos (Tier-1 Permission + Context-Fork)
- [[Matt-Pocock-Principles]] — TypeScript-Educator CC-Prinzipien (Ralph-Wiggum, Anti-CLAUDE.md)
- [[GPT-Code-Review-Findings]] — 8 Runden GPT-Kritik zu signal_manager.py (6 ACCEPT, 6 REJECT)

## Ingest-Convention

Jede neue Page bekommt hier einen Eintrag im Format:
- `[[page-name]]` — 1-Satz-Summary (type: entity/concept/tool/person/pattern/moc)

## Stand

- **W1 Foundation** (2026-04-20 11:07 UTC): CLAUDE.md Schema-Append + index + log angelegt
- **W2 Pages** (2026-04-20 11:25 UTC): 7 Pages (3 MOCs + 2 Entities + 2 Patterns)
- **W2b Pages** (2026-04-20 abends): +4 Pages (1 Tool + 3 Concepts aus Research-Notes) = 11 total
- **W3 Infra** (2026-04-20 10:10 UTC): `raw/` Folder live (README + YT-Seed) + Skill `vault-ingest` registriert. Hybrid-Ansatz statt GitHub-Plugin.
- **W3 Lint-Tool** (2026-04-20 12:08 UTC): `scripts/wiki_lint.py` (backtick-aware) + 2 Orphan-Fixes (Hermes-Gateway, GPT-Code-Review-Findings ← Signal-Bot-MOC). Lint-State: 13 pages / 127 links / 0 dead / 0 orphans.
