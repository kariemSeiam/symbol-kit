# Compositions (L3)

Recipes combining sets into reusable patterns.

---

## Status Line

**Vibe:** status-operational
**Weight:** W1–W2
**Tier budget:** max 2 from Tier 3

```text
● live · 47ms · 99.9%
```

**Atoms:** ● · — (from sets: severity-dots, separator-series)

**Rules:**
- State dot first, then metrics separated by ·.
- End with no punctuation.
- One weight class throughout.

---

## Progress Bar

**Vibe:** modern-minimal
**Weight:** W2
**Tier budget:** 0 from Tier 3+

```text
▰▰▰▰▰▰▱▱▱▱  60%
```

**Atoms:** ▰ ▱ (from sets: parallelogram-progress-bar)

**Rules:**
- 10 cells default. Adjust with n parameter.
- Percentage aligned right, separated by 2 spaces.
- Never use shaded blocks (░▒▓) in the same widget — weight mismatch.

---

## Health Card

**Vibe:** status-operational
**Weight:** W1–W2
**Tier budget:** max 1 from Tier 3

```text
┌──────────────┐
│ ● geolink-api │
│ ◐ hvar-cron   │
│ ○ taxi-arab   │
└──────────────┘
```

**Atoms:** ┌ ─ ┐ │ └ ┘ ● ◐ ○ (from sets: box-drawing-lines, severity-dots)

**Rules:**
- Box frame from box-drawing set.
- Status dots left-aligned, 1 space padding.
- All rows same width; pad with spaces.

---

## HUD Frame

**Vibe:** terminal-hacker
**Weight:** W1
**Tier budget:** 0 from Tier 3+

```text
┌──[ STATUS ]──┐
│ ● live       │
│ ▓▓▓▓▓░░░ 50% │
└──────────────┘
```

**Atoms:** ┌ ─ ┐ │ └ ┘ [ ] ● ▓ ░ (from sets: box-drawing-lines, severity-dots, shade-ladder)

**Rules:**
- Header bracketed with [ ] inside top border.
- Mix severity dots with shade ladder only if both are W1/W2.
- Monospace required.

---

## Tree Line

**Vibe:** terminal-hacker
**Weight:** W1
**Tier budget:** 0 from Tier 3+

```text
project/
├── src/
│   ├── main.ts
│   └── lib/
│       └── util.ts
└── tests/
    └── main.test.ts
```

**Atoms:** ├── │ └── (from sets: box-drawing-lines)

**Rules:**
- ├ for non-last children, └ for last child.
- │ continues depth for all but last child at each level.
- Indent 4 spaces per depth level before tree glyphs.

---

## Separator Line

**Vibe:** any
**Weight:** any
**Tier budget:** 0 from Tier 3+

```text
──────────────
```

**Atoms:** ─ (from sets: box-drawing-lines)

**Rules:**
- Length matches widget width.
- Used between sections in HUD or card widgets.

---

## Cross-Vibe Allowlist

Atoms permitted in any vibe without lint violation:

- ● ○ ◐ (severity dots)
- → ← ↑ ↓ (arrows)
- · — … ⋯ (separators)
- ✓ ✗ (check/cross)

These are the "universal" atoms. Every vibe starter set includes them.
