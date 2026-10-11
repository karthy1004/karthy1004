"""Generates every image on the profile from one source of truth.

    python assets/build_assets.py

Outputs (light + dark for each): banner, one card per featured project, and the domain map.
Self-hosted SVG only: no third-party image services, so nothing can rate-limit or disappear.
Every number on a card must match the project's README, whose numbers come from real runs.
Edit the data below; never hand-edit the SVGs (CI fails if they drift from this script).
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

import build_domain_map

THEMES = {
    "light": {"bg": "#ffffff", "card": "#f6f8fa", "text": "#1f2328", "muted": "#59636e",
              "accent": "#9a6700", "accent_soft": "#fff8c5", "line": "#d1d9e0", "ok": "#1a7f37"},
    "dark": {"bg": "#0d1117", "card": "#151b23", "text": "#f0f6fc", "muted": "#9198a1",
             "accent": "#d29922", "accent_soft": "#272115", "line": "#3d444d", "ok": "#3fb950"},
}
FONT = ("font-family=\"-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif\"")

NAME = "Karthik Bhumireddy"
HEADLINE = "Product leader in payments and responsible-gold due diligence"
SUBHEAD = "who also builds the systems: state machines, audit trails, evidence-backed decisions."
CREDENTIALS = "Principal PM, Qenta  ·  ex-Paytm, Dineout  ·  Co-founder, Deccan Foods  ·  MBA, Rice"

# (slug, title, problem line, three proof lines, stack, status)
CARDS = [
    ("evidence-review-engine", "evidence-review-engine",
     "Due diligence that scores evidence, not claims",
     ["12 'yes' answers, bad documents: scores 16/100",
      "LLM extraction gated by grounding checks",
      "59 tests · 98% branch coverage"],
     "Python · Pydantic", "Working demo"),
    ("payments-reliability-lab", "payments-reliability-lab",
     "Payments that stay correct when everything retries",
     ["Timeout = unknown, never failed",
      "Exactly-once webhooks, one charge per retry",
      "59 tests · all 5 reconciliation break types"],
     "TypeScript · Node 24 · SQLite", "Working demo"),
    ("payee-verdict", "payee-verdict",
     "One payee-name decision across four payment systems",
     ["EU VoP · UK CoP · India · PIX, simulated",
      "181 hard cases: 96.1%, zero false matches",
      "143 tests · replayable evidence log"],
     "Python · Pydantic", "Working demo"),
    ("operon", "operon",
     "Job applications done for you, you keep the veto",
     ["Exactly-once Stripe webhooks (test mode)",
      "Approval engine with compare-and-set",
      "20-model domain · 13 unit tests"],
     "Next.js · Prisma · Stripe", "Prototype, not launched"),
]


def svg_open(w: int, h: int, title: str, desc: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" role="img" aria-labelledby="t d" {FONT}>'
            f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>')


def banner(c: dict[str, str]) -> str:
    w, h = 1100, 236
    p = [svg_open(w, h, NAME, f"{NAME}. {HEADLINE}, {SUBHEAD} {CREDENTIALS}"),
         f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{c["card"]}" '
         f'stroke="{c["line"]}"/>',
         f'<rect x="0" y="24" width="6" height="{h - 48}" rx="3" fill="{c["accent"]}"/>',
         f'<text x="42" y="80" font-size="46" font-weight="700" fill="{c["text"]}">{escape(NAME)}</text>',
         f'<text x="42" y="124" font-size="25" font-weight="600" fill="{c["text"]}">{escape(HEADLINE)}</text>',
         f'<text x="42" y="157" font-size="19" fill="{c["muted"]}">{escape(SUBHEAD)}</text>',
         f'<text x="42" y="204" font-size="17" fill="{c["accent"]}">{escape(CREDENTIALS)}</text>']
    # Motif: a short hash chain, the profile's theme (every step linked to the one before).
    x0, y = 930, 60
    for i in range(4):
        x = x0 + i * 40
        p.append(f'<rect x="{x}" y="{y + (i % 2) * 22}" width="26" height="26" rx="6" '
                 f'fill="{c["accent_soft"]}" stroke="{c["accent"]}" stroke-width="1.5"/>')
        if i:
            px = x - 40 + 26
            p.append(f'<line x1="{px}" y1="{y + 13 + ((i - 1) % 2) * 22}" x2="{x}" '
                     f'y2="{y + 13 + (i % 2) * 22}" stroke="{c["accent"]}" stroke-width="1.5"/>')
    p.append(f'<path d="M{x0 + 126} {y + 35} l5 5 l9 -11" fill="none" stroke="{c["ok"]}" '
             'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append(f'<text x="{x0 + 70}" y="{y + 82}" text-anchor="middle" font-size="11" '
             f'letter-spacing="1.2" fill="{c["muted"]}">EVIDENCE · AUDIT TRAIL</text>')
    p.append("</svg>")
    return "".join(p) + "\n"


def card(c: dict[str, str], data: tuple[str, str, str, list[str], str, str]) -> str:
    _slug, title, problem, proofs, stack, status = data
    w, h = 520, 262
    prototype = "Prototype" in status
    chip_fill = c["accent_soft"] if prototype else c["card"]
    chip_text = c["accent"] if prototype else c["ok"]
    p = [svg_open(w, h, title, f"{title}: {problem}. " + ". ".join(proofs) + f". {stack}. {status}."),
         f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{c["card"]}" '
         f'stroke="{c["line"]}"/>',
         f'<text x="22" y="40" font-size="22" font-weight="700" fill="{c["accent"]}">{escape(title)}</text>',
         f'<text x="22" y="70" font-size="16" font-weight="600" fill="{c["text"]}">{escape(problem)}</text>']
    for i, line in enumerate(proofs):
        y = 110 + i * 29
        p.append(f'<circle cx="28" cy="{y - 5}" r="3" fill="{c["accent"]}"/>')
        p.append(f'<text x="40" y="{y}" font-size="15.5" fill="{c["text"]}">{escape(line)}</text>')
    p.append(f'<line x1="22" y1="{h - 52}" x2="{w - 22}" y2="{h - 52}" stroke="{c["line"]}"/>')
    p.append(f'<text x="22" y="{h - 23}" font-size="14" fill="{c["muted"]}">{escape(stack)}</text>')
    chip_w = 14 + len(status) * 7.6
    p.append(f'<rect x="{w - 22 - chip_w}" y="{h - 42}" width="{chip_w}" height="27" rx="13.5" '
             f'fill="{chip_fill}" stroke="{chip_text}"/>')
    p.append(f'<text x="{w - 22 - chip_w / 2}" y="{h - 24}" text-anchor="middle" font-size="13" '
             f'font-weight="600" fill="{chip_text}">{escape(status)}</text>')
    p.append("</svg>")
    return "".join(p) + "\n"


if __name__ == "__main__":
    here = Path(__file__).parent
    for theme, colours in THEMES.items():
        (here / f"banner-{theme}.svg").write_text(banner(colours), encoding="utf-8", newline="\n")
        for data in CARDS:
            (here / f"card-{data[0]}-{theme}.svg").write_text(card(colours, data), encoding="utf-8",
                                                              newline="\n")
        (here / f"domain-map-{theme}.svg").write_text(
            build_domain_map.render(build_domain_map.THEMES[theme]), encoding="utf-8", newline="\n")
    print("wrote banner, cards and map for", ", ".join(THEMES))
