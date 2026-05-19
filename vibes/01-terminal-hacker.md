---
vibe: terminal-hacker
weight: W1
---

# 01 — Terminal Hacker

> The aesthetic of ncurses, htop, ranger, and the shell. Box-drawing frames, shaded blocks, bracketed tags. Every pixel is monospace and intentional.

## Signature

`┌─┐ │ └─┘ [OK] ▓░ ⠋⠙⠹`

## Philosophy

Terminal-hacker treats the UI as a TTY. Proportional fonts are the enemy. Every composition must survive in an 80×25 grid. Borders are structural, not decorative. Shade blocks carry data density. Brackets frame states.

This vibe is the default for CLI tools, server dashboards, and any context where font choice is not under your control.

## When to Choose

- Monospace-only environment
- Health boards and system monitors
- File trees and directory listings
- Any widget that must render in a terminal

## When Not to Choose

- Proportional-font contexts (iOS apps, web pages with sans-serif body)
- Decorative or "friendly" UIs (the brackets read as cold)
- RTL Arabic body text (box-drawing does not mirror correctly)

## Starter Set

### Structural (box-drawing, W1)
┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ─ │

### Density (shade ladder, W1–W2)
░ ▒ ▓ █

### Status (severity dots, W1)
● ◐ ○

### Indicators
✓ ✗ ⚠ → ← ↑ ↓

### Separators
· — … ⋯

### Brackets (Tier 2, optional)
[ ] ( )

### Full set count: ~40 atoms

## Worked Widgets

### Widget 1: Health Board

```text
┌────────────────┐
│ HEALTH BOARD   │
├────────────────┤
│ ● geolink-api  │
│ ◐ hvar-cron    │
│ ○ taxi-arab    │
└────────────────┘
```

Vibe: terminal-hacker · Weight: W1 · Atoms: ┌─┐│└┘├┤●◐○

### Widget 2: Sparkline Monitor

```text
CPU  ▓▓▓▓▓░░░ 62%
MEM  ▓▓▓▓░░░░░ 41%
NET  ░░▓▓▓▓▓▓░ 58%
```

Vibe: terminal-hacker · Weight: W1 · Atoms: ▓░·

### Widget 3: File Tree

```text
repo/
├── src/
│   ├── main.ts
│   └── lib/
│       └── util.ts
└── package.json
```

Vibe: terminal-hacker · Weight: W1 · Atoms: ├──│└──

## Do Not Mix With

- **modern-minimal** — parallelograms (▰▱) clash with box-drawing; pick one frame system
- **maximalist-decorative** — ornaments break the structural discipline
- **rtl-arabic-elegant** — box-drawing does not participate in bidirectional text
