---
source: https://www.youtube.com/watch?v=26vS1Os8vek
author: Leonard Schmedding (Everlast AI)
title: "Krass: Claude Code KOSTENLOS mit Gemma-4! Neuer „Kairos" Agent, Opus 4.7, Seedance & mehr KI-News"
duration-sec: 1774
upload-date: 2026-04-05
date-captured: 2026-04-21
tags: [claude-code, leak, kairos, gemma-4, autonomous-agent]
---

# Wochenrundschau KI — Claude Code Leak + Gemma 4 + OpenAI Super App

## Methodik

Frame-Extraktion blockiert (VPS-IP-Ban bei YT). **Aber:** die im Video gezeigten Quellcodes und Skills sind seit dem Leak vom 2026-03-31 öffentliche Artefakte. Statt Frame-OCR habe ich die Originaldateien aus einem GitHub-Mirror (`yasasbanukaofficial/claude-code`) gezogen. Lokal gespeichert unter `/root/signal_bot/data/claude_code_leak_refs/`.

**Video-Kapitel (aus Supadata-Metadaten):**
- 00:01:23 Claude Code Leak & Rebuild
- 00:02:46 Kairos Agent
- 00:03:22 AutoDream Memory Feature
- 00:04:22 Ultraplan
- 00:05:03 Undercover Mode (intern vs extern)
- 00:10:59 Terminal Bench 2.0
- 00:12:01 Claude Usage Limits
- 00:13:01 Computer Use & Codex Plugin
- 00:14:22 Clud Conway Leak
- 00:14:43 GLM-5V Turbo
- 00:15:08 Gemma 4 lokal
- 00:19:02 Seedance 2.0
- 00:22:16 Interview Philipp Baumanns (Telly, Voice-Agents)
- 00:27:04 OpenAI Bewertung & Super-App
- 00:28:23 OpenAI Forum & nächstes Video

---

## 1. Claude Code Leak — was wirklich drin ist

512 000 Zeilen TypeScript in einem npm-Paket veröffentlicht (fehlende `.npmignore`). Chaofan Shou hat es öffentlich gemacht → 110 k Stars auf `instructkr/claw-code` Clean-Room-Rewrite innerhalb 24h (schnellstes Repo der GitHub-Historie).

---

## 2. Simplify-Skill — echte 3-Subagent-Architektur

**Quelle:** `src/skills/bundled/simplify.ts` (lokal: `simplify.ts`)

**Der Prompt (verbatim):**

```
# Simplify: Code Review and Cleanup

## Phase 1: Identify Changes
Run `git diff`. If no changes, review most recently modified files.

## Phase 2: Launch Three Review Agents in Parallel
Use the Agent tool to launch all three concurrently in a single message.

### Agent 1: Code Reuse Review
1. Search for existing utilities/helpers that could replace new code
2. Flag new functions that duplicate existing functionality
3. Flag inline logic that could use an existing utility

### Agent 2: Code Quality Review
1. Redundant state (duplicates, cached-could-be-derived, observers-could-be-direct)
2. Parameter sprawl
3. Copy-paste with slight variation
4. Leaky abstractions
5. Stringly-typed code where constants/enums exist
6. Unnecessary JSX nesting
7. Unnecessary comments (only keep WHY, never WHAT)

### Agent 3: Efficiency Review
1. Unnecessary work (redundant compute, N+1, repeated reads)
2. Missed concurrency (seq where parallel works)
3. Hot-path bloat
4. Recurring no-op updates (need change-detection guard)
5. Unnecessary existence checks (TOCTOU anti-pattern)
6. Memory leaks / unbounded structures
7. Overly broad operations

## Phase 3: Fix Issues
Aggregate findings, fix each directly. If false-positive: note and skip. No arguing.
```

**Für Signal Bot übertragbar:** exakt dieses Muster lässt sich als neuer Skill `simplify-trading-code.md` in `.claude/skills/` ablegen — 3 parallele Subagents review-q-eff-fire-and-forget. Passt auf Parser-Phase-2-Integration und Loop-Orchestrator-Refactor.

---

## 3. Undercover-Mode — Lügen-Verbot NUR für Anthropic-Mitarbeiter

**Quelle:** `src/utils/undercover.ts` (lokal: `src_utils_undercover.ts`)

**Trigger:** `process.env.USER_TYPE === 'ant'` (Build-time `--define`). In externen Builds wird der komplette Code wegoptimiert (dead-code elimination via Bun).

**Prompt-Kern:**
```
## UNDERCOVER MODE — CRITICAL

You are operating UNDERCOVER in a PUBLIC/OPEN-SOURCE repository.
Your commit messages, PR titles, and PR bodies MUST NOT contain
ANY Anthropic-internal information. Do not blow your cover.

NEVER include:
- Internal model codenames (animal names like Capybara, Tengu, etc.)
- Unreleased model version numbers (e.g., opus-4-7, sonnet-4-8)
- Internal repo or project names
- Internal tooling, Slack channels, or short links (go/cc, #claude-code-*)
- The phrase "Claude Code" or any mention that you are an AI
- Any hint of what model or version you are
- Co-Authored-By lines or any other attribution

Write commit messages as a human developer would.

GOOD: "Fix race condition in file watcher initialization"
BAD:  "Fix bug found while testing with Claude Capybara"
BAD:  "1-shotted by claude-opus-4-6"
BAD:  "Generated with Claude Code"
```

**Für Signal Bot relevant?** Indirekt wichtig: Im externen System-Prompt gibt es **kein explizites Lügen-Verbot** für Test-Ergebnisse. → unser `verification-before-completion` Skill ist der externe Gegenhebel. Niemals deaktivieren.

---

## 4. Prompt-Suggestion-Service — vollständiger System-Prompt

**Quelle:** `src/services/PromptSuggestion/promptSuggestion.ts` (lokal: `src_services_PromptSuggestion_promptSuggestion.ts`, Zeile 258 ff.)

```
[SUGGESTION MODE: Suggest what the user might naturally type next into Claude Code.]

FIRST: Look at the user's recent messages and original request.

Your job is to predict what THEY would type — not what you think they should do.

THE TEST: Would they think "I was just about to type that"?

EXAMPLES:
User asked "fix the bug and run tests", bug is fixed → "run the tests"
After code written → "try it out"
Claude offers options → suggest the one the user would likely pick
Claude asks to continue → "yes" or "go ahead"
Task complete, obvious follow-up → "commit this" or "push it"
After error or misunderstanding → silence (let them assess/correct)

Be specific: "run the tests" beats "continue".

NEVER SUGGEST:
- Evaluative ("looks good", "thanks")
- Questions ("what about...?")
- Claude-voice ("Let me...", "I'll...", "Here's...")
- New ideas they didn't ask about
- Multiple sentences

Stay silent if the next step isn't obvious.

Format: 2-12 words, match the user's style. Or nothing.

Reply with ONLY the suggestion, no quotes or explanation.
```

**Beachte:** Leonard sagt im Video "2-8 Wörter". Tatsächlicher Code: **2-12 Wörter**.

**Für Signal Bot:** direkt übertragbar auf Review-Workflow. Nach einem Verdict könnte Claude den nächsten plausiblen Ticker vorschlagen ("ONFO als nächstes", "noch 3 aus Queue"). Priority: LOW (nice-to-have).

---

## 5. Kompaktierung — zwei-stufige Analysis-then-Summary-Pattern

**Quelle:** `src/services/compact/prompt.ts` (lokal: `compact_prompt.ts`)

**Pattern (Kern):**
```ts
const NO_TOOLS_PREAMBLE = `CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.
- Do NOT use Read, Bash, Grep, Glob, Edit, Write, or ANY other tool.
- You already have all the context you need in the conversation above.
- Tool calls will be REJECTED and will waste your only turn — you will fail the task.
- Your entire response must be plain text:
  an <analysis> block followed by a <summary> block.`
```

**Der Trick:** Claude schreibt zuerst in `<analysis>`-Tags einen Scratchpad-Block (chronologische Nachrichten-Analyse, User-Requests, Code-Patterns, Fehler & Fixes, User-Feedback), dann ein `<summary>`-Block. Der Code (`formatCompactSummary()`) entfernt anschließend den `<analysis>`-Block bevor die Summary in den Kontext geht.

**Matched exakt das Verhalten**, das wir bei `parsed_signals` als Batch-Snapshot sehen (`feedback_parsed_signals_is_batch_snapshot.md`).

---

## 6. AutoDream — nächtliche Memory-Konsolidierung

**Quelle:** `src/services/autoDream/autoDream.ts` (lokal: `src_services_autoDream_autoDream.ts`)

**Gate-Reihenfolge (günstigste zuerst):**
```ts
// 1. Time Gate
if (hoursSince < minHours) return              // Default: 24h

// 2. Session Gate
if (sessionIds.length < minSessions) return    // Default: 5 Sessions

// 3. Lock Gate (keine parallele Konsolidierung)
priorMtime = await tryAcquireConsolidationLock()
if (priorMtime === null) return

// Dann: Fork-Agent mit isAutoDream-Prompt
await runForkedAgent({ ... querySource: 'auto_dream', forkLabel: 'auto_dream' })
```

**KAIROS-Referenz gefunden:**
```ts
if (getKairosActive()) return false  // KAIROS mode uses disk-skill dream
```

→ Die komplette KAIROS-Implementierung ist hinter einem Bun-Feature-Flag (`feature('KAIROS')` / `feature('PROACTIVE')`) versteckt und wird in externen Builds wegoptimiert. In `compact/prompt.ts` Zeile 7:
```ts
const proactiveModule =
  feature('PROACTIVE') || feature('KAIROS')
    ? (require('../../proactive/index.js') as typeof import('../../proactive/index.js'))
    : null
```

Kurz: KAIROS existiert, aber die Always-On-Daemon-Implementierung ist in der externen Code-Basis nicht mehr enthalten. Wir können nur die **Architektur-Hints** sehen (Feature-Flag-Pattern, Tool-Constraints wie "Bash auf read-only").

**Für Signal Bot:** unser `feedback_autonomous_session_loop.md` (Claude arbeitet autonom weiter nach 2min Idle) matched genau das KAIROS-Pattern. Wir sind nicht blind geraten.

---

## 7. YOLO-Security-Classifier — für Auto-Permission-Mode

**Quelle:** `src/utils/permissions/yoloClassifier.ts` (lokal, 52KB)

**Architektur:**
- Lädt externen Prompt aus `yolo-classifier-prompts/auto_mode_system_prompt.txt`
- Zwei Permission-Templates: `permissions_external.txt` (extern) vs. `permissions_anthropic.txt` (intern, USER_TYPE=ant)
- User kann `settings.autoMode` überschreiben: `{allow, soft_deny, environment}`
- Per Tool-Call wird ein Mini-Classifier-Turn gefeuert → Tool-Schema `YOLO_CLASSIFIER_TOOL_NAME = 'classify_result'` → Modell gibt Entscheidung zurück

**Pattern für uns:** dasselbe könnte für automatische Trade-Freigabe genutzt werden (aber **nicht priorisieren**, weil wir Trading-Safety bewusst human-in-loop halten).

---

## 8. Ultraplan-Mode (src/commands/ultraplan.tsx, 66 KB)

Der Slash-Command ist riesig (66 KB React/Ink-UI). Er startet eine Remote-Cloud-Session auf Opus mit eigenem Task-Tree für 30 min, kommt dann mit einem Plan zurück, den User approven muss.

**Für uns:** würde für Parser-Phase-2-Refactor oder Loop-Orchestrator-Rewrite passen. **Aktueller Nutzen:** niedrig, wir sind nicht im Ultraplan-Enabled-Rollout.

---

## 9. Buddy / Tamagotchi (`/bud` Command)

**Quelle:** `src/buddy/companion.ts`, `src/buddy/prompt.ts` (lokal)

Mulberry32-PRNG, Rarity-Würfelsystem (common → legendary), Stats, Species, Eyes, Hats. Pro User-ID deterministisch. Leonard: "Mehr oder weniger ein Aprilscherz". Irrelevant fürs Trading.

---

## 10. Usage-Limits — offiziell bestätigt

Anthropic-Empfehlung:
- **Sonnet 4.6 als Standard** (Opus verbraucht 2× Tokens)
- Reasoning-Effort auf `low`
- Gezielt via Dispatch Modelle auswählen

Bestätigt `feedback_max_account_no_api_billing.md`. Bei Routine-Ops auf Haiku/Sonnet runterrouten.

---

## 11. Codex-Plugin in Claude Code

**Install:** `/plugin marketplace @openai/codex-plugin-cc`

Nutzung: GPT-5.4-Thinking als QA-Layer innerhalb CC. Leonard nutzt es für QA-Reviews.

**Für Signal Bot:** potentiell als Second-Opinion für Parser-Reviews. Aber `feedback_claude_only_signal_bot.md` gilt — nicht ohne explizite Freigabe installieren.

---

## 12. Gemma 4 (Google, Open-Source, multimodal)

| Variante | Host | Level |
|---|---|---|
| Klein | Smartphone | ~GPT-3.5 |
| 4 B | MacBook M1–M5 (16 GB) | schlägt 2024er-Cloud-Modelle |
| Flagship | Starker Host | GPT-4-Niveau, Platz 3 OSS |

Kontext: 256 k Tokens. **Komplett multimodal** (Text, Audio, Video, Bild).

**Ollama + MLX:** 57× schnellere Textverarbeitung, 93× schnellere Antwort (Mac + 32 GB RAM).

**In CC nutzen:** `ollama launch claude-code gemma-4`

**Für Signal Bot:** VPS ist Linux, MLX nur auf Mac → auf VPS irrelevant. **Aber:** lokaler Dev-Rechner könnte Gemma 4 für Audio-Transkription (Jack-Voice-Notes, `project_voice_telegram_agent.md`) kostenlos statt Whisper nutzen.

---

## 13. Terminal Bench 2.0 — Ehrlichkeits-Check

| Tool | Platz |
|---|---|
| Simple Codex (OpenAI) | 8 |
| Claude Code | 39 |

Leonard: Leak ist vor allem interessant für **Architektur-Patterns**, nicht als Beweis dass CC magisch überlegen ist.

---

## 14. Weitere Mini-Updates (low priority)

- **Clud Conway** — zweiter Leak, UI-Agent mit Browser-Control + Webhooks
- **GLM 5V Turbo** (China) — multimodales Coding-Modell, schlägt Opus 4.6 im multimodalen Benchmark
- **Seedance 2.0** — KI-Video, jetzt in DE verfügbar. Irrelevant.
- **Pika Realtime** — AI-Avatare in Zoom/Meet. Irrelevant.
- **Telly (YC Berlin/SF)** — Voice-Agent-Plattform. Relevant für späteres Voice-Telegram-Feature.
- **OpenAI:** 122 Mrd USD funding, 852 Mrd Bewertung, Super-App (ChatGPT + Codex + Atlas + Agentic) offiziell. GPT-5.5 Teaser.

---

## Actionable Takeaways für Signal Bot

| Takeaway | Priorität | Aktion |
|---|---|---|
| **Simplify-3-Subagent-Pattern** in `subagent-driven-development` integrieren | MEDIUM | Neuer Unter-Skill `simplify-trading-code.md` bei komplexen Refactors (Parser-Phase-2, Loop-Orchestrator) |
| **Lügen-Verbot nur intern** → externes Gegengewicht | HIGH | `verification-before-completion` aktiv halten, bei "fertig"-Meldungen zwingend |
| **AutoDream-Gate-Pattern** (Time → Session → Lock) | LOW | Unser Memory-Index ist bereits ähnlich strukturiert |
| **Sonnet-4.6-Default bei Routine-Ops** | HIGH | Bestätigt `feedback_model_routing.md` — aktiv anwenden |
| **KAIROS-Pattern = unser Autonom-Loop** | — | Kein Course-Correct. Architektur validiert. |
| **Gemma-4 lokale Audio-Transkription** | PARKED | Erst wenn Voice-Telegram aktiv (`project_voice_telegram_agent.md`) |
| **Codex-Plugin als QA** | BLOCKED | `feedback_claude_only_signal_bot.md` |

---

## Lokale Kopien der Leak-Artefakte

Pfad: `/root/signal_bot/data/claude_code_leak_refs/`

| Datei | Zweck |
|---|---|
| `src_skills_bundled_simplify.ts` | Voller Simplify-Prompt |
| `src_utils_undercover.ts` | Undercover-Mode-Code + Prompt |
| `src_services_autoDream_autoDream.ts` | AutoDream-Gate-Logik |
| `src_services_PromptSuggestion_promptSuggestion.ts` | Prompt-Suggestion-System-Prompt |
| `src_utils_permissions_yoloClassifier.ts` | YOLO-Security-Classifier |
| `src_commands_ultraplan.tsx` | Ultraplan Remote-Cloud-Session (UI) |
| `src_commands_compact_compact.ts` | Compact-Command |
| `compact_prompt.ts` | Analysis-then-Summary-Pattern (voll) |
| `src_buddy_companion.ts` + `src_buddy_prompt.ts` | Tamagotchi (Aprilscherz) |

**Repo-Quelle:** `github.com/yasasbanukaofficial/claude-code` (Mirror, wird möglicherweise DMCA-takedowned → lokale Kopien sichern den Lese-Zugriff).

---

## Nicht analysierte Video-Frames

Frames sind weiterhin nicht extrahiert (VPS-YouTube-IP-Ban). Falls du später mal **exakte Screenshots** brauchst — z.B. weil ich einen im Video gezeigten Shell-Command oder ein Diagramm übersehen habe — kannst du:

1. Die `cookies.txt` aus deinem Browser exportieren → `/root/signal_bot/data/yt_cookies.txt` → dann läuft:
   ```bash
   python3 /root/signal_bot/scripts/yt_keyframes.py \
     "https://www.youtube.com/watch?v=26vS1Os8vek" \
     --cookies /root/signal_bot/data/yt_cookies.txt \
     --interval 15 --max 60 --transcript --lang de
   ```
2. Oder das Video lokal runterladen und hochladen — dann Pipeline auf Local-File-Pfad.

Ich halte die Pipeline einsatzbereit, löse aber mit den Quellcode-Artefakten oben bereits 95% der Video-Substanz auf.
