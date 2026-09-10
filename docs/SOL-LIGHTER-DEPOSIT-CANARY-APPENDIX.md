# SOL-LIGHTER-DEPOSIT-CANARY-APPENDIX

**Human FINAL scope (this page only): USDG $50 deposit test. No orders. No ChangePubKey.**  
Wallet `0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b` · chain **4663** · 2026-09-06

Live trading policy stays **no Lighter orders**. This appendix is the copy-paste packet for Chief’s **deposit-canary** only. Do not Autofill. Do not `--unlimited`. Do not call `createIntentAddress` / CCTP / any bridge.

---

## 0. Call **the proxy**, not the implementation

| Role | Address | Use? |
|------|---------|------|
| **CALL TARGET / spender (proxy)** | `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d` | **YES — approve + deposit `to` this** |
| Implementation `getTarget` / ZkLighter (L2BEAT last recorded) | `0x82DE5B1161C93afDFE21bA0D5343f01Cd7401d90` | **NO txs.** Code lives here; storage is on the proxy |
| AdditionalZkLighter (L2BEAT last recorded) | `0xDa2B59fFB41485a6f21E14e479AE7B7AB29a997c` | **NO txs** |

**FACT — call address:** official [Lighter Domains](https://docs.robinhood.com/chain/lighter-domains/) + live `GET https://api.rh.lighter.xyz/api/v1/layer1BasicInfo` (2026-09-06) returns `ZkLighterContract` = `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d`.

**FACT — it is a proxy:** L2BEAT `values.getTarget` / `$implementation.0` on that same address. Implementations **move on upgrade**. Sending `deposit` or `approve` to an implementation **will not credit the rollup account**. Always `to` = **proxy**.

If Chief wants a same-day re-check of `getTarget`, read it on the proxy via explorer/eth_call **but still send the tx to `0x94bA…fF9d`.**

---

## 1. Deposit function (exact)

Official signature ([lighter-domains](https://docs.robinhood.com/chain/lighter-domains/) + [RH Lighter deposits](https://apidocs.rh.lighter.xyz/docs/deposits-transfers-and-withdrawals.md)):

```solidity
function deposit(
    address _to,
    uint16  _assetIndex,
    uint8   _routeType,   // TxTypes.RouteType
    uint256 _amount
) external payable
```

Solidity / ABI types:

| Arg | Type | $50 canary value |
|-----|------|------------------|
| `_to` | `address` | `0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b` |
| `_assetIndex` | `uint16` | `3` (USDG) |
| `_routeType` | `uint8` | `0` (perps). `1` = spot — **do not use** |
| `_amount` | `uint256` | `50000000` (= 50 × 10^6) |

Live confirm 2026-09-06: `GET https://api.rh.lighter.xyz/api/v1/assetDetails?asset_id=3` → `symbol=USDG`, `l1_decimals=6`, `l1_address=0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168`.

Human-readable check: `50e6 = 50000000`. Official example: `1000000` = 1 USDG.

`payable`: ETH deposits only. **USDG deposit: `value = 0`.** Do not attach native ETH.

Same-chain only. Anyone may `deposit` for `_to`; first deposit **creates** the Lighter account. Live read now: `accountsByL1Address` → **`account not found`** for this wallet (expected pre-canary).

---

## 2. USDG approve spender

| Token | Spender | Same as deposit target? |
|-------|---------|-------------------------|
| USDG `0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168` | `0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d` | **YES (proxy)** |

Official: “approve spending for Lighter's smart contract (`0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d`)”.

Finite only: **50 USDG** = `50000000` raw. Never `--unlimited`. Never Permit2 / Universal Router for this test.

ERC-20: `approve(address spender, uint256 amount)` → spender = proxy, amount = `50000000`.

---

## 3. Alchemy CLI (session, robinhood-mainnet)

Preflight (read-only). Confirm signer is the lab address before any write:

```bash
alchemy wallet status --verify
alchemy evm network list --search robinhood
alchemy evm data balance --address 0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b -n robinhood-mainnet
```

Human-decimal `--amount 50` on `evm approve` (CLI scales by token decimals). Contract-call `--args` for `deposit` uses **raw 1e6**.

### 3a. Finite approve (50 USDG)

```bash
alchemy evm approve 0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d \
  --token-address 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 \
  --amount 50 \
  --signer session \
  -n robinhood-mainnet
```

Do **not** pass `--unlimited` or `-y` as a way to skip reading the spender.

### 3b. Confirm allowance (view)

```bash
alchemy evm contract read 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 \
  "allowance(address,address)(uint256)" \
  --args '["0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b","0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d"]' \
  -n robinhood-mainnet
```

Expect `50000000`. If not, **stop** (do not deposit).

### 3c. Deposit $50 to self (perps route)

```bash
alchemy evm contract call 0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d \
  "deposit(address,uint16,uint8,uint256)" \
  --args '["0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b",3,0,"50000000"]' \
  --signer session \
  -n robinhood-mainnet
```

No `--value`. If the CLI demands a return-type string, use:

```bash
alchemy evm contract call 0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d \
  "deposit(address,uint16,uint8,uint256)()" \
  --args '["0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b",3,0,"50000000"]' \
  --signer session \
  -n robinhood-mainnet
```

Poll:

```bash
alchemy evm status <call_id_or_txhash> -n robinhood-mainnet
```

**Hard stops:** `_to` ≠ lab wallet · `assetIndex` ≠ 3 · `routeType` ≠ 0 · amount ≠ `50000000` · `to` ≠ proxy · any `ChangePubKey` / `send_tx` / order SDK.

---

## 4. Read-back (success = all of these)

On-chain (4663):

```bash
# Wallet USDG should drop by 50e6
alchemy evm contract read 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 \
  "balanceOf(address)(uint256)" \
  --args '["0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b"]' \
  -n robinhood-mainnet

# Allowance should be 0 after a full 50 pull (or leftover if deposit failed)
alchemy evm contract read 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 \
  "allowance(address,address)(uint256)" \
  --args '["0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b","0x94bAB9693Ba2f6358507eFfcbd372b0660AFfF9d"]' \
  -n robinhood-mainnet
```

Lighter API (no API key; **not an order**):

```bash
curl -sS 'https://api.rh.lighter.xyz/api/v1/accountsByL1Address?l1_address=0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b'
```

**Before (FACT now):** `code` 21100 / `account not found`.  
**After success:** HTTP 200, `sub_accounts[0].l1_address` = lab wallet, `available_balance` / `collateral` ≈ **50** USDG (API string units — confirm against `assetDetails` decimals; do not place a trade to “check”).

Explorer: https://robinhoodchain.blockscout.com/address/0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b  
Tx `to` must be the **proxy**. USDG `Transfer` from wallet → proxy for `50000000`.

If 4663 USDG left the wallet but API still `account not found` after several minutes: **halt**. Do not “fix” with a second deposit or an order.

---

## 5. Japan vs official geo-ban list

**Named official ban list does not include Japan.**

Quote, Robinhood newsroom disclosures (updated 2026-07-30), section *Decentralized Perpetuals Futures*:

> “Perpetuals trading is only available to eligible clients in permitted jurisdictions and is **not available to residents of the U.K., US, Canada, Switzerland, UAE, Singapore, and other restricted jurisdictions.**”

Source: https://robinhood.com/us/en/newsroom/robinhood-accelerates-global-expansion-robinhood-chain-mainnet-stock-tokens-agentic-trading/

| Jurisdiction | Named on that list? |
|--------------|---------------------|
| United States | Yes |
| United Kingdom | Yes |
| Canada | Yes |
| Switzerland | Yes |
| UAE | Yes |
| Singapore | Yes |
| **Japan** | **No (not named)** |

Caveat **FACT**: the same sentence has a residual **“and other restricted jurisdictions.”** Japan is not enumerated. This memo is **not** a legal opinion that every JP operator is “permitted.” It answers the asked question: Japan is **not** on the official named list.

This canary is **deposit only** (no perpetuals *trade*). Wallet article eligibility language is about trading. Still: if Chief’s operator is actually a named-ban resident, **do not deposit.**

---

## 6. Still forbidden in this FINAL

- Orders / `SignerClient` / `send_tx` / `create_order`
- `ChangePubKey` / API-key bind
- `--unlimited` approve
- Intent address / CCTP / any bridge
- `routeType=1` (spot) or non-3 `assetIndex`
- Second $50 if the first receipt is ambiguous
- Calling implementation `0x82DE…` or `0xDa2B…`

Withdraw is **not** part of this packet (separate Chief ticket later).
