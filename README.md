# rh-lp-lab-public

Secret-free public snapshot feed + static dashboard for RH Autonomous LP Lab.

## Data
- `data/latest.json` — overwritten by lab snapshot job (no secrets)
- `data/equity_history.json` — durable challenge-level MTM series; also embedded in `latest.json` as `equity_history`
- `equity_history[]` records: `{ at_jst, total_assets_usd, baseline_usd, pnl_usd, quality }`
  - `total_assets_usd` matches `wallet.approx_mtm_usd` (idle USDG + meme QuoterV2 exit + native ETH + spot residuals; no double-count)
  - `baseline_usd` is frozen B0 **1881.69** (never overwritten with daily NAV)
  - `pnl_usd` is challenge-level `total − B0`, not cumulative trade P&L
  - `quality` is `estimated` | `partial` (retained fallback, e.g. RPC 429 idle USDG) | `unavailable` (numerics `null`, never coerced to 0)
  - Front-ends (including ChatGPT Sites) can plot `equity_history`; this repo also draws a small PnL chart on `index.html`

## Local preview
```bash
python3 -m http.server 8080
# open http://localhost:8080/
```

## GitHub Pages
Settings → Pages → Deploy from branch `main` / root.

## Snapshot build notes
- `scripts/build_public_snapshot.py` refreshes `data/latest.json`.
- **Idle USDG** is read live each publish via public-RPC `balanceOf` on USDG (`0x5fc5…d168`) for the lab wallet — not the frozen SM3-ALTROT-POST-SNAP value.
- On RPC 403/429, the builder retains the previous live idle USDG when fresher than ALTROT; it does not silently revert to the stale ALTROT figure. Retained inputs mark the new `equity_history` point as `quality=partial`.
- Each publish appends/merges into `data/equity_history.json` (dedupe by `at_jst`, ascending). Older points may downsample to ~10–15 min if the series grows large; the latest evaluation is always kept.
- Meme position `amount` fields prefer `/workspace/rh-meme-lab/STATE.json` `open_positions` (post-ST bags).
- Publish entrypoint: `/workspace/rh-lp-lab/bin/publish-public-snapshot`.

