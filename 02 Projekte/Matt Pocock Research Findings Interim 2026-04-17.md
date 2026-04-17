# Matt Pocock Research — Interim Findings (vor Transkripten)

**Kontext:** User auf B umgeschwenkt (Supadata API statt Fallback C). Diese Findings aus 8 parallelen WebSearches sind bereits handfest.

## Matt's Public Resources (Gold)

| Resource | URL | Wert für uns |
|---|---|---|
| **Skills Repo (GitHub)** | `github.com/mattpocock/skills` | ⭐⭐⭐ Direkter Quellcode aller 5 Daily-Skills — installierbar via `npx skills@latest add mattpocock/skills/tdd` |
| Blog aihero.dev | `aihero.dev` | ⭐⭐⭐ Artikel-Versionen mehrerer Videos, mehr Tiefe als Tweets |
| X/Twitter @mattpocockuk | — | Kurze Takes, Updates |
| LinkedIn posts | — | Karriere-Pitch, weniger technisch |

## Bestätigte Kern-Aussagen (noch ohne Video-Deep-Dive)

### 1. Matt's Top-5-Skills (Daily)
Direkt aus seinem Tweet (confirmed):
- `/grill-me` — Skeptischer Tech-Lead: verhört DICH bis dein Plan wasserdicht ist (16-50 Fragen)
- `/write-a-prd` — Product Requirements Document mit LLM
- `/prd-to-issues` — Bricht PRD in GitHub-Issues (vertikale Slices)
- `/tdd` — Red-Green-Refactor Skill
- `/improve-codebase-architecture` — Exploriert Codebase auf Kopplungs-Probleme

### 2. CLAUDE.md vs AGENTS.md
Matt's Beef: **Claude Code unterstützt AGENTS.md nicht**, nur CLAUDE.md. Cursor, Codex, Builder.io alle auf AGENTS.md-Standard. Muss doppelt pflegen. Deswegen **bevorzugt er Codex** für seinen CLI-Flow.

→ **Relevanz für uns:** Unser CLAUDE.md-Setup ist nicht verkehrt, aber Matt argumentiert Portabilität. Nicht kritisch für Signal-Bot (Single-Tool-Setup, nicht Multi-Agent).

Zusatz: Matt hat ein Clean-up-Skill für schlechte AGENTS.md/CLAUDE.md (18.01.2026 Post).

### 3. Ralph Wiggum Technique (autonome Loops)
Matt-Zitat: *"Ralph Wiggum + Opus 4.5 is really, really good"*.
Philosophie: *"How it started: Swarms, multi-agent orchestrators, complex frameworks. How it's going: Ralph Wiggum"* (Januar 2026).

**Technik:**
- While-Loop feedet AI-Agent immer wieder dasselbe Prompt bis Stop-Condition
- Exit-Code 2 blockt Claude vom Stoppen, re-injiziert Prompt
- Agent sieht via Git-History/modified-files seinen Progress
- **Anthropic-offizielles Plugin:** `github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md`

**Notable Cases:**
- Geoffrey Huntley: 3 Monate Loop → funktionsfähiger Compiler "Cursed" (Gen-Z-Slang-Golang)
- YC-Hackathon: 6+ Repos über Nacht für ~$297 API-Kosten

→ **Relevanz für uns:** ⭐⭐⭐ Direkt. Passt auf Codex-Review-Queue-Abarbeitung (autonom über Nacht), Parser-Quality-Tuning, Testcenter-Walk-Forward. `schedule`-Skill oder Cron-Wrapper ist unsere Variante davon.

### 4. 7 Phases of AI Development (aihero.dev)
Kein vollständiger 7-Punkt-Abriss gefunden. Bekannte Phasen:
1. Idea refinement (via `/grill-me`)
2. Research (externe Deps, cacht Infos in Repo)
3. PRD + Planning (chunking in Context-Window-große Häppchen)
4. (+4 weitere im Video, nicht öffentlich geschrieben)

→ **Volltext = genau das, was wir mit Supadata transkribieren werden.**

### 5. Plan Mode
Matt (Oktober 2025): *"Without plan mode: code is so bad it's basically a liability. Plan mode: basically as good as I could write it. Indispensable."*

**Subagent-Workflow:**
> Enter plan mode → explicitly say how many subagents → let it rip. Super for research across large repo.

**Plan-Mode-Power-Prompt:**
> "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions"

→ **Relevanz für uns:** ⭐⭐ Wir haben `writing-plans` + `executing-plans`. Matt's Interview-Prompt könnte als zusätzlicher Skill `/grill-me`-Äquivalent taugen. **Kandidat für Skill-Stack-Erweiterung.**

### 6. TDD Skill (Red-Green-Refactor)
**Problem:** LLMs schreiben alle Tests auf einmal, dann Code, der Tests passt — Tests validieren imaginierten Code, nicht echten.

**Matt's Fix:** 3 strikte Phasen
- RED: **EIN** failing test
- GREEN: minimal code nur für diesen Test
- REFACTOR: Nach allen Tests, clean up

**Tracer-Bullets:** vertikale Slices statt horizontal.

**Core-Prinzipien:**
- Tests verifizieren Behavior via public interfaces, NICHT implementation details
- Code darf sich komplett ändern, Tests nicht
- Integration-Style Tests > Unit-Tests von Implementation-Details

Install: `npx skills@latest add mattpocock/skills/tdd`

→ **Relevanz für uns:** ⭐⭐⭐ **Direkt für Parser-Quality-Maximization-Wochenendtask.** Wir haben `test-driven-development` Skill, aber Matt's ist präziser. **Kandidat: klonen + vergleichen.**

### 7. Worktrees
Matt (März 2026): *"claude --worktree is so good I'm making it my new default."*

**Sandcastle-Projekt:**
- Backlog von Issues
- Spawnt N Claudes in Docker-Sandboxes, jede auf eigenem worktree
- Mergt back zu target branch
- Lokal, nur Docker + TS nötig

→ **Relevanz für uns:** ⭐⭐ Wir haben `using-git-worktrees` Skill. Signal-Bot ist Single-Branch (kein Git aktuell sogar), aber für Parser-Experimente gut.

---

## Noch offene Videos (brauchen Supadata-Transkripte)

Ohne öffentliche Summary gefunden:
- "Never Trust An LLM" (14m) — Prinzip, wahrscheinlich generisch
- "Claude Code tried to improve /init... Is it any better?" (11m) — Meta-Test
- "Building a REAL feature with Claude Code: every step explained" (44m) — **längster, wertvollster**
- "Never Run claude /init" (11m) — Anti-Pattern-Details
- "Your codebase is NOT ready for AI (here's how to fix it)" (9m)
- "How to actually force Claude Code to use the right CLI (don't use CLAUDE.md)" (7m) — Alternative?
- "I'm using claude --worktree for everything now" (8m) — Video-Details
- "Ship working code while you sleep (Ralph Wiggum)" (16m) — Implementation-Walkthrough
- "How I use Claude Code for real engineering" (10m) — Workflow-Details
- "Frontend is HARDER for AI than backend" (5m) — Begründung
- "Red Green Refactor is OP With Claude Code" (5m) — Live-Demo
- "Most devs don't understand" × 3 — Foundation

---

## Action Plan nach Supadata-Setup

1. Python-Skript `/root/signal_bot/scripts/yt_transcript.py` bauen — wiederverwendbar für künftige Kanäle (User sagte: „machen wir öfter")
2. 17 Video-IDs batch durchziehen → `/tmp/matt_transcripts/*.txt`
3. Pro Video: 1-2-Sätze-Summary + Scoring nach **Signal-Bot-Relevanz**
4. Finale Empfehlung: welche Matt-Skills in unseren Stack aufnehmen, welche Anti-Patterns vermeiden
5. Update dieser Datei von „Interim" → „Final"
