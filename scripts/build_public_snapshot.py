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
    files = sorted((LP_ROOT / "pnl").glob("*triple-nav*.json"))
    if not files:
        return {}
    return load_json(files[-1])


def main():
    now = datetime.now(JST)
    meme = load_json(MEME_ROOT / "STATE.json")
    nav = latest_nav()
    positions = meme.get("open_positions") or []
    meme_cost = sum(float(p.get("cost_usdg") or 0) for p in positions)
    snap = {
        "schema_version": 1,
        "generated_at_jst": now.isoformat(),
        "label": "READ-ONLY PUBLIC SNAPSHOT",
        "live": False,
        "lab": {
            "name": "RH Autonomous LP Lab",
            "chain_id": 4663,
            "dex": "uniswap-v3",
            "wallet_public": "0xeb2e…4c7b",
            "leverage": False,
        },
        "caps": {
            "lp_simultaneous_usd": 800,
            "lp_max_positions": 3,
            "meme_per_trade_usd": 100,
            "meme_sleeve_usd": 1000,
        },
        "lp": {
            "simultaneous_usd": nav.get("simultaneous_lp_usd"),
            "nav_usd": nav.get("nav_usd"),
            "start_nav_usd": nav.get("start_nav_usd"),
            "nft_ids": [986899, 1002007, 1016424],
            "pools": [
                {"pair": "WETH/USDG", "fee": "0.01%", "role": "hub"},
                {"pair": "USDG/RBLX", "fee": "0.3%", "role": "farm"},
                {"pair": "DJT/USDG", "fee": "1%", "role": "farm"},
            ],
            "status": "HOLD",
            "source_nav_file": None,
        },
        "meme": {
            "positions": positions,
            "cost_usd": meme_cost,
            "status": "HOLD",
            "marks_note": "Any mark/PnL fields are INFERENCE unless explicitly labeled on-chain",
        },
        "timeline": KNOWN_FILLS,
        "notes": [
            "No secrets. No Alchemy keys. No session material.",
            "LP NAV and meme cost are separate books sharing one physical wallet.",
        ],
    }
    # attach nav filename only (not path with home)
    files = sorted((LP_ROOT / "pnl").glob("*triple-nav*.json"))
    if files:
        snap["lp"]["source_nav_file"] = files[-1].name
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
