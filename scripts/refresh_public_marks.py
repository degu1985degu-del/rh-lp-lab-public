#!/usr/bin/env python3
"""Read-only QuoterV2 exit marks for open meme positions; updates STATE.json."""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))
MEME_ROOT = Path("/workspace/rh-meme-lab")
STATE_PATH = MEME_ROOT / "STATE.json"
TICKETS_DIR = MEME_ROOT / "tickets"
PUBLIC_RPC = "https://rpc.mainnet.chain.robinhood.com"
QUOTER_V2 = "0x33e885eD0Ec9bF04EcfB19341582aADCb4c8A9E7"
WETH = "0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73"
USDG = "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168"


def rpc_eth_call(to: str, data: str) -> str:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [{"to": to, "data": data}, "latest"],
    }
    req = urllib.request.Request(
        PUBLIC_RPC,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "rh-public-marks/0.1"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())
    if "error" in body:
        raise RuntimeError(str(body["error"]))
    return str(body.get("result") or "")


def quote_exact_input(path_hex: str, amount_in: int) -> int:
    sel = "cdca1753"
    head = f"{64:064x}" + f"{amount_in:064x}"
    raw = path_hex[2:] if path_hex.startswith("0x") else path_hex
    if len(raw) % 2:
        raw = "0" + raw
    blen = len(raw) // 2
    body = f"{blen:064x}" + raw + ("0" * ((32 - (blen % 32)) % 32 * 2))
    result = rpc_eth_call(QUOTER_V2, "0x" + sel + head + body)
    if not result or result == "0x":
        raise RuntimeError("empty quoter result")
    return int(result[2:66], 16)


def encode_exit_path(ticket: dict) -> tuple[str, list[str]]:
    """Buy was USDG-(hub fee)-WETH-(meme fee)-TOKEN; exit reverses."""
    errors: list[str] = []
    token_out = ticket.get("token_out") if isinstance(ticket.get("token_out"), dict) else {}
    route = ticket.get("route") if isinstance(ticket.get("route"), list) else []
    meme = str(token_out.get("address") or "").lower()
    if not meme.startswith("0x"):
        return "", ["missing token_out.address"]
    fees: list[int] = []
    for hop in route:
        if not isinstance(hop, dict):
            errors.append("bad hop")
            continue
        try:
            fees.append(int(hop.get("fee")))
        except (TypeError, ValueError):
            errors.append(f"bad fee {hop.get('fee')!r}")
    if errors:
        return "", errors
    if len(fees) != 2:
        return "", [f"need 2-hop buy route, got {len(fees)}"]
    # buy fees order: [hub USDG/WETH, meme/WETH] → exit [meme fee, hub fee]
    meme_fee, hub_fee = fees[1], fees[0]
    tokens = [meme, WETH.lower(), USDG.lower()]
    out = "0x"
    for i, fee in enumerate([meme_fee, hub_fee]):
        out += tokens[i].replace("0x", "")
        out += f"{fee:06x}"
    out += tokens[-1].replace("0x", "")
    return out, []


def load_ticket_for_symbol(symbol: str) -> dict | None:
    sym = symbol.upper()
    best = None
    # Prefer SM3-MEME buys (current book), fall back to legacy MEME-CANARY
    paths = sorted(TICKETS_DIR.glob("SM3-MEME-*.json")) + sorted(TICKETS_DIR.glob("MEME-CANARY-*.json"))
    for path in paths:
        try:
            t = json.loads(path.read_text())
        except Exception:
            continue
        if str(t.get("action") or "") not in ("swap_buy", "buy", ""):
            # still allow if token_out matches buy-shaped tickets
            pass
        tout = t.get("token_out") if isinstance(t.get("token_out"), dict) else {}
        tin = t.get("token_in") if isinstance(t.get("token_in"), dict) else {}
        if str(tout.get("symbol") or "").upper() != sym:
            continue
        # skip sells (token_in is the meme)
        if str(tin.get("symbol") or "").upper() == sym:
            continue
        best = t
    return best


def main() -> int:
    now = datetime.now(JST)
    state = json.loads(STATE_PATH.read_text())
    positions = state.get("open_positions") or []
    marks = []
    errors = []
    sum_exit = 0.0
    for pos in positions:
        if not isinstance(pos, dict):
            continue
        symbol = str(pos.get("symbol") or "")
        amount = float(pos.get("amount") or 0)
        cost = float(pos.get("cost_usdg") or 0)
        ticket = load_ticket_for_symbol(symbol)
        if not ticket:
            errors.append(f"{symbol}: no ticket")
            marks.append({"symbol": symbol, "mark_usd": pos.get("mark_usd"), "ok": False})
            if pos.get("mark_usd") is not None:
                sum_exit += float(pos.get("mark_usd") or 0)
            continue
        path, path_err = encode_exit_path(ticket)
        if path_err or not path:
            errors.append(f"{symbol}: {path_err}")
            marks.append({"symbol": symbol, "mark_usd": pos.get("mark_usd"), "ok": False})
            if pos.get("mark_usd") is not None:
                sum_exit += float(pos.get("mark_usd") or 0)
            continue
        decimals = int((ticket.get("token_out") or {}).get("decimals") or 18)
        amount_raw = int(amount * (10**decimals))
        mark = None
        last_err = None
        for attempt in range(4):
            try:
                if attempt:
                    time.sleep(0.8 * attempt)
                out_raw = quote_exact_input(path, amount_raw)
                mark = round(out_raw / 1e6, 4)  # USDG 6 decimals
                break
            except Exception as e:
                last_err = e
                msg = str(e)
                if "429" not in msg and "Too Many" not in msg:
                    break
                time.sleep(1.2)
        time.sleep(0.35)  # gentle spacing between symbols
        if mark is not None:
            pos["mark_usd"] = mark
            pos["unrealized_pnl_usd"] = round(mark - cost, 4)
            pos["mark_source"] = "quoter_v2_exit"
            pos["marks_updated_at_jst"] = now.isoformat()
            sum_exit += mark
            marks.append({"symbol": symbol, "mark_usd": mark, "ok": True})
        else:
            errors.append(f"{symbol}: {last_err}")
            marks.append({"symbol": symbol, "mark_usd": pos.get("mark_usd"), "ok": False})
            if pos.get("mark_usd") is not None:
                sum_exit += float(pos.get("mark_usd") or 0)

    state["open_positions"] = positions
    state["marks_updated_at_jst"] = now.isoformat()
    state["meme_mark_exit_sum_usd"] = round(sum_exit, 4)
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(STATE_PATH)
    summary = {
        "ok": len(errors) == 0,
        "measured_at_jst": now.isoformat(),
        "sum_exit": round(sum_exit, 4),
        "marks": marks,
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if marks else 1


if __name__ == "__main__":
    sys.exit(main())
