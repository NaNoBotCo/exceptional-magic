#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figures.py — every picture on the site, drawn from the algebra in tools/.

    python3 tools/figures.py

Writes build/img/*.svg, build/img/*.png and build/facts.json. Nothing here is traced
from anyone's figure; each drawing is a plot of numbers this repository computes.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import algebra as al          # noqa: E402
import roots as rt            # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
IMG = BUILD / "img"
IMG.mkdir(parents=True, exist_ok=True)

INK = "#f2ede3"
MUTE = "#9d9689"
LINE = "#2c2c3a"
BG = "#0a0a10"
PANEL = "#12121c"
# one colour per triality eigenspace, used everywhere the three-way split appears
C0, C1, C2 = "#ffc247", "#5fd3c6", "#ff7ab6"
HOT = "#ffc247"
COOL = "#5fd3c6"
ROSE = "#ff7ab6"
VIOLET = "#b79cff"
DIM = {"R": "#7e8aa0", "C": "#5fd3c6", "H": "#b79cff", "O": "#ffc247",
       "C'": "#3f8f88", "H'": "#7a64bd", "O'": "#bd8d2e"}

FACTS: dict = {}


def svg(name, w, h, body, title, desc=""):
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'role="img" aria-labelledby="t d" font-family="system-ui,-apple-system,Segoe UI,sans-serif">'
           f'<title id="t">{title}</title><desc id="d">{desc}</desc>'
           f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')
    (IMG / name).write_text(out, encoding="utf-8")
    return name


def txt(x, y, s, fill=INK, size=13, anchor="middle", weight="400", family=None, extra=""):
    fam = f' font-family="{family}"' if family else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{fam}{extra}>{s}</text>')


# ------------------------------------------------------------------ 1. the ladder

def ladder():
    """1, 2, 4, 8 — and the price of each doubling, measured on random elements."""
    survey = al.law_survey(trials=2000)
    FACTS["survey"] = survey
    rows = [("R", "the reals", 1), ("C", "the complex numbers", 2), ("H", "the quaternions", 4),
            ("O", "the octonions", 8), ("S", "the sedenions", 16)]
    laws = [("commutative", "ab = ba"), ("associative", "(ab)c = a(bc)"),
            ("alternative", "(aa)b = a(ab)"), ("composition", "|ab| = |a||b|")]
    W, H = 900, 420
    cw, ch = 132, 44
    x0, y0 = 250, 96
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(txt(24, 38, "Every doubling costs you something", INK, 21, "start", "700"))
    b.append(txt(24, 60, f'measured on {survey[0]["trials"]:,} random triples per algebra, exact integer arithmetic',
                 MUTE, 12.5, "start"))
    for k, (_, label) in enumerate(laws):
        b.append(txt(x0 + k * cw + cw / 2, y0 - 10, label, MUTE, 12, "middle", "600",
                     family="ui-monospace,Menlo,monospace"))
    for r, (tag, name, dim) in enumerate(rows):
        y = y0 + r * ch
        row = next(s for s in survey if s["algebra"] == tag)
        col = DIM.get(tag, VIOLET)
        b.append(f'<rect x="24" y="{y}" width="{W - 48}" height="{ch - 6}" rx="6" fill="{PANEL}"/>')
        b.append(txt(40, y + 27, name, INK, 15, "start", "600"))
        b.append(txt(232, y + 27, f"{dim}", col, 17, "end", "800"))
        for k, (key, _) in enumerate(laws):
            hits = row[key]
            frac = hits / row["trials"]
            x = x0 + k * cw
            good = frac > 0.999
            fill = col if good else "#2a2a38"
            b.append(f'<rect x="{x}" y="{y + 8}" width="{cw - 14}" height="{ch - 22}" rx="4" '
                     f'fill="{fill}" opacity="{0.9 if good else 1}"/>')
            label = "holds" if good else ("never" if not hits else f"{hits} of {row['trials']:,}")
            b.append(txt(x + (cw - 14) / 2, y + 30, label, "#0a0a10" if good else MUTE, 12,
                         "middle", "700"))
    y = y0 + len(rows) * ch + 14
    zd = al.zero_divisors(limit=4)
    FACTS["zero_divisor_pairs"] = len(al.zero_divisors())
    FACTS["zero_divisor_example"] = zd[0]
    (a1, a2), (c1, c2) = zd[0]
    b.append(txt(24, y + 16, f"Past eight, two things that are not zero can multiply to zero: "
                             f"(e{a1} + e{a2})(e{c1} + e{c2}) = 0 — "
                             f"{FACTS['zero_divisor_pairs']:,} such pairs of basis planes.",
                 MUTE, 12.5, "start"))
    return svg("ladder.svg", W, H, "".join(b),
               "The four division algebras and the laws each one keeps",
               "A table: the reals keep every law; the complex numbers lose nothing yet; the "
               "quaternions stop commuting; the octonions stop associating but stay alternative "
               "and keep the norm law; the sedenions lose the norm law as well.")


# -------------------------------------------------------------------- 2. the Fano

def fano():
    lines = al.fano_lines()
    FACTS["fano_lines"] = lines
    W = H = 560
    R = 205
    cx, cy = W / 2, H / 2 + 16
    # three corners, three edge midpoints, one centre
    corner = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))
              for a in (-90, 30, 150)]
    mid = [((corner[i][0] + corner[j][0]) / 2, (corner[i][1] + corner[j][1]) / 2)
           for i, j in ((0, 1), (1, 2), (2, 0))]
    centre = (cx, cy)
    # place the seven units so that every computed line is one of the seven drawn lines
    pos, used = {}, {}
    slots = {0: corner[0], 1: corner[1], 2: corner[2], 3: mid[0], 4: mid[1], 5: mid[2], 6: centre}
    # find a labelling of e1..e7 onto the seven points for which the table's lines are the
    # Fano lines: three sides, three medians, one inner circle
    geo = [(0, 3, 1), (1, 4, 2), (2, 5, 0), (0, 6, 4), (1, 6, 5), (2, 6, 3), (3, 4, 5)]
    geoset = {frozenset(t) for t in geo}
    import itertools as it
    for perm in it.permutations(range(1, 8)):
        m = {u: s for s, u in enumerate(perm)}
        if all(frozenset(m[u] for u in ln) in geoset for ln in lines):
            pos = {u: slots[m[u]] for u in range(1, 8)}
            used = m
            break
    assert pos, "no labelling of the drawn plane matches the table"
    FACTS["fano_labelling_ok"] = True

    b = []
    b.append(txt(W / 2, 38, "The octonion table is a seven-point plane", INK, 19, "middle", "700"))
    b.append(txt(W / 2, 58, "seven points, seven lines, three points on every line, "
                            "three lines through every point", MUTE, 12))

    def P(u):
        return pos[u]

    # draw the six straight lines and the circle
    circle_line = None
    for ln in lines:
        idx = [used[u] for u in ln]
        if set(idx) == {3, 4, 5}:
            circle_line = ln
            continue
        pts3 = [slots[i] for i in idx]
        p1, p2 = max(((a, c) for a in pts3 for c in pts3), key=lambda pr: math.dist(*pr))
        b.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
                 f'stroke="{LINE}" stroke-width="2.5"/>')
    rr = math.dist(slots[3], centre)
    b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" fill="none" stroke="{LINE}" '
             f'stroke-width="2.5"/>')

    def head(x, y, dx, dy, col=HOT, k=8.0):
        L = math.hypot(dx, dy) or 1
        dx, dy = dx / L, dy / L
        return (f'<path d="M{x - dx * k - dy * k * 0.62:.1f},{y - dy * k + dx * k * 0.62:.1f} '
                f'L{x + dx * k:.1f},{y + dy * k:.1f} '
                f'L{x - dx * k + dy * k * 0.62:.1f},{y - dy * k - dx * k * 0.62:.1f}" '
                f'fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" '
                f'stroke-linejoin="round"/>')

    # each straight line: find which end the cycle runs towards, then two arrowheads on it
    for ln in lines:
        if ln is circle_line:
            continue
        idx = [used[u] for u in ln]
        ends = [i for i in idx if idx.count(i) == 1]
        # the middle point is the one lying between the other two
        pts = [slots[i] for i in idx]
        mid_k = min(range(3), key=lambda k: abs(
            math.dist(pts[(k + 1) % 3], pts[k]) + math.dist(pts[k], pts[(k + 2) % 3])
            - math.dist(pts[(k + 1) % 3], pts[(k + 2) % 3])))
        # the cycle a -> b -> c: travel runs from the point before the middle to the one after
        start, finish = pts[(mid_k - 1) % 3], pts[(mid_k + 1) % 3]
        dx, dy = finish[0] - start[0], finish[1] - start[1]
        for t in (0.27, 0.73):
            b.append(head(start[0] + dx * t, start[1] + dy * t, dx, dy))

    # the circle: three arcs, arrowheads tangent to it
    if circle_line:
        ang = {u: math.atan2(slots[used[u]][1] - cy, slots[used[u]][0] - cx) for u in circle_line}
        a0, a1 = ang[circle_line[0]], ang[circle_line[1]]
        step = (a1 - a0) % (2 * math.pi)
        ccw = step > math.pi          # which way round the cycle actually runs
        for u in circle_line:
            a = ang[u] + (-0.52 if ccw else 0.52)
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            tx, ty = (math.sin(a), -math.cos(a)) if ccw else (-math.sin(a), math.cos(a))
            b.append(head(x, y, tx, ty))

    for u in range(1, 8):
        x, y = P(u)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="{BG}" stroke="{COOL}" stroke-width="2.5"/>')
        b.append(txt(x, y + 5, f"e{u}", INK, 14, "middle", "700"))
    b.append(txt(W / 2, H - 14, "follow an arrow: e" + str(lines[0][0]) + " e" + str(lines[0][1])
                 + " = e" + str(lines[0][2]) + ", and go against it for a minus sign", MUTE, 12))
    return svg("fano.svg", W, H, "".join(b), "The Fano plane of the octonion units",
               "Seven circles labelled e1 to e7 at the corners, edge midpoints and centre of a "
               "triangle, joined by three sides, three medians and one inner circle. Each of the "
               "seven lines carries arrows showing the cyclic order of multiplication.")


# ---------------------------------------------------------- 3. multiplication tables

def tables():
    algs = [al.C, al.H, al.O, al.OS]
    cell = 26
    pad = 26
    colw = 232
    W = pad * 2 + colw * len(algs) - 30
    H = 112 + 8 * cell + 76
    b = [txt(pad, 38, "The tables, coloured", INK, 20, "start", "700"),
         txt(pad, 58, "row a, column b, colour = which unit e_a e_b lands on; "
                      "pale = plus, dark = minus", MUTE, 12.5, "start")]
    wheel = ["#5a5f70", "#ff7ab6", "#ffc247", "#5fd3c6", "#b79cff", "#7fd46a", "#ff9060", "#69a6ff"]
    for k, A in enumerate(algs):
        x = pad + k * colw
        b.append(txt(x, 92, A.tag, INK, 17, "start", "800"))
        b.append(txt(x + (30 if len(A.tag) > 1 else 22), 92, A.name, MUTE, 12, "start"))
        for i in range(A.n):
            for j in range(A.n):
                sgn, c = A.table[i][j]
                b.append(f'<rect x="{x + j * cell}" y="{112 + i * cell}" width="{cell - 2}" '
                         f'height="{cell - 2}" fill="{wheel[c % len(wheel)]}" '
                         f'opacity="{1.0 if sgn > 0 else 0.4}"/>')
                if A.n <= 4:
                    b.append(txt(x + j * cell + cell / 2 - 1, 112 + i * cell + cell / 2 + 4,
                                 f'{"−" if sgn < 0 else ""}{c}', "#0a0a10", 11, "middle", "700"))
    ky = H - 34
    for k in range(8):
        b.append(f'<rect x="{pad + k * 62}" y="{ky}" width="15" height="15" fill="{wheel[k]}"/>')
        b.append(txt(pad + 21 + k * 62, ky + 12, f"e{k}", MUTE, 12, "start"))
    b.append(txt(pad + 8 * 62 + 14, ky + 12,
                 "the split table differs from 𝕆 in a quarter of its signs", MUTE, 12, "start"))
    return svg("tables.svg", W, H, "".join(b), "Multiplication tables of C, H, O and split O",
               "Four square grids of coloured cells, two by two for the complex numbers, four by "
               "four for the quaternions, eight by eight for the octonions and the split octonions. "
               "Colour names the unit the product lands on; darker cells are the negative sign.")


# -------------------------------------------------------------- 4. root system shadows

def shadow_svg(name, system, title, note, size=560, dot=4.6, colour=None, legend=None):
    p = rt.project(system)
    pts = p["points"]
    rad = np.linalg.norm(pts, axis=1)
    scale = (size / 2 - 40) / rad.max()
    cx = cy = size / 2
    b = [txt(cx, 34, title, INK, 19, "middle", "700"), txt(cx, 54, note, MUTE, 12.5)]
    rings = sorted({round(r, 6) for r in rad if r > 1e-9})
    for r in rings:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r * scale:.2f}" fill="none" stroke="{LINE}" '
                 f'stroke-width="1"/>')
    for i, (x, y) in enumerate(pts):
        c = colour(i) if colour else HOT
        b.append(f'<circle cx="{cx + x * scale:.2f}" cy="{cy - y * scale:.2f}" r="{dot}" fill="{c}"/>')
    if legend:
        for k, (lab, col) in enumerate(legend):
            b.append(f'<rect x="{18}" y="{size - 66 + k * 20}" width="12" height="12" fill="{col}"/>')
            b.append(txt(36, size - 55 + k * 20, lab, MUTE, 12, "start"))
    return svg(name, size, size, "".join(b), title, note), p


def shadows():
    out = {}
    for tag, sysname in [("G2", "G2"), ("D4", "D4"), ("F4", "F4"), ("E6", "E6"), ("E7", "E7"), ("E8", "E8")]:
        R = rt.SYSTEMS[sysname]
        p = rt.project(R)
        rank = int(np.linalg.matrix_rank(R))
        note = (f"{len(R)} roots · rank {rank} · {len(R) + rank} dimensions · "
                f"{p['h']}-fold shadow")
        shadow_svg(f"{sysname.lower()}.svg", R, sysname, note,
                   size=520 if sysname != "E8" else 620,
                   dot=5.2 if len(R) < 80 else 4.0)
        out[sysname] = {"roots": int(len(R)), "rank": rank, "dim": len(R) + rank,
                        "h": int(p["h"]), "rings": [[r, n] for r, n in p["rings"] if r > 1e-9]}
    FACTS["systems"] = out
    return out


def e8_z3():
    """The E8 shadow, coloured by which of the three triality eigenspaces each root
    falls in."""
    R = rt.E8
    simple = rt.simple_roots(R)
    c, m = rt.z3_grading(R, simple)
    tested, bad = rt.grading_violations(R, m)
    counts = [int((m == k).sum()) for k in range(3)]
    FACTS["e8_z3"] = {"counts": counts, "root_sums_checked": int(tested), "violations": int(bad),
                      "g0_dim": counts[0] + 8, "g0_rank": int(np.linalg.matrix_rank(R[m == 0]))}
    cols = [C0, C1, C2]
    shadow_svg("e8-z3.svg", R,
               "E8, cut three ways by triality",
               f"{counts[0]} roots stand still · {counts[1]} turn one way · {counts[2]} turn the other",
               size=620, dot=4.2, colour=lambda i: cols[int(m[i])],
               legend=[(f"fixed — so(14) + u(1), {counts[0]} + 8 = {counts[0] + 8} dimensions", C0),
                       (f"one third turn, {counts[1]} roots", C1),
                       (f"two thirds turn, {counts[2]} roots", C2)])
    whole = rt.two_grading(R)
    FACTS["e8_two_grading"] = {"so16": int(whole.sum()) + 8, "spinor": int((~whole).sum())}
    shadow_svg("e8-two.svg", R, "E8, cut two ways",
               f"{int(whole.sum())} + 8 = {int(whole.sum()) + 8} make so(16); the other "
               f"{int((~whole).sum())} are one spinor",
               size=620, dot=4.2,
               colour=lambda i: COOL if whole[i] else ROSE,
               legend=[("so(16) — whole-number coordinates", COOL),
                       ("the 128 — half-integer coordinates, where the fermions go", ROSE)])
    return m


def hero(m):
    """The E8 shadow with its 6,720 sixty-degree edges, drawn big."""
    R = rt.E8
    p = rt.project(R)
    pts = p["points"]
    S = 1600
    SS = 2
    W = S * SS
    im = Image.new("RGB", (W, W), (10, 10, 16))
    d = ImageDraw.Draw(im, "RGBA")
    scale = (W / 2 - 60 * SS) / np.linalg.norm(pts, axis=1).max()
    cx = cy = W / 2
    XY = [(cx + x * scale, cy - y * scale) for x, y in pts]
    pal = [(255, 194, 71), (95, 211, 198), (255, 122, 182)]
    edges = 0
    for i in range(len(R)):
        for j in range(i + 1, len(R)):
            if abs(R[i] @ R[j] - 1) < 1e-9:
                edges += 1
                col = pal[int(m[i])]
                d.line([XY[i], XY[j]], fill=col + (16,), width=SS)
    for i, (x, y) in enumerate(XY):
        c = pal[int(m[i])]
        d.ellipse([x - 5 * SS, y - 5 * SS, x + 5 * SS, y + 5 * SS], fill=c + (230,))
    im = im.resize((1400, 1400), Image.LANCZOS)
    im.save(IMG / "hero.jpg", quality=90, optimize=True, progressive=True)

    # a wide crop for the share card, with the title burnt in
    card = Image.new("RGB", (1200, 630), (10, 10, 16))
    sq = im.resize((630, 630), Image.LANCZOS)
    card.paste(sq, (570, 0))
    dc = ImageDraw.Draw(card)
    dc.rectangle([570, 0, 600, 630], fill=(10, 10, 16))

    def font(size, bold=True):
        for path in ("/System/Library/Fonts/Avenir Next Condensed.ttc",
                     "/System/Library/Fonts/Supplemental/Futura.ttc",
                     "/System/Library/Fonts/Helvetica.ttc"):
            try:
                return ImageFont.truetype(path, size, index=5 if bold else 0)
            except Exception:
                continue
        return ImageFont.load_default()

    dc.text((60, 168), "EXCEPTIONAL", fill=(242, 237, 227), font=font(84))
    dc.text((60, 258), "MAGIC", fill=(255, 194, 71), font=font(84))
    dc.text((62, 372), "eight ways to multiply,", fill=(157, 150, 137), font=font(34, False))
    dc.text((62, 412), "and where they get you", fill=(157, 150, 137), font=font(34, False))
    dc.text((62, 520), "nanobotco.github.io/exceptional-magic", fill=(95, 211, 198), font=font(26, False))
    card.save(IMG / "card.jpg", quality=88, optimize=True)
    FACTS["hero_edges"] = edges
    return edges


# ------------------------------------------------------------------ 5. triality

def three_eights():
    """8v, 8s and 8c of so(8), drawn in the plane where triality is a 120 degree turn."""
    J, W8, checks = rt.d4_triality()
    FACTS["d4_triality_checks"] = checks
    vals, vecs = np.linalg.eig(J)
    k = int(np.argmin(np.abs(vals - np.exp(2j * np.pi / 3))))
    v = vecs[:, k]
    a, b0 = np.real(v), np.imag(v)
    a /= np.linalg.norm(a)
    b0 = b0 - (b0 @ a) * a
    b0 /= np.linalg.norm(b0)
    size = 560
    cx = cy = size / 2 + 10
    sets = [("8v — vectors", W8["v"], C0), ("8c — one spinor", W8["c"], C1),
            ("8s — the other spinor", W8["s"], C2)]
    allp = np.array([[w @ a, w @ b0] for _, S, _ in sets for w in S])
    scale = (size / 2 - 70) / max(np.linalg.norm(allp, axis=1).max(), 1e-9)
    body = [txt(cx, 34, "Triality is a third of a turn", INK, 19, "middle", "700"),
            txt(cx, 54, "the three eight-dimensional faces of so(8), in the plane where the "
                        "symmetry rotates", MUTE, 12.5)]
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{scale * np.linalg.norm(allp, axis=1).max():.1f}" '
                f'fill="none" stroke="{LINE}"/>')
    for ang in (90, 210, 330):
        x = cx + math.cos(math.radians(ang)) * (size / 2 - 52)
        y = cy - math.sin(math.radians(ang)) * (size / 2 - 52)
        body.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{LINE}" '
                    f'stroke-dasharray="3 5"/>')
    for name, S, col in sets:
        for w in S:
            x, y = (w @ a) * scale, (w @ b0) * scale
            body.append(f'<circle cx="{cx + x:.1f}" cy="{cy - y:.1f}" r="7" fill="{col}" '
                        f'fill-opacity=".92"/>')
    for k2, (name, _, col) in enumerate(sets):
        body.append(f'<rect x="18" y="{size + 8 + k2 * 22}" width="12" height="12" fill="{col}"/>')
        body.append(txt(36, size + 19 + k2 * 22, name, MUTE, 12.5, "start"))
    body.append(txt(18, size + 92, "turn the page 120° and the colours trade places",
                    MUTE, 12.5, "start"))
    return svg("three-eights.svg", size, size + 104, "".join(body),
               "The three eight-dimensional representations of so(8) under triality",
               "Twenty-four dots in three colours arranged with three-fold symmetry; a third of a "
               "turn carries each colour onto the next.")


def dynkin():
    """The D4 diagram and its three-fold symmetry; then E6, E7, E8 in a row."""
    W, H = 900, 306
    b = [txt(24, 38, "One diagram has a three-fold symmetry", INK, 20, "start", "700"),
         txt(24, 58, "so(8) is the only simple Lie algebra whose diagram can be turned by a third",
             MUTE, 12.5, "start")]
    cx, cy = 190, 175
    r = 62
    outer = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
             for a in (-90, 30, 150)]
    for x, y in outer:
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{MUTE}" stroke-width="2"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{INK}"/>')
    for k, (x, y) in enumerate(outer):
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{[C0, C1, C2][k]}"/>')
    ar = 44
    b.append(f'<path d="M{cx + 96 + ar * math.cos(math.radians(-60)):.1f},'
             f'{cy + ar * math.sin(math.radians(-60)):.1f} '
             f'A{ar},{ar} 0 1 1 {cx + 96 + ar * math.cos(math.radians(60)):.1f},'
             f'{cy + ar * math.sin(math.radians(60)):.1f}" fill="none" stroke="{HOT}" '
             f'stroke-width="2.2"/>')
    hx, hy = cx + 96 + ar * math.cos(math.radians(60)), cy + ar * math.sin(math.radians(60))
    b.append(f'<path d="M{hx - 9:.1f},{hy - 7:.1f} L{hx:.1f},{hy + 2:.1f} L{hx + 8:.1f},{hy - 9:.1f}" '
             f'fill="none" stroke="{HOT}" stroke-width="2.2" stroke-linecap="round" '
             f'stroke-linejoin="round"/>')
    b.append(txt(cx, cy + 108, "D4 — so(8)", INK, 14, "middle", "700"))
    b.append(txt(cx, cy + 128, "turn the three outer nodes", MUTE, 11.5))

    # E6, E7, E8: a chain of n-1 nodes with one hung off the third from the left
    x0 = 430
    for k, (name, n) in enumerate((("E6", 6), ("E7", 7), ("E8", 8))):
        y = 108 + k * 56
        chain = n - 1
        for i in range(chain - 1):
            b.append(f'<line x1="{x0 + i * 34}" y1="{y}" x2="{x0 + (i + 1) * 34}" y2="{y}" '
                     f'stroke="{MUTE}" stroke-width="2"/>')
        b.append(f'<line x1="{x0 + 2 * 34}" y1="{y}" x2="{x0 + 2 * 34}" y2="{y - 28}" '
                 f'stroke="{MUTE}" stroke-width="2"/>')
        for i in range(chain):
            b.append(f'<circle cx="{x0 + i * 34}" cy="{y}" r="7" fill="{INK}"/>')
        b.append(f'<circle cx="{x0 + 2 * 34}" cy="{y - 28}" r="7" fill="{HOT}"/>')
        b.append(txt(x0 + (chain - 1) * 34 + 22, y + 5,
                     f"{name} · {rt.ALGEBRA_DIM[name]}", INK, 13.5, "start", "700"))
    b.append(txt(x0, 108 + 3 * 56 + 6, "each new node lengthens the chain by one",
                 MUTE, 11.5, "start"))

    return svg("dynkin.svg", W, H, "".join(b), "Dynkin diagrams: D4's three-fold symmetry, and E6, E7, E8",
               "A three-pointed star for D4 with a rotation arrow, and beside it the three "
               "exceptional diagrams as a line of nodes with one node branching off.")


def rotation():
    """What a triality automorphism does to one generator: a 120 degree turn."""
    W, H = 760, 400
    cx, cy, r = 210, 220, 100
    b = [txt(24, 38, "A third of a turn, three times over", INK, 20, "start", "700"),
         txt(24, 58, "each pair of eigenvectors spans a plane that triality rotates by 120°",
             MUTE, 12.5, "start")]
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}"/>')
    for ang, col, lab in [(90, C0, "I"), (210, C1, "II"), (330, C2, "III")]:
        x = cx + r * math.cos(math.radians(ang))
        y = cy - r * math.sin(math.radians(ang))
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="3"/>')
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{col}"/>')
        b.append(txt(cx + (r + 26) * math.cos(math.radians(ang)),
                     cy - (r + 26) * math.sin(math.radians(ang)) + 5, lab, col, 15, "middle", "700"))
    b.append(txt(cx, cy + r + 62, "generation I, II, III — if the guess is right", MUTE, 12.5))
    b.append(txt(420, 150, "the matrix triality applies to the pair", MUTE, 12.5, "start"))
    for i, line in enumerate(["⎡ −1/2   −√3/2 ⎤", "⎣  √3/2  −1/2  ⎦"]):
        b.append(txt(420, 186 + i * 28, line, INK, 16, "start", "600",
                     family="ui-monospace,Menlo,monospace"))
    b.append(txt(420, 258, "apply it three times and you are back where you started",
                 MUTE, 12.5, "start"))
    b.append(txt(420, 280, "Lisi §6 — the (V^R, V^I) plane of each eigenvector pair",
                 MUTE, 11.5, "start"))
    return svg("rotation.svg", W, H, "".join(b), "Triality as a 120 degree rotation",
               "A circle with three spokes at 120 degrees, labelled I, II and III, beside the two "
               "by two rotation matrix that carries one spoke to the next.")


# ------------------------------------------------------------------ 6. magic square

def magic():
    sq = al.magic_square()
    FACTS["magic"] = sq
    order = al.ORDER
    cell = 104
    pad = 96
    W = pad + cell * 7 + 24
    H = pad + cell * 7 + 84
    b = [txt(24, 38, "The magic square", INK, 21, "start", "700"),
         txt(24, 58, "dim = tri(A) + tri(B) + 3 · dim A · dim B — one formula fills all "
                     "forty-nine boxes", MUTE, 12.5, "start")]
    for j, tag in enumerate(order):
        b.append(txt(pad + j * cell + cell / 2, pad - 14, tag, DIM[tag], 16, "middle", "800"))
    for i, a in enumerate(order):
        b.append(txt(pad - 16, pad + i * cell + cell / 2 + 5, a, DIM[a], 16, "end", "800"))
        for j, bb in enumerate(order):
            c = sq[i][j]
            x, y = pad + j * cell, pad + i * cell
            big = c["dim"] >= 52
            fill = "#191a26" if not big else "#1e2030"
            edge = HOT if c["name"].startswith("e8") else (
                COOL if c["name"].startswith("e7") else (
                    ROSE if c["name"].startswith("e6") else (
                        VIOLET if c["name"].startswith("f4") else (INK if big else LINE))))
            exc = c["name"][0] in "ef"
            b.append(f'<rect x="{x}" y="{y}" width="{cell - 6}" height="{cell - 6}" rx="7" '
                     f'fill="{fill}" stroke="{edge if exc else LINE}" '
                     f'stroke-width="{2 if exc else 1}"/>')
            b.append(txt(x + (cell - 6) / 2, y + 40, c["name"], INK if big else MUTE,
                         16 if big else 13.5, "middle", "800" if big else "600"))
            b.append(txt(x + (cell - 6) / 2, y + 64, str(c["dim"]), edge if big else MUTE, 20 if big else 15,
                         "middle", "800"))
            b.append(txt(x + (cell - 6) / 2, y + 84, f'{c["tri_a"]}+{c["tri_b"]}+{c["prod"]}',
                         MUTE, 10.5, "middle", "400", family="ui-monospace,Menlo,monospace"))
    b.append(txt(24, H - 34, "top-left quarter: the four division algebras. "
                             "right and bottom: their split cousins, which give the other real forms.",
                 MUTE, 12.5, "start"))
    return svg("magic.svg", W, H, "".join(b), "The magic square of Lie algebras",
               "A seven by seven grid. Each box names a Lie algebra and its dimension, with the "
               "arithmetic that produced it underneath. The four corners of the top-left quarter "
               "run from su(2) at three dimensions to e8 at two hundred and forty-eight.")


def eigen():
    rows = al.EIGEN
    W, H = 920, 436
    b = [txt(24, 38, "Cut three ways", INK, 21, "start", "700"),
         txt(24, 58, "a triality automorphism splits each of these into a fixed part and two "
                     "equal halves that trade places", MUTE, 12.5, "start")]
    x0, bw = 190, 480
    top = 96
    rowh = 46
    mx = max(r["total"] for r in rows)
    for i, r in enumerate(rows):
        y = top + i * rowh
        b.append(txt(24, y + 26, r["g"], INK, 17, "start", "800"))
        b.append(txt(x0 - 12, y + 26, f'{r["total"]}', MUTE, 13.5, "end"))
        w0 = bw * r["fixed_dim"] / mx
        w1 = bw * r["moving_dim"] / mx
        b.append(f'<rect x="{x0}" y="{y + 8}" width="{w0:.1f}" height="26" fill="{C0}"/>')
        b.append(f'<rect x="{x0 + w0:.1f}" y="{y + 8}" width="{w1:.1f}" height="26" fill="{C1}"/>')
        b.append(f'<rect x="{x0 + w0 + w1:.1f}" y="{y + 8}" width="{w1:.1f}" height="26" fill="{C2}"/>')
        b.append(txt(x0 + w0 / 2, y + 26, str(r["fixed_dim"]), "#0a0a10", 12.5, "middle", "700"))
        b.append(txt(x0 + w0 + w1 / 2, y + 26, str(r["moving_dim"]), "#0a0a10", 12.5, "middle", "700"))
        b.append(txt(x0 + w0 + 1.5 * w1, y + 26, str(r["moving_dim"]), "#0a0a10", 12.5, "middle", "700"))
        b.append(txt(x0 + bw + 16, y + 26, r["fixed"], MUTE, 11.5, "start"))
    b.append(txt(24, H - 26, "the fixed part is a subalgebra; the two halves are where the "
                             "three generations would live", MUTE, 12.5, "start"))
    return svg("eigen.svg", W, H, "".join(b), "The three-way split of each triality algebra",
               "Six stacked bars, one each for su(3), sp(3), f4, e6, e7 and e8. Each bar has a "
               "fixed part and two equal moving parts whose lengths add to the algebra's dimension.")


def su3d():
    """su(3, D) = tri(D) + three copies of D."""
    W, H = 880, 250
    b = [txt(24, 38, "One shape, four sizes", INK, 21, "start", "700"),
         txt(24, 58, "tri(D) plus three copies of D — the triality Lie algebras", MUTE, 12.5, "start")]
    x = 40
    for tag in ["R", "C", "H", "O"]:
        name = al.TRIALITY_ALGEBRA[tag]
        t, d = al.TRI[tag], al.DIM[tag]
        total = t + 3 * d
        col = DIM[tag]
        w = 180
        b.append(f'<rect x="{x}" y="100" width="{w}" height="94" rx="8" fill="{PANEL}" stroke="{col}"/>')
        b.append(txt(x + w / 2, 128, name, INK, 20, "middle", "800"))
        b.append(txt(x + w / 2, 152, f"{t} + 3 × {d} = {total}", col, 14, "middle", "700",
                     family="ui-monospace,Menlo,monospace"))
        b.append(txt(x + w / 2, 176, f"tri({tag}) + {tag}+{tag}+{tag}", MUTE, 12))
        b.append(txt(x + w / 2, 212, {"R": "the reals", "C": "the complex numbers",
                                      "H": "the quaternions", "O": "the octonions"}[tag], MUTE, 12))
        x += w + 20
    return svg("su3d.svg", W, H, "".join(b), "The four triality Lie algebras",
               "Four boxes: su(2) is 0 plus three ones; su(3) is 2 plus three twos; sp(3) is 9 plus "
               "three fours; f4 is 28 plus three eights, which is fifty-two.")


def export_data():
    """One source of truth for the tables and the shadows: the browser reads the same
    numbers the figures were drawn from."""
    out = BUILD / "data"
    out.mkdir(parents=True, exist_ok=True)
    tabs = {}
    for A in al.ALL:
        tabs[A.tag] = {"n": A.n, "name": A.name, "sig": list(A.sig),
                       "table": [[[s, c] for s, c in row] for row in A.table]}
    (out / "algebra.json").write_text(json.dumps(
        {"tables": tabs, "fano": [list(t) for t in al.fano_lines()],
         "magic": al.magic_square(), "order": al.ORDER,
         "tri": al.TRI, "dim": al.DIM, "eigen": al.EIGEN}), encoding="utf-8")

    systems = {}
    for name, R in rt.SYSTEMS.items():
        p = rt.project(R)
        pts = p["points"]
        scale = float(np.linalg.norm(pts, axis=1).max())
        entry = {"h": int(p["h"]), "n": int(len(R)),
                 "rank": int(np.linalg.matrix_rank(R)),
                 "pts": [[round(float(x / scale), 5), round(float(y / scale), 5)] for x, y in pts],
                 "edges": []}
        # the 60-degree neighbours, for the line drawing
        pairs = []
        for i in range(len(R)):
            for j in range(i + 1, len(R)):
                if abs(float(R[i] @ R[j]) - 1.0) < 1e-9:
                    pairs.append([i, j])
        entry["edges"] = pairs
        if name == "E8":
            simple = rt.simple_roots(R)
            _, m = rt.z3_grading(R, simple)
            entry["z3"] = [int(v) for v in m]
            entry["whole"] = [int(v) for v in rt.two_grading(R)]
        systems[name] = entry
    (out / "roots.json").write_text(json.dumps(systems), encoding="utf-8")
    kb = sum(f.stat().st_size for f in out.glob("*.json")) / 1024
    return round(kb)


def main():
    ladder()
    fano()
    tables()
    shadows()
    m = e8_z3()
    three_eights()
    dynkin()
    rotation()
    magic()
    eigen()
    su3d()
    hero(m)
    FACTS["data_kb"] = export_data()

    # numbers the pages quote
    worst = al.triality_is_cyclic(al.O, 4000)
    cases, bad, rnd, miss = al.reflection_flips_sign(al.O, exact_each=120, random_units=3000)
    FACTS["triality_cyclic"] = {"trials": 4000, "worst_gap": worst}
    FACTS["reflection"] = {"exact_cases": cases, "failures": bad, "random_units": rnd,
                           "worst_miss": miss}
    FACTS["tri_dims"] = {k: {"tri": al.TRI[k], "dim": al.DIM[k], "algebra": al.TRIALITY_ALGEBRA[k],
                             "total": al.TRI[k] + 3 * al.DIM[k]} for k in al.ORDER}
    FACTS["eigen"] = al.EIGEN
    imgs, cube = al.quaternion_triality_cycle()
    FACTS["quaternion_cycle"] = {"images": [[str(v) for v in im] for im in imgs],
                                 "cube": [str(v) for v in cube]}
    fails_a, lines_a = al.check_all(verbose=False)
    fails_r, lines_r = rt.check_all(verbose=False)
    FACTS["checks"] = {"algebra": {"total": len(lines_a), "failures": fails_a, "lines": lines_a},
                       "roots": {"total": len(lines_r), "failures": fails_r, "lines": lines_r}}
    FACTS["checks"]["total"] = len(lines_a) + len(lines_r)
    FACTS["checks"]["failures"] = fails_a + fails_r
    (BUILD / "facts.json").write_text(json.dumps(FACTS, indent=1, default=float), encoding="utf-8")
    n = len(list(IMG.glob("*.svg"))) + len(list(IMG.glob("*.png")))
    print(f"build/img ← {n} figures · facts.json ← {FACTS['checks']['total']} checks, "
          f"{FACTS['checks']['failures']} failing")


if __name__ == "__main__":
    main()
