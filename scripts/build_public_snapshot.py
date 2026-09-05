#!/usr/bin/env python3
"""Build secret-free public snapshot for RH LP Lab dash."""
from __future__ import annotations
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
LP_ROOT = Path("/workspace/rh-lp-lab")
MEME_ROOT = Path("/workspace/rh-meme-lab")
OUT = Path(__file__).resolve().parents[1] / "data" / "latest.json"
SM3_SNAP = Path("/workspace/rh-lp-lab/handoff/SM3-POST-DEPLOY-SNAP.json")
LP_STATE = Path("/workspace/rh-lp-lab/STATE.json")
STATIC = Path(__file__).resolve().parent / "public_snapshot_static.json"

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
        if sym not in ("PONS", "NUDES", "NEKO"):
            continue
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


def public_spot(snap):
    positions = []
    for p in snap.get("spot_positions") or []:
        if not isinstance(p, dict):
            continue
        positions.append({
            "symbol": p.get("symbol"),
            "amount": p.get("amount_onchain"),
            "mark_usd": p.get("mark_usd"),
            "usd_per_token": p.get("usd_per_token"),
            "mark_source": p.get("mark_source"),
        })
    bals = snap.get("balances") or {}
    usd = snap.get("usd_values") or {}
    residuals = []
    if bals.get("weth"):
        residuals.append({"symbol": "WETH", "amount": bals.get("weth"), "mark_usd": usd.get("weth"), "role": "spot_residual"})
    if bals.get("rblx"):
        residuals.append({"symbol": "RBLX", "amount": bals.get("rblx"), "mark_usd": usd.get("rblx"), "role": "spot_residual"})
    return {
        "positions": positions,
        "residuals": residuals,
        "spot_tokens_sum_usd": usd.get("spot_tokens_sum_usd"),
        "spot_incl_weth_rblx_usd": usd.get("spot_incl_weth_residuals_usd"),
        "status": "HOLD",
        "source": "SM3-POST-DEPLOY-SNAP",
        "observed_at_jst": snap.get("observed_at_jst"),
    }


def main():
    now = datetime.now(JST)
    meme = load_json(MEME_ROOT / "STATE.json")
    lp_state = load_json(LP_STATE)
    sm3 = load_json(SM3_SNAP)
    static = load_json(STATIC)
    nav, nav_name = latest_nav()
    amount_by_sym = {}
    for mp in sm3.get("meme_positions") or []:
        if isinstance(mp, dict) and mp.get("symbol"):
            amount_by_sym[mp["symbol"]] = mp.get("amount_onchain")
    positions = meme.get("open_positions") or []
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
    idle_usdg = usd.get("idle_usdg_usd")
    native_eth = usd.get("native_eth")
    approx_mtm = None
    if spot_incl is not None:
        try:
            approx_mtm = float(spot_incl) + float(meme_mark)
            if idle_usdg is not None:
                approx_mtm += float(idle_usdg)
            if native_eth is not None:
                approx_mtm += float(native_eth)
            approx_mtm = round(approx_mtm, 4)
        except (TypeError, ValueError):
            approx_mtm = None
    soft = meme.get("soft_alert") if isinstance(meme.get("soft_alert"), dict) else {}
    snap = {
        "schema_version": 3,
        "generated_at_jst": now.isoformat(),
        "label": "READ-ONLY PUBLIC SNAPSHOT",
        "live": True,
        "mark_source": "quoter_v2_exit+sm3_post_deploy_snap",
        "lab": {
            "name": "RH Autonomous LP Lab",
            "chain_id": 4663,
            "dex": "uniswap-v3",
            "wallet_public": "0xeb2e…4c7b",
            "leverage": False,
        },
        "mandate": {
            "plan": (sm3.get("mandate") or {}).get("plan") or (static.get("mandate_defaults") or {}).get("plan") or "SM3-52/46/02",
            "b0_usd": 1881.69,
            "target_3x_usd": 5645.07,
            "primary_target_multiple": 3,
            "target_5x_usd": 9408.45,
            "split": (sm3.get("mandate") or {}).get("split") or {"spot_pct": 52, "meme_pct": 46, "gas_pct": 2, "perp_pct": 0, "lp_pct": 0},
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
        "spot": public_spot(sm3) if sm3 else {"positions": [], "status": "UNKNOWN"},
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
            "native_eth_usd": native_eth,
            "weth_usd": usd.get("weth"),
            "surplus_usdg_excluded": surplus_f,
            "note": "approx = spot(incl WETH+RBLX) + meme QuoterV2 exit + idle USDG + native ETH",
            "b0_frozen_usd": 1881.69,
            "target_3x_usd": 5645.07,
            "target_5x_usd": 9408.45,
            "vs_b0_usd": round(approx_mtm - 1881.69, 4) if approx_mtm is not None else None,
        },
        "deploy": {
            "status": "STOP",
            "completed": ["Spot T1", "Spot T2", "Spot T3", "Meme M1", "Meme M2"],
            "aborted": ["Meme M3"],
            "m3_note": ((sm3.get("m3_abort") or {}).get("note") if isinstance(sm3.get("m3_abort"), dict) else None) or "Meme M3 aborted low USDG; STOP further buys",
            "idle_usdg_usd": idle_usdg,
            "stop_further_buys": True,
        },
        "timeline": list(KNOWN_FILLS) + list((static.get("sm3_timeline_extra") or [])),
        "notes": [
            "No secrets. No Alchemy keys. No session material.",
            "Post-SM3: LP EXITED/CLEARED. Spot 52% + Meme 46% + Gas 2%.",
            "Primary target 3x ($5645.07 from B0 $1881.69); 5x secondary only.",
            "Deploy STOP after Spot T1-T3 + Meme M1-M2; M3 aborted (low USDG).",
            "Refreshed roughly every 5 minutes when publish routine runs.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
