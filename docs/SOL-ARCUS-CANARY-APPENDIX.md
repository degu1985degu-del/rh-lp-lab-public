# SOL-ARCUS-CANARY-APPENDIX

**Appendix only. Agent does not send txs, quotes, or orders.**  
Wallet `0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b` · chain **4663** · 2026-09-06

Human: Lighter withdraw **deferred** ($50 stays on Lighter, account 23139). Next research = **Arcus on Robinhood Chain**, not Lighter orders.

Idle wallet USDG ~$794 (human). Do not spend Lighter collateral. Do not Autofill. Do not `--unlimited`. Do not `createIntentAddress` / CCTP / Fun / Relay / Across / LayerZero from a bot.

Labels: **FACT** = official Arcus / Robinhood Chain docs, official ABI repo, or first-party API this pass. **INFERENCE** = labeled why. **UNKNOWN** = do not trade on it.

No secrets.

---

## 0. 日本語サマリ（Chief / human）

- **Arcus は 4663 上に「スポット」と「パープ」の二層がある（FACT）。** 公式チェーン表は両方を Perps パートナーとして列記。スポットはウォレット内の Stock Token / RFQ（SwapShell）。パープはオフチェーン CLOB + API + EVM カストディ。
- **Alchemy セッションだけで Lighter の geo-gate を回避できるわけではない（FACT / UNKNOWN）。** この環境の `GET https://api.arcus.xyz/v1/compliance` は **US-VA** で `perpetuals=true, spot=true`（両方制限）。公式は書き込みを `403 GEO_RESTRICTED` で止める。Lighter 公式エラー表に **20558 は無い**。JP オペレータの IP での compliance は **UNKNOWN（現地で再取得）**。
- **推奨カナリアはパープではなくスポット往復 ≤$50 USDG（FACT 理由）。** ラボ財布は `GET /v1/account` が **403 `address not on access whitelist`**。メインネットの perps 入金プロキシ住所は公式未掲載。公式入金 Fun は CCTP/Relay/Across/LZ（ラボ bot ブリッジ禁止）。
- **スポットは ChangePubKey 不要。** トークンはウォレットに残る。Approve は **SwapShell（および RFQ なら Permit2）へ有限額のみ**。
- **Lighter の $50 には触らない。出金しない。**

---

## Live reads this pass (2026-09-06, no writes)

| Call | Result |
|------|--------|
| `GET https://api.arcus.xyz/health` | `{"status":"ok"}` |
| `GET https://api.arcus.xyz/v1/compliance` (this host) | `geo.country=US`, `region=US-VA`, `restrictions.perpetuals=true`, `restrictions.spot=true`, `bypassed=false` |
| Same + `?address=0xeb2e…4c7b` | address `status=COMPLIANT` — **wallet screening ≠ geo** |
| `GET https://api.arcus.xyz/v1/account?address=0xeb2e…4c7b` | **403** `address not on access whitelist` |
| `GET https://api.arcus.xyz/v1/apiKeys?address=0xeb2e…4c7b` | `apiKeys: []` |
| `GET https://api.arcus.xyz/v1/markets` | 64 perps, **ONLINE** |
| `GET https://router.spot.arcus.xyz/health` | `ok`, `chainId=4663`, venues `arcus`,`rialto`, `swapShell=0x4262efBd176F02824af27010bEa218429c33c7E8` |
| `GET https://router.spot.arcus.xyz/v1/tokens` | 235 tokens; **USDG** present; **WETH not listed** |

---

## 1. What Arcus is on 4663 (spot vs perps)

Official Robinhood Chain ecosystem table: **Perps = Lighter** and **Perps = Arcus** (two named perpetuals DEXes). [docs.robinhood.com/chain](https://docs.robinhood.com/chain/)

Official Arcus: built by **dYdX Labs** with Robinhood Crypto; Stock Tokens (spot) + perpetuals on Robinhood Chain. UI: https://app.arcus.xyz · help: https://help.arcus.xyz · docs: https://docs.arcus.xyz/ · waitlist: https://waitlist.arcus.xyz  
[welcome](https://arcus.xyz/blog/welcome-to-arcus) · [how to start](https://arcus.xyz/blog/how-do-i-start-trading-on-arcus)

They are **not** Uniswap v3 AMM perps and **not** Lighter Domain.

### 1.1 Spot (on-chain, wallet self-custody) — FACT

Official [Stock Tokens / spot](https://docs.arcus.xyz/concepts/spot-overview.md): no leverage, no funding, no liquidation. Tokens live **in the wallet**. Arcus is a **router** (AMM + RFQ), atomic settle on-chain. “Sign each trade + one-time authorization the first time you interact with a given token.”

Official ABI / deploy table ([arcus-xyz/spot-contracts-abis](https://github.com/arcus-xyz/spot-contracts-abis), `deployments.json`, network = Robinhood mainnet **4663**):

| Contract | Integrate address (proxy) | Impl (repo, can move) | Role |
|----------|---------------------------|------------------------|------|
| **SwapShell** | `0x4262efBd176F02824af27010bEa218429c33c7E8` | `0x8B4420Fb0B3C366D1661B88466613F161D619f34` | Entry router. **Call / approve here.** |
| **ArcusSettlement** | `0x006102b16A04c20306A28b652745D3973D7D24fa` | `0x28Fe3236da3Cea9AFDf1045c19e1139A7Da89457` | Settlement / balance-delta. Not the taker entry. |
| RfqExecutor | `0xf4da3c42D9c9F494d4688A0112a9DB3C9b18a914` | — | Ordinary RFQ fill |
| WrappedTokenRfqExecutor | `0x43cF43056C33128329B54F66CA3649CF2975f1A6` | `0x4829D52f7099537e38Ee0B08c133f96810df67e2` | Wrapped-token RFQ |
| WrappedTokenFactory | `0x8bc71aE8EaC8B25F30c2990930Cc3A80E72e169e` | `0xD3Fd212d087E084B748fF4D00D936a9f1E8936a9` | Wrapped-token factory |
| WrappedTokenEscrow | `0x6d56Ab475069B7E93886b3D3F06c5435B87Ba158` | `0xCC31B65F43672A4151B30a6e181e0E8C1b1BC9B2` | Wrapped escrow |
| WrappedTokenBeacon | `0x27fEB332759F8d2f351D7fC72D29af37664ffd77` | `0x95b58BF6C2b1d5f4D1786f1B0dEa42e80132833E` | Beacon |

ERC-1967: bind the **proxy**, not the impl.

Spot router HTTP (official npm `@arcus-xyz/arcus-spot-sdk`): `https://router.spot.arcus.xyz/v1` · health confirms SwapShell above.

Canonical USDG (official chain contracts + Arcus token list): `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` (6 decimals).

Explorer: https://robinhoodchain.blockscout.com/address/0x4262efBd176F02824af27010bEa218429c33c7E8  
(This pass: Blockscout contract API HTML/500 — same flake as the landscape memo. Re-open the address in a browser before a ticket.)

### 1.2 Perps (hybrid CLOB) — FACT architecture, UNKNOWN mainnet vault

Official [architecture](https://docs.arcus.xyz/concepts/exchange-architecture.md): off-chain matching → permissioned appchain → EVM **Checkpoint Manager** + **Bridge Vault** (custody, withdrawals, escape hatch).

Official [API intro](https://docs.arcus.xyz/api-reference/introduction.md): REST/WS are **perpetuals** APIs.

| Env | REST | WS |
|-----|------|-----|
| Mainnet | `https://api.arcus.xyz` | `wss://api.arcus.xyz/v1/ws` |
| Testnet | `https://api.testnet.arcus.xyz` | `wss://api.testnet.arcus.xyz/v1/ws` |

Live books (this pass): **BTC-USD `marketId=1`**, **ETH-USD `marketId=2`**, both `PERPETUAL` / `ONLINE`. Default IMF ETH **0.04** (25x class); BTC **0.025** (40x class). Lab cap if ever used: **≤2x**. `minOrderNotional=5` (quote units).

**Mainnet Bridge Vault / PaxosDepositProxy / Checkpoint Manager addresses: not published on the official pages fetched.** Testnet-only ([fund testnet](https://docs.arcus.xyz/guides/fund-testnet-account.md)): chain **46630**, `PaxosDepositProxy` `0xb872…a34d`, `initiateDeposit(owner, accountIndex, token, amount)` — **do not copy those addresses onto 4663.**

Official [onboarding](https://docs.arcus.xyz/concepts/onboarding.md): app deposits go through **Fun** and may route **Circle CCTP, Relay, Across, LayerZero**. That is a **bridge**. Lab bot-bridge ban applies.

---

## 2. Can an Alchemy session trade Arcus without a Lighter-style geo-blocked API?

**Short answer: session-only does not unlock Arcus perps, and it does not erase geo.**

### 2.1 Lighter “20558”

Official RH Lighter error catalog ([data structures](https://apidocs.rh.lighter.xyz/docs/data-structures-constants-and-errors.md)) has **no code 20558** (this pass). Treat the human’s “Lighter 20558” as **their observed geo/API reject**, not a published Lighter constant. **UNKNOWN** exact mapping.

### 2.2 Arcus has its own geo gate (FACT)

Official [compliance](https://docs.arcus.xyz/api-reference/public/get-compliance-status.md):

- `geo.restrictions` from **request origin IP**, per product (`perpetuals` / `spot` independent).
- Restricted callers keep **read-only** API; **state-changing** calls return **`403` `GEO_RESTRICTED`**.
- Example in that page: a GB caller may be perps-restricted but spot-allowed.

This Cloud Agent egress: **US-VA, both products restricted.**  
Lab wallet screening: **COMPLIANT**. Screening ≠ permission to trade from a US IP.

**INFERENCE:** a Japan-resident operator calling `GET /v1/compliance` from a JP IP may see `restrictions.*.false`. **Must re-read from the human’s browser/IP before any ticket.** VPN to bypass is **forbidden by Arcus ToS** (FACT).

### 2.3 Session vs each layer

| Action | Alchemy session enough? | Extra key? |
|--------|-------------------------|------------|
| Spot: finite USDG `approve` + EIP-712 intent / permit | **Likely yes** (same class as deposit canary `eth_signTypedData` / `evm approve`) | No Lighter/Arcus API key. Router may submit the settle tx. |
| Spot: if RFQ path needs Permit2 | Session can finite-approve Permit2 | Still no Arcus API key |
| Perps: `POST /v1/createApiKey` | Session **might** sign EIP-712 `Arcus API Key` / `chainId=4663` if the session exposes `eth_signTypedData_v4` | Then **Ed25519 API key** signs every `placeOrder`. Session ≠ order signer. |
| Perps: place/cancel | **No** | Ed25519 key required ([authentication](https://docs.arcus.xyz/api-reference/authentication.md)) |
| Perps: this wallet today | **No** | **403 whitelist** even before an order |

This is **not** Lighter `ChangePubKey` on `0x94bA…`. It is a different key ceremony (Ed25519 + EIP-712). Same *class* of problem: **session alone cannot place perps.**

---

## 3. Deposit / margin / approve targets (finite only)

### 3.1 Spot canary — no vault deposit

Spot does **not** lock USDG into a perps vault. Sell token stays in the wallet until `SwapShell.swap` pulls it.

| Token | Spender | Amount |
|-------|---------|--------|
| USDG `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` | **SwapShell** `0x4262efBd176F02824af27010bEa218429c33c7E8` | Exact canary, e.g. **50e6 = 50000000**. Never `--unlimited`. |
| If the winning route is RFQ | Official RH **Permit2** `0x000000000022D473030F116dDEE9F6B43aC78BA3` ([protocol-contracts](https://docs.robinhood.com/chain/protocol-contracts/)) | Same finite raw amount. Never max-uint. Prefer a short-deadline permit over a standing allowance. |
| SwapShell impl / Settlement / RfqExecutor | — | **Do not approve these.** |

SwapShell ABI (official repo) exposes `PERMIT2()` and `swap(..., PermitData[], ...)`. `PermitData` is per-token `value` + `deadline` (finite). After the round-trip, revoke leftover allowance to 0.

Alchemy shape (human/Chief — **do not run from this agent**):

```bash
# Finite only. Human-decimal --amount 50 on evm approve.
alchemy evm approve 0x4262efBd176F02824af27010bEa218429c33c7E8 \
  --token-address 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 \
  --amount 50 \
  --signer session \
  -n robinhood-mainnet
```

Do **not** pass `--unlimited`. Do **not** approve Fun / a deposit QR / a CCTP messenger.

### 3.2 Perps deposit — not this packet

- App **Fun** = third-party swap+bridge. **Forbidden** as a bot/Autofill path.
- Testnet `PaxosDepositProxy.initiateDeposit` is the *shape* of a same-chain deposit. **Mainnet proxy address = UNKNOWN.** Do not guess. Do not reuse testnet `0xb872…`.
- Do not send USDG to SwapShell thinking it is perps margin. SwapShell is **spot**.
- Do not send USDG to Lighter proxy `0x94bA…` for Arcus.

---

## 4. Minimal ≤$50 canary (recommended = spot round-trip)

### 4.1 Do **not** start with Arcus perps

Blockers (FACT unless labeled):

1. This wallet: **not on access whitelist**.
2. Official marketing still describes **Perps Beta / waitlist** ([welcome FAQ](https://arcus.xyz/blog/welcome-to-arcus), page updated 2026-08-28). Books are ONLINE, but *this address* is gated.
3. Mainnet deposit contract **UNKNOWN**.
4. Fun = bridges.
5. Perps API key + geo write-gate.
6. Official product copy: **cross-margined** perps ([welcome](https://arcus.xyz/blog/welcome-to-arcus)). Isolated exists in the API (`setLeverage` / margin mode) but Wallet-style isolated-only is **not** the Arcus default story.

If whitelist + a **published** 4663 deposit proxy ever land, a later packet could size ETH-USD (`marketId=2`) at `minOrderNotional=5` / `minOrderSize=0.001` (~$2.5 at fetched mark; **$5 floor binds**), isolated, **≤2x**, open then reduce-only close. **Not this appendix.**

### 4.2 Spot packet (copy-paste intent, not execution)

**Size:** ≤ **$50** USDG (`50000000` raw). Prefer **$20** if the quote looks wide.

**Pair:** Arcus spot token list has **USDG** and Stock Tokens / some memes. **WETH is not on the router list** this pass — do not invent a WETH hop.

| Option | Why |
|--------|-----|
| **A (preferred):** USDG → a **already-held** meme (PONS or CASHCAT, both listed) → immediately USDG | No new Stock Token sleeve. Venue test only. |
| **B:** USDG → liquid Stock Token (e.g. NVDA on the list) → immediately USDG | Cleaner book, but temporary RWA inventory. Flatten the same session. |

Do **not** keep the bought token. Do **not** add a 5th meme. Do **not** size from the full $794.

**Flow (human / Chief, session):**

1. From a **non-restricted IP**, `GET https://api.arcus.xyz/v1/compliance` — both `restrictions.spot` and (if curious) `perpetuals` must be understood. If `spot=true`, **stop**.
2. `GET https://router.spot.arcus.xyz/v1/tokens` — confirm USDG + the chosen `buyToken` address (do not use ticker twins).
3. Request a quote from the official spot router (`chainId=4663`, `sellToken=USDG`, `sellAmount` ≤ 50e6, `taker=0xeb2e…4c7b`). **Agent does not request a firm quote.**
4. Finite approve SwapShell (and Permit2 only if the quote requires it).
5. Sign the taker intent / permits (EIP-712). `minBuyAmount` is the slippage floor (official RFQ).
6. Let the **official router** submit `SwapShell.swap`. Do not hand-roll calldata.
7. Read 4663 balances: USDG down, `tokenOut` up.
8. Reverse quote immediately (`sellToken` = what you bought, `buyToken` = USDG). Finite approve that token to SwapShell. Flatten.
9. Revoke leftover allowances to 0.
10. **Stop.** No second hop, no perps enable, no Fun.

SDK pointer (no secrets): `@arcus-xyz/arcus-spot-sdk` + `https://router.spot.arcus.xyz/v1`.

---

## 5. Geo / ToS

Named **Restricted Persons** ([Interface Terms](https://arcus.xyz/legal/terms), [Protocol Terms](https://arcus.xyz/legal/protocol-terms)):

- Reside / located / incorporated / registered office in **United States, Canada, United Kingdom**
- Sanctioned persons / comprehensive-sanctions countries (Iran, Cuba, North Korea, Crimea, Donetsk, Luhansk named)
- Anyone whose use would violate applicable law
- **VPN to circumvent: prohibited**

[Protocol Terms §6.3](https://arcus.xyz/legal/protocol-terms): US / CA / UK (and any jurisdiction that bans those features) **must not** use **perps / derivatives**. Spot only **to the extent permitted by law**.

**Japan is not named.** Residual “applicable law” + “other restricted” language remains. This memo is **not** a legal opinion.

Disclaimer ([docs](https://docs.arcus.xyz/concepts/disclaimer.md) + blog footer): not a regulated FSP; not available in US / Canada / UK and other restricted jurisdictions.

Lighter newsroom list (US/UK/CA/CH/UAE/SG + other) is a **different product**. Do not assume the two lists are equal. Arcus ToS is **narrower on named countries** (no CH/UAE/SG in the Restricted Person sentence) and **stricter on VPN**.

---

## 6. Do-not list (current lab)

- Live execution from this agent / Autofill / Scout-as-order
- `--unlimited` / max-uint to SwapShell, Permit2, Settlement, Fun, “the relayer”
- Bot **bridge**: Fun, CCTP, Relay, Across, LayerZero, `createIntentAddress`, any QR deposit on another chain
- Lighter Core / Lighter orders / Lighter withdraw (human deferred)
- Approving or depositing to **guessed** perps vaults or testnet `0xb872…`
- On-chain Lighter `createOrder` or Arcus perps while whitelist 403
- Cross / >2x / stock-token **perps** / second venue in the same ticket
- Selling PONS to fund Arcus
- Spending Lighter’s $50
- Publishing API private keys / session material
- Treating Arcus spot as the 3× engine (3× remains 4663 Uniswap meme/spot)

---

## 7. API keys / ChangePubKey / off-box UI

| Surface | Key? | UI? |
|---------|------|-----|
| **Spot** | **No** Arcus Ed25519 key. No Lighter `ChangePubKey`. Wallet / session signs approve + intent. | Optional: https://app.arcus.xyz Spot tab (human). |
| **Perps** | **Yes.** Generate Ed25519; register with EIP-712 `CreateApiKey` domain `name=Arcus API Key`, `version=1`, **`chainId=4663`** (production). Orders: `X-API-Key` + `X-Timestamp` + Ed25519 `X-Signature`. [createApiKey](https://docs.arcus.xyz/api-reference/onboarding/create-api-key.md) | App “enable trading” / API Keys page is the documented easy path. |
| **Waitlist** | X + wallet at waitlist.arcus.xyz | Off-box. Do not Autofill. |

`createApiKey` is **REST-only** (WS returns 501). Valid window: 1–180 days. Do not put the signing key in this repo.

---

## 8. Halt

Halt (leave USDG in the 4663 wallet; do not touch Lighter $50) if any:

- `GET /v1/compliance` from the **operator IP** shows `spot=true` (or perps=true if someone later tries perps)
- Quote / submit returns `GEO_RESTRICTED` / 403 whitelist
- Router `swapShell` ≠ `0x4262efBd…c7E8`
- Approve target ≠ SwapShell (or finite Permit2)
- Fun / bridge / unlimited approve appears in the wallet UI
- Reverse swap fails and leftover inventory is not flattened in the same session
- MTM approaches `$1223.10`

---

## 9. Sources

- [Robinhood Chain ecosystem](https://docs.robinhood.com/chain/) · [token contracts](https://docs.robinhood.com/chain/contracts/) · [Permit2](https://docs.robinhood.com/chain/protocol-contracts/)
- [Arcus architecture](https://docs.arcus.xyz/concepts/exchange-architecture.md) · [spot](https://docs.arcus.xyz/concepts/spot-overview.md) · [spot RFQ](https://docs.arcus.xyz/concepts/spot-rfq.md) · [onboarding / Fun](https://docs.arcus.xyz/concepts/onboarding.md) · [perps](https://docs.arcus.xyz/concepts/perpetuals/overview.md) · [auth](https://docs.arcus.xyz/api-reference/authentication.md) · [compliance](https://docs.arcus.xyz/api-reference/public/get-compliance-status.md)
- [spot-contracts-abis](https://github.com/arcus-xyz/spot-contracts-abis) · [arcus-spot-sdk](https://www.npmjs.com/package/@arcus-xyz/arcus-spot-sdk)
- [Welcome](https://arcus.xyz/blog/welcome-to-arcus) · [How to start](https://arcus.xyz/blog/how-do-i-start-trading-on-arcus) · [Interface ToS](https://arcus.xyz/legal/terms) · [Protocol Terms](https://arcus.xyz/legal/protocol-terms)
- Sibling: `docs/SOL-LIGHTER-ORDER-CANARY-APPENDIX.md` (Lighter orders deferred) · Lighter $50 stays on account 23139

---

*Sol. Appendix only. Agent does not quote, approve, or swap.*
