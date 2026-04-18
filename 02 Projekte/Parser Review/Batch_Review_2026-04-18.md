# Batch-Review 2026-04-18

**Anleitung:** Default = ✅ (vorausgefüllt). Haken ENTFERNEN = rejecten/override. Zeile ändern wenn spot-fix. Danach speichern, ich parse zurück.

---

## Section A — Neue Ticker bestätigen (19 Einträge)

Default: Checkbox ✅ = als Ticker speichern. Uncheck = FP, Row bleibt NULL-ticker.

- [x] **#1** msg=3481 → `COOT`  *'I am watching that move in COOT Stock. The volume is neutral so far The price action is bu'*
- [x] **#2** msg=3542 → `OLMA`  *'OLMA got a sell off due to some news. The news itself not too bad regardless I placed a pr'*
- [x] **#3** msg=3543 → `AZTR`  *'AZTR low float got some news and it is moving. I am watching for a possible trade'*
- [x] **#4** msg=3549 → `LAC`  *'LAC I might share a swing trade plan soon for it'*
- [x] **#5** msg=3624 → `RECT`  *'RECT  News  I am watching for a trade'*
- [x] **#6** msg=3673 → `INTS`  *'I am watching all market activities . I saw some stocks moving but today I was mainly focu'*
- [x] **#7** msg=3676 → `HKD`  *'HKD is an interesting spot so far today. But it is a high float with some risky warrants. '*
- [x] **#8** msg=3775 → `IVDA`  *'I am watching the current action in IVDA They got news The volume is increasing  Price act'*
- [x] **#9** msg=4025 → `AFJK`  *'AFJK Omg 1000% mover… Crazy day team.'*
- [x] **#10** msg=4047 → `CAMP`  *'CAMP from October email cross the project target above 5 congrats whoever got it back then'*
- [x] **#11** msg=4081 → `TLRY`  *'Good evening my team. I honestly don’t see anything worth the risk AH tonight. Most likely'*
- [x] **#12** msg=4188 → `PRPH`  *'Good morning my great team . So far PRPH pre market mover with a small price tags. I am wa'*
- [x] **#13** msg=4398 → `SKYQ`  *'Good afternoon 🌞 my great team. I am watching current market activities carefully. SKYQ I '*
- [x] **#14** msg=5015 → `RITR`  *'RITR is moving pre market with some news! The stock got around 66 M float! So it will need'*
- [x] **#15** msg=160 → `SRTS`  *'Good morning 🌞 my great team here. SRTS Might be  in my trading plan for today and next we'*
- [x] **#16** msg=5183 → `ALUR`  *'Placed me an order for day trade at ALUR 1.67~1.69 valid for 10 minutes. I am planning to '*
- [x] **#17** msg=5329 → `IBO`  *'Good evening my great team. I am watching the current move in IBO Not trading yet as I pre'*
- [x] **#18** msg=5371 → `LGVN`  *'LGVN interested move Might share a trade soon .'*
- [x] **#19** msg=497 → `VNDA`  *'VNDA is moving AH in case any have it team. I shared it before in my email group and I am '*

---

## Section B — Divergent Multi-Ticker-Verdicts (35 Messages, je 103 Ticker-Zeilen)

Für jede Ticker-Zeile: **Verdict-Code ins Feld schreiben** (b/e/x/s/w/n/u). Default leer = muss gesetzt werden.

### B#1 msg=3482
> OCGN took out little more profit at 1.68 for the swing left the rest. SLS still holding 80% of what I got yesterday at 1.89 .

- [ ] Ticker **OCGN** [hold,sell] → Verdict: ___
- [ ] Ticker **SLS** [hold] (clone 1003482) → Verdict: ___

### B#2 msg=3595
> Have a wonderful night my great team. So far  OMEX OMER Balanced around good support  OMEX by the way got to 2.70 AH tonight. LAES I will most likely add more tomorrow if it gets to below 5 I will kee

- [ ] Ticker **OMEX** [praise] → Verdict: ___
- [ ] Ticker **OMER** [praise] (clone 1003595) → Verdict: ___
- [ ] Ticker **LAES** [buy,status] (clone 2003595) → Verdict: ___

### B#3 msg=3599
> In day trade there are few spots am watching. BENF might be one of them VTYX So far those two

- [ ] Ticker **BENF** [watch] → Verdict: ___
- [ ] Ticker **VTYX** [] (clone 1003599) → Verdict: ___

### B#4 msg=3610
> OMER OMEX still in my hold with Half of what I got on Wednesday of LAES. Again LAES it’s self part of my long term so I have special plans for those trades .

- [ ] Ticker **OMER** [hold] → Verdict: ___
- [ ] Ticker **OMEX** [hold] (clone 1003610) → Verdict: ___
- [ ] Ticker **LAES** [] (clone 2003610) → Verdict: ___

### B#5 msg=3833
> SMX KTTA  both mentioned in our group  Both did good in the day trade season. I am watching few other stocks for possible nice swing will share soon 🔜

- [ ] Ticker **SMX** [praise] → Verdict: ___
- [ ] Ticker **KTTA** [praise,watch] (clone 1003833) → Verdict: ___

### B#6 msg=3858
> So far the top two we shared here QTTB full success trade  AHMA also I said it is in the top list so far almost 200% .

- [ ] Ticker **QTTB** [status] → Verdict: ___
- [ ] Ticker **AHMA** [] (clone 1003858) → Verdict: ___

### B#7 msg=3906
> PLRZ Still the top mover pre market but if you all noticed the volume still weaker than usual. I might share a trade idea about it soon . Another trade idea : NDRA stock got some data today and honest

- [ ] Ticker **PLRZ** [hold] → Verdict: ___
- [ ] Ticker **NDRA** [] (clone 1003906) → Verdict: ___

### B#8 msg=3992
> TWG closed that last trade with small profit . Still holding GURE so far the only hold from today trades.

- [ ] Ticker **TWG** [hold,sell] → Verdict: ___
- [ ] Ticker **GURE** [hold] (clone 1003992) → Verdict: ___

### B#9 msg=4059
> Congrats for anyone traded BBGI team. Hard luck for that POM but again we focus on the overall results not stopping at one stop as the money train will keep moving ✅.

- [ ] Ticker **BBGI** [praise] → Verdict: ___
- [ ] Ticker **POM** [] (clone 1004059) → Verdict: ___

### B#10 msg=4069
> Again  Team. Stocks like GURE I only trade for short swing range. While stocks like  NDRA VSTM SLS  GEVO ..and others  those like a glue stick in my 😁. So each stock got their story I am sure you agre

- [ ] Ticker **GURE** [praise] → Verdict: ___
- [ ] Ticker **NDRA** [] (clone 1004069) → Verdict: ___
- [ ] Ticker **VSTM** [] (clone 2004069) → Verdict: ___
- [ ] Ticker **SLS** [] (clone 3004069) → Verdict: ___
- [ ] Ticker **GEVO** [] (clone 4004069) → Verdict: ___

### B#11 msg=4119
> So far two days trades successfully done With RADX MASK I  am watching the activities in AMCI but the volume there looks weak. Will see if it will get any better

- [ ] Ticker **RADX** [watch] → Verdict: ___
- [ ] Ticker **MASK** [watch] (clone 1004119) → Verdict: ___
- [ ] Ticker **AMCI** [] (clone 2004119) → Verdict: ___

### B#12 msg=4161
> PCSA Halted up  It may be a day trade target . MIST  Averaged more at 2.03 Final average order for this week for me 1.89 I will hold from here and see how it goes  Yesterday it got to 2.58 that’s why 

- [ ] Ticker **PCSA** [status] → Verdict: ___
- [ ] Ticker **MIST** [buy] (clone 1004161) → Verdict: ___

### B#13 msg=4189
> Added another small block of RADX at 5.18 still holding it. Mist still holding  No day trade yet today  I saw AZI might try there will keep you posted but overall  The volume today is below last week 

- [ ] Ticker **RADX** [hold] → Verdict: ___
- [ ] Ticker **AZI** [status] (clone 1004189) → Verdict: ___

### B#14 msg=4212
> So far today no more open positions for me traded SIDU twice and secured some profit at LAES. I will be watching as I need to review few other things!  Enjoy team!

- [ ] Ticker **SIDU** [status,watch] → Verdict: ___
- [ ] Ticker **LAES** [praise,status,watch] (clone 1004212) → Verdict: ___

### B#15 msg=4317
> Overall the market in a hold mode. OMER still holding got some profit there but will carry on and hold most likely. IMRX  I am hoping I can exit some of it by Friday to not risk much through the data 

- [ ] Ticker **OMER** [hold] → Verdict: ___
- [ ] Ticker **IMRX** [hold,sell] (clone 1004317) → Verdict: ___
- [ ] Ticker **BMRA** [] (clone 2004317) → Verdict: ___

### B#16 msg=4352
> VRME Made a successful trade from 0.92 to 1.12 Will watch to see if more trading levels might show. Another one  TMDE I placed a day trade order at  0.86

- [ ] Ticker **VRME** [watch] → Verdict: ___
- [ ] Ticker **TMDE** [buy] (clone 1004352) → Verdict: ___

### B#17 msg=4455
> ACRV last order filled 1.69  I will just hold no more add . I may add extra budget for it if I make profit through any day trade next week! Again full transparency! I mainly used my profit from IMRX a

- [ ] Ticker **ACRV** [buy,hold] → Verdict: ___
- [ ] Ticker **IMRX** [] (clone 1004455) → Verdict: ___
- [ ] Ticker **ALMS** [] (clone 2004455) → Verdict: ___
- [ ] Ticker **NRXP** [] (clone 3004455) → Verdict: ___

### B#18 msg=4564
> AUID sold another 25% at 1.91 so far covered all my capital with good gain.  CJMB as a low float might show more volatility. I am watching to see how to trade it

- [ ] Ticker **AUID** [sell,status] → Verdict: ___
- [ ] Ticker **CJMB** [watch] (clone 1004564) → Verdict: ___

### B#19 msg=4881
> ELPW halted up again! IBRX is doing good team ✅! GUTS still holding it.  I am still watching this crazy move in ELPW for a day trade

- [ ] Ticker **ELPW** [hold,praise,status] → Verdict: ___
- [ ] Ticker **IBRX** [hold,praise,status,watch] (clone 1004881) → Verdict: ___
- [ ] Ticker **GUTS** [hold,praise,watch] (clone 2004881) → Verdict: ___

### B#20 msg=4920
> So far team  Look at  DKI the best day trade pre market in the market! Even SXTC the one earlier didn’t end red so basically pre market trades all successful ✅! I am still watching for any incoming tr

- [ ] Ticker **DKI** [praise] → Verdict: ___
- [ ] Ticker **SXTC** [status] (clone 1004920) → Verdict: ___

### B#21 msg=4934
> DKI team the one I alerted to you here with entry/exit and time frame appeared to be the best day trade for the day! GUTS  Sellers are putting more pressure into 0.44 0.45 levels  I might add little u

- [ ] Ticker **DKI** [buy,praise,sell,status,watch] → Verdict: ___
- [ ] Ticker **GUTS** [buy] (clone 1004934) → Verdict: ___

### B#22 msg=4952
> So far MAMO got to 1.42 dropped back to 1.31 entry  was good pre market still holding. Big pressure into GUTS . But still holding might get few to average but will use only profit from day trades . AT

- [ ] Ticker **MAMO** [buy,hold] → Verdict: ___
- [ ] Ticker **GUTS** [hold] (clone 1004952) → Verdict: ___
- [ ] Ticker **ATOS** [] (clone 2004952) → Verdict: ___

### B#23 msg=4970
> Last update: MAMO still hold GUTS  placed an order at 0.395 for little average if it gets there today. ATOS Hold IBRX Hold

- [ ] Ticker **MAMO** [buy,hold] → Verdict: ___
- [ ] Ticker **GUTS** [buy,hold] (clone 1004970) → Verdict: ___
- [ ] Ticker **ATOS** [hold] (clone 2004970) → Verdict: ___
- [ ] Ticker **IBRX** [hold] (clone 3004970) → Verdict: ___

### B#24 msg=4990
> My great team. I am watching all market activities. So far we are doing good at  IBRX MAMO is trying to find a support still above 1  Still a hold as long as no drop below 0.90  GUTS  Is also trying s

- [ ] Ticker **IBRX** [hold,status] → Verdict: ___
- [ ] Ticker **MAMO** [hold,status] (clone 1004990) → Verdict: ___
- [ ] Ticker **GUTS** [status] (clone 2004990) → Verdict: ___

### B#25 msg=5001
> So by now I guess anyone traded  SMX today made some money! Anyone got the fantastic entry in BBAI made a great trade! We still waiting  MAMO GUTS  ATOS  But going by numbers  In even in this crazy ma

- [ ] Ticker **SMX** [buy] → Verdict: ___
- [ ] Ticker **BBAI** [buy,hold] (clone 1005001) → Verdict: ___
- [ ] Ticker **MAMO** [hold] (clone 2005001) → Verdict: ___
- [ ] Ticker **GUTS** [hold] (clone 3005001) → Verdict: ___
- [ ] Ticker **ATOS** [] (clone 4005001) → Verdict: ___

### B#26 msg=12
> GOOD MORNING 🌞 MY GREAT INCREDIBLE TEAM MEMBERS! THE BIOTECH BIG SHOW BIG FUN WILL BE STARTING TOMORROW STAY TUNED ✅✅‼️✅✅‼️✅✅!

- [ ] Ticker **GOOD** [praise,status] → Verdict: ___
- [ ] Ticker **GREAT** [praise,status] (clone 1000012) → Verdict: ___
- [ ] Ticker **SHOW** [] (clone 2000012) → Verdict: ___
- [ ] Ticker **STAY** [] (clone 3000012) → Verdict: ___
- [ ] Ticker **TUNED** [] (clone 4000012) → Verdict: ___

### B#27 msg=274
> I am watching and taking all notes for : SLS still hold  ABOS hold and might add check the previous post here or if you are in the email group my last night email! GUTS  I will be watching to see if i

- [ ] Ticker **SLS** [buy,hold] → Verdict: ___
- [ ] Ticker **ABOS** [buy,hold] (clone 1000274) → Verdict: ___
- [ ] Ticker **GUTS** [watch] (clone 2000274) → Verdict: ___

### B#28 msg=339
> Good evening my wonderful team here. Took some great notes about biotech stocks : IBRX the expected pullback happened today we were prepared. I even mentioned it this morning earlier! SLS still in the

- [ ] Ticker **IBRX** [status] → Verdict: ___
- [ ] Ticker **SLS** [hold] (clone 1000339) → Verdict: ___
- [ ] Ticker **OCGN** [] (clone 2000339) → Verdict: ___

### B#29 msg=5253
> Team ENSC If it can’t break above 0.66 soon I might reduce it . I don’t need to stress about it while already got nice profit in BATL trade .

- [ ] Ticker **ENSC** [praise,status] → Verdict: ___
- [ ] Ticker **BATL** [praise] (clone 1005253) → Verdict: ___

### B#30 msg=417
> Some overnight activities. I am working on sharing new plans and charts for  IBRX : Tonight earning brought it down I will be watching for levels in case I decide to trade it will share here! IMUX Is 

- [ ] Ticker **IBRX** [watch] → Verdict: ___
- [ ] Ticker **IMUX** [] (clone 1000417) → Verdict: ___
- [ ] Ticker **SLS** [] (clone 2000417) → Verdict: ___

### B#31 msg=5348
> IMPORTANT ‼️‼️‼️: I hope you are enjoying your weekend my incredible team! THE LONG TERM LIST MARCH 2026 COPY is ready if you ever signed up for it please email me asap to get your copy!! My email: Js

- [ ] Ticker **TERM** [praise] → Verdict: ___
- [ ] Ticker **LIST** [praise] (clone 1005348) → Verdict: ___
- [ ] Ticker **MARCH** [] (clone 2005348) → Verdict: ___
- [ ] Ticker **COPY** [] (clone 3005348) → Verdict: ___

### B#32 msg=480
> Good morning my great team here! OCGN got to 1.89 pre market ✅! Today will share the updated chart! IBRX still trying to regain above 8 level! SLS under RSI pressure ( overbought) I will also share a 

- [ ] Ticker **OCGN** [hold,praise] → Verdict: ___
- [ ] Ticker **IBRX** [buy,hold,status] (clone 1000480) → Verdict: ___
- [ ] Ticker **SLS** [buy,status] (clone 2000480) → Verdict: ___

### B#33 msg=568
> RCKT  4.17 partially filled earlier  4.30 fully filled  So far holding! I am watching  The action: SLS IBRX OCGN ABOS I will share some updates later

- [ ] Ticker **RCKT** [hold,watch] → Verdict: ___
- [ ] Ticker **SLS** [] (clone 1000568) → Verdict: ___
- [ ] Ticker **IBRX** [] (clone 2000568) → Verdict: ___
- [ ] Ticker **OCGN** [] (clone 3000568) → Verdict: ___
- [ ] Ticker **ABOS** [] (clone 4000568) → Verdict: ___

### B#34 msg=574
> ATOS Moved some today still holding. SLS IBRX OCGN RCKT I will share more updates still also in the hold zone✅✅

- [ ] Ticker **ATOS** [hold,status] → Verdict: ___
- [ ] Ticker **SLS** [hold] (clone 1000574) → Verdict: ___
- [ ] Ticker **IBRX** [hold] (clone 2000574) → Verdict: ___
- [ ] Ticker **OCGN** [hold] (clone 3000574) → Verdict: ___
- [ ] Ticker **RCKT** [hold] (clone 4000574) → Verdict: ___

### B#35 msg=612
> OCGN  IBRX  dropped due to some news ( overreaction still a possibility here) SLS  Red with the market sentiment.

- [ ] Ticker **OCGN** [hold] → Verdict: ___
- [ ] Ticker **IBRX** [hold,status] (clone 1000612) → Verdict: ___
- [ ] Ticker **SLS** [status] (clone 2000612) → Verdict: ___

---

## Section C — (optional) L1-Blocked Review
*41 msgs die bei L1-Chain-Inheritance geskippt wurden, weil Text einen plausiblen neuen Ticker enthielt. Separater Review bei Bedarf.*