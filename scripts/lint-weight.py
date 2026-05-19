#!/usr/bin/env python3
"""
scripts/lint-weight.py — enforce single weight class per code block element.

Only checks glyphs within ```text code blocks in widgets.md — not prose.
"""

import os
import sys
import re
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_atom_weights(atoms_dir):
    weights = {}
    for f in Path(atoms_dir).glob("*.yaml"):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if data.get('weight_class'):
            weights[data['glyph']] = data['weight_class']
    return weights

def extract_code_blocks(text):
    blocks = re.findall(r'```(?:text)?\n(.*?)```', text, re.DOTALL)
    return blocks

def main():
    errors = 0
    weights = load_atom_weights(ROOT / "atoms")
    
    # Check widgets.md
    if os.path.exists(ROOT / "widgets.md"):
        content = (ROOT / "widgets.md").read_text()
        
        # Split by widget sections (front matter)
        sections = re.split(r'\n---\n', content)
        
        current_vibe = None
        declared_weight = None
        
        for section in sections:
            lines = section.strip().split('\n')
            if not lines:
                continue
            
            for line in lines[:5]:
                if line.strip().startswith('vibe:'):
                    current_vibe = line.split(':',1)[1].strip()
                if line.strip().startswith('weight:'):
                    declared_weight = line.split(':',1)[1].strip()
            
            # Get code blocks
            blocks = extract_code_blocks('\n'.join(lines))
            
            for block in blocks:
                weight_classes = set()
                for ch in block:
                    if ch in weights:
                        weight_classes.add(weights[ch])
                
                if len(weight_classes) > 1:
                    # Some mixing is allowed if close (W1+W2 is ok, W1+W4 is not)
                    wc_sorted = sorted(weight_classes)
                    wc_str = ", ".join(wc_sorted)
                    
                    # Calculate severity
                    w_nums = [int(w[1]) for w in wc_sorted if w.startswith('W') and w[1].isdigit()]
                    if w_nums and max(w_nums) - min(w_nums) <= 1:
                        continue  # Adjacent weight classes tolerated
                    
                    context = block[:60].replace('\n', '\\n')
                    print(f"  ⚠ weight mix: {wc_str} in {'  '.join(context.split())} (declared: {declared_weight})")
                    errors += 1
    
    # Also check vibe files' code blocks
    vibe_dir = ROOT / "vibes"
    for f in sorted(vibe_dir.glob("*.md")):
        content = f.read_text()
        declared_weight = None
        for line in content.split('\n')[:5]:
            if line.strip().startswith('weight:'):
                declared_weight = line.split(':',1)[1].strip()
        
        blocks = extract_code_blocks(content)
        for block in blocks:
            weight_classes = set()
            for ch in block:
                if ch in weights:
                    weight_classes.add(weights[ch])
            
            if len(weight_classes) > 1:
                wc_sorted = sorted(weight_classes)
                w_nums = [int(w[1]) for w in wc_sorted if w.startswith('W') and w[1].isdigit()]
                if w_nums and max(w_nums) - min(w_nums) <= 1:
                    continue
                wc_str = ", ".join(wc_sorted)
                print(f"  ⚠ {f.name}: weight mix {wc_str} (declared: {declared_weight})")
                errors += 1
    
    print(f"\n{'✓ weight class coherence ok' if errors == 0 else f'✗ {errors} violation(s)'}")
    return errors

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
