#!/usr/bin/env bash
# scripts/ci.sh — orchestrates all quality gates.
#
# This script grows as phases land (see CLAUDE.md §11). Adding a "--skip" flag
# is forbidden (CLAUDE.md §18 ACAP-08: test-skip cascade). To advance a phase,
# implement the next script and add its invocation below — do not bypass.

set -euo pipefail

cd "$(dirname "$0")/.."

PY=${PYTHON:-python3}

step() {
  printf '\n▸ %s\n' "$1"
}

step "atom schema validation"
"$PY" scripts/validate-atom.py atoms/

# Phase 3 — cross-references (pending)
# step "cross-reference resolution"
# "$PY" scripts/check-cross-references.py

# Phase 4 — vibe & weight coherence (pending)
# step "vibe coherence"
# "$PY" scripts/lint-vibe.py widgets.md vibes/
# step "weight-class coherence"
# "$PY" scripts/lint-weight.py widgets.md
# step "tier budget"
# "$PY" scripts/lint-tier-budget.py widgets.md

# Phase 5 — grammar (pending)
# step "grammar test suite (python)"
# "$PY" grammar/python/test_symbolkit.py
# step "grammar test suite (typescript)"
# (cd grammar/typescript && npm test)

# Phase 6 — render harness (pending)
# step "render harness (smoke)"
# "$PY" scripts/render-harness.py --smoke

# Phase 8 — self-reference (pending)
# step "self-reference (README uses only catalogued atoms)"
# "$PY" scripts/check-self-reference.py README.md

printf '\n✓ all implemented checks passed\n'
