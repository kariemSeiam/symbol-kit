---
name: select-atom
description: Given a semantic need and optional vibe, find the best glyph from symbol-kit's atom catalog. Returns full metadata including tier, weight, platform status, and alternatives.
---

# Select Atom

Look up the right glyph for a UI need using semantic search, not codepoint reference.

## How to select

### 1. Define your need semantically
Don't think "I need U+25CF." Think "I need a live/active status indicator."

### 2. Search atoms by semantic tags
```bash
grep -l "status:on\|status:live" atoms/*.yaml
# → atoms/black-circle.yaml
```

Or read the semantic field directly:
```python
import yaml
with open('atoms/black-circle.yaml') as f:
    atom = yaml.safe_load(f)
print(atom['semantic']['primary'])  # → status:on
print(atom['tier'])                  # → 0
print(atom['vibes'])                 # → ['terminal-hacker', 'modern-minimal', ...]
```

### 3. Filter by constraints
- **Vibe**: Only atoms in your vibe's starter set (check `vibes/*.md`)
- **Tier**: Prefer 0 → 1 → 2. Tier 3+ needs justification.
- **Weight**: Match your widget's weight class (W1-W4)
- **Platform**: Check `platforms` field — avoid `tofu`-marked platforms

### 4. Check the atom's own guidance
Each atom file contains:
- `prefer_over`: when this atom beats alternatives
- `prefer_under`: when alternatives beat this atom
- `anti_uses`: when NOT to use this atom
- `pairs_with`: complementary glyphs

### 5. Cross-reference
```bash
python3 scripts/check-cross-references.py
```

## Quick reference: Tier 0 pocket (memorize these)

| Need | Atom | Glyph |
|------|------|-------|
| live / on | black-circle | ● |
| offline / off | white-circle | ○ |
| partial / idle | circle-with-left-half-black | ◐ |
| success | check-mark | ✓ |
| failure | ballot-x | ✗ |
| caution | warning-sign | ⚠ |
| next / flow | rightwards-arrow | → |
| separator | middle-dot | · |
| divider | em-dash | — |
| progress filled | black-parallelogram | ▰ |
| progress empty | white-parallelogram | ▱ |
| overflow | midline-horizontal-ellipsis | ⋯ |

## Full search
Browse `atoms/` directory or `TIERS.md` for the complete catalog.
