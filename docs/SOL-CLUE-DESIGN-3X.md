# SOL-CLUE-DESIGN-3X

Sol / RH Autonomous LP Lab — strategy memo for Chief  
Date: 2026-09-06 JST · Horizon: **3× by 2026-09-30** · Venue: **4663 Uniswap v3 Spot only**

This note is public and secret-free. It names **no token addresses**. Scout must resolve every name against the **official Robinhood Chain Mainnet (chainId 4663) Uniswap v3 factory** and Quoter exit FACT before Chief arms a ticket.

---

## 0. Adopt today / 本日採用

Decision-ready. Do not wait for a richer source list.

| # | JP | EN |
|---|----|----|
| A | **3×は4663ネイティブの凸（ミーム/新規ペア）以外では届かない。** WETHベータと株式トークンでは届かない。 | **3× only comes from 4663-native convexity** (meme / new official v3 pair). WETH beta and stock tokens cannot close the gap. |
| B | 手がかりの主電源を入れ替える: **① 4663公式v3 FACT（新規ペア＋出来高）→ ② 先物ティッカーは文字列だけ → ③ 人間の時間帯は並び替え専用。** | Reweight sources: **(1) 4663 official v3 FACT (new pairs + volume) first → (2) futures tickers as strings only → (3) human time windows as reorder only.** |
| C | 戦術USDGは **触らない予備 $80–100 + 武装1枚 $100。** 残りはガス/kill緩衝。全額投入禁止。 | Keep **$80–100 never-touch USDG + $100 one-ticket dry powder.** Do not empty idle USDG. |
| D | **5本目は出さない。** 新規FACTが来たら弱い1本を回す。切る順: CASHCAT → NEKO → NUDES。PONSは最後。 | **No 5th name.** Rotate the weakest if a FACT hit appears. Cut order: CASHCAT → NEKO → NUDES. PONS last. |
| E | Autofill OFFのまま。手がかり → FACT → Chiefがチケット武装。先物・他チェーン・ブリッジ・無制限approveは「アルファに見える禁止」。 | Autofill stays OFF. Clue → FACT → Chief arms. Futures / other chains / bridges / unlimited approve look like alpha and are forbidden. |

---

## 1. Book and the 3× gap / 現状とギャップ

Public snapshot morning 2026-09-06 JST (`data/latest.json`, generated 09:04 JST):

| Sleeve | Cost | Mark / note |
|--------|------|-------------|
| Idle USDG | — | **~$287** |
| Native ETH | — | ~$24 (gas, not a sleeve) |
| WETH spot residual | $537 (base $187 + autonomy +$350) | ~$553 · ballast, not the 3× engine |
| PONS | $282 | ~$405 · **only working convexity (~+43%)** |
| NUDES | $275 | ~$277 · flat |
| NEKO | $282 | ~$269 · slight red |
| CASHCAT | $100 | ~$98 · smallest / newest / flat |
| Meme sleeve | $939 / cap $1000 | ~$1049 exit via QuoterV2 |
| Wallet MTM | B0 $1881.69 | **~$1913 ≈ 1.02× B0** |
| Primary 3× | — | **$5645.07** · gap **~$3732** |
| Kill floor | — | **MTM < $1223.10 → stop** · cushion ~$690 |
| Mandate | SM3-52/46/02 | spot 52 / meme 46 / gas 2 / **perp 0** / **lp 0** |
| Caps | — | meme $100/ticket · sleeve $1000 · grandfather **max ~4 open** · high-convexity **max 3** |
| Posture | Deploy **STOP** | LP EXITED · stocks sold · Autofill OFF · Chief arms |

**Math that matters / 効く計算**

- 24日で +$3732。WETHが2倍でも +$550 程度。株式トークンは既に売却済みで、4663上にHYPE級スポットは未検出。
- ミーム枠はほぼ満杯（$939/$1000）。新規は **予備USDG1枚** か **弱い1本の回転** しかない。
- 1本が10×になっても、CASHCATの$98では足りない。3×は **PONS級が続く + 新規1本が本物**、または **既存1–2本が数倍** の形。
- 結論: 手がかりを増やすこと自体が目的ではない。**4663に実在し、Quoterで抜けられる名前だけを、枠を壊さず1枚ずつ当てる。**

EN: Twenty-four days, +$3732. Doubling WETH adds ~$550. Stock tokens are already sold. No HYPE-class alt is sitting on 4663. The meme sleeve is nearly full. A 10× on CASHCAT’s ~$98 does not close 3×. The path is **keep PONS-class convexity alive + one real new 4663 name**, or **1–2 existing names multi-bag**. More clues without a harder FACT gate only mint fake-HYPE tickets.

---

## 2. Rank / improve the three sources / 3ソースの順位と改修

Keep the existing flow: **clue → 4663 factory v3 FACT (liquidity + Quoter exit) → Chief Spot/meme ticket if present, else skip.**

Add one source that was implicit and is now first-class.

### Weight table / 重み

| Rank | Source | Weight | Role | Keep / change |
|------|--------|--------|------|----------------|
| **1 (add / promote)** | **4663 official v3 FACT: new USDG/WETH pairs + swap-log volume** | **55** | Only proof the name is tradeable *here* | **Primary discovery.** Volume spikes stay inside this bucket, not a separate religion. |
| **2 (keep, demote)** | Futures / perp / HL **top names as ticker strings only** | **20** | Attention prior, never a trade | Keep. **Drop** any use of OI, funding, mark, or size. |
| **3 (keep, narrow)** | Human weekday / time-window notes | **15** | **Reorder cadence**, not name creation | Keep. Do not let a note invent a ticker. |
| **4 (add, gate)** | Held-book relative volume / Quoter exit vs new clue | **10** | Rotate vs hold | Add. Stops cutting a live winner for a rumor. |

JP要約

1. **上げる:** 4663公式ファクトリの新規ペア監視 + スワップログ出来高。これが唯一の「ここに市場がある」信号。
2. **残すが見るだけ:** 先物トップは **ティッカー文字列の検索キー**。マッチしなければ即スキップ。資金調達率・建玉・他チェーン価格は捨てる。
3. **残すが発見源にしない:** 人間の曜日・時間帯メモは、スカウト頻度の並べ替えだけ。名前を増やさない。
4. **足す:** 保有4本の4663出来高とQuoter抜け。新規より既存が熱いなら回転しない。
5. **捨てる:** 株式トークン再 Chase、ソーシャルを一次ソースにする、他チェーンの「本物HYPE」を買う前提、ファクトリ未掲載の予約買い。

EN: Promote 4663 official v3 (new pairs + swap volume) to the only discovery engine. Keep futures as a **string dictionary**. Keep human notes as a **clock**, not a catalog. Add a held-book FACT so we do not rotate PONS for a ghost. Drop stock-token re-entry, social-as-primary, and “it will list on 4663 soon” tickets.

### Suggested clue record (no addresses) / 手がかりレコード案

Concept file (lab-private, not this public repo): `HOT_NAME_CLUES.json`

```text
{
  "as_of_jst": "...",
  "name": "TICKER",
  "source": "v3_volume | factory_new_pair | futures_ticker | human_window",
  "source_weight": 55 | 20 | 15 | 10,
  "official_4663_v3_fact": "pass | fail | not_checked",
  "quote_side": "USDG | WETH | other | none",
  "quoter_exit_for_intended_usd": "pass | fail | not_checked",
  "liq_vs_ticket": "ok | thin | unknown",
  "held_overlap": "none | PONS | NUDES | NEKO | CASHCAT",
  "action": "draft_for_chief | skip | rotate_candidate",
  "skip_reason": "no_factory | thin_exit | fake_ticker | other_chain_only | kill_cushion"
}
```

Do not store keys, session material, or invented addresses. If `official_4663_v3_fact != pass`, action is **skip**.

---

## 3. Tactical USDG vs chase / 戦術USDGの置き方

Idle USDG ~$287. Kill cushion ~$690. M3 already aborted on low USDG. Sleeve room left ≈ $60 before the $1000 cap — so a **new 5th name is economically wrong even before the grandfather rule**.

### Split (adopt) / 分割（採用）

| Bucket | USD | Rule |
|--------|-----|------|
| **Never-touch reserve** | **$80–100** | Gas to 9/30 + kill airbag + “do not repeat M3”. Never arms a ticket. |
| **Armed-ready (1 ticket)** | **$100** | Only after FACT pass. One $75–100 Spot/meme ticket. Prefer $75 if Quoter exit is tight. |
| **Buffer / second look** | **~$90–100** | Not a second simultaneous name. Becomes a **second ticket only after** (a) first fill marks via Quoter, (b) reserve still intact, (c) rotation USDG arrived, or (d) sleeve room exists. |
| **WETH** | hold | Do **not** sell WETH to fund a rumor. It is the only listed beta and the gas-adjacent stack. Sell WETH only if a FACT name is clearly superior **and** kill math still holds. |

JP

- 手がかりが当たっても **一度に1枚。** 287を全振りしない。
- ミームが半値かつ新規$100がゼロ、だと MTM は kill 近傍まで落ち得る。だから予備は残す。
- 2枚目は「予備を削る」のではなく、**弱い既存を売って得たUSDG** か、1枚目の確認後。
- 目標は3×でも、kill $1223 を割ったら実験終了。3×より生存。

EN: Chase with **one ticket**, not the whole $287. A 50% meme drawdown plus a dead new $100 ticket can press the kill floor. The second ticket is funded by a **rotation sell**, not by eating the reserve. Survival beats a heroic all-in that prints M3-abort again.

### When a 4663 match appears / マッチ時のサイズ

1. FACT pass (factory pair + Quoter full intended size + USDG or WETH quote).
2. Chief arms **one** ticket ≤ $100.
3. Recheck idle USDG ≥ never-touch after gas.
4. If sleeve would exceed $1000, **rotate first**, do not add.
5. If MTM < ~$1500 (cushion < ~$280), **freeze new risk**; only reduce.

---

## 4. Rotate vs 5th name / 回転 vs 5本目

**Do not add a 5th name.** Grandfather max ~4. High-convexity max 3. Sleeve is already $939/$1000. A 5th name is a mandate break **and** a convexity leak.

### Rotation policy / 回転方針

| Priority | Name | Bias | Why |
|----------|------|------|-----|
| Keep | **PONS** | Last to cut | Only live convexity. Cutting it to “make room” is how 3× dies. |
| Hold | **NUDES** | Hold unless a clearly better FACT | Flat, not broken. Needs 4663 volume death before it is funding. |
| Cut-2 | **NEKO** | Rotate if still red / no own spike | Slightly underwater; do not average. |
| Cut-1 | **CASHCAT** | **First rotation donor** | Smallest notion, ~flat, uses a slot that high-convexity max-3 already wants back. |

Rules

- 回転トリガー（全部必須）:
  1. 新規手がかりが **4663公式v3 FACT pass**（ファクトリ＋Quoter intended size）。
  2. 切る側に **直近の自前出来高スパイクがない**。
  3. 売却後に **武装$100 + 予備$80–100** が残る（ガス込み）。
  4. 売却も公式v3、無制限approveなし、Chief武装。
- 高凸なら **4→3** を lag ではなく目標にする。CASHCATを切って新規1本、が標準形。
- 弱い3本を同時に売って1本に全寄せしない。一度に1本。killとスリッページを守る。
- 新規が「先物では熱いが4663 FACT fail」なら **スキップ**。枠を空けない。

EN: Rotate, don’t expand. Standard shape: **sell CASHCAT → one FACT ticket**, book stays at 4 or goes to 3. Do not triple-sell into one name. Do not vacate a slot for a futures-only ghost.

---

## 5. Scout checklist / スカウト点検表

### Inputs (allowed) / 入力（許可）

- Official **4663** Uniswap v3 factory: new pools whose quote side is **USDG or WETH**.
- Public 4663 swap logs / public DEX: notional and trade-count spikes, **multi-block**, not one-block fireworks.
- QuoterV2 **full intended size** exit (same method as public marks). Thin book = fail.
- Futures / HL / other-venue **top movers → ticker string list only**.
- Human weekday / session notes (JST morning, US overlap, weekend).
- Held book: PONS / NUDES / NEKO / CASHCAT Quoter marks + their 4663 volume.
- Mandate tape: kill floor, idle USDG, sleeve cap, max names, Autofill OFF.

### Inputs (forbidden) / 入力（禁止）

- Perp marks as portfolio marks.
- Other-chain pool addresses as “the” token.
- Social follower counts as FACT.
- Invented or remembered-from-another-chain addresses.
- Bridged wrappers, unlimited approve “so the next ticket is faster”.

### Cadence / 頻度

| Window (JST) | 4663 factory + volume | Futures ticker pull | Human reorder |
|--------------|----------------------|---------------------|---------------|
| Weekday 08:00–11:00 | Every **1–2h** | 2× (open + mid) | Raise priority |
| Weekday 21:00–01:00 (US overlap) | Every **1–2h** | 1–2× | Raise priority |
| Other weekday | Every **4h** | 1× | Normal |
| Weekend / holiday | Every **2–4h** | **0–1×** (low value) | 4663-native only |

On any clue: **FACT immediately**, before a ticket draft. No batch of five drafts. One name, one FACT, one Chief decision.

Daily close (short): pass/fail counts, skip reasons, idle USDG, distance to kill, distance to $5645. No secrets.

### False-positive traps / 偽陽性

| Trap | Why it looks like alpha | Kill it with |
|------|-------------------------|--------------|
| **Fake HYPE / ticker twins** | Same letters as a famous perp | Official 4663 factory pair. No pair → skip. Do not “use the other-chain contract”. |
| One-block volume spike | Wash / seed / screenshot | Persist across **several blocks / >1h**. Quoter still must exit. |
| USDG-less exotic quote | “New pair!” | Quote must be **USDG or WETH**. Other quote = skip. |
| Thin 0.3% / 1% pool | TVL screenshot | QuoterV2 **intended $75–100** fails → skip. Do not size down below useful convexity just to force a fill. |
| Stock-token replay | NVDA/AMZN tape familiarity | Already sold. Low convexity on this venue. Not a 3× path. |
| “Lists tomorrow” | Narrative | No factory today → **no ticket today**. |
| Bridge / wrap to “real” market | Get the real HYPE | **Never.** Venue lock is 4663 v3 Spot. |
| Average-down NEKO/CASHCAT | “cost basis hygiene” | Sleeve full; violates 1-ticket discipline. Rotate or hold, don’t add. |
| 5th name “just a canary” | Small notion | Slot + sleeve + grandfather all say no. |
| Unlimited approve | Ops convenience | Hard ban. Exact-size approve only, Chief-armed. |

---

## 6. What NOT to do / やってはいけない（アルファに見えるもの）

Looks smart. Breaks the lab.

- Trade **perp / futures / Hyperliquid / any chain ≠ 4663**. `perp_pct = 0` is locked. Futures are **clues only**.
- **Bridge**, wrap, or hop to buy the “real” ticker.
- **Leverage**, borrow, or LP re-entry (`lp_pct = 0`, LP EXITED/CLEARED).
- **Unlimited approve** or Autofill ON.
- Arm a ticket **without** official 4663 v3 factory FACT + Quoter exit.
- Mark the book with futures/other-chain prices.
- Invent or paste **unverified token addresses**.
- Spend below **kill floor** or spend the never-touch USDG.
- Sell **all** memes in one burst to “go concentrated”.
- Re-buy **stock tokens** as a 3× plan.
- Sell **PONS** first to fund a rumor.
- Add a **5th** name, or a 4th high-convexity name when max is 3.
- Dump **WETH** to chase a FACT-fail clue.
- Size > **$100/ticket** or sleeve > **$1000**.
- Treat Scout output as an order. **Chief arms.**

---

## 7. One-page operating loop / 運用ループ（1枚）

```text
[clock] human window raises/lowers scan rate
    ↓
[clue] 4663 new pair / 4663 volume  >>  futures ticker string  >>  (never social-first)
    ↓
[FACT] official 4663 v3 factory + USDG/WETH quote + Quoter exit(intended USD)
    ↓ fail → SKIP (do not reserve a slot)
    ↓ pass
[slot] names >= 4 or sleeve + ticket > 1000?
    ↓ yes → rotate CASHCAT (else NEKO) via Chief sell, refill USDG, keep reserve
    ↓ no  → use armed-ready $100 only
[arm]  Chief ticket, Autofill OFF, exact approve, 4663 v3 Spot only
    ↓
[after] remake marks via Quoter; idle USDG ≥ $80–100; MTM vs $1223.10 and $5645
```

If no FACT pass all day: **do nothing**. Holding WETH + PONS + $287 USDG is a valid 3× day. Forced tickets are how the kill floor gets paid.

---

## 8. Honesty about 3× / 3×についての正直さ

3× is **possible only if 4663 lists and trades a real convex name** (or PONS/NUDES-class already held rerate hard). Scout cannot manufacture that listing. Scout **can** refuse fake HYPE fast enough that the $100 powder and the PONS slot are still there when the real pair prints.

Success metric for this design is not “more clues.” It is:

1. **Zero** FACT-fail tickets.
2. **Zero** 5th names.
3. Reserve USDG still there on 2026-09-30 or at kill review.
4. When a real 4663 pair appears, Chief has **one clean $100** and a pre-agreed rotation donor (CASHCAT).

---

## Constraints recap / 制約再掲

- Trade **only** Robinhood Chain Mainnet **chainId 4663** Uniswap v3 Spot.
- Perp / futures / HL / other chains: **never trade**.
- No leverage, no bridge, no unlimited approve.
- Kill floor: MTM < **$1223.10**.
- Autofill **OFF**. Chief arms.
- No secrets. No fake on-chain addresses.
