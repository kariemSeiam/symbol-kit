# Anti-Patterns

Documented failures. Each entry: what people do, why it breaks, the fix, and how the linter catches it.

---

### AP-01 — Mixing weight classes in one element

**The pattern:** Using ● (W1) with ⬤ (W3) in the same status line.

**Why it breaks:** Visual rhythm collapses. The heavier glyph draws disproportionate attention, destroying the hierarchy.

**The fix:** Pick one weight class per widget. Use atom metadata `weight_class` to verify.

**Detection:** `lint-weight.py` flags any widget containing atoms from two different weight classes.

---

### AP-02 — Emoji-form glyphs inside `<code>` blocks

**The pattern:** `⚠️` (with VS16) inside a monospace code span.

**Why it breaks:** The emoji-form glyph is typically wider than monospace cells, breaking alignment. VS16 also forces colour where the context expects monochrome.

**The fix:** Use text-form `⚠` (no VS16) in code blocks. Set `default: text` in the atom.

**Detection:** `lint-weight.py` does not catch this; manual review of widget examples required.

---

### AP-03 — Unicode 14+ glyphs in pinned/persistent UI

**The pattern:** Using recently-added Unicode symbols in a Telegram pinned message.

**Why it breaks:** Budget Android devices on older OS versions render tofu (□) for Unicode 14+ codepoints.

**The fix:** Check `unicode_version` in atom metadata. Prefer ≤ 1.1 for Tier 0, ≤ 7.0 for Tier 1.

**Detection:** `validate-atom.py` surfaces `unicode_version`. Platform matrix marks untested platforms.

---

### AP-04 — ZWJ-sequence emojis in cross-platform messages

**The pattern:** Using family or profession emojis that rely on ZWJ sequences.

**Why it breaks:** WhatsApp Web and some Linux clients split ZWJ sequences into individual emoji components.

**The fix:** This kit does not catalogue emoji. Do not use emoji here.

**Detection:** Out of scope — the kit is monochrome-glyph only.

---

### AP-05 — LTR arrows in RTL Arabic body without explicit `dir`

**The pattern:** `→ التالي` in an Arabic Telegram message without `dir="rtl"`.

**Why it breaks:** The arrow flips visually, becoming a "back" arrow, while the text says "next." Cognitive dissonance.

**The fix:** Use `dir="rtl"` on the container, or use Arabic-native direction indicators, or accept the flip and design for it.

**Detection:** Manual review. `rtl-arabic.md` §4 covers this.

---

### AP-06 — Stars + dots in the same rating widget

**The pattern:** `★ ● ☆ ○` mixed in a single rating display.

**Why it breaks:** Two different symbol systems for the same concept. Users cannot parse which symbol means "filled."

**The fix:** Pick one rating system per widget. ● for modern-minimal/status, ★ for maximalist/game.

**Detection:** `lint-vibe.py` flags cross-vibe atom mixing without allowlist entry.

---

### AP-07 — Box-drawing in proportional fonts

**The pattern:** Using ┌─┐ in a Telegram message with the default sans-serif font.

**Why it breaks:** Horizontal and vertical strokes do not align. Gaps appear at corners. The frame looks broken.

**The fix:** Use `monospace` font or switch to modern-minimal vibe (no box frames).

**Detection:** Platform matrix. Terminal and code contexts are safe; general chat is not.

---

### AP-08 — Tier 4 atoms in production UI without `tier_override`

**The pattern:** Using an obscure archive glyph because "it looks cool."

**Why it breaks:** Tier 4 atoms are unmemorable, untested on many platforms, and increase cognitive load.

**The fix:** Prefer Tier 0–2. If Tier 3+ is necessary, annotate with `tier_override` and justify.

**Detection:** `lint-tier-budget.py` warns on Tier 3+ usage without override.

---

### AP-09 — Hand emojis with regional cultural sensitivity

**The pattern:** Using 👌 in a MENA-context UI.

**Why it breaks:** Cultural meaning collision. What is neutral in one region is offensive in another.

**The fix:** This kit does not catalogue emoji. Do not use emoji here.

**Detection:** Out of scope.

---

### AP-10 — Cross-vibe atom theft

**The pattern:** Using `❀` (maximalist-decorative) in a terminal-hacker HUD.

**Why it breaks:** The ornament destroys the structural discipline of the terminal vibe. It reads as a mistake.

**The fix:** Stay inside the vibe's starter set. Cross-vibe atoms are listed in `compositions.md` §cross-vibe-allowlist.

**Detection:** `lint-vibe.py` flags atoms not in the declared vibe's starter set or allowlist.

---

### AP-11 — Variation selector misuse

**The pattern:** Forcing `⚠️` (VS16, emoji-form) where text-form `⚠` is correct.

**Why it breaks:** Emoji-form glyphs override monospace alignment and introduce colour where monochrome is expected.

**The fix:** Respect atom `default: text`. Only use VS16 when the platform explicitly requires emoji-form.

**Detection:** `validate-atom.py` checks `default` field. Manual review for VS16 usage in composition.

---

### AP-12 — Combining diacritics that don't render in Telegram body

**The pattern:** Using complex combining sequences in Telegram inline text.

**Why it breaks:** Telegram's text shaping engine may drop or misplace combining marks.

**The fix:** Use precomposed characters only. Check platform matrix before shipping.

**Detection:** Platform matrix marks untested combinations.

---

### AP-13 — Right-to-left override (U+202E) anywhere

**The pattern:** Using U+202E to force RTL direction.

**Why it breaks:** Security risk. Spoofing vector. Bidi override attacks.

**The fix:** Never use U+202E. Use HTML `dir="rtl"` or Unicode bidi algorithm naturally.

**Detection:** `validate-atom.py` rejects any atom with U+202E in its codepoint.

---

### AP-14 — Full-width punctuation in CJK contexts vs ASCII

**The pattern:** Mixing full-width `，` with ASCII `,` in the same paragraph.

**Why it breaks:** Visual rhythm collision. The full-width comma occupies a full cell; the ASCII comma does not.

**The fix:** Use full-width punctuation consistently in CJK contexts. This kit does not yet catalogue CJK punctuation.

**Detection:** Out of scope for v0.1.0.

---

### AP-15 — Assuming `→` is safe in all RTL contexts

**The pattern:** Using `→` as "next" in an Arabic UI without testing.

**Why it breaks:** The arrow mirrors. It becomes a "back" arrow. The semantic label may no longer match the visual direction.

**The fix:** Test in RTL context. Consider using text labels instead of arrows, or use ← for "next" if cross-direction consistency matters.

**Detection:** `rtl-arabic.md` §4. Manual review.
