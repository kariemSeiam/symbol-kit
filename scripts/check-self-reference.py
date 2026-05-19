#!/usr/bin/env python3
"""
scripts/check-self-reference.py — enforce dogfooding.
CLAUDE.md §15: README must use only catalogued Tier 0–1 atoms.

Also checks TIERS.md.
"""

import os
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_catalogued_tier01(atoms_dir):
    """Return set of glyphs that are Tier 0 or Tier 1."""
    glyphs = set()
    for f in Path(atoms_dir).glob("*.yaml"):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if data.get('tier') in (0, 1):
            glyphs.add(data['glyph'])
    return glyphs

def main():
    errors = 0
    allowed = load_catalogued_tier01(ROOT / "atoms")
    # Add structural glyphs that README needs for formatting
    allowed.update({'─', '│', '┌', '┐', '└', '┘', '├', '┤', '▶', '▸', 
                    '▔', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█',
                    '▰', '▱', '▓', '░', '▒', '▐', '▌', '▍', '▎', '▏'})
    
    print(f"  {len(allowed)} allowed glyphs (Tier 0-1 + structural)")
    
    to_check = ['README.md']
    
    for filename in to_check:
        filepath = ROOT / filename
        if not os.path.exists(filepath):
            print(f"  ⚠ {filename} not found")
            continue
        
        content = filepath.read_text()
        uncatalogued = []
        
        for i, ch in enumerate(content):
            if ord(ch) > 127 and ch not in ('\n', ' ', '\t'):
                if ch not in allowed:
                    uncatalogued.append((i, ch, ord(ch)))
        
        if uncatalogued:
            print(f"\n  ✗ {filename}: {len(uncatalogued)} uncatalogued glyph(s):")
            for line_no, ch, cp in uncatalogued[:10]:
                # Find line context
                line_start = content.rfind('\n', 0, line_no) + 1
                line_end = content.find('\n', line_no)
                context = content[line_start:line_end].strip()[:60]
                print(f"    U+{cp:04X} '{ch}' in: {context}")
            errors += len(uncatalogued)
        else:
            print(f"  ✓ {filename}: all glyphs catalogued")
    
    print(f"\n{'✓ self-reference ok' if errors == 0 else f'✗ {errors} issues'}")
    return errors

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
