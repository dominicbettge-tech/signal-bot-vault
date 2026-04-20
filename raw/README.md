---
title: raw/ — Immutable Source-Store
type: meta
created: 2026-04-20
---

# `raw/` — Immutable Source-Dokumente

Karpathy-Pattern (W3): Dieser Ordner enthält **immutable Source-Dokumente** — nie editieren, nur anhängen.

## Regeln

1. **Immutable** — einmal hier, nie ändern. Neue Version = neuer File.
2. **Naming** — `YYYY-MM-DD_<type>_<slug>.md` (z.B. `2026-04-20_yt_R0_R-zZ8p8U_karpathy.md`)
3. **Wiki-Pages in `00 Wiki/` leiten davon ab** — setzen `sources: [[raw/<file>]]` im Frontmatter, ersetzen das Original nicht.
4. **Nicht versehentlich als normale Vault-Note behandeln** — Obsidian-Graph wird `raw/` mit anzeigen, das ist okay. Struktur via `00 Wiki/` statt via `raw/`.

## Content-Typen

- `yt_<videoid>` — YouTube-Transkripte (verbatim oder rekonstruiert)
- `article_<slug>` — Blog-Artikel, Web-Clipper-Output
- `paper_<slug>` — wissenschaftliche Paper / Drafts
- `transcript_<slug>` — Meeting/Interview-Transkripte
- `chat_<slug>` — wichtige ChatGPT/Claude-Gespräche die Context bilden

## Workflow

1. Paste Source → `raw/<date>_<type>_<slug>.md` ablegen
2. Skill `vault-ingest` ausführen (siehe `/root/.claude/skills/vault-ingest/SKILL.md`)
3. Ingest erzeugt/updated Pages in `00 Wiki/`, fügt Zeile in `00 Wiki/log.md`, updatet `00 Wiki/index.md`

## Aktuelle Sources

- `2026-04-20_yt_R0_R-zZ8p8U_karpathy.md` — Nate Herk YT-Video „Claude ist jetzt 10x schlauer geworden mit Obsidian" (Seed für [[Karpathy-LLM-Wiki]])
