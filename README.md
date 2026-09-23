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

<!-- fleet-roster -->

## Elsewhere from the same publisher

- [Mot Dang](https://motdang.net/) — city directory for Chiang Mai and Chiang Rai
- [The Mae Hong Son Loop](https://nanobotco.github.io/mae-hong-son-loop/) — motorcycling the 600 km loop out of Chiang Mai — curves counted, air measured
- [Muay Thai](https://motdang.net/muay-thai/) — the eight limbs, the thirty named techniques, the ceremony, and every gym on the map
- [Roads of Chiang Mai](https://motdang.net/roads/) — the square of 1296, four rings, and what each one did to the city — counted from the map
- [wichaa](https://wichaa.net/) — Lanna manuscripts, the amulet market, and the traditions around them
- [Hand Poke](https://nanobotco.github.io/hand-poke/) — 28 traditions of marking skin by hand — the leg-tattoo zone of Burma, the Shan States and Lanna, counted
- [Black Holes, Drawn](https://nanobotco.github.io/black-holes/) — black holes modelled and drawn from the equations — generators, the past, present and future, the legends
- [Quantum Computing, plainly](https://nanobotco.github.io/quantum-computing/) — the history and theory of quantum computing in plain words, with demos; refreshed weekly
- [Goin' Fast](https://nanobotco.github.io/goin-fast/) — a dirt-simple explainer about speed — twenty measured speeds from the ground under the house to light, and what each one costs
- [The Three-Body Problem](https://nanobotco.github.io/three-body/) — the mathematics of the three-body problem in plain words, with the orbits found rather than copied
- [Amulet Atlas](https://nanobotco.github.io/amulet-atlas/) — amulets, charms and talismans worldwide
- [Carolina Barbecue](https://nanobotco.github.io/carolina-barbecue/) — barbecue in North and South Carolina
- [Wing Country](https://nanobotco.github.io/buffalo-wings/) — the American chicken wing
- [Pink Box](https://nanobotco.github.io/pink-box/) — the American mom-and-pop donut shop
- [Basque Tables](https://nanobotco.github.io/basque-tables/) — Basque dining rooms of California, Nevada and Idaho
- [Pinot Country](https://nanobotco.github.io/pinot-noir/) — pinot noir: the vine, the regions, the cellars
- [Care Abroad](https://nanobotco.github.io/care-abroad/) — treatment across borders, with published prices and their dates
- [Thai Roots](https://nanobotco.github.io/thairoots/) — a root dictionary of Thai, with a word decomposer
- [The index](https://nanobotco.github.io/index/) — every corpus, site and repository, counted
- [Uptake](https://nanobotco.github.io/uptake/) — a field manual on publishing for machines that copy
- [NaNoBotCo](https://nanobotco.github.io/) — the portal
- [ฮักฝรั่ง](https://hakfarang.net/) — เรื่องเงิน วีซ่า และชีวิตกับแฟนฝรั่ง
- [Offrampt](https://offrampt.net/) — turning crypto into spendable local money, Thailand first

All of it, counted: https://nanobotco.github.io/index/ · roster as JSON: https://nanobotco.github.io/index/fleet.json
