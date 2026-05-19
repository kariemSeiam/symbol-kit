# Platform Compatibility

Human-readable matrix. Machine-readable version: `platforms.yaml`.

---

## Legend

| Mark | Meaning |
|------|---------|
| ✓ | Renders correctly (tested) |
| □ | Tofu / undefined glyph |
| ○ | Fallback substitution |
| ? | Untested |

---

## Tier 0 Atoms

| Atom | Telegram iOS | Telegram Android | Telegram Desktop | Telegram Web | iMessage | WhatsApp | Discord | Slack | GitHub MD | VS Code | Terminal* | Print/PDF |
|------|:----------:|:----------------:|:----------------:|:------------:|:--------:|:--------:|:-------:|:-----:|:---------:|:-------:|:---------:|:---------:|
| ● | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ○ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ◐ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ✓ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ✗ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ⚠ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| → | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| · | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| — | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ▰ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ▱ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| ⋯ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |

*Terminal = Monaco, Cascadia Code, JetBrains Mono, SF Mono, default Linux mono

---

## Methodology

1. Render each atom in a canonical context (footer, body, `<code>`, `<pre>`, RTL div).
2. Screenshot across browser engines (Chromium, Firefox, WebKit, mobile Safari).
3. Compare to reference fingerprint.
4. Mark: ✓ correct, □ tofu, ○ fallback, ? untested.

For Telegram clients: manual verification with actual app on device. Screenshot stored in `platforms/manual-verification/`.

---

## Untested Policy

Every atom × platform pair starts as `?`. It moves to ✓ / □ / ○ only after explicit testing. There are no default assumptions.
