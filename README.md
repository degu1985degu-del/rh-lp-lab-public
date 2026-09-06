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
