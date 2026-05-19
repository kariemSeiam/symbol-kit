---
name: compose-widget
description: Compose a UI widget from symbol-kit atoms, sets, and the grammar DSL. Pick a vibe, stay inside its starter set, use grammar functions.
---

# Compose Widget

Build a production UI element using symbol-kit's layered composition model.

## Quick start

```python
from symbolkit import render
render('STATUS_DOT("live") + " · " + PROGRESS(0.6)')
# → ● · ▰▰▰▰▰▰▱▱▱▱
```

## Composition workflow

### 1. Pick a vibe
Choose one of 8 vibes: `terminal-hacker | modern-minimal | maximalist-decorative | rtl-arabic-elegant | scientific-technical | game-ui | status-operational | diff-patch`

Read `vibes/NN-name.md` for the starter set and philosophy.

### 2. Find your atoms
Look up atoms by semantic meaning in `atoms/*.yaml`. Prefer Tier 0-1. Check `TIERS.md` for the cheatsheet.

### 3. Use grammar functions
Don't hand-assemble glyphs. Use stdlib:
- `STATUS_DOT(state)` → ● ◐ ○ ⊘
- `PROGRESS(pct, n=10)` → ▰▰▰▰▱▱▱▱▱▱
- `SEVERITY(level, max)` → ●●●○○
- `BAR(value, max, n)` → ▓▓▓▓░░░░
- `RATING(stars, max)` → ●●●○○
- `TREE(depth, last)` → ├── / └──
- `KASHIDA_FILL(text, width)` → جيولينكــــ
- `RETRY_NOTICE(sec)` → ↻ 30s

### 4. Validate
- Is weight class consistent? (run `lint-weight.py`)
- Are all glyphs from the declared vibe? (run `lint-vibe.py`)
- Any Tier 3+ atoms? Justify or replace.
- Is it monospace-safe if it uses box-drawing?

## Anti-patterns
- Mixing vibes in one element → AP-10
- Mixing weight classes → AP-01
- Stars + dots in same rating → AP-06
- Box-drawing in proportional fonts → AP-07

## Widget template

```markdown
---
vibe: terminal-hacker
weight: W1
tier_budget: { tier3: 0, tier4: 0 }
---

## Widget Name

[code block with glyphs]

**Composition:** [which compositions used]
**Sets:** [which sets used]
**Atoms:** [list atoms]

**Use when:** [context]
```
