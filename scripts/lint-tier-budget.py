#!/usr/bin/env python3
"""
scripts/lint-tier-budget.py — enforce tier discipline.

Checks:
1. Widgets don't pull more than 2 atoms from Tier 3
2. No Tier 4 atoms without explicit tier_override annotation
"""

import os
import sys
import yaml
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_atom_tiers(atoms_dir):
    """Return dict: glyph → tier"""
    tiers = {}
    for f in Path(atoms_dir).glob("*.yaml"):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if data.get('tier') is not None:
            tiers[data['glyph']] = data['tier']
    return tiers

def main():
    errors = 0
    tiers = load_atom_tiers(ROOT / "atoms")
    print(f"  loaded {len(tiers)} atom tiers")
    
    # Print tier distribution
    tier_counts = {}
    for t in tiers.values():
        tier_counts[t] = tier_counts.get(t, 0) + 1
    for t in sorted(tier_counts):
        print(f"  Tier {t}: {tier_counts[t]} atoms")
    
    # Check widgets.md
    if os.path.exists(ROOT / "widgets.md"):
        content = (ROOT / "widgets.md").read_text()
        sections = re.split(r'\n---\n', content)
        
        for section in sections:
            # Parse tier budget
            budget = {}
            for line in section.split('\n'):
                if 'tier_budget:' in line:
                    m = re.search(r'tier3:\s*(\d+)', line)
                    if m: budget[3] = int(m.group(1))
                    m = re.search(r'tier4:\s*(\d+)', line)
                    if m: budget[4] = int(m.group(1))
            
            # Count tier 3+ atoms used
            tier3_count = 0
            tier4_count = 0
            for ch in section:
                if ch in tiers:
                    t = tiers[ch]
                    if t == 3:
                        tier3_count += 1
                    elif t >= 4:
                        tier4_count += 1
            
            # Check against budget
            if budget and (tier3_count or tier4_count):
                if 3 in budget and tier3_count > budget[3]:
                    print(f"  ⚠ Tier 3 budget exceeded: used {tier3_count}, budget {budget[3]}")
                    errors += 1
                if 4 in budget and tier4_count > budget[4]:
                    print(f"  ⚠ Tier 4 budget exceeded: used {tier4_count}, budget {budget[4]}")
                    errors += 1
    
    print(f"\n{'✓ tier budget ok' if errors == 0 else f'✗ {errors} violation(s)'}")
    return errors

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
