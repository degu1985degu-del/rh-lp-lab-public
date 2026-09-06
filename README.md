# rh-lp-lab-public

Secret-free public snapshot feed + static dashboard for RH Autonomous LP Lab.

## Data
- `data/latest.json` — overwritten by lab snapshot job (no secrets)

## Docs
- `docs/SOL-4663-EARNING-LANDSCAPE.md` — Sol research: what an EVM wallet can actually earn/trade on chain 4663 (FACT vs INFERENCE; not a policy change)
- `docs/SOL-LIGHTER-PERP-UNLOCK-CHECKLIST.md` — Sol prep: path toward Lighter perps (DRAFT only; live `perp_pct=0`)
- `docs/SOL-LIGHTER-DEPOSIT-CANARY-APPENDIX.md` — Human FINAL packet: $50 USDG deposit only (no orders)
- `docs/SOL-LIGHTER-ORDER-CANARY-APPENDIX.md` — Human packet: one isolated ≤2x ETH/BTC-PERP open+close (appendix only; no agent orders)
- `docs/SOL-ARCUS-CANARY-APPENDIX.md` — Arcus on 4663: spot vs perps; recommended ≤$50 spot round-trip (appendix only; Lighter $50 untouched)
- `docs/SOL-SNIPE-ROUTINE-REVIEW.md` — Is the current Uniswap Scout/Chief routine enough to snipe 4663 hot coins early? (research only)

## Local preview
```bash
python3 -m http.server 8080
# open http://localhost:8080/
```

## GitHub Pages
Settings → Pages → Deploy from branch `main` / root.
