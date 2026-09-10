# SOL-SM3-SHORT-TERM-RULES-2026-09-06

Sol → Chief + human  
**Advisory. Not live until human FINAL.** No tickets from this memo. Autofill stays **OFF**.  
Date: 2026-09-06 · Venue: **4663 Uniswap v3 only** · Book: 4 memes + idle USDG

---

## 0. JP TLDR

今日のミームが振れているのに短期をやらなかったのは、**ルールが無かったから**（ポリシー）。ここからは **最小ルール** を置く。新規買いより **既存4本の部分利確／部分損切**。5本目なし。CASHCAT から回す。idle USDG ~$844 は原則触らない。Perp でヘッジしない。Autofill は付けない（例外も作らない）。

**Sol 推奨 FINAL: まず paper-only 48h。** マークが「今日 internally 大きく振れた」事実のあとに即ライブは、スリッページで kill を削る。48h でシグナルが :53 と矛盾しなければ adopt。

---

## 1. Why there was no scalp (FACT)

Operated policy: HOLD + war-council marks + Chief arms + no written scalp/stop. That is **not** a missing trader bot. It is a **missing rule**. This memo is the rule draft.

**Not a fix:** Lighter/Arcus/HL perp, a 5th name, Autofill, selling all four into one chase.

---

## 2. FACT vs speculation

| FACT | Speculation (do not trade on it) |
|------|----------------------------------|
| 4 names, costs **$939**; last public Quoter exit sum was ~$1108 (09:51 JST snap). Human: marks **swinging hard today**. | “It will reclaim” / social / other-chain twin. |
| Marks = **QuoterV2 full-size exit** (same as dash). | Mid, last-tick, or 1-block print. |
| Official v3 only. RPC **429** already happens. | “Retry harder / wider range.” |
| Kill **$1223.10**. Idle USDG ~$844. | Using idle to “average NEKO.” |
| PONS was the only live convexity in the morning snap (~+$119 / cost $282). | PONS must be the 3× engine forever. |

All triggers below use **QuoterV2 full intended clip** (the slice you would sell), not a 1-unit quote.

---

## 3. Minimal rule set (draft for FINAL)

### 3.1 Universe

- **Only** PONS, NUDES, NEKO, CASHCAT.
- **No 5th.** No idle-USDG **new buy** unless §3.6 (default: **off**).
- Rotate **CASHCAT first** if a slot is needed for a **factory FACT** name (snipe Clerk) — that is **not** a scalp; it is the existing rotate rule.

### 3.2 Intent

**Reduce** winning/losing inventory in **clips**. Do not day-trade the sleeve to zero in one session.

### 3.3 Size

| Action | Size | Cap |
|--------|------|-----|
| Take-profit clip | **25% of that name’s token amount** | ≤ **$100** Quoter notional |
| Stop clip | **25%** of that name | ≤ **$100** |
| Max clips / name / day | **1** | — |
| Max tickets / day (all names) | **2** | — |
| Idle USDG add | **0** (default) | — |

Never sell 100% of PONS in this rule set (3× still wants a convex stub). Hard floor: after a TP, **≥50% of original PONS tokens** remain unless kill §3.8.

### 3.4 Signals (need **two** consecutive :53 **or** two dash Quoters ≥25m apart)

Use **cost** as the anchor (ledger), mark = latest Quoter exit for the **clip** (25% of bag).

| Name | TP (clip) | Stop (clip) |
|------|-----------|-------------|
| **PONS** | clip mark ≥ **+40% vs cost** (morning snap was already ~+42% on full bag — **if still ≥+40% on the clip Quoter, TP is live**) | clip mark ≤ **−25% vs cost** |
| **NUDES** | ≥ **+35% vs cost** | ≤ **−25% vs cost** |
| **NEKO** | ≥ **+35% vs cost** | ≤ **−25% vs cost** |
| **CASHCAT** | ≥ **+40% vs cost** | ≤ **−30% vs cost** (smallest; looser stop so we don’t churn $100 dust) |

**Hysteresis:** if a name is within 5 percentage points of TP and last clip was a TP, **skip** (no instant buyback).

**INFERENCE:** these % are desk-sized for $75–100 tickets and ~1%–3% expected v3 fee+slip on thin 4663 memes. They are **not** backtested. That is why paper 48h is the default FINAL.

### 3.5 Cooldown / skip

- **Cooldown:** 2h after any fill on that name; 4h after any **stop**.
- **SKIP (no ticket):** RPC 429 / Quoter fail / factory call fail; clip slippage **> 5%** vs Quoter mid-clip; `minOut` cannot be set from a fresh Quoter; MTM **<$1500** (soft freeze — clue memo); already 2 tickets today; war-council and dash disagree on mark by **>15%** (stale/thin).
- **One name per ticket.** No basket.

### 3.6 New buys from idle USDG

**Default OFF.**  
Only if (all): factory FACT-pass on a **new** official v3 USDG/WETH pool **and** CASHCAT rotate completed **and** never-touch USDG ≥$80 **and** Chief arms. That is snipe, not scalp. Do not “buy the dip” on NEKO from $844.

### 3.7 Fees / slippage (assumptions for the ticket)

- Assume **≤ 3%** all-in (pool fee + impact) on a $75–100 clip; if Quoter impact **> 5%**, SKIP.
- Finite approve of the **meme token** to the official v3 router only, exact clip raw amount. Revoke leftover. Never `--unlimited`.
- `minOut` = Quoter minus **2%** buffer, else skip.

### 3.8 Kill / flatten

- Wallet MTM **<$1223.10** → this rule set **stops**. Flattening still needs Chief+human tickets (existing lock).
- This scalp book must not be the thing that **causes** kill: if two stops would push projected MTM under **$1400**, **skip the second** and ping Chief.

### 3.9 Who does what (Autofill OFF — no exception)

| Role | Does | Does not |
|------|------|----------|
| Program / :53 | Compute % vs cost from Quoter | Send txs |
| Snipe Clerk or Scout | Confirm official v3 + skip reasons | Arm |
| **Chief** | Arms 0–2 tickets/day | Autofill |
| Executor | One signed swap | Invent size |
| Auditor | Cost basis, clip %, spender, minOut, daily cap | |

**No Autofill exception.** A “narrow band TP bot” is how the envelope dies on a 429-stale mark.

---

## 4. Worked example (illustrative, not a ticket)

Morning snap PONS cost $282, full-bag mark ~$401 (~+42%).  
If **two** later Quoters on a **25% clip** still show ≥+40% vs **clip cost** ($70.5): Chief may arm **sell 25% PONS**, minOut from Quoter−2%, ≤$100 notional. Then cooldown. Do **not** buy it back the same day.

If CASHCAT clip Quoter ≤ −30% vs $25 cost: one stop clip, then stop-cooldown 4h. Do not refill from USDG.

---

## 5. What this will not do

- Print 3× by itself (clips harvest, they do not create a new HYPE).
- Catch the exact wick (Autofill OFF + 2-print rule is **slow on purpose**).
- Fix 4663 thin edge (that is Memo A / Solana).
- Use perps to short the meme sleeve.

---

## 6. Human FINAL ballot

| Choice | Meaning |
|--------|---------|
| **Adopt live** | Rules §3 become operable tickets today. |
| **Adopt paper-only 48h** | **Sol recommendation.** Log every TP/STOP/SKIP at :53 for 48h. No Executor. Then re-ballot. |
| **Reject** | Stay HOLD-only. Honest if you do not want any 4663 sells until a factory FACT. |

| Extra gates | Accept | Reject |
|-------------|--------|--------|
| Autofill OFF (no exception) | **Sol: accept** | |
| No idle-USDG dip buys | **Sol: accept** | |
| No perp hedge | **Sol: accept** | |
| Paper 48h before live | **Sol: accept** | |

---

*Sol. Short-term is harvest rules, not a new personality.*
