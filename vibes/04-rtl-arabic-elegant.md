---
vibe: rtl-arabic-elegant
weight: W1–W2
---

# 04 — RTL Arabic Elegant

> Arabic-Indic numerals, kashida, sacred ornaments. A kit within the kit. Not a translation — a parallel design system.

## Signature

`٠١٢٣٤٥٦٧٨٩ ۞ ـ ، ؟ ⁘`

## Philosophy

Arabic UI has its own numerals, punctuation, and ornaments. Western glyphs flip or stay put depending on bidi rules. The kashida (ـ) is not decoration — it is structural justification.

This vibe is mandatory for any UI where Arabic is the primary language. It is not optional. It is not an afterthought.

## When to Choose

- Arabic-primary user interfaces
- MENA-region dashboards
- Any mixed LTR/RTL context where Arabic dominates

## When Not to Choose

- Pure LTR contexts (the numerals confuse Western users)
- Terminal-only environments (kashida may not render correctly in all mono fonts)

## Starter Set

### Arabic-Indic numerals
٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩

### Eastern Arabic-Indic numerals (Persian/Gulf)
۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹

### Sacred ornaments
۞ ﷺ ﷻ ﷽

### Kashida
ـ

### Arabic punctuation
، ؛ ؟

### Status (universal, safe in RTL)
● ○ ✓ ✗ ⚠

### Separators
· — …

### Full set count: ~35 atoms

## Worked Widgets

### Widget 1: Arabic Status Line

```text
● نشط · ٤٧ مللي · ٩٩٫٩٪
```

Vibe: rtl-arabic-elegant · Weight: W1 · Atoms: ●·

### Widget 2: Kashida Justification

```text
جيولينكـــــــــ
```

Vibe: rtl-arabic-elegant · Weight: W1 · Atoms: ـ

### Widget 3: Arabic Health Board

```text
● خدمة-جيو   ◐ مهمة-زمن   ○ سيارة-عرب
```

Vibe: rtl-arabic-elegant · Weight: W1 · Atoms: ●◐○

## Do Not Mix With

- **terminal-hacker** — box-drawing does not participate in RTL shaping
- **maximalist-decorative** — Western ornaments clash with Arabic calligraphic tradition
- **game-ui** — chess pieces and suits have no cultural resonance in MENA contexts

## RTL-Specific Rules

1. Arrows flip: → becomes ← visually in RTL context.
2. Use Arabic comma (،) not Western comma (,).
3. Use Arabic question mark (؟) not Western (?).
4. Kashida fills space after text, not before.
5. Sacred ornaments (۞ ﷺ) require cultural judgment — do not use casually.
