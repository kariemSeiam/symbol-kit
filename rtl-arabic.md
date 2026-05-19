# RTL Arabic Chapter

Independent. Not a translation. Not a mirror. A parallel design system.

---

## 1. Numerals

### Arabic-Indic
٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ (U+0660–U+0669)

Standard across the Arab world. Use these as the default for Arabic-primary UI.

### Eastern Arabic-Indic
۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹ (U+06F0–U+06F9)

Used in Iran, Afghanistan, Pakistan, and parts of the Gulf. Do not use for Egypt, Levant, or Maghreb.

### When to use which

| Region | Preferred |
|--------|-----------|
| Egypt, Levant, Maghreb, Gulf (general) | Arabic-Indic |
| Iran, Afghanistan, Pakistan | Eastern Arabic-Indic |

**Rule:** If you do not know the user's region, default to Arabic-Indic.

---

## 2. Sacred Ornaments

۞ ﷺ ﷻ ﷽

These carry religious weight. They are not decorative.

| Glyph | Name | Use |
|-------|------|-----|
| ۞ | ARABIC END OF AYAH | Quranic verse marker |
| ﷺ | SALLALLAHOU ALAYHE WASALLAM | Honorific after the Prophet's name |
| ﷻ | JALLAJALALOUHOU | Honorific for Allah |
| ﷽ | BISMILLAH AR-RAHMAN AR-RAHIM | Opening invocation |

**Rules:**
- Never use these in casual or game contexts.
- Never combine with Western ornaments (❀ ✦).
- Always use the precomposed ligatures, not decomposed sequences.

---

## 3. Bidirectional Behavior

### Which Western glyphs flip

| Glyph | In RTL | Behavior |
|-------|--------|----------|
| → | ← visually | Mirrors |
| ← | → visually | Mirrors |
| ↑ | ↑ | No change |
| ↓ | ↓ | No change |
| ✓ | ✓ | No change |
| ● | ● | No change |
| ○ | ○ | No change |

### Mirror pairs

In LTR: «quote»
In RTL: »quote«

The guillemets swap. Do not force LTR order in RTL text.

---

## 4. Kashida

ـ (U+0640)

Used for justification. Fills space after Arabic text to reach a target width.

```text
جيولينكـــــــــ
target width: 15
```

**Grammar:** `KASHIDA_FILL(text, width)`

**Rules:**
- Kashida extends from the last letter. It does not precede text.
- Only meaningful in Arabic script. Do not use with Latin text.
- Some monospace fonts render kashida poorly. Verify with target font.

---

## 5. Punctuation

Always use Arabic punctuation in Arabic-context UI.

| Arabic | Western | Use |
|--------|---------|-----|
| ، | , | Comma |
| ؛ | ; | Semicolon |
| ؟ | ? | Question mark |

**Rule:** Never mix Western punctuation in Arabic body text. It reads as a mistake.

---

## 6. Vibe-04 Starter Set

The full curated set for RTL-Arabic-Elegant:

### Numerals
٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ۹

### Sacred (restricted)
۞ ﷺ ﷻ ﷽

### Structural
ـ · — …

### Status (universal)
● ○ ✓ ✗ ⚠

### Flow (mirrors)
→ ←

### Punctuation
، ؛ ؟

---

## 7. RTL-Specific Anti-Patterns

See `anti-patterns.md`:
- AP-05 — LTR arrows without explicit `dir`
- AP-15 — Assuming → is safe in RTL

Additional failure modes:

### Forcing LTR direction on Arabic text

**The pattern:** `<span dir="ltr">مرحبا</span>`

**Why it breaks:** The text reads right-to-left naturally. Forcing LTR produces visual garbage.

**The fix:** Let the bidi algorithm handle direction. Use `dir="auto"` or `dir="rtl"`.

### Using box-drawing in Arabic body

**The pattern:** `┌ مرحبا ┐`

**Why it breaks:** Box-drawing glyphs are LTR-neutral. They do not participate in Arabic shaping and may detach from the text flow.

**The fix:** Use spaces or kashida for structure. Do not use box-drawing in Arabic body.

---

## 8. Worked Example — Arabic HUD

```text
┌──────────────────┐
│  لوحة الصحة      │
├──────────────────┤
│ ● خدمة-جيو       │
│ ◐ مهمة-زمن       │
│ ○ سيارة-عرب      │
│ ⚠ طابور-البناء   │
└──────────────────┘
```

**Vibe:** rtl-arabic-elegant
**Weight:** W1
**Atoms:** ┌─┐│└┘├┤●◐○⚠

**Note:** The box frame is acceptable here because the container is monospace and the Arabic text is inside the frame, not shaping around it. The frame itself is LTR-neutral and does not flip.
