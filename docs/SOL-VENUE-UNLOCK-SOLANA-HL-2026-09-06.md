# SOL-VENUE-UNLOCK-SOLANA-HL-2026-09-06

Sol → Chief + human  
**Advisory only.** No POLICY change. No tickets. No wallet spend.  
Date: 2026-09-06 · Axis 1 (grow money) only. Axis 2 (bot factory) is out of scope.

---

## 0. JP TLDR

**解禁順は Solana 先。Hyperliquid は並行しない。** 4663 はエッジ供給が薄い（FACT としてのオペ実感）。伸ばす金は「上場が多いスポット」に先に出す。HL はラボ egress（US-VA）が Lighter/Arcus と同じ geo 失敗を繰り返すリスクが高い。

- **Phase 0:** 4663 は HOLD＋監視。工場5分は続ける。idle USDG の大部分は RH に残す。
- **Phase 1:** 人間が **別ウォレット** に **$50（上限 $100）** を **手で** 入れる（bot ブリッジ禁止）。Solana スポット往復1本（Jupiter 等）。Chief 武装・Autofill OFF。
- **Phase 2:** Phase 1 が kill を踏まずに閉じた **あと**、HL は **許可 egress + 新 FINAL** が揃ってから $50 カナリア。今のラボ IP からは HL を解禁しない。
- 全部同時は却下。4663 ミームの短期ルールは別メモ（`SOL-SM3-SHORT-TERM-RULES-2026-09-06.md`）。Perp を「スイングの代わり」にしない。

---

## 1. Unlock order — pick one

| Option | What | Sol rec |
|--------|------|---------|
| **A. Solana first** | $50–100 spot canary, separate wallet, human-funded | **ADOPT** |
| B. HL first | Perp API from day one | Reject |
| C. Parallel sleeves | Solana $50 + HL $50 same week | Reject |

**Why A**

1. **Edge supply (axis 1).** 4663 official v3 is quiet (lab FACT: few HYPE-class alts). Solana has continuous listings. Same *class* of work the desk already knows: quote → finite approve → swap → Quoter-like exit check. Does not require a new perp mandate.
2. **Egress.** Lab IP already **geo-blocked Lighter orders and Arcus writes** (US-VA). HL from the same pipe is **likely the same class of fail** (INFERENCE; do not “test live to see”). Solana DEX HTTP/RPC is not that gate.
3. **Envelope.** One new sleeve ≤$100 keeps RH kill math ($1223.10) almost unchanged if the Solana wallet is **separate** and **not** funded from never-touch RH USDG.
4. **Parallel (C)** doubles Auditor surface (two bridges-or-onramps, two kill switches, two Autofill temptations) before one venue is proven. Human said not all chains at once.

**Why not HL first:** perps + leverage + liquidation + API keys + possible US geo/ToS. That is a **new FINAL**, not a Scout-therapy. Same reason we did not unlock Arcus perps after whitelist 403.

---

## 2. Per-venue canary design

Hard defaults for **both**: Autofill OFF · Chief arms · Executor sends · **no bot bridge** · no unlimited approve · no 5th RH meme · do not drain RH idle $844.

### 2.1 Solana (Phase 1)

| Item | Rule |
|------|------|
| **Sleeve** | **$50** first. Cap **$100**. Not from RH never-touch $80–100. Prefer **new human money** or a **human-signed** RH withdraw of ≤$50 *after* a separate FINAL (default: **new money**, leave RH $844). |
| **Wallet** | **New Solana keypair / Phantom (or equivalent).** Not `0xeb2e…4c7b`. Do not reuse RH session as “the Solana signer.” |
| **Bridge** | **Human-funded only.** CEX off-ramp → SOL/USDC on Solana, or a **human-clicked** official bridge. **Bot CCTP / Relayer / Autofill bridge = NO.** |
| **Geo / egress** | No Lighter-style API geo expected for Jupiter/RPC. Still: do not run from a sanctioned context. Lab US-VA **may** run **reads**; writes are human/Chief from the operator’s permitted machine. |
| **Tooling** | Official Solana RPC (pay for one; public 429s exist). Spot via **Jupiter** (or another named aggregator Chief picks **once**). Finite token approve to **that** program only. No random “snipe bot” binaries. |
| **What to trade** | One **round-trip** canary: USDC (or SOL) → one liquid pair → back. **Not** a meme farm. Not 10 launches. |
| **Kill** | Solana sleeve MTM **< 50% of sleeve** → flatten + halt that venue. RH kill **$1223.10** unchanged (RH book only). Do not “top up” Solana from RH to save a bag. |
| **Auditor** | (1) Wallet ≠ RH. (2) Fund path is human, not bot. (3) Spender is the named aggregator. (4) Size ≤$100. (5) One open risk at a time. (6) Flatten receipt + remaining USDC. (7) No Autofill. |

### 2.2 Hyperliquid (Phase 2 only)

| Item | Rule |
|------|------|
| **Sleeve** | **$50** isolated-style (or HL account isolated if available). Cap $100. **Separate** from Solana sleeve **and** RH. |
| **Wallet / account** | Dedicated HL-capable signer. Not the RH 4663 session. Not the Solana key. |
| **Bridge** | Human-funded USDC onto the HL path Chief names in the FINAL. **No bot bridge.** |
| **Geo / egress** | **FACT:** this lab’s US-VA egress already failed Lighter/Arcus writes. **Do not** place HL orders from that IP. Phase 2 gate = **permitted egress** (operator JP or other non-restricted) **plus** written FINAL. VPN-to-bypass: treat as **NO** (same class as Arcus ToS). |
| **Tooling** | Official HL API / app. API wallet bind is a **human sign**. No Autofill bot. |
| **What to trade** | One BTC or ETH perp, **isolated, ≤2x**, min size, open then close (same spirit as Lighter order appendix). Not a 10x desk. |
| **Kill** | Flatten if isolated margin ≤ 50% or HL mark dislocation Auditor cannot explain. Do not add RH USDG. |
| **Auditor** | (1) FINAL + permitted IP attested. (2) Isolated ≤2x. (3) $50. (4) Separate keys. (5) Close same session if canary. (6) No HL+Solana+RH tickets the same day. |

If permitted egress never arrives: **HL stays locked.** That is a valid outcome.

---

## 3. What stays on RH 4663

| Sleeve | During Solana Phase 1 |
|--------|------------------------|
| 4 memes | **HOLD + monitor** (factory 5m, dash 5m, :53). Short-term **rules** = Memo B, still 4663-only. |
| Idle USDG ~$844 | **Stay.** Never-touch $80–100. Do not fund Solana from this by default. |
| LP | EXITED. Stay exited. |
| Lighter / Arcus | No orders from lab IP. No new deposit. |
| Patch A factory | **Keep.** Quiet 4663 ≠ abandoned 4663. |
| 3× target | Still counted on **consolidated** MTM only if Chief later says so. Until then, Solana P&L is a **side sleeve**, not a silent B0 rewrite. |

---

## 4. Do not unlock everything at once

- [ ] No Solana **and** HL the same FINAL.
- [ ] No second Solana name until the first canary is flat.
- [ ] No bot bridge “just this once.”
- [ ] No moving >$100 off RH in week one.
- [ ] No Autofill on the new chain.
- [ ] No using HL to hedge 4663 meme swings (Memo B: no perp-as-fix).
- [ ] No merging keys / one session for three venues.
- [ ] No “Axis 2 bot factory” shipping a trader that skips Chief.
- [ ] No raising RH kill or B0 because Solana printed a number.

---

## 5. Phases — human ballot

### Phase 0 — RH hold (now)

**Do:** 4663 monitor + factory 5m + optional Memo B paper.  
**Success:** kill intact; no bot bridge; Scout sleeps on empty factory.  
**Fail:** Autofill or 5th meme.

### Phase 1 — Solana $50 canary

**Do:** human-fund separate wallet; one round-trip; Chief ticket.  
**Success (one sitting to accept):** (a) fund path documented human-only; (b) one flatten; (c) sleeve loss ≤$50; (d) RH MTM still >$1500 soft / $1223.10 kill; (e) Auditor checklist green.  
**Fail → stay Phase 0:** any bot bridge, unlimited approve, or second venue sneak-in.

### Phase 2 — HL $50 (optional)

**Pre-gates:** Phase 1 success **and** permitted egress **and** new FINAL.  
**Success:** isolated ≤2x open+close; no lab-US-VA writes.  
**Fail → HL locked:** geo 403, cross margin, >2x, or same-day multi-venue.

---

## 6. Chief ballot

| Item | Accept | Reject |
|------|--------|--------|
| Solana **first** (not HL first, not parallel) | **Sol: accept** | |
| Phase 1 sleeve $50 (cap $100), **new wallet**, human-fund | **Sol: accept** | |
| Default **no** RH→Solana drain of the $844 | **Sol: accept** | |
| HL only Phase 2 + permitted egress + new FINAL | **Sol: accept** | |
| Unlock HL from current lab US-VA now | | **Sol: reject** |
| Parallel Solana+HL this week | | **Sol: reject** |

---

*Sol. Thin 4663 is a venue problem. Fix with one new spot sleeve, not a perp from a blocked IP.*
