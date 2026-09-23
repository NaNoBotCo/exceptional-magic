#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site.py — the pages, built from build/facts.json and the figures beside it.

    SITE_URL=https://nanobotco.github.io/exceptional-magic python3 tools/site.py
"""
from __future__ import annotations

import html
import json
import os
import shutil
from datetime import date
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fleet                                   # noqa: E402
from css import CSS                            # noqa: E402
from sources import PAPER, SOURCES, BY_ID, url as src_url, cite_html   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SITE = BUILD / "site"
IMG = BUILD / "img"
SITE_URL = os.environ.get("SITE_URL", "https://nanobotco.github.io/exceptional-magic").rstrip("/")
tail = SITE_URL.split("//", 1)[-1]
BASE = "/" + tail.split("/", 1)[1] + "/" if "/" in tail else "/"
SELF = "exceptional-magic"
NAME = "Exceptional Magic"
TAG = ("Eight ways to multiply, and where they get you: the octonions, triality, the magic "
       "square and E8, drawn from the arithmetic and told plain.")
CREDIT = "Nan · hongdam.net · CC BY 4.0"
TODAY = date.today().isoformat()
F = json.loads((BUILD / "facts.json").read_text(encoding="utf-8"))
FLEET = fleet.load(ROOT / "data" / "fleet.json")

E = html.escape

NAV = [("numbers/", "Numbers"), ("wheel/", "Wheel"), ("triality/", "Triality"),
       ("square/", "Square"), ("e8/", "E8"), ("physics/", "Physics"),
       ("checks/", "Checks"), ("gallery/", "Gallery"), ("credit/", "Credit")]

ALT = {
    "hero.jpg": ("Two hundred and forty dots in eight rings, every dot joined to fifty-six others "
                 "by faint lines, the whole thing turning about a dark centre with thirty-fold "
                 "symmetry. The dots come in three colours: amber, teal and rose."),
    "ladder.svg": ("A table of five algebras against four laws. The reals and the complex numbers "
                   "keep every law; the quaternions lose commutativity; the octonions lose "
                   "associativity; the sedenions lose the norm law too."),
    "fano.svg": ("Seven labelled circles at the corners, edge midpoints and centre of a triangle, "
                 "joined by three sides, three medians and one inner circle, with arrows around "
                 "each line."),
    "tables.svg": ("Four coloured grids, two by two up to eight by eight, one for each algebra's "
                   "multiplication table."),
    "three-eights.svg": ("Twenty-four dots in three colours with three-fold symmetry: a third of a "
                         "turn carries each colour onto the next."),
    "dynkin.svg": ("A three-pointed star with a rotation arrow, beside the three exceptional "
                   "diagrams drawn as lines of nodes with one node branching off."),
    "rotation.svg": ("A circle with three spokes 120 degrees apart, labelled I, II and III, beside "
                     "the rotation matrix that carries one spoke to the next."),
    "magic.svg": ("A seven by seven grid of Lie algebras, each box carrying a name, a dimension and "
                  "the arithmetic behind it. E8 at 248 sits in the corner."),
    "eigen.svg": ("Six stacked bars, each split into a fixed part and two equal moving parts."),
    "su3d.svg": ("Four boxes: su(2), su(3), sp(3) and f4, each showing its triality algebra plus "
                 "three copies of a division algebra."),
    "e8-z3.svg": ("The E8 shadow with each root coloured by which of three eigenspaces it falls in: "
                  "84 amber, 78 teal, 78 rose."),
    "e8-two.svg": ("The E8 shadow with 112 roots in teal and 128 in rose."),
    "e8.svg": "The E8 root system in the Coxeter plane: 240 dots on eight rings of thirty.",
    "e7.svg": "The E7 root system: 126 dots on seven rings of eighteen.",
    "e6.svg": "The E6 root system: 72 dots, twelve-fold.",
    "f4.svg": "The F4 root system: 48 dots on four rings of twelve.",
    "d4.svg": "The D4 root system: 24 dots, six-fold.",
    "g2.svg": "The G2 root system: 12 dots, six long and six short.",
    "card.jpg": "The site's name beside the E8 shadow.",
}


# --------------------------------------------------------------------- helpers

def rel():
    return BASE


def fig(name, caption, cls="", w=0):
    alt = ALT.get(name, caption)
    size = f' width="{w}"' if w else ""
    return (f'<figure class="fig {cls}"><img src="{BASE}img/{name}" alt="{E(alt)}" '
            f'loading="lazy" decoding="async"{size}>'
            f'<figcaption>{caption}</figcaption></figure>')


def cite(*ids):
    return cite_html(ids, E)


def paper_cite(section=""):
    where = f" §{section}" if section else ""
    return (f'<a class="cite" href="{PAPER["url"]}" rel="noopener">Lisi 2026{E(where)}</a>')


def eq(body, note=""):
    n = f'<div class="small mute" style="margin-top:.35rem">{note}</div>' if note else ""
    return f'<div class="eq">{body}{n}</div>'


def credit_block(short=False):
    p = PAPER
    body = (f'<h3>The paper this reads</h3>'
            f'<p><b>{E(p["authors"])}</b>, <a href="{p["url"]}" rel="noopener">'
            f'<i>{E(p["title"])}</i></a>, {E(p["where"])}. '
            f'<a href="{p["html"]}" rel="noopener">HTML</a> · '
            f'<a href="{p["pdf"]}" rel="noopener">PDF</a> · '
            f'<a href="{p["licence_url"]}" rel="noopener">{E(p["licence"])}</a>.</p>')
    if not short:
        body += ('<p class="small">That licence allows no derivatives, so nothing here is a copy '
                 'of it. The mathematics is nobody\'s property: every table, picture and number on '
                 'this site is computed in this repository from the definitions, and the paper is '
                 'named wherever it is the reason a thing is here. Read it; it is better than this '
                 'page.</p>')
    return f'<div class="credit">{body}</div>'


def page(title, body, path, desc="", cur="", scripts=(), jsonld=None):
    cur_attr = ' aria-current="page"'
    nav = "".join(
        f'<a href="{BASE}{h}"{cur_attr if cur == h else ""}>{E(t)}</a>' for h, t in NAV)
    js = "".join(f'<script src="{BASE}js/{s}" defer></script>' for s in scripts)
    ld = (f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else "")
    canon = SITE_URL + "/" + path if path else SITE_URL + "/"
    head_title = title if path else f"{NAME} — {TAG.split(':')[0]}"
    out = f"""<!doctype html><html lang="en" translate="no" class="notranslate"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(head_title)}</title>
<meta name="description" content="{E(desc or TAG)}">
<link rel="canonical" href="{E(canon)}">
<meta property="og:title" content="{E(head_title)}">
<meta property="og:description" content="{E(desc or TAG)}">
<meta property="og:image" content="{SITE_URL}/img/card.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{BASE}icon.svg" type="image/svg+xml">
<style>{CSS}</style>{ld}
<meta name="google" content="notranslate">
<meta name="robots" content="notranslate">
<script>if(/[.]translate[.]goog$/.test(location.hostname))location.replace("https://"+location.hostname.slice(0,-15).replace(/--/g,"~").replace(/-/g,".").replace(/~/g,"-")+location.pathname+location.search.replace(/([?&])_x_tr_[^&]*/g,"$1").replace(/[?&]+$/,"").replace(/[?]&+/,"?")+location.hash)</script>
</head>
<body data-base="{BASE}">
<a class="sr" href="#main">Skip to the page</a>
<header class="top"><div class="in">
<a class="brand" href="{BASE}"><i></i>Exceptional <b>Magic</b></a>
<nav aria-label="Sections">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer class="bot"><div class="in">
<p><b>{E(NAME)}</b> — {E(TAG)}</p>
<p>Text and figures {E(CREDIT)}. Code MIT. Built {E(TODAY)}.
Every figure was computed by <code>tools/figures.py</code> in
<a href="https://github.com/NaNoBotCo/{SELF}">the repository</a>; none is traced from anyone's drawing.</p>
<p>Reading <a href="{PAPER['url']}" rel="noopener">{E(PAPER['authors'])}, {E(PAPER['title'])}</a>,
{E(PAPER['where'])}, used under <a href="{PAPER['licence_url']}" rel="noopener">{E(PAPER['licence'])}</a>
— quoted from, not reproduced.</p>
{fleet.row_html(SELF, roster=FLEET)}
{fleet.support_html(self_id="exceptional-magic", roster=FLEET)}
{fleet.maker_html(roster=FLEET)}
</div></footer>{js}
<script src="{BASE}js/nav.js" defer></script>
</body></html>"""
    write(SITE / path / "index.html" if path else SITE / "index.html", out)
    return out


def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# ----------------------------------------------------------------------- pages

def home():
    s = F["systems"]
    surv = {r["algebra"]: r for r in F["survey"]}
    b = [f"""<h1><span class="kind">Eight ways to multiply</span>Exceptional<br>Magic</h1>
<p class="lede">Numbers you can multiply <i>and divide</i> come in four sizes: one, two, four,
eight. That is the whole list, and it has been the whole list since 1898. Every time the size
doubles you give up a law you were counting on. Follow the last one far enough and you arrive
at the biggest exceptional object in mathematics — {s['E8']['dim']} dimensions, {s['E8']['roots']}
directions, and a three-way symmetry that some physicists think is the reason there are three
generations of matter.</p>

<div class="hero"><img src="{BASE}img/hero.jpg" alt="{E(ALT['hero.jpg'])}" width="1400" height="1400"></div>
<p class="small mute">E8's {s['E8']['roots']} roots, flattened onto the one plane where the whole
thing turns like a wheel — {s['E8']['h']} clicks to the full turn, {F['hero_edges']:,} lines
joining every pair of roots sixty degrees apart. The three colours are the three pieces triality
cuts it into: {F['e8_z3']['counts'][0]} that stand still, {F['e8_z3']['counts'][1]} that turn one
way, {F['e8_z3']['counts'][2]} that turn the other. Drawn here from the coordinates, not traced.</p>

{credit_block()}

<h2>The short version</h2>
<div class="prose">
<p>A <strong>division algebra</strong> is a number system where you can undo a multiplication —
every nonzero thing has a reciprocal. There are four, of dimension 1, 2, 4 and 8: the reals,
the complex numbers, the quaternions, the octonions.</p>
<p>Each one is built by doubling the one before it, and each doubling takes something away.
Going to the quaternions, multiplication stops caring about order. Going to the octonions, it
stops caring about grouping. Go one more rung and it stops being a division algebra at all —
two things that are not zero multiply to zero. Sixteen is where the wheels come off, and the
{surv['O']['trials']:,} random products measured on <a href="{BASE}numbers/">the numbers page</a>
show exactly where each law quits.</p>
<p>In eight dimensions something rare happens. Vectors have eight components. Spinors — the
things that describe matter, and that turn only halfway when you turn the world all the way —
also have eight. Two kinds of them, in fact. So there are three different eight-dimensional
objects sitting in the same room, and a symmetry called <strong>triality</strong> shuffles all
three like a three-legged stool. That symmetry is the octonion product wearing a different hat.</p>
<p>Stack two of these algebras and you get the <strong>magic square</strong>: a seven-by-seven
chart whose boxes are Lie algebras, filled by one arithmetic rule, with every exceptional
algebra in it. Octonions times octonions is E8.</p>
</div>

<h2>Where to start</h2>
<div class="grid">""",
         card("numbers/", "Numbers", "1, 2, 4, 8 — and the price of each doubling",
              "Four algebras, the ladder that builds them, and a multiplier you can break "
              "associativity with."),
         card("wheel/", "Wheel", "Seven posts, seven wires",
              "The octonion table is a seven-point plane. Click two units and watch the line "
              "light up."),
         card("triality/", "Triality", "The same thing, three ways",
              "One cyclic form, three arguments, and a symmetry that shuffles them. Checked on "
              f"{F['triality_cyclic']['trials']:,} random triples."),
         card("square/", "Square", "Forty-nine boxes, one formula",
              "The Freudenthal–Tits magic square, dimensions computed rather than quoted."),
         card("e8/", "E8", f"{s['E8']['roots']} roots, {s['E8']['dim']} dimensions",
              "Every exceptional root system, turned live in your browser, cut three ways and "
              "two ways."),
         card("physics/", "Physics", "What it is all supposed to be for",
              "One generation in e6, three in e8 — the proposal, and the objections to it, "
              "side by side."),
         "</div>",
         f"""<h2>How to read this site</h2>
<div class="prose">
<p>The mathematics on these pages is old, settled and not in dispute: division algebras,
triality, the magic square, E8's root system. Where a page turns to particle physics it says
so out loud, names whose proposal it is, and lists the objections in the same breath
{cite('distler2010')}.</p>
<p>Nothing is asserted here that this repository does not compute. Every number in the text is
read out of <code>build/facts.json</code> at build time, and
<a href="{BASE}checks/">{F['checks']['total']} checks</a> run before the site will publish —
{F['checks']['failures']} failing as of {TODAY}.</p>
</div>"""]
    return page("", "".join(b), "", TAG, "", scripts=())


def card(href, title, kicker, text):
    return (f'<a class="card" href="{BASE}{href}"><h3>{E(title)}</h3>'
            f'<p class="mute small">{E(kicker)}</p><p>{E(text)}</p></a>')


def numbers():
    surv = {r["algebra"]: r for r in F["survey"]}
    zd = F["zero_divisor_example"]
    b = [f"""<h1><span class="kind">One, two, four, eight</span>Numbers</h1>
<p class="lede">Four number systems let you divide. Nobody is going to find a fifth. Hurwitz
shut that door in 1898, and the reason is the one law in the table below that the octonions
still keep and the next rung does not.</p>

{fig("ladder.svg", f"Measured, not quoted: {surv['O']['trials']:,} random triples per algebra, "
     "multiplied out in exact integer arithmetic by <code>tools/algebra.py</code>. A cell says "
     "<i>holds</i> only when every trial held.")}

<h2>The ladder</h2>
<div class="prose">
<p>Each algebra is the one before it, doubled. Take a pair of quaternions and call the pair an
octonion; the rule for multiplying pairs is one line, and it is the same line at every rung:</p>
{eq("(p, q)(r, s) = ( pr − s̃q ,&nbsp; sp + qr̃ )",
    "the tilde is conjugation — flip the sign on everything but the real part. "
    "This is the Cayley–Dickson construction, and tools/algebra.py runs it verbatim.")}
<p>Start with the reals, turn the crank, and you get the complex numbers. Turn it again:
quaternions. Again: octonions. Again: sedenions, sixteen of them, and the bottom falls out.</p>

<h3>What each turn costs</h3>
<ul class="prose">
<li><b>1 → 2.</b> You lose the ordering. There is no saying whether <code>i</code> is bigger or
smaller than zero.</li>
<li><b>2 → 4.</b> You lose commuting. <code>e1 e2 = e3</code>, but <code>e2 e1 = −e3</code>.
Order of operations now matters, which is exactly why quaternions describe rotations —
rotations do not commute either.</li>
<li><b>4 → 8.</b> You lose associating. <code>(ab)c</code> and <code>a(bc)</code> part company.
What survives is the weaker <strong>alternative</strong> law: any two octonions still generate
an associative patch, so <code>(aa)b = a(ab)</code> always. That is enough structure to build
on, and it is the last rung where you get it.</li>
<li><b>8 → 16.</b> You lose the norm law, <code>|ab| = |a||b|</code> — and with it, division.
Two nonzero sedenions can multiply to zero. There are {F['zero_divisor_pairs']:,} such pairs of
basis planes; the first one the search finds is
<code>(e{zd[0][0]} + e{zd[0][1]})(e{zd[1][0]} + e{zd[1][1]}) = 0</code>.</li>
</ul>
<p>So the norm law, <code>|ab| = |a||b|</code>, is the thing that picks out 1, 2, 4 and 8 and
nothing else. It is also, read a different way, the triality form that runs the rest of this
site.</p>
</div>

<h2>Break it yourself</h2>
<div class="tool" id="mul">
<h3>The multiplier</h3>
<p class="small mute">Pick three basis units and watch the laws hold or fail. Everything is
exact — these are integers, not decimals.</p>
<div class="row"><label>algebra</label>
<span class="units">
<button data-alg="C" aria-pressed="false">ℂ</button>
<button data-alg="H" aria-pressed="false">ℍ</button>
<button data-alg="O" aria-pressed="true">𝕆</button>
<button data-alg="O'" aria-pressed="false">𝕆′ split</button>
</span></div>
<div class="row"><label>a</label><span class="units" id="ua"></span></div>
<div class="row"><label>b</label><span class="units b" id="ub"></span></div>
<div class="row"><label>c</label><span class="units" id="uc"></span></div>
<div class="row"><button class="go" id="roll">roll three</button></div>
<div class="out" id="mulout"></div>
</div>

<h2>The split cousins</h2>
<div class="prose">
<p>Beside each division algebra sits a <strong>split</strong> one of the same size, written
ℂ′, ℍ′, 𝕆′. Same construction, one sign flipped, so the length of a thing can come out
negative. They are not division algebras — some nonzero elements have length zero and cannot be
divided by — but they multiply the same way, and they are how the same Lie algebra shows up in
several real forms {paper_cite("2")}. Physics cares about that, because spacetime has a minus
sign in it too.</p>
<p>Switch the multiplier above to 𝕆′ and watch <code>|ab| = |a||b|</code> keep holding while
the signs on the diagonal go the other way.</p>
</div>

{fig("tables.svg", "The four tables that run this site. Row <i>a</i>, column <i>b</i>, colour "
     "for which unit the product lands on, dark for a minus sign. The split octonion table is "
     "the same shape with a quarter of it flipped.")}
"""]
    return page("Numbers — one, two, four, eight", "".join(b), "numbers/",
                "The four division algebras, the Cayley-Dickson ladder that builds them, what "
                "each doubling costs, and a multiplier that breaks associativity on demand.",
                "numbers/", scripts=("algebra.js", "multiply.js"))


def wheel():
    lines = F["fano_lines"]
    b = [f"""<h1><span class="kind">Seven posts, seven wires</span>The Wheel</h1>
<p class="lede">The octonion multiplication table looks like sixty-four entries to memorise. It
is not. It is seven lines drawn through seven points, and once you can see the fence you never
need the table again.</p>

<div class="prose">
<p>Take the seven imaginary units, <code>e1</code> through <code>e7</code>. Put them at the
three corners of a triangle, the three midpoints of its sides, and the middle. Draw the three
sides, the three medians, and one circle through the midpoints. That is seven lines. Every line
touches three points; every point sits on three lines. Mathematicians call it the
<strong>Fano plane</strong> — the smallest projective plane there is.</p>
<p>Each line carries an arrow. Go with the arrow and the product is a plus; go against it and
it is a minus:</p>
{eq("e<b>%d</b> · e<b>%d</b> = e<b>%d</b>&nbsp;&nbsp;&nbsp;&nbsp;e<b>%d</b> · e<b>%d</b> = −e<b>%d</b>"
    % (lines[0][0], lines[0][1], lines[0][2], lines[0][1], lines[0][0], lines[0][2]),
    "and every unit squares to −1")}
<p>The seven lines below were not drawn from a picture. <code>tools/algebra.py</code> walks the
table looking for triples where <code>e_a e_b = e_c</code>, <code>e_b e_c = e_a</code> and
<code>e_c e_a = e_b</code>, finds exactly seven, and the drawing is laid out afterwards to
match what it found {paper_cite("2")}.</p>
</div>

<h2>Click two</h2>
<div class="tool">
<canvas id="wheel" width="460" height="460" aria-label="{E(ALT['fano.svg'])}"></canvas>
<div class="out" id="wheelout"></div>
<p class="small mute">The whole octonion table, in one picture you can hold in your head.</p>
</div>

{fig("fano.svg", "The same wheel, drawn at build time. Arrows show which way round each line "
     "multiplies.")}

<h2>The seven lines</h2>
<div class="wrap"><table>
<thead><tr><th>line</th><th>read it</th><th>and backwards</th></tr></thead><tbody>""",
         *[f"<tr><td><code>({a} {c} {d})</code></td>"
           f"<td><code>e{a}e{c} = e{d}</code>, <code>e{c}e{d} = e{a}</code>, "
           f"<code>e{d}e{a} = e{c}</code></td>"
           f"<td><code>e{c}e{a} = −e{d}</code></td></tr>" for a, c, d in lines],
         f"""</tbody></table></div>
<p class="small mute">Seven lines, three units on each, every unit on three lines —
{len(lines)} × 3 = 21 products, and the other forty-two entries in the table follow from the
signs and the unit.</p>

<h2>Why a plane at all</h2>
<div class="prose">
<p>Because the octonions are built by doubling three times, and each doubling adds a new
independent direction: <code>e1</code>, then <code>e2</code>, then <code>e4</code> in the
labelling used here. Everything else is a product of those, and the pattern of which products
give which is exactly the incidence pattern of a plane over the two-element field. Seven
nonzero triples of bits, seven points. The table has to be the Fano plane; there was no room
for it to be anything else.</p>
</div>
"""]
    return page("The Wheel — the octonion table as a seven-point plane", "".join(b), "wheel/",
                "The octonion multiplication table is the Fano plane: seven points, seven lines, "
                "three points to a line. Click two units and read off the product.",
                "wheel/", scripts=("algebra.js", "wheel.js"))


def triality():
    t = F["triality_cyclic"]
    r = F["reflection"]
    d = F["d4_triality_checks"]
    tri = F["tri_dims"]
    b = [f"""<h1><span class="kind">The same thing, three ways</span>Triality</h1>
<p class="lede">In eight dimensions there are three different things with eight components:
vectors, and two kinds of spinor. Triality is the symmetry that shuffles all three and leaves
the arithmetic alone. It exists in eight dimensions and nowhere else.</p>

<div class="prose">
<p>First, the words.</p>
<p>A <strong>vector</strong> is an arrow: turn the world all the way round and an arrow comes
back to itself. A <strong>spinor</strong> is the other kind of thing — turn the world all the
way round and a spinor comes back with a minus sign; it takes two full turns to get home.
Electrons are spinors. In eight dimensions, spinors come in two handednesses, and each one has
eight components, same as the vector.</p>
<p>So you have three eight-dimensional objects that ought to be strangers, and they are not.
There is one function of all three at once:</p>
{eq("T(v, ψ, χ) = ( χ̃ , v ψ )",
    "a real number out of three octonions: multiply two, conjugate the third, take the inner "
    "product. Lisi eq. (3.1).")}
<p>and it does not care which of the three you call which:</p>
{eq("T(v, ψ, χ) = T(ψ, χ, v) = T(χ, v, ψ)",
    f"checked on {t['trials']:,} random triples in exact integer arithmetic, worst disagreement "
    f"{t['worst_gap']:.0f}")}
<p>That cyclic symmetry <em>is</em> the octonion product, looked at from the side. You can go
the other way and define the product from the form. Vector, spinor, other spinor: the labels
come off.</p>
</div>

<h2>Check it yourself</h2>
<div class="tool" id="tri">
<h3>Three ways round</h3>
<div class="row"><label>algebra</label><span class="units">
<button data-alg="C" aria-pressed="false">ℂ</button>
<button data-alg="H" aria-pressed="false">ℍ</button>
<button data-alg="O" aria-pressed="true">𝕆</button>
<button data-alg="O'" aria-pressed="false">𝕆′</button>
</span><button class="go" id="triroll">new numbers</button></div>
<div class="out" id="triout"></div>
<p class="small mute">The last line reflects all three through a unit. A reflection turns the
form into minus itself — the same size, the other sign — which is how you know a reflection is
not one of the rotations. Two reflections make a rotation; four of them, through two different
units, make a triality automorphism {paper_cite("3")}. Checked at build time on
{r['exact_cases']:,} exact cases and {r['random_units']:,} random unit octonions, worst miss
{r['worst_miss']:.1e}.</p>
</div>

<h2>A third of a turn</h2>
{fig("three-eights.svg", "The three eight-dimensional faces of so(8) — the algebra of rotations "
     "in eight dimensions — drawn in the plane where triality acts as a rotation. Twenty-four "
     "weights, three colours, 120 degrees apart.")}
<div class="prose">
<p>Here is the same fact in pictures. The rotations of eight-dimensional space form an algebra
called <code>so(8)</code>, and it has three different eight-dimensional representations:
<code>8v</code> for the vectors, <code>8s</code> and <code>8c</code> for the two spinors.
Triality is a symmetry of <code>so(8)</code> that cycles them.</p>
<p>The matrix that does it is built here from the diagram symmetry and then checked
{"; ".join(k.replace("_", " ") for k, v in d.items() if v)}: it is orthogonal, it cubes to the
identity, it permutes all 24 roots among themselves, and it carries 8v → 8c → 8s → 8v.</p>
</div>

{fig("dynkin.svg", "D4 is the only simple Lie algebra whose diagram has a three-fold symmetry. "
     "Three outer nodes around one centre; turn it a third and nothing changed.")}

<div class="prose">
<p>That picture on the left is the whole reason triality exists. A Lie algebra's diagram records
how its building blocks lean on each other, and symmetries of the diagram are symmetries of the
algebra. Most diagrams have a mirror at best. D4 — the diagram of <code>so(8)</code> — is a
three-pointed star, and you can turn it by a third.</p>
</div>

<h2>Four algebras, four sizes of the same shape</h2>
{fig("su3d.svg", "Each division algebra has a triality algebra, tri(D), and adding three copies "
     "of D to it gives a Lie algebra — su(2), su(3), sp(3), and f4 with 52 dimensions.")}
<div class="prose">
<p>Every division algebra carries its own triality symmetry, and every one of them fits the
same template: take the symmetry algebra, add one copy of the algebra for the vector and one
for each spinor, and what comes out is a Lie algebra {cite('evans2009', 'barton2003')}
{paper_cite("4")}.</p>
</div>
<div class="wrap"><table>
<thead><tr><th>algebra</th><th class="n">dim</th><th>tri(𝔻)</th><th class="n">dim tri</th>
<th>+ three copies</th><th class="n">total</th><th>which is</th></tr></thead><tbody>""",
         *[f"<tr><td>{E(nm)}</td><td class='n'>{tri[k]['dim']}</td>"
           f"<td>{E(tn)}</td><td class='n'>{tri[k]['tri']}</td>"
           f"<td class='n'>3 × {tri[k]['dim']} = {3 * tri[k]['dim']}</td>"
           f"<td class='n'><b>{tri[k]['total']}</b></td><td><code>{E(tri[k]['algebra'])}</code></td></tr>"
           for k, nm, tn in (("R", "the reals ℝ", "nothing"), ("C", "the complex ℂ", "u(1) + u(1)"),
                             ("H", "the quaternions ℍ", "three copies of su(2)"),
                             ("O", "the octonions 𝕆", "so(8)"))],
         f"""</tbody></table></div>
<p class="small mute">The bottom row is the point: <code>so(8)</code> has 28 dimensions, three
octonions make 24, and 28 + 24 = 52 — which is <code>f4</code>, an exceptional Lie algebra,
built out of nothing but the octonions and their own symmetry.</p>

<h2>Why anyone in physics cares</h2>
{fig("rotation.svg", "A triality automorphism rotates each pair of eigenvectors by 120 degrees. "
     "Three positions, labelled I, II and III.")}
<div class="prose">
<p>Matter comes in three generations. The electron, the muon and the tau are the same particle
three times over with different masses, and nobody knows why there are three
{cite('furey2025')}. Triality is a symmetry of order three that acts on exactly the objects
spinors live in. The temptation is obvious, and it is old.</p>
<p>Whether the temptation pays off is <a href="{BASE}physics/">a separate page</a>, with the
objections on it.</p>
</div>
"""]
    return page("Triality — the same thing three ways", "".join(b), "triality/",
                "Triality: one cyclic form of three arguments, the symmetry that shuffles "
                "vectors and both kinds of spinor, and the 120-degree turn behind the "
                "three-generation guess.",
                "triality/", scripts=("algebra.js", "triality.js"))


def square():
    sq = F["magic"]
    order = ["R", "C", "H", "O", "C'", "H'", "O'"]
    pretty = {"R": "ℝ", "C": "ℂ", "H": "ℍ", "O": "𝕆", "C'": "ℂ′", "H'": "ℍ′", "O'": "𝕆′"}
    rows = []
    for i, a in enumerate(order):
        cells = [f'<th>{pretty[a]}</th>']
        for j, bb in enumerate(order):
            c = sq[i][j]
            cls = ""
            nm = c["name"]
            if nm.startswith("e8"):
                cls = "big"
            elif nm.startswith("e7"):
                cls = "e7"
            elif nm.startswith("e6"):
                cls = "e6"
            elif nm.startswith("f4"):
                cls = "f4"
            cells.append(f'<td class="{cls}"><b>{E(nm)}</b>{c["dim"]}<br>'
                         f'<span>{c["tri_a"]}+{c["tri_b"]}+{c["prod"]}</span></td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    head = "<tr><th></th>" + "".join(f"<th>{pretty[o]}</th>" for o in order) + "</tr>"
    b = [f"""<h1><span class="kind">Forty-nine boxes, one rule</span>The Square</h1>
<p class="lede">Put two division algebras together and a Lie algebra falls out. Do it for every
pair and you get the magic square — which is magic because nobody ordered the exceptional
algebras to show up in it, and there they all are.</p>

<div class="prose">
<p>A <strong>Lie algebra</strong> is the bookkeeping of a continuous symmetry: the list of
independent ways to nudge something, and the rule for what happens when you nudge twice in
different orders. Rotations in three dimensions give a three-dimensional one. Most of them come
in four tidy families that run forever. Five do not: <code>g2</code>, <code>f4</code>,
<code>e6</code>, <code>e7</code>, <code>e8</code>. Those five are the exceptional ones, and they
exist because the octonions do.</p>
<p>Freudenthal and Tits found the square in the sixties {cite('freudenthal1964', 'tits1966')}.
The construction is: take the triality algebra of 𝔸, the triality algebra of 𝔹, and three
copies of 𝔸 ⊗ 𝔹 — one for the vector, one for each spinor.</p>
{eq("dim L(𝔸, 𝔹) = tri(𝔸) + tri(𝔹) + 3 · dim𝔸 · dim𝔹",
    "one line, forty-nine boxes. The small print under each box below is that sum for that box.")}
<p>Every dimension in the table is computed from that formula by <code>tools/algebra.py</code>
and then checked against the known dimension of the algebra named in the box. All forty-nine
agree.</p>
</div>

<h2>The square</h2>
<div class="wrap"><table class="square">{head}{"".join(rows)}</table></div>
<p class="small mute">Top-left quarter: the four division algebras, giving the compact real
forms. The right and bottom bands are the split algebras, which give the other real forms of the
same complex algebras — <code>e8</code> and <code>e8(8)</code> and <code>e8(−24)</code> are the
same 248 dimensions with different signs in the metric {paper_cite("5")}.</p>

{fig("magic.svg", "The same square as a figure, with the arithmetic under every box.")}

<h2>Reading the corners</h2>
<div class="wrap"><table>
<thead><tr><th>pair</th><th>sum</th><th class="n">dim</th><th>algebra</th><th>what it is</th></tr>
</thead><tbody>
<tr><td>ℝ × 𝕆</td><td class="n">0 + 28 + 24</td><td class="n">52</td><td><code>f4</code></td>
<td>the symmetries of the octonion projective plane</td></tr>
<tr><td>ℂ × 𝕆</td><td class="n">2 + 28 + 48</td><td class="n">78</td><td><code>e6</code></td>
<td>big enough to hold the SO(10) grand unified theory and one generation of matter</td></tr>
<tr><td>ℍ × 𝕆</td><td class="n">9 + 28 + 96</td><td class="n">133</td><td><code>e7</code></td>
<td>where ℂ ⊗ ℍ ⊗ 𝕆 fermions land {cite('dixon1994', 'furey2022')}</td></tr>
<tr><td>𝕆 × 𝕆</td><td class="n">28 + 28 + 192</td><td class="n">248</td><td><code>e8</code></td>
<td>the largest exceptional Lie algebra. There is no sixth.</td></tr>
</tbody></table></div>

<div class="prose">
<p>Look down that column. 52, 78, 133, 248 — the whole exceptional series except
<code>g2</code>, produced by one arithmetic rule from the octonions and one other algebra.
<code>g2</code> is the odd one out because it is not in the square at all: it is the symmetry
group <em>of</em> the octonions, the fourteen-dimensional set of ways to relabel them that
leaves every product where it was {paper_cite("11")}.</p>
<p>And the square is symmetric, which it had no right to be. L(𝔸, 𝔹) and L(𝔹, 𝔸) are built
differently and come out the same. That is the part that earns the name.</p>
</div>
"""]
    return page("The Square — forty-nine boxes, one formula", "".join(b), "square/",
                "The Freudenthal-Tits magic square, every dimension computed from "
                "tri(A) + tri(B) + 3 dim A dim B and checked against the algebra it names.",
                "square/")


def e8():
    s = F["systems"]
    z = F["e8_z3"]
    tg = F["e8_two_grading"]
    ring_rows = []
    for k in ["G2", "D4", "F4", "E6", "E7", "E8"]:
        d = s[k]
        rings = " · ".join(f"{n}" for _, n in d["rings"])
        ring_rows.append(f"<tr><td><code>{k.lower()}</code></td><td class='n'>{d['roots']}</td>"
                         f"<td class='n'>{d['rank']}</td><td class='n'>{d['dim']}</td>"
                         f"<td class='n'>{d['h']}</td><td class='n'>{rings}</td></tr>")
    b = [f"""<h1><span class="kind">{s['E8']['roots']} directions, {s['E8']['dim']} dimensions</span>E8</h1>
<p class="lede">E8 is the biggest of the five exceptional Lie algebras and the end of the line.
Two hundred and forty roots, each a direction in eight-dimensional space, each one knowing
about all the others. Octonions times octonions.</p>

<div class="prose">
<p>A <strong>root</strong> is a direction in which the algebra can be stretched — one arrow per
independent way the symmetry can act. E8 has {s['E8']['roots']} of them in 8 dimensions, plus
the 8 directions of the stretching itself, and {s['E8']['roots']} + 8 = {s['E8']['dim']}.</p>
<p>You cannot draw eight dimensions. What you can do is find the one plane the whole thing turns
in — every root system has a <strong>Coxeter element</strong>, one grand rotation that carries
the root system onto itself, and it turns one particular plane by the same angle every time.
For E8 that angle is a thirtieth of a full turn. Flatten the roots onto that plane and they land
on eight rings of thirty.</p>
</div>

<div class="tool">
<h3>Turn it</h3>
<div class="row"><label>system</label><span class="units">
<button data-sys="G2" aria-pressed="false">G2</button>
<button data-sys="D4" aria-pressed="false">D4</button>
<button data-sys="F4" aria-pressed="false">F4</button>
<button data-sys="E6" aria-pressed="false">E6</button>
<button data-sys="E7" aria-pressed="false">E7</button>
<button data-sys="E8" aria-pressed="true">E8</button>
</span></div>
<div class="row"><label>colour</label><span class="units">
<button data-mode="z3" aria-pressed="true">triality, three ways</button>
<button data-mode="two" aria-pressed="false">two ways</button>
<button data-mode="plain" aria-pressed="false">plain</button>
</span>
<button id="spin" aria-pressed="false">turn it</button>
<button id="edges" aria-pressed="true">lines on</button></div>
<canvas id="shadow" data-system="E8" aria-label="{E(ALT['e8.svg'])}"></canvas>
<div class="out" id="shadowinfo"></div>
<p class="small mute">Points and lines come from <code>build/data/roots.json</code>, computed by
<code>tools/roots.py</code>: the root system is built from its definition, the Coxeter element
is multiplied out from the simple reflections, and its eigenvector for e<sup>2πi/h</sup> gives
the plane.</p>
</div>

<h2>Every one of them, counted</h2>
<div class="wrap"><table>
<thead><tr><th>system</th><th class="n">roots</th><th class="n">rank</th><th class="n">dim</th>
<th class="n">turn</th><th class="n">rings</th></tr></thead>
<tbody>{"".join(ring_rows)}</tbody></table></div>
<p class="small mute">Rank is how many independent directions of stretching; dim is roots plus
rank; turn is the Coxeter number, how many clicks to the full rotation. E7 and E6 are pulled out
of E8 here as the roots orthogonal to one root, and to a pair of roots meeting at 120 degrees.</p>

<h2>Cut three ways</h2>
{fig("e8-z3.svg", f"Triality cuts E8 into {z['counts'][0]} roots that hold still and two sets of "
     f"{z['counts'][1]} that trade places. The {z['counts'][0]} fixed roots have rank "
     f"{z['g0_rank']} — they are so(14), and with the eight Cartan directions that is "
     f"{z['g0_dim']} dimensions.")}
<div class="prose">
<p>Apply a triality automorphism to E8 and every direction in it does one of three things:
stands still, turns a third of the way round, or turns two thirds. The algebra splits into
three pieces {paper_cite("6")}:</p>
{eq(f"e8 = <b>{z['g0_dim']}</b> &nbsp;+&nbsp; <b>{z['counts'][1]}</b> &nbsp;+&nbsp; "
    f"<b>{z['counts'][2]}</b> &nbsp;=&nbsp; 248",
    f"the fixed part is so(14) + u(1); the other two are each {z['counts'][1]}-dimensional and "
    f"complex conjugates of each other")}
<p>The split is not decorative. Brackets respect it: nudge in a third-turn direction, then in
another third-turn direction, and you land in a two-thirds direction, every time. That was
checked here on all {z['root_sums_checked']:,} pairs of roots whose sum is again a root —
{z['violations']} violations. Vinberg's Θ-groups are the general theory of these three-way
splits {cite('vinberg1976')}, and Lisi's proposal is that the three generations of matter sit
in the pieces that move.</p>
</div>

<h2>Cut two ways</h2>
{fig("e8-two.svg", f"The other natural cut: {tg['so16'] - 8} roots plus 8 stretching directions "
     f"make so(16), the rotations of sixteen-dimensional space; the remaining {tg['spinor']} are "
     "a single spinor of it.")}
<div class="prose">
<p>E8 also splits clean down the middle a different way: <code>{tg['so16']} + {tg['spinor']} =
248</code>. The first part is <code>so(16)</code> — ordinary rotations in sixteen dimensions.
The second is one spinor of <code>so(16)</code>, {tg['spinor']} components, and this is where
the bosons-and-fermions story wants to live: the even half is forces, the odd half is matter
{paper_cite("10")}.</p>
<p>The roots with whole-number coordinates are the first half; the ones with halves all the way
across are the second. That is all the distinction amounts to, and you can see it in the
picture.</p>
</div>

<h2>The other four</h2>
<div class="grid">
{"".join(f'<figure class="fig"><img src="{BASE}img/{k.lower()}.svg" alt="{E(ALT[k.lower() + ".svg"])}" loading="lazy"><figcaption>{k} — {s[k]["roots"]} roots, {s[k]["dim"]} dimensions, {s[k]["h"]}-fold</figcaption></figure>' for k in ["G2", "D4", "F4", "E6", "E7"])}
</div>
"""]
    return page("E8 — 240 roots, 248 dimensions", "".join(b), "e8/",
                "E8 and its relatives, each root system built from its definition and flattened "
                "onto the plane its Coxeter element turns, with the three-way and two-way splits "
                "computed and checked.",
                "e8/", scripts=("shadow.js",))


def physics():
    z = F["e8_z3"]
    eig = F["eigen"]
    rows = "".join(
        f"<tr><td><code>{E(e['g'])}</code></td><td class='n'>{e['total']}</td>"
        f"<td>{E(e['fixed'])}</td><td class='n'>{e['fixed_dim']}</td>"
        f"<td>{E(e['moving'])}</td><td class='n'>{e['moving_dim']}</td></tr>" for e in eig)
    b = [f"""<h1><span class="kind">What it is supposed to be for</span>Physics</h1>
<p class="lede">Everything up to here is settled mathematics. This page is not. It is a research
programme with real results and real problems, and the problems are on the page.</p>

<div class="note"><b>Where the line is.</b> The division algebras, triality, the magic square
and E8's root system are nineteenth- and twentieth-century mathematics, proved and not in
dispute. Whether nature uses any of it is an open question, and the models below are proposals
under construction — Lisi's own summary of them, in his §10, is a list of what each one still
cannot do.</div>

<h2>The shape of the idea</h2>
<div class="prose">
<p>The Standard Model of particle physics is a list: twelve force carriers, a Higgs, and three
copies of a set of twelve matter particles. The copies are identical except for mass. Nobody
knows why there are three.</p>
<p>The grand-unified idea is that the forces are one force seen through a broken symmetry, and
the standard big symmetry for that is <code>so(10)</code> — 45 dimensions, with one generation
of matter and its antimatter fitting exactly into a 16-component spinor. That part is
respectable and decades old.</p>
<p>The exceptional idea goes one further: put the forces <em>and</em> the matter in the same
Lie algebra, as different parts of one connection. Bosons in the even half, fermions in the odd
half. For that you need an algebra with the right two-way split, and the magic square hands you
three candidates {paper_cite("10")}.</p>
</div>

<div class="wrap"><table>
<thead><tr><th>algebra</th><th class="n">dim</th><th>fixed part</th><th class="n">dim</th>
<th>each moving part</th><th class="n">dim</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small mute">The three-way split of each triality algebra, from Lisi eq. (6.1). Fixed
part plus twice a moving part equals the whole, in every row — checked at build time.</p>

{fig("eigen.svg", "Fixed part in amber, the two moving parts in teal and rose. The proposal is "
     "that generations live in the parts that move.")}

<h2>Three candidates, three catches</h2>
<div class="prose">
<h3>e6 — 78 dimensions</h3>
<p>The smallest one that works. <code>so(10)</code> and its 45 gauge directions fit, one
generation of left-handed matter fits in a 16, one generation of right-handed in the other 16,
and there are six directions of charge left over. <b>The catch:</b> one generation. Triality is
barely used. It is a tidy repackaging of a grand unified theory, not an explanation of three
{cite('dray2010')}.</p>

<h3>e7 — 133 dimensions</h3>
<p>This is where the ℂ ⊗ ℍ ⊗ 𝕆 programme lands — Dixon's algebra, and Furey and Hughes' work on
generations {cite('dixon1994', 'furey2022', 'furey2025')}. Three generations do fit, related by
triality. <b>The catch:</b> you cannot have all three generations <em>and</em> both handednesses
<em>and</em> the antiparticles at once. You must pick. Taking three generations forces a complex
form of <code>e7</code>, which then misbehaves for the gauge fields, and the gravitational frame
is missing altogether {paper_cite("10")}.</p>

<h3>e8 — 248 dimensions</h3>
<p>The whole thing: gravity's spin connection, the frame, the Higgs, the SO(10) gauge fields,
and three generations of fermions related by triality. This is the 2007 paper {cite('lisi2007')}
brought up to date. The 2026 version puts the three generations in the moving parts of the
three-way split, so all three carry identical charges — which is what the Standard Model
actually shows {paper_cite("10")}.</p>
<p><b>The catches, plural.</b> The compact version is Euclidean: no time direction, so it has to
be part of something bigger to describe the world we are in. The natural two-way split of
<code>e8</code> does not line up with that particular assignment of fermions. And the three
generations are not independent of each other, so the model predicts generational mixing it
then has to account for.</p>
</div>

<div class="note"><b>The standing objection.</b> Distler and Garibaldi proved in 2010 that you
cannot embed three generations of Standard Model fermions in E8 in the way the 2007 paper needed
— there is always an unwanted mirror generation {cite('distler2010')}. Lisi's answer in §10 is
not a denial: it accepts the mirror fermions and reinterprets them as the second and third
generations, reached by triality rotation. That is a real answer and it has a real cost, which
is the generational mixing above. This remains contested. If you read one criticism, read that
one.</div>

<h2>What would settle it</h2>
<div class="prose">
<p>Nothing on this page is a prediction yet in the sense that would settle anything. The state
of play, as the paper itself puts it in its discussion, is that the mathematical
scaffolding is now written down in enough detail that model-building can proceed — the point of
the 2026 paper is the scaffolding, not a finished theory {paper_cite("12")}.</p>
<p>What makes it worth watching is the coincidence count. Eight is the last dimension with a
division algebra. Eight is the only dimension with triality. Triality has order three; matter
comes in three generations; the charges of the three generations are identical, which is what a
symmetry of order three would produce. None of that is proof. It is a set of numbers that keep
lining up.</p>
</div>
"""]
    return page("Physics — the proposal, and the objections", "".join(b), "physics/",
                "What the exceptional algebras are supposed to be for in particle physics: "
                "one generation in e6, three in e8, and the standing objections to each.",
                "physics/")


def checks():
    ca = F["checks"]["algebra"]
    cr = F["checks"]["roots"]

    def block(lines):
        out = []
        for line in lines:
            ok = line.startswith("ok")
            text = line[4:].strip()
            mark = "✓" if ok else "✗"
            out.append(f'<li><b>{mark}</b> {E(text)}</li>')
        return "".join(out)

    b = [f"""<h1><span class="kind">{F['checks']['total']} of them</span>Checks</h1>
<p class="lede">Every claim this site makes about these algebras is computed before the page is
built, and the build refuses to publish if one fails. Here is the list, as of {TODAY}:
{F['checks']['total']} checks, {F['checks']['failures']} failing.</p>

<div class="prose">
<p>Two files do the work. <code>tools/algebra.py</code> multiplies things out in exact integer
arithmetic — the tables, the laws, the Fano lines, the triality form, the magic square.
<code>tools/roots.py</code> builds each root system from its definition, finds the simple roots
by cutting with a generic hyperplane, multiplies out the Coxeter element, and reads the
projection plane off its eigenvector.</p>
<p>Run them yourself:</p>
<pre><code>python3 tools/algebra.py
python3 tools/roots.py</code></pre>
</div>

<h2>Algebra <small>{ca['total']} checks, {ca['failures']} failing</small></h2>
<ul class="checks">{block(ca['lines'])}</ul>

<h2>Root systems <small>{cr['total']} checks, {cr['failures']} failing</small></h2>
<ul class="checks">{block(cr['lines'])}</ul>

<h2>What is not checked here</h2>
<div class="prose">
<p>The names in the magic square — which real form each box is — are taken from the paper's
Table 6 and from the literature it cites {cite('barton2003', 'evans2009')}; what this repository
verifies is that the dimension formula reproduces the dimension of the algebra named. The
particle assignments on the physics page are not checkable arithmetic at all; they are
proposals, attributed where they are made.</p>
</div>
"""]
    return page("Checks — every claim, computed", "".join(b), "checks/",
                f"All {F['checks']['total']} arithmetic checks this site runs before it will "
                "publish, listed.", "checks/")


def gallery():
    items = [
        ("hero.jpg", "E8, all of it", "240 roots, 6,720 lines, coloured by the three-way split"),
        ("e8-z3.svg", "E8 cut three ways", "84 fixed, 78 and 78 turning"),
        ("e8-two.svg", "E8 cut two ways", "120 + 128"),
        ("e8.svg", "E8", "eight rings of thirty"),
        ("e7.svg", "E7", "126 roots"),
        ("e6.svg", "E6", "72 roots"),
        ("f4.svg", "F4", "48 roots"),
        ("d4.svg", "D4", "24 roots — the one with triality"),
        ("g2.svg", "G2", "12 roots — the octonions' own symmetry"),
        ("ladder.svg", "The ladder", "what each doubling costs, measured"),
        ("fano.svg", "The wheel", "the octonion table as seven lines"),
        ("tables.svg", "The tables", "ℂ, ℍ, 𝕆 and split 𝕆, coloured"),
        ("three-eights.svg", "8v, 8s, 8c", "the three faces of so(8)"),
        ("dynkin.svg", "The diagrams", "D4's three-fold turn, and E6, E7, E8"),
        ("rotation.svg", "A third of a turn", "what triality does to a generator"),
        ("su3d.svg", "su(3, 𝔻)", "four sizes of one shape"),
        ("magic.svg", "The magic square", "forty-nine boxes, one formula"),
        ("eigen.svg", "The three-way splits", "fixed part and two halves"),
        ("card.jpg", "The share card", ""),
    ]
    cards = "".join(
        f'<a href="{BASE}img/{n}" download><img src="{BASE}img/{n}" alt="{E(ALT.get(n, t))}" '
        f'loading="lazy"><b>{E(t)}</b><br>{E(sub)}</a>' for n, t, sub in items)
    b = [f"""<h1><span class="kind">{len(items)} of them, yours</span>Gallery</h1>
<p class="lede">Every picture on this site, computed by <code>tools/figures.py</code> from the
algebra in <code>tools/algebra.py</code> and <code>tools/roots.py</code>. None is traced from,
or a copy of, anyone else's drawing. Click to download.</p>
<p class="small mute">{E(CREDIT)} — use them with the credit line and a link back. The SVGs are
plain text; open one in an editor and the coordinates are the numbers.</p>
<div class="gallery">{cards}</div>
"""]
    return page("Gallery — every figure", "".join(b), "gallery/",
                "Every figure on the site, downloadable, CC BY 4.0.", "gallery/")


def credit():
    rows = []
    for sid, who, year, title, where, arx, why in SOURCES:
        u = src_url((sid, who, year, title, where, arx, why))
        link = f'<a href="{u}" rel="noopener">{E(title)}</a>' if u else E(title)
        sub = f'<br><span class="mute small">{E(where)}</span>' if where else ""
        rows.append(f"<tr><td>{E(who)}</td><td class='n'>{year}</td><td>{link}{sub}</td>"
                    f"<td class='small mute'>{E(why)}</td></tr>")
    b = [f"""<h1><span class="kind">Whose work this is</span>Credit</h1>
<p class="lede">This site exists because of one paper, and that paper exists because of
thirty-four others. All of them are below, with links.</p>

{credit_block()}

<h2>What was done here, and what was not</h2>
<div class="prose">
<ul class="ticks">
<li>The mathematics is not mine and not the paper's — it runs from Hamilton and Graves in the
1840s through Cartan, Freudenthal, Tits and Vinberg.</li>
<li>The paper is the reason this site picks these topics, in this order, with these
decompositions. Where a page follows its §, the page says so.</li>
<li>Every table, figure, number and check on this site was computed in this repository from the
definitions. The multiplication tables in <code>tools/algebra.py</code> are transcribed from the
paper's §2, which prints the standard ones, and are then verified against the laws they have to
satisfy.</li>
<li>No text, equation image or figure from the paper is reproduced here. Its licence is
CC BY-NC-ND 4.0, which permits no derivatives, and this site is not one.</li>
<li>Where physics is proposal rather than result, the proposer is named and the objections are
on the same page.</li>
</ul>
</div>

<h2>The paper's references</h2>
<p class="small mute">Lisi's own list, transcribed with its links. The right-hand column is this
site's note on what each one is here for.</p>
<div class="wrap"><table>
<thead><tr><th>who</th><th class="n">year</th><th>what</th><th>why it is on the list</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>

<h2>This site</h2>
<dl class="kv">
<dt>Text and figures</dt><dd>{E(CREDIT)} —
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Credit line:
<code>{E(CREDIT)}</code>, with a link to {SITE_URL}/.</dd>
<dt>Code</dt><dd>MIT — <code>tools/</code>, <code>js/</code>, <code>tests/</code>.</dd>
<dt>Source</dt><dd><a href="https://github.com/NaNoBotCo/{SELF}">github.com/NaNoBotCo/{SELF}</a></dd>
<dt>Built</dt><dd>{E(TODAY)}, from {F['checks']['total']} passing checks</dd>
</dl>

<h2>Reading order, if you want the mathematics properly</h2>
<div class="prose">
<ol>
<li><b>Baez, <i>The Octonions</i></b> (2002) — the place to start, and the paper Lisi's follows.
{cite('baez2002')}</li>
<li><b>Dray and Manogue, <i>The Geometry of the Octonions</i></b> (2015) — book length, worked
out.</li>
<li><b>Evans, <i>Trialities and exceptional Lie algebras</i></b> (2009) — the magic square taken
apart. {cite('evans2009')}</li>
<li><b>Lisi, <i>Division Algebras, Triality, and Exceptional Magic</i></b> (2026) — the one this
site reads, and the most explicit of them about how to actually compute with triality.</li>
</ol>
</div>
"""]
    return page("Credit — whose work this is", "".join(b), "credit/",
                "The paper this site reads, its thirty-four references with links, and what was "
                "computed here rather than copied.", "credit/")


def not_found():
    b = f"""<h1><span class="kind">404</span>Not here</h1>
<p class="lede">That page is not on this site. The nine that are:</p>
<div class="grid">
{"".join(f'<a class="card" href="{BASE}{h}"><h3>{E(t)}</h3></a>' for h, t in NAV)}
</div>
<p><a href="{BASE}">Back to the front</a>.</p>"""
    out = page("Not here", b, "404")
    shutil.move(SITE / "404" / "index.html", SITE / "404.html")
    (SITE / "404").rmdir()
    return out


# ------------------------------------------------------------------- machine files

def machine_files():
    pages = [("", "The front page")] + [(h, t) for h, t in NAV]
    urls = "".join(f"<url><loc>{SITE_URL}/{h}</loc><lastmod>{TODAY}</lastmod></url>"
                   for h, _ in pages)
    write(SITE / "sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>")
    write(SITE / "robots.txt",
          f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    s = F["systems"]
    write(SITE / "llms.txt", f"""# {NAME}

> {TAG}

{SITE_URL}/

Reads: {PAPER['authors']}, "{PAPER['title']}", {PAPER['where']}, {PAPER['url']} —
licensed {PAPER['licence']}. Nothing from that paper is reproduced here; the mathematics is
recomputed from the definitions in this repository and the paper is cited where it is the
reason a topic is present.

## Numbers this site computes
- division algebras: 1, 2, 4, 8 — reals, complex, quaternions, octonions; split forms beside each
- the octonion table has {len(F['fano_lines'])} Fano lines, each unit on three of them
- sedenion zero divisors: {F['zero_divisor_pairs']} pairs of basis planes multiply to zero
- triality form T(v,psi,chi) cyclic on {F['triality_cyclic']['trials']} random triples, exact
- triality Lie algebras: su(2) 3, su(3) 8, sp(3) 21, f4 52 — tri(D) + 3 dim D
- magic square: dim = tri(A) + tri(B) + 3 dim A dim B, all 49 boxes agree with the named algebra
- root systems: G2 {s['G2']['roots']}, D4 {s['D4']['roots']}, F4 {s['F4']['roots']}, E6 {s['E6']['roots']}, E7 {s['E7']['roots']}, E8 {s['E8']['roots']} roots
- E8 Coxeter number {s['E8']['h']}, eight rings of thirty in the Coxeter plane
- E8 triality split: {F['e8_z3']['counts'][0]} + {F['e8_z3']['counts'][1]} + {F['e8_z3']['counts'][2]} roots, {F['e8_z3']['violations']} bracket violations on {F['e8_z3']['root_sums_checked']} root sums
- E8 two-grading: so(16) {F['e8_two_grading']['so16']} + spinor {F['e8_two_grading']['spinor']} = 248
- {F['checks']['total']} checks run before publication, {F['checks']['failures']} failing

## Pages
""" + "".join(f"- {SITE_URL}/{h} — {t}\n" for h, t in NAV) + f"""
## Data
- {SITE_URL}/data/algebra.json — multiplication tables, Fano lines, the magic square
- {SITE_URL}/data/roots.json — every root system, projected, with the E8 gradings
- {SITE_URL}/data/facts.json — every number quoted on the site

## Terms
Text and figures: {CREDIT}, CC BY 4.0. Code: MIT.
""")
    write(SITE / "humans.txt", f"""/* the site */
Name: {NAME}
Built: {TODAY}
Source: https://github.com/NaNoBotCo/{SELF}
Terms: text and figures CC BY 4.0 ({CREDIT}); code MIT

/* the paper */
{PAPER['authors']}, {PAPER['title']}
{PAPER['where']} — {PAPER['url']}
Licensed {PAPER['licence']}. Cited throughout, reproduced nowhere.

/* the tools */
python3, numpy, Pillow. Static HTML with the stylesheet inlined; the scripts in js/ read
the same JSON the figures were drawn from.
""")
    write(SITE / "icon.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
          '<rect width="32" height="32" rx="6" fill="#0a0a10"/>'
          '<circle cx="16" cy="9" r="4" fill="#ffc247"/>'
          '<circle cx="9" cy="21" r="4" fill="#5fd3c6"/>'
          '<circle cx="23" cy="21" r="4" fill="#ff7ab6"/></svg>')
    shutil.copy(BUILD / "facts.json", SITE / "data" / "facts.json")


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    shutil.copytree(IMG, SITE / "img")
    shutil.copytree(BUILD / "data", SITE / "data")
    shutil.copytree(ROOT / "js", SITE / "js")
    home()
    numbers()
    wheel()
    triality()
    square()
    e8()
    physics()
    checks()
    gallery()
    credit()
    not_found()
    machine_files()
    fleet.decorate(SITE, SELF, roster=FLEET)
    (SITE / ".basepath").write_text(BASE, encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    n = len(list(SITE.rglob("index.html")))
    print(f"build/site ← {n} pages")


if __name__ == "__main__":
    main()
