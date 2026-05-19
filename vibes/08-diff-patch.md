---
vibe: diff-patch
weight: W1
---

# 08 — Diff Patch

> `+ - ~ ±` markers, code review, git-native, survives terminals. The aesthetic of pull requests and patches.

## Signature

`+ - ~ ± ▸ → ↩ ⊕ ⊖`

## Philosophy

Diff-patch is the most constrained vibe. Only four primary markers: added, removed, modified, and moved. Everything else is secondary. The vibe must survive in email, terminal, and GitHub markdown without degradation.

## When to Choose

- Code review summaries
- Git diff previews
- Changelogs and release notes
- Any text that represents code change

## When Not to Choose

- Non-technical users (the symbols require git literacy)
- Status dashboards (+ reads as "good," not "added")
- Decorative contexts

## Starter Set

### Core markers
+ - ~ ±

### Navigation
→ ← ↩

### Bullets
▸ ▹

### Status (universal, secondary)
● ○ ✓ ✗

### Separators
· —

### Full set count: ~25 atoms

## Worked Widgets

### Widget 1: Diff Summary

```text
+  added: 12 lines
-  removed: 3 lines
~  modified: 7 lines
```

Vibe: diff-patch · Weight: W1 · Atoms: + - ~ ·

### Widget 2: File Move

```text
→ src/old.ts  →  src/new.ts
```

Vibe: diff-patch · Weight: W1 · Atoms: → ·

### Widget 3: Review Decision

```text
✓ approve   ~ request changes   ✗ reject
```

Vibe: diff-patch · Weight: W1 · Atoms: ✓ ~ ✗ ·

## Do Not Mix With

- **terminal-hacker** — box-drawing in diffs is noise
- **game-ui** — suits and dice are absurd in code review
- **maximalist-decorative** — ornaments destroy the functional register
