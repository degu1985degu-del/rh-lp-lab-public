# SOL-LIGHTER-ORDER-CANARY-APPENDIX

**Human FINAL scope (this page only): ONE isolated ≤2x ETH-PERP (preferred) or BTC-PERP — open then close.**  
Wallet `0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b` · Lighter account **23139** · 2026-09-06

**Agent does not place live orders.** This file is a copy-paste packet for Chief / human. Do not Autofill. Do not `--unlimited`. Do not `createIntentAddress` / CCTP / any bot bridge. Do not send USDG to Lighter Core (`mainnet.zklighter.elliot.ai`).

Deposit already **FILLED** (ticket SM3-PERP-0001). This appendix starts **after** that deposit. Withdraw is **not** in this packet.

Labels: **FACT** = official RH Lighter docs / first-party `api.rh.lighter.xyz` / verified 4663 implementation ABI. **INFERENCE** = labeled why. **UNKNOWN** = halt or human-sign, do not invent.

No secrets in this public file. Use env placeholders only (`$LIGHTER_API_PRIVATE_KEY`, `$LIGHTER_API_PUBLIC_KEY`, `$API_KEY_INDEX`, `$L1_OWNER_ETH_PRIVATE_KEY`). Never commit keys, auth tokens, or session material.

---

## 0. 日本語サマリ（Chief / human）

- **入金は完了（FACT）。** account **23139**, collateral **50.000000** USDG, `positions=[]`, `total_order_count=0`。API 鍵はまだ無い（`apikeys` は空配列）。
- **Alchemy セッションだけでは注文できない（FACT）。** 公式: 注文の署名には Lighter API 鍵が必須。セッションは 4663 の `approve`/`deposit` と同じレイヤ。注文は `api.rh.lighter.xyz` + `SignerClient`。
- **API 鍵の生成は L1 不要。紐付けは L1 オーナー署名が必要（FACT）。** 公式 SDK `change_api_key(eth_private_key=…)` **または** プロキシ上の `changePubKey`。セッションから EOA 秘密鍵は出せない。`changePubKey` をセッションで送れるかは **UNKNOWN**（失敗したら停止ルール §6）。
- **推奨カナリア:** ETH-PERP **market_id=0**, isolated, **2x**, 最小サイズ **0.005 ETH**（`base_amount=50`）。開いてすぐ閉じる。BTC は market **1**（代替）。
- **無制限 approve / bot ブリッジ / Core / Autofill / レバ>2 / 2本目は禁止のまま。**

---

## Live account FACT (read 2026-09-06, no API key)

```bash
curl -sS 'https://api.rh.lighter.xyz/api/v1/account?by=index&value=23139'
curl -sS 'https://api.rh.lighter.xyz/api/v1/accountsByL1Address?l1_address=0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b'
curl -sS 'https://api.rh.lighter.xyz/api/v1/apikeys?account_index=23139&api_key_index=255'
```

| Field | Value |
|-------|--------|
| `l1_address` | `0xeB2e6efFbc6e8D0362690cfdEBa098D7eB6d4c7b` |
| `index` / `account_index` | **23139** |
| `collateral` | `50.000000` |
| `available_balance` | `50.000000` |
| USDG `asset_id=3` `margin_balance` | `50.000000` |
| `positions` | `[]` |
| `total_order_count` | `0` |
| `account_trading_mode` | `1` (**Unified**; official OpenAPI: Classic=0, Unified=1) |
| `api_keys` | `[]` — **no key bound** |

---

## 1. FACT vs UNKNOWN (the six questions)

### 1.1 Can we place/cancel with ONLY an Alchemy session (no Lighter API key / ChangePubKey)?

**FACT: No.**

Official [Signing Transactions](https://apidocs.rh.lighter.xyz/docs/signing-transactions.md): “Creating an API key is **required** to sign transactions.” Orders are `SignerClient` → `sendTx` / `create_order` on `https://api.rh.lighter.xyz`, **not** a 4663 Uniswap `swap` and **not** `alchemy evm contract call` of a documented “placeOrder” that this lab should use.

Official [API keys](https://apidocs.rh.lighter.xyz/docs/api-keys.md):

- **Generating** a key does **not** need the L1 key.
- **Associating** it with the account **does**. Via the SDK **or** the on-chain `ChangePubKey` function (docs call this out for multi-sig).

Live FACT: `GET /api/v1/apikeys?account_index=23139&api_key_index=255` → `api_keys: []`. Until a key is bound, `SignerClient` / `sendTx` will fail (`AppErrInvalidPublicKey` / `please run changePubKey` — official error 21108).

Alchemy session **can** sign 4663 EVM (deposit canary already used `--signer session`). That is a different machine from Lighter order signing.

| Bind path | What human must sign | Session-only? |
|-----------|----------------------|---------------|
| **A. Official SDK** `SignerClient.change_api_key(eth_private_key=…, new_pubkey=…, api_key_index=…)` then `send_tx` | L1 owner **Ethereum private key** (SDK attaches `L1Sig`) | **No.** Session does not export an EOA key. |
| **B. On-chain** `changePubKey` on the **proxy** `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d` | 4663 tx from the **L1 owner** (same surface as deposit if `msg.sender` is the lab wallet) | **UNKNOWN** until Chief tries. If session/`msg.sender` is not treated as owner → halt (§6). |
| **C. Robinhood Wallet UI** | Each order on-device | Not an API key. Isolated-only in Wallet. Fallback if A/B fail — **human UI**, not Autofill. |

**Exact bind steps (no secrets):**

1. Offline, on a machine that will **not** commit output: `pip install lighter-sdk`.
2. Generate one keypair (`lighter.create_api_key()`). Store private key in an env var. Never paste it into Slack, this repo, or a ticket.
3. Choose `$API_KEY_INDEX` **≥ 4 and ≠ 157**. Official api-keys page reserves `{0,1,2,3,157}` for desktop/mobile. Get-started still says 0–1 only — **prefer the api-keys page**. Confirm unused with the `apikeys` curl above (today: all unused).
4. Associate:
   - **Prefer A if** human has the **exportable L1 owner key** for `0xeb2e…4c7b` (UNKNOWN whether this wallet is an EOA).
   - **Else try B** with Alchemy session (same `-n robinhood-mainnet --signer session` as deposit) — §2.
5. Wait ~10s (official `system_setup.py` sleeps 10). Re-read `apikeys`. Expect one row: `account_index=23139`, `api_key_index=$API_KEY_INDEX`, non-empty `public_key`.
6. `SignerClient.check_client()` must return no error **before** any order.

On-chain ABI **FACT** (implementation verified on Blockscout; **call the proxy**, never the impl):

```solidity
function changePubKey(uint48 _accountIndex, uint8 _apiKeyIndex, bytes _pubKey) external
```

| Arg | Canary value |
|-----|----------------|
| `_accountIndex` | `23139` |
| `_apiKeyIndex` | `$API_KEY_INDEX` (e.g. `4`) |
| `_pubKey` | bytes of the **public** key from `create_api_key()` (not the private key) |

Implementation last recorded by L2BEAT / deposit appendix: `0x82DE5B1161C93afDFE21bA0D5343f01Cd7401d90`. Implementations move. **`to` = proxy.**

The impl ABI also exposes an on-chain `createOrder(...)`. Official RH **signing / get-started** path for bots is still API key + `sendTx`. That on-chain `createOrder` has **no `reduce_only`**. **Do not use it** for this canary.

Fast withdraw / transfer to another address still need the **wallet L1 key** (official api-keys). This packet does not withdraw.

---

### 1.2 Exact market ids (live `api.rh.lighter.xyz`, 2026-09-06)

`GET https://api.rh.lighter.xyz/api/v1/orderBooks` + `orderBookDetails`.

| Book | `symbol` | `market_id` | `market_type` | `status` | mark (then) | `min_base_amount` | `min_quote_amount` | `size_decimals` | `price_decimals` |
|------|----------|-------------|---------------|----------|-------------|-------------------|--------------------|-----------------|------------------|
| **ETH-PERP** | **ETH** | **0** | perp | active | ~2492.27 | **0.0050** | **10** USDG | **4** | **2** |
| **BTC-PERP** | **BTC** | **1** | perp | active | ~79890.8 | **0.00020** | **10** USDG | **5** | **1** |
| ETH spot (do **not** use) | ETH/USDG | **2048** | spot | active | — | 0.0050 | 10 | 4 | 2 |

Official get-started example: `market_index=0` = ETH perps.

Also live on those two books:

| Field | ETH-PERP | BTC-PERP |
|-------|----------|----------|
| `taker_fee` / `maker_fee` | `0.0000` | `0.0000` |
| `default_initial_margin_fraction` | **5000** | **5000** |
| `min_initial_margin_fraction` | 200 | 200 |
| `maintenance_margin_fraction` | 120 | 120 |

**INFERENCE (SDK):** `SignerClient.update_leverage` sets `imf = int(10_000 / leverage)`. So **2x → IMF 5000**, which matches the live default. Protocol min IMF 200 would be **50x** — **lab cap is still ≤2x**. Do not send leverage 5 because Wallet UI can show it.

Re-fetch `orderBookDetails` immediately before send. Marks move.

---

### 1.3 Minimal order size with $50 collateral at ≤2x isolated

**Notional cap at 2x = $100.** Isolated: only this position’s allocated margin is at risk (Wallet FACT). API also describes isolated fee pull-from-cross — keep **no other Lighter positions**.

| | ETH-PERP (preferred) | BTC-PERP (alt) |
|--|----------------------|----------------|
| Min base | 0.0050 | 0.00020 |
| Notional at fetched mark | 0.005 × 2492.27 ≈ **$12.46** | 0.00020 × 79890.8 ≈ **$15.98** |
| ≥ min quote $10? | Yes | Yes |
| Fits in $100 notional / $50 at 2x? | **Yes** | **Yes** |
| Integer `base_amount` | `0.0050 * 10^4` = **50** | `0.00020 * 10^5` = **20** |
| Isolated margin at 2x (approx) | ~$6.23 | ~$7.99 |

Official [signing-transactions](https://apidocs.rh.lighter.xyz/docs/signing-transactions.md): min base/quote “only apply to **maker** orders”; the higher of the two applies for makers. **INFERENCE:** still size at/above both mins for IOC so the sequencer does not reject.

**Use ETH market 0, `base_amount=50`.** One open, one reduce-only close. Do not scale up “because $50 remains.”

Price integers (official example `3100_00` = $3100 when `price_decimals=2`):

`price = round(mark * 10^price_decimals)` then add **worst-price** headroom for IOC.

- Buy (`is_ask=False`): price **above** mark (slippage you accept).
- Sell (`is_ask=True`): price **below** mark.

Example at the fetched ETH mark 2492.27, +2% buy cap: `int(2492.27 * 1.02 * 100)` ≈ **254212**. **Recompute at send time.** Official: if the sequencer cannot fill at an equal-or-better price than `price`, the IOC is cancelled.

---

### 1.4 Exact SDK / REST/sign flow (create-order + close / reduce-only)

**FACT stack**

- No RH-specific SDK. Official: Core SDKs + base `https://api.rh.lighter.xyz` — [SDK](https://apidocs.rh.lighter.xyz/docs/sdk.md).
- `pip install lighter-sdk` · Python `lighter.SignerClient` · Go `elliottech/lighter-go`.
- Lighter app-chain id for this instance: **466324** (official get-started + SDK `ROBINHOOD.chain_id`). **Not** 4663.
- REST: `POST /api/v1/sendTx` with **already-signed** `tx_type` + `tx_info`. Do not invent `tx_info` by hand.
- Tx types (official constants): ChangePubKey=8, CreateOrder=14, CancelOrder=15, UpdateLeverage=20.

**Host / client (placeholders only — do not put real keys here):**

```python
# Chief-local only. Never commit.
import os, asyncio, lighter

BASE_URL = "https://api.rh.lighter.xyz"
ACCOUNT_INDEX = 23139
API_KEY_INDEX = int(os.environ["API_KEY_INDEX"])  # e.g. 4
PRIVATE_KEY = os.environ["LIGHTER_API_PRIVATE_KEY"]  # Lighter API key, NOT Alchemy session

client = lighter.SignerClient(
    url=BASE_URL,
    api_private_keys={API_KEY_INDEX: PRIVATE_KEY},
    account_index=ACCOUNT_INDEX,
    chain_id=466324,
)
```

**0. Bind (once)** — pick A or B.

Path A (official SDK; needs L1 owner key):

```python
priv, pub, err = lighter.create_api_key()
# persist priv privately; pub is safe to use as changePubKey input
resp, err = await client.change_api_key(
    eth_private_key=os.environ["L1_OWNER_ETH_PRIVATE_KEY"],
    new_pubkey=pub,
    api_key_index=API_KEY_INDEX,
)
```

Path B (4663, same Alchemy session as deposit). `_pubKey` = public key bytes from step `create_api_key()`. Confirm encoding against the SDK string (usually hex) **before** send. If the CLI rejects the bytes encoding, **stop** (do not guess a second format on-chain).

```bash
alchemy evm contract call 0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d \
  "changePubKey(uint48,uint8,bytes)" \
  --args '["23139","4","$LIGHTER_API_PUBLIC_KEY"]' \
  --signer session \
  -n robinhood-mainnet
```

`to` must be the **proxy**. No `--value`. No `--unlimited`.

**1. Isolated ≤2x (before the first order)**

```python
tx_info, resp, err = await client.update_leverage(
    market_index=0,  # ETH-PERP; use 1 for BTC
    margin_mode=client.ISOLATED_MARGIN_MODE,  # 1; CROSS=0 — do not send 0
    leverage=2,  # SDK: imf = int(10000/2) = 5000
)
```

Do **not** skip this. Account is Unified (`account_trading_mode=1`); that is **not** the same as isolated margin on a market. Official error 21132: cannot change margin mode with a position or open order.

**2. Open — market IOC long (simplest close)**

```python
# Re-read mark; set PRICE to worst acceptable integer (see §1.3)
tx, resp, err = await client.create_order(
    market_index=0,
    client_order_index=1001,          # unique uint48 you choose; unused on this account
    base_amount=50,                   # 0.0050 ETH
    price=PRICE,                      # worst acceptable (above mark for a bid)
    is_ask=False,                     # buy / long
    order_type=client.ORDER_TYPE_MARKET,  # 1
    time_in_force=client.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,  # 0
    reduce_only=False,
    order_expiry=client.DEFAULT_IOC_EXPIRY,
)
```

Official helper `create_market_order_limited_slippage` also exists in the SDK (computes `price` from book + `max_slippage`). Either is fine. **Do not** use GTT/limit for this canary.

**3. Verify fill (§1.5). If flat / cancelled: stop. Do not retry larger.**

**4. Close — opposite + reduce-only**

Read `positions[0].position` and `sign`. Long → `is_ask=True`. Convert size with `size_decimals=4` (ETH). Prefer the **live position size**, not a hardcoded 50, if the fill was partial.

```python
tx, resp, err = await client.create_order(
    market_index=0,
    client_order_index=1002,
    base_amount=CLOSE_BASE,           # from account readback
    price=PRICE_SELL,                 # worst acceptable (below mark)
    is_ask=True,                      # sell to flatten a long
    order_type=client.ORDER_TYPE_MARKET,
    time_in_force=client.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
    reduce_only=True,                 # required
    order_expiry=client.DEFAULT_IOC_EXPIRY,
)
```

**5. If an order is still working (should not happen for IOC):**

```python
tx, resp, err = await client.cancel_order(market_index=0, order_index=1001)
```

`order_index` = the `client_order_index` you set (official signing docs).

**FACT:** `sendTx` `code=200` means the **API accepted syntax**. Sequencer can still reject. Fill = account/position/trade readback, not HTTP 200.

Do not withdraw here. Do not open a second market.

---

### 1.5 How to verify fill via API readback

Public, **no auth** (use these first):

```bash
# After open: one ETH position; after close: positions []
curl -sS 'https://api.rh.lighter.xyz/api/v1/account?by=index&value=23139'

curl -sS 'https://api.rh.lighter.xyz/api/v1/accountsByL1Address?l1_address=0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b'

# Mark vs your fill
curl -sS 'https://api.rh.lighter.xyz/api/v1/orderBookDetails'
```

**Open success (FACT checklist)**

- `positions` length **1**
- `symbol=ETH`, `market_id=0` (or BTC/`1` if you chose alt)
- `position` ≈ `0.0050` (or `0.00020` BTC)
- `margin_mode` **1** (isolated — SDK `ISOLATED_MARGIN_MODE`)
- `sign` **1** for a long (official `AccountPosition.sign`)
- `allocated_margin` in the isolated-margin ballpark (~$6–8 at 2x min size), **not** the full $50 unless the venue allocated more
- `total_order_count` ≥ 1
- `collateral` still ~50 ± tiny fee/pnl (book fees were 0.0000 at fetch; slippage/funding still exist)

**Close success**

- `positions` **[]** (or `active_only` empty)
- `pending_order_count=0`
- `collateral` / `available_balance` ≈ 50 ± realized pnl / funding / fees
- No leftover working order

**Auth-gated (optional, after bind):** `create_auth_token_with_expiry` then `accountActiveOrders` / `GET /api/v1/trades?...&account_index=23139&sort_by=timestamp&limit=10`. Official: `auth` required for master/sub account trades. **Do not paste a real token into this repo.**

Public `recentTrades` is the **market** tape, not “our fill.” Confirm **account** `positions` / auth `trades` with `ask_account_id` or `bid_account_id` = **23139**.

---

### 1.6 Halt rules if an API key cannot be created / bound from the session

**Stop. Do not place an order.**

1. Do **not** Autofill. Do **not** `--unlimited`. Do **not** `createIntentAddress` / CCTP / any bridge. Do **not** switch to Lighter Core (`mainnet.zklighter.elliot.ai`, USDC, Ethereum contracts).
2. Do **not** invent a second Lighter account or a second deposit “to retry bind.”
3. Do **not** call on-chain `createOrder` as a workaround (no `reduce_only` in that ABI; not the official bot path).
4. Human options only:
   - Sign **Path A** from a surface that **is** the L1 owner (exported owner key, or Wallet/extension that can produce the SDK `L1Sig`).
   - Or sign **Path B** `changePubKey` from RH Wallet / a confirmed-owner 4663 sender (not a random session that fails `msg.sender` checks).
   - Or **UI canary**: Robinhood Wallet isolated ETH-PERP open+close (Wallet FACT: isolated only). Still ≤2x, min size, then flatten. That is a **human** click path, not an agent ticket.
5. Until bind is visible on `GET /api/v1/apikeys?account_index=23139&api_key_index=255`, **$50 stays idle on Lighter**. Withdraw = **separate** Chief ticket (secure withdraw to the **same** L1). Do not “test” withdraw in this packet.
6. Do not raise leverage, do not open a second market, do not use stock-token perps, do not sell PONS to fund another deposit.

If bind **succeeds** but `create_order` / sequencer rejects: flatten if a position exists; otherwise halt. Do not increase size.

---

## 2. Copy-paste sequence (human / Chief)

```text
[ ] 1. Re-read account 23139: collateral=50, positions=[], apikeys=[]
[ ] 2. Generate API key OFFLINE. Index 4+ and not 157. No secret in git.
[ ] 3. Bind Path A (L1 key) or Path B (proxy changePubKey via session/owner)
[ ] 4. Confirm apikeys row + check_client()
[ ] 5. update_leverage(market=0, isolated, 2)
[ ] 6. Re-read orderBookDetails; compute PRICE
[ ] 7. create_order open: market 0, base_amount=50, IOC, reduce_only=False
[ ] 8. Readback: one isolated ETH position
[ ] 9. create_order close: opposite, reduce_only=True, size from readback
[ ]10. Readback: positions=[]
[ ]11. STOP. No withdraw, no second order, no Autofill
```

If any box fails: §1.6.

---

## 3. Still forbidden

- Live orders from this agent / Autofill / Scout playbooks
- Unlimited approve / Permit2 / Universal Router
- Intent address / CCTP / bot bridge
- Lighter Core URLs and Ethereum/USDC contracts
- Calling implementation `0x82DE…` or `0xDa2B…` as `to`
- Spot `ETH/USDG` market **2048**
- Cross margin (`CROSS_MARGIN_MODE=0`) or leverage **> 2**
- A second market, stock-token perp, meme perp (PONS etc.)
- On-chain `createOrder` as a “session-only” shortcut
- Publishing `$LIGHTER_API_PRIVATE_KEY` / auth tokens / session keys
- Treating this canary as the 3× engine (3× remains 4663 spot / meme)

---

## 4. Sources

- [Signing Transactions](https://apidocs.rh.lighter.xyz/docs/signing-transactions.md) — API key required; `SignerClient`; IOC price = worst acceptable; maker mins
- [Get Started](https://apidocs.rh.lighter.xyz/docs/get-started.md) — `create_order` / `cancel_order`; `market_index=0` ETH; `BASE_URL=https://api.rh.lighter.xyz/`; chain ids `466324` / `300`
- [API keys](https://apidocs.rh.lighter.xyz/docs/api-keys.md) — generate vs associate; reserved `{0,1,2,3,157}`; on-chain ChangePubKey
- [SDK](https://apidocs.rh.lighter.xyz/docs/sdk.md) — no RH-specific SDK
- [Data structures](https://apidocs.rh.lighter.xyz/docs/data-structures-constants-and-errors.md) — tx types 8 / 14 / 15 / 20; error 21108
- [account](https://apidocs.rh.lighter.xyz/reference/account-1.md) — Unified=1; `positions[]`
- [apikeys](https://apidocs.rh.lighter.xyz/reference/apikeys.md) — `api_key_index=255` lists all
- [sendTx](https://apidocs.rh.lighter.xyz/reference/sendtx.md)
- [trades](https://apidocs.rh.lighter.xyz/reference/trades.md) — auth for account trades
- Python SDK: `create_api_key`, `change_api_key`, `update_leverage` (`imf=10000/leverage`), `ISOLATED_MARGIN_MODE=1`, `ROBINHOOD.chain_id=466324` — https://github.com/elliottech/lighter-python
- [Wallet perpetual futures](https://robinhood.com/us/en/support/articles/robinhood-wallet-perpetual-futures/) — Wallet path isolated only
- Sibling: `docs/SOL-LIGHTER-DEPOSIT-CANARY-APPENDIX.md` (deposit packet, already FILLED)

---

*Sol. Appendix only. Agent does not `send_tx` / `create_order` / `changePubKey`.*
