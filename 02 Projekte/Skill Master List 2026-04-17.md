---
tags: [skills, roadmap, wochenende]
created: 2026-04-17
review_date: 2026-04-18
---

# Skill & Transkript Master-Liste — 2026-04-17

Konsolidierte Übersicht aller heute analysierten YouTube-Transkripte + daraus extrahierter Skills. Markiert was schon im System ist, sortiert Offenes nach Score.

**Scoring-Kriterien (1-10, höher = wichtiger):**
- **P** = Profit-Hebel für Signal-Bot (direkt auf Bankroll)
- **Q** = Qualität (Code/Entscheidungs-Robustheit)
- **E** = Effort-to-install (invertiert: hoch = leicht)
- **Score** = (P×3 + Q×2 + E) / 6

---

## A — Heute transkribiert (8 Videos)

| ID | Thema / Kanal | Score | Status |
|---|---|---|---|
| lH5wrfNwL3k | Samin Yasar — Claude Stock Trading (CapitolTrades + Wheel Options) | 8.5 | ✅ extrahiert (2 Wochenend-Projekte) |
| Nl43duXzPhM | AI LABS — „Skills are the future" (Anthropic-Prediction) | 7.0 | ⏸ nur gescannt, Deep-Dive offen |
| alSAEkHP0tk | Chase-AI — CC Power-Features „10%-Usage" | 7.5 | ✅ 8 Features in `project_claude_code_power_features_2026_04_17.md` |
| JkrH3ftxPYc | Matt Pocock — Automation-Lifecycle (Ralph-Wiggum Pattern) | 9.0 | ✅ `codex_queue_loop.sh` + `grill-me` Skill |
| LjHkf0pxrYc | AI-Prompting-Workflow (generisch) | 4.0 | ❌ nicht relevant für Signal-Bot |
| hgBrznchTd4 | AI-Business „$10k/month" | 2.0 | ❌ nicht Signal-Bot-Scope |
| vrPCr72Z1bY | Claude-Code für Non-Coder | 3.0 | ❌ Zielgruppen-Mismatch |
| x3RCe4Xefdg | „60 days Andrew Case-Study" | 2.0 | ❌ Marketing |

**Netto-Signal heute:** 4 von 8 Videos haben verwertbare Patterns geliefert.

---

## B — Heute implementiert ✅ (9 Artefakte)

| # | Skill/Artefakt | Pfad | Quelle | P | Q |
|---|---|---|---|---|---|
| 1 | `wrap-up` Skill | `/root/.claude/skills/wrap-up/SKILL.md` | Jack Roberts NotebookLM | 5 | 9 |
| 2 | `grill-me` Skill | `/root/.claude/skills/grill-me/SKILL.md` | Matt Pocock Adversarial-Pre-Mortem | 6 | 9 |
| 3 | `scope` Skill | `/root/.claude/skills/scope/SKILL.md` | Samin Yasar 5-Phasen-Lifecycle | 5 | 9 |
| 4 | `codex_queue_loop.sh` | `/root/signal_bot/scripts/codex_queue_loop.sh` | Matt Pocock Ralph-Wiggum | 7 | 8 |
| 5 | DOE-Struktur `parser_quality/` | `/root/signal_bot/projects/parser_quality/` | Samin DOE-Pattern | 6 | 7 |
| 6 | `allowed-tools` Frontmatter Retrofit | 4 Skills (brainstorming, six-path, writing-plans, executing-plans) | Chase-AI Power-Features | 4 | 8 |
| 7 | `project_capitol_trades_stream.md` | Memory | Samin lH5wrfNwL3k | 8 | 5 |
| 8 | `project_wheel_options_strategy.md` | Memory | Samin lH5wrfNwL3k | 8 | 5 |
| 9 | `project_mem0_install_deferred.md` | Memory (deferred) | Samin Context-Engineering | 6 | 7 |

**Implementations-Rate heute: 9/9 der geplanten Artefakte = 100%.**

---

## C — Installations-Kandidaten (Backlog, nach Score sortiert)

| Rank | Kandidat | Score | Effort | Quelle | Nächster Schritt |
|---|---|---|---|---|---|
| 1 | ~~**Mem0 MCP (Node 20 Upgrade)**~~ | 8.2 | ~~20 min~~ | Samin lH5wrfNwL3k | ✅ **DONE 2026-04-17 Abend** — stdio-lokal statt Smithery-Gateway, 9 Tools, `project_mem0_install_done.md` |
| 2 | **CapitolTrades-Scraper + Paper-Acc** | 7.8 | 1 Tag | Samin lH5wrfNwL3k | ⏰ Wochenende (Plan in `project_capitol_trades_stream.md`) |
| 3 | **Wheel-Bot MVP** | 7.5 | 2 Tage | Samin lH5wrfNwL3k | ⏰ Wochenende (Plan in `project_wheel_options_strategy.md`) |
| 4 | **`context: fork` auf six-path + parallel-agents** | 7.2 | 15 min | Chase-AI P1 | wartet auf User-Go (verändert Skill-Semantik) |
| 5 | **`!`cmd`` Bootstrap-Injection in signal-parser-review** | 7.0 | 20 min | Chase-AI P1 | wartet auf User-Go (Shell-Risiko) |
| 6 | **`paths:` Glob Auto-Activation** | 6.0 | 30 min | Chase-AI P2 | Trigger: Skill-Rauschen spürbar |
| 7 | **Deep-Dive Nl43duXzPhM (AI LABS Skills-Future)** | 5.5 | 30 min | AI LABS | Transkript vorhanden, nur lesen+extrahieren |
| 8 | **Skill-scoped `hooks:`** | 5.5 | 45 min | Chase-AI P2 | nach Voice-Agent (Auto-Persist Verdicts) |
| 9 | **`effort:` + `model:` per Skill** | 5.0 | 15 min | Chase-AI P2 | bei Token-Druck re-evaluieren |
| 10 | **`$ARGUMENTS` Parametrierung** | 4.8 | 20 min | Chase-AI P2 | bei CLI-Skill-Bau (Wheel-Bot?) |

---

## D — Bereits im System (nicht heute, Referenz)

**17 Skills aktiv:** brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, grill-me ✨, grounded-decisions, receiving-code-review, requesting-code-review, scope ✨, signal-parser-review, six-path-solution, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, wrap-up ✨, writing-plans, writing-skills

**✨ = heute hinzugefügt (3 von 17 = 18% Zuwachs heute)**

**Bundled / entdeckt (nicht installiert, nächste Session testen):**
- `less-permission-prompts` — scannt Transkripte + allowlist (Session-Restart-Kandidat)
- `loop` — `/loop 5m /foo` recurring (Codex-Review-Cron-Kandidat)
- `schedule` — Cron-like scheduled remote agents
- `claude-api` — API-App-Building (Caching-Migration)

---

## E — Qualitäts-Steigerungs-Roadmap

**Phase-1 (Wochenende 2026-04-18/19):**
1. Mem0 MCP installieren → Voice-Agent + Codex + CC geteilter Memory
2. CapitolTrades-Paper-Test starten (60-90 Tage Outcome-Gate)
3. Wheel-Bot-MVP auf TSLA (8-Wochen-Zyklus)
4. Deep-Dive Nl43duXzPhM Transkript (Skills-Future-Vision)

**Phase-2 (Session 2 nach Restart):**
5. `context: fork` auf six-path + parallel-agents (User-Go einholen)
6. `!`cmd``-Injection auf signal-parser-review Bootstrap (User-Go einholen)
7. less-permission-prompts Skill testen

**Phase-3 (nach 7-Tage-Evidence):**
8. paths:-Glob + hooks: wenn Reibungspunkte dokumentiert
9. effort:/model: wenn Token-Usage-Metrik zeigt das es lohnt

**Kill-Kriterium:** Jeder Skill ohne 3× Einsatz in 14 Tagen wird dekommissioniert (Anti-Bloat-Regel).

---

## F — Wochenend-Reminder (explizit vom User angefordert)

**Samstag 2026-04-18 Morgen:** Diese Liste lesen. Starte mit Rank-1 (Mem0 Install) → Rank-2 (CapitolTrades) → Rank-3 (Wheel-Bot).

Reminder gesetzt in:
- Daily Note `2026-04-18.md` (Sektion „Wochenend-Tasks aus Master-Liste")
- Memory: `project_weekend_master_list_2026_04_18.md`

---

## G — Was NICHT gemacht wird (Scope-Begrenzung)

- ❌ Videos LjHkf0pxrYc / hgBrznchTd4 / vrPCr72Z1bY / x3RCe4Xefdg — nicht Signal-Bot-relevant
- ❌ Trigger.dev Cloud-MCP-Deployment — Kosten-Argument offen
- ❌ Umbau bestehender Skills auf DOE-Struktur — erst wenn Scope ≥3 Module
- ❌ R-Regel-Automation via hooks: — erst nach Voice-Agent-Integration

---

**Stand:** 2026-04-17 spät
**Next-Touch:** 2026-04-18 (Wochenend-Tasks)
**Owner:** Dominic + Claude-Code (kollaborativ)
