# Exceptional Magic

Eight ways to multiply, and where they get you: the octonions, triality, the magic square
and E8 — drawn from the arithmetic and told plain. A reading of one paper, with everything in
it recomputed here.

**Live:** https://nanobotco.github.io/exceptional-magic/

## The paper

A. Garrett Lisi, *Division Algebras, Triality, and Exceptional Magic*,
arXiv:2609.12112v1 [math-ph], 10 September 2026 — https://arxiv.org/abs/2609.12112 —
licensed CC BY-NC-ND 4.0.

That licence permits no derivatives, and this site is not one. No text, equation image or
figure from the paper is reproduced. The mathematics is recomputed from the definitions in
`tools/`; the paper is cited by section wherever it is the reason a topic appears; its 34
references are transcribed with links on the credit page. Read the paper first.

## What is on it

- **Numbers** — the four division algebras, the Cayley–Dickson ladder that builds them, what
  each doubling costs (measured on random elements, not asserted), and a multiplier that
  breaks associativity on demand.
- **Wheel** — the octonion table is the Fano plane. Seven lines found by walking the table;
  click two units and the line lights up.
- **Triality** — the cyclic form T(v, ψ, χ), checked three ways round on thousands of random
  triples; the 8v → 8c → 8s cycle of so(8), built from the diagram symmetry and verified;
  su(3, 𝔻) = tri(𝔻) + 3𝔻 for all four algebras.
- **Square** — the magic square, all forty-nine boxes from
  `dim = tri(A) + tri(B) + 3·dim A·dim B`, each checked against the algebra it names.
- **E8** — G2, D4, F4, E6, E7, E8 built from their definitions and projected onto the Coxeter
  plane (eight rings of thirty), turnable in the browser; the triality split 92 + 78 + 78
  found by search and checked on 13,440 root sums; the two-grading 120 + 128.
- **Physics** — what it is all supposed to be for, with the objections on the same page.
- **Checks** — the 139 arithmetic checks that run before the site will publish, listed.
- **Gallery · Credit** — every figure, downloadable; every source, linked.

## Build

```
python3 tools/algebra.py    # the algebra checks, printed
python3 tools/roots.py      # the root-system checks, printed
python3 tools/figures.py    # every figure (SVG, JPG), build/facts.json, build/data/
python3 tools/site.py       # the pages, into build/site/
./publish.sh                # all of it, gated, into docs/
python3 tools/serve.py 8849 # a local preview, mounted at /exceptional-magic/
```

Python 3.9+, numpy, Pillow. Static HTML with the stylesheet inlined; the scripts in `js/`
read the same JSON the figures were drawn from.

## Terms

Text and figures CC BY 4.0 — credit line `Nan · hongdam.net · CC BY 4.0` with a link back.
Code MIT. See `NOTICE.txt`.
