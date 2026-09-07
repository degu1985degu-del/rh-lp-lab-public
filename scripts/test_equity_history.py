#!/usr/bin/env python3
"""Unit tests for equity_history accumulate / quality / downsample."""
from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from equity_history import (
    B0_USD,
    QUALITY_ESTIMATED,
    QUALITY_PARTIAL,
    QUALITY_UNAVAILABLE,
    accumulate,
    downsample_records,
    infer_quality,
    make_record,
    meme_marks_are_partial,
    merge_records,
    record_from_live_build,
    record_from_snapshot,
    MAX_POINTS_BEFORE_DOWNSAMPLE,
)


class QualityTests(unittest.TestCase):
    def test_unavailable_when_total_missing(self):
        self.assertEqual(
            infer_quality(total_assets_usd=None),
            QUALITY_UNAVAILABLE,
        )

    def test_estimated_when_live(self):
        self.assertEqual(
            infer_quality(
                total_assets_usd=1900.0,
                idle_usdg_source="onchain_balanceOf",
                mark_source="quoter_v2_exit+live_usdg_balanceOf",
            ),
            QUALITY_ESTIMATED,
        )

    def test_partial_when_idle_retained(self):
        self.assertEqual(
            infer_quality(
                total_assets_usd=1900.0,
                idle_usdg_source="previous_live_retained",
                idle_usdg_rpc_error="HTTP Error 429: Too Many Requests",
            ),
            QUALITY_PARTIAL,
        )

    def test_partial_when_altrot_stale_fallback(self):
        self.assertEqual(
            infer_quality(
                total_assets_usd=1900.0,
                idle_usdg_source="sm3_altrot_post_snap_stale",
            ),
            QUALITY_PARTIAL,
        )

    def test_historical_altrot_primary_source_is_estimated(self):
        # Then-current method, not a soft-fail retain.
        rec = record_from_snapshot(
            {
                "generated_at_jst": "2026-09-06T11:44:27.934894+09:00",
                "mark_source": "quoter_v2_exit+sm3_altrot_post_snap",
                "wallet": {
                    "approx_mtm_usd": 1871.7828,
                    "idle_usdg_usd": 844.379235,
                },
            }
        )
        self.assertEqual(rec["quality"], QUALITY_ESTIMATED)
        self.assertEqual(rec["pnl_usd"], round(1871.7828 - B0_USD, 4))

    def test_pre_mtm_schema_skipped(self):
        self.assertIsNone(
            record_from_snapshot(
                {
                    "generated_at_jst": "2026-09-05T11:31:28.223936+09:00",
                    "schema_version": 1,
                    "wallet": {},
                }
            )
        )

    def test_null_mtm_is_unavailable_not_zero(self):
        rec = record_from_snapshot(
            {
                "generated_at_jst": "2026-09-05T19:40:17.765390+09:00",
                "mark_source": "quoter_v2_exit+triple_nav",
                "wallet": {"approx_mtm_usd": None},
            }
        )
        self.assertEqual(rec["quality"], QUALITY_UNAVAILABLE)
        self.assertIsNone(rec["total_assets_usd"])
        self.assertIsNone(rec["pnl_usd"])
        self.assertEqual(rec["baseline_usd"], B0_USD)


class RecordTests(unittest.TestCase):
    def test_pnl_vs_frozen_b0(self):
        rec = make_record(
            at_jst="2026-09-07T12:00:00+09:00",
            total_assets_usd=1900.00,
            quality="estimated",
        )
        self.assertEqual(rec["baseline_usd"], 1881.69)
        self.assertEqual(rec["pnl_usd"], 18.31)
        self.assertEqual(rec["total_assets_usd"], 1900.0)

    def test_unavailable_forces_nulls(self):
        rec = make_record(
            at_jst="2026-09-07T12:00:00+09:00",
            total_assets_usd=0.0,
            quality="unavailable",
        )
        self.assertIsNone(rec["total_assets_usd"])
        self.assertIsNone(rec["pnl_usd"])

    def test_live_build_partial_stale_meme_marks(self):
        rec = record_from_live_build(
            generated_at_jst="2026-09-07T12:00:00+09:00",
            approx_mtm=1850.0,
            idle_usdg_source="onchain_balanceOf",
            idle_usdg_rpc_error=None,
            mark_source="quoter_v2_exit+live_usdg_balanceOf",
            meme={
                "positions": [
                    {
                        "symbol": "PONS",
                        "mark_usd": 11.0,
                        "mark_source": "quoter_v2_exit",
                        "marks_updated_at_jst": "2026-09-07T11:00:00+09:00",
                    }
                ]
            },
        )
        self.assertEqual(rec["quality"], QUALITY_PARTIAL)

    def test_meme_fresh_marks_not_partial(self):
        at = datetime.fromisoformat("2026-09-07T12:00:00+09:00")
        self.assertFalse(
            meme_marks_are_partial(
                {
                    "positions": [
                        {
                            "mark_source": "quoter_v2_exit",
                            "marks_updated_at_jst": "2026-09-07T11:55:00+09:00",
                        }
                    ]
                },
                at,
            )
        )


class MergeDownsampleTests(unittest.TestCase):
    def test_dedupe_same_at_jst_last_wins(self):
        a = make_record(at_jst="2026-09-07T12:00:00+09:00", total_assets_usd=1, quality="estimated")
        b = make_record(at_jst="2026-09-07T12:00:00+09:00", total_assets_usd=2, quality="partial")
        merged = merge_records([a], [b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["total_assets_usd"], 2.0)
        self.assertEqual(merged[0]["quality"], QUALITY_PARTIAL)

    def test_sort_ascending(self):
        later = make_record(at_jst="2026-09-07T13:00:00+09:00", total_assets_usd=2, quality="estimated")
        earlier = make_record(at_jst="2026-09-07T12:00:00+09:00", total_assets_usd=1, quality="estimated")
        merged = merge_records([later, earlier])
        self.assertEqual([r["at_jst"] for r in merged], [earlier["at_jst"], later["at_jst"]])

    def test_downsample_keeps_latest_and_thins_old(self):
        start = datetime.fromisoformat("2026-08-01T00:00:00+09:00")
        recs = []
        # 2-minute points over many days → large
        n = MAX_POINTS_BEFORE_DOWNSAMPLE + 200
        for i in range(n):
            at = (start + timedelta(minutes=2 * i)).isoformat()
            recs.append(make_record(at_jst=at, total_assets_usd=1800 + i * 0.01, quality="estimated"))
        out = downsample_records(recs)
        self.assertLess(len(out), len(recs))
        self.assertEqual(out[-1]["at_jst"], recs[-1]["at_jst"])
        self.assertEqual(out[0]["at_jst"], recs[0]["at_jst"])

    def test_no_downsample_when_small(self):
        recs = [
            make_record(at_jst=f"2026-09-07T12:0{i}:00+09:00", total_assets_usd=1900, quality="estimated")
            for i in range(3)
        ]
        self.assertEqual(downsample_records(recs), recs)


class AccumulateTests(unittest.TestCase):
    def test_persist_and_reload(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "equity_history.json"
            cur = make_record(
                at_jst="2026-09-07T12:00:00+09:00",
                total_assets_usd=1900.0,
                quality="estimated",
            )
            out = accumulate(
                current=cur,
                history_path=path,
                reconstruct_if_empty=False,
            )
            self.assertEqual(len(out), 1)
            raw = json.loads(path.read_text())
            self.assertEqual(raw["baseline_usd"], B0_USD)
            self.assertTrue(raw["note"].startswith("equity_history:"))
            again = make_record(
                at_jst="2026-09-07T12:05:00+09:00",
                total_assets_usd=1901.0,
                quality="estimated",
            )
            out2 = accumulate(
                current=again,
                history_path=path,
                reconstruct_if_empty=False,
            )
            self.assertEqual(len(out2), 2)
            self.assertEqual(out2[-1]["pnl_usd"], round(1901.0 - B0_USD, 4))


if __name__ == "__main__":
    unittest.main()
