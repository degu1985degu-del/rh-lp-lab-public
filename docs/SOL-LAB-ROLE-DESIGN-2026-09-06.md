# SOL-LAB-ROLE-DESIGN-2026-09-06

Sol → Chief + human operator  
**Advisory only.** No POLICY change. No tickets. No wallet spend.  
Date: 2026-09-06 · Book: wait + monitor, 4663 Uniswap v3 only

---

## 0. JP TLDR

**骨格（Scout 読み取り専用 / Chief 武装 / Executor 執行）は SM3 の wait-and-snipe に正しい。Scout が弱く感じる主因は「役割不足」ではなく「今は買う FACT が無い」＋「空ループで LLM を起こさない」こと。**

トレーダーを増やすな。**イベント時だけ動く 1 体（Snipe Clerk）** を足せ。常時 Spot/Meme Trader、時間帯エッジ、News デスク、Chief と並ぶ War-room chair は **却下**。Risk Officer は LLM ではなく **プログラム**（既存 NAV/:53）。Perp/bridge は Scout 弱さの治療にしない。

| 役割 | 採否 | Phase |
|------|------|-------|
| 現状骨格 + Scout は空ループで寝かす | **採用** | 0 |
| **Snipe Clerk**（工場 N>0 / 人間名だけ起こす。FACT 1枚＋下書き。チケット不可） | **採用（最大1体）** | 1 |
| Risk Officer as **program** (kill / sleeve / 4本 / never-touch) | **採用（新人格ではない）** | 0–1 |
| Spot Trader / Meme Trader / Session bot / News desk / 別 War-room chair | **却下** | — |

---

## 1. Snapshot this memo assumes (Chief, 2026-09-06 JST)

- Lab: 4663 only. AI research → select → execute → monitor inside a hard max-loss envelope. No bot bridge / borrow / leverage. B0 **$1881.69** → 3× **~$5645**. Wallet `0xeb2e…4c7b`.
- LP EXITED. Spot **HOLD_USDG_CASH** (idle USDG ~$844). Meme HOLD×4 (PONS/NUDES/NEKO/CASHCAT, marks ~$999). MTM ~$1865 (~flat B0).
- Perp **0%**. Lighter/Arcus geo from lab egress. No perp until new human FINAL + permitted egress.
- Locks: Autofill OFF, no new LP, no self-raising caps, kill **MTM < $1223.10**.
- Patch A **live**: 5m `PoolCreated` on official v3 factory `0x1f7d7550…`, USDG/WETH only; Scout **not** woken on empty loops.
- Human concern: Scout feels like a passive clue checker; maybe **more trader bots**, not more Scout tokens.

Envelope math (INFERENCE, for role sizing): kill $1223 vs MTM ~$1865 ≈ **~$640** airbag. A “$500-ish loss” budget is the **same airbag**, not extra risk to spend. One bad Autofill meme can print it.

---

## 2. Q1 — Is the skeleton still right?

**Yes. Keep Scout read-only / Chief arms / Executor executes / Auditor checks / Reporter narrates.**

Scout is **under-woken**, not under-scoped.

| Feeling | What is actually true |
|---------|------------------------|
| “Scout isn’t a trader” | **By design.** Autofill OFF means **nobody** except Executor-after-Chief is a trader. Adding a “Trader” persona that can fire is a **policy change**, not a role upgrade. |
| “Scout only checks clues” | Discovery moved to **program** (5m factory). Empty loops **should not** burn LLM. That is Patch A succeeding. |
| “We need more bots” | More **standing chat agents** = more opinions on a quiet book = fifth-meme pressure and token burn. Edge now is **alert → one FACT page → one armed ticket**. |

A trader without Autofill is a **clerk that drafts**. Call it that. Do not staff four clerks.

---

## 3. Evaluated personas (accept / reject)

### REJECT — Spot Trader

- **Pitch:** always-on bot for USDG↔stocks/WETH.
- **Why reject:** Spot mandate is HOLD_USDG_CASH. Stocks sold, WETH sold. No 4663 HYPE-class alt sitting in official v3. This role **invents re-entry**. Cost: LLM every session for $0 edge. Risk: sleeve leak, kill via “just one stock hop.”

### REJECT — Meme Trader

- **Pitch:** flip / add memes like a desk.
- **Why reject:** 4/4 slots. No 5th. Rotate CASHCAT only after FACT. An always-on meme bot will **propose size** to look busy. That is Autofill-shaped. War-council :53 already marks HOLD.

### REJECT — Time-of-day / session edge bot

- **Pitch:** Tokyo / US overlap alpha.
- **Why reject:** Clue memo: human windows **reorder cadence**, they do not create names. 4663 is FCFS, not NYSE session microstructure. This bot will mint tickers from the clock.

### REJECT — News / clue desk

- **Pitch:** social + futures + headlines.
- **Why reject:** Futures are **strings only**. Social-as-primary is a false-positive factory. Token-heavy, FACT-light. Scout already may pull strings at 60m; do not add a desk.

### REJECT — War-room chair ≠ Chief

- **Pitch:** someone else runs :53 so Chief can think.
- **Why reject:** Two “chairs” split **arming**. Committee Autofill. :53 is marks; Reporter can write the digest. Chief stays the only arm.

### ADOPT as program, not a persona — Risk Officer

- **Mandate:** halt flags only. Kill floor, never-touch USDG $80–100, meme sleeve $1000, max 4 names, MTM vs $1500 soft freeze (clue memo).
- **Inputs:** existing dash 5m + CANARY NAV hourly + :53 marks.
- **Outputs:** `GREEN / SOFT / KILL` one-liner to Chief. No names, no tickets.
- **Must NOT:** arm, rotate, “buy to hedge,” raise caps, wake Scout.
- **Why this is the real envelope edge:** the $500-ish budget dies from **process failure**, not from missing a tweet.

### ADOPT — one new LLM persona: **Snipe Clerk** (not “Trader”)

| | |
|--|--|
| **Name** | Snipe Clerk |
| **Mandate** | When (and only when) factory job says `N>0` USDG/WETH v3 pools **or** human/Chief names a ticker: produce **one** FACT one-pager + optional ticket **draft fields**. |
| **Inputs** | Factory log (pool, fee, tokens from **the log**). Official factory `0x1f7d7550…`. QuoterV2 full $75–100. Held book (4 names, CASHCAT first rotate). Kill / idle USDG. |
| **Outputs** | `pass / fail / skip`. If pass: size ≤$100, rotate-or-not, finite-approve reminder, Quoter minOut. Same clue-record fields as the 3× memo. **Not a ticket.** |
| **Must NOT** | Autofill, approve, swap, 5th name, v4/Pools.trade execution, other chain, perp/bridge, empty-loop chat, five drafts, invent addresses, wake on `N=0`. |

This is Patch A **plus** Patch B’s “arming path” as a **person**, not a 24/7 trader.

**0 extra personas if Chief refuses even this:** Phase 0 only. Scout-on-alert already covers it if you **write the one-pager template** and keep Scout asleep otherwise. Snipe Clerk is Scout **renamed and trigger-gated**, not a second standing teammate.

---

## 4. Surface + cost (program-first)

| Job | Surface | Token discipline |
|-----|---------|------------------|
| Factory `PoolCreated` 5m | **Grok Bot / program** (already live) | **$0 LLM** on empty. Keep. |
| Dash 5m marks | **Program** | No LLM. |
| NAV hourly / :53 marks | **Program + short Chief/Reporter** | No new agent. |
| Risk Officer flags | **Grok Bot program** on NAV/dash numbers | Thresholds, not prose. |
| Snipe Clerk | **Cursor cloud agent on event** (preferred) or **one-shot Grok** when `N>0` | LLM **only on alert**. Do **not** make a standing teammate chat that idles in Discord. |
| Scout (legacy) | Standing chat **asleep** until human ask or Clerk overflow | No 5m LLM. |
| Chief / Executor / Auditor | Unchanged | Chief arms; Executor sends; Auditor checks mandate PDF-style gates. |

**Do not** add a 24/7 Cursor cloud cron that “thinks about the book.” That is Scout token spend with a cooler name.

---

## 5. What Scout keeps vs hands off

| Keep (Scout) | Hand off |
|--------------|----------|
| Human-named ticker FACT (same checklist as Clerk) | Empty factory loops → **program** (already) |
| 60m futures **strings** if Chief still wants them | Held-book marks → **dash / :53** |
| Weekend “any 4663-native rumor?” only if human asks | Risk math → **program Risk** |
| Refuse tickets | Ticket drafts on factory hit → **Snipe Clerk** (or Scout-on-alert; **not both**) |

If Phase 1 Clerk is accepted, **do not also** wake Scout on the same `N>0` ping. One LLM per listing.

---

## 6. Out of scope (not a Scout fix)

- Unlock perp / Lighter / Arcus from lab egress.
- Bot bridge, borrow, LP re-open, Autofill ON.
- Separate human-gated perp sandbox: **only** after a new FINAL + permitted IP. Not this memo.

---

## 7. Phased rollout (accept in one sitting)

### Phase 0 — KEEP (do this even if you reject Phase 1)

- [ ] Skeleton unchanged. Autofill OFF.
- [ ] Factory 5m stays program-only; Scout sleeps on `N=0`.
- [ ] Risk flags as **program** on existing NAV/dash (no new chat agent).
- [ ] One written FACT one-pager template (private lab). No extra bot.

**Success:** days of `new_v3_pools=0` cost **zero** Scout tokens. Human no longer reads “Scout checked nothing.”

### Phase 1 — ADD ONE (recommended)

- [ ] **Snipe Clerk** on `N>0` or human name. Cursor cloud **event** or single Grok shot.
- [ ] Scout **not** dual-woken.
- [ ] Clerk may attach Patch B draft fields (CASHCAT rotate + $75–100 buy). Chief still arms.

**Success (2 weeks):** (a) every official USDG/WETH `PoolCreated` gets a pass/fail page the same 5m bucket; (b) zero tickets without Chief; (c) LLM calls ≈ number of real listings, not 288/day; (d) no 5th meme; (e) MTM stay above $1500 soft / $1223.10 kill.

**Fail → revert to Phase 0** if Clerk emits >1 draft per listing, or chats on empty, or proposes perp/bridge/v4.

### Phase 2 — OPTIONAL (only after Phase 1 is boring)

- [ ] Public dash `new_v3_pool_count_24h` (Patch C). Still no trade button.
- [ ] **Not** a second trader. **Not** session/news bots.

---

## 8. Chief ballot (circle one each)

| Item | Accept | Reject |
|------|--------|--------|
| Phase 0 keep skeleton + sleep Scout on empty | | |
| Phase 1 Snipe Clerk (event-only, no tickets) | | |
| Risk as program (not a persona) | | |
| Spot Trader | | **Sol: reject** |
| Meme Trader | | **Sol: reject** |
| Session / news / extra chair | | **Sol: reject** |
| Unlock perp/bridge to “give Scout work” | | **Sol: reject** |

Sol recommendation: **Accept / Accept / Accept / Reject the rest.**

---

*Sol. If the book is quiet, a quiet Scout is the product working.*
