---
name: lint-vibe
description: Check widget code blocks for vibe coherence violations. Every glyph in a widget must belong to its declared vibe's starter set or the cross-vibe allowlist.
---

# Lint Vibe

Enforce vibe coherence across all widget and vibe code blocks.

## Context

symbol-kit has 8 aesthetic vibes, each with a curated starter set of 30-50 atoms. When a widget declares `vibe: terminal-hacker`, every glyph in its code blocks must come from the terminal-hacker starter set or the cross-vibe allowlist (`● ○ ◐ → ← ↑ ↓ · — … ⋯ ✓ ✗`).

## How to lint

```bash
cd symbol-kit && python3 scripts/lint-vibe.py
```

## What it checks

1. Extracts all code blocks from `widgets.md`
2. Finds the declared vibe for each widget (YAML front matter)
3. Loads each vibe's starter set from `vibes/*.md`
4. Flags any glyph not in the declared vibe's set or cross-vibe allowlist
5. Reports which vibe the glyph actually belongs to

## Common fixes

- **Glyph belongs to wrong vibe**: Change the widget's declared vibe
- **Vibe missing the glyph**: Add the glyph to the vibe's starter set in `vibes/NN-name.md`
- **Cross-vibe glyph**: Add it to `compositions.md` §cross-vibe-allowlist

## Pre-commit

Run: `bash scripts/ci.sh` — includes lint-vibe as a gate.
