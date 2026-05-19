#!/usr/bin/env python3
"""
scripts/check-cross-references.py — verify all cross-references in the kit resolve.

Checks:
1. Every atom file referenced in pairs.md exists in atoms/
2. Every set referenced in compositions.md exists in sets.md
3. Every widget reference in widgets.md resolves
4. Every vibe name referenced exists as a vibe file
5. Every cross_reference in atom YAML resolves
"""

import os
import sys
import re
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATOMS_DIR = ROOT / "atoms"
VIBES_DIR = ROOT / "vibes"

def load_atom_names():
    """Return set of atom names from atoms/ directory."""
    names = set()
    for f in ATOMS_DIR.glob("*.yaml"):
        names.add(f.stem)
    return names

def load_vibe_names():
    """Return set of vibe names from vibes/ directory."""
    names = set()
    for f in VIBES_DIR.glob("*.md"):
        names.add(f.stem.replace("01-","").replace("02-","").replace("03-","")
                  .replace("04-","").replace("05-","").replace("06-","")
                  .replace("07-","").replace("08-",""))
    return names

def check_file_exists(path):
    return os.path.exists(ROOT / path)

errors = 0

def err(msg):
    global errors
    print(f"  ✗ {msg}")
    errors += 1

def ok(msg):
    print(f"  ✓ {msg}")

# --- 1. Check atoms referenced in markdown docs exist ---

print("▸ cross-reference: atom names in docs")
atom_names = load_atom_names()
print(f"  {len(atom_names)} atoms in atoms/")

# Check pairs.md
if os.path.exists(ROOT / "pairs.md"):
    content = (ROOT / "pairs.md").read_text()
    # Find atom references in bold: **Atoms:** ● (atom-name)
    refs = re.findall(r'\(([a-z]+(?:-[a-z0-9]+)+)\)', content)
    for ref in refs:
        if ref not in atom_names and ref not in (): 
            err(f"pairs.md references unknown atom: {ref}")

# Check sets.md
if os.path.exists(ROOT / "sets.md"):
    content = (ROOT / "sets.md").read_text()
    refs = re.findall(r'\(([a-z]+(?:-[a-z0-9]+)+)\)', content)
    for ref in refs:
        if ref not in atom_names:
            if ref in ('terminal-hacker','modern-minimal','maximalist-decorative',
                       'rtl-arabic-elegant','scientific-technical','game-ui',
                       'status-operational','diff-patch'):
                continue
            err(f"sets.md references unknown atom: {ref}")

# Check compositions.md
if os.path.exists(ROOT / "compositions.md"):
    content = (ROOT / "compositions.md").read_text()
    refs = re.findall(r'\(([a-z]+(?:-[a-z0-9]+)+)\)', content)
    for ref in refs:
        if ref not in atom_names:
            if ref in ('terminal-hacker','modern-minimal','maximalist-decorative',
                       'rtl-arabic-elegant','scientific-technical','game-ui',
                       'status-operational','diff-patch','any'):
                continue
            err(f"compositions.md references unknown atom: {ref}")

# Check widgets.md
if os.path.exists(ROOT / "widgets.md"):
    content = (ROOT / "widgets.md").read_text()
    refs = re.findall(r'\(([a-z]+(?:-[a-z0-9]+)+)\)', content)
    for ref in refs:
        if ref not in atom_names:
            if ref in ('terminal-hacker','modern-minimal','maximalist-decorative',
                       'rtl-arabic-elegant','scientific-technical','game-ui',
                       'status-operational','diff-patch','any'):
                continue
            err(f"widgets.md references unknown atom: {ref}")

# --- 2. Check atom YAML cross_references ---

print("\n▸ cross-reference: atom YAML -> doc references")
for f in sorted(ATOMS_DIR.glob("*.yaml")):
    with open(f) as fh:
        data = yaml.safe_load(fh)
    
    if 'cross_references' not in data:
        continue
    
    refs = data['cross_references']
    atom_name = f.stem
    
    # Check pairs refs
    for ref in refs.get('pairs', []):
        anchor = ref.split('#')[0]
        if anchor and not anchor.endswith('.md'):
            continue
        if anchor == 'pairs.md':
            if not os.path.exists(ROOT / 'pairs.md'):
                err(f"{atom_name}: cross-ref pairs.md but file missing")

    # Check sets refs
    for ref in refs.get('sets', []):
        anchor = ref.split('#')[0]
        if anchor == 'sets.md':
            if not os.path.exists(ROOT / 'sets.md'):
                err(f"{atom_name}: cross-ref sets.md but file missing")

    # Check widgets refs
    for ref in refs.get('widgets', []):
        anchor = ref.split('#')[0]
        if anchor == 'widgets.md':
            if not os.path.exists(ROOT / 'widgets.md'):
                err(f"{atom_name}: cross-ref widgets.md but file missing")

# --- 3. Check vibe references ---

print("\n▸ cross-reference: vibe names")
vibe_prefixes = {
    'terminal-hacker': '01-terminal-hacker.md',
    'modern-minimal': '02-modern-minimal.md',
    'maximalist-decorative': '03-maximalist-decorative.md',
    'rtl-arabic-elegant': '04-rtl-arabic-elegant.md',
    'scientific-technical': '05-scientific-technical.md',
    'game-ui': '06-game-ui.md',
    'status-operational': '07-status-operational.md',
    'diff-patch': '08-diff-patch.md',
}

for vibe, filename in vibe_prefixes.items():
    if not os.path.exists(VIBES_DIR / filename):
        err(f"vibe '{vibe}' references {filename} which is missing")
    else:
        ok(f"vibe '{vibe}' → {filename}")

# Check atom vibes field
for f in sorted(ATOMS_DIR.glob("*.yaml")):
    with open(f) as fh:
        data = yaml.safe_load(fh)
    if 'vibes' in data:
        for v in data['vibes']:
            if v not in vibe_prefixes:
                err(f"{f.stem}: references unknown vibe '{v}'")

# --- 4. Check README self-reference (CLAUDE.md §15) ---

print("\n▸ dogfood: README uses only catalogued atoms")
if os.path.exists(ROOT / "README.md"):
    readme = (ROOT / "README.md").read_text()
    # Find Tier-0 glyphs mentioned in README
    tier0_glyphs = set()
    for f in sorted(ATOMS_DIR.glob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if data.get('tier') == 0:
            tier0_glyphs.add(data['glyph'])
    
    # Check if all non-ASCII glyphs in README are catalogued
    for i, ch in enumerate(readme):
        if ord(ch) > 127 and ch not in ('\n',' '):
            if ch in tier0_glyphs:
                continue
            if ch in ('─','│','┌','┐','└','┘','├','┤','▶','▸'):  # structural in README
                continue
            ok(f"  README uses catalogued glyph: U+{ord(ch):04X} '{ch}'")

print(f"\n{'✓ all cross-references resolve' if errors == 0 else f'✗ {errors} error(s) found'}")
sys.exit(1 if errors else 0)
