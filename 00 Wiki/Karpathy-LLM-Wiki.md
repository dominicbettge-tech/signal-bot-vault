---
title: Karpathy LLM-Wiki-Pattern
type: pattern
tags: [obsidian, llm, knowledge-management, karpathy]
created: 2026-04-20
updated: 2026-04-20
sources: [[04 Ressourcen/KI Allgemein/Claude Obsidian System Daniel Walter 2026-04-20]], [[raw/2026-04-20_yt_R0_R-zZ8p8U_karpathy]]
---

## Summary

Pattern von Andrej Karpathy (via Nate Herk/Daniel Walter YT R0_R-zZ8p8U): LLM-Wissensspeicher auf Basis von `raw/` (immutable Sources) + `wiki/` (LLM-generierte Konzept-Pages mit `[[Wikilinks]]`) + `CLAUDE.md` (Schema) + `index.md` + `log.md`. Berichtet bis zu **95% Token-Savings** bei Queries gegenüber klassischer Similarity-Search, weil Claude strukturell via Index+Backlinks navigiert statt ganzen Corpus zu scannen.

## Die 3 Operationen

| Op | Zweck | Details |
|:-|:-|:-|
| `ingest <source>` | raw → wiki | Entities extrahieren, Pages updaten, Links setzen, index.md + log.md fortschreiben |
| `query <frage>` | wiki → Antwort | Index lesen, Wikilinks folgen, grounded antworten, Zitate |
| `lint` | wiki → Health | Dead Links, Orphans, Contradictions, Stale Content |

## Die 4 Bausteine (Daniel-Walter-Framing)

1. **CLAUDE.md** als Routing-Handbuch — wir haben × 3 (Root, signal_bot, obsidian_vault)
2. **Vault** als Wissensspeicher — PARA-Struktur vorhanden
3. **Auto-Write** — Daily-Note-Mandate + Memory-System
4. **Skills** als SOPs — 20+ Skills in `/root/.claude/skills/`

**Befund:** Wir sind schon weiter als das Video. Karpathy/Walter validieren den Ansatz.

## Adoption bei uns

- **W1 (done 2026-04-20 11:07 UTC)** — Foundation: `CLAUDE.md` Schema-Append + `00 Wiki/{index,log}.md`.
- **W2 (done 2026-04-20)** — diese Page + 6 weitere Wiki-Pages (3 MOCs + 3 Entities + dieses Pattern selbst).
- **W3 (pending)** — `raw/` Folder-Split + GitHub-Plugin-Adoption (`ekadetov/llm-wiki`, `AgriciDaniel/claude-obsidian`, `Pratiyush/llm-wiki`).

## Empirie

- Nate Herk: 36 YT-Videos → Wiki-Pages in 14min
- X-User-Case: 383 scattered Files → 95% Token-Savings via Wiki-Navigation

## Related

- [[Signal-Bot-MOC]] — 1. Konsument der Wiki-Navigation
- [[Parser-MOC]] — nutzt Wiki für Konzept-Referenzen
- [[04 Ressourcen/KI Allgemein/Claude Obsidian System Daniel Walter 2026-04-20|Daniel Walter Notiz]] — Source

## Externe Referenzen

- YT-Video: https://www.youtube.com/watch?v=R0_R-zZ8p8U (Nate Herk, 17min)
- Raw-Seed: [[raw/2026-04-20_yt_R0_R-zZ8p8U_karpathy]] — immutable Transkript
- Raw-Regeln: [[raw/README|raw/ README]] — Naming, Content-Typen, Workflow
- Memory: `project_karpathy_llm_wiki_pattern_obsidian.md` — Adoption-Plan
- Memory: `reference_yt_transcript_vps_ban_bypass.md` — wie wir das Transkript trotz IP-Ban rekonstruierten
- Report: `signal_bot/reports/yt_transcript_R0_R-zZ8p8U.md` (Terminal-CC-Work)
- Report: `signal_bot/reports/cycle32_obsidian_vault_audit_2026-04-20.md` — Orphan-Problem das W2-MOCs adressieren
