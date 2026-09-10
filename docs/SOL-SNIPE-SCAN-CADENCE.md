# SOL-SNIPE-SCAN-CADENCE

Sol / RH Autonomous LP Lab — **cadence memo only**  
Date: 2026-09-06 · Sibling: `docs/SOL-SNIPE-ROUTINE-REVIEW.md` (Patch A)  
Not a ticket. Autofill stays OFF. Chief still arms.

Question: is **scan frequency / count** too low for early snipe on 4663 FCFS — and what cadence actually fits a Grok Bot **@every 5m** floor?

---

## 0. 日本語サマリ

**人間の感覚は正しい。ただし「5分ダッシュ」が遅いのではなく、工場スキャンの回数がほぼゼロなのが遅い。**

- 公開ダッシュ 5分は **保有マークの再計算**。`PoolCreated` は見ていない。:53 は HOLD。Scout はイベント／人間頼み。これでは新規ペアの一次センサが **1日に数回以下**。
- 4663 は **FCFS**。1分ループでも「ブロック先頭」は取れない。Autofill OFF なら執行はさらに Chief 待ち。それでも **工場ログを 5分ごと** に見るのと、出来高が盛れてから見るのとでは、発見が **時間単位でずれる**。
- Grok Bot の床 **@every 5m（1m 不可）** は、早期スナイプの **実用上限** として十分使う価値がある。全部を 5分にはしない。
- **5分:** 公式 v3 factory の `PoolCreated` だけ（前回ブロック以降、1アドレス・1トピック）。USDG/WETH クォートなら Quoter 1回。Chief に「新規N件 / 0件」。
- **15–60分:** ウォッチリスト＋保有4本の出来高、先物ティッカー文字列、任意で v4/Pools.trade **手がかり**。
- **イベントのみ:** 人間が名前を投げた瞬間の FACT。429 のときは工場ポーリングを間引く（出来高全スキャンは増やさない）。
- これは **パッチAの実装形**。Autofill は付けない。

---

## 1. Is the human right?

**Yes — for factory / new-pool scans. No — if they mean “make the dash faster.”**

| Clock that already exists | Interval | Is it a FACT-scan of new pools? |
|---------------------------|----------|----------------------------------|
| Public dash | **5m** | **No.** Snapshot / Quoter on **held** book. |
| NAV watch | hourly daytime | **No.** Book health. |
| Meme war-council | hourly :53 | **No.** Marks / HOLD. |
| Team digest | 3×/day | **No.** Narrative. |
| Scout | ad-hoc + human asks | **Sometimes**, one name, not a `PoolCreated` loop. |
| Fastest Grok Bot floor | **5m** (cannot 1m) | **Unused** for factory today. |

So the lab already pays for a **5m** heartbeat and spends it on marks. New-pool **count** is near zero. That is the frequency bug.

**FCFS FACT** ([docs.robinhood.com/chain](https://docs.robinhood.com/chain/)): higher gas does not jump the line. A 1m bot still loses to whoever’s `eth_send` arrived first. **INFERENCE:** “early” for this lab = **see the listing in the same 5m bucket it was created**, then FACT, then Chief — not first-block inclusion.

With Autofill OFF, you will **never** be the first fill on a hot pool. Cadence still matters: 5m discovery vs hourly/:53 vs “human noticed volume” is the difference between a Chief ticket **during** the first wave and a ticket **after** it.

**Verdict:** raise **factory poll count** to the Grok floor. Do **not** raise dash/Quoter/futures to 5m.

---

## 2. Recommended FACT-scan cadence (minutes)

Official v3 factory: `0x1f7d7550b1b028f7571e69a784071f0205fd2efa`  
QuoterV2: `0x33e885ed0ec9bf04ecfb19341582aadcb4c8a9e7`  
Quote filter: USDG `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` or WETH `0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73`.

| Scan | Interval | What “FACT” means this tick |
|------|----------|------------------------------|
| **A. Factory `PoolCreated`** | **5m always** (Grok floor). Same night and weekend. | `getLogs` from `last_block+1` → now, **one** address, **one** topic. New USDG/WETH pool → FACT job (below). Else emit `new_v3_pools=0`. |
| **B. Quoter / intended-size exit** | **Event-driven** on each new USDG/WETH pool from A. Not on a timer. | Full **$75–100** QuoterV2. Pass / fail / thin. One name. |
| **C. Volume (swap logs) on a name** | **15m** if the name is on the **watchlist** (new pool <24h or futures-string match). **60m** for held 4. | Multi-block notional + trade count. Not one-swap fireworks. |
| **D. Futures ticker strings** | **60m** weekday; **0–1×** weekend (clue memo). | Strings only. No OI/funding. |
| **E. v4 `Initialize` / Pools.trade** | **15–60m** clue-only, or skip if 429. | “Name exists on 4663.” **Not** a v3 trade ticket. |

Prior review said “≤15m in JST windows / ≤60m else” for a **mixed** factory+volume watch. **This memo tightens factory to 5m** because the bot floor exists and factory logs are cheap. Volume stays 15–60m.

Do **not** run B every 5m on every pool. That is how you 429 and mint false positives.

---

## 3. What to poll at each speed

### Every 5m (Grok `@every 5m` — **one** cheap job)

```text
1. eth_blockNumber
2. eth_getLogs: v3 factory, PoolCreated, [last_seen_block+1, head]
3. Filter token0/token1 ∈ {USDG, WETH}
4. If zero: write last_seen_block; stop.
5. If N>0: for each new pool, queue FACT-B (Quoter) — still read-only
6. Ping Chief/Scout: "N new official v3 USDG/WETH pools" + fee tier from the log
```

**Not** in this 5m job: all-pool Swap scans, 4× Quoter marks (dash already does that), futures HTTP, Arcus/Lighter, social, full token metadata for non-USDG/WETH pools.

### Every 15–60m

- Watchlist volume (15m).
- Held PONS/NUDES/NEKO/CASHCAT volume (60m is enough; :53 already marks).
- Futures name list (60m).
- Optional v4/launchpad clue (15–60m). If RPC is hot, **drop this first**.

### Event-driven only

- Human / digest names a ticker → **immediate** factory membership + Quoter (do not wait for :53).
- `new_v3_pools>0` from the 5m job → immediate Quoter.
- 429 / RPC fail → **no** extra retries in the same 5m tick; skip to next tick (see §4).
- Chief arms → human-signed ticket. **Never** from the 5m cron.

---

## 4. Cost / noise (429 we already see)

**FACT-shaped constraint:** public 4663 RPC / explorer already 429 or 500 on wide calls (landscape memo; lab ops).

| Pattern | RPC cost | Noise | Use? |
|---------|----------|-------|------|
| Factory `PoolCreated` since last block (1 addr, 1 topic, short range) | **Low** | Low (listings are rare) | **5m yes** |
| QuoterV2 × 1 new pool × 1 size | Low | Medium (thin books fail — that is the gate) | On alert only |
| QuoterV2 × all held + all new every 5m | High | High | **No** (dash already 5m on held) |
| `Swap` logs for all v3 pools every 5m | **Very high** | Very high (false “spikes”) | **No** |
| Futures leaderboard every 5m | External + busywork | Fake-HYPE names | **No** |

**429 rules (adopt):**

1. One factory poll per 5m tick. No parallel `getLogs` fan-out.
2. Range = last success → head. If the node rejects the span, **halve once**; if still 429, store `last_seen_block` unchanged and exit.
3. After 429: next tick is still 5m (do not jump to 1m — bot cannot). After **three** consecutive 429s: factory job stays 5m but **disable** 15m volume / v4 clue until one clean factory poll.
4. Never widen to “scan the whole chain for Swap.”

**False positives:** `PoolCreated` ≠ tradeable. Thin Quoter = skip. One-block volume = skip. Ticker twin = skip. v4-only name = clue, not a ticket. The 5m job is allowed to shout `N=1` often if the chain is spam-listing; **Chief still needs FACT-B pass** and a slot (rotate CASHCAT, no 5th).

---

## 5. Concrete Scout / Chief plan (fits 5m floor, no Autofill)

### Scout — Grok Bot `@every 5m` (new; Patch A)

Read-only. Secret-free public output can be a count + symbols, **no** private keys.

```text
every 5m:
  factory_poll()           # §3
  if new USDG/WETH pools:
    quoter_fact($75–100)   # fail → skip
    emit one-pager to Chief (not a ticket)
  else:
    heartbeat "0 new official v3 pools"
```

Scout does **not** raise Autofill, does **not** approve, does **not** reuse Lighter $50.

### Scout — `@every 15m` (weekday windows JST 08–11, 21–01) / `@every 60m` otherwise

Watchlist volume + optional v4 clue. Skip entirely on 429 backoff.

### Scout — `@every 60m` weekday

Futures **strings** only. Weekend: off or 1×.

### War-council `:53` (keep)

Marks / HOLD / kill / sleeve. **Not** the discovery clock. If the 5m job already pinged a FACT-pass, :53 only repeats HOLD vs “Chief still deciding.”

### Dash 5m (keep)

Held marks. Do **not** fold factory logs into the public JSON unless Chief wants a public `new_v3_pool_count_24h` later (Patch C). Not required to fix cadence.

### Digest 3×/day (keep)

Pass/fail counts, skips, idle USDG, distance to $5645 / $1223.10. Not a scan.

### Chief

- Sleeps until `FACT-pass` one-pager **or** human ask.
- Arms **one** ≤$100 ticket; rotate CASHCAT first if at 4 names.
- Finite approve; official v3 only.
- If 5m Scout is quiet for days: that is a **quiet chain**, not a broken cron. Do not loosen FACT to “make scans useful.”

---

## 6. Tie to Patch A

| Patch A (review memo) | This cadence memo |
|----------------------|-------------------|
| Factory as **primary** sensor | **How often:** 5m `PoolCreated`, not 15–60m mixed. |
| FACT same session | Quoter **event-driven** on new USDG/WETH rows. |
| Futures demoted | 60m strings, never 5m. |
| v4 / Pools.trade clue-only | 15–60m, first to drop on 429. |
| Autofill OFF | 5m job **reports**; Chief arms. |
| Held-book volume | 60m / :53 — do not put on the 5m factory job. |

Patch B (pre-written rotate/buy drafts) is unchanged and still useful: 5m visibility is wasted if Chief has to design a ticket from scratch.

**Do not** interpret “scan more” as “buy more.” Frequency upgrade is **logs**, not size, not a 5th meme, not Autofill.

---

## 7. One-line answers

1. **Yes** — factory scan count is too low; dash 5m is not that scan.  
2. **Factory 5m; Quoter on alert; volume 15–60m.**  
3. **5m = PoolCreated only. 15–60m = volume / futures / optional v4. Event = named FACT.**  
4. **Narrow getLogs is cheap; all-swap + all-Quoter 5m is how you 429 and false-positive.**  
5. **Grok `@every 5m` factory heartbeat → ping Chief; :53 stays HOLD; no Autofill.**  
6. **This is Patch A with the bot floor used for the factory leg.**

---

*Sol. Memo only. No tickets.*
