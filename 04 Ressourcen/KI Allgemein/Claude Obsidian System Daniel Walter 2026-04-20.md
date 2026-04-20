---
tags: [claude, obsidian, workflow]
status: review
date: 2026-04-20
source: https://www.youtube.com/watch?v=R0_R-zZ8p8U
---

# Claude ist jetzt 10x schlauer geworden mit Obsidian — Daniel Walter (KI ohne Team)

## Kernthese
KI wie Praktikant → macht jede Woche die gleichen Fehler. Mit **4 Bausteinen** wird Claude zum vollwertigen Mitarbeiter der nie vergisst.

## Die 4 Bausteine

| # | Baustein | Unser Status | Pfad bei uns |
|:-:|:-|:-|:-|
| 1 | **CLAUDE.md** als Routing-Handbuch (wer bin ich, wie arbeite ich, Regeln) | ✅ vorhanden × 3 | `/root/CLAUDE.md`, `/root/signal_bot/CLAUDE.md`, `/root/obsidian_vault/CLAUDE.md` |
| 2 | **Vault** als Wissensspeicher (Claude liest Kontext) | ✅ vorhanden | `/root/obsidian_vault/` (PARA-Struktur) |
| 3 | **Auto-Write** — Claude schreibt selbst in Vault (Korrekturen werden Regeln, Session-Ende schreibt Log) | ✅ teilweise | Daily Notes aktiv, Memory-System + REGEL 1 erzwingt Daily Journal |
| 4 | **Skills** als SOPs (Prozess einmal zeigen, ab dann 1-Satz-Trigger) | ✅ vorhanden | `/root/.claude/skills/` (20+ Skills) |

**Befund:** Wir sind schon weiter als das Video. Das Video validiert nur den Ansatz.

## Konkrete Lücken (daraus gezogen und behoben 2026-04-20)

1. **Vault-Root war unaufgeräumt** — `signal_bot.log`, `watchdog.log`, `trades.db` (leer) lagen im Root → nach `06 Archiv/_relikte_2026-04-20/` verschoben.
2. **Vault-CLAUDE.md kannte Memory + Skills nicht** — Section *"Parallele Wissens-Systeme (Routing)"* ergänzt. Claude weiß jetzt: Vault = lesbare Notizen, Memory = interne Regeln, Skills = Prozeduren.
3. **Transkript-Archivierung** — diese Notiz hier statt nur `/root/signal_bot/reports/`.

## Zitate zum Merken
- *"Produktivitätssysteme scheitern nicht am Aufbau, sie scheitern an der Wartung."*
- *"Nicht optimieren, einfach anfangen."*
- *"Das System wird jeden Tag besser, weil du damit arbeitest."*

## Was wir NICHT übernehmen
- Daniels Ordnerstruktur-Prompt (5 Fragen → generierte Struktur). Unsere PARA-Struktur ist schon lebend und gewachsen — refaktorieren wäre Arbeit ohne Mehrwert.

## Quelle
Transkript voll: `/root/signal_bot/reports/yt_transcript_R0_R-zZ8p8U.md`
