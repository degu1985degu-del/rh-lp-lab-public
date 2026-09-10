# SOL-LIGHTER-PERP-UNLOCK-CHECKLIST

Sol / RH Autonomous LP Lab — **prep ONLY**  
Date: 2026-09-06 · Status: **NOT LIVE POLICY · NOT A TICKET · NOT EXECUTION**

Autofill OFF, kill floor MTM `< $1223.10`. Agent does **not** send orders.  
**2026-09-06 human FINAL (deposit):** `docs/SOL-LIGHTER-DEPOSIT-CANARY-APPENDIX.md` — **FILLED** ($50, account 23139).  
**2026-09-06 human: proceed to order canary:** copy-paste packet is `docs/SOL-LIGHTER-ORDER-CANARY-APPENDIX.md` — one isolated ≤2x ETH-PERP or BTC-PERP open then close. No secrets. No unlimited approve / bot bridge.

Labels: **FACT** = official docs / L2BEAT / first-party API. **INFERENCE** = labeled why. **UNKNOWN** = do not trade on it.

No secrets. Do not invent a second Lighter address. Do not use Lighter Core (Ethereum/USDC) contracts on this lab.

---

## 0. 日本語サマリ（Chief / human）

- **Lighter-on-Robinhood は実在する（FACT）。** 4663上の公式契約 `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d` に USDG を預け、マッチは別インスタンス（Lighter Domain）。Uniswap v3 AMM パープではない。
- **RH Wallet 経路は isolated only（FACT）。** API 側は isolated と cross の両方を記述。草案は **isolated 強制**。
- **USDG が quote 兼マージン（FACT）。** perps 口座へ預けられるのは USDG のみ。approve 先は上記 Lighter 契約。金額は **6 decimals**。
- **地理制限（公式ニュースルーム開示）:** Wallet 分散型perpは **US / UK / Canada / Switzerland / UAE / Singapore** ほか制限地では不可。ラボ解禁の **ゲート0** は法域確認。未確認なら FINAL しない。
- **取引は 4663 の `swap()` ではない（FACT）。** 入金・（任意で）`ChangePubKey` は EVM。注文は `api.rh.lighter.xyz` + Lighter API 鍵。Alchemy セッションだけでフル周回できるかは **UNKNOWN**（API鍵の紐付けは L1 オーナー署名が必要、公式）。
- **リスクはレバ＋清算＋資金調達＋オラクル＋アップグレード／オペレータ。** 現本 ~$2k、kill `$1223.10`。カナリアは **≤ $50 USDG / 最大 2x / 1本** を提案。
- **入金カナリアは FILLED。** 注文カナリアの手順は `docs/SOL-LIGHTER-ORDER-CANARY-APPENDIX.md`。無制限 approve・bot ブリッジ・Autofill は禁止のまま。エージェントは注文しない。

---

## 1. FACT inventory

### 1.1 What this instance is

| Item | Value | Source |
|------|-------|--------|
| Product | Dedicated **Lighter Domain** on Robinhood Chain. **Not Lighter Core** (own contracts, sequencer, blockspace, liquidity) | [docs.robinhood.com/chain/lighter-domains](https://docs.robinhood.com/chain/lighter-domains/) |
| Host chain | Robinhood Chain mainnet **chainId 4663** | Official connecting + lighter-domains |
| Lighter app-chain IDs (API) | `466324` (their mainnet), `300` (testnet) — **not** 4663 | [apidocs.rh.lighter.xyz get-started](https://apidocs.rh.lighter.xyz/docs/get-started) |
| Architecture | App-specific ZK rollup **hosted on** 4663; USDG instead of USDC | [L2BEAT Lighter on Robinhood](https://l2beat.com/layer2s/projects/lighter-robinhood) |
| Public UI | https://robinhoodchain.lighter.xyz | official lighter-domains |
| API | https://api.rh.lighter.xyz/ · docs https://apidocs.rh.lighter.xyz/docs/get-started | official |
| Wallet UX | Robinhood Wallet perps hub (tech provider; user signs) | [Wallet perpetual futures](https://robinhood.com/us/en/support/articles/robinhood-wallet-perpetual-futures/) |
| TVS (L2BEAT, fetched 2026-09-06) | ~$58M | L2BEAT |

### 1.2 Contracts (4663)

Official RH **Lighter Contract** (same address L2BEAT names as the rollup / escrow):

| Role | Address | Source |
|------|---------|--------|
| **Lighter / deposit-withdraw / “Relayer” system** | `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d` | official lighter-domains + L2BEAT + RH API deposit docs |
| ZkLighterVerifier | `0xe1aFBE2D670eFF0e7C8A41F080792C011916ac31` | L2BEAT |
| Governance | `0xf6F6Bd6eEA2b9A2041328732CcAe4c5e1DD278B7` | L2BEAT |
| UpgradeGatekeeper | `0x43CfF77CD060A155dCe5deb12B93b875f69F2716` | L2BEAT |
| DesertVerifier (escape) | `0x56aeED6920DBB9E198C2C0072147A45684A06E10` | L2BEAT |
| USDG (canonical) | `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` | [docs.robinhood.com/chain/contracts](https://docs.robinhood.com/chain/contracts/) + L2BEAT `assetIndex` 3 |
| WETH (canonical; **not** perp quote) | `0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73` | official token contracts |

Wallet copy says “Lighter Relayer Smart Contract.” Official chain docs name one **Lighter Contract** at `0x94bA…fF9d`. Treat **Relayer = this contract** unless a later official page splits them (**INFERENCE**, high). Do not approve a third address.

Explorer: https://robinhoodchain.blockscout.com/address/0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d  
L2BEAT: https://l2beat.com/layer2s/projects/lighter-robinhood

### 1.3 USDG on 4663 (what it does here)

| Fact | Detail |
|------|--------|
| Canonical stable | Official token list: USDG `0x5fc5360D…d168` |
| Perp quote + margin | L2BEAT + Wallet article + RH Lighter API: this fork uses **USDG not USDC** |
| Deposit decimals | Official: **1 USDG = 1e6 (6 decimals)** |
| Perps route | `_routeType = 0` → perps account. `_routeType = 1` → spot account. **Only USDG can be deposited to perps** |
| Asset index | Official example + L2BEAT `QUOTE_ASSET_INDEX`: **3** |
| Min deposit | Official API: **1 USDG** (and equivalent for other ERC-20s on non-perp routes) |
| Approve | Official API: if not ETH, **approve the Lighter contract** to spend that ERC-20 |
| In the lab book | Public snap 2026-09-06 ~09:51 JST: idle USDG **~$844**, MTM **~$1974**, memes ~$1108. USDG is also Uniswap quote and kill-floor cash |

Stock-token margin on Lighter appears in secondary press. **Canary must be USDG-only** until official RH/Lighter assetDetails is re-read on FINAL day. Other `assetIndex` rows on L2BEAT are **not** a license to deposit them as perp margin.

### 1.4 Deposit / settle / withdraw flow (FACT)

```text
[4663 wallet USDG]
    -- exact approve --> Lighter 0x94bA…fF9d
    -- deposit(_to, assetIndex=3, routeType=0, amount) --> credited Lighter perps account
    -- orders via API / Wallet (NOT Uniswap router) --> isolated (Wallet) or isolated/cross (API)
    -- close --> margin returns to Lighter trading-contract balance (still NOT wallet)
    -- withdraw --> USDG back to 4663 wallet
```

**Direct deposit (preferred for RH Wallet, official):**

```text
deposit(address _to, uint16 _assetIndex, uint8 _routeType, uint256 _amount) payable
```

- Anyone may call `deposit` **on behalf of** `_to`. First deposit creates the account.
- This is inventory of the official ABI, **not** a go-ahead to send it.

**Intent / cross-chain deposit (official, exists):** `createIntentAddress` then send USDG to that address. API also documents CCTP-style intent. **Lab bot-bridge ban: do not use this path.** Stay same-chain 4663 USDG already in the wallet.

**Withdraw (official RH + API):**

| Mode | Official note | Extra signer |
|------|----------------|--------------|
| Fast | RH docs: RH Chain soft finality, near-instant. API: USDG only, min 1 USDG | API: also needs **wallet L1 key** (can send to other addresses) |
| Secure | RH docs: standard L2 full finality. API: can be called on contract `withdraw`; API key can do secure withdraw **only to the same L1 that created the account** | Same-address secure: API key may suffice |

Wallet UX: close ≠ withdraw. Funds sit on the Lighter balance until a separate withdraw.

**Settle of fills:** matching is on the Lighter instance; 4663 contract verifies ZK batches (L2BEAT). User does not “settle a Uniswap swap.”

### 1.5 Margin modes

| Path | Mode | Source |
|------|------|--------|
| Robinhood **Wallet** | **Isolated only.** One position’s loss does not take other positions or leftover USDG on Lighter | Wallet article FACT |
| Lighter **RH API** | Documents **both isolated and cross**. Isolated fees can pull from cross to keep a position healthy | [account-types](https://apidocs.rh.lighter.xyz/docs/account-types.md) FACT |
| Leverage | Wallet example uses 5x; “leverage can’t be decreased after opening.” Levels differ by underlying | Wallet article |
| Liquidation waterfall | Healthy → pre-liq → partial (≤1% fee to LLP) → full (LLP takes remainder) → ADL | Wallet article |

**DRAFT rule:** even if the API allows cross, lab canary is **isolated-only, Wallet-equivalent**. Cross is a later FINAL question, default no.

### 1.6 Official geo restrictions

First-party newsroom disclosure (2026-07-01, updated 2026-07-30): decentralized Wallet perps on Lighter are **only for eligible clients in permitted jurisdictions** and **not available to residents of the U.K., US, Canada, Switzerland, UAE, Singapore, and other restricted jurisdictions**.  
https://robinhood.com/us/en/newsroom/robinhood-accelerates-global-expansion-robinhood-chain-mainnet-stock-tokens-agentic-trading/

Wallet article: “Restrictions and eligibility requirements apply.”

**UNKNOWN (must clear before FINAL):** whether *this lab wallet / operating human / session IP / RPC exit* is in a permitted jurisdiction. A 4663 address alone does not prove eligibility. If UNKNOWN remains UNKNOWN, **do not FINAL.**

### 1.7 Points (not a reason to unlock)

Newsroom: 11M LIT reserved; **2× points via Robinhood Wallet**, 1× via Lighter web. Wallet article: Lighter runs the program; Robinhood does not. Points must not drive size.

---

## 2. What an Agent Wallet / Alchemy session would need

Prep map only. **No session widening, no key creation, no approve, no deposit in this memo.**

### 2.1 Two different machines

| Layer | What it is | Signs with | Can it place a perp? |
|-------|------------|------------|----------------------|
| **4663 EVM** | USDG `approve` + `deposit` / `withdraw` / optional `ChangePubKey` on `0x94bA…` | EOA, 4337 UserOp, or 7702 session that is allowed to touch those selectors | No. Only moves USDG in/out |
| **Lighter instance** | Orders, cancels, funding, most account ops | Lighter **API key** via `SignerClient` → `send_tx` on `api.rh.lighter.xyz` | Yes, after account exists |

Official get-started: creating/cancelling orders is **not** a 4663 Uniswap call. App-chain IDs `466324` / `300`.

### 2.2 Contracts / approve targets (if FINAL ever happens)

| Action | Target | Allowance rule (DRAFT) |
|--------|--------|------------------------|
| USDG approve | **only** `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d` | Exact canary size (+1 USDG dust), **never unlimited** |
| `deposit` | same | `assetIndex=3`, `routeType=0`, `_to` = lab wallet |
| `withdraw` / secure withdraw | same | `_to` = lab wallet only |
| Uniswap / Morpho / Arcus / Permit2 | — | **No new spenders** for this path |
| Intent / CCTP / createIntentAddress | — | **Forbidden** (bridge) |

### 2.3 UI vs pure EVM vs API

| Surface | Deposit | Trade | Withdraw | Notes |
|---------|---------|-------|----------|-------|
| **Robinhood Wallet UI** | 4663 tx, on-device sign every step | On-device sign; isolated only; market/limit; TP/SL copy is **internally inconsistent** in the same article (see UNKNOWN) | Separate withdraw sign | Circuit breaker if Lighter API/engine down |
| **robinhoodchain.lighter.xyz** | Official public UI | API-backed | UI | Same instance, not Core |
| **Pure EVM** | `approve` + `deposit` FACT | **Cannot** place perps by calling Uniswap or a 4663 “openPosition” we can name | Secure `withdraw` exists on contract (API docs) | Fast withdraw / transfer need L1 key (API) |
| **lighter-sdk + api.rh.lighter.xyz** | No; deposit is 4663 | FACT path for bots | Fast/secure via SDK; secure-to-self can be API key | API key bind needs **L1 owner** (`ChangePubKey`) |

### 2.4 Alchemy / AA / session — honest UNKNOWN

Official [Account Abstraction](https://docs.robinhood.com/chain/account-abstraction/): 4663 has ERC-4337 + EIP-7702; Alchemy is the recommended programmable-wallet stack (batching, spend policies, gas sponsorship, session keys). EntryPoint addresses are published. Connecting docs also name Alchemy gasless infrastructure.

| Question | Status |
|----------|--------|
| Is the **lab** wallet an EOA, 4337 smart account, 7702-delegated EOA, or Privy/Alchemy embedded? | **UNKNOWN** (not in this public repo). Must be written on the FINAL packet |
| Can a session key `approve`+`deposit` USDG to `0x94bA…` under a spend cap? | **INFERENCE:** Alchemy session ERC-20 permissions can cap cumulative transfer/approve. Not lab-tested |
| Can a session key register a Lighter API key? | Official: generating the key does not need L1; **associating it does** (`ChangePubKey` or SDK). Session-without-owner = **UNKNOWN / likely no** |
| Can a session key place Lighter orders? | Only after a bound API key exists. Whether that API private key may live in an agent host = **policy UNKNOWN** (secret-handling, not a chain fact) |
| Fast withdraw from session-only? | Official: needs **wallet L1 key**. Treat as **no** unless proven |
| Does RH Wallet “every action on-device” apply to Alchemy agents? | That sentence is **Wallet UX FACT**. Agent path is the API, not that UI |
| Gas sponsorship for `deposit`? | AA docs show paymaster patterns. Whether lab paymaster may sponsor Lighter calls = **UNKNOWN** |
| Will Lighter `deposit` from a 4337 sender credit the right `_to`? | Official: anyone can deposit for any `_to`. Still **must test on shadow**, not assume |

**Prep implication:** an Agent Wallet is enough to *draft* a capped 4663 deposit **after FINAL**. It is **not** proven sufficient to trade or fast-withdraw without an owner-bound Lighter API key. Do not “just enable Autofill” to paper over that.

---

## 3. Risk (and kill-floor math)

Public book ~2026-09-06 09:51 JST: MTM **~$1974**, B0 $1881.69, 3× $5645, idle USDG **~$844**, memes ~$1108, native ETH ~$22, **kill $1223.10**, cushion **~$751**.

### 3.1 Market / protocol

| Risk | FACT / note | Kill-floor interaction |
|------|-------------|-------------------------|
| **Liquidation** | Wallet: 5x, −20% underlying can zero the isolated margin. Waterfall to LLP / ADL. Robinhood cannot reverse | Isolated canary loss ≤ deposited $X. Cross would couple to leftover Lighter USDG — **do not enable** |
| **Funding** | Hourly, peer-to-peer. Persistent adverse funding eats isolated margin | Small $X still dies slowly if left open. Halt if funding is the thesis |
| **Leverage lock** | Cannot decrease after open | Cap **max 2x** on canary so a 20% move is not instant zero (5x example in their own article) |
| **Oracle** | L2BEAT: index oracles; signatures **not** checked on the settlement contract; sequencer trusted | Wrong mark → wrong liq. No lab hedge |
| **Operator / MEV** | Centralized batch posters; L2BEAT: operator can frontrun | Accept as venue risk or do not unlock |
| **Upgrade** | Gatekeeper 21d delay; **Security Council can set delay to 0**. L2BEAT still flags instant upgrade / theft | Halt on upgrade notice |
| **Host L2** | 4663 FCFS Orbit; L2BEAT combined row: sequencer failure “no mechanism,” filtered force-include | Desert/escape is slow and technical — not a canary exit plan |
| **Rollup / withdraw** | Fast vs secure; close ≠ wallet. Outage: Wallet cannot trade/close | **Never** put more USDG on Lighter than the canary cap. Keep never-touch USDG in the 4663 wallet |
| **Bridge / intent** | Official path exists | Using it is a **policy break**, not a risk to “accept” |
| **Geo / eligibility** | Official restricted list | Trading while restricted is not an alpha trade |
| **Delist** | Wallet: position closed at mark | Canary only on ETH/BTC-style names they already document |
| **Points** | Lighter-discretionary | Ignore for sizing |
| **UI contradiction** | Same Wallet article both describes attaching TP/SL **and** says automated TP/SL “aren’t available” | **UNKNOWN** which sentence is current. Do not rely on TP/SL as a kill-floor control |

### 3.2 Canary vs kill (why $50)

Need: leftover MTM after **canary = 0** and a **meme −40%** still `> $1223`.

`1974 − 50 − 0.40×1108 ≈ 1481` → cushion remains ~$258.  
`1974 − 100 − 0.50×1108 ≈ 1320` → thin.  
`1974 − 200 − 0.50×1108 ≈ 1220` → **at/under kill**.

Also keep never-touch USDG **$80–100** in-wallet (gas + M3 lesson), not on Lighter.

**Proposed canary $X = $50 USDG** (hard ceiling $75 before any “scaled” talk). Max leverage **2x** ⇒ notional ≤ $100. One isolated position. Loss of the whole canary is ~2.5% of book and ~7% of kill cushion.

3× ($5645) is **not** the canary’s job. Canary proves: deposit credits, isolated fill, mark/funding read, withdraw returns USDG, Auditor packet works, kill math holds.

---

## 4. POLICY amendment **DRAFT** (not FINAL)

Live file of record remains `perp_pct=0`. The table is what a future FINAL *could* say. Human must adopt it in a separate mandate.

### 4.1 What would change vs today

| Knob | LIVE today | DRAFT (canary only) |
|------|------------|---------------------|
| `perp_pct` | **0 locked** | Still **0** until FINAL. After FINAL: **≤ 3** *or* **≤ $50**, whichever is tighter |
| Venue | 4663 Uniswap v3 Spot only | Add **Lighter-on-Robinhood only** (not Core, not Arcus, not HL, not RH brokerage Futures, not EU app perps) |
| Chain for funds | 4663 | 4663 USDG in/out only. **No** intent/CCTP/canonical bridge |
| Margin | n/a | **Isolated only.** No cross. No stock-token margin |
| Max leverage | n/a (banned) | **2x** canary. Not increased without a new FINAL |
| Size | n/a | **≤ $50** USDG deposited on Lighter at once. Min official 1 USDG |
| Positions | n/a | **1** isolated. Names: ETH-PERP or BTC-PERP (Wallet examples) until a later list |
| Approvals | exact, no unlimited | Exact USDG to `0x94bA…fF9d` only. Revoke after withdraw |
| Ticket arming | Chief arms Spot/meme | Same **plus** Lighter deposit/order/withdraw are **three tickets**. Autofill **OFF** |
| Who authorizes | Chief arms; no Autofill | **Human FINAL** on the mandate, then Chief arms each ticket, then human confirms the signed payload. Agent/Scout may **draft only** |
| Marks | QuoterV2 exit | Wallet MTM = 4663 Quoter book + idle USDG + ETH + **Lighter equity (API)**. Never mark with HL/CME |
| Sleeve math | spot 52 / meme 46 / gas 2 / perp 0 / lp 0 | Canary sits inside **gas/cash**, not meme sleeve. Do not fund Lighter by selling PONS |

### 4.2 Explicitly **keep** (even after a future FINAL)

- No **bot bridge** (intent address, CCTP, LZ, canonical withdraw-to-L1, Relay, …)
- No **unlimited approve**
- No Autofill
- No borrow / Morpho loop / LP re-entry unless a different FINAL
- **Human FINAL required before any live ticket**
- Kill floor **$1223.10** unchanged
- Secrets stay out of this public repo and out of Scout transcripts

### 4.3 Auditor checks (every Lighter ticket, if FINAL)

1. Mandate PDF/note says FINAL and cites this checklist version.  
2. Geo/eligibility attestation attached (**UNKNOWN** today → fail).  
3. Spender == `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d`. Allowance ≤ canary.  
4. `deposit` calldata: `assetIndex=3`, `routeType=0`, `_to` = lab address, amount ≤ $50 (6 decimals).  
5. No intent/bridge payload.  
6. Isolated, leverage ≤ 2, one market, reduce-only on close.  
7. Pre/post MTM vs $1223.10 and vs never-touch USDG ≥ $80 in **wallet** (not on Lighter).  
8. After close: withdraw ticket; Lighter available margin → 0; 4663 USDG increased; approve revoked.  
9. No Lighter API private keys in public artifacts.

### 4.4 Halt rules (DRAFT)

Halt new Lighter risk (and flatten if already in, via Chief+human tickets) if any:

- Wallet MTM `< $1500` (cushion `< ~$280`)  
- Any partial/full liquidation or ADL  
- Lighter API / Wallet “exchange unavailable”  
- UpgradeGatekeeper delay cut, or unexpected `ChangePubKey`  
- Funding or mark dislocation vs 4663 WETH/USDG that Auditor cannot explain  
- Idle wallet USDG `< $80`  
- Geo status becomes UNKNOWN/restricted  
- Human or Chief says stop  

Flattening still requires human-signed tickets. No hidden Autofill flatten.

---

## 5. Phased unlock

| Phase | Name | Allowed | $ / action | Exit criteria into next |
|-------|------|---------|------------|-------------------------|
| **0** | Research | This file + landscape memo. Read-only API (`accounts_by_l1_address`, `assetDetails`, `orderBookDetails`) | $0 | Human says phase 1 |
| **1** | Shadow / paper | Watch ETH-PERP & BTC-PERP marks/funding. Paper isolated 2x $50. **No approve, no deposit, no API key bind** | $0 | 5–10 sessions logged; Auditor template filled; geo resolved |
| **2** | Canary | **Only after written FINAL.** Exact approve + deposit **≤ $50**. One isolated ≤2x. Then close + withdraw + revoke | **$X = $50** (cap $75) | Round-trip USDG ± fees accounted; no halt trip; kill intact |
| **3** | Scaled | New FINAL only. Not designed in this memo | n/a | Do not pre-commit. 3× is still mostly a 4663 spot-meme problem |

Phase 0–1 may run **now** under live `perp_pct=0`. Phase 2+ is illegal under live policy until FINAL.

Suggested canary packet (still not a ticket): `$50 USDG`, `2x`, isolated, ETH-PERP **or** BTC-PERP, hold minutes-to-hours not overnight if funding is ugly, then withdraw.

---

## 6. Do-not list until FINAL

- Do not change live `perp_pct`, Autofill, or session spend policies.  
- Do not `approve` / `deposit` / `ChangePubKey` / `createIntentAddress`.  
- Do not bind a Lighter API key to the lab address.  
- Do not send USDG to any “relayer” other than the official `0x94bA…fF9d` (and not even that until FINAL).  
- Do not use **Lighter Core** USDC/CCTP flows or `mainnet.zklighter.elliot.ai`.  
- Do not use Arcus **perps**, HL, RH brokerage Futures, or EU app perps as a “substitute unlock.” Spot-only Arcus packet (if ever FINAL): `docs/SOL-ARCUS-CANARY-APPENDIX.md`. Lighter $50 stays; no Fun/bridge.  
- Do not bridge “to get more USDG” or to reach Core liquidity.  
- Do not unlimited-approve Permit2 / Universal Router “so Lighter is easier.”  
- Do not enable cross margin, stock-token margin, or >2x “because Wallet shows 5x.”  
- Do not size canary from idle $844. Most of that is kill + meme dry powder.  
- Do not sell PONS/NUDES/NEKO to fund a perp canary.  
- Do not treat points/LIT as mandate.  
- Do not mark the book with Lighter while `perp_pct=0` and nothing is deposited.  
- Do not write Scout/Autofill playbooks that skip Chief + human FINAL.  
- Do not publish API private keys, session material, or Alchemy policy IDs.  
- Do not assume TP/SL will save the kill floor.  
- Do not skip geo. If restricted, the path **stops at phase 1 forever**.

---

## 7. Open UNKNOWN (block FINAL)

1. Lab wallet type (EOA / 4337 / 7702 / embedded) and whether the operator is geo-eligible.  
2. Relayer vs `0x94bA…` identity if RH later publishes a second address.  
3. Wallet TP/SL contradiction.  
4. Whether `deposit` from a 4337/session sender credits `_to` the same in production.  
5. Live `assetDetails` — confirm index 3 still USDG on FINAL day.  
6. Whether RH Wallet isolated-only is enforced at the contract or only in the app (API describes cross).  
7. Fast-withdraw failure modes on this instance (API text sometimes says “Arbitrum”; RH docs say RH Chain soft finality).  
8. Exact max leverage per market on the RH instance (Wallet says it varies).

---

## 8. Sources

- [Lighter Domains](https://docs.robinhood.com/chain/lighter-domains/) — contract, UI, API, `deposit`, intent, fast/secure withdraw  
- [Token contracts](https://docs.robinhood.com/chain/contracts/) — USDG / WETH  
- [Account abstraction](https://docs.robinhood.com/chain/account-abstraction/) — Alchemy / 4337 / 7702  
- [Wallet perpetual futures](https://robinhood.com/us/en/support/articles/robinhood-wallet-perpetual-futures/) — isolated, funding, waterfall, deposit/withdraw UX  
- [Newsroom 2026-07-01](https://robinhood.com/us/en/newsroom/robinhood-accelerates-global-expansion-robinhood-chain-mainnet-stock-tokens-agentic-trading/) — geo list, LIT points  
- [RH Lighter API get-started](https://apidocs.rh.lighter.xyz/docs/get-started) · [deposits](https://apidocs.rh.lighter.xyz/docs/deposits-transfers-and-withdrawals.md) · [API keys](https://apidocs.rh.lighter.xyz/docs/api-keys.md) · [account types](https://apidocs.rh.lighter.xyz/docs/account-types.md)  
- [L2BEAT Lighter on Robinhood](https://l2beat.com/layer2s/projects/lighter-robinhood)  
- Sibling: `docs/SOL-4663-EARNING-LANDSCAPE.md`

---

*Sol. Phase 0 complete. Phase 1 = paper only. Phase 2 waits on a written FINAL from the human. Until then, `perp_pct` is 0.*
