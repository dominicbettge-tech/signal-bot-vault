---
title: Chase-AI Insights
type: concept
tags: [claude-code, skills, research]
created: 2026-04-20
updated: 2026-04-20
sources: [[02 Projekte/Chase-AI YouTube Analyse 2026-04-17|Chase-AI YouTube Analyse 2026-04-17]]
---

## Summary

Claude-Code-Feature-Audit abgeleitet aus Chase-H-AI (@Chase-H-AI, 40 Videos ≤6 Monate) + Anthropic-Slash-Commands-Docs. Fokus auf Features die wir im [[Signal-Bot-MOC|Signal Bot]] noch nicht nutzten — primär um Permission-Prompt-Frust und Kontext-Kosten zu reduzieren.

## Details

### Tier-1 (sofort umzusetzen)

| # | Feature | Effekt | Ort |
|:-:|:-|:-|:-|
| 1 | `allowed-tools` in Skill-Frontmatter | Beendet Permission-Prompt-Bestätigungen während Skill aktiv | Skill-YAML |
| 2 | `context: fork` + `agent: Explore` | 60-80% Kontext-Ersparnis in Research-Phasen | Skill-YAML |
| 3 | Slash-Commands mit `$ARGUMENTS` | Parametrisierbare Prompts (Review-Ticker direkt) | `.claude/commands/` |
| 4 | Subagent `Explore` für Vault-Query | Grounded-Answers ohne Main-Context-Pollution | Agent-Dispatch |

### Tier-2 (mittel)

- MCP-Server für DB-Queries (statt sqlite3-Bash-Calls in jeder Review)
- Session-Hooks für Auto-Wrap-Up
- Output-Redirection für lange Command-Outputs

### Was NICHT übernehmen

- Chase's Click-Bait-Thumbnails-Style — für uns irrelevant, aber erklärt warum der Channel substantiell hinter [[Matt-Pocock-Principles|Matt Pocock]] liegt als Lehrer.

## Related

- [[Matt-Pocock-Principles]] — vergleichbarer Audit, höhere Signal-Dichte
- [[Signal-Bot-MOC]] — Anwendungs-Kontext
- [[Karpathy-LLM-Wiki]] — paralleles Pattern-Adoption

## History / Log

- 2026-04-17: Audit gelaufen, 40 Videos durchgearbeitet
- 2026-04-20: Ingest ins Wiki
