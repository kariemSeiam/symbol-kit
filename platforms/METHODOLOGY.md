# Platform Verification Methodology

How to verify glyph rendering across platforms.

---

## Test Setup

### Contexts

Render each glyph in 5 canonical contexts:

1. **Standalone** — the glyph by itself on a line
2. **Body paragraph** — embedded in running text
3. **`<code>` block** — inside inline monospace
4. **`<pre>` block** — inside a monospace block
5. **RTL container** — inside `<div dir="rtl">` with Arabic text

### Font stacks

| Context | Font stack |
|---------|------------|
| General | system-ui, -apple-system, sans-serif |
| Monospace | ui-monospace, SF Mono, Cascadia Code, Consolas, monospace |
| Terminal | Monaco, Cascadia Code, JetBrains Mono, SF Mono, default Linux mono |

### Browser engines

- Chromium (latest)
- Firefox (latest)
- WebKit (Playwright WebKit)
- Mobile Safari emulation (Playwright)

---

## Manual Verification (Telegram clients)

For Telegram-specific platforms, automated testing is not possible. Use manual verification:

1. Open Telegram on the target device
2. Send a message containing the glyph in each canonical context
3. Screenshot the result
4. Compare to reference rendering

### Required manual coverage for v0.1.0

| Platform | Tier 0 | Tier 1 |
|----------|--------|--------|
| Telegram iOS | all 12 | all 18 |
| Telegram Android | all 12 | all 18 |
| Telegram Desktop | all 12 | sample 5 |
| Telegram Web-K | all 12 | sample 5 |
| Telegram Web-A | all 12 | sample 5 |

Store screenshots in `platforms/manual-verification/`.

---

## Automated Verification (browser + terminal)

`scripts/render-harness.py` automates verification for:

- Browsers: Chrome, Safari, Firefox
- Code editors: VS Code, GitHub Markdown
- Terminals: Monaco, Cascadia Code, JetBrains Mono
- Print: Chrome headless PDF

### Fingerprints

Reference renderings are stored as pixel fingerprints in `render-proofs/fingerprints.yaml`.

Any glyph that deviates from its fingerprint by more than a threshold (5% pixel difference) is flagged for review.

### Tofu Detection

Glyphs that render as the undefined-glyph box (□, U+25A1 or similar) are automatically detected by comparing the rendered glyph's bounding box to known tofu patterns.

---

## Marking

| Mark | Meaning |
|------|---------|
| `yes` | Renders correctly — verified by test |
| `tofu` | Renders as undefined-glyph box |
| `fallback` | A different glyph appeared as substitution |
| `unverified` | Not yet tested |

Default for all new atoms: `unverified`.

---

## Smoke Test

Before v0.1.0 ships:

1. All 12 Tier-0 atoms pass automated harness (browser + terminal)
2. All 12 Tier-0 atoms manually verified on Telegram iOS + Android
3. Any `tofu` or `fallback` results are documented with remediation

Remediation options:
- Replace the glyph with a better-supported alternative
- Mark the glyph as Tier 4 (archive only)
- Document the platform limitation and provide a fallback atom
