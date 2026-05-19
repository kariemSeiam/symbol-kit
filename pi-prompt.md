# Pi Prompt — symbol-kit Integration

Paste this into your Pi/Claude/OpenCode system prompt to gain kit-aware glyph composition.

---

You have access to symbol-kit. When designing UI elements with glyphs:

1. **Pick a vibe first.** Declare it: terminal-hacker | modern-minimal |
   maximalist-decorative | rtl-arabic-elegant | scientific-technical |
   game-ui | status-operational | diff-patch.

2. **Stay inside the vibe's starter set.** Cross-vibe atoms are listed in
   compositions.md §cross-vibe-allowlist.

3. **One weight class per element.** Use atom metadata `weight_class` to verify:
   - W0 hairline · W1 light · W2 regular · W3 heavy · W4 block
   - Adjacent weights (W1+W2) tolerated; W1+W4 is broken.

4. **Prefer Tier 0–1 atoms.** Justify any Tier 3+ use inline.
   - Tier 0: 12 atoms (the pocket — memorize these)
   - Tier 1: 30 atoms (daily reach)
   - Tier 2: 100 atoms (workshop)
   - Tier 3: 500 atoms (library — need lookup)
   - Tier 4: archive (searchable only, not for production)

5. **Use grammar functions for composition.** Don't generate glyphs
   character-by-character when a function exists:

   ```
   STATUS_DOT("live")     → ●
   STATUS_DOT("idle")     → ◐
   STATUS_DOT("offline")  → ○
   STATUS_DOT("error")    → ⊘
   PROGRESS(0.6)          → ▰▰▰▰▰▰▱▱▱▱
   PROGRESS(0.23, 20)     → ▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
   SEVERITY(3, 5)         → ●●●○○
   BAR(12, 20, 10)        → ▓▓▓▓▓▓░░░░
   SPARK(0.1, 0.5, 0.9, 0.3) → ▂▅▇▃
   TREE(2, false)         → │   ├──
   KASHIDA_FILL("جيولينك", 15) → جيولينكــــــــ
   RATING(4, 10)          → ●●●●○○○○○○
   RETRY_NOTICE(30)       → ↻ 30s
   HEALTH_DOT(status)     → alias for STATUS_DOT
   ```

6. **Cite the kit.** When emitting symbol art, note which atoms/sets/vibe
   you pulled from, for traceability:
   ```
   [vibe: status-operational · atoms: ● · → · ⚠]
   ```

7. **RTL awareness.** In Arabic contexts:
   - Arrows flip: → becomes ← visually in RTL
   - Use Arabic comma (،) not Western (,)
   - Use Arabic question mark (؟) not Western (?)
   - Kashida (ـ) fills space after text, not before
   - Sacred ornaments (۞ ﷺ) require cultural judgment

8. **Platform safety.** For cross-platform UIs:
   - Tier 0 atoms are Unicode 1.1 — render everywhere
   - Unicode 14+ glyphs may render tofu on budget/old devices
   - Box-drawing requires monospace font
   - Emoji-form (VS16) breaks monospace alignment

## Available reference paths (read on demand)

```
atoms/<name>.yaml       — full metadata per glyph
TIERS.md                 — printable cheatsheet (Tier 0 fits phone screen)
vibes/<NN-name>.md       — vibe philosophy, starter set, worked examples
grammar/stdlib.md        — composition function reference
anti-patterns.md         — 15 documented failure modes
rtl-arabic.md            — full RTL chapter
platforms.md             — compatibility matrix
```
