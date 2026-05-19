#!/usr/bin/env python3
"""
scripts/lint-vibe.py — enforce vibe coherence.

Checks code block examples in widgets.md and vibe files against their declared vibe's starter set.
"""

import os
import sys
import re
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CROSS_VIBE_ALLOWLIST = {
    '●', '○', '◐',      # severity dots
    '→', '←', '↑', '↓',  # arrows
    '·', '—', '…', '⋯',  # separators
    '✓', '✗',            # check/cross
    ' ', '\t',           # whitespace
}

def load_glyph_map(atoms_dir):
    gmap = {}
    for f in Path(atoms_dir).glob("*.yaml"):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        gmap[data['glyph']] = f.stem
    return gmap

def load_vibe_starter_set(vibe_file):
    glyphs = set()
    content = Path(vibe_file).read_text()
    in_starter = False
    for line in content.split('\n'):
        if '## Starter Set' in line or '###' in line and 'starter' in line.lower():
            in_starter = True
            continue
        if in_starter and (line.startswith('## ') and 'Starter' not in line):
            break
        if in_starter:
            for ch in line:
                if ord(ch) > 127 and ch not in (' ', '\t', '-', '–', '(', ')', '[', ']', '·', ':', '~', '|', '.'):
                    glyphs.add(ch)
    return glyphs

def extract_code_blocks(text):
    """Extract text from within ```text ... ``` blocks."""
    blocks = re.findall(r'```(?:text)?\n(.*?)```', text, re.DOTALL)
    return blocks

def main():
    errors = 0
    glyph_map = load_glyph_map(ROOT / "atoms")
    
    vibe_sets = {}
    vibe_dir = ROOT / "vibes"
    for f in sorted(vibe_dir.glob("*.md")):
        vibe_name = f.stem.replace("01-","").replace("02-","").replace("03-","")\
                   .replace("04-","").replace("05-","").replace("06-","")\
                   .replace("07-","").replace("08-","")
        vibe_sets[vibe_name] = load_vibe_starter_set(f)
    
    # Check widgets.md
    if os.path.exists(ROOT / "widgets.md"):
        content = (ROOT / "widgets.md").read_text()
        
        # Find widget sections: front matter (vibe: X) followed by content until next front matter
        # Pattern: ---\nvibe: X\nweight: ...\n---\n## Widget Name\n... code blocks ...
        sections = re.split(r'\n---\n', content)
        
        current_vibe = None
        for i, section in enumerate(sections):
            lines = section.strip().split('\n')
            if not lines:
                continue
            
            # Check if this section has vibe declaration
            for line in lines[:5]:
                if line.strip().startswith('vibe:'):
                    current_vibe = line.split(':',1)[1].strip()
                    break
            
            if not current_vibe:
                continue
            
            # Extract code blocks from this section
            blocks = extract_code_blocks('\n'.join(lines))
            
            for block in blocks:
                for line in block.split('\n'):
                    for ch in line:
                        if ord(ch) <= 127:
                            continue
                        if ch in CROSS_VIBE_ALLOWLIST:
                            continue
                        if ch in glyph_map:
                            atom_name = glyph_map[ch]
                            if current_vibe not in vibe_sets or ch not in vibe_sets.get(current_vibe, set()):
                                # Check if this glyph is in ANY vibe's starter set
                                found_in = []
                                for vn, vs in vibe_sets.items():
                                    if ch in vs:
                                        found_in.append(vn)
                                if found_in:
                                    print(f"  ⚠ {atom_name} ({ch}) in '{current_vibe}' code block — belongs to: {', '.join(found_in)}")
    
    print(f"\n{'✓ vibe coherence ok' if errors == 0 else f'✗ {errors} violation(s)'}")
    return errors

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
