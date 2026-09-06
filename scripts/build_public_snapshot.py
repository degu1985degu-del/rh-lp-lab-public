#!/usr/bin/env python3
"""Build secret-free public snapshot for RH LP Lab dash."""
from __future__ import annotations
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
LP_ROOT = Path("/workspace/rh-lp-lab")
MEME_ROOT = Path("/workspace/rh-meme-lab")
OUT = Path(__file__).resolve().parents[1] / "data" / "latest.json"
SM3_ALTROT_SNAP = Path("/workspace/rh-lp-lab/handoff/SM3-ALTROT-POST-SNAP.json")
SM3_POST_DEPLOY_SNAP = Path("/workspace/rh-lp-lab/handoff/SM3-POST-DEPLOY-SNAP.json")
LP_STATE = Path("/workspace/rh-lp-lab/STATE.json")
STATIC = Path(__file__).resolve().parent / "public_snapshot_static.json"
SPOT_COST_LEDGER = Path("/workspace/rh-lp-lab/handoff/SPOT-COST-LEDGER.json")

# Live USDG (same public RPC path as refresh_public_marks.py / memectl)
PUBLIC_RPC = "https://rpc.mainnet.chain.robinhood.com"
USDG_ADDR = "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168"
WALLET_ADDR = "0xeb2e6effbc6e8d0362690cfdeba098d7eb6d4c7b"
USDG_DECIMALS = 6
# Known stale ALTROT post-snap idle — never silently re-publish as live.
ALTROT_STALE_IDLE_USDG = 844.379235

# Spot dust below this USD (or missing mark) is omitted from valued positions.
SPOT_DUST_USD = 0.05

KNOWN_FILLS = [
    {
        "id": "MEME-CANARY-0001",
        "at_jst": "2026-09-04T23:52:00+09:00",
        "kind": "meme_buy",
        "symbol": "PONS",
        "notional_usd": 100,
        "approve_tx": "0x03a36fe68893fcd81c80ef8227203fe5aa6953392d554ff80a9f02838c749658",
        "swap_tx": "0x660f3ec138bc2d186bf5740031a7249ecfe2c55441e3c325b5e415cbecf51b4e",
    },
    {
        "id": "MEME-CANARY-0003",
        "at_jst": "2026-09-05T07:57:00+09:00",
        "kind": "meme_buy",
        "symbol": "NUDES",
        "notional_usd": 75,
        "approve_tx": "0x26ecf04c2fcb692722ed479367f1cef1d49f530469f726bf1ca21b6f9d481d8c",
        "swap_tx": "0xe8056a871a32bd816e8bccab73e8b8eb3f8b6437e039940a582ee782465e0e98",
    },
    {
        "id": "MEME-CANARY-0004",
        "at_jst": "2026-09-05T09:05:00+09:00",
        "kind": "meme_buy",
        "symbol": "MEME",
        "notional_usd": 75,
        "approve_tx": "0xfe3bde0c473eb1725842ced0da6cac1bae24d9994833ded071df7657a510aa06",
        "swap_tx": "0x8dbd6224539831e2f85c6abbcf43a371c5a1da3f2500963f958cd20a9657535f",
    },
    {
        "id": "MEME-CANARY-0005",
        "at_jst": "2026-09-05T12:53:00+09:00",
        "kind": "meme_buy",
        "symbol": "NEKO",
        "notional_usd": 50,
        "approve_tx": "0x075da7bc66da9d1d2d884f0bab23fe7733d1809775149f477266618f9c48757b",
        "swap_tx": "0xfadfee8af7aa2e4f6ddbe05e2c43531a03147b05f99b37f4f7dce072664cbc8b",
    },
]


def load_json(path: Path):
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def _f(x, default=None):
    try:
        return float(x) if x is not None else default
    except (TypeError, ValueError):
        return default


def _live_human(live: dict, sym: str):
    bals = (live or {}).get("balances") or {}
    row = bals.get(sym) if isinstance(bals.get(sym), dict) else None
    if not row:
        return None
    return _f(row.get("human"))



def fetch_live_usdg_balance() -> tuple[float | None, str | None]:
    """Read-only ERC20 balanceOf(USDG) for the lab wallet. Returns (human_usd, err)."""
    data = "0x70a08231" + WALLET_ADDR[2:].lower().zfill(64)
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [{"to": USDG_ADDR, "data": data}, "latest"],
    }
    req = urllib.request.Request(
        PUBLIC_RPC,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "rh-public-snapshot/0.2"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = json.loads(resp.read().decode())
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
    if isinstance(body, dict) and body.get("error"):
        return None, str(body["error"])
    result = str((body or {}).get("result") or "")
    if not result or result == "0x":
        return None, "empty eth_call result"
    try:
        raw = int(result, 16)
    except ValueError as e:
        return None, f"bad hex: {e}"
    return round(raw / (10 ** USDG_DECIMALS), 6), None


def resolve_idle_usdg(snap_idle, prev_snap: dict) -> tuple[float | None, str, str | None]:
    """Prefer live on-chain USDG each publish; never silently revert to stale ALTROT 844.

    Fallback order on RPC failure:
      1) previous latest.json idle if sourced live / retained-live (fresher than ALTROT)
      2) previous idle if materially different from ALTROT_STALE_IDLE_USDG
      3) snap idle only as last resort (explicit source label)
    """
    live, err = fetch_live_usdg_balance()
    if live is not None:
        return live, "onchain_balanceOf", None

    prev_wallet = (prev_snap or {}).get("wallet") if isinstance(prev_snap, dict) else {}
    if not isinstance(prev_wallet, dict):
        prev_wallet = {}
    prev_idle = _f(prev_wallet.get("idle_usdg_usd"))
    prev_src = str(prev_wallet.get("idle_usdg_source") or "")
    live_srcs = ("onchain_balanceOf", "previous_live_retained", "previous_non_altrot_retained")

    if prev_idle is not None and (
        prev_src in live_srcs
        or abs(prev_idle - ALTROT_STALE_IDLE_USDG) > 0.5
    ):
        label = (
            "previous_live_retained"
            if prev_src in ("onchain_balanceOf", "previous_live_retained")
            else "previous_non_altrot_retained"
        )
        return prev_idle, label, err

    # Last resort: snap value, but never pretend it is live
    snap_v = _f(snap_idle)
    return snap_v, "sm3_altrot_post_snap_stale", err


def normalize_altrot_to_canonical(alt: dict, deploy: dict) -> dict:
    """Map SM3-ALTROT-POST-SNAP into the POST-DEPLOY-shaped fields the builder uses.

    Balances come only from ALTROT live FACT. Mark *rates* may be reused from the
    prior POST-DEPLOY snap (price, not inventory) to value unchanged WETH / ETH.
    Sold stock tokens are not emitted as valued spot_positions.
    """
    live = alt.get("live") if isinstance(alt.get("live"), dict) else {}
    deploy_marks = (deploy or {}).get("marks") or {}
    deploy_usd = (deploy or {}).get("usd_values") or {}

    usdg = _f(alt.get("usdg"))
    if usdg is None:
        usdg = _live_human(live, "USDG")
    weth = _f(alt.get("weth"))
    if weth is None:
        weth = _live_human(live, "WETH")
    eth_native = _f(alt.get("eth_native"))
    if eth_native is None:
        eth_row = (live.get("ETH_native") or {}) if isinstance(live.get("ETH_native"), dict) else {}
        eth_native = _f(eth_row.get("human"))

    meme_amts = alt.get("meme") if isinstance(alt.get("meme"), dict) else {}
    meme_costs = alt.get("meme_costs_usdg") if isinstance(alt.get("meme_costs_usdg"), dict) else {}

    # Stock balances from live (FACT only) — sold = 0 / dust
    stock_syms = ("NVDA", "COST", "TSLA", "AMZN", "RBLX")
    spot_bal = {}
    for sym in stock_syms:
        if sym == "RBLX":
            continue
        h = _live_human(live, sym)
        if h is None:
            continue
        spot_bal[sym] = h
    rblx = _live_human(live, "RBLX")
    if rblx is None:
        rblx = 0.0

    # Price rates from prior deploy snap (not inventories)
    usdg_per_weth = _f(deploy_marks.get("usdg_per_weth"))
    if usdg_per_weth is None and _f(deploy_usd.get("weth")) and _f((deploy.get("balances") or {}).get("weth")):
        bw = _f((deploy.get("balances") or {}).get("weth"))
        if bw:
            usdg_per_weth = _f(deploy_usd.get("weth")) / bw

    weth_usd = round(weth * usdg_per_weth, 6) if (weth is not None and usdg_per_weth) else None
    native_eth_usd = (
        round(eth_native * usdg_per_weth, 6) if (eth_native is not None and usdg_per_weth) else None
    )

    # No valued stock positions after ALTROT sells (dust omitted from valued book)
    spot_positions = []
    spot_tokens_sum = 0.0

    meme_positions = []
    # Prefer keys present on ALTROT meme map (includes CASHCAT after autonomy adds)
    syms = [s for s in meme_amts.keys() if isinstance(s, str) and s.upper() != "SUM"]
    if not syms:
        syms = ["PONS", "NUDES", "NEKO"]
    for sym in syms:
        amt = _f(meme_amts.get(sym))
        if amt is None:
            amt = _live_human(live, sym)
        if amt is None:
            continue
        cost = _f(meme_costs.get(sym))
        meme_positions.append(
            {
                "symbol": sym,
                "amount_onchain": amt,
                "cost_usdg": cost,
                "mark_source": "amount_from_altrot_snap",
            }
        )

    spot_incl = weth_usd if weth_usd is not None else 0.0
    # RBLX sold — do not add residual mark even if dust somehow present
    if rblx and rblx > 0 and False:
        pass

    out = {
        "schema": "SM3-POST-DEPLOY-SNAP/v1+altrot_overlay",
        "kind": "post_sm3_altrot_snapshot",
        "read_only": True,
        "source_snap": "SM3-ALTROT-POST-SNAP",
        "observed_at_jst": alt.get("observed_at_jst"),
        "chain_id": alt.get("chain_id") or live.get("chain_id"),
        "block_number": alt.get("block") or live.get("block"),
        "wallet": alt.get("wallet") or live.get("wallet"),
        "npm_balanceOf": 0,
        "balances": {
            "native_eth": eth_native,
            "weth": weth,
            "usdg": usdg,
            "rblx": rblx if rblx else 0.0,
            "djt": 0.0,
            "spot": spot_bal,
            "memes": {k: _f(v) for k, v in meme_amts.items()},
            "meme_dust": 0,
        },
        "usd_values": {
            "usdg": usdg,
            "weth": weth_usd,
            "native_eth": native_eth_usd,
            "rblx": 0.0,
            "djt": 0.0,
            "spot_tokens_sum_usd": spot_tokens_sum,
            "spot_incl_weth_residuals_usd": spot_incl,
            "idle_usdg_usd": usdg,
            "lp_usd": 0.0,
        },
        "marks": {
            "usdg_per_weth": usdg_per_weth,
            "source": "altrot_balances+post_deploy_weth_rate",
        },
        "mandate": (deploy or {}).get("mandate")
        or {
            "plan": "SM3-52/46/02",
            "b0_usd": 1881.69,
            "target_3x_usd": 5645.07,
            "split": {"spot_pct": 52, "meme_pct": 46, "gas_pct": 2, "perp_pct": 0, "lp_pct": 0},
        },
        "spot_positions": spot_positions,
        "meme_positions": meme_positions,
        "spot_posture": alt.get("spot_posture") or "HOLD_USDG",
        "filled_tonight": alt.get("filled_tonight"),
        "m3_abort": {
            "meme_m3_aborted": True,
            "note": "Post-ALTROT: stocks sold→USDG; meme name-cap adds done; spot HOLD_USDG + WETH hop; STOP further buys.",
            "idle_usdg_actual": usdg,
            "stop_further_buys": True,
        },
        "altrot_meta": {
            "revoke_needed": alt.get("revoke_needed"),
            "allowances_all_zero": alt.get("allowances_all_zero"),
            "schema": alt.get("schema"),
        },
    }
    return out


def load_sm3_snap() -> tuple[dict, str]:
    """Prefer ALTROT live FACT; fall back to POST-DEPLOY."""
    alt = load_json(SM3_ALTROT_SNAP)
    deploy = load_json(SM3_POST_DEPLOY_SNAP)
    if alt and (alt.get("usdg") is not None or (alt.get("live") or {}).get("balances")):
        return normalize_altrot_to_canonical(alt, deploy), "SM3-ALTROT-POST-SNAP"
    if deploy:
        return deploy, "SM3-POST-DEPLOY-SNAP"
    return {}, "NONE"


def latest_nav():
    files = list((LP_ROOT / "pnl").glob("*triple-nav*.json"))
    if not files:
        return {}, None
    files.sort(key=lambda p: p.stat().st_mtime)
    return load_json(files[-1]), files[-1].name


def public_positions(raw, amount_by_sym=None):
    out = []
    amount_by_sym = amount_by_sym or {}
    for p in raw or []:
        if not isinstance(p, dict):
            continue
        sym = p.get("symbol")
        if not sym:
            continue
        # Allow any open meme in STATE (PONS/NUDES/NEKO/CASHCAT/…)
        row = {
            "symbol": sym,
            "cost_usdg": p.get("cost_usdg"),
            "mark_usd": p.get("mark_usd"),
            "unrealized_pnl_usd": p.get("unrealized_pnl_usd"),
            "status": p.get("status") or "HOLD",
            "mark_source": p.get("mark_source"),
            "marks_updated_at_jst": p.get("marks_updated_at_jst"),
        }
        amt = amount_by_sym.get(sym)
        if amt is None and p.get("amount") is not None:
            amt = p.get("amount")
        if amt is not None:
            row["amount"] = amt
        out.append(row)
    return out


def public_spot(snap, cost_ledger=None, source_label: str = "SM3-POST-DEPLOY-SNAP"):
    """Build public spot sleeve; attach cost basis from SPOT-COST-LEDGER when present."""
    by_sym = {}
    if isinstance(cost_ledger, dict):
        by_sym = cost_ledger.get("by_symbol") or {}

    def cost_row(sym):
        row = by_sym.get(sym) if isinstance(by_sym.get(sym), dict) else {}
        return row

    def attach_cost(entry, sym):
        row = cost_row(sym)
        cost = row.get("cost_usdg") if row else None
        entry["cost_usdg"] = cost
        if row.get("note"):
            entry["cost_note"] = row.get("note")
        # Sold roles: never show phantom valued PnL
        if row.get("role") == "sold":
            entry["mark_usd"] = 0.0 if entry.get("amount") else entry.get("mark_usd")
            if not entry.get("amount"):
                entry["mark_usd"] = 0.0
            entry["unrealized_pnl_usd"] = 0.0
            entry["status"] = "SOLD"
            return entry
        mark = entry.get("mark_usd")
        if cost is not None and mark is not None:
            try:
                entry["unrealized_pnl_usd"] = round(float(mark) - float(cost), 6)
            except (TypeError, ValueError):
                entry["unrealized_pnl_usd"] = None
        else:
            entry["unrealized_pnl_usd"] = None
        return entry

    positions = []
    for p in snap.get("spot_positions") or []:
        if not isinstance(p, dict):
            continue
        sym = p.get("symbol")
        amt = _f(p.get("amount_onchain"), 0.0) or 0.0
        mark = _f(p.get("mark_usd"))
        # Skip sold / dust — no valued phantom stock marks
        row = cost_row(sym)
        if row.get("role") == "sold":
            continue
        if mark is not None and abs(mark) < SPOT_DUST_USD and abs(amt) < 1e-4:
            continue
        if mark is None and abs(amt) < 1e-4:
            continue
        if abs(amt) < 1e-8:
            continue
        entry = {
            "symbol": sym,
            "amount": p.get("amount_onchain"),
            "mark_usd": p.get("mark_usd"),
            "usd_per_token": p.get("usd_per_token"),
            "mark_source": p.get("mark_source"),
        }
        positions.append(attach_cost(entry, sym))

    bals = snap.get("balances") or {}
    usd = snap.get("usd_values") or {}
    residuals = []
    weth_amt = _f(bals.get("weth"))
    if weth_amt and weth_amt > 0:
        residuals.append(
            attach_cost(
                {
                    "symbol": "WETH",
                    "amount": bals.get("weth"),
                    "mark_usd": usd.get("weth"),
                    "role": "spot_residual",
                },
                "WETH",
            )
        )
    # RBLX: only if still held with material balance — ALTROT sold to 0
    rblx_amt = _f(bals.get("rblx"), 0.0) or 0.0
    rblx_mark = _f(usd.get("rblx"), 0.0) or 0.0
    if rblx_amt > 1e-6 and rblx_mark >= SPOT_DUST_USD and cost_row("RBLX").get("role") != "sold":
        residuals.append(
            attach_cost(
                {
                    "symbol": "RBLX",
                    "amount": bals.get("rblx"),
                    "mark_usd": usd.get("rblx"),
                    "role": "spot_residual",
                },
                "RBLX",
            )
        )

    known_cost = 0.0
    known_pnl = 0.0
    known_n = 0
    for e in positions + residuals:
        if e.get("status") == "SOLD":
            continue
        c = e.get("cost_usdg")
        if c is None:
            continue
        try:
            known_cost += float(c)
            if e.get("unrealized_pnl_usd") is not None:
                known_pnl += float(e["unrealized_pnl_usd"])
            known_n += 1
        except (TypeError, ValueError):
            pass

    return {
        "positions": positions,
        "residuals": residuals,
        "cost_usd": round(known_cost, 4) if known_n else None,
        "unrealized_pnl_usd": round(known_pnl, 4) if known_n else None,
        "spot_tokens_sum_usd": usd.get("spot_tokens_sum_usd"),
        "spot_incl_weth_rblx_usd": usd.get("spot_incl_weth_residuals_usd"),
        "status": snap.get("spot_posture") or "HOLD",
        "source": source_label,
        "cost_source": "SPOT-COST-LEDGER" if by_sym else None,
        "observed_at_jst": snap.get("observed_at_jst"),
    }


def main():
    now = datetime.now(JST)
    meme = load_json(MEME_ROOT / "STATE.json")
    lp_state = load_json(LP_STATE)
    sm3, sm3_source = load_sm3_snap()
    static = load_json(STATIC)
    cost_ledger = load_json(SPOT_COST_LEDGER)
    nav, nav_name = latest_nav()
    # Prefer STATE open_positions amounts (post-ST bags); ALTROT only fills gaps.
    amount_by_sym = {}
    bals_memes = (sm3.get("balances") or {}).get("memes") or {}
    for sym, amt in bals_memes.items():
        if amt is not None:
            amount_by_sym[sym] = amt
    for mp in sm3.get("meme_positions") or []:
        if isinstance(mp, dict) and mp.get("symbol") and mp.get("amount_onchain") is not None:
            amount_by_sym[mp["symbol"]] = mp.get("amount_onchain")
    positions = meme.get("open_positions") or []
    for p in positions:
        if isinstance(p, dict) and p.get("symbol") and p.get("amount") is not None:
            amount_by_sym[p["symbol"]] = p.get("amount")
    pub_pos = public_positions(positions, amount_by_sym)
    meme_cost = sum(float(p.get("cost_usdg") or 0) for p in pub_pos)
    meme_mark = sum(float(p.get("mark_usd") or 0) for p in pub_pos if p.get("mark_usd") is not None)
    if meme.get("meme_mark_exit_sum_usd") is not None:
        try:
            meme_mark = float(meme.get("meme_mark_exit_sum_usd"))
        except (TypeError, ValueError):
            pass
    lp_nav = 0.0  # post-SM3 LP cleared
    surplus = nav.get("surplus_usdg_excluded")
    try:
        surplus_f = float(surplus) if surplus is not None else None
    except (TypeError, ValueError):
        surplus_f = None
    usd = sm3.get("usd_values") or {}
    spot_incl = usd.get("spot_incl_weth_residuals_usd")
    prev_snap = load_json(OUT)
    idle_usdg, idle_usdg_source, idle_usdg_err = resolve_idle_usdg(
        usd.get("idle_usdg_usd"), prev_snap
    )
    native_eth = usd.get("native_eth")
    approx_mtm = None
    try:
        approx_mtm = float(meme_mark or 0.0)
        if spot_incl is not None:
            approx_mtm += float(spot_incl)
        if idle_usdg is not None:
            approx_mtm += float(idle_usdg)
        if native_eth is not None:
            approx_mtm += float(native_eth)
        # spot residuals already in spot_incl; keep explicit if separately valued later
        approx_mtm = round(approx_mtm, 4)
    except (TypeError, ValueError):
        approx_mtm = None
    soft = meme.get("soft_alert") if isinstance(meme.get("soft_alert"), dict) else {}
    mark_source = "quoter_v2_exit+live_usdg_balanceOf"
    if idle_usdg_source != "onchain_balanceOf":
        mark_source = f"quoter_v2_exit+{idle_usdg_source}"
    snap = {
        "schema_version": 3,
        "generated_at_jst": now.isoformat(),
        "label": "READ-ONLY PUBLIC SNAPSHOT",
        "live": True,
        "mark_source": mark_source,
        "lab": {
            "name": "RH Autonomous LP Lab",
            "chain_id": 4663,
            "dex": "uniswap-v3",
            "wallet_public": "0xeb2e…4c7b",
            "leverage": False,
        },
        "mandate": {
            "plan": (sm3.get("mandate") or {}).get("plan")
            or (static.get("mandate_defaults") or {}).get("plan")
            or "SM3-52/46/02",
            "b0_usd": 1881.69,
            "target_3x_usd": 5645.07,
            "primary_target_multiple": 3,
            "target_5x_usd": 9408.45,
            "split": (sm3.get("mandate") or {}).get("split")
            or {"spot_pct": 52, "meme_pct": 46, "gas_pct": 2, "perp_pct": 0, "lp_pct": 0},
        },
        "caps": {
            "lp_simultaneous_usd": 800,
            "lp_max_positions": 3,
            "meme_per_trade_usd": 100,
            "meme_sleeve_usd": 1000,
        },
        "lp": {
            "simultaneous_usd": 0,
            "nav_usd": lp_nav,
            "start_nav_usd": nav.get("start_nav_usd"),
            "nft_ids": [],
            "pools": [],
            "note": "LP canary NFTs burned in SM3 exit; not live",
            "status": "EXITED/CLEARED",
            "npm_balanceOf": 0,
            "source_nav_file": nav_name,
            "checked_at_jst": (sm3.get("observed_at_jst") or nav.get("checked_at_jst")),
        },
        "spot": public_spot(sm3, cost_ledger, sm3_source)
        if sm3
        else {"positions": [], "status": "UNKNOWN"},
        "meme": {
            "positions": pub_pos,
            "cost_usd": meme_cost,
            "mark_usd_exit": round(meme_mark, 4),
            "unrealized_pnl_usd": round(meme_mark - meme_cost, 4) if meme_cost else None,
            "status": "HOLD",
            "soft_alert_active": bool(soft.get("active")) if soft else None,
            "marks_updated_at_jst": meme.get("marks_updated_at_jst"),
            "marks_note": "Exit marks via QuoterV2 full-size; PONS/NUDES/NEKO only (MEME sold)",
        },
        "wallet": {
            "approx_mtm_usd": approx_mtm,
            "idle_usdg_usd": idle_usdg,
            "idle_usdg_source": idle_usdg_source,
            "idle_usdg_rpc_error": idle_usdg_err,
            "native_eth_usd": native_eth,
            "weth_usd": usd.get("weth"),
            "surplus_usdg_excluded": surplus_f,
            "note": "approx = idle USDG (live balanceOf each publish) + meme QuoterV2 exit + native ETH (+ spot residuals if any)",
            "b0_frozen_usd": 1881.69,
            "target_3x_usd": 5645.07,
            "target_5x_usd": 9408.45,
            "vs_b0_usd": round(approx_mtm - 1881.69, 4) if approx_mtm is not None else None,
        },
        "deploy": {
            "status": "STOP",
            "completed": [
                "Spot T1",
                "Spot T2",
                "Spot T3",
                "Meme M1",
                "Meme M2",
                "ALTROT stock sells",
                "Meme 0012-0014 adds",
            ],
            "aborted": ["Meme M3"],
            "m3_note": (
                ((sm3.get("m3_abort") or {}).get("note") if isinstance(sm3.get("m3_abort"), dict) else None)
                or "STOP further buys"
            ),
            "idle_usdg_usd": idle_usdg,
            "stop_further_buys": True,
            "spot_posture": sm3.get("spot_posture") or "HOLD_USDG",
        },
        "timeline": list(KNOWN_FILLS) + list((static.get("sm3_timeline_extra") or [])),
        "notes": [
            "No secrets. No Alchemy keys. No session material.",
            "Post-SM3 + ALTROT: LP EXITED/CLEARED. Spot HOLD_USDG + WETH hop; stocks sold.",
            "Idle USDG from live on-chain balanceOf each publish (not SM3-ALTROT-POST-SNAP).",
            "Meme amounts prefer rh-meme-lab STATE open_positions (post-ST bags).",
            "Spot cost_usdg from handoff/SPOT-COST-LEDGER; sold stocks cost-zeroed / omitted.",
            "Primary target 3x ($5645.07 from B0 $1881.69); 5x secondary only.",
            "Deploy STOP; no new spot alts / meme adds until Chief.",
            "Refreshed roughly every 5 minutes when publish routine runs.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n")
    print("wrote", OUT, "source=", sm3_source, "idle_usdg=", idle_usdg, "idle_src=", idle_usdg_source, "approx_mtm=", approx_mtm)


if __name__ == "__main__":
    main()
