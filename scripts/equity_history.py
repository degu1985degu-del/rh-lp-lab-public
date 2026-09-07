#!/usr/bin/env python3
"""Accumulate challenge-level wallet MTM history for the public snapshot.

PnL is vs frozen B0 ($1881.69), not cumulative realized trade P&L.
Missing totals stay null; retained/fallback inputs mark quality=partial.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

JST = timezone(timedelta(hours=9))
B0_USD = 1881.69
QUALITY_ESTIMATED = "estimated"
QUALITY_PARTIAL = "partial"
QUALITY_UNAVAILABLE = "unavailable"
QUALITIES = (QUALITY_ESTIMATED, QUALITY_PARTIAL, QUALITY_UNAVAILABLE)

# Soft-fail / retained idle sources from resolve_idle_usdg().
RETAINED_IDLE_SOURCES = frozenset(
    {
        "previous_live_retained",
        "previous_non_altrot_retained",
        "sm3_altrot_post_snap_stale",
    }
)
RETAINED_MARK_FRAGMENTS = (
    "previous_live_retained",
    "previous_non_altrot_retained",
    "sm3_altrot_post_snap_stale",
)

# Per-position meme marks older than this vs evaluation time → partial.
MEME_MARK_STALE = timedelta(minutes=20)

# Downsample only if the series gets large; keep recent cadence intact.
MAX_POINTS_BEFORE_DOWNSAMPLE = 2500
RECENT_KEEP_ALL = timedelta(hours=36)
OLD_MIN_SPACING = timedelta(minutes=10)
TIGHTER_OLD_SPACING = timedelta(minutes=15)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HISTORY_PATH = REPO_ROOT / "data" / "equity_history.json"
HISTORY_NOTE = (
    "equity_history: challenge-level wallet MTM (same scope as wallet.approx_mtm_usd) "
    "vs frozen B0 $1881.69; pnl_usd is not cumulative trade P&L. "
    "quality=partial when any input was a retained fallback (e.g. RPC 429 idle USDG); "
    "unavailable totals are null, never coerced to 0."
)


def _f(x, default=None):
    try:
        return float(x) if x is not None else default
    except (TypeError, ValueError):
        return default


def _parse_at(at: str | None) -> datetime | None:
    if not at or not isinstance(at, str):
        return None
    try:
        dt = datetime.fromisoformat(at)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=JST)
    return dt


def _round4(x: float | None) -> float | None:
    if x is None:
        return None
    return round(float(x), 4)


def infer_quality(
    *,
    total_assets_usd: float | None,
    idle_usdg_source: str | None = None,
    idle_usdg_rpc_error: str | None = None,
    mark_source: str | None = None,
    meme_marks_partial: bool = False,
    other_partial: bool = False,
) -> str:
    """Mirror builder soft-fail / retained-value paths."""
    if total_assets_usd is None:
        return QUALITY_UNAVAILABLE
    src = str(idle_usdg_source or "")
    if src in RETAINED_IDLE_SOURCES:
        return QUALITY_PARTIAL
    if idle_usdg_rpc_error:
        return QUALITY_PARTIAL
    ms = str(mark_source or "")
    if any(frag in ms for frag in RETAINED_MARK_FRAGMENTS):
        return QUALITY_PARTIAL
    if meme_marks_partial or other_partial:
        return QUALITY_PARTIAL
    return QUALITY_ESTIMATED


def meme_marks_are_partial(meme: dict | None, at: datetime | None) -> bool:
    """True when any open meme mark is a retained/stale fallback."""
    if not isinstance(meme, dict):
        return False
    positions = meme.get("positions") or []
    if not isinstance(positions, list):
        return False
    for p in positions:
        if not isinstance(p, dict):
            continue
        src = str(p.get("mark_source") or "")
        if src and src not in ("quoter_v2_exit",):
            return True
        ts = _parse_at(p.get("marks_updated_at_jst"))
        if at is not None and ts is not None and (at - ts) > MEME_MARK_STALE:
            return True
    return False


def make_record(
    *,
    at_jst: str,
    total_assets_usd: float | None,
    quality: str,
    baseline_usd: float = B0_USD,
) -> dict:
    q = quality if quality in QUALITIES else QUALITY_ESTIMATED
    total = _round4(total_assets_usd) if total_assets_usd is not None else None
    if q == QUALITY_UNAVAILABLE:
        total = None
    pnl = _round4(total - baseline_usd) if total is not None else None
    return {
        "at_jst": at_jst,
        "total_assets_usd": total,
        "baseline_usd": float(baseline_usd),
        "pnl_usd": pnl,
        "quality": q,
    }


def record_from_snapshot(snap: dict | None) -> dict | None:
    """Build a history row from a published snapshot. Skip pre-MTM schema."""
    if not isinstance(snap, dict):
        return None
    wallet = snap.get("wallet") if isinstance(snap.get("wallet"), dict) else {}
    if "approx_mtm_usd" not in wallet:
        return None
    at = snap.get("generated_at_jst")
    if not at:
        return None
    total = _f(wallet.get("approx_mtm_usd"))
    at_dt = _parse_at(at)
    meme_partial = meme_marks_are_partial(snap.get("meme") if isinstance(snap.get("meme"), dict) else {}, at_dt)
    quality = infer_quality(
        total_assets_usd=total,
        idle_usdg_source=wallet.get("idle_usdg_source"),
        idle_usdg_rpc_error=wallet.get("idle_usdg_rpc_error"),
        mark_source=snap.get("mark_source"),
        meme_marks_partial=meme_partial,
    )
    return make_record(at_jst=str(at), total_assets_usd=total, quality=quality)


def record_from_live_build(
    *,
    generated_at_jst: str,
    approx_mtm: float | None,
    idle_usdg_source: str | None,
    idle_usdg_rpc_error: str | None,
    mark_source: str | None,
    meme: dict | None,
) -> dict:
    at_dt = _parse_at(generated_at_jst)
    quality = infer_quality(
        total_assets_usd=approx_mtm,
        idle_usdg_source=idle_usdg_source,
        idle_usdg_rpc_error=idle_usdg_rpc_error,
        mark_source=mark_source,
        meme_marks_partial=meme_marks_are_partial(meme, at_dt),
    )
    return make_record(at_jst=generated_at_jst, total_assets_usd=approx_mtm, quality=quality)


def normalize_record(raw: Any) -> dict | None:
    if not isinstance(raw, dict):
        return None
    at = raw.get("at_jst")
    if not at:
        return None
    q = raw.get("quality")
    if q not in QUALITIES:
        total = _f(raw.get("total_assets_usd"))
        q = QUALITY_UNAVAILABLE if total is None else QUALITY_ESTIMATED
    total = _f(raw.get("total_assets_usd"))
    baseline = _f(raw.get("baseline_usd"), B0_USD)
    if baseline is None:
        baseline = B0_USD
    return make_record(at_jst=str(at), total_assets_usd=total, quality=q, baseline_usd=baseline)


def merge_records(*lists: Iterable) -> list[dict]:
    """Dedupe by identical at_jst (last write wins); ascending time."""
    by_at: dict[str, dict] = {}
    for lst in lists:
        if not lst:
            continue
        for raw in lst:
            rec = normalize_record(raw)
            if rec:
                by_at[rec["at_jst"]] = rec

    def sort_key(rec: dict):
        dt = _parse_at(rec["at_jst"])
        return (dt or datetime.min.replace(tzinfo=JST), rec["at_jst"])

    return sorted(by_at.values(), key=sort_key)


def downsample_records(records: list[dict]) -> list[dict]:
    """If large, thin older points to ~10–15 min. Always keep the latest point."""
    if len(records) <= MAX_POINTS_BEFORE_DOWNSAMPLE:
        return list(records)
    last_dt = _parse_at(records[-1].get("at_jst"))
    if last_dt is None:
        return list(records)
    cutoff = last_dt - RECENT_KEEP_ALL

    def thin(src: list[dict], spacing: timedelta) -> list[dict]:
        kept: list[dict] = []
        last_old: datetime | None = None
        n = len(src)
        for i, rec in enumerate(src):
            if i == n - 1:
                kept.append(rec)
                continue
            dt = _parse_at(rec.get("at_jst"))
            if dt is None or dt >= cutoff:
                kept.append(rec)
                continue
            if last_old is None or (dt - last_old) >= spacing:
                kept.append(rec)
                last_old = dt
        return kept

    out = thin(records, OLD_MIN_SPACING)
    if len(out) > MAX_POINTS_BEFORE_DOWNSAMPLE:
        out = thin(out, TIGHTER_OLD_SPACING)
    return out


def load_history_file(path: Path | None = None) -> list[dict]:
    path = path or DEFAULT_HISTORY_PATH
    if not path.is_file():
        return []
    try:
        raw = json.loads(path.read_text())
    except Exception:
        return []
    if isinstance(raw, list):
        return merge_records(raw)
    if isinstance(raw, dict):
        return merge_records(raw.get("records") or [])
    return []


def save_history_file(records: list[dict], path: Path | None = None) -> None:
    path = path or DEFAULT_HISTORY_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "rh-equity-history/v1",
        "baseline_usd": B0_USD,
        "note": HISTORY_NOTE,
        "records": records,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def reconstruct_from_git(repo: Path | None = None) -> list[dict]:
    """Walk committed data/latest.json. Do not fabricate gaps."""
    repo = repo or REPO_ROOT
    try:
        commits = subprocess.check_output(
            ["git", "log", "--reverse", "--format=%H", "--", "data/latest.json"],
            cwd=repo,
            text=True,
            timeout=90,
        ).strip().splitlines()
    except Exception:
        return []
    out: list[dict] = []
    for h in commits:
        try:
            raw = subprocess.check_output(
                ["git", "show", f"{h}:data/latest.json"],
                cwd=repo,
                text=True,
                timeout=30,
            )
            snap = json.loads(raw)
        except Exception:
            continue
        rec = record_from_snapshot(snap)
        if rec:
            out.append(rec)
    return merge_records(out)


def accumulate(
    *,
    current: dict,
    history_path: Path | None = None,
    prev_snap: dict | None = None,
    reconstruct_if_empty: bool = True,
    repo: Path | None = None,
) -> list[dict]:
    """Load durable history, optionally seed from git, append current, persist."""
    history_path = history_path or DEFAULT_HISTORY_PATH
    stored = load_history_file(history_path)
    prev_hist = []
    if isinstance(prev_snap, dict):
        prev_hist = prev_snap.get("equity_history") or []
    seeded: list[dict] = []
    if reconstruct_if_empty and not stored and not prev_hist:
        seeded = reconstruct_from_git(repo)
    merged = downsample_records(merge_records(seeded, stored, prev_hist, [current]))
    save_history_file(merged, history_path)
    return merged


def ensure_history_note(notes: list | None) -> list:
    notes = list(notes or [])
    if not any(isinstance(n, str) and n.startswith("equity_history:") for n in notes):
        notes.append(HISTORY_NOTE)
    return notes
