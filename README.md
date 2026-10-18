# oakencode-website

The Oakencode website (oakencode.com) — homepage, `/apps/` section, and privacy policy.

## Layout

- `site/` — the built website. This is the publish directory for Cloudflare Pages.
  - `index.html` — homepage
  - `apps/` — apps index + one subpage per app
  - `pers-int-privacy/` — Pers-int privacy policy (kept identical to the approved page)
  - `assets/` — seal, app icons, art
- `build.py` — regenerates `site/` from the approved copy baked into the script.
- `assets-src/` — source art (seal).

## Regenerating

```bash
python3 build.py
```

Copy lives in `build.py`. Statuses are words, never dates — update a badge in
`build.py` and rebuild when reality changes.

## Deploy

Cloudflare Pages → connect this repo → publish directory `site/`.
Custom domain: oakencode.com.
