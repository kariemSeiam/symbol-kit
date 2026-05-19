# CHANGELOG

## 0.1.0-rc.1 — 2026-05-19

### Foundation
- 30 atoms with full YAML metadata (12 Tier-0 pocket + 18 Tier-1)
- Validation script: `scripts/validate-atom.py`
- CI orchestrator: `scripts/ci.sh`

### Layer 1–4 Documentation
- `pairs.md` — two-glyph relationships (8 documented pairs)
- `sets.md` — n-glyph series (7 documented sets)
- `compositions.md` — 6 recipes with cross-vibe allowlist
- `widgets.md` — 7 full UI elements with vibe declarations

### Vibes (L5)
- 8 vibe files: terminal-hacker, modern-minimal, maximalist-decorative, rtl-arabic-elegant, scientific-technical, game-ui, status-operational, diff-patch
- Each with philosophy, starter set, 3 worked widgets, and "do not mix with" warnings

### Grammar (L6)
- Formal EBNF: `grammar/symbol-kit.ebnf`
- Standard library: 10 functions documented in `grammar/stdlib.md`
- Python reference implementation: `grammar/python/symbolkit.py` (13/13 tests passing)
- TypeScript reference implementation: `grammar/typescript/symbolkit.ts`
- Cross-implementation test fixtures: `grammar/tests/fixtures.yaml`

### RTL & Anti-patterns
- `rtl-arabic.md` — full RTL chapter (numerals, kashida, ornaments, bidi, Arabic punctuation)
- `anti-patterns.md` — AP-01 through AP-15 documented

### Quality Infrastructure
- `scripts/check-cross-references.py` — cross-reference resolution
- `scripts/lint-vibe.py` — vibe coherence enforcement
- `scripts/lint-weight.py` — weight class enforcement
- `scripts/lint-tier-budget.py` — tier discipline
- `scripts/check-self-reference.py` — dogfooding enforcement
- All gates passing in CI

### Public Surface
- `README.md` — uses only Tier 0–1 atoms (self-reference check passes)
- `TIERS.md` — printable cheatsheet
- `pi-prompt.md` — ready-to-paste system prompt for agent integration
- `platforms.md` + `platforms.yaml` — compatibility matrix

### Repository
- MIT License
- `package.json` with npm scripts
- `.gitignore`
