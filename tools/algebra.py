#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""algebra.py — the division algebras, their trialities, and the magic square,
computed from the multiplication tables rather than looked up.

Everything the site states as a number comes out of here and is checked here.
Run it alone to see the checks:

    python3 tools/algebra.py
"""
from __future__ import annotations

import itertools
import random
from fractions import Fraction

# ---------------------------------------------------------------- Cayley-Dickson

def cd_mul(a, b):
    """Cayley-Dickson product of two tuples of equal power-of-two length.

    (p,q)(r,s) = (pr - s~q, sp + q r~).  One line of recursion builds the reals,
    the complexes, the quaternions, the octonions, and everything past them.
    """
    n = len(a)
    if n == 1:
        return (a[0] * b[0],)
    h = n // 2
    p, q = a[:h], a[h:]
    r, s = b[:h], b[h:]
    left = sub(cd_mul(p, r), cd_mul(conj(s), q))
    right = add(cd_mul(s, p), cd_mul(q, conj(r)))
    return left + right


def conj(a):
    return (a[0],) + tuple(-x for x in a[1:])


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm2(a):
    return sum(x * x for x in a)


def unit(n, i):
    return tuple(1 if j == i else 0 for j in range(n))


def table(n):
    """The n x n multiplication table of the Cayley-Dickson algebra of dimension n,
    as (sign, index) pairs."""
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            p = cd_mul(unit(n, i), unit(n, j))
            k = next(t for t, v in enumerate(p) if v)
            row.append((p[k], k))
            assert sum(1 for v in p if v) == 1
        out.append(row)
    return out


# ---------------------------------------------------- the tables the paper prints

# Lisi (arXiv:2609.12112v1) §2 prints these tables; they are transcribed here as the
# structure constants M_ab^c, then checked against the laws below. Split algebras
# carry a signature: n_aa = +1 for a spacelike basis element, -1 for a timelike one.

def _parse(rows):
    out = []
    for r in rows:
        row = []
        for t in r.split():
            row.append((-1, int(t[2:])) if t[0] == "-" else (1, int(t[1:])))
        out.append(row)
    return out


O_TABLE = _parse([
    "e0  e1  e2  e3  e4  e5  e6  e7",
    "e1 -e0  e4  e7 -e2  e6 -e5 -e3",
    "e2 -e4 -e0  e5  e1 -e3  e7 -e6",
    "e3 -e7 -e5 -e0  e6  e2 -e4  e1",
    "e4  e2 -e1 -e6 -e0  e7  e3 -e5",
    "e5 -e6  e3 -e2 -e7 -e0  e1  e4",
    "e6  e5 -e7  e4 -e3 -e1 -e0  e2",
    "e7  e3  e6 -e1  e5 -e4 -e2 -e0",
])

OS_TABLE = _parse([          # the split octonions, O'
    "e0  e1  e2  e3  e4  e5  e6  e7",
    "e1 -e0  e3 -e2 -e5  e4 -e7  e6",
    "e2 -e3 -e0  e1 -e6  e7  e4 -e5",
    "e3  e2 -e1 -e0 -e7 -e6  e5  e4",
    "e4  e5  e6  e7  e0  e1  e2  e3",
    "e5 -e4 -e7  e6 -e1  e0  e3 -e2",
    "e6  e7 -e4 -e5 -e2 -e3  e0  e1",
    "e7 -e6  e5 -e4 -e3  e2 -e1  e0",
])

H_TABLE = _parse([
    "e0  e1  e2  e3",
    "e1 -e0  e3 -e2",
    "e2 -e3 -e0  e1",
    "e3  e2 -e1 -e0",
])

HS_TABLE = _parse([          # the split quaternions, H'
    "e0  e1  e2  e3",
    "e1  e0  e3  e2",
    "e2 -e3 -e0  e1",
    "e3 -e2 -e1  e0",
])

C_TABLE = _parse(["e0  e1", "e1 -e0"])
CS_TABLE = _parse(["e0  e1", "e1  e0"])      # the split complexes, C'
R_TABLE = _parse(["e0"])


class Algebra:
    """A composition algebra given by its multiplication table."""

    def __init__(self, name, tag, tbl, split=False):
        self.name, self.tag, self.table, self.split = name, tag, tbl, split
        self.n = len(tbl)
        # signature: e_a~ e_a = n_aa. Read it off the table's diagonal.
        self.sig = tuple(1 if a == 0 else (-tbl[a][a][0]) for a in range(self.n))

    def mul(self, x, y):
        out = [0] * self.n
        for a, xa in enumerate(x):
            if not xa:
                continue
            for b, yb in enumerate(y):
                if not yb:
                    continue
                s, c = self.table[a][b]
                out[c] += s * xa * yb
        return tuple(out)

    def conj(self, x):
        return (x[0],) + tuple(-v for v in x[1:])

    def form(self, x, y):
        """The metric (x,y) = 1/2 (x~y + y~x), read off the scalar part."""
        return sum(self.sig[a] * x[a] * y[a] for a in range(self.n))

    def norm2(self, x):
        return self.form(x, x)

    def e(self, i):
        return unit(self.n, i)

    def rand(self, rng, lo=-4, hi=4):
        return tuple(rng.randint(lo, hi) for _ in range(self.n))


R = Algebra("the reals", "R", R_TABLE)
C = Algebra("the complex numbers", "C", C_TABLE)
H = Algebra("the quaternions", "H", H_TABLE)
O = Algebra("the octonions", "O", O_TABLE)
CS = Algebra("the split complexes", "C'", CS_TABLE, split=True)
HS = Algebra("the split quaternions", "H'", HS_TABLE, split=True)
OS = Algebra("the split octonions", "O'", OS_TABLE, split=True)

ALL = [R, C, H, O, CS, HS, OS]
DIVISION = [R, C, H, O]


# ------------------------------------------------------------------- the laws

def commutes(A, x, y):
    return A.mul(x, y) == A.mul(y, x)


def associates(A, x, y, z):
    return A.mul(A.mul(x, y), z) == A.mul(x, A.mul(y, z))


def associator(A, x, y, z):
    return sub(A.mul(A.mul(x, y), z), A.mul(x, A.mul(y, z)))


def alternative(A, x, y):
    """(xx)y = x(xy) and (yx)x = y(xx) — the weak form of associativity that
    survives all the way up to the octonions."""
    return (associator(A, x, x, y) == (0,) * A.n
            and associator(A, y, x, x) == (0,) * A.n)


def composes(A, x, y):
    """|xy| = |x||y| — the law that picks out 1, 2, 4 and 8."""
    return A.norm2(A.mul(x, y)) == A.norm2(x) * A.norm2(y)


def law_survey(trials=4000, seed=20260923):
    """Measure, don't assert: how often each law holds on random elements of each
    algebra, and of the 16-dimensional sedenions past the end of the ladder."""
    rng = random.Random(seed)
    rows = []
    cd = {16: "the sedenions"}
    for A in [R, C, H, O]:
        hits = {"commutative": 0, "associative": 0, "alternative": 0, "composition": 0}
        for _ in range(trials):
            x, y, z = A.rand(rng), A.rand(rng), A.rand(rng)
            hits["commutative"] += commutes(A, x, y)
            hits["associative"] += associates(A, x, y, z)
            hits["alternative"] += alternative(A, x, y)
            hits["composition"] += composes(A, x, y)
        rows.append({"algebra": A.tag, "name": A.name, "dim": A.n, "trials": trials,
                     **{k: v for k, v in hits.items()}})
    # one rung past the octonions
    hits = {"commutative": 0, "associative": 0, "alternative": 0, "composition": 0}
    for _ in range(trials):
        x = tuple(rng.randint(-4, 4) for _ in range(16))
        y = tuple(rng.randint(-4, 4) for _ in range(16))
        z = tuple(rng.randint(-4, 4) for _ in range(16))
        hits["commutative"] += cd_mul(x, y) == cd_mul(y, x)
        hits["associative"] += cd_mul(cd_mul(x, y), z) == cd_mul(x, cd_mul(y, z))
        hits["alternative"] += (sub(cd_mul(cd_mul(x, x), y), cd_mul(x, cd_mul(x, y))) == (0,) * 16
                                and sub(cd_mul(cd_mul(y, x), x), cd_mul(y, cd_mul(x, x))) == (0,) * 16)
        hits["composition"] += norm2(cd_mul(x, y)) == norm2(x) * norm2(y)
    rows.append({"algebra": "S", "name": "the sedenions", "dim": 16, "trials": trials, **hits})
    return rows


def zero_divisors(limit=None):
    """Pairs of sedenion basis-plane elements whose product vanishes. Hunted, not
    quoted: (e_a + e_b)(e_c + e_d) = 0 with all four basis units distinct."""
    found = []
    units = [unit(16, i) for i in range(16)]
    for a, b in itertools.combinations(range(1, 16), 2):
        x = add(units[a], units[b])
        for c, d in itertools.combinations(range(1, 16), 2):
            y = add(units[c], units[d])
            if cd_mul(x, y) == (0,) * 16:
                found.append(((a, b), (c, d)))
                if limit and len(found) >= limit:
                    return found
    return found


# --------------------------------------------------------------- the Fano plane

def fano_lines(A=O):
    """The seven lines of the octonion table, found by following the table rather
    than by drawing a picture: triples (a,b,c) with e_a e_b = e_c cyclically."""
    lines = set()
    for a in range(1, A.n):
        for b in range(1, A.n):
            if a == b:
                continue
            s, c = A.table[a][b]
            if s == 1 and c != 0:
                s2, c2 = A.table[b][c]
                s3, c3 = A.table[c][a]
                if (s2, c2) == (1, a) and (s3, c3) == (1, b):
                    lines.add(tuple(sorted((a, b, c))) + (a, b, c))
    # keep one oriented representative per unordered triple
    seen, out = set(), []
    for t in sorted(lines):
        key = t[:3]
        if key in seen:
            continue
        seen.add(key)
        out.append(t[3:])
    return out


# ------------------------------------------------------------------- triality

def triality(A, v, psi, chi):
    """T(v, psi, chi) = (chi~, v psi) — a real, cyclic, trilinear form.
    Lisi eq. (3.1); the cyclic symmetry is the thing this site is about."""
    return A.form(A.conj(chi), A.mul(v, psi))


def triality_is_cyclic(A, trials=3000, seed=7):
    """Check T(v,psi,chi) = T(psi,chi,v) = T(chi,v,psi) on random triples."""
    rng = random.Random(seed)
    worst = 0
    for _ in range(trials):
        v, p, c = A.rand(rng), A.rand(rng), A.rand(rng)
        t1 = triality(A, v, p, c)
        t2 = triality(A, p, c, v)
        t3 = triality(A, c, v, p)
        worst = max(worst, abs(t1 - t2), abs(t1 - t3))
    return worst


def reflection_flips_sign(A, exact_each=200, random_units=3000, seed=11):
    """A reflection through a unit u sends (v, psi, chi) to (-u v~ u, u~ chi~, psi~ u~)
    and turns T into -T. Lisi eq. (3.2). Two passes: exact integer arithmetic on every
    signed basis unit, then floating point on random unit elements.

    Returns (exact_cases, exact_failures, random_cases, worst_miss).
    """
    import math
    rng = random.Random(seed)
    n = A.n

    def refl(u, v, p, c, mul, cj):
        return (tuple(-x for x in mul(mul(u, cj(v)), u)), mul(cj(u), cj(c)), mul(cj(p), cj(u)))

    cases = fails = 0
    for a in range(n):
        for sgn in (1, -1):
            u = tuple(sgn if i == a else 0 for i in range(n))
            if A.norm2(u) != 1:
                continue
            for _ in range(exact_each):
                v, p, c = A.rand(rng, -3, 3), A.rand(rng, -3, 3), A.rand(rng, -3, 3)
                v2, p2, c2 = refl(u, v, p, c, A.mul, A.conj)
                cases += 1
                fails += triality(A, v2, p2, c2) != -triality(A, v, p, c)

    def fmul(x, y):
        out = [0.0] * n
        for a, xa in enumerate(x):
            if not xa:
                continue
            for b, yb in enumerate(y):
                if not yb:
                    continue
                s, c = A.table[a][b]
                out[c] += s * xa * yb
        return tuple(out)

    def fcj(x):
        return (x[0],) + tuple(-v for v in x[1:])

    def fform(x, y):
        return sum(A.sig[i] * x[i] * y[i] for i in range(n))

    worst = 0.0
    for _ in range(random_units):
        u = [rng.gauss(0, 1) for _ in range(n)]
        q = sum(A.sig[i] * u[i] * u[i] for i in range(n))
        if q <= 0:
            continue                      # split algebras have null and timelike directions
        u = tuple(t / math.sqrt(q) for t in u)
        v = tuple(rng.gauss(0, 1) for _ in range(n))
        p = tuple(rng.gauss(0, 1) for _ in range(n))
        c = tuple(rng.gauss(0, 1) for _ in range(n))
        v2, p2, c2 = refl(u, v, p, c, fmul, fcj)
        worst = max(worst, abs(fform(fcj(c2), fmul(v2, p2)) + fform(fcj(c), fmul(v, p))))
    return cases, fails, random_units, worst


def quaternion_triality_cycle():
    """t = -1/2 (e0+e1+e2+e3) cycles the three imaginary units by conjugation, and
    t^3 = 1. Lisi §11. Done in halves so it stays exact in integers."""
    A = H
    t = (Fraction(-1, 2),) * 1 + (Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2))
    def mulf(x, y):
        out = [Fraction(0)] * 4
        for a, xa in enumerate(x):
            for b, yb in enumerate(y):
                s, c = A.table[a][b]
                out[c] += s * xa * yb
        return tuple(out)
    tin = A.conj(t)                     # t~ = t^-1 for a unit
    def ad(x):
        return mulf(mulf(t, x), tin)
    imgs = [ad(tuple(Fraction(v) for v in A.e(i))) for i in (1, 2, 3)]
    cube = mulf(mulf(t, t), t)
    return imgs, cube


# --------------------------------------------------- triality algebras, magic square

# dim tri(D): the Lie algebra of the triality group of each algebra.
#   tri(R) = 0, tri(C) = u(1)+u(1) = 2, tri(H) = 3 su(2) = 9, tri(O) = so(8) = 28.
# Checked below against su(3,D) = tri(D) + 3 D.
TRI = {"R": 0, "C": 2, "H": 9, "O": 28, "C'": 2, "H'": 9, "O'": 28}
DIM = {"R": 1, "C": 2, "H": 4, "O": 8, "C'": 2, "H'": 4, "O'": 8}

TRIALITY_ALGEBRA = {"R": "su(2)", "C": "su(3)", "H": "sp(3)", "O": "f4",
                    "C'": "sl(3)", "H'": "sp(6,R)", "O'": "f4(4)"}

ORDER = ["R", "C", "H", "O", "C'", "H'", "O'"]

# Lisi Table 6 — the magic square, including the split rows and columns.
MAGIC_NAMES = {
    ("R", "R"): "su(2)",     ("R", "C"): "su(3)",      ("R", "H"): "sp(3)",      ("R", "O"): "f4",
    ("C", "C"): "2 su(3)",   ("C", "H"): "su(6)",      ("C", "O"): "e6",
    ("H", "H"): "so(12)",    ("H", "O"): "e7",
    ("O", "O"): "e8",
    ("R", "C'"): "sl(3)",    ("R", "H'"): "sp(6,R)",   ("R", "O'"): "f4(4)",
    ("C", "C'"): "sl(3,C)",  ("C", "H'"): "su(3,3)",   ("C", "O'"): "e6(2)",
    ("H", "C'"): "sl(3,H)",  ("H", "H'"): "sp(6,H)",   ("H", "O'"): "e7(-5)",
    ("O", "C'"): "e6(-26)",  ("O", "H'"): "e7(-25)",   ("O", "O'"): "e8(-24)",
    ("C'", "C'"): "2 sl(3)", ("C'", "H'"): "sl(6,R)",  ("C'", "O'"): "e6(6)",
    ("H'", "H'"): "so(6,6)", ("H'", "O'"): "e7(7)",
    ("O'", "O'"): "e8(8)",
}


def magic_dim(a, b):
    """dim L(A,B) = tri(A) + tri(B) + 3 dim(A) dim(B).  One formula fills the square."""
    return TRI[a] + TRI[b] + 3 * DIM[a] * DIM[b]


def magic_square():
    rows = []
    for a in ORDER:
        row = []
        for b in ORDER:
            key = (a, b) if (a, b) in MAGIC_NAMES else (b, a)
            row.append({"a": a, "b": b, "name": MAGIC_NAMES.get(key, "?"),
                        "dim": magic_dim(a, b),
                        "tri_a": TRI[a], "tri_b": TRI[b],
                        "prod": 3 * DIM[a] * DIM[b]})
        rows.append(row)
    return rows


# known dimensions, to check the formula against
KNOWN_DIM = {"su(2)": 3, "su(3)": 8, "sp(3)": 21, "f4": 52, "2 su(3)": 16, "su(6)": 35,
             "e6": 78, "so(12)": 66, "e7": 133, "e8": 248, "sl(3)": 8, "sp(6,R)": 21,
             "f4(4)": 52, "sl(3,C)": 16, "su(3,3)": 35, "e6(2)": 78, "sl(3,H)": 35,
             "sp(6,H)": 66, "e7(-5)": 133, "e6(-26)": 78, "e7(-25)": 133, "e8(-24)": 248,
             "2 sl(3)": 16, "sl(6,R)": 35, "e6(6)": 78, "so(6,6)": 66, "e7(7)": 133,
             "e8(8)": 248}


# --------------------------------------------- the three-way split (Vinberg, Z3)

# Lisi eq. (6.1): a triality automorphism cuts each algebra into three eigenspaces,
# g = g_-1 + g_0 + g_+1, with dim g_-1 = dim g_+1. The parts are named in the paper;
# their dimensions are added up here and checked against the whole.
EIGEN = [
    {"g": "su(3)", "total": 8, "fixed": "u(1) + u(1)", "fixed_dim": 2,
     "moving": "1 + 1 + 1", "moving_dim": 3},
    {"g": "sp(3)", "total": 21, "fixed": "so(4) + u(1)", "fixed_dim": 7,
     "moving": "3 + 4", "moving_dim": 7},
    {"g": "f4", "total": 52, "fixed": "so(7) + u(1)", "fixed_dim": 22,
     "moving": "7 + 8", "moving_dim": 15},
    {"g": "e6", "total": 78, "fixed": "so(8) + u(1) + u(1)", "fixed_dim": 30,
     "moving": "8v + 8s+ + 8s-", "moving_dim": 24},
    {"g": "e7", "total": 133, "fixed": "so(10) + su(2) + u(1)", "fixed_dim": 49,
     "moving": "10 + 2x16", "moving_dim": 42},
    {"g": "e8", "total": 248, "fixed": "so(14) + u(1)", "fixed_dim": 92,
     "moving": "14 + 64", "moving_dim": 78},
]


def check_all(verbose=True):
    """Every claim the site makes about these algebras, checked here first."""
    out, fails = [], 0

    def say(ok, line):
        nonlocal fails
        fails += not ok
        out.append(("ok  " if ok else "FAIL") + "  " + line)

    # the tables are what they say they are
    for A in ALL:
        rng = random.Random(3)
        alt = all(alternative(A, A.rand(rng), A.rand(rng)) for _ in range(500))
        comp = all(composes(A, A.rand(rng), A.rand(rng)) for _ in range(500))
        say(alt, f"{A.tag}: alternative")
        say(comp, f"{A.tag}: |xy| = |x||y|")
        say(all(A.mul(A.e(0), A.e(i)) == A.e(i) for i in range(A.n)), f"{A.tag}: e0 is the unit")

    # Cayley-Dickson reproduces the same laws at 1, 2, 4, 8 and breaks at 16
    surv = law_survey(trials=800)
    say(surv[3]["composition"] == 800, "O: composition holds on 800 random pairs")
    say(surv[4]["composition"] < 800, "S: composition fails past dimension 8")
    say(len(zero_divisors(limit=1)) == 1, "S: a pair of nonzero sedenions multiplying to zero")

    # the Fano plane
    lines = fano_lines()
    say(len(lines) == 7, f"O: {len(lines)} lines in the table")
    say(sorted(set(itertools.chain(*[l for l in lines]))) == list(range(1, 8)),
        "O: the seven lines cover the seven imaginary units")
    say(all(sum(1 for l in lines if i in l) == 3 for i in range(1, 8)),
        "O: each imaginary unit lies on three lines")

    # triality
    for A in DIVISION[1:] + [CS, HS, OS]:
        say(triality_is_cyclic(A, 600) == 0, f"{A.tag}: T(v,psi,chi) is cyclic")
    cases, bad, rnd, worst = reflection_flips_sign(O, exact_each=60, random_units=1500)
    say(bad == 0 and cases > 0, f"O: a reflection flips the sign of T ({cases} exact cases)")
    say(worst < 1e-9, f"O: and on {rnd} random unit octonions, worst miss {worst:.1e}")

    imgs, cube = quaternion_triality_cycle()
    say(imgs[0] == tuple(Fraction(v) for v in H.e(2))
        and imgs[1] == tuple(Fraction(v) for v in H.e(3))
        and imgs[2] == tuple(Fraction(v) for v in H.e(1)), "H: t cycles e1 -> e2 -> e3 -> e1")
    say(cube == tuple(Fraction(v) for v in H.e(0)), "H: t^3 = 1")

    # su(3, D) = tri(D) + 3D
    for tag, name in TRIALITY_ALGEBRA.items():
        say(TRI[tag] + 3 * DIM[tag] == KNOWN_DIM[name],
            f"su(3,{tag}) = tri({tag}) + 3x{DIM[tag]} = {KNOWN_DIM[name]} = {name}")

    # the magic square, from one formula
    for row in magic_square():
        for c in row:
            say(c["dim"] == KNOWN_DIM[c["name"]],
                f"L({c['a']},{c['b']}) = {c['tri_a']}+{c['tri_b']}+{c['prod']} = {c['dim']} = {c['name']}")

    # the three-way split adds back up
    for e in EIGEN:
        say(e["fixed_dim"] + 2 * e["moving_dim"] == e["total"],
            f"{e['g']}: {e['fixed_dim']} + 2 x {e['moving_dim']} = {e['total']}")

    if verbose:
        for line in out:
            print(line)
        print(f"\n{len(out) - fails}/{len(out)} checks pass")
    return fails, out


if __name__ == "__main__":
    import sys
    fails, _ = check_all()
    sys.exit(1 if fails else 0)
