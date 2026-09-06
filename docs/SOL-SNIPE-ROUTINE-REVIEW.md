# SOL-SNIPE-ROUTINE-REVIEW

Sol / RH Autonomous LP Lab — **research memo only**  
Date: 2026-09-06 · Venue: **Robinhood Chain 4663 Uniswap v3 Spot**  
Not a ticket. Not Autofill. Not a policy change.

Question: is the **current Uniswap monitoring routine** good enough to **snipe hot coins early** on 4663?

Labels: **FACT** = official docs / factory addresses / this lab’s operated routine as stated by the human. **INFERENCE** = labeled. **UNKNOWN** = do not trade on it.

---

## 0. 日本語サマリ / 判定

**判定: 「早期スナイプ」装置としては不十分。死なないための監視としては十分。**

- 今のルーチンは **偽物HYPE・他チェーン・ブリッジを踏まない** ようにできている（FACT gate + Autofill OFF + Chief武装）。それは正しい。
- しかし「早い」は **出来高スパイクの後追い** と **先物の名前リスト** と **人間の東京時間** に依存している。出来高は値動きの**結果**であり、上場の**原因**ではない。
- 4663の新規ネイティブ銘柄の一次センサは **公式 v3 `PoolCreated`（および参考として v4 `Initialize` / Pools.trade `TokenLaunched`）** である。現行オペはそれを第一電源にしていない。
- さらに、公式ローンチパッド **pools.trade は Uniswap v4**（第三者索引・Uniswap Labs ブログ）。ラボの執行は **v3 only**。v3出来高だけ見ると、熱い新規が **見えなかった／遅れて見える**。
- 4663は **FCFS**。ガスオークション型のメンプール・スナイプは構造的に弱い。必要なのは「ブロック内で割り込む」ことではなく、**新規ペアを数分以内に FACT して Chief に1枚渡す**こと。
- 現状（HYPE級がほぼ出ない・4本満杯・HOLD_USDG）では、待っていること自体は合理。出た瞬間に取る装置にはなっていない。
- **推奨はパッチA**（工場イベント監視を一次センサにする）。Autofill は付けない。

---

## 1. Verdict (EN)

| Question | Answer |
|----------|--------|
| Good enough to **not buy junk / fake HYPE / other-chain twins**? | **Yes.** FACT gate is the feature. |
| Good enough to **snipe the first minutes** of a real 4663 listing? | **No.** Sensors are lagging; arming path is hours-shaped; dash/war-council watch the **held book**, not **new pools**. |
| Good enough while **nothing HYPE-class exists**? | **Yes, as a wait posture.** Idle USDG + 4 memes + kill floor is correct until a FACT name prints. |
| Will this routine, unchanged, close **3× by 2026-09-30** via new alts? | **Unlikely.** 3× still needs a real 4663-native name (or existing names multi-bag). The routine will **not create** that name; it may **miss** it if one appears off-cadence or on v4 first. |

“Snipe” here does **not** mean Autofill, mempool, or other chains. It means: **see an official 4663 pool early → FACT (factory + Quoter exit) → Chief arms one ≤$100 ticket.** That is compatible with current locks.

---

## 2. Current routine (as operated — FACT from human)

| Layer | What it does | What it does **not** do |
|-------|----------------|-------------------------|
| **Scout (read-only)** | (a) Futures leaderboard **names as strings**; (b) **4663 v3 volume spikes**; (c) human **Asia/Tokyo** windows. Clue → verify official v3 pool/token → report Chief. | Tickets, trades, Autofill. |
| **Chief** | `HOLD_USDG_CASH` for Spot until strong FACT; ~$100 clip; max 4 memes; no 5th; rotate from CASHCAT; Autofill OFF; arms only. | Instant buy on a Scout ping. |
| **War-council :53 hourly** | Marks / HOLD. No autofill buys. | Discovery of **new** factory pairs. |
| **Public dash ~5m** | `data/latest.json` + `index.html`: held meme Quoter marks, idle USDG, MTM. | Pool-created tape. |
| **NAV/digest** | Book health vs B0 $1881.69 / 3× $5645.07 / kill $1223.10. | Name creation. |
| **Locks** | 4663 only, Uniswap **v3**, no bot bridge, live **perp 0%**, Autofill OFF. | Lighter geo-blocked from lab IP (human). $50 Lighter withdraw L2-pending — **do not spend it here**. |

Sibling memo `SOL-CLUE-DESIGN-3X` (other PR) already **reweighted** sources to **(1) 4663 factory new pairs + volume, (2) futures strings, (3) human clock**. **Operated Scout still leads with futures + volume + Tokyo windows.** That gap is the main sensor bug.

Reality now (human + last public snap): few/no new HYPE-class alts on 4663; idle USDG ~$794 (+$50 Lighter pending); 4 memes held (PONS / NUDES / NEKO / CASHCAT); deploy STOP / HOLD_USDG_CASH.

---

## 3. What “early” can even mean on 4663

**FACT — sequencing is FCFS** ([docs.robinhood.com/chain](https://docs.robinhood.com/chain/)): first-come at the sequencer; paying more gas does **not** jump the line. Classic PGA / “I saw the mempool and bribed” snipe is the **wrong model**.

**FACT — official public AMM is Uniswap v2/v3/v4 + UniswapX** ([Uniswap blog 2026-07-02](https://blog.uniswap.org/robinhood-chain-is-live)). Lab execution lock = **v3**. Official v3 factory (landscape, explorer-verified): `0x1f7d7550b1b028f7571e69a784071f0205fd2efa`. QuoterV2: `0x33e885ed0ec9bf04ecfb19341582aadcb4c8a9e7`.

**FACT — Pools.trade** is the Uniswap Labs launchpad on this chain ([blog 2026-08-05](https://blog.uniswap.org/robinhood-chain-is-live) related post). Third-party indexers describe launches as **v4 PoolManager `Initialize`**, quote often **native ETH**, not a v3 USDG pool. Treat that as **discovery FACT for “a name was born on 4663”**, not as a license to trade v4 or ETH-quoted launch pads.

**INFERENCE:** “Hot coin early” on this chain is usually:

1. `TokenCreated` / `TokenLaunched` / v4 `Initialize` / v3 `PoolCreated` (seconds–minutes), **then**
2. first swaps (seconds–hours), **then**
3. “volume spike” that Scout already watches (hours–day, **late**).

A routine that starts at (3) cannot snipe (1).

---

## 4. Bottlenecks (latency budget)

Assume a real USDG/WETH v3 pool appears at `T=0`. Desired: Chief has a FACT-passed one-pager before the first honest volume wave (`T+5–30m`). Current path:

| Step | Typical delay | Why it hurts snipe |
|------|----------------|--------------------|
| **Scout cadence** | Hours (Tokyo windows) or “when someone looks” | Misses US-hours and weekend launches. Clue design already wanted 1–2h in windows; operated text does not make factory poll first-class. |
| **Sensor = volume spike** | **After** the move | You buy the print, not the listing. |
| **Sensor = futures names** | Wrong chain / wrong product | Good as a **search key**. Zero if no 4663 pool. Creates fake-HYPE work. |
| **Sensor = Asia/Tokyo window** | Reorder only | Does not create names. Sleeps the US afternoon. |
| **FACT gate** | Minutes if someone is awake; hours if not | Gate itself is **correct**. The cost is **no pre-computed Quoter script** and **no standing factory watch**. |
| **Chief arming** | Human + ticket + finite approve + swap | Unavoidable under Autofill OFF. Can be **minutes** if a draft packet exists; **hours** if Scout only said “name looks hot.” |
| **War-council :53** | Up to **59 minutes** if that is the only look | Correct for HOLD. Wrong as the only discovery heartbeat. |
| **Dash 5m** | Fast for **marks** | Does not list new factory events. Looking at the dash harder will not snipe. |
| **Slot lock (max 4, no 5th)** | Even a perfect snipe needs **CASHCAT rotate first** | Discovery without a pre-written rotation packet still cannot arm. |
| **v3-only vs v4 launchpad** | Structural | A Pools.trade name may have **no v3 pool yet**. Current Scout “verify official v3” correctly **skips** — and you never hear about it again. |

**INFERENCE:** end-to-end, operated routine is **hour-scale**, not **minute-scale**. That is fine for capital preservation. It is not early snipe.

---

## 5. Concrete upgrades (locks stay)

Hard locks unchanged: **4663 only · Uniswap v3 execution · no bot bridge · Autofill OFF · Chief arms · no 5th meme · kill $1223.10 · perp 0% live**.

### Patch A — sensors (recommended minimum)

Read-only. No tickets from the watcher.

1. **Primary:** poll / subscribe official **v3 factory** `PoolCreated` for pairs whose quote is **USDG or WETH** (canonical `0x5fc5…d168` / `0x0Bd7…AD73`). Cadence: **≤15 min** in JST 08:00–11:00 and 21:00–01:00; **≤60 min** otherwise. Alert Scout + Chief: name, fee tier, pool address from the **log** (do not invent).
2. **Immediate FACT on alert (same session):** official factory membership + QuoterV2 **full intended $75–100** exit. Fail → skip. Pass → one Chief draft, not five.
3. **Secondary (clue only):** v4 PoolManager `Initialize` and Pools.trade `TokenLaunched` / `TokenCreated`. **Do not trade v4. Do not trade native-ETH launch pads** unless/until a **v3 USDG or WETH** pool FACT-passes. Purpose: know the ticker exists on 4663 so Scout does not wait for a v3 volume spike that never comes.
4. **Demote futures** to a string dictionary (already the written rule). No OI / funding / other-chain mark as a trade reason.
5. **Held-book volume:** PONS/NUDES/NEKO/CASHCAT 4663 swap counts so you do not rotate a live winner.

### Patch B — arming path (A plus)

Still Autofill OFF.

1. **Standing “CASHCAT rotate” draft** (private lab, not this repo): sell ticket shape + finite approve + v3 swap back to USDG. Only used if a new FACT pass needs a slot.
2. **Standing “new FACT buy” draft:** $75–100, USDG→token via official v3 router, finite approve, Quoter minOut, kill-cushion check (idle USDG after fill ≥ $80–100 never-touch).
3. **Scout output = one page:** clue record fields from the clue memo (`official_4663_v3_fact`, `quoter_exit`, `liq_vs_ticket`, `held_overlap`, `action`). No addresses in the public repo.
4. **Off-:53 ping:** factory alert may fire **any** minute. War-council stays marks/HOLD and does **not** become a buy meeting.

### Patch C — coverage (A+B plus)

1. Weekend factory poll at least every 2–4h (clue memo). Do not raise futures pulls on weekends.
2. If lab IP stays US-geo-blocked on Lighter, **do not** add Lighter marks as a snipe sensor (already forbidden as book marks).
3. Optional: public dash adds a **read-only** “last 24h new v3 USDG/WETH pools: N” count — still no trade button.

**Do not** add: Autofill, session-unbounded spender, Universal Router unlimited, other-chain watchers that emit tickets, social follower ranks as FACT, Arcus/Lighter perps as a snipe substitute.

---

## 6. What NOT to do

| Don’t | Why it looks like snipe | Why it dies |
|-------|-------------------------|-------------|
| Autofill / Scout-as-order | “We were 2 minutes late last time” | Mandate break; one bad pair prints kill. |
| Buy ticker-twin / fake HYPE | Same letters as HL / Lighter / Core | Official Stock Token page: matching ticker ≠ same contract. Same for memes. |
| Other chain / bridge “then we’ll list” | Real volume elsewhere | Bot-bridge ban; 4663 FACT fail. |
| Trade Pools.trade **v4** because it is “more official” | Uniswap Labs launchpad | Live lock is **v3**. Watch ≠ execute. |
| One-block volume firework | Looks like “it started” | Clue memo: multi-block. Thin Quoter = fail. |
| 5th meme | “This one is the one” | Mandate + sleeve. Rotate CASHCAT first. |
| Empty never-touch USDG | Max size | M3 already aborted on low USDG. |
| Futures OI / funding as size | “Smart money” | Wrong venue. String only. |
| Dash 5m refresh as discovery | Feels live | It remakes **held** marks. |
| Lighter / Arcus perps | Convex | Live perp 0%; Lighter geo from lab IP; Arcus whitelist. Not a snipe sensor. |

---

## 7. Ranked options

| Rank | Option | What changes | Snipe adequacy | Risk to locks |
|------|--------|--------------|----------------|---------------|
| **1 — adopt** | **Patch A** | Factory (and optional v4/launchpad **clue**) as primary sensor; FACT on the same session; futures demoted | Minute–tens-of-minutes **visibility**. Execution still Chief-paced. | Low. Read-only. |
| **2** | **Patch B** | A + pre-written rotate/buy drafts | Visibility **plus** arming that can finish in one human sitting | Low if drafts stay finite-approve / v3. |
| **3** | **Patch C** | B + weekend poll + dash counter | Fewer sleep misses | Low. |
| **4 — only if 3× is abandoned** | **Keep as-is** | Nothing | Adequate **wait / anti-fake**. Inadequate **early snipe**. Honest if the bet is “existing 4 names + PONS convexity” only. | Lowest process risk; highest **missed listing** risk. |

**Do not pick “Autofill ON” as Patch D.** That is a different lab.

---

## 8. Honest constraint

Even Patch C cannot manufacture a HYPE-class alt. If 4663 simply does not print new official v3 USDG/WETH pairs, the routine will keep reporting **skip / no FACT** — that is success of the gate, not failure of Scout.

3× by 2026-09-30 then depends on **held names** (PONS-class) or a later policy fork (not this memo).

Idle ~$794 is **powder + kill airbag**, not a reason to loosen FACT. Clue memo split still applies: never-touch $80–100 + one $100 clip.

---

## 9. Sources

- Operated routine: human brief this memo answers (Scout / Chief / :53 / dash 5m / locks).
- [SOL-CLUE-DESIGN-3X](https://github.com/degu1985degu-del/rh-lp-lab-public/blob/cursor/sol-clue-design-3x-37f5/docs/SOL-CLUE-DESIGN-3X.md) — adopted weights; factory-first (not yet how Scout is *run*).
- `docs/SOL-4663-EARNING-LANDSCAPE.md` — v3 factory / Quoter / Pools.trade / FCFS.
- [About Robinhood Chain](https://docs.robinhood.com/chain/) — FCFS.
- [Uniswap is Live on Robinhood Chain](https://blog.uniswap.org/robinhood-chain-is-live) — v2/v3/v4; Pools.trade related (2026-08-05).
- Uniswap v3 Robinhood deployments — factory `0x1f7d7550…d2efa`, QuoterV2 `0x33e885ed…c8a9e7`.
- Public dash: `data/latest.json` + `index.html` (held marks, not new pools).

---

*Sol. Research only. No live tickets. If Chief wants Patch A, that is a Scout-watch change — not Autofill.*
