# Pairs (L1)

Two-glyph relationships. Every pair is bidirectional; order matters in composition.

---

## Filled / Empty Circles

**Atoms:** ● (black-circle) · ○ (white-circle)

The foundational on/off pair. Used in status indicators, toggles, binary choice.

| Context | Composition |
|---------|-------------|
| Live / offline | `● live · ○ offline` |
| All on / all off | `● ● ● ●` / `○ ○ ○ ○` |

**Rules:**
- Prefer ● over ○ when the default state is "on" (positive framing).
- Never mix with ⬤ (weight mismatch: W1 vs W3).

**Cross-vibe:** All vibes except diff-patch.

---

## Check / Cross

**Atoms:** ✓ (check-mark) · ✗ (ballot-x)

Success / failure. Terminal-native, survives monospace.

| Context | Composition |
|---------|-------------|
| Test result | `✓ pass · ✗ fail` |
| Feature flag | `✓ enabled` / `✗ disabled` |

**Rules:**
- In diff-patch vibe, use `+` / `-` instead (weight match with code context).
- Never use ✓ as a bullet — it reads as "done," not "item."

---

## Full / Light Shade

**Atoms:** ▓ (dark-shade) · ░ (light-shade)

The density pair for sparklines and block gradients.

| Context | Composition |
|---------|-------------|
| Sparkline 2-step | `▓░▓▓░▓░░` |
| Volume indicator | `▓▓▓▓▓░░░` |

**Rules:**
- Always pair with █ (full-block) for 3-step or 4-step ladders.
- In proportional fonts, shaded blocks may misalign vertically — verify with target font.

---

## Filled / Empty Parallelogram

**Atoms:** ▰ (black-parallelogram) · ▱ (white-parallelogram)

Modern-minimal progress bar cells. Flatter than shaded blocks, cleaner than circles.

| Context | Composition |
|---------|-------------|
| 10-cell progress | `▰▰▰▰▰▰▱▱▱▱` |
| Download | `▰▰▰▰▰▱▱▱▱▱ 50%` |

**Rules:**
- One weight class (W2). Safe to mix with ● ○ in the same widget.
- Prefer over shaded blocks in modern-minimal and status-operational vibes.

---

## Directional Arrows

**Atoms:** → (rightwards-arrow) · ← (leftwards-arrow) · ↑ (upwards-arrow) · ↓ (downwards-arrow)

Flow indicators. In RTL contexts, → flips to ← visually; use with `dir="rtl"` awareness.

| Context | Composition |
|---------|-------------|
| Next step | `→ deploy` |
| Back | `← back` |
| Trend up | `↑ +12%` |
| Trend down | `↓ -8%` |

**Rules:**
- In RTL Arabic body, → becomes a "back" arrow visually. Use ← for "next" if you need semantic consistency across directions.
- Never use emoji-form arrows (➡️) in code or terminal contexts.

---

## Box Corners

**Atoms:** ┌ (box-drawings-light-down-and-right) · ┐ (box-drawings-light-down-and-left) · └ (box-drawings-light-up-and-right) · ┘ (box-drawings-light-up-and-left)

The four corners of a W1 box frame.

| Context | Composition |
|---------|-------------|
| Top border | `┌──────────┐` |
| Bottom border | `└──────────┘` |

**Rules:**
- All four must be the same weight class (W1). No mixing with heavy variants.
- Requires monospace font. In proportional fonts, horizontal and vertical strokes misalign.

---

## Box T-Junctions

**Atoms:** ├ (box-drawings-light-vertical-and-right) · ┤ (box-drawings-light-vertical-and-left)

Tree branches and table row connectors.

| Context | Composition |
|---------|-------------|
| File tree mid | `├── src/` |
| File tree end | `└── main.ts` |

**Rules:**
- Use ├ for all but the last child; use └ (corner) for the last child.
- Precede with │ (vertical) for depth continuation.

---

## Dash / Separator

**Atoms:** — (em-dash) · · (middle-dot)

Section dividers vs inline separators.

| Context | Composition |
|---------|-------------|
| Section break | `———` |
| Inline separator | `● live · 47ms · 99.9%` |

**Rules:**
- Em-dash sets sections apart; middle-dot joins related tokens.
- Never use `·` at sentence boundaries — it reads as an error.
