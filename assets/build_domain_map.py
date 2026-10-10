"""Generates assets/domain-map-{light,dark}.svg from one layout.

    python assets/build_domain_map.py

Kept as code so the graphic is reproducible and diffable: edit labels here, never the SVG.
Colours follow GitHub's light/dark palettes so the map sits naturally on either theme.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

THEMES = {
    "light": {"text": "#1f2328", "muted": "#59636e", "accent": "#9a6700", "line": "#d1d9e0",
              "box": "#f6f8fa", "hub": "#fff8c5"},
    "dark": {"text": "#f0f6fc", "muted": "#9198a1", "accent": "#d29922", "line": "#3d444d",
             "box": "#151b23", "hub": "#272115"},
}

DOMAINS = [
    ("Payments & fintech", "Paytm · Dineout · Qenta"),
    ("Responsible gold", "due diligence · provenance"),
    ("Digital identity", "verification orchestration"),
    ("Entrepreneurship", "Deccan Foods · growth"),
]
HUB = ("Evidence & auditability", "every decision carries its evidence;", "every state change leaves a trail")
PROJECTS = [
    ("evidence-review-engine", "explainable due-diligence scoring"),
    ("payments-reliability-lab", "idempotency · webhooks · reconciliation"),
    ("operon", "human-approved job applications"),
]

W, H = 900, 330
FONT = "font-family=\"-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif\""


def box(x: int, y: int, w: int, h: int, fill: str, stroke: str, title: str, sub: str,
        c: dict[str, str], bold_color: str | None = None) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}"/>'
        f'<text x="{x + 14}" y="{y + 24}" font-size="14" font-weight="600" '
        f'fill="{bold_color or c["text"]}">{escape(title)}</text>'
        f'<text x="{x + 14}" y="{y + 43}" font-size="12" fill="{c["muted"]}">{escape(sub)}</text>'
    )


def render(c: dict[str, str]) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-labelledby="t d" {FONT}>',
        "<title id=\"t\">Domains to theme to projects</title>",
        "<desc id=\"d\">Four domains (payments and fintech, responsible gold, digital identity, "
        "entrepreneurship) connect to one theme, evidence and auditability, which connects to three "
        "projects: evidence-review-engine, payments-reliability-lab and operon.</desc>",
        f'<text x="20" y="22" font-size="11" letter-spacing="1.5" fill="{c["muted"]}">WHERE I HAVE WORKED</text>',
        f'<text x="{W - 280}" y="22" font-size="11" letter-spacing="1.5" fill="{c["muted"]}">WHAT I HAVE BUILT</text>',
    ]
    left_x, left_w, row_h, gap, top = 20, 230, 56, 18, 40
    hub_x, hub_y, hub_w, hub_h = 330, 118, 250, 96
    right_x, right_w = W - 280, 260

    # connectors first so boxes paint over line ends
    for i in range(len(DOMAINS)):
        y = top + i * (row_h + gap) + row_h / 2
        parts.append(f'<path d="M{left_x + left_w} {y} C {left_x + left_w + 50} {y}, {hub_x - 50} '
                     f'{hub_y + hub_h / 2}, {hub_x} {hub_y + hub_h / 2}" fill="none" stroke="{c["line"]}" '
                     'stroke-width="1.5"/>')
    proj_top, proj_gap = 62, 22
    for i in range(len(PROJECTS)):
        y = proj_top + i * (row_h + proj_gap) + row_h / 2
        parts.append(f'<path d="M{hub_x + hub_w} {hub_y + hub_h / 2} C {hub_x + hub_w + 50} '
                     f'{hub_y + hub_h / 2}, {right_x - 50} {y}, {right_x} {y}" fill="none" '
                     f'stroke="{c["accent"]}" stroke-width="1.5"/>')

    for i, (title, sub) in enumerate(DOMAINS):
        parts.append(box(left_x, top + i * (row_h + gap), left_w, row_h, c["box"], c["line"], title, sub, c))

    parts.append(f'<rect x="{hub_x}" y="{hub_y}" width="{hub_w}" height="{hub_h}" rx="12" '
                 f'fill="{c["hub"]}" stroke="{c["accent"]}" stroke-width="1.5"/>')
    parts.append(f'<text x="{hub_x + hub_w / 2}" y="{hub_y + 36}" text-anchor="middle" font-size="16" '
                 f'font-weight="700" fill="{c["text"]}">{escape(HUB[0])}</text>')
    for j, line in enumerate(HUB[1:]):
        parts.append(f'<text x="{hub_x + hub_w / 2}" y="{hub_y + 60 + j * 17}" text-anchor="middle" '
                     f'font-size="12" fill="{c["muted"]}">{escape(line)}</text>')

    for i, (title, sub) in enumerate(PROJECTS):
        parts.append(box(right_x, proj_top + i * (row_h + proj_gap), right_w, row_h, c["box"],
                         c["accent"], title, sub, c, bold_color=c["accent"]))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, colours in THEMES.items():
        (here / f"domain-map-{name}.svg").write_text(render(colours), encoding="utf-8")
        print(f"wrote domain-map-{name}.svg")
