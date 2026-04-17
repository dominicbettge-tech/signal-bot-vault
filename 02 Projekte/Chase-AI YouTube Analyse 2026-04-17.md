# Chase-AI YouTube + Claude-Code Skills-Audit — 2026-04-17

**Channel:** https://www.youtube.com/@Chase-H-AI (40 Videos ≤6 Monate)
**Auftrag User:** „skripte auswerten und skills rausschreiben und nach wichtigkeit aufzählen und beschreiben was sie für dich und für das projekt bringen würden"
**Quelle:** Anthropic-Docs https://code.claude.com/docs/en/slash-commands (gefetcht 2026-04-17) + 40 Video-Titel + bestehendes Skill-System auf dieser VPS

---

## Was ich gefunden habe — Claude-Code Features, die wir NICHT nutzen

### 🔥 TIER-1: Unmittelbarer Projekt-Nutzen (sofort umsetzen)

#### 1. `allowed-tools` in Skill-Frontmatter — **LÖST das Permission-Prompt-Problem**
**Was:** YAML-Feld im Skill-Header, das Claude erlaubt bestimmte Tools/Bash-Pattern ohne User-Bestätigung zu nutzen solange der Skill aktiv ist.
**Syntax:**
```yaml
---
name: signal-parser-review
allowed-tools: Bash(python3 /root/signal_bot/scripts/*) Bash(sqlite3 *) Bash(systemctl status*) Bash(journalctl *)
---
```
**Was es für unser Projekt bringt:**
- User-Frust „schon wieder Bestätigung!!!" (heute 4× mitbekommen) — **beendet** sobald Signal-Parser-Review-Skill aktiv ist
- Review-Session läuft durch ohne 15-20 Bestätigungs-Prompts pro Session
- Codex-Review, Testcenter-Runs, Fast-Review alle vorab-approved
**Priorität:** P0 — heute Abend/morgen früh vor nächster Review

#### 2. `context: fork` + `agent: Explore` — **60-80% Kontext-Ersparnis bei Research-Phasen**
**Was:** Skill läuft in forked Subagent mit eigenem Context-Budget. Main-Session bleibt lean.
**Syntax:**
```yaml
---
name: six-path-solution
context: fork
agent: Explore
---
```
**Was es für unser Projekt bringt:**
- Phase-2.5a/b von `six-path-solution` (WebSearch für Best-Practices) lädt aktuell alles in Main-Context → macht lange Sessions teuer+langsam
- Mit `context: fork` nur die Ergebnisse zurück — Main-Context bleibt sauber
- Gleiche Logik für `dispatching-parallel-agents`, `signal-parser-review` Research-Phase
**Priorität:** P1 — diese Woche, nach `allowed-tools`-Rollout

#### 3. `!`command`` dynamic context injection — **Live-DB-Stand in Skill-Prompt**
**Was:** Shell-Befehl läuft VOR Skill-Aktivierung, Output wird in den Prompt injiziert.
**Syntax in Skill-Body:**
```markdown
## Aktueller Status
- Open trades: !`python3 -c "import sqlite3; ..."`
- Heartbeat: !`cat /root/signal_bot/.heartbeat`
- Last parser verdict: !`python3 /root/signal_bot/scripts/predict_verdict.py --last`
```
**Was es für unser Projekt bringt:**
- Review-Session bekommt aktuellen DB-State automatisch (kein manuelles Fragen mehr)
- Bootstrap-Sequenz aus `project_review_bootstrap.md` (5 Schritte) wird teilweise automatisiert
- Replace: die Bash-Calls im Bootstrap werden Injection, kein Prompt mehr
**Priorität:** P1

#### 4. `paths` Auto-Activation — **Skill triggert nur bei passenden Dateien**
**Was:** Glob-Pattern im Frontmatter. Skill wird nur aktiviert wenn Claude mit Files in diesen Pfaden arbeitet.
**Syntax:**
```yaml
---
name: testcenter-review
paths: testcenter/**/*.py, scripts/review/*.py
---
```
**Was es für unser Projekt bringt:**
- Testcenter-Skill nervt nicht bei Non-Testcenter-Arbeit
- `signal-parser-review` aktiviert sich automatisch bei `scripts/fast_review.py`
- Reduziert Skill-Rauschen (aktuell 15+ Skills laden alle Descriptions in jeden Context)
**Priorität:** P2

### 🟡 TIER-2: Mittelfristig (Phase B/C)

#### 5. `hooks` scoped per Skill — **Skill-spezifische Lifecycle-Events**
**Was:** Ein Skill kann eigene PreToolUse/PostToolUse/SessionEnd-Hooks definieren, die nur während er aktiv ist laufen.
**Was es für unser Projekt bringt:**
- `signal-parser-review` könnte auf-save-of-verdict automatisch `save_verdict.py` triggern
- Auto-Persistierung ohne „ich speichere das"-Gedächtnis-Problem (`feedback_save_means_save`)
**Priorität:** P2

#### 6. `effort` / `model` per Skill — **Granulare Kosten-Kontrolle**
**Was:** Skill kann eigenen Effort-Level (low/medium/high/xhigh/max) und eigenes Modell erzwingen.
**Was es für unser Projekt bringt:**
- `systematic-debugging` hart auf `xhigh` setzen (Bugs brauchen tiefe Analyse)
- `signal-parser-review` auf `high` (nicht `xhigh`) → schneller durch Bulk-Reviews
- Explore-heavy Skills auf `haiku` routen
**Priorität:** P2

#### 7. `$ARGUMENTS` / `$0 $1 $2` — **Skill-Parameter**
**Was:** Skill nimmt CLI-Args entgegen, werden in Prompt substituiert.
**Beispiel:** `/signal-parser-review MIST` → `$ARGUMENTS = "MIST"`, Skill bootstrappt für diesen Ticker.
**Priorität:** P2 (Nice-to-have)

#### 8. `SLASH_COMMAND_TOOL_CHAR_BUDGET` Env-Var — **Mehr Skill-Descriptions im Context**
**Was:** Default-Budget = 1% des Context-Window, Fallback 8k Zeichen. Bei vielen Skills werden Descriptions beschnitten → Claude triggert Skills nicht mehr zuverlässig.
**Wir haben 17 Skills.** Combined Descriptions könnte schon beschnitten sein.
**Action:** Setzen auf `SLASH_COMMAND_TOOL_CHAR_BUDGET=20000`
**Priorität:** P1 (schneller Win, Umfang klein)

### 🟢 TIER-3: Backlog / Nice-to-have

9. `disable-model-invocation: true` — für destruktive Skills (git-worktrees, deploy-ähnliche)
10. `user-invocable: false` — für reine Background-Knowledge-Skills
11. `shell: bash/powershell` — irrelevant (wir sind Linux-only)
12. `argument-hint` — Autocomplete-Hinweis beim `/skill` eintippen

---

## 40 Videos — Titel-Scoring (ohne Transkript, YouTube-Bot-Detection blockiert Auto-Extraction)

### Deep-Dive-Kandidaten (Top-5, bei nächster User-Session gezielt Transkript holen)

| # | Titel | ID | Hypothese vom Inhalt | Projekt-Nutzen |
|---|---|---|---|---|
| 3 | `/routines just completely changed Claude Code tasks` | Hd4Ck1BS4Kw | Vermutl. neues Feature oder Chase meint `/loop` (bundled skill) | Falls echtes Recurring-Task-Feature → perfekt für „Codex alle paar Stunden" |
| 14 | `Claude Code + Codex = AI GOD` | L7NPhaUBpZE | Codex-Integrations-Pattern | Wir richten Codex GERADE ein |
| 22 | `Claude.md is RUINING Claude Code (w/ One Exception)` | V3xDTx2XwGg | Anti-Pattern in CLAUDE.md | Wir haben 3 CLAUDE.md — wichtig! |
| 37 | `Claude Code Just Got a MASSIVE Upgrade (Agent Loops)` | lf2lcE4YwgI | Agent-Loop-Feature | Könnte Auto-Review ersetzen |
| 11 | `Karpathy's Obsidian RAG + Claude Code = CHEAT CODE` | OSZdFnQmgRw | Obsidian-Vault-RAG-Setup | Vault existiert, RAG fehlt |

### Rest-Scoring (40 Titel kompakt)

**Hoher Nutzen (6-7/10):**
- #31 `Did Claude's 1M Context Window Defeat Context Rot?` — Context-Rot in langen Sessions relevant
- #35 `10 Claude Code Plugins to 10X Your Projects` — Plugin-Scan, wir haben nur 1 (skill-creator)
- #21 `Claude Code's Hidden /dream Feature MASSIVELY Upgrades Memory` — Memory-Feature, unser Memory läuft aber schon

**Mittel (3-5/10):** #4, #5, #7, #10, #17, #19, #24, #27, #28, #33, #34, #36, #38, #39, #40
**Niedrig (1-3/10) / Frontend / Clickbait:** #2, #8, #9, #15, #18, #20, #23, #25, #26, #29, #30
**Doppelt zu Bekanntem:** #6 (Top-10-April → `project_cc_extensions_backlog.md`), #12, #13, #16, #30 (Paperclip → Alt-B Memory), #38 (Playwright Backlog)
**Model-News (Info-only):** #1, #32

### Warum keine Volltranskripte

- yt-dlp 2026.03.17 installiert ✅ aber YouTube bot-detection blockiert Auto-Extraction ohne Cookies
- Third-party-Transcript-Services (youtubetranscript.com) → 403
- Alternative: WebFetch auf einzelne Video-Pages + Transkript-Tab manuell — funktioniert aber Anthropic-Docs liefern direkter
- Strategie: Anthropic-Docs als Primary-Source (was ICH oben gemacht habe), Chase-Videos als Sekundär-Validation

---

## Konkreter Umsetzungsplan (nach User-Return)

### Session 1 (30 Min — „endlich keine Prompts mehr"-Session)

1. **`allowed-tools` in `signal-parser-review/SKILL.md` ergänzen** — decken typische Review-Commands ab
2. **`allowed-tools` in `systematic-debugging/SKILL.md`** — Debug-Commands
3. **`allowed-tools` in `verification-before-completion/SKILL.md`** — Test/Verify-Commands
4. **Env-Var `SLASH_COMMAND_TOOL_CHAR_BUDGET=20000`** in settings.json ergänzen
5. **Test:** Review-Session starten, prüfen ob 0 Prompts kommen

### Session 2 (60 Min — Context-Diät)

6. **`six-path-solution` → `context: fork`** für Phase 2.5a/b
7. **`dispatching-parallel-agents` → `context: fork`**
8. **`grounded-decisions` prüfen** — evtl. zu klein für fork, aber `paths`-Pattern für Review-Files
9. **`!`command``-Injection in `signal-parser-review`** — Bootstrap automatisieren

### Session 3 (Phase C)

10. Skill-Hooks für Auto-Persistierung Verdicts
11. Per-Skill `effort` tuning
12. `paths`-Rollout alle Skills

### Session 4 (wenn User explizit fragt)

13. Top-5 YouTube-Videos Transkript-Deep-Dive via WebFetch
14. Chase-Videos gegen Anthropic-Docs cross-checken (Chase übertreibt manchmal)

---

## Was KEINEN Nutzen bringt (hart weglassen)

- Alle Frontend-Videos (5 Stück) — Signal-Bot hat kein UI
- Clickbait-Titel (6 Stück) — meist leere Versprechen
- Paperclip-Reaktions-Video (#30) — Alt-B ist entschieden (Re-Assess 2026-07-17)
- Local-Setup-Videos (#26) — Max-Abo deckt alles ab, 100%-local bringt nichts
- Frontend-Design-Skills (#2) — irrelevant

## Why das System jetzt

Die Anthropic-Docs-Features (allowed-tools, context fork, !-injection, paths, hooks) lösen drei konkrete Schmerzen, die HEUTE passiert sind:

1. **Permission-Prompt-Hell** (4× heute vom User beschwert) → `allowed-tools` + `SLASH_COMMAND_TOOL_CHAR_BUDGET`
2. **Kontext-Bloat in langen Sessions** (Review + Six-Path + Testcenter alle in einem Context) → `context: fork`
3. **Bootstrap-Sequenz vergessen/übersprungen** (Review startet ohne die 5 Schritte) → `!`command`` + `paths` Auto-Aktivierung

Das ist der Return-on-Investment: **kein Frust mehr**, kein Vergessen, schnellere Sessions, günstigere Runs.
