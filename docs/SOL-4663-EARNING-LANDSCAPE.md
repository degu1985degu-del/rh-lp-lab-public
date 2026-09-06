# SOL-4663-EARNING-LANDSCAPE

Sol / RH Autonomous LP Lab — **research memo only**  
Date: 2026-09-06 · Scope: **Robinhood Chain Mainnet, chain ID 4663**  
Not a policy change. Not a ticket. Not live execution.

Current lab context (unchanged): trade **4663 Uniswap v3 Spot only**; `perp_pct=0`; no bot bridge / borrow / leverage / perp; Autofill OFF; Chief arms; kill floor MTM `< $1223.10`. This note catalogs **what exists** if those bans were lifted later. It does not recommend lifting them.

Epistemic labels used everywhere below:

| Label | Meaning |
|-------|---------|
| **FACT** | Official docs, official GitHub/deploy tables, explorer-verified contract, or first-party dashboard |
| **INFERENCE** | Strong but not a primary-source one-liner; labeled why |
| **UNKNOWN** | Searched; not confirmed. Do not trade on it |

No secrets. Addresses below are copied from **named official sources**. Do not treat a ticker-twin as the same contract.

---

## 0. Executive summary / 結論

Human suspicion is **confirmed**: perp products exist around this ecosystem. They are **not** Uniswap-style AMM perps sitting in the same 4663 factory the lab already uses.

Three layers must not be collapsed:

1. **OFF-CHAIN brokerage Futures** — Robinhood app `/ES` `/NQ` etc., Robinhood Derivatives LLC / CFTC. **Not chain 4663.** [FACT](https://robinhood.com/us/en/about/futures/) [FACT](https://robinhood.com/us/en/support/articles/futures-orders/)
2. **OFF-CHAIN / app EU perpetual futures** — Robinhood Europe app+web, up to 10x, 15-minute P&L settlement, partner venue. **Not the EVM wallet path.** [FACT](https://robinhood.com/eu/en/support/articles/about-perpetual-futures/) [FACT newsroom](https://robinhood.com/us/en/newsroom/robinhood-accelerates-global-expansion-robinhood-chain-mainnet-stock-tokens-agentic-trading/)
3. **ON-CHAIN / in-ecosystem on 4663**
   - **Lighter perps: FACT.** Official chain docs list Lighter as “Perpetuals dex”. Wallet support says USDG is deposited into a Lighter contract **on Robinhood Chain**. L2BEAT describes an app-specific ZK rollup **hosted on Robinhood Chain** with a 4663 settlement contract. Matching is **not** a 4663 Uniswap pool.
   - **Arcus perps: FACT they are listed; settlement model is hybrid.** Official chain docs list Arcus as “Perpetuals dex”. Arcus docs: off-chain CLOB + permissioned appchain + **EVM rootchain custody**. Spot router contracts are published for **chain 4663**. A single official sentence “Arcus perps vault = this 4663 address” was **not** found → perps *existence in-ecosystem* is FACT; *exact perps vault address on 4663* is **UNKNOWN**.

What an EVM wallet can actually touch **on 4663** today:

| Exists | Maturity | Can a ~$2k book 3× by 2026-09-30 without bridging out? |
|--------|----------|--------------------------------------------------------|
| Uniswap v2 / v3 / v4 + UniswapX spot | Live, primary public AMM | **Only realistic 3× path** (meme / new-pair convexity). v3 is what the lab already uses. |
| Uniswap concentrated LP fees | Live (NPM on 4663) | No. Fees ≠ 3× in 24 days. IL + inventory. Lab already exited LP. |
| Rialto propAMM / Arcus spot / 0x·1inch RFQ | Live / listed | Execution venue for Stock Tokens. Not a 3× engine. |
| Morpho lend/borrow | Live; official dashboard ~$0.52B TVL | Single-digit USDG yield (Earn advertised ~7%). **Cannot 3×.** Borrow is leverage — banned now. |
| Lighter perps + points | Live for *eligible* jurisdictions | Could theoretically convexify; also the fastest way to print the kill floor. **Banned now.** |
| Arcus perps | In-ecosystem; beta / waitlist historically | Same class as Lighter. **Banned now.** Exact 4663 perps vault **UNKNOWN**. |
| Canonical + partner bridges | Documented | Existence only. Lab bot-bridge ban stays. |
| Native ETH staking / restaking | Not found | **UNKNOWN / none found** |
| Priority-gas MEV | Structurally weak | Chain is **FCFS**. Classic PGA backruns are the wrong mental model. |

**Bottom line for Chief:** the 4663 wallet already sits on the only venue that can 3× this book without leaving the chain (Uniswap spot/meme). Lending and LP are real but too slow. Perps *exist* (Lighter FACT; Arcus FACT-as-listed). They are a later-policy question, not a missing Uniswap pool.

---

## 1. Landscape table

Capital column is “typical useful size,” not a ticket. Automatable = *technically* callable by an EVM bot, not “lab should.”

| Method | On-chain 4663? | Maturity | Capital needed | Risk class | Bot-automatable? | Notes |
|--------|----------------|----------|----------------|------------|------------------|-------|
| Uniswap v3 spot swap | **Yes FACT** | High | Dust → $100 tickets | Market / thin-book | Yes (Quoter + router) | Lab venue. Official factory + QuoterV2 explorer-verified. |
| Uniswap v2 spot | **Yes FACT** | Medium | Same | Market | Yes | Official factory + Router02. Thinner than v3 for lab marks. |
| Uniswap v4 spot / hooks | **Yes FACT** | Medium | Same | Market / hook risk | Yes | Official PoolManager. Permissioned-pool hooks exist in Uniswap product line (may matter for RWAs). |
| UniswapX intents | **Yes FACT** (blog) | Medium | Same | Filler / intent | Partial | Live on RH Chain per Uniswap Labs. Reactor address not copied here (playbook fetch empty). |
| Uniswap v3/v4 LP (CL) | **Yes FACT** | High proto / low yield | $100s–$800s | IL + inventory | Yes (NPM) | Fee farm. Not 3×. Lab LP EXITED. |
| Rialto propAMM | **Yes FACT** (listed + own docs) | Medium | Swap notional | MM / routing | Yes (on-chain quote+settle) | Stock-token liquidity when AMM is thin. Router address **UNKNOWN** here (not copied from unofficial dumps). |
| Arcus **spot** (RFQ / SwapShell) | **Yes FACT** | Medium | Swap notional | RFQ / upgradeable proxy | Yes | Official ABI repo, chain 4663. |
| 0x / 1inch / LiFi RFQ | **Partial FACT** | Medium | Swap notional | Off-chain quote, on-chain settle | Partial | Stock-token docs: RFQ at launch. 1inch named in RH newsroom wallet list. |
| Morpho supply USDG | **Yes FACT** | High TVL | $10s+ | Smart-contract + borrower | Yes | Official Morpho chain page + SDK address book. Earn ~7% is **app UX** over this. |
| Morpho borrow / loop | **Yes FACT** | High TVL | Collateral | **Leverage / liquidation** | Yes | Stock tokens / WETH / memes appear as collateral *names* on Morpho dashboard. **Lab-banned.** |
| Robinhood Earn | **On-chain Morpho, app-gated FACT** | Live US roll-out | Idle USDG | Same as Morpho + eligibility | App, not raw bot | Insurance marketing is app-side. Not a new protocol. |
| Lighter perps | **Custody on 4663 FACT; matching on Lighter ZK app-rollup FACT** | Live, geo-gated | Margin in USDG | **Leverage / liq / operator** | Partial (deposit on 4663; trade via Lighter/Wallet) | See §3. **Lab-banned.** |
| Lighter Points / LIT | **Program FACT** | Live | Trade volume | Points / dilution | Via trading | 2× points through RH Wallet vs 1× Lighter web (newsroom). |
| Arcus perps | **In-ecosystem FACT; 4663 vault addr UNKNOWN** | Beta / waitlist historically | Margin | **Leverage / hybrid CLOB** | Partial | Off-chain match, EVM settle. **Lab-banned.** |
| Pools.trade launchpad | **FACT** (Uniswap Labs blog 2026-08-05) | Early | Bid / launch size | Launch / meme | Partial | 4663-native name factory. Convexity cousin of current meme path. |
| Canonical Arb bridge | **Yes FACT** | Live | Any | 7-day withdraw / retryables | Yes | Existence only. **Lab bot-bridge ban.** |
| LZ / Stargate / CCIP / Relay / Across / LiFi | **Documented FACT** | Live (partner) | Any | Bridge / messenger | Yes | Existence only. |
| Stock Tokens hold / RFQ | **Yes FACT** | Live, geo-gated | Any | RWA / issuer / hours | Yes | Low convexity. Lab already sold stocks. |
| Meme v3 hold | **Yes FACT** (lab book) | Thin | $75–$100 | Rug / thin exit | Yes | Only 3× engine without leaving 4663. |
| Native stake / restake | **Not found** | — | — | — | — | ETH is L2 gas; no 4663 beacon stake found. **UNKNOWN.** |
| Priority-gas MEV | **Structurally weak FACT** | — | — | Sequencer | Low | FCFS: higher fee cannot jump the line. |
| Cross-venue arb / basis | **INFERENCE** | Low for $2k | Inventory + gas | Inventory / revert | Possible | Uniswap vs Rialto vs Arcus spot vs Lighter mark. Size-capped. |
| CEX / RH brokerage Futures | **No — off-chain FACT** | Mature | Brokerage margin | CFTC futures | App | Clue source only for this lab. |

---

## 2. Inventory (verified as far as sources allow)

### 2.1 Spot swap / AMM

**FACT — Uniswap is the official public DEX.**

- Chain docs ecosystem table: “Public DEX = Uniswap”. [docs.robinhood.com/chain](https://docs.robinhood.com/chain/)
- Uniswap Labs (2026-07-02): **v2, v3, v4, and UniswapX live** on Robinhood Chain; Web App / Wallet / API from day one; chain ID `4663`. [blog.uniswap.org/robinhood-chain-is-live](https://blog.uniswap.org/robinhood-chain-is-live)
- Uniswap governance (temp-check): launch at 2026-07-01 mainnet debut; **>$1B cumulative swap volume by 2026-07-10**. [gov.uniswap.org](https://gov.uniswap.org/t/temp-check-protocol-fee-expansion-robinhood-chain/26168)

Official Uniswap **v3** addresses ([developers.uniswap.org v3 Robinhood deployments](https://developers.uniswap.org/docs/protocols/v3/deployments/v3-robinhood-chain-deployments)):

| Contract | Address | Explorer check (this memo) |
|----------|---------|----------------------------|
| UniswapV3Factory | `0x1f7d7550b1b028f7571e69a784071f0205fd2efa` | Blockscout **verified**, name `UniswapV3Factory` |
| QuoterV2 | `0x33e885ed0ec9bf04ecfb19341582aadcb4c8a9e7` | Blockscout **verified**, name `QuoterV2` |
| SwapRouter02 | `0xcaf681a66d020601342297493863e78c959e5cb2` | Official docs; explorer API 500 this pass |
| NonfungiblePositionManager | `0x73991a25c818bf1f1128deaab1492d45638de0d3` | Official docs; explorer API 500 this pass |
| UniversalRouter | `0x8876789976decbfcbbbe364623c63652db8c0904` | Official v3 + v4 pages |
| Permit2 | `0x000000000022D473030F116dDEE9F6B43aC78BA3` | Canonical + RH protocol-contracts |

Official Uniswap **v2** ([developers.uniswap.org v2 deployments](https://developers.uniswap.org/docs/protocols/v2/deployments)):

| Contract | Address | Explorer check |
|----------|---------|----------------|
| Factory | `0x8bceaa40b9acdfaedf85adf4ff01f5ad6517937f` | Also in Uniswap gov temp-check |
| Router02 | `0x89e5db8b5aa49aa85ac63f691524311aeb649eba` | Blockscout **verified**, name `UniswapV2Router02` |

Official Uniswap **v4** ([developers.uniswap.org v4 deployments](https://developers.uniswap.org/docs/protocols/v4/deployments), section Robinhood Chain: 4663):

| Contract | Address |
|----------|---------|
| PoolManager | `0x8366a39cc670b4001a1121b8f6a443a643e40951` |
| PositionManager | `0x58daec3116aae6d93017baaea7749052e8a04fa7` |
| Quoter | `0x8dc178efb8111bb0973dd9d722ebeff267c98f94` |
| StateView | `0xf3334192d15450cdd385c8b70e03f9a6bd9e673b` |

**FACT — other spot venues (not Uniswap):**

- **Rialto** PropAMM / aggregator — official chain ecosystem table; own docs describe on-chain `getAmountOut` + atomic `swapExactIn` via `RialtoRouter`. [docs.rialto.xyz](https://docs.rialto.xyz/developers/propamm-integration-overview)
- **Arcus spot** — official ABI repo, **Network = Robinhood mainnet, chain ID 4663**. SwapShell `0x4262efBd176F02824af27010bEa218429c33c7E8` (ERC-1967). [github.com/arcus-xyz/spot-contracts-abis](https://github.com/arcus-xyz/spot-contracts-abis)
- **0x RFQ / 1inch Fusion / LiFi** — official Stock Token docs as launch liquidity. [docs.robinhood.com/chain/building-with-stock-tokens](https://docs.robinhood.com/chain/building-with-stock-tokens/)
- **1inch** — named in official newsroom wallet DEX list with Uniswap, Rialto, Lighter, Arcus.
- **Pleiades** — newsroom “proprietary AMM” day-one partner. **INFERENCE:** same family as Rialto (docs say Rialto; newsroom says Pleiades). Do not assume a second AMM without a factory address.

Canonical tokens ([docs.robinhood.com/chain/contracts](https://docs.robinhood.com/chain/contracts/)):

| Symbol | Address |
|--------|---------|
| WETH | `0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73` |
| USDG | `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` |

WETH explorer check: Blockscout **verified** `TransparentUpgradeableProxy`. USDG explorer API 500 this pass; address is still official docs.

Stock-token addresses are a **live on-chain registry** on that same page — do not hardcode a stale ticker list here. A matching ticker with a different address is **not** a Robinhood Stock Token (**FACT**, official warning).

### 2.2 LP / concentrated liquidity fee farming

**FACT.** v3 NPM and v4 PositionManager are officially deployed. Anyone can mint a position and collect fees. Uniswap Labs blog invites “swap and provide liquidity” on this chain.

**INFERENCE for a $2k book:** WETH/USDG and Stock-Token pools are the deep(ish) fee venues; meme pools pay fee only if volume exists and IL does not eat it. Lab already burned LP NFTs in SM3 exit. Fee APY cannot close a **+$3732** 3× gap by 2026-09-30.

### 2.3 Lending / borrow / money markets

**FACT — Morpho is the official lending partner.**

- Chain docs: “Lending = Morpho”.
- Morpho docs API lists **Robinhood Chain, chain ID 4663**. [docs.morpho.org](https://docs.morpho.org/developers/api/get-started/)
- Official Morpho dashboard **data.morpho.org/chain/robinhood-chain** (fetched 2026-09-06): Total Deposits **~$936M**, Outstanding Loans **~$414M**, TVL **~$522M**. Collateral *names* shown include USDe, syrupUSDG, spUSDG, mGLO, **PONS**, **CASHCAT**, SPY, WETH.
- Official Morpho TypeScript address book (`@morpho-org/morpho-ts`, `ChainId.RobinhoodMainnet`): Morpho Blue `0x9D53d5E3bd5E8d4Cbfa6DB1ca238AEA02E651010`. [github.com/morpho-org/sdks](https://github.com/morpho-org/sdks)
- Robinhood Earn: official newsroom — eligible **US** users lend USDG via self-custody wallet into Morpho (Steakhouse / Ethena / Spark / Maple), advertised **~7% APY**. On-chain lending disclosure: Morpho is independent; principal can be lost.

**INFERENCE:** curated Earn / Vault V2 deposits may be allowlisted or capped (third-party toolkit reported `maxDeposit==0` for random addresses). Direct Morpho Blue `supply` is the permissionless path on other chains; treat vault UX vs Blue `supply` as **two different doors**. Confirm `maxDeposit` on the specific vault before assuming a bot can enter Earn.

**UNKNOWN:** live supply APY on the exact market a permissionless EOA can enter (dashboard is aggregate; Earn 7% is product copy).

Borrowing USDG against WETH / SPY / memes **exists as a Morpho market design** (dashboard collateral list). That is leverage. Current lab: **do not**.

No Aave / Compound official listing on the RH chain ecosystem table. **UNKNOWN** if forks exist; none official.

### 2.4 Staking / restaking / points / airdrop farms

| Item | Label | Evidence |
|------|-------|----------|
| Native ETH staking on 4663 | **UNKNOWN / none found** | ETH is L2 gas (Arbitrum Orbit). No official stake page. |
| EigenLayer-style restaking | **UNKNOWN / none found** | Not on official ecosystem table. |
| Lighter Points → LIT | **FACT** | Wallet perps article + newsroom: 11M LIT reserved; 2× points via RH Wallet, 1× via Lighter web. Lighter, not Robinhood, runs the program. |
| Uniswap / Morpho points on 4663 | **UNKNOWN** | Not evidenced in official RH docs. |
| Pools.trade launch / bid | **FACT** product exists | Uniswap Labs blog 2026-08-05: launchpad for Robinhood Chain (`pools.trade`). |

### 2.5 Perps / futures / synthetics — see §3

### 2.6 Bridges / messaging (existence only)

**FACT** — [docs.robinhood.com/chain/bridging](https://docs.robinhood.com/chain/bridging/):

| Route | Type | Speed (docs) |
|-------|------|----------------|
| Arbitrum canonical | Trustless L1↔L2 | Deposit ~10 min · Withdrawal **~7 days** |
| LayerZero OFT / Stargate | Messaging + OFT | Minutes (WBTC, USDG, other OFTs named) |
| Chainlink CCIP / Transporter | Messaging + tokens | Minutes (docs example: SyrupUSDG → lending) |
| Relay | Intents | Seconds; bridge-and-execute |
| Across | Intents | Seconds |
| LiFi / 0x | Aggregators | Seconds–minutes |

Protocol-contracts page publishes L2 Multicall `0x2cAC2D899eCC914d704FeaAE33ac1bF36277DaD1` and Permit2. Full L1 inbox / L2 gateway tables rendered poorly in the fetch (many rows missing in HTML). Uniswap gov names L2 Gateway Router `0x1E324B9316138CA9a73F960213621AD1aaf01B89` and Ethereum inbox `0x1A07cc4BD17E0118BdB54D70990D2158AbAD7a2D` — **FACT as Uniswap governance post**, not re-verified on explorer this pass.

This memo does **not** describe how to move lab funds off 4663.

### 2.7 Stock tokens / RWAs / meme liquidity

**FACT** ([stock-tokens](https://docs.robinhood.com/chain/stock-tokens/), [building-with-stock-tokens](https://docs.robinhood.com/chain/building-with-stock-tokens/)):

- ERC-20, 18 decimals, issued by Robinhood Assets (Jersey) Limited; economic exposure, **not** legal share ownership.
- ERC-8056 `uiMultiplier()` for corporate actions; Chainlink per-asset feeds (price **already** includes multiplier).
- **Not for US persons** (and other restricted jurisdictions). Official.
- Liquidity stack:
  1. **RFQ** (0x / 1inch Fusion / LiFi) — “at launch”
  2. **AMM** (Uniswap)
  3. **propAMM** (Rialto) when AMM is thin
  4. **Lighter orderbook** (spot & perps)
  5. **Primary mint/burn** — Authorized Participants only (KYB)

**INFERENCE (lab-consistent):** Stock Tokens are low-convexity vs memes. Lab sold NVDA/AMZN/TSLA/COST/RBLX already. They are useful as Morpho collateral or Lighter margin *in the abstract*, not as a 3× sleeve.

Memes (PONS / NUDES / NEKO / CASHCAT in the public snapshot) are ordinary 4663 ERC-20s in Uniswap v3 pools, marked via QuoterV2. They are **not** Stock Tokens. Fake-ticker risk is the same as SOL-CLUE-DESIGN-3X.

### 2.8 MEV / arb / basis

**FACT:** official docs — sequencing is **first-come, first-served by arrival at the sequencer**. “No transaction can bypass others by paying higher fees.” Public sequencer feed: `wss://feed.mainnet.chain.robinhood.com`.

**INFERENCE:**

- Classic Ethereum PGA / priority-gas sandwich is the wrong tool.
- Residual MEV: sequencer/operator privilege (L2BEAT flags this on Lighter), UniswapX fillers, RFQ, CEX-DEX, Uniswap↔Rialto↔Arcus spot.
- Basis: Lighter (or Arcus) ETH/BTC mark vs Uniswap WETH/USDG. Realistic only if both books are live and size clears. A ~$2k wallet is fee- and inventory-capped.
- FCFS + ~100ms-class blocks (often cited; treat block time as **INFERENCE** unless re-measured) makes toxic flow less about gas auctions and more about **who is closer to the sequencer**.

**UNKNOWN:** whether any searcher program or official rebate exists on 4663.

### 2.9 Other TVL / volume

| Surface | Label | Figure / note |
|---------|-------|----------------|
| Uniswap cumulative volume | FACT (gov, 2026-07-10) | >$1B shortly after launch |
| Morpho 4663 | FACT (dashboard, 2026-09-06 fetch) | ~$522M TVL, ~$936M deposits |
| Lighter-on-Robinhood TVS | FACT (L2BEAT page fetch) | **~$22.04M** |
| Pools.trade | FACT (Uniswap blog) | Launchpad; TVL not fetched |
| DualPool / Uniswap Earn | FACT (Uniswap blog, general) | Morpho-powered Earn in Uniswap UI — **confirm 4663 coverage before assuming** (blog examples USDC/USDT/ETH; RH native stable is USDG) |

---

## 3. Perps on 4663 — confirm or falsify

### Verdict

| Claim | Verdict |
|-------|---------|
| “There are no perps anywhere in the Robinhood product family.” | **FALSIFIED** |
| “There is a Uniswap v3 / v4 perpetual AMM on official 4663 factory.” | **FALSIFIED** (no official perp AMM; Uniswap listed as spot DEX only) |
| “An EVM wallet on 4663 can deposit into a Lighter contract and trade perps.” | **CONFIRMED (FACT)** for *eligible* jurisdictions |
| “Arcus perps settle as 4663 contracts a bot can call like SwapRouter.” | **NOT CONFIRMED.** In-ecosystem listing FACT; hybrid off-chain CLOB FACT; exact 4663 perps vault **UNKNOWN** |
| “RH app Futures / EU perps are the same as 4663 Lighter.” | **FALSIFIED** — different legal entities, venues, and settlement |

### 3.1 Lighter — ON-CHAIN / in-ecosystem (FACT)

Evidence, stacked:

1. Official chain ecosystem: **Perps = Lighter**. [docs.robinhood.com/chain](https://docs.robinhood.com/chain/)
2. Official Wallet article: deposit **USDG from wallet balance into a Lighter trading smart contract on the Robinhood Chain**; trades (BTC-PERP, ETH-PERP, …) signed in-wallet; isolated margin through RH Wallet; hourly funding; liquidation waterfall including LLP / ADL; **Lighter Points**. [robinhood.com support: wallet perpetual futures](https://robinhood.com/us/en/support/articles/robinhood-wallet-perpetual-futures/)
3. Official newsroom (2026-07-01, updated 2026-07-30): Wallet integration; 11M LIT; 2× points via Wallet. Disclosures: “Perpetual futures in your self-custody wallet are traded on Lighter … settles trades onchain through smart contracts.” **Not available** to residents of UK, US, Canada, Switzerland, UAE, Singapore, and other restricted jurisdictions.
4. L2BEAT **Lighter on Robinhood**: “application-specific ZK rollup deployed on Robinhood Chain”; USDG quote/margin (not USDC); deployed ~2026-06-26; Wallet integration 2026-07-01. Host chain = Robinhood Chain. Main rollup contract listed as `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d` (`ZkLighterWithSpotQuoteAsset`). Verifier `0xe1aFBE2D670eFF0e7C8A41F080792C011916ac31`. Governance `0xf6F6Bd6eEA2b9A2041328732CcAe4c5e1DD278B7`. TVS ~$22M. Risks: upgradeability / security-council can zero the delay; centralized operators; oracle trust. [l2beat.com/layer2s/projects/lighter-robinhood](https://l2beat.com/layer2s/projects/lighter-robinhood)

**What this is not:** a 4663 Uniswap pool. Order matching lives on the Lighter app-rollup. **4663 contracts custody USDG and verify ZK batches.** Wallet copy names a “Lighter Relayer Smart Contract”; L2BEAT names the rollup contract above. Treat them as **the same system**, not as a second unverified address. Exact “Relayer” vs rollup identity = **INFERENCE**.

Explorer API returned HTTP 500 for the L2BEAT address this pass. Address still stands on L2BEAT; re-check Blockscout before any future ticket.

### 3.2 Arcus — ON-CHAIN spot FACT; perps in-ecosystem FACT; 4663 perps vault UNKNOWN

- Official chain table: **Perps = Arcus**.
- Arcus: “built by dYdX Labs in partnership with Robinhood Crypto” for Stock Tokens and perps on Robinhood Chain. Spot beta; perps historically waitlisted. Restricted: US, UK, Canada, others. [arcus.xyz/blog/welcome-to-arcus](https://arcus.xyz/blog/welcome-to-arcus)
- Architecture: off-chain CLOB (~100k orders/s claimed) → permissioned appchain → **EVM rootchain** Checkpoint Manager + Bridge Vault + escape hatch. Audits named (Trail of Bits June 2026; OpenZeppelin). [docs.arcus.xyz architecture](https://docs.arcus.xyz/concepts/exchange-architecture)
- Spot contracts **explicitly chain 4663** (SwapShell etc.). Perps vault / checkpoint addresses on 4663: **not found on the pages fetched** → **UNKNOWN**.

**INFERENCE (strong):** Arcus perps are “in the 4663 ecosystem” the way Lighter is — deposit/settle against EVM contracts, match elsewhere. They are **not** a Uniswap v3 perpetual.

### 3.3 OFF-CHAIN — do not confuse with 4663

| Product | Where | Settlement | 4663? |
|---------|-------|------------|-------|
| Robinhood **Futures** (`/ES`, `/NQ`, energy, metals, crypto futures) | Main investing app / Legend | CME-style FCM: Robinhood Derivatives, LLC (CFTC/NFA) | **No** |
| Robinhood **Europe perpetual futures** (crypto + commodity/ETF/FX, up to 10x) | EU app + web, Perpetuals tab | App product; 15-min P&L; “partner venue” language | **No** (not an EVM wallet flow) |
| Futures **ticker tape** as Scout clues | Off-chain | n/a | Clue only (existing lab rule) |

### 3.4 Synthetics besides perps

Stock Tokens themselves are **tokenised debt securities**, not perps. Classic Stock Tokens in the Europe app are a **separate** derivative vs RHEU (**FACT** newsroom disclosures). Do not mix those with 4663 ERC-20 Stock Tokens.

---

## 4. Ranked shortlist — ~$2k Spot+meme book, 3× by 2026-09-30, **no bridge out**

Public book (morning 2026-09-06 JST): MTM ~$1.9k ≈ 1.0× B0; gap to $5645 ≈ **$3.7k**; idle USDG ~$287; WETH ballast; 4 memes at sleeve cap. Horizon ~24 days.

This ranking **does not change POLICY**. Rows marked *if bans lifted* are research only.

| Rank | Method | 3× relevance | Why |
|------|--------|--------------|-----|
| **1** | **4663 Uniswap v3 (v4) spot / meme convexity** — current path | **Only honest 3× path without leaving the chain or the mandate** | Need a name that is factory-real and Quoter-exitable. See `docs/SOL-CLUE-DESIGN-3X.md` on the clue PR. WETH 2× adds ~$0.5k. Morpho 7% on $287 adds ~$4. |
| **2** | **Pools.trade / official new v3·v4 pairs** | High if a real pair prints | Same FACT gate. Launchpad is a discovery surface, not a bypass. |
| **3** | **Better spot execution (Rialto / Arcus spot / RFQ) for exits** | Indirect | Helps **salvage** Stock/meme exits; does not create 3×. |
| **4** | **Hold WETH** | Ballast | Listed beta. Keep as gas-adjacent stack. Not the engine. |
| **5** | **Morpho USDG supply** (*if lend ban lifted*) | Preservation, not 3× | Best “idle yield” on 4663. Still ~7% class. Check vault `maxDeposit` vs Blue `supply`. |
| **6** | **Uniswap v3 LP on WETH/USDG** (*if LP re-opened*) | Fee income, IL | Lab already exited. Cannot close $3.7k. |
| **7** | **Lighter isolated perp, tiny USDG** (*if perp/leverage ban lifted*) | Convex **and** ruin | Only newly unlocked tool that *can* 3× a small USDG stub. Also the fastest kill-floor printer. Geo-gated. Operator/oracle/upgrade risk (L2BEAT). |
| **8** | **Arcus perps** (*if ban lifted*) | Same class as 7 | Confirm 4663 vault + eligibility first. Still **UNKNOWN** vault address. |
| **9** | **Morpho borrow against WETH/stocks to buy memes** (*if borrow/leverage ban lifted*) | Looks like alpha; usually death | Liquidation + thin meme exit. Do not rank this as a 3× plan even in a future memo without new FACT. |

Without a policy change, **stop at ranks 1–4**. Ranks 5–8 are a catalog for a later Chief decision, not Scout tickets.

---

## 5. Do not do — **current lab policy**

These look like “the landscape has more alpha.” They break the live mandate.

- Trade **perp / futures / Lighter / Arcus perps / Hyperliquid / any chain ≠ 4663**. `perp_pct = 0`.
- Use RH **brokerage Futures** or **EU app perps** from this wallet. Off-chain, wrong account, wrong legal box.
- **Bridge** (canonical, LZ, CCIP, Relay, Across, LiFi) from a bot / Autofill path.
- **Borrow** on Morpho or loop USDG. Leverage.
- Re-open **LP** or set `lp_pct > 0` without a new Chief mandate (LP EXITED).
- **Unlimited approve** to Universal Router, Permit2, Morpho, Lighter, Arcus SwapShell, or “the relayer.”
- Autofill ON. Scout-as-order.
- Deposit USDG into Lighter/Arcus “just to farm points.”
- Mark the book with Lighter / HL / CME / EU-perp prices.
- Treat a **fake HYPE / ticker twin** as Lighter’s underlying or as a Stock Token.
- Invent addresses. If explorer is 500, **do not guess**.
- Spend never-touch USDG or print MTM `< $1223.10`.
- Add a 5th meme or empty idle USDG (see clue memo).

---

## 6. Sources

### Official Robinhood Chain / Wallet / newsroom

- [About Robinhood Chain](https://docs.robinhood.com/chain/) — ecosystem table (Uniswap, Rialto, Morpho, Lighter, Arcus, USDG, LayerZero, Chainlink); FCFS sequencing
- [Connecting](https://docs.robinhood.com/chain/connecting/) — chain ID **4663**, RPC, explorer, public sequencer feed
- [Bridging](https://docs.robinhood.com/chain/bridging/)
- [Token contracts](https://docs.robinhood.com/chain/contracts/) — WETH, USDG
- [Protocol contracts](https://docs.robinhood.com/chain/protocol-contracts/) — Permit2, L2 Multicall
- [Stock Tokens](https://docs.robinhood.com/chain/stock-tokens/) · [Building with Stock Tokens](https://docs.robinhood.com/chain/building-with-stock-tokens/)
- [Wallet perpetual futures](https://robinhood.com/us/en/support/articles/robinhood-wallet-perpetual-futures/)
- [Chain mainnet support](https://robinhood.com/us/en/support/articles/robinhood-chain-mainnet/)
- [Newsroom 2026-07-01](https://robinhood.com/us/en/newsroom/robinhood-accelerates-global-expansion-robinhood-chain-mainnet-stock-tokens-agentic-trading/)
- [Brokerage Futures](https://robinhood.com/us/en/about/futures/) · [Futures orders](https://robinhood.com/us/en/support/articles/futures-orders/)
- [EU About perpetual futures](https://robinhood.com/eu/en/support/articles/about-perpetual-futures/)

### Uniswap

- [Uniswap is Live on Robinhood Chain](https://blog.uniswap.org/robinhood-chain-is-live)
- [v3 Robinhood deployments](https://developers.uniswap.org/docs/protocols/v3/deployments/v3-robinhood-chain-deployments)
- [v4 deployments (4663 section)](https://developers.uniswap.org/docs/protocols/v4/deployments)
- [v2 deployments](https://developers.uniswap.org/docs/protocols/v2/deployments)
- [Gov temp-check: volume + factories](https://gov.uniswap.org/t/temp-check-protocol-fee-expansion-robinhood-chain/26168)
- Uniswap Labs blog index: Pools.trade (2026-08-05)

### Morpho / Lighter / Arcus / Rialto

- [Morpho API supported networks](https://docs.morpho.org/developers/api/get-started/)
- [Morpho Robinhood dashboard](https://data.morpho.org/chain/robinhood-chain)
- [morpho-org/sdks addresses.ts `ChainId.RobinhoodMainnet`](https://github.com/morpho-org/sdks)
- [L2BEAT Lighter on Robinhood](https://l2beat.com/layer2s/projects/lighter-robinhood)
- [Arcus architecture](https://docs.arcus.xyz/concepts/exchange-architecture) · [perps overview](https://docs.arcus.xyz/concepts/perpetuals/overview)
- [arcus-xyz/spot-contracts-abis](https://github.com/arcus-xyz/spot-contracts-abis)
- [Rialto propAMM](https://docs.rialto.xyz/developers/propamm-integration-overview)

### Explorer

- [robinhoodchain.blockscout.com](https://robinhoodchain.blockscout.com) — this memo verified `UniswapV3Factory`, `QuoterV2`, `UniswapV2Router02`, WETH proxy. Several other official addresses returned API 500 on 2026-09-06; re-query before use.

---

## 7. Open questions (honest UNKNOWN)

1. Exact **Lighter Relayer** address vs L2BEAT rollup `0x94bA…fF9d` (same system **INFERENCE**).
2. **Arcus perps** Checkpoint Manager / Bridge Vault on 4663.
3. **RialtoRouter** official address.
4. UniswapX **reactor** address on 4663.
5. Whether Uniswap Earn / DualPool hooks are actually wired for **USDG on 4663**.
6. Permissionless Morpho Blue `supply` APY vs gated Earn vault APY for a random EOA.
7. Native stake / restake / extra DEX factories not on the official ecosystem table.
8. Live Uniswap 4663 TVL (gov figure is cumulative volume as of 2026-07-10).

---

*Sol. Research only. If Chief later wants a policy fork (e.g. Morpho-supply canary or Lighter isolated dust), that is a new mandate — not this memo.*
