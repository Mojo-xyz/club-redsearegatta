#!/usr/bin/env python3
"""
Aligns index-source.html with SOMABAY Yacht Club MOU Draft 3.

Usage:
    python3 patch_deck.py index-source.html

Writes index-source.html and keeps a backup at index-source.html.bak
Every replacement must match exactly once, or the script aborts without
writing anything.
"""
import sys, shutil, os

def label(name, tag):
    return (
        f'<div class="rev-label">{name}</div>',
        f'<div class="rev-label">{name} <span style="font-size:9px;'
        f'letter-spacing:1.5px;color:var(--text-muted);text-transform:uppercase">'
        f'&middot; {tag}</span></div>'
    )

NEW_PILLARS = '''      <div class="pillar-item">
        <svg class="s-icon" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#c9784a" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><path d="M8 12h8M12 8v8"/></svg>
        <div class="pillar-tag">Pillar 05</div>
        <div class="pillar-name">Club Membership &amp; Community</div>
        <div class="pillar-desc">A curated membership of Egyptian and international yacht owners and sailors, with a year-round calendar of member events, racing, and social programming. The community is the institution.</div>
      </div>
      <div class="pillar-item">
        <svg class="s-icon" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--teal)" stroke-width="1.5"><path d="M4 8h16l-1.5 12h-13z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>
        <div class="pillar-tag">Pillar 06</div>
        <div class="pillar-name">Retail &amp; Chandlery</div>
        <div class="pillar-desc">A sailing retail and chandlery outlet within the permanent clubhouse &mdash; equipment, technical clothing, safety gear, and SOMABAY Yacht Club branded apparel for members, berth holders, students, and resort guests.</div>
      </div>
      <div class="pillar-winter">'''

REPLACEMENTS = [
    # ---- 1. Section 06 : revenue attribution -------------------------------
    ("06 framing paragraph",
     'The figures below are <strong style="color:var(--text-primary)">steady-state estimates</strong> \u2014 what each pillar contributes annually once the club is established and the Winter Yacht Program has scaled to full capacity (50\u201370 wintering yachts), consistent with the economic model that follows. Year one is a fraction of these numbers; each stream ramps over three to four seasons as the fleet grows, membership matures, and the events calendar fills. We\'re showing the destination at maturity \u2014 conservatively \u2014 not the opening season.',
     'The figures below are <strong style="color:var(--text-primary)">steady-state estimates</strong> \u2014 what the Club generates annually once established and the Winter Yacht Program has scaled to full capacity (50\u201370 wintering yachts). Streams marked <strong style="color:var(--text-primary)">RSS-operated</strong> are run, staffed, and funded by Red Sea Sails at its own cost and risk. Streams marked <strong style="color:var(--text-primary)">to SOMABAY</strong> accrue directly to the resort. Berth revenue is shared between the parties. Year one is a fraction of these numbers; each stream ramps over three to four seasons. Illustrative ranges \u2014 not targets or commitments.'),

    ("06 label \u2014 berth fees",  *label("Marina Berth Fees", "Shared")),
    ("06 label \u2014 hotel & F&B", *label("Hotel & F&B Spend", "To SOMABAY")),
    ("06 label \u2014 membership",  *label("Club Membership", "RSS-operated")),
    ("06 label \u2014 charter",     *label("Charter Revenue", "RSS-operated")),
    ("06 label \u2014 events",      *label("Events & Sponsorship", "RSS-operated")),
    ("06 label \u2014 real estate", *label("Real Estate Value", "To SOMABAY")),

    ("06 charter card body",
     'Day and multi-day charters generate direct revenue through agreed commercial arrangements and referral structures between RSS and SOMABAY.',
     'Day and multi-day charters for resort guests, residents, and visiting clients. Operated by RSS, with charter guests driving hotel nights, F&amp;B, and marina spend at SOMABAY.'),

    ("06 closing note",
     'At-maturity annual estimates for core Club operations at steady state. The Winter Yacht Program is additional to these figures',
     'Illustrative at-maturity estimates for core Club operations at steady state \u2014 not targets or commitments. The Winter Yacht Program is additional to these figures'),

    # ---- 2. Section 05 : pillars ------------------------------------------
    ("contents \u2014 pillar count",
     'Four pillars, one umbrella \u2014 and the wider maritime world',
     'Seven pillars, one umbrella \u2014 and the wider maritime world'),

    ("05 charter fleet size",
     'Premium fleet of 40\u201360ft monohulls and catamarans.',
     'Premium fleet of 30\u201380ft monohulls and catamarans.'),

    ("05 add pillars 05\u201307",
     '      <div class="pillar-winter">',
     NEW_PILLARS),

    # ---- 3. Section 09 : roadmap ------------------------------------------
    ("05 winter strip \u2192 pillar 07",
     '<span><strong>+ FX\u2013RSS Winter Yacht Program</strong> &nbsp;\u00b7&nbsp; October through April &nbsp;\u00b7&nbsp; Red Sea Season</span>',
     '<span><strong>Pillar 07 &nbsp;\u00b7&nbsp; FX\u2013RSS Winter Yacht Program</strong> &nbsp;\u00b7&nbsp; October through April &nbsp;\u00b7&nbsp; Red Sea Season</span>'),

    ("09 roadmap \u2014 Q3 2026",
     '<div class="tl-date">Q3 2026</div><div class="tl-title">Charter & School Launch</div><div class="tl-body">Charter operations begin. Sailing school Phase 1 opens for hotel guests, residents, and students.</div>',
     '<div class="tl-date">Q3 2026</div><div class="tl-title">Charter Operations Launch</div><div class="tl-body">Charter operations begin at SOMABAY. Winter Yacht Program preparations underway.</div>'),

    ("09 roadmap \u2014 Q4 2026",
     '<div class="tl-date tl-date-gold">Q4 2026</div><div class="tl-title">Yacht Club Launch</div><div class="tl-body">Full club structure, membership programme, and winter yacht program fully operational.</div>',
     '<div class="tl-date tl-date-gold">Nov\u2013Dec 2026</div><div class="tl-title">School Opens &middot; Yacht Club Launch</div><div class="tl-body">Sailing school opens as an RYA-accredited affiliate satellite. Club formally established and membership launched. 2027 runs as the pilot year.</div>'),

    # ---- 4. Section 11 : the ask ------------------------------------------
    ("11 ask 03 \u2014 title",
     'Berths from September / October',
     'Dedicated Sailing Berths'),

    ("11 ask 03 \u2014 body",
     'Several berths from the start of the autumn season for the yachts we bring to SOMABAY \u2014 both locally-owned vessels and the FX Winter Program fleet.',
     'An allocation of 30 dedicated sailing berths (15 catamaran, 15 monohull) managed by RSS for the Club\u2019s fleet and community \u2014 locally-owned vessels and the FX Winter Program fleet \u2014 from the start of the autumn season.'),

    ("11 ask 06 \u2014 body",
     'A growing allocation of sailing yacht berths as the winter fleet and resident community scale \u2014 building to 30 dedicated sailing berths (15 catamaran, 15 monohull) at marina completion, managed by RSS under the Club.',
     'The dedicated sailing berths carried through to the completed marina, managed by RSS under the Club, with capacity growing as the winter fleet and resident community scale.'),

    ("11 ask 08 \u2014 body",
     'A mutually beneficial agreement covering revenue sharing, berth fee structures, charter referrals, and school operations \u2014 to be defined together.',
     'A mutually beneficial agreement covering berth fee structures and revenue sharing, space and fit-out terms, and the operating framework for each pillar \u2014 to be defined together.'),
]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "index-source.html"
    if not os.path.exists(path):
        sys.exit(f"File not found: {path}")

    html = open(path, encoding="utf-8").read()

    errors, applied = [], []
    for name, find, repl in REPLACEMENTS:
        n = html.count(find)
        if n == 0:
            errors.append(f"  NOT FOUND  {name}")
        elif n > 1:
            errors.append(f"  {n} MATCHES {name}  (must be exactly 1)")
        else:
            html = html.replace(find, repl, 1)
            applied.append(f"  ok  {name}")

    if errors:
        print("ABORTED \u2014 nothing written.\n")
        print("\n".join(errors))
        if applied:
            print("\nWould have applied:")
            print("\n".join(applied))
        sys.exit(1)

    shutil.copy(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(html)
    print("\n".join(applied))
    print(f"\n{len(applied)} replacements applied.")
    print(f"Backup: {path}.bak")


if __name__ == "__main__":
    main()
