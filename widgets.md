# Widgets (L4)

Full UI elements. Each widget declares its vibe in YAML front matter.

---

---
vibe: status-operational
weight: W1
tier_budget: { tier3: 1, tier4: 0 }
---

## Status Footer

```text
● live · 47ms · 99.9%  →  dashboard
```

**Composition:** status-line + arrow-directions
**Sets:** severity-dots, separator-series, arrow-directions
**Atoms:** ● · — →

**Use when:** Telegram footer, CLI status bar, health page header.

---

---
vibe: modern-minimal
weight: W2
tier_budget: { tier3: 0, tier4: 0 }
---

## Progress Widget

```text
▰▰▰▰▰▰▱▱▱▱  60%
```

**Composition:** progress-bar
**Sets:** parallelogram-progress-bar
**Atoms:** ▰ ▱

**Use when:** Upload/download progress, build step tracker, battery indicator.

---

---
vibe: terminal-hacker
weight: W1
tier_budget: { tier3: 0, tier4: 0 }
---

## Health Board

```text
┌────────────────┐
│ HEALTH BOARD   │
├────────────────┤
│ ● geolink-api  │
│ ◐ hvar-cron    │
│ ○ taxi-arab    │
│ ⚠ build-queue  │
└────────────────┘
```

**Composition:** HUD-frame + status-line
**Sets:** box-drawing-lines, severity-dots, separator-series
**Atoms:** ┌ ┐ └ ┘ ├ ┤ ─ │ ● ◐ ○ ⚠

**Use when:** Terminal dashboard, Telegram monospace block, devops health page.

---

---
vibe: modern-minimal
weight: W1
tier_budget: { tier3: 0, tier4: 0 }
---

## Inline Rating

```text
● ● ● ○ ○  3/5
```

**Composition:** SEVERITY(3, max=5)
**Sets:** severity-dots
**Atoms:** ● ○

**Use when:** Quick rating in chat, feature satisfaction poll.

---

---
vibe: terminal-hacker
weight: W1
tier_budget: { tier3: 0, tier4: 0 }
---

## File Tree

```text
repo/
├── src/
│   ├── index.ts
│   └── utils/
│       └── helpers.ts
└── package.json
```

**Composition:** tree-line
**Sets:** box-drawing-lines
**Atoms:** ├── │ └──

**Use when:** Directory listing, dependency tree, git branch visualization.

---

---
vibe: status-operational
weight: W2
tier_budget: { tier3: 0, tier4: 0 }
---

## Metric Card

```text
CPU    ▓▓▓▓▓░░░  62%
MEM    ▓▓▓▓░░░░░  41%
DISK   ▓▓▓▓▓▓▓░░░  78%
```

**Composition:** BAR(value, max, n=10) per row
**Sets:** shade-ladder, separator-series
**Atoms:** ▓ ░ ·

**Use when:** System monitor, resource dashboard, server health.

---

---
vibe: diff-patch
weight: W1
tier_budget: { tier3: 0, tier4: 0 }
---

## Diff Header

```text
+  added: 12 lines
-  removed: 3 lines
~  modified: 7 lines
```

**Composition:** diff markers + status-line
**Sets:** diff-patch markers
**Atoms:** + - ~ ·

**Use when:** Code review summary, git diff preview, changelog.

---

## Widget Index

| Widget | Vibe | Weight | Key Atoms |
|--------|------|--------|-----------|
| Status Footer | status-operational | W1 | ● · → |
| Progress Widget | modern-minimal | W2 | ▰ ▱ |
| Health Board | terminal-hacker | W1 | ┌─┐│└┘●◐○ |
| Inline Rating | modern-minimal | W1 | ● ○ |
| File Tree | terminal-hacker | W1 | ├──│└── |
| Metric Card | status-operational | W2 | ▓ ░ |
| Diff Header | diff-patch | W1 | + - ~ |
