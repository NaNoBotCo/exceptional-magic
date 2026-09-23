#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""roots.py — the exceptional root systems, and the Coxeter-plane shadow of each.

The rings you see on the site are not a traced picture. Each root system is built
from its own definition, the Coxeter element is multiplied out, its eigenvector for
e^(2 pi i / h) gives the plane, and every root is dropped onto it.

    python3 tools/roots.py
"""
from __future__ import annotations

import itertools
import math

import numpy as np

# ------------------------------------------------------------------ root systems


def e8_roots():
    out = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            v = np.zeros(8)
            v[i], v[j] = si, sj
            out.append(v)
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            out.append(np.array(signs, float) / 2)
    return np.array(out)


def d4_roots():
    out = []
    for i, j in itertools.combinations(range(4), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            v = np.zeros(4)
            v[i], v[j] = si, sj
            out.append(v)
    return np.array(out)


def f4_roots():
    out = [v for v in d4_roots()]
    for i in range(4):
        for s in (1, -1):
            v = np.zeros(4)
            v[i] = s
            out.append(v)
    for signs in itertools.product((1, -1), repeat=4):
        out.append(np.array(signs, float) / 2)
    return np.array(out)


def g2_roots():
    """Drawn in its own plane: six short at 60-degree steps, six long between them."""
    out = []
    for k in range(6):
        th = math.radians(60 * k)
        out.append(np.array([math.cos(th), math.sin(th)]))
        th2 = math.radians(60 * k + 30)
        out.append(math.sqrt(3) * np.array([math.cos(th2), math.sin(th2)]))
    return np.array(out)


def orthogonal_subsystem(roots, fixed):
    """The roots orthogonal to every vector in `fixed` — how E7 and E6 sit inside E8."""
    keep = [r for r in roots if all(abs(r @ f) < 1e-9 for f in fixed)]
    return np.array(keep)


def in_own_span(roots):
    """Re-express a root system in an orthonormal basis of the space it spans, so its
    rank is its dimension. E7 and E6 arrive as subsets of E8 living in 8 coordinates."""
    u, s, vt = np.linalg.svd(roots)
    rank = int((s > 1e-9).sum())
    basis = vt[:rank]
    return roots @ basis.T


E8 = e8_roots()
E7 = in_own_span(orthogonal_subsystem(E8, [E8[0]]))
# E6 is what is left orthogonal to a pair of roots meeting at 120 degrees — an A2.
_a = E8[0]
_b = next(r for r in E8 if abs(r @ _a + 1) < 1e-9)
E6 = in_own_span(orthogonal_subsystem(E8, [_a, _b]))
D4 = d4_roots()
F4 = f4_roots()
G2 = g2_roots()


# ------------------------------------------------------------- simple roots, Coxeter

def simple_roots(roots):
    """A set of simple roots, found by cutting the root system with a generic
    hyperplane and keeping the positive roots that are not sums of two others."""
    d = roots.shape[1]
    rng = np.random.default_rng(12)
    while True:
        h = rng.normal(size=d)
        if all(abs(r @ h) > 1e-6 for r in roots):
            break
    pos = [r for r in roots if r @ h > 0]
    simple = []
    for r in pos:
        if not any(np.allclose(r, a + b) for a, b in itertools.combinations(pos, 2)):
            simple.append(r)
    return np.array(simple)


def reflection(alpha, d):
    return np.eye(d) - 2 * np.outer(alpha, alpha) / (alpha @ alpha)


def coxeter_element(simple):
    d = simple.shape[1]
    w = np.eye(d)
    for a in simple:
        w = reflection(a, d) @ w
    return w


def coxeter_number(w, cap=200):
    d = w.shape[0]
    p = w.copy()
    for k in range(1, cap + 1):
        if np.allclose(p, np.eye(d), atol=1e-8):
            return k
        p = p @ w
    return None


def coxeter_plane(w, h):
    """The plane the Coxeter element turns by 2 pi / h — its eigenvector for that
    eigenvalue, split into real and imaginary parts."""
    vals, vecs = np.linalg.eig(w)
    target = np.exp(2j * np.pi / h)
    k = int(np.argmin(np.abs(vals - target)))
    v = vecs[:, k]
    a, b = np.real(v), np.imag(v)
    a = a / np.linalg.norm(a)
    b = b - (b @ a) * a
    b = b / np.linalg.norm(b)
    return a, b


def project(roots, seed_note=""):
    """Roots -> (x, y) in the Coxeter plane, plus the rings they fall into."""
    simple = simple_roots(roots)
    w = coxeter_element(simple)
    h = coxeter_number(w)
    a, b = coxeter_plane(w, h)
    pts = np.array([[r @ a, r @ b] for r in roots])
    rad = np.linalg.norm(pts, axis=1)
    rings = []
    for r in sorted(rad):
        if not rings or abs(r - rings[-1][0]) > 1e-6:
            rings.append([r, 0])
        rings[-1][1] += 1
    return {"points": pts, "h": h, "rings": [(round(r, 6), n) for r, n in rings],
            "simple": simple, "w": w}


SYSTEMS = {"G2": G2, "D4": D4, "F4": F4, "E6": E6, "E7": E7, "E8": E8}
EXPECT_H = {"G2": 6, "D4": 6, "F4": 12, "E6": 12, "E7": 18, "E8": 30}
ALGEBRA_DIM = {"G2": 14, "D4": 28, "F4": 52, "E6": 78, "E7": 133, "E8": 248}


# --------------------------------------------------------------- D4 and triality

def d4_triality():
    """The order-3 symmetry of the D4 diagram, written out as a matrix and checked:
    it turns the 24 roots among themselves and cycles the three eight-dimensional
    representations of so(8)."""
    a = [np.array(v, float) for v in ([1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 1, 1])]
    B = np.array(a).T
    img = np.array([a[2], a[1], a[3], a[0]]).T      # a1 -> a3 -> a4 -> a1, a2 fixed
    J = img @ np.linalg.inv(B)
    v8 = [np.eye(4)[i] * s for i in range(4) for s in (1, -1)]
    s8 = [np.array(c) / 2 for c in itertools.product([1, -1], repeat=4) if list(c).count(-1) % 2 == 0]
    c8 = [np.array(c) / 2 for c in itertools.product([1, -1], repeat=4) if list(c).count(-1) % 2 == 1]

    def st(x):
        return {tuple(np.round(t, 6)) for t in x}

    roots = st(D4)
    checks = {
        "orthogonal": bool(np.allclose(J.T @ J, np.eye(4))),
        "order3": bool(np.allclose(J @ J @ J, np.eye(4))),
        "permutes_roots": all(tuple(np.round(J @ r, 6)) in roots for r in D4),
        "8v_to_8c": st([J @ w for w in v8]) == st(c8),
        "8c_to_8s": st([J @ w for w in c8]) == st(s8),
        "8s_to_8v": st([J @ w for w in s8]) == st(v8),
    }
    return J, {"v": np.array(v8), "s": np.array(s8), "c": np.array(c8)}, checks


# ------------------------------------------------------- gradings of e8

def simple_coords(roots, simple):
    """Every root as integer coefficients on the simple roots."""
    G = simple @ simple.T
    coef = np.array([np.linalg.solve(G, simple @ r) for r in roots])
    out = np.round(coef).astype(int)
    assert np.allclose(out @ simple, roots, atol=1e-8)
    return out


def z3_grading(roots=None, simple=None):
    """A three-way split of e8 of the shape Lisi's triality automorphism produces:
    84 roots fixed, 78 turned one way, 78 the other. Found by sweeping the small
    functionals on the simple roots and counting residues mod 3, not assumed."""
    roots = E8 if roots is None else roots
    simple = simple_roots(roots) if simple is None else simple
    coef = simple_coords(roots, simple)
    for c in itertools.product((0, 1, 2), repeat=coef.shape[1]):
        m = (coef @ np.array(c)) % 3
        if (int((m == 0).sum()), int((m == 1).sum()), int((m == 2).sum())) == (84, 78, 78):
            return np.array(c), m
    raise RuntimeError("no (84, 78, 78) split found")


def grading_violations(roots, m):
    """[g_i, g_j] lands in g_(i+j): checked on every pair of roots whose sum is a root."""
    index = {tuple(np.round(r, 6)): int(k) for r, k in zip(roots, m)}
    bad = tested = 0
    for a, ka in zip(roots, m):
        for b, kb in zip(roots, m):
            s = tuple(np.round(a + b, 6))
            if s in index:
                tested += 1
                bad += index[s] != (int(ka) + int(kb)) % 3
    return tested, bad


def two_grading(roots=None):
    """e8 = so(16) + 128: the roots with whole-number coordinates against the rest."""
    roots = E8 if roots is None else roots
    whole = np.array([all(abs(x - round(x)) < 1e-9 for x in r) for r in roots])
    return whole


def check_all(verbose=True):
    fails, out = 0, []

    def say(ok, line):
        nonlocal fails
        fails += not ok
        out.append(("ok  " if ok else "FAIL") + "  " + line)

    counts = {"G2": 12, "D4": 24, "F4": 48, "E6": 72, "E7": 126, "E8": 240}
    for name, R in SYSTEMS.items():
        say(len(R) == counts[name], f"{name}: {len(R)} roots")
        p = project(R)
        say(p["h"] == EXPECT_H[name], f"{name}: Coxeter number {p['h']}")
        rings = p["rings"]
        inner = [n for r, n in rings if r > 1e-6]
        say(all(n % p["h"] == 0 for n in inner),
            f"{name}: rings of {', '.join(str(n) for n in inner)} on {len(inner)} circles")
        rank = int(np.linalg.matrix_rank(R))
        say(len(p["simple"]) == rank, f"{name}: {len(p['simple'])} simple roots, rank {rank}")
        say(ALGEBRA_DIM[name] == len(R) + rank,
            f"{name}: dim = {len(R)} roots + rank {rank} = {len(R) + rank}")

    c, m = z3_grading()
    counts = (int((m == 0).sum()), int((m == 1).sum()), int((m == 2).sum()))
    say(counts == (84, 78, 78), f"e8: a triality split of {counts[0]} + {counts[1]} + {counts[2]} roots")
    say(int(np.linalg.matrix_rank(E8[m == 0])) == 7,
        "e8: the fixed 84 roots have rank 7 — so(14), and 84 + 8 = 92 with the Cartan")
    tested, bad = grading_violations(E8, m)
    say(bad == 0, f"e8: the split respects brackets on all {tested} root sums")
    whole = two_grading()
    say(int(whole.sum()) == 112 and int((~whole).sum()) == 128,
        f"e8: {int(whole.sum())} + 8 = 120 = so(16), and {int((~whole).sum())} = one spinor")

    J, W, ch = d4_triality()
    for k, v in ch.items():
        say(v, f"D4 triality: {k}")

    if verbose:
        for line in out:
            print(line)
        print(f"\n{len(out) - fails}/{len(out)} checks pass")
    return fails, out


if __name__ == "__main__":
    import sys
    f, _ = check_all()
    sys.exit(1 if f else 0)
