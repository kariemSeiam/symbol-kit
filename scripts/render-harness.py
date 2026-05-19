#!/usr/bin/env python3
"""
scripts/render-harness.py — generate HTML proof pages for all atoms.

Produces falsifiable render verification. Each atom rendered in
5 canonical contexts across multiple font stacks.

Usage:
  python3 scripts/render-harness.py              # all atoms
  python3 scripts/render-harness.py --tier 0      # Tier 0 only
  python3 scripts/render-harness.py --smoke       # Tier 0, fast check
  python3 scripts/render-harness.py --output proofs/  # custom output dir
"""

import os
import sys
import argparse
import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
ATOMS_DIR = ROOT / "atoms"
PROOFS_DIR = ROOT / "render-proofs"


def load_atoms(tier_filter=None):
    """Load all atoms, optionally filtered by tier."""
    atoms = []
    for f in sorted(ATOMS_DIR.glob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if tier_filter is not None and data.get('tier') != tier_filter:
            continue
        atoms.append(data)
    return atoms


def html_page(title, body, css_extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — symbol-kit render proof</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ 
    font-family: system-ui, -apple-system, sans-serif;
    background: #0d1117; color: #c9d1d9;
    padding: 2rem;
  }}
  h1 {{ color: #f0f6fc; margin-bottom: 0.5rem; }}
  .subtitle {{ color: #8b949e; margin-bottom: 2rem; font-size: 0.9rem; }}
  table {{ 
    width: 100%; border-collapse: collapse;
    margin-bottom: 3rem;
  }}
  th, td {{ 
    padding: 1rem; text-align: center;
    border: 1px solid #21262d;
  }}
  th {{ 
    background: #161b22; color: #f0f6fc;
    font-weight: 600; font-size: 0.85rem;
  }}
  .glyph-cell {{ font-size: 2rem; line-height: 1.5; }}
  .glyph-standalone {{ font-size: 3rem; }}
  .glyph-code {{ 
    font-family: ui-monospace, SF Mono, Cascadia Code, Consolas, monospace;
    font-size: 1.2rem;
  }}
  .glyph-pre {{ 
    font-family: ui-monospace, SF Mono, Cascadia Code, Consolas, monospace;
    font-size: 1rem; white-space: pre; text-align: left;
    background: #0d1117; padding: 0.5rem;
  }}
  .glyph-body {{ font-size: 1.2rem; text-align: left; }}
  .glyph-rtl {{ direction: rtl; text-align: right; font-size: 1.2rem; }}
  .atom-name {{ font-size: 0.7rem; color: #8b949e; }}
  .tier-badge {{ 
    display: inline-block; padding: 0.1rem 0.5rem;
    border-radius: 1rem; font-size: 0.7rem; font-weight: 600;
  }}
  .tier-0 {{ background: #238636; color: #fff; }}
  .tier-1 {{ background: #1f6feb; color: #fff; }}
  .tier-2 {{ background: #8957e5; color: #fff; }}
  .tier-3 {{ background: #6e7681; color: #fff; }}
  .tier-4 {{ background: #21262d; color: #8b949e; }}
  .vibe-tag {{ 
    display: inline-block; padding: 0.1rem 0.4rem;
    border-radius: 0.3rem; font-size: 0.65rem; 
    background: #21262d; color: #8b949e; margin: 0.1rem;
  }}
  .status-yes {{ color: #3fb950; }}
  .status-tofu {{ color: #f85149; }}
  .status-unverified {{ color: #8b949e; }}
  .separator {{ border-top: 2px solid #30363d; }}
{css_extra}
</style>
</head>
<body>
{body}
</body>
</html>"""


def render_atom_cells(atom):
    """Generate the 5-context cells for one atom."""
    g = atom['glyph']
    name = atom.get('name', '?')
    tier = atom.get('tier', 4)
    
    cells = []
    # 1. Standalone
    cells.append(f'<td class="glyph-cell glyph-standalone">{g}</td>')
    # 2. Body paragraph
    cells.append(f'<td class="glyph-cell glyph-body">The glyph {g} appears in running text like this. Status: {g} active.</td>')
    # 3. Inline code
    cells.append(f'<td class="glyph-cell glyph-code">status = <code>{g}</code>;</td>')
    # 4. Pre block
    cells.append(f'<td class="glyph-cell glyph-pre">┌─── status ───┐\n│ {g} live       │\n│ {g} active     │\n└──────────────┘</td>')
    # 5. RTL context
    cells.append(f'<td class="glyph-cell glyph-rtl">الحالة: {g} نشط · {g} متاح</td>')
    
    return "".join(cells)


def build_tier_page(atoms, tier):
    """Build an HTML page showing atoms for a specific tier."""
    tier_name = {0: "Pocket", 1: "Daily", 2: "Workshop", 3: "Library", 4: "Archive"}
    title = f"Tier {tier} — {tier_name.get(tier, '')}"
    
    rows = []
    for atom in atoms:
        g = atom['glyph']
        name = atom.get('name', '?')
        cp = atom.get('codepoint', '?')
        vibe_list = atom.get('vibes', [])
        tier = atom.get('tier', 4)
        
        vibe_tags = " ".join(f'<span class="vibe-tag">{v}</span>' for v in vibe_list[:3])
        
        rows.append(f"""<tr>
  <td style="font-size: 2.5rem;">{g}</td>
  <td style="text-align:left;">
    <div style="font-weight:600;">{name}</div>
    <div class="atom-name">{cp}</div>
    <div>{vibe_tags}</div>
  </td>
  {render_atom_cells(atom)}
</tr>""")
    
    body = f"""<h1>{title}</h1>
<div class="subtitle">{len(atoms)} atoms · symbol-kit render proof · generated {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}</div>
<table>
<thead><tr>
  <th>Glyph</th><th>Metadata</th>
  <th>Standalone</th><th>Body</th><th>&lt;code&gt;</th><th>&lt;pre&gt;</th><th>RTL</th>
</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>"""
    
    return html_page(title, body)


def build_vibe_showcase(atoms):
    """Build a page showing all vibes side by side."""
    vibes_order = [
        "terminal-hacker", "modern-minimal", "maximalist-decorative",
        "rtl-arabic-elegant", "scientific-technical", "game-ui",
        "status-operational", "diff-patch"
    ]
    
    vibe_atoms = defaultdict(list)
    for atom in atoms:
        for v in atom.get('vibes', []):
            vibe_atoms[v].append(atom)
    
    sections = []
    for vibe in vibes_order:
        atoms_in_vibe = vibe_atoms.get(vibe, [])
        if not atoms_in_vibe:
            continue
        
        glyph_row = " ".join(a['glyph'] for a in atoms_in_vibe[:30])
        
        sections.append(f"""<div class="vibe-section">
<h2>{vibe}</h2>
<div style="font-size: 1.5rem; letter-spacing: 0.5rem; line-height: 2.5; padding: 1rem; background: #161b22; border-radius: 0.5rem; margin-bottom: 1rem;">
{glyph_row}
</div>
<div class="subtitle">{len(atoms_in_vibe)} atoms in starter set</div>
</div>""")
    
    body = f"""<h1>All Vibes Side by Side</h1>
<div class="subtitle">symbol-kit render proof · {len(atoms)} total atoms</div>
{chr(10).join(sections)}"""
    
    return html_page("All Vibes", body)


def build_widget_gallery():
    """Build a page showing widget examples from widgets.md."""
    widgets_md = ROOT / "widgets.md"
    if not widgets_md.exists():
        return None
    
    content = widgets_md.read_text()
    
    # Extract code blocks
    import re
    blocks = re.findall(r'```text\n(.*?)```', content, re.DOTALL)
    
    sections = []
    for i, block in enumerate(blocks):
        sections.append(f"""<div class="widget-section">
<h3>Widget {i+1}</h3>
<pre style="font-family: ui-monospace, SF Mono, Cascadia Code, Consolas, monospace; 
     font-size: 1rem; background: #161b22; padding: 1rem; border-radius: 0.5rem;
     line-height: 1.6; overflow-x: auto;">
{block.strip()}
</pre>
</div>""")
    
    body = f"""<h1>Widget Gallery</h1>
<div class="subtitle">symbol-kit · {len(sections)} widget examples</div>
{chr(10).join(sections)}"""
    
    return html_page("Widget Gallery", body)


def build_rtl_showcase(atoms):
    """Build an Arabic/RTL render proof page."""
    arabic_atoms = [a for a in atoms if 'rtl-arabic-elegant' in a.get('vibes', [])]
    
    rows = []
    for atom in arabic_atoms:
        g = atom['glyph']
        name = atom.get('name', '?')
        cp = atom.get('codepoint', '?')
        
        rows.append(f"""<tr>
  <td style="font-size: 2rem;">{g}</td>
  <td style="text-align:right; font-size: 1.2rem;" dir="rtl">{g} مثال نص عربي</td>
  <td style="text-align:left; font-size: 0.8rem;">{name}<br><span class="atom-name">{cp}</span></td>
</tr>""")
    
    body = f"""<h1>RTL Arabic Showcase</h1>
<div class="subtitle">{len(arabic_atoms)} Arabic-context atoms · symbol-kit</div>
<table>
<thead><tr>
  <th>Glyph</th><th dir="rtl">سياق عربي</th><th>Metadata</th>
</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>"""
    
    return html_page("RTL Arabic Showcase", body, """
  body { direction: ltr; }
""")


def main():
    parser = argparse.ArgumentParser(description="symbol-kit render proof harness")
    parser.add_argument('--tier', type=int, help='Generate proof for specific tier only')
    parser.add_argument('--smoke', action='store_true', help='Tier 0 only (fast check)')
    parser.add_argument('--output', type=str, default=None, help='Output directory (default: render-proofs/)')
    args = parser.parse_args()
    
    if args.smoke:
        args.tier = 0
    
    out_dir = Path(args.output) if args.output else PROOFS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    
    all_atoms = load_atoms()
    tier_atoms = load_atoms(args.tier) if args.tier is not None else None
    
    pages = []
    
    # Tier pages
    if tier_atoms is not None:
        pages.append(("tier", f"tier-{args.tier}-{['pocket','daily','workshop','library','archive'][args.tier]}.html",
                       build_tier_page(tier_atoms, args.tier)))
    else:
        for tier in range(5):
            tier_a = [a for a in all_atoms if a.get('tier') == tier]
            if not tier_a:
                continue
            tier_names = {0: "pocket", 1: "daily", 2: "workshop", 3: "library", 4: "archive"}
            pages.append(("tier", f"tier-{tier}-{tier_names[tier]}.html",
                          build_tier_page(tier_a, tier)))
    
    # Vibe showcase
    pages.append(("vibe", "all-vibes-side-by-side.html", build_vibe_showcase(all_atoms)))
    
    # Widget gallery
    widget_html = build_widget_gallery()
    if widget_html:
        pages.append(("widget", "widget-gallery.html", widget_html))
    
    # RTL showcase
    pages.append(("rtl", "rtl-arabic-showcase.html", build_rtl_showcase(all_atoms)))
    
    # Write all pages
    for category, filename, html in pages:
        path = out_dir / filename
        with open(path, 'w') as f:
            f.write(html)
        size_kb = os.path.getsize(path) / 1024
        print(f"  ✓ {path.name} ({size_kb:.1f} KB)")
    
    total = len(pages)
    print(f"\n{total} render proof page(s) generated in {out_dir}/")
    print("Open with: python3 -m http.server 8080 -d render-proofs/")


if __name__ == "__main__":
    main()
