# rh-lp-lab-public

Secret-free public snapshot feed + static dashboard for RH Autonomous LP Lab.

## Data
- `data/latest.json` — overwritten by lab snapshot job (no secrets)

## Docs
- `docs/SOL-CLUE-DESIGN-3X.md` — Sol memo: HOT NAME clue weights for the 3× path (secret-free)

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
- On RPC 403/429, the builder retains the previous live idle USDG when fresher than ALTROT; it does not silently revert to the stale ALTROT figure.
- Meme position `amount` fields prefer `/workspace/rh-meme-lab/STATE.json` `open_positions` (post-ST bags).
- Publish entrypoint: `/workspace/rh-lp-lab/bin/publish-public-snapshot`.

