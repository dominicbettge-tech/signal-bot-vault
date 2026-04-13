---
tags: [projekt]
status: aktiv
erstellt: 2026-04-09
---

# Signal Bot v3

## Ziel

Vollautomatischer US-Aktienhandel über IBKR. Liest Signale aus Jack Sparo's Telegram-Kanälen, parsed sie mit Claude, führt Orders über Interactive Brokers aus. Aktuell Paper Trading — nach 2+ Wochen stabiler Performance → Live mit 5k€.

## Stack

- Python, SQLite, asyncio, ib_insync, Telethon
- VPS: Hostinger MK2 (187.124.166.210)
- Services: signal-bot, signal-watchdog, ibgateway

## Status

Paper Trading aktiv. Alle P0-P3 Bugs behoben (Stand 2026-04-09).

## Nächste Schritte

- [ ] 2+ Wochen fehlerfreies Paper Trading
- [ ] Performance auswerten
- [ ] Live-Start vorbereiten

## Bekannte offene Punkte

- GV Ghost-Short: BUY 500 Cover-Order PreSubmitted (füllt bei Marktöffnung)
- Replay-Bug: alte Telegram-Nachrichten bekommen Expiry ab "jetzt" nach Restart
- Separaten Anthropic API-Key für Bot erstellen

## Parser-Bugs (aus Review identifiziert)

1. **Reply-Chain Ticker fehlt** — Parser übergibt Reply-Kontext nicht, Ticker aus Parent-Nachricht geht verloren (durchgehend)
2. **Averaging als update/watchlist** — Nachkäufe ("got another order filled") werden nicht als Averaging erkannt
3. **Kurs-Update als Entry** — "GURE at 11.60" ist Preisinfo, kein Entry (halluzinierter Trade)
4. **Halluzinierte Preise** — VRAX: 0.79/0.70 komplett erfunden
5. **Bedingte Exits als commentary** — "if it gets to X I will sell" nicht als bedingter Exit erkannt
6. **Conditional entries als watchlist** — "might" + konkrete Params (Preis+SL+Expiry) = Entry, nicht Watchlist
7. **Nachrichten ohne Ticker nur durch Zeitkontext zuordenbar** — z.B. "So far moved 12% today" (3973) hat keinen Ticker, kein Reply, gehört aber zu GURE durch zeitlichen Zusammenhang
8. **Reply zeigt auf falschen Ticker** — #3970 replied auf GNS-Nachricht (3962), redet aber über GURE. Parser darf Reply-Ticker nicht blind übernehmen

## Jack's eigene Regeln (aus seinen Nachrichten gelernt)

1. **Kein SL-Exit erwähnt = Position noch offen** — "If I don't say I used the SL that means I still have the position" (ID 3990). Bot darf nicht annehmen dass SL getriggert wurde.
2. **Swing SL = flexibel, wird editiert** — "For swing trade I try to use a flexible SL where I can just edit" (ID 3990). Parser muss SL-Updates bei Swings erwarten.
3. **Day Trade expired → neue Order folgt** — "In day trades when I pick time frame... if my order doesn't fill then I will share new order" (ID 3990). Nach Expiry auf Follow-up warten, nicht sofort Trade schließen.

## Aktive Unterprojekte

- [[Signal Bot Live-Roadmap]] — Master-Arbeitsplan zum Live-Trading (7 Phasen)
- [[Parser Rebuild — Stress Test Phase A]] — aktueller Fokus, Phase A v2 mit Vision-Support läuft
- [[Parser Rebuild — Phase B Review Queue]] — manuelle Review-Queue
- [[Claude Daily Reports]] — geplante Automatisierung: Morning/Evening/Weekly Opus-Reports via @Jacksanalyse_bot (wird nach Parser Rebuild gebaut)

## Notizen

Backtest-Ergebnisse: [[Backtest 2026-04-07]]
Fehler-Historie: siehe [[Signal Bot Fehler-Log]]

## Ideen-Backlog (noch nicht umgesetzt)

### Near-Miss & Watching-Simulation (2026-04-11)
Jack kommuniziert sehr konservativ — drei Muster die der Bot verpasst:
1. **"Watching/Monitor"** — kein Entry-Signal, Kurs läuft +40%, Jack gratuliert nachher den "Mutigen"
2. **Knapper Miss** — Entry $X, Kurs kommt bis $X+2-3cent, läuft dann +40% — Limit-Order nie gefüllt
3. **Impliziter Entry** — "Started small at 5.54 will monitor" = eigentlich ein Entry, aber kein explizites BUY

**Idee:** Simulation einbauen die rückwirkend berechnet was passiert wäre wenn man trotzdem eingestiegen wäre (am Low des Tages oder nächsten Open). Direkt im Review-Tool als Extra-Entscheidung `m` = "Market-Entry simulieren". **Noch nicht gebaut — erst nach Parser Review + Phase 2.**
