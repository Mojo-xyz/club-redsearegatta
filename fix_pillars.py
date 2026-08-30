#!/usr/bin/env python3
"""
fix_pillars.py

Run this ONLY if you already ran patch_deck.py successfully once (the run
that reported "18 replacements applied").

It does two things:
  1. Removes the Winter Yacht Program pillar CARD, leaving six cards so the
     two-column grid fills evenly with no empty cell.
  2. Relabels the existing teal winter strip as Pillar 07.

Usage:
    python3 fix_pillars.py index-source.html

Aborts without writing if the file is not in the expected state.
Backup written to index-source.html.bak2
"""
import sys, os, shutil

WINTER_CARD = '''      <div class="pillar-item">
        <svg class="s-icon" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#c9784a" stroke-width="1.5"><path d="M3 18h18"/><path d="M6 18V9l6-5 6 5v9"/><path d="M12 4v14"/></svg>
        <div class="pillar-tag">Pillar 07</div>
        <div class="pillar-name">Winter Yacht Program</div>
        <div class="pillar-desc">A European fleet wintering at SOMABAY from October through April with FX Yachting &mdash; SOMABAY as the fleet&rsquo;s Red Sea home port. A pillar in its own right, distinct from local charter.</div>
      </div>
'''

STRIP_OLD = ('<span><strong>+ FX\u2013RSS Winter Yacht Program</strong> '
             '&nbsp;\u00b7&nbsp; October through April &nbsp;\u00b7&nbsp; Red Sea Season</span>')
STRIP_NEW = ('<span><strong>Pillar 07 &nbsp;\u00b7&nbsp; FX\u2013RSS Winter Yacht Program</strong> '
             '&nbsp;\u00b7&nbsp; October through April &nbsp;\u00b7&nbsp; Red Sea Season</span>')

STEPS = [
    ("remove Winter pillar card", WINTER_CARD, ""),
    ("relabel winter strip as Pillar 07", STRIP_OLD, STRIP_NEW),
]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "index-source.html"
    if not os.path.exists(path):
        sys.exit(f"File not found: {path}")

    html = open(path, encoding="utf-8").read()

    cards = html.count('class="pillar-item"')
    if cards != 7:
        sys.exit(
            f"ABORTED \u2014 expected 7 pillar cards, found {cards}.\n"
            "This script only fixes a file already patched once by patch_deck.py."
        )

    errors, applied = [], []
    for name, find, repl in STEPS:
        n = html.count(find)
        if n != 1:
            errors.append(f"  {'NOT FOUND' if n == 0 else str(n) + ' MATCHES'}  {name}")
        else:
            html = html.replace(find, repl, 1)
            applied.append(f"  ok  {name}")

    if errors:
        print("ABORTED \u2014 nothing written.\n")
        print("\n".join(errors))
        sys.exit(1)

    final = html.count('class="pillar-item"')
    if final != 6:
        sys.exit(f"ABORTED \u2014 ended with {final} cards, expected 6. Nothing written.")

    shutil.copy(path, path + ".bak2")
    open(path, "w", encoding="utf-8").write(html)
    print("\n".join(applied))
    print(f"\nPillar cards: 7 \u2192 6 (even 2\u00d73 grid, no orphan)")
    print(f"Backup: {path}.bak2")


if __name__ == "__main__":
    main()
