# Sets (L2)

N-glyph series. Progressive, sequential, or categorical.

---

## Severity Dots

**Atoms:** ● ◐ ○

A 3-step severity / readiness ladder.

| Level | Glyph | Meaning |
|-------|-------|---------|
| 3 (full) | ● | live / healthy / critical |
| 2 (partial) | ◐ | idle / degraded / warning |
| 1 (empty) | ○ | offline / dead / ok |

**Grammar:** `SEVERITY(level, max=3)` → e.g. `SEVERITY(2)` = `●●○`

**Vibes:** status-operational (primary), modern-minimal, terminal-hacker

---

## Circle Fill Progression

**Atoms:** ○ ◐ ●

The same triad ordered for progress readout.

| Step | Composition |
|------|-------------|
| 0% | `○○○○○` |
| 50% | `◐○○○○` or `●●◐○○` |
| 100% | `●●●●●` |

**Rules:**
- For discrete steps, use SEVERITY(). For continuous, use BAR() or PROGRESS().
- ◐ is always "half" — do not invent quarter-fill states.

---

## Shade Ladder

**Atoms:** ░ ▒ ▓ █

4-step block density. For sparklines and heatmaps.

| Level | Glyph | Density |
|-------|-------|---------|
| 1 | ░ | 25% |
| 2 | ▒ | 50% |
| 3 | ▓ | 75% |
| 4 | █ | 100% |

**Grammar:** `SPARK(values)` maps normalized values to this ladder.

**Vibes:** terminal-hacker (primary), status-operational

---

## Parallelogram Progress Bar

**Atoms:** ▰ ▱

2-state progress cells. Clean, flat, modern.

| Step | Composition |
|------|-------------|
| 0% | `▱▱▱▱▱▱▱▱▱▱` |
| 60% | `▰▰▰▰▰▰▱▱▱▱` |
| 100% | `▰▰▰▰▰▰▰▰▰▰` |

**Grammar:** `PROGRESS(pct, n=10)` → e.g. `PROGRESS(0.6)` = `▰▰▰▰▰▰▱▱▱▱`

**Vibes:** modern-minimal (primary), status-operational

---

## Arrow Directions

**Atoms:** → ← ↑ ↓

Cardinal flow indicators.

| Direction | Glyph |
|-----------|-------|
| Right / next / forward | → |
| Left / back / previous | ← |
| Up / increase / deploy | ↑ |
| Down / decrease / rollback | ↓ |

**Rules:**
- In RTL contexts, → mirrors visually. See rtl-arabic.md §4.
- Never use diagonal arrows (↗ ↘ ↙ ↖) in terminal-hacker vibe — they break box alignment.

---

## Box Drawing Lines

**Atoms:** ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼

W1 line-drawing set for frames, tables, and trees.

| Element | Atoms |
|---------|-------|
| Horizontal | ─ |
| Vertical | │ |
| Corners | ┌ ┐ └ ┘ |
| T-junctions | ├ ┤ ┬ ┴ |
| Cross | ┼ |

**Rules:**
- Requires monospace font. Verify with target terminal font before shipping.
- All atoms in a single frame must be W1. No mixing with heavy variants.

---

## Separator Series

**Atoms:** · — … ⋯

Inline and block separators.

| Glyph | Use |
|-------|-----|
| · | Token separator in status lines |
| — | Section divider (triple for emphasis) |
| … | Truncation indicator |
| ⋯ | Midline ellipsis, overflow in lists |

**Rules:**
- · never appears at line start or end.
- — never appears more than three in a row (becomes noise).
