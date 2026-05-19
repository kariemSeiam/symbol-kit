# symbol-kit

> A glyph design system, not a catalog. Compose with confidence.

## What

`symbol-kit` answers:

> Given a UI to build, which glyphs should I use, in what combinations, in what aesthetic register, that will render correctly across the platforms I actually ship to — and how do I know it works?

## The Pocket (Tier 0 — memorize these 12)

| # | Glyph | Atom | Use |
|---|-------|------|-----|
| 1 | ● | black-circle | live / on |
| 2 | ○ | white-circle | offline / off |
| 3 | ◐ | circle-with-left-half-black | partial / idle |
| 4 | ✓ | check-mark | success |
| 5 | ✗ | ballot-x | failure |
| 6 | ⚠ | warning-sign | caution |
| 7 | → | rightwards-arrow | next |
| 8 | · | middle-dot | separator |
| 9 | — | em-dash | divider |
| 10 | ▰ | black-parallelogram | progress filled |
| 11 | ▱ | white-parallelogram | progress empty |
| 12 | ⋯ | midline-horizontal-ellipsis | overflow |

## Quick Start

```python
from symbolkit import render

render('PROGRESS(0.6)')      # ▰▰▰▰▰▰▱▱▱▱
render('STATUS_DOT("live")') # ●
render('SEVERITY(2, 5)')     # ●●○○○
```

## The Eight Vibes

1. **terminal-hacker** — ncurses, htop, box-drawing
2. **modern-minimal** — Stripe, Linear, no frames
3. **maximalist-decorative** — stars, ornaments, flourishes
4. **rtl-arabic-elegant** — Arabic numerals, kashida, sacred ornaments
5. **scientific-technical** — math, Greek, precision
6. **game-ui** — chess, suits, rewards
7. **status-operational** — SRE, health, severity
8. **diff-patch** — git, code review, patches

## Structure

```
symbol-kit/
├── atoms/          # L0 — individual glyphs with metadata
├── pairs.md        # L1 — two-glyph relationships
├── sets.md         # L2 — n-glyph series
├── compositions.md # L3 — recipes
├── widgets.md      # L4 — full UI elements
├── vibes/          # L5 — aesthetic profiles
├── grammar/        # L6 — DSL + implementations
└── scripts/        # validation & build
```

## Validation

```bash
bash scripts/ci.sh
```

Runs: atom schema validation, cross-reference checks, vibe lint, weight lint, tier budget, grammar tests.

## License

MIT
