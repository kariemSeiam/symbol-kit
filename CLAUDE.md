# CLAUDE.md

> Source of truth for `symbol-kit`. Read fully before writing any other file in this repo. When this file conflicts with intuition, this file wins.

---

## §0 — Identity

`symbol-kit` is a **glyph design system**, not a glyph catalog. The world has hundreds of Unicode reference sites — Compart, xahlee, Unicode Table, "Cool Symbols," emojipedia. They are catalogs: lists organized by Unicode block, opaque to semantic lookup, untested across platforms, indifferent to RTL languages, and incapable of teaching composition.

This kit answers a different question:

> Given a UI to build, which glyphs should I use, in what combinations, in what aesthetic register, that will render correctly across the platforms I actually ship to — and how do I know it works?

The kit must outperform every existing reference on six axes:

1. **Semantic lookup over glyph lookup.** Find by what it *does*, not what block it's in.
2. **Coherence via vibe profiles.** Eight named aesthetics with curated sets. The kit teaches discipline.
3. **Platform truth, not platform claims.** Every render claim is testable; untested claims marked.
4. **Composition as a formal language.** A DSL any agent can consume to generate UIs from data.
5. **RTL/Arabic as a first-class chapter.** Not a footnote — Arabic-Indic numerals, kashida, mirror pairs, MENA-appropriate ornaments.
6. **Self-referential dogfooding.** The kit's own docs use only the kit's own glyphs. If `README.md` needs a glyph not in `atoms/`, the build fails.

If you, Claude Code, find yourself building a catalog, **stop**. Return to this section.

---

## §1 — Architectural axioms

Non-negotiable. Violating any of these is grounds for rejecting the work.

- **A — Atoms have full metadata.** No glyph enters `atoms/` without complete metadata per §3. Partial entries corrupt the system's promises.
- **B — Bottom-up build order.** Pairs precede sets, sets precede compositions, compositions precede widgets, widgets precede vibes. Never invert.
- **C — Vibe exclusivity within an element.** A single UI element (footer, card, HUD line) sources all glyphs from one vibe. The `lint-vibe` script enforces.
- **D — Single weight class per element.** Mixing W1 (`─ ○ ●`) with W4 (`█ ⬛`) is visually broken. The `lint-weight` script enforces.
- **E — Text-form default.** When a glyph has text and emoji variants (`⚠` vs `⚠️`), default to text-form. Variation selectors are documented per glyph in §3.
- **F — Falsifiability over assertion.** Every render-claim is either marked verified by a test ID or marked `unverified`. No bare claims.
- **G — RTL is not LTR-mirrored.** Arabic has its own glyphs, numerals, ornaments, bidi rules. The RTL chapter is independent — not a translation of the LTR one.
- **H — Tier discipline.** Every atom is tier-tagged (0–4). Tier 0 = 12 glyphs you must memorize; Tier 4 = archive. UIs should preferentially use lower tiers. Linter warns when a widget uses Tier 3+ atoms without justification.

---

## §2 — The seven-layer model

Every concept in this kit fits exactly one layer. If you can't place a concept, the concept is wrong.

| Layer | Name | Contains | File(s) |
|-------|------|----------|---------|
| L0 | Atoms | individual glyphs with metadata | `atoms/*.yaml` |
| L1 | Pairs | two-glyph relationships (filled/empty, on/off) | `pairs.md` |
| L2 | Sets | n-glyph series (weight axes, severity ladders, spinner frames) | `sets.md` |
| L3 | Compositions | recipes combining sets (progress bar, status line) | `compositions.md` |
| L4 | Widgets | full UI elements (HUD, footer, badge, health card) | `widgets.md` |
| L5 | Vibes | aesthetic profiles constraining which sets compose | `vibes/*.md` |
| L6 | Grammars | formal DSL for generating UIs from data | `grammar.md` + `grammar/*` |

**Read the layers up when designing** ("I'm building a footer → which widget → which compositions → which sets → which atoms?"). **Read down when looking up** ("I have this glyph → what set → what pairs → what vibe?").

---

## §3 — Per-glyph metadata schema

Every atom in `atoms/` is a YAML file. One glyph per file. Filename = lowercase official Unicode name with hyphens (`black-circle.yaml`).

**Full schema. No optional fields. Missing fields fail validation.**

```yaml
# atoms/black-circle.yaml
glyph: ●
name: BLACK CIRCLE
codepoint: U+25CF
unicode_block: Geometric Shapes
unicode_version: "1.1"

aliases:
  - filled dot
  - status dot
  - solid bullet
  - the live one

form:
  default: text          # text | emoji
  variation_selectors:   # which VS produce which form
    none: text
  emoji_form_exists: false

weight_class: W2         # W0 hairline · W1 light · W2 regular · W3 heavy · W4 block
width_class: variable    # narrow | variable | 2ch | emoji-wide

tier: 0                  # 0 pocket · 1 daily · 2 workshop · 3 library · 4 archive

semantic:
  primary: status:on
  also:
    - severity:full
    - marker:primary
    - rating:filled
  not:
    - decoration

pairs_with:              # L1 relationships
  complement: ○ (white-circle)        # filled/empty pair
  next_in_set:                        # part of progressive sets
    - ◐ (circle-with-left-half-black)
  family:                             # same weight, same style
    - ◯ ◑ ◒ ◓ ⊙

visual_neighbors:        # things it can be confused with
  - ⬤ heavier
  - ⚫ medium-black-circle (emoji)
  - ◉ fisheye
  - ⬩ small black diamond (different shape)

prefer_over:             # rule-based selection guidance
  - "⬤ when surrounded by W1/W2 glyphs (weight match)"
  - "• when used as standalone status indicator (• is bullet semantics)"
prefer_under:
  - "⬤ in standalone HUD where extra visual weight serves emphasis"

anti_uses:
  - "Inside <code> blocks adjacent to emoji-form glyphs — visual collision"
  - "As bullet in body prose (use • instead)"

platforms:               # falsifiable; every entry has a test_id or `unverified`
  telegram_ios:      { renders: yes, test_id: PLAT-001 }
  telegram_android:  { renders: yes, test_id: PLAT-002 }
  telegram_desktop:  { renders: yes, test_id: PLAT-003 }
  telegram_web:      { renders: yes, test_id: PLAT-004 }
  imessage:          { renders: yes, test_id: PLAT-005 }
  whatsapp:          { renders: yes, test_id: PLAT-006 }
  github_markdown:   { renders: yes, test_id: PLAT-007 }
  vscode_default:    { renders: yes, test_id: PLAT-008 }
  terminal_monaco:   { renders: yes, test_id: PLAT-009 }
  terminal_cascadia: { renders: yes, test_id: PLAT-010 }
  print_pdf:         { renders: yes, test_id: PLAT-011 }

rtl_behavior:
  mirrors: false          # does it flip in RTL? (arrows do, dots don't)
  arabic_equivalent: null # if there's an Arabic-native alternative, name it
  safe_in_rtl: true

copy_paste_safe: yes      # survives cat / git / json / shell pipe without mangling
monochrome_guaranteed: yes

vibes:                    # which vibe profiles include this atom in their starter set
  - terminal-hacker
  - modern-minimal
  - status-operational

examples:                 # 2–4 real-world usage demos
  - context: "Telegram footer status dot"
    snippet: "● live · 47ms · 99.9%"
  - context: "Health board left column"
    snippet: "● geolink-api   ○ hvar-cron   ◐ taxi-arab"

cross_references:
  pairs: ["pairs.md#filled-empty-circles"]
  sets:  ["sets.md#severity-dots"]
  widgets: ["widgets.md#status-line", "widgets.md#health-card"]

added_in: 0.1.0
last_verified: 2026-05-19
```

This schema is the **canonical** atom format. Validation script `scripts/validate-atom.py` checks every file in `atoms/` against it on every commit.

---

## §4 — The eight vibe profiles

Each vibe is a curated starter set of 30–50 atoms that compose cleanly together. Each vibe ships:

- `vibes/NN-name.md` — philosophy, signature glyphs, when to choose, when not to
- starter set inline (atom list)
- 3 worked widget examples in that vibe
- explicit "do not mix with" warning

The eight:

1. **`01-terminal-hacker.md`** — Box-drawing, bracketed tags, shaded blocks, sparklines. ncurses, htop, ranger. Signature: `┌─┐ │ └─┘ [OK] ▓░ ⠋⠙⠹`
2. **`02-modern-minimal.md`** — Filled dots, pills, middle-dot separators, no borders. Linear, Stripe, Vercel. Signature: `● ○ ▰▱ · → ↗`
3. **`03-maximalist-decorative.md`** — Rounded boxes, ornaments, stars, flourishes. Manuscript, illuminated. Signature: `╭╮╰╯ ❖ ❀ ✦ ★ ⁂`
4. **`04-rtl-arabic-elegant.md`** — Arabic-Indic numerals, kashida, ۞ ﷺ, mirror-aware. MENA-native. Signature: `٠١٢٣٤٥٦٧٨٩ ۞ ـ ، ؟ ⁘`
5. **`05-scientific-technical.md`** — Math symbols, Greek, dimensional notation, set theory. arXiv, Wolfram. Signature: `∂ ∇ ∑ ∫ ≈ ≡ α β γ ⟨⟩`
6. **`06-game-ui.md`** — Chess pieces, suits, hearts, weather, retro game feel. Signature: `♠♣♥♦ ♔♕ ★☆ ⚔ ⚒ ⚓`
7. **`07-status-operational.md`** — Green/red signal carried by fill state, severity ladders, SRE. Datadog, PagerDuty. Signature: `● ◐ ○ ⊘ ▰▱ ⚠ ⚡ ↻`
8. **`08-diff-patch.md`** — `+ - ~ ±` markers, code review, git-native, survives terminals. Signature: `+ - ~ ± ▸ → ↩ ⊕ ⊖`

**Vibe rules:**
- A widget declares its vibe at the top in a YAML front matter.
- The `lint-vibe` script enforces that every glyph in the widget exists in that vibe's starter set or is on the cross-vibe allowlist (defined in `compositions.md`).
- Some atoms are cross-vibe (`●`, `─`, `·`, `→`) and belong to multiple vibes. These are explicitly marked in each atom's `vibes:` field.

---

## §5 — Tier system

Memorability is a deliberate axis. The kit pushes you to use lower tiers; archive exists for completeness but should not appear in production UI.

| Tier | Size | Role | Mental model |
|------|------|------|--------------|
| 0 | 12 | Pocket | Memorize. Cover 80% of daily use. |
| 1 | 30 | Daily | Reach without thinking. |
| 2 | 100 | Workshop | Specialized, recallable. |
| 3 | 500 | Library | Need lookup. |
| 4 | unlimited | Archive | Searchable only. Not for production. |

The lint pass `lint-tier-budget` warns when a single widget pulls more than 2 atoms from Tier 3 or any atom from Tier 4 without an explicit `tier_override` annotation.

`TIERS.md` is the entry-point document — a printable cheatsheet. Tier 0 fits on a phone screen. Tier 1 fits on a postcard. Tier 2 fits on a sheet.

---

## §6 — The composition grammar (DSL)

Real, parseable, with reference implementations in Python and TypeScript so pi (the coding agent) and any other agent can consume it directly.

**EBNF (see `grammar/symbol-kit.ebnf`):**

```ebnf
expression  = literal | atom | invocation | repetition | sequence ;
literal     = '"' { char } '"' ;
atom        = '@' identifier ;                    (* @black-circle *)
invocation  = identifier '(' [ args ] ')' ;       (* PROGRESS(0.6, 10) *)
repetition  = expression '×' integer ;            (* @black-circle × 5 *)
sequence    = expression { '+' expression } ;
args        = expression { ',' expression } ;
identifier  = letter { letter | digit | '-' | '_' } ;
```

**Core stdlib functions (defined in `grammar/stdlib.md`):**

```
STATUS_DOT(state)            -> { live: ●, idle: ◐, offline: ○, error: ⊘ }[state]
PROGRESS(pct, n=10)          -> @filled-pill × round(pct·n) + @empty-pill × (n-round(pct·n))
SEVERITY(level, max=4)       -> ● × level + ○ × (max-level)
SPARK(values)                -> map(values, v -> @spark[round(v·7)])  using @spark = [▁▂▃▄▅▆▇█]
TREE(depth, last)            -> (@tree-line + " ") × (depth-1) + (last ? @tree-last-branch : @tree-mid-branch)
KASHIDA_FILL(text, width)    -> text + @kashida × (width - len(text))   (* RTL justification *)
RATING(stars, max=5)         -> @filled-star × stars + @empty-star × (max-stars)
BAR(value, max, n=20)        -> @full-block × round(value/max·n) + @light-shade × (n - round(value/max·n))
HEALTH_DOT(status)           -> STATUS_DOT(status)
RETRY_NOTICE(seconds)        -> "↻ " + seconds + "s"
```

**Reference implementations:**

- `grammar/python/symbolkit.py` — pure Python, no deps, ~200 LOC. Function: `render(expression: str, env: dict) -> str`
- `grammar/typescript/symbolkit.ts` — pure TS, no deps, same interface
- Both implementations are tested against the same fixture set in `grammar/tests/fixtures.yaml`

**Pi integration (see §16):** Pi loads the stdlib in its system prompt and calls `render("PROGRESS(0.6, 10)")` instead of generating glyphs character-by-character. This is how the kit becomes infrastructure.

---

## §7 — Anti-patterns

Documented in `anti-patterns.md`. Each entry follows the format:

```markdown
### AP-NN — Short Name

**The pattern:** [what people do]

**Why it breaks:** [concrete failure mode]

**The fix:** [what to do instead]

**Detection:** [how the linter catches it]
```

Minimum coverage:

- **AP-01** Mixing weight classes in one element
- **AP-02** Emoji-form glyphs inside `<code>` blocks (VS16 vs monospace)
- **AP-03** Unicode 14+ glyphs in pinned/persistent UI (older Android renders tofu)
- **AP-04** ZWJ-sequence emojis in cross-platform messages
- **AP-05** LTR arrows in RTL Arabic body without explicit `dir`
- **AP-06** Stars + dots in the same rating widget
- **AP-07** Box-drawing in proportional fonts
- **AP-08** Tier 4 atoms in production UI without `tier_override`
- **AP-09** Hand emojis with regional cultural sensitivity (👌 in MENA contexts)
- **AP-10** Cross-vibe atom theft (using `❀` in Terminal-Hacker)
- **AP-11** Variation selector misuse (forcing emoji where text-form is correct)
- **AP-12** Combining diacritics that don't render in Telegram body
- **AP-13** Right-to-left override (U+202E) anywhere — security risk
- **AP-14** Full-width punctuation in CJK contexts vs ASCII
- **AP-15** Assuming `→` is safe in all RTL contexts (it flips)

---

## §8 — Platform compatibility matrix

`platforms.md` plus machine-readable `platforms.yaml`. Schema:

```yaml
test_id: PLAT-001
glyph: ●
platform: telegram_ios
platform_version: ">= 10.0"
renders: yes              # yes | tofu | fallback | unverified
notes: ""                 # optional caveats
last_tested: 2026-05-19
tester: claude-build-001
evidence: screenshots/PLAT-001.png   # optional
```

**Tested platforms (mandatory coverage):**

- Telegram: iOS, Android, Desktop (Win/Mac/Linux), Web-K, Web-A
- iMessage
- WhatsApp (iOS, Android, Web)
- Discord
- Slack
- GitHub Markdown (web, API render)
- VS Code default font
- Terminal: Monaco, Cascadia Code, JetBrains Mono, SF Mono, default Linux mono
- Browsers: Chrome, Safari, Firefox (Win, Mac, Linux, iOS, Android)
- Print/PDF (Chrome headless rendering)

**Methodology** (see `platforms/METHODOLOGY.md`):

For each atom × platform pair, render the glyph in a canonical context (footer of a Telegram bubble, body of a markdown doc, etc.). Mark `yes` only if visually correct. Mark `tofu` if rendered as undefined-glyph box. Mark `fallback` if a substitute glyph appeared. Mark `unverified` if untested.

**Automated test:** `scripts/render-harness.py` generates a 100-glyph-per-page HTML file rendered by Playwright across browser engines, screenshots compared to reference. Run via `npm run test:render`.

---

## §9 — RTL/Arabic chapter

`rtl-arabic.md` is independent — not a translation, not a mirror. It addresses what nobody else does:

**Required sections:**

1. **Numerals.** Arabic-Indic `٠١٢٣٤٥٦٧٨٩` (U+0660–0669) vs Eastern Arabic-Indic `۰۱۲۳۴۵۶۷۸۹` (U+06F0–06F9). When to use which. Regional preferences (Egypt vs Gulf vs Persian).
2. **Sacred ornaments.** `۞ ﷺ ﷻ ﷽` — what they mean, when appropriate, when not. Cultural register.
3. **Bidirectional behavior.** Which Western glyphs flip in RTL context (arrows: `→ ↩ ↗`) and which do not (status dots, stars, warnings). Concrete examples with `dir="rtl"` HTML.
4. **Mirror pairs.** `« »` vs `» «` — which is correct in Arabic body.
5. **Kashida.** `ـ` (U+0640) for justification. How to use it in glyph art for filling Arabic-context space.
6. **Punctuation.** Arabic comma `،`, Arabic semicolon `؛`, Arabic question mark `؟`. Always use these in Arabic-context UI, never the Western equivalents.
7. **Vibe-04 starter set.** The full curated set for RTL-Arabic-Elegant vibe with examples.
8. **Anti-patterns specific to RTL.** AP-05 expanded, plus RTL-specific failure modes.
9. **Worked example.** A complete Arabic-context HUD widget composed entirely from this chapter's atoms.

This chapter is reviewed by a native Arabic-context judgment (the kit author). Pi must not modify this chapter without explicit human approval.

---

## §10 — Directory & file specification

The complete repo structure. Build to match exactly.

```
symbol-kit/
├── CLAUDE.md                          # this file
├── README.md                          # public-facing intro, uses only Tier 0–1 atoms
├── TIERS.md                           # printable cheatsheet, Tier 0/1/2 tables
├── CHANGELOG.md                       # semver history
├── LICENSE                            # MIT
├── package.json                       # for npm scripts only; no runtime deps
│
├── atoms/                             # L0 — one yaml file per glyph
│   ├── black-circle.yaml
│   ├── white-circle.yaml
│   ├── ...                            # ~300 in main set, ~500 in archive/
│   └── archive/
│       └── ...
│
├── pairs.md                           # L1 — relationships
├── sets.md                            # L2 — series (weight axis, severity, sparklines)
├── compositions.md                    # L3 — recipes
├── widgets.md                         # L4 — full UI elements
│
├── vibes/                             # L5
│   ├── 01-terminal-hacker.md
│   ├── 02-modern-minimal.md
│   ├── 03-maximalist-decorative.md
│   ├── 04-rtl-arabic-elegant.md
│   ├── 05-scientific-technical.md
│   ├── 06-game-ui.md
│   ├── 07-status-operational.md
│   └── 08-diff-patch.md
│
├── grammar.md                         # L6 — DSL overview
├── grammar/
│   ├── symbol-kit.ebnf                # formal grammar
│   ├── stdlib.md                      # documented stdlib functions
│   ├── python/
│   │   ├── symbolkit.py
│   │   └── test_symbolkit.py
│   ├── typescript/
│   │   ├── symbolkit.ts
│   │   └── symbolkit.test.ts
│   └── tests/
│       └── fixtures.yaml
│
├── platforms.md                       # human-readable matrix
├── platforms.yaml                     # machine-readable matrix
├── platforms/
│   └── METHODOLOGY.md
│
├── anti-patterns.md                   # AP-01..AP-15
├── rtl-arabic.md                      # the chapter
├── pi-prompt.md                       # ready-to-paste system prompt for pi/Claude
│
├── scripts/                           # validation & build
│   ├── validate-atom.py               # checks atoms against schema
│   ├── lint-vibe.py                   # detects vibe-mixing
│   ├── lint-weight.py                 # detects weight-class mixing
│   ├── lint-tier-budget.py            # tier discipline
│   ├── check-self-reference.py        # README uses only catalogued atoms
│   ├── check-cross-references.py      # all cross-refs resolve
│   ├── render-harness.py              # Playwright render tests
│   ├── generate-tier-cheatsheet.py    # auto-generates TIERS.md
│   └── ci.sh                          # runs everything; CI entry point
│
├── render-proofs/                     # HTML samples for visual verification
│   ├── tier-0-pocket.html
│   ├── tier-1-daily.html
│   ├── all-vibes-side-by-side.html
│   ├── rtl-arabic-showcase.html
│   └── widget-gallery.html
│
└── .claude/
    └── skills/                        # Claude Code skills the kit ships
        ├── lint-vibe/SKILL.md
        ├── compose-widget/SKILL.md
        ├── select-atom/SKILL.md
        └── render-preview/SKILL.md
```

---

## §11 — Build plan (dependency-ordered)

Execute in this exact order. Each phase has acceptance criteria; do not advance until they pass.

### Phase 1 — Foundation (no parallelism)
1. Create directory skeleton matching §10.
2. Write `scripts/validate-atom.py` with full schema validation.
3. Write `scripts/ci.sh` that orchestrates all checks.
4. Write 12 Tier-0 atoms in `atoms/` (the pocket — see §20).
5. Run `validate-atom.py` against all 12. Must pass.

### Phase 2 — Layer 0 expansion (parallelizable)
6. Write Tier-1 atoms (30 total — including the 12 from phase 1).
7. Write Tier-2 atoms (100 total).
8. Write Tier-3 atoms (~500 total).
9. **Sub-agent strategy:** dispatch one sub-agent per Unicode block (Geometric Shapes, Arrows, Box Drawing, Block Elements, Miscellaneous Symbols, etc.). Each sub-agent writes 30–80 atoms in its block, all conforming to §3 schema. Main thread merges and validates.
10. Run `validate-atom.py` against every atom. Must pass.

### Phase 3 — Layer 1–4 docs (sequential)
11. Write `pairs.md` referencing only atoms that exist.
12. Write `sets.md`.
13. Write `compositions.md`.
14. Write `widgets.md` — every widget declares its vibe in front matter.
15. Run `check-cross-references.py`. Must pass.

### Phase 4 — Vibes (parallelizable, 8-way)
16. Dispatch one sub-agent per vibe to write `vibes/NN-name.md`.
17. Each sub-agent must use only atoms from `atoms/` and must produce 3 worked widget examples.
18. Main thread runs `lint-vibe.py` against each vibe file. Must pass.

### Phase 5 — Grammar
19. Write `grammar.md`, `grammar/symbol-kit.ebnf`, `grammar/stdlib.md`.
20. Implement `grammar/python/symbolkit.py`.
21. Implement `grammar/typescript/symbolkit.ts`.
22. Both implementations must pass `grammar/tests/fixtures.yaml`.

### Phase 6 — Platform truth
23. Write `platforms.md` and `platforms.yaml`. Initial population from atom files.
24. Write `scripts/render-harness.py` using Playwright (instructions in `platforms/METHODOLOGY.md`).
25. Run harness; populate `platforms.yaml` with results. Anything untested is marked `unverified`.

### Phase 7 — RTL & specialty
26. Write `rtl-arabic.md` per §9. This file is the highest quality bar in the repo.
27. Write `anti-patterns.md` with all AP-01..AP-15.
28. Write `pi-prompt.md` — a system prompt that loads the kit into any agent.

### Phase 8 — Public surface & self-reference
29. Write `README.md`. May use only Tier 0–1 atoms. `check-self-reference.py` validates.
30. Auto-generate `TIERS.md` via `scripts/generate-tier-cheatsheet.py`.
31. Build `render-proofs/*.html` files.
32. Write `.claude/skills/` skills.
33. Write `CHANGELOG.md` entry for v0.1.0.

### Phase 9 — Final gate
34. Run `scripts/ci.sh`. All checks must pass: atom validation, cross-refs, vibe lint, weight lint, tier budget, self-reference, grammar tests.
35. Tag `v0.1.0`.

---

## §12 — Parallel execution strategy

Phases 2.9 (atoms by Unicode block) and 4.16 (vibes) are the only points where sub-agent delegation is appropriate.

**Sub-agent contract:**

When you (Claude Code) dispatch a sub-agent to write a vibe file or a block of atoms, give it:

1. Pointer to this `CLAUDE.md` as required reading.
2. Its specific scope (e.g., "Write all atoms for Unicode block 'Arrows' (U+2190–U+21FF). Tier each one 0–4 using §5 criteria.").
3. The atom YAML schema (§3) as a checklist.
4. A return spec: list of files written + a summary of decisions.

**Sub-agent boundaries:**

- A sub-agent must not edit `CLAUDE.md`.
- A sub-agent must not modify files outside its scope.
- A sub-agent must run `validate-atom.py` on its own outputs before returning.
- The main thread does final merge and global validation.

**Do not parallelize:**

- Schema design (§3) — single source of truth.
- `pairs.md`, `sets.md`, `compositions.md` — they cross-reference; parallel work creates merge conflicts.
- `rtl-arabic.md` — requires unified voice and cultural calibration.
- `grammar/*` — reference implementations must match each other.

---

## §13 — Validation & quality gates

Every commit runs `scripts/ci.sh`, which runs in order:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "▸ atom schema validation"
python3 scripts/validate-atom.py atoms/

echo "▸ cross-reference resolution"
python3 scripts/check-cross-references.py

echo "▸ vibe coherence"
python3 scripts/lint-vibe.py widgets.md vibes/

echo "▸ weight-class coherence"
python3 scripts/lint-weight.py widgets.md

echo "▸ tier budget"
python3 scripts/lint-tier-budget.py widgets.md

echo "▸ self-reference (README uses only catalogued atoms)"
python3 scripts/check-self-reference.py README.md

echo "▸ grammar test suite"
python3 grammar/python/test_symbolkit.py
cd grammar/typescript && npm test && cd ../..

echo "▸ render harness (subset, smoke)"
python3 scripts/render-harness.py --smoke

echo "✓ all checks passed"
```

CI fails on any non-zero exit. No exceptions, no `--skip` flags.

---

## §14 — Render proof harness

`scripts/render-harness.py` produces falsifiability for the platform claims.

**How it works:**

1. Reads `atoms/*.yaml` and assembles an HTML page rendering each atom in 5 canonical contexts: standalone, in a body paragraph, inside `<code>`, inside `<pre>`, and inside an RTL `<div dir="rtl">`.
2. Uses Playwright to load the page in Chromium, Firefox, WebKit, and a mobile Safari emulation, with multiple font stacks.
3. Screenshots each cell.
4. Compares against reference fingerprints stored in `render-proofs/fingerprints.yaml`.
5. Anything that doesn't match the fingerprint is flagged as either a tofu (undefined glyph), a fallback substitution, or an unintended change.
6. Generates a delta report.

This is not perfect — it can't test actual Telegram clients programmatically. For those, we ship a manual checklist in `platforms/METHODOLOGY.md` and require that each Tier 0 and Tier 1 atom has at least one manually verified Telegram render screenshot in `platforms/manual-verification/`.

**Required smoke test:** All Tier-0 atoms must pass full harness before v0.1.0 ships.

---

## §15 — Self-referential test

`scripts/check-self-reference.py` enforces dogfooding:

1. Parses `README.md` glyph-by-glyph.
2. For each non-ASCII glyph, checks: is there an atom file documenting it?
3. For each atom referenced, checks: is its tier ≤ 1?
4. Fails the build if any atom is missing or above Tier 1.

The README's pretty status indicators, progress bars, headers — all of it — must come from atoms the kit catalogues. The kit cannot recommend what it does not practice.

Applies to `README.md` only. Other files may use higher tiers (with budget enforcement per §5).

---

## §16 — Pi integration handshake

The kit produces `pi-prompt.md`: a system prompt block that any agent (pi, Claude, OpenCode, Cursor) can paste in to gain kit-aware behavior.

**Required content of `pi-prompt.md`:**

```markdown
You have access to symbol-kit. When designing UI elements with glyphs:

1. **Pick a vibe first.** Declare it: terminal-hacker | modern-minimal |
   maximalist-decorative | rtl-arabic-elegant | scientific-technical |
   game-ui | status-operational | diff-patch.
2. **Stay inside the vibe's starter set.** Cross-vibe atoms are listed in
   compositions.md §cross-vibe-allowlist.
3. **One weight class per element.** Use atom metadata `weight_class` to verify.
4. **Prefer Tier 0–1 atoms.** Justify any Tier 3+ use inline.
5. **Use grammar functions for composition.** Don't generate glyphs
   character-by-character when a function exists. Examples:
   - `PROGRESS(0.6)` → ▰▰▰▰▰▰▱▱▱▱
   - `STATUS_DOT(live)` → ●
   - `SEVERITY(3)` → ●●●○
   - `KASHIDA_FILL("جيولينك", 15)` → جيولينكـــــــــ
6. **Cite the kit.** When emitting symbol art, comment with which atoms/sets
   you pulled from, for traceability.

Available reference paths (read on demand):
- atoms/<name>.yaml — full metadata per glyph
- TIERS.md — quick cheatsheet
- vibes/<NN-name>.md — vibe starter sets and worked examples
- grammar/stdlib.md — composition functions
- anti-patterns.md — what not to do
- rtl-arabic.md — RTL/Arabic specific
```

Pigo will load this into pi-telegram's bot config so every agent session is kit-aware by default.

---

## §17 — Versioning & extension protocol

Semver: `MAJOR.MINOR.PATCH`.

- **PATCH** — fixing wrong metadata, broken cross-refs, render-harness updates.
- **MINOR** — adding atoms, adding widgets, adding compositions, refining vibe sets.
- **MAJOR** — changing the schema (§3), removing atoms from a vibe set, changing the layer model.

**Adding an atom (non-breaking):**

1. Create `atoms/<name>.yaml` per §3.
2. Decide tier per §5 criteria.
3. Decide vibe memberships.
4. Add cross-references to relevant `pairs.md` / `sets.md` entries.
5. Add platform test entries; mark `unverified` for untested platforms.
6. Run CI. Open PR. Bump MINOR.

**Removing an atom (breaking):**

1. Mark `deprecated: true` and `deprecated_in: X.Y.Z` in the YAML for one MINOR cycle.
2. Update all downstream references to a replacement atom.
3. Remove in next MAJOR.

**Vibe set changes:**

- Adding an atom to a vibe's starter set is MINOR.
- Removing an atom from a vibe's starter set is MAJOR (breaks downstream UIs).

---

## §18 — Anti-patterns for Claude Code itself

Failure modes you, Claude Code, are statistically likely to fall into when building this kit. Recognize the warning signs.

**ACAP-01 — Drift into catalog mode.** You start writing atom files and forget the system. Symptom: atom files have no `prefer_over` / `anti_uses` / `pairs_with` content. Fix: pause, re-read §0 and §3, fill the relational metadata.

**ACAP-02 — Vibe greedy.** You add atoms to multiple vibes' starter sets because they "kind of fit." Vibe sets become 80+ atoms each and lose discipline. Fix: each vibe starter set caps at 50. Be precise about what defines the vibe.

**ACAP-03 — Falsifiability slop.** You mark all platforms as `renders: yes` without running the harness. Fix: never claim a render is verified without a `test_id`. Default to `unverified`.

**ACAP-04 — Grammar bloat.** You define 80 stdlib functions because each one "might be useful." Fix: cap stdlib at ~15 functions. New functions enter via a versioned proposal.

**ACAP-05 — README polish trap.** You spend hours making README.md pretty. Fix: README is auto-checked by §15 self-reference. Get the rest of the kit right; README falls into place once the atoms exist.

**ACAP-06 — RTL afterthought.** You write the LTR kit, then translate it to RTL. Wrong. The RTL chapter is independent (Axiom G). Write it from Arabic-context first principles.

**ACAP-07 — Sub-agent fan-out without merge discipline.** You dispatch 8 sub-agents for vibes and they each cross-reference different atoms inconsistently. Fix: phase order in §11. Atoms first, vibes second.

**ACAP-08 — Test-skip cascade.** A test fails, you add `--skip` to ci.sh "temporarily." Then you forget. Fix: never add skip flags to CI. Fix the failing thing or drop the work.

**ACAP-09 — Emoji creep.** You start cataloguing emojis because they're "symbols too." Fix: §0 — monochrome glyphs only. Emojis are a different system.

**ACAP-10 — Tier inflation.** Tier 0 grows from 12 to 30 because "everything's important." Fix: Tier 0 is 12. Anything more goes to Tier 1.

---

## §19 — Definition of done (v0.1.0)

The kit ships v0.1.0 when:

- [ ] `scripts/ci.sh` passes with zero warnings
- [ ] 300+ atoms in main `atoms/`, every one schema-valid
- [ ] All 8 vibe files written, each with 3 worked widgets
- [ ] `pairs.md`, `sets.md`, `compositions.md`, `widgets.md` complete with no broken cross-refs
- [ ] `grammar/python/symbolkit.py` and `grammar/typescript/symbolkit.ts` pass fixture tests
- [ ] `rtl-arabic.md` written and reviewed by Arabic-context judgment
- [ ] `anti-patterns.md` has all AP-01..AP-15 documented
- [ ] `pi-prompt.md` written and tested by loading into a pi session
- [ ] `README.md` written using only Tier 0–1 atoms; self-reference check passes
- [ ] `TIERS.md` auto-generated
- [ ] Render harness has been run; results populated in `platforms.yaml`; Tier 0 atoms manually verified on Telegram iOS + Android
- [ ] Five `.claude/skills/` skills written
- [ ] `CHANGELOG.md` entry for v0.1.0
- [ ] Git tag `v0.1.0` applied

Below 100% on this checklist = pre-release. Tag `0.1.0-rc.N` instead.

---

## §20 — The pocket (Tier 0, memorize these 12)

These twelve atoms cover ~80% of daily symbol-art needs. They are in every vibe's starter set except where explicitly excluded. Memorize them.

| # | Glyph | Atom name | Primary use |
|---|-------|-----------|-------------|
| 1 | ● | black-circle | status: live / on |
| 2 | ○ | white-circle | status: offline / off |
| 3 | ◐ | left-half-black-circle | status: partial / idle |
| 4 | ✓ | check-mark | success / done |
| 5 | ✗ | ballot-x | failure / cancel |
| 6 | ⚠ | warning-sign (text form) | caution |
| 7 | → | rightwards-arrow | flow / next |
| 8 | · | middle-dot | separator |
| 9 | — | em-dash | section divider |
| 10 | ▰ | filled-rounded-square | progress filled cell |
| 11 | ▱ | empty-rounded-square | progress empty cell |
| 12 | ⋯ | midline-horizontal-ellipsis | more / overflow |

If you can compose with these twelve, you can build most of the kit's widgets. They are the muscle memory.

---

## §∞ — Spirit clause

When this file is silent on a question, default to the philosophy:

- Bottom-up over top-down.
- Coherence over completeness.
- Falsifiable over assertive.
- Memorable over comprehensive.
- Composable over standalone.
- RTL-equal, not RTL-afterthought.
- Dogfood or die.

Build the kit the kit would recommend.

— end of CLAUDE.md —
