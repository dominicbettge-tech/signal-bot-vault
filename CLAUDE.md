# Vault Context

Dieses Vault ist das Zweite Gehirn von Dominic Bettge.

## Über mich

Dominic Bettge, Physiotherapeut aus Deutschland. Baut automatisierte Trading-Systeme — aktuell den Signal Bot v3 der Telegram-Signale von Jack Sparo parsed und über IBKR Paper Trading ausführt. Ziel: finanzielle Unabhängigkeit durch automatisierten Handel. Ausführliches Profil in 00 Kontext/Über mich.md.

## Vault-Struktur

- **00 Kontext/**: Persönliches Kontext-Profil (Über mich.md, ICP.md, Angebot.md, Schreibstil.md, Branding.md). Zentrale Referenz für alle inhaltlichen Aufgaben.
- **01 Inbox/**: Schnelle Gedanken, Brain Dumps, unverarbeitete Notizen. Alles was noch keinen festen Platz hat landet hier.
- **02 Projekte/**: Aktive Projekte. Signal Bot.md (Hauptprojekt), Trading.md (Strategie), Signal Bot Fehler-Log.md (alle Bugs).
- **03 Bereiche/**: Trading/ (Strategie, Parameter, Kanäle), Finanzen/ (IBKR Account, Ziele).
- **04 Ressourcen/**: Claude Skills/, Claude Code Tools/, KI Allgemein/, Trading Gruppen/ (Jack Sparo Kanäle).
- **05 Daily Notes/**: Tägliches Logbuch. Format: YYYY-MM-DD.md
- **06 Archiv/**: Abgeschlossene Projekte und inaktive Bereiche.
- **07 Anhänge/**: Bilder, PDFs, Medien.

## Was Claude hier speichert

- Bugfixes → `02 Projekte/Signal Bot Fehler-Log.md`
- Projektfortschritt → `02 Projekte/Signal Bot.md`
- Trading-Erkenntnisse → `03 Bereiche/Trading/Trading.md`
- Neue Skills/Tools → `04 Ressourcen/Claude Skills/`
- Session-Ende → Daily Note in `05 Daily Notes/YYYY-MM-DD.md` anbieten

## Parallele Wissens-Systeme (Routing — Alt-B ab 2026-04-20)

Claude hat **5 Wissens-Layer** mit klaren Ownership-Boundaries. Alt-B-Regel: Wiki ist die durable-knowledge-Ebene, Memory nur Runtime-Ops.

| Layer | Pfad | Inhalt | Schreibt | Auto-Load? |
|:-|:-|:-|:-|:-:|
| **raw/** | `/root/obsidian_vault/raw/` | Immutable Sources (YT-Transkripte, Artikel, Papers) — NIE editieren | Claude via `vault-ingest ingest` | ❌ |
| **00 Wiki/** | `/root/obsidian_vault/00 Wiki/` | **Durable Concepts** — Entities, Tools, People, Patterns, MOCs (cross-linked via Wikilinks) | Claude curated | ❌ (on-demand) |
| **PARA 01-06** | `/root/obsidian_vault/0[1-6]*/` | Active Workspace: Projekt-Docs, Daily Notes, Research-Notes, Brainstorms, Inbox | Dominic + Claude | Teilweise (Session-Start Inbox-Check) |
| **Memory** | `/root/.claude/projects/-root-signal-bot/memory/` | **Runtime-Ops**: user-profile, feedback_*, ephemeral project-state, adoption-triggers | Claude auto-save | ✅ (MEMORY.md Index 200 Zeilen) |
| **Skills** | `/root/.claude/skills/` | Wiederverwendbare SOPs (grounded-decisions, brainstorming, wrap-up, …) | Menschlich curated | ❌ (via Skill-Tool) |

### Routing-Regel (WIKI-FIRST für durable Knowledge)

- **Durable Concept** (Pattern, Entity, Tool, Person) → **Wiki FIRST**. Neue Memory-Einträge für durable Knowledge nur als Pointer ("@see Wiki-Page" Pointer) + operational „How to apply"/„Why (Timing)".
- **Ephemeral State** (aktuelle Review-Queue, Sprint-Backlog, feedback-Regel) → **Memory**.
- **Durable + Operational** (z.B. Halt-Up-Pattern + 8-Punkt-Checkliste): **Wiki = Summary + Validated-Metriken**, **Memory = „How to apply"-Trigger** mit Pointer zu Wiki. Kein Duplikat der Summary.
- **Research-Input** (neuer Artikel/Video): `raw/` → Wiki-Ingest via `vault-ingest` Skill. PARA bleibt unberührt.

Faustregel (kurz): **Was für Dominic lesbar sein muss → Vault. Was durable Wissen ist → 00 Wiki/. Was Claude sich selbst merkt → Memory. Was wiederholbare Prozedur ist → Skill.**

## Regeln für dieses Vault

- Nutze [[Wikilinks]] für Verknüpfungen zwischen Notizen
- Neue Notizen ohne klaren Platz kommen in 01 Inbox/
- Daily Notes im Format: YYYY-MM-DD.md
- YAML Frontmatter nutzen: tags, status, date
- Dateinamen in normaler Schreibweise mit Leerzeichen und Großbuchstaben
- Neue Projekte als einzelne .md Datei direkt unter 02 Projekte/
- Bereiche und Ressourcen sind immer Ordner
- Abgeschlossene Projekte nach 06 Archiv/ verschieben — nur auf Anweisung
- Bevor Dateien gelöscht oder überschrieben werden, nachfragen
- Wenn Dominic sagt "merk dir das" → in die passende Kontext-Datei speichern

## Session-Routinen

### Bei Session-Start
1. Prüfe 01 Inbox/ auf neue Notizen, zeige was drin liegt, biete an einzusortieren

### Kontext bei Bedarf
Wenn Dominic fragt "Was ist gerade aktuell?" oder "Wo war ich stehen geblieben?": Lies die letzten 2-3 Daily Notes und die aktiven Projekt-Dateien für ein kurzes Briefing.

### Bei Session-Ende
Anbieten:
1. Daily Note in 05 Daily Notes/ erstellen mit Zusammenfassung
2. Neue Erkenntnisse als Notizen speichern
3. Inbox aufräumen falls nötig

---

## LLM-Wiki-Layer (Karpathy-Pattern, W1 Foundation 2026-04-20)

Ergänzend zur PARA-Struktur oben: Claude nutzt `00 Wiki/` als LLM-optimierte Konzept-Ebene. PARA bleibt als menschenlesbare Ablage unverändert — das Wiki ist ein paralleler Index für grounded LLM-Queries statt Halluzination.

### Struktur

```
00 Wiki/         ← LLM-generierte Wiki-Pages (cross-linked via [[Wikilinks]])
├── index.md      ← Liste aller Wiki-Pages (bei jedem ingest updated)
├── log.md        ← Append-only Log aller ingest-Operationen
└── hot.md        ← ~500-Wort Session-Context (later, W1b)

raw/             ← NEU: immutable Source-Dokumente (W3, leer im W1)
```

**Regel:** `raw/` (wenn angelegt) ist immutable. Wiki-Pages werden daraus abgeleitet, ersetzen das Original nicht.

### Die 3 Operationen (W3-Target)

**`ingest <file-or-url>`**
1. Lies Source aus `raw/` (lege ab falls Input URL/Paste)
2. Extrahiere Entities, Konzepte, Tools, People, Pattern
3. Updatiere bestehende Wiki-Pages (falls Entity schon existiert), erstelle neue falls nötig
4. Setze `[[Wikilinks]]` zu allen verwandten Pages
5. Append-Entry in `00 Wiki/log.md`: `YYYY-MM-DD HH:MM UTC — ingest <source> → N pages updated, M new`
6. Regeneriere `00 Wiki/index.md` (Liste aller Pages + 1-Satz-Summary)

**`query <natural-language-question>`**
1. Read `00 Wiki/index.md` + `00 Wiki/hot.md` zuerst
2. Folge Wikilinks zu relevanten Pages (strukturelle Navigation, nicht similarity-search)
3. Synthetisiere Antwort mit Zitaten `[[page-name#section]]`
4. Bei Gaps: ehrlich sagen „Info liegt nicht im Vault"

**`lint` (monatlich / on-demand)**
1. Dead Wikilinks finden (Target-Page existiert nicht)
2. Orphan-Pages (keine Incoming-Links)
3. Contradictions (gleiche Claim in ≥2 Pages, unterschiedliche Werte)
4. Stale Content (Pages älter als 90 Tage)
5. Report als `reports/vault_lint_YYYY-MM-DD.md`

### Wiki-Page-Template

```markdown
---
title: <Entity/Konzept-Name>
type: entity | concept | tool | person | pattern
tags: [topic1, topic2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [[raw/source-file-name]]
---

## Summary
<1-3 Sätze Kern>

## Details
<strukturiert>

## Related
- [[page-a]] — <warum verwandt>
- [[page-b]] — <warum verwandt>

## History / Log
- YYYY-MM-DD: <ingest X added Y>
```

### Co-Existence mit PARA

W1 legt nur `00 Wiki/index.md` + `00 Wiki/log.md` an. Alte 01-06 bleiben unverändert. W2 beginnt dann, Material aus `04 Ressourcen/` sukzessive in `00 Wiki/` zu extrahieren — aber nicht löschen, sondern cross-linken.

### Referenzen

- Karpathy LLM-Wiki (Konzept-Origin)
- Nate Herk YT R0_R-zZ8p8U (Obsidian-Implementation)
- GitHub-Plugins: `ekadetov/llm-wiki`, `AgriciDaniel/claude-obsidian`, `Pratiyush/llm-wiki`
- Audit-Quelle: `signal_bot/reports/cycle32_obsidian_vault_audit_2026-04-20.md`
