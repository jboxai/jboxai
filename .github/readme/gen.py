#!/usr/bin/env python3
"""Generate cream-themed README section SVGs matching jboxai.com."""
import os, textwrap, html

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

W = 1200
BG, CARD, BORDER = "#fcfaf1", "#ffffff", "#e2ddd5"
INK, MUTED, SEC = "#110c09", "#5a544e", "#f4f0e5"
MINT, MINT_SOFT, GREEN = "#7fdddd", "#d1f7f7", "#3aa66b"
SERIF = "Georgia, 'Times New Roman', Times, serif"
SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

def esc(s): return html.escape(s, quote=True)

def svg(name, h, body):
    doc = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img">
<rect width="{W}" height="{h}" fill="{BG}"/>
{body}
</svg>'''
    with open(os.path.join(OUT, name), "w") as f: f.write(doc)
    print("wrote", name, h)

def t(x, y, s, size=15, fill=INK, fam=SANS, weight="400", anchor="start", ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{esc(s)}</text>')

def label(x, y, s, fill=MUTED, anchor="start"):
    return t(x, y, s.upper(), 11, fill, MONO, "500", anchor, ls=2.4)

def h2(x, y, s, size=42, fill=INK, anchor="start"):
    return t(x, y, s, size, fill, SERIF, "400", anchor, ls=-0.5)

def wrap(x, y, s, width_px, size=15, fill=INK, fam=SANS, lh=None, weight="400", anchor="start"):
    lh = lh or round(size * 1.55)
    cw = size * (0.5 if fam == SERIF else 0.53)
    lines = textwrap.wrap(s, max(8, int(width_px / cw)))
    return "\n".join(t(x, y + i * lh, l, size, fill, fam, weight, anchor) for i, l in enumerate(lines)), len(lines) * lh

def rect(x, y, w, h, fill=CARD, stroke=BORDER, sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def button(x, y, w, h, s, dark=True):
    fill, fg, stroke = (INK, BG, INK) if dark else (CARD, INK, INK)
    return (rect(x, y, w, h, fill, stroke) +
            t(x + w / 2, y + h / 2 + 5, s + "  ↗", 14, fg, SANS, "500", "middle"))

def check(x, y):
    return (f'<rect x="{x}" y="{y}" width="14" height="14" fill="{MINT_SOFT}"/>'
            f'<path d="M{x+3.5} {y+7.5} L{x+6} {y+10} L{x+10.5} {y+4.5}" stroke="{GREEN}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def sq(x, y, c=INK, s=6): return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{c}"/>'

def rule(y, x1=0, x2=W): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{BORDER}"/>'

# ------------------------------------------------------------------ HERO
def hero():
    b = []
    b.append(label(60, 78, "From brief to working product"))
    for i, l in enumerate(["Describe", "it. Jbox", "builds it."]):
        b.append(t(58, 168 + i * 74, l, 76, INK, SERIF, "400", ls=-2))
    bullets = ["Plain-language brief in, working product out",
               "Every screen, role and decision mapped first",
               "Build without context loss or tech debt",
               "Hosted and live, not a prototype"]
    for i, s in enumerate(bullets):
        y = 372 + i * 32
        b.append(sq(60, y - 10, INK, 6)); b.append(t(78, y, s, 16, INK))
    b.append(button(60, 520, 190, 50, "Get started free"))
    b.append(t(268, 545, "50 credits · no card", 12, MUTED, MONO, "500", ls=1))
    # right card: flow map
    cx, cy, cw, ch = 620, 100, 520, 470
    b.append(rect(cx, cy, cw, ch, CARD, BORDER))
    b.append('<defs><linearGradient id="mint" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{MINT}" stop-opacity="0.45"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></linearGradient>'
             f'<pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="{BORDER}" stroke-width="0.6"/></pattern></defs>')
    b.append(f'<rect x="{cx+1}" y="{cy+1}" width="{cw-2}" height="{ch-92}" fill="url(#grid)"/>')
    b.append(f'<rect x="{cx+1}" y="{cy+1}" width="{cw-2}" height="120" fill="url(#mint)"/>')
    # nodes
    nodes = [(cx+40, cy+60, 130, "Brief", True),
             (cx+220, cy+60, 110, "Admin", False), (cx+220, cy+130, 110, "Clinician", False), (cx+220, cy+200, 110, "Patient", False),
             (cx+370, cy+60, 120, "Dashboard", False), (cx+370, cy+130, 120, "Booking", False), (cx+370, cy+200, 120, "Billing", False), (cx+370, cy+270, 120, "Records", False)]
    def mid(n): return (n[0] + n[2], n[1] + 16)
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 6), (2, 5), (2, 7), (3, 5)]
    for a, c in edges:
        x1, y1 = mid(nodes[a]); x2, y2 = nodes[c][0], nodes[c][1] + 16
        b.append(f'<path d="M{x1} {y1} C{x1+40} {y1} {x2-40} {y2} {x2} {y2}" stroke="{INK}" stroke-opacity="0.35" stroke-width="1.2" fill="none"/>')
    for x, y, w, s, dark in nodes:
        b.append(rect(x, y, w, 32, INK if dark else CARD, INK if dark else BORDER))
        b.append(t(x + 12, y + 21, s, 13, BG if dark else INK, SANS, "500"))
        if not dark: b.append(sq(x + w - 14, y + 13, MINT, 6))
    b.append(t(cx + 24, cy + 350, "jbox", 22, INK, SERIF, "400", extra='font-style="italic"'))
    b.append(f'<circle cx="{cx+72}" cy="{cy+347}" r="3" fill="{MINT}"/>')
    b.append(rule(cy + ch - 92, cx + 1, cx + cw - 1))
    q, _ = wrap(cx + 24, cy + ch - 56, "A clinic platform for patient care: admin, clinician and patient roles, appointment booking and billing dashboard.", cw - 48, 13, MUTED)
    b.append(q)
    svg("hero.svg", 620, "\n".join(b))

# ------------------------------------------------------------------ HOW IT WORKS
def how():
    b = [label(60, 70, "How it works"), h2(60, 122, "Catch what is missing before it becomes rework.")]
    s, _ = wrap(60, 160, "See every role, screen, decision and handoff together. Review the full product before development starts.", 700, 16, MUTED)
    b.append(s)
    steps = [("01", "Describe the product", "Type what you want to build in plain language, or paste in a brief."),
             ("02", "Review every path", "Check screens, roles and decisions together before the build starts."),
             ("03", "Ship the product", "Open the connected product, test it and publish.")]
    cw, gap, y = 346, 21, 230
    for i, (n, title, desc) in enumerate(steps):
        x = 60 + i * (cw + gap)
        b.append(rect(x, y, cw, 190))
        b.append(t(x + 24, y + 40, n, 12, MUTED, MONO, "500", ls=2))
        b.append(sq(x + cw - 34, y + 28, MINT, 8))
        b.append(t(x + 24, y + 86, title, 24, INK, SERIF))
        d, _ = wrap(x + 24, y + 122, desc, cw - 48, 14, MUTED)
        b.append(d)
    svg("how-it-works.svg", 470, "\n".join(b))

# ------------------------------------------------------------------ STACK
def stack():
    b = [label(60, 60, "The working build uses")]
    items = ["Next.js", "Supabase", "GitHub", "Jbox Hosting"]
    x = 60
    for s in items:
        w = 40 + int(len(s) * 10.5)
        b.append(rect(x, 84, w, 48, CARD, BORDER))
        b.append(sq(x + 16, 105, MINT, 6)); b.append(t(x + 32, 113, s, 16, INK, SANS, "500"))
        x += w + 14
    svg("stack.svg", 170, "\n".join(b))

# ------------------------------------------------------------------ BUILDS
def builds():
    b = [label(60, 70, "Selected builds"), h2(60, 122, "We built Jbox with Jbox.")]
    b.append(t(60, 158, "Here are some other shipped products.", 16, MUTED))
    items = [("DermaLens", "Instant AI skin check"), ("Redmond Harvey", "Editorial commerce"), ("Anantrix", "Vedic astrology"),
             ("EOR", "Employer of record"), ("Project Resist", "Rights & campaigns"), ("GRE Capital", "UK real estate lending")]
    cw, ch, gap = 346, 120, 21
    for i, (n, c) in enumerate(items):
        x = 60 + (i % 3) * (cw + gap); y = 210 + (i // 3) * (ch + gap)
        b.append(rect(x, y, cw, ch))
        b.append(t(x + 24, y + 30, f"0{i+1}", 11, MUTED, MONO, "500", ls=2))
        b.append(t(x + 24, y + 68, n, 24, INK, SERIF))
        b.append(t(x + 24, y + 96, c.upper(), 11, MUTED, MONO, "500", ls=2))
        b.append(t(x + cw - 24, y + 30, "↗", 14, INK, SANS, "400", "end"))
    svg("builds.svg", 520, "\n".join(b))

# ------------------------------------------------------------------ TESTIMONIALS
def testimonials():
    b = [label(60, 70, "What builders say"), h2(60, 122, "Build with less guesswork.")]
    # G2 badge
    b.append(rect(880, 82, 260, 56, CARD, BORDER))
    b.append(t(902, 120, "4.6", 30, INK, SERIF)); b.append(t(952, 120, "/ 5", 14, MUTED))
    b.append(t(1120, 116, "G2", 16, INK, SANS, "700", "end"))
    for i in range(5):
        b.append(f'<path transform="translate({1000+i*14} {102}) scale(0.5)" d="M12 2l3 6.5 7 .8-5.2 4.8 1.4 7L12 17.5 5.8 21l1.4-7L2 9.3l7-.8z" fill="{MINT}"/>')
    quotes = [("It finally builds the system, not just screens. Seeing the whole product as a connected map changed how we ship. We stopped guessing about edge cases.", "A", "Angel Bacareza", "Product Manager at Fronted · Global"),
              ("We could talk through the product with the whole team before anyone opened a code editor. The missing paths became obvious much earlier.", "T", "Tiaan Alberts", "Chartered Quantity Surveyor at Turner & Townsend alinea · United Kingdom"),
              ("Jbox turns app ideas into a fast MVP prototype on the first try.", "A", "Asbjørn Rørvik", "Full Stack Developer · CTO / Co-Founder at Supportify · Norway")]
    cw, ch, gap, y = 346, 300, 21, 180
    for i, (q, ini, name, role) in enumerate(quotes):
        x = 60 + i * (cw + gap)
        b.append(rect(x, y, cw, ch))
        b.append(t(x + 24, y + 34, f"0{i+1}", 11, MUTED, MONO, "500", ls=2))
        b.append(t(x + 22, y + 92, "“", 54, MINT, SERIF))
        qq, _ = wrap(x + 24, y + 116, q, cw - 48, 15, INK, SERIF, 24)
        b.append(qq)
        by = y + ch - 62
        b.append(f'<circle cx="{x+40}" cy="{by+14}" r="16" fill="{SEC}" stroke="{BORDER}"/>')
        b.append(t(x + 40, by + 19, ini, 13, INK, SANS, "600", "middle"))
        b.append(t(x + 66, by + 10, name, 14, INK, SANS, "600"))
        rr, _ = wrap(x + 66, by + 28, role, cw - 100, 11, MUTED, SANS, 15)
        b.append(rr)
    svg("testimonials.svg", 520, "\n".join(b))

# ------------------------------------------------------------------ PRICING
def pricing():
    b = [label(60, 70, "Simple pricing"), h2(60, 122, "Your first build is on us.")]
    s, _ = wrap(820, 100, "50 credits are included. Add 100 more for $20 whenever you need them.", 330, 15, MUTED)
    b.append(s)
    # ---- Pro card
    x, y, cw, ch = 60, 180, 530, 470
    b.append(rect(x, y, cw, ch))
    b.append(sq(x + 24, y + 26, MINT, 6)); b.append(label(x + 40, y + 32, "Self-serve"))
    b.append(t(x + 40, y + 60, "Jbox Pro", 20, INK, SERIF))
    b.append(t(x + cw - 24, y + 48, "For individuals and small teams", 12, MUTED, SANS, "400", "end"))
    b.append(rule(y + 84, x + 1, x + cw - 1))
    b.append(t(x + 30, y + 160, "$0", 64, INK, SERIF))
    b.append(t(x + 112, y + 152, "to start", 14, MUTED))
    b.append(t(x + 30, y + 192, "50 credits included", 14, INK, SANS, "500"))
    bx, by, bw, bh = x + 250, y + 108, 256, 106
    b.append(rect(bx, by, bw, bh, MINT_SOFT, "none"))
    b.append(label(bx + 20, by + 30, "When you need more"))
    b.append(t(bx + 20, by + 62, "$20 / 100 additional", 19, INK, SERIF))
    b.append(t(bx + 20, by + 88, "credits", 19, INK, SERIF))
    b.append(rule(y + 238, x + 1, x + cw - 1))
    feats = ["No subscription", "No credit card to start", "Unlimited flow generation", "Export to production code"]
    gx, gy, gw, gh = x + 24, y + 262, (cw - 48) // 2, 48
    b.append(rect(gx, gy, gw * 2, gh * 2, CARD, BORDER))
    b.append(f'<line x1="{gx+gw}" y1="{gy}" x2="{gx+gw}" y2="{gy+gh*2}" stroke="{BORDER}"/>')
    b.append(f'<line x1="{gx}" y1="{gy+gh}" x2="{gx+gw*2}" y2="{gy+gh}" stroke="{BORDER}"/>')
    for i, f in enumerate(feats):
        fx = gx + (i % 2) * gw; fy = gy + (i // 2) * gh
        b.append(check(fx + 18, fy + 17)); b.append(t(fx + 42, fy + 29, f, 13, INK))
    b.append(button(x + 24, y + ch - 76, cw - 48, 48, "Get started free", True))
    # ---- Enterprise card
    x = 610
    b.append(rect(x, y, cw, ch))
    b.append(label(x + 24, y + 32, "For teams"))
    b.append(t(x + 24, y + 60, "Enterprise", 20, INK, SERIF))
    b.append(t(x + 24, y + 78, "For growing teams", 12, MUTED))
    b.append(rule(y + 84, x + 1, x + cw - 1))
    b.append(t(x + 24, y + 160, "Custom", 56, INK, SERIF))
    b.append(t(x + 24, y + 194, "Credits, controls, and support sized around your organization.", 13, MUTED))
    b.append(rule(y + 238, x + 1, x + cw - 1))
    feats = ["Custom credit allocation", "Team controls and SSO", "White-glove onboarding", "Dedicated account support"]
    for i, f in enumerate(feats):
        fy = y + 262 + i * 26
        b.append(check(x + 24, fy)); b.append(t(x + 48, fy + 12, f, 13, INK))
    b.append(button(x + 24, y + ch - 76, cw - 48, 48, "Talk to our team", False))
    b.append(t(x + cw / 2, y + ch - 12, "Reply within 24 hours", 11, MUTED, SANS, "400", "middle"))
    svg("pricing.svg", 700, "\n".join(b))

# ------------------------------------------------------------------ SECTION HEADERS
def header(name, lab, head, sub):
    b = [label(60, 60, lab), h2(60, 112, head)]
    if sub: b.append(t(60, 148, sub, 15, MUTED))
    svg(name, 180, "\n".join(b))

# ------------------------------------------------------------------ CTA
def cta():
    h = 400
    b = [f'<rect width="{W}" height="{h}" fill="{INK}"/>']
    b.append(f'<pattern id="g2" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="{BG}" stroke-opacity="0.06" stroke-width="0.6"/></pattern>')
    b.append(f'<rect width="{W}" height="{h}" fill="url(#g2)"/>')
    b.append(label(60, 80, "Ready to build", MINT))
    for i, l in enumerate(["Ready to build", "a complete product", "in one tool?"]):
        b.append(t(58, 150 + i * 58, l, 54, BG, SERIF, "400", ls=-1))
    b.append(t(720, 132, "Join the builders who ship", 20, BG, SERIF))
    b.append(t(720, 160, "faster with total clarity.", 20, BG, SERIF))
    s, _ = wrap(720, 200, "Jbox turns a product brief into a working web app with connected screens, roles, data, authentication, and hosting.", 420, 14, "#b8b2ab", SANS, 22)
    b.append(s)
    b.append(rect(720, 286, 190, 48, BG, BG)); b.append(t(815, 315, "Get started free  ↗", 14, INK, SANS, "500", "middle"))
    b.append(rect(926, 286, 214, 48, "none", "#b8b2ab")); b.append(t(1033, 315, "Join us on Discord", 14, BG, SANS, "500", "middle"))
    b.append(t(60, 360, "jbox", 22, BG, SERIF, "400", extra='font-style="italic"'))
    b.append(f'<circle cx="{108}" cy="{357}" r="3" fill="{MINT}"/>')
    b.append(t(1140, 360, "jboxai.com", 12, "#b8b2ab", MONO, "500", "end", ls=1))
    svg("cta.svg", h, "\n".join(b))

hero(); how(); stack(); builds(); testimonials(); pricing()
header("faq-header.svg", "Need to know", "Questions, answered.", "What Jbox builds, how hosting works, and what you pay. No fine print.")
header("team-header.svg", "The people behind Jbox", "The team behind the product.", "A small team building the product we wanted to use ourselves.")
cta()

# ------------------------------------------------------------------ VIDEO
def video():
    import base64
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb-1200.png")
    if not os.path.exists(src): src = os.path.join(OUT, "thumb-1200.png")
    data = base64.b64encode(open(src, "rb").read()).decode()
    h = 674
    b = [f'<image href="data:image/png;base64,{data}" x="0" y="0" width="{W}" height="{h}" preserveAspectRatio="xMidYMid slice"/>']
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" fill="none" stroke="{BORDER}"/>')
    # play button
    cx, cy = W / 2, 196
    b.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="{INK}" fill-opacity="0.08"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="{INK}"/>')
    b.append(f'<path d="M{cx-12} {cy-18} L{cx+20} {cy} L{cx-12} {cy+18} Z" fill="{BG}"/>')
    b.append(t(cx, cy + 80, "Watch: prompt to product", 15, INK, SANS, "500", "middle"))
    # bottom-left tag
    b.append(rect(24, h - 60, 230, 36, INK, INK))
    b.append(f'<circle cx="44" cy="{h-42}" r="4" fill="{MINT}"/>')
    b.append(t(58, h - 37, "JBOX DEMO · MP4", 11, BG, MONO, "500", ls=2))
    b.append(t(W - 24, h - 37, "jboxai.com", 12, MUTED, MONO, "500", "end", ls=1))
    svg("video.svg", h, "\n".join(b))

video()
