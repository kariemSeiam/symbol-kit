---
name: render-preview
description: Generate visual HTML proof pages from symbol-kit atoms. Verify how glyphs render across contexts (standalone, body, code, pre, RTL) before shipping.
---

# Render Preview

Generate HTML proof pages to visually verify glyph rendering before shipping a UI.

## Quick preview

```bash
# Generate all proof pages
python3 scripts/render-harness.py

# Tier 0 only (fast smoke test)
python3 scripts/render-harness.py --smoke

# Serve locally
python3 -m http.server 8080 -d render-proofs/
```

## What you get

Each proof page renders every atom in 5 canonical contexts:

1. **Standalone** — large, centered glyph
2. **Body** — embedded in running text
3. **`<code>`** — inside inline monospace
4. **`<pre>`** — inside a monospace block (tests terminal rendering)
5. **RTL** — inside Arabic RTL container (tests bidi behavior)

## Generated pages

| File | Contents |
|------|----------|
| `tier-0-pocket.html` | 13 Tier-0 atoms |
| `tier-1-daily.html` | 46 Tier-1 atoms |
| `tier-2-workshop.html` | 57 Tier-2 atoms |
| `tier-3-library.html` | 13 Tier-3 atoms |
| `all-vibes-side-by-side.html` | All 8 vibes |
| `widget-gallery.html` | Widget examples |
| `rtl-arabic-showcase.html` | Arabic/RTL atoms |

## What to check

1. **No tofu (□)**: Every glyph should render correctly
2. **Monospace alignment**: Box-drawing and progress bars should align
3. **RTL behavior**: Arabic text flows right-to-left, arrows mirror correctly
4. **Weight consistency**: No visually jarring weight mismatches
5. **Color intrusion**: Monochrome guarantee holds (no colored emoji by surprise)

## After checking

- Update `platforms.yaml` with verified renders
- Mark `renders: yes` for tested platforms
- Flag `tofu` or `fallback` findings in the atom's YAML file
- Add platform screenshots to `platforms/manual-verification/`
