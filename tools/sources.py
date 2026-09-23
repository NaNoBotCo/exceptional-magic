# -*- coding: utf-8 -*-
"""sources.py — the paper this site reads, and everything the paper cites.

The reference list is Lisi's own, arXiv:2609.12112v1, transcribed with its links so
that a reader here can walk straight back to the work. `why` is this site's note on
what each one is for; the rest is the citation as the paper gives it.
"""

PAPER = {
    "id": "lisi2026",
    "authors": "A. Garrett Lisi",
    "year": 2026,
    "title": "Division Algebras, Triality, and Exceptional Magic",
    "where": "arXiv:2609.12112v1 [math-ph], 10 September 2026",
    "url": "https://arxiv.org/abs/2609.12112",
    "html": "https://arxiv.org/html/2609.12112v1",
    "pdf": "https://arxiv.org/pdf/2609.12112v1",
    "licence": "CC BY-NC-ND 4.0",
    "licence_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
}

SOURCES = [
    ("baez2002", "J. Baez", 2002, "The Octonions", "Bull. Amer. Math. Soc. 39",
     "math/0105155", "The standing introduction to the octonions and the magic square. Lisi's "
     "paper says it follows this one, in more painful detail."),
    ("barton2003", "C. H. Barton and A. Sudbery", 2003, "Magic squares and matrix models of Lie algebras",
     "Adv. Math. 180, 596–647", "math/0203010", "Where the magic square gets its matrix models."),
    ("boyle2020", "L. Boyle and S. Farnsworth", 2020,
     "The standard model, the Pati-Salam model, and 'Jordan geometry'", "New J. Phys. 22",
     "1910.11888", "Another route from the exceptional algebras into particle physics."),
    ("chester2023a", "D. Chester, A. Marrani, D. Corradetti, R. Aschheim and K. Irwin", 2023,
     "Dixon-Rosenfeld lines and the standard model", "Eur. Phys. J. C 83 (849)", "2303.11334",
     "Division algebra lines and the standard model."),
    ("chester2023b", "D. Chester, M. Rios and A. Marrani", 2023,
     "Beyond the standard model with six-dimensional spinors", "Particles 6 (1)", "2002.02391",
     "Six-dimensional spinors past the standard model."),
    ("distler2010", "J. Distler and R. Garibaldi", 2010,
     "There is no 'theory of everything' inside E8", "Comm. Math. Phys. 298 (2), 419–436",
     "0905.2658", "The standing objection to fitting three generations in E8. The site's "
     "physics page states it; Lisi §10 and §12 answer it."),
    ("dixon1994", "G. M. Dixon", 1994,
     "Division algebras: octonions, quaternions, complex numbers, and the algebraic design of physics",
     "Kluwer", "", "The book that made C ⊗ H ⊗ O a programme."),
    ("douglas2014", "A. Douglas and J. Repka", 2014,
     "The gravigut algebra is not a subalgebra of E8, but E8 does contain an extended gravigut algebra",
     "SIGMA 10 (072)", "1305.6946", "What does and does not embed."),
    ("dray2010", "T. Dray and C. A. Manogue", 2010, "Octonions, E6, and particle physics",
     "J. Phys. Conf. Ser. 254 (012005)", "0911.2253", "E6 as the minimal exceptional home."),
    ("dray2015", "T. Dray and C. A. Manogue", 2015, "The geometry of the octonions",
     "World Scientific", "", "Where su(3, D) as a way of writing these algebras comes from."),
    ("dubois2018", "M. Dubois-Violette and I. Todorov", 2018,
     "Exceptional quantum geometry and particle physics II", "Nucl. Phys. B 938", "1808.08110",
     "The Jordan-algebra line of attack."),
    ("evans2009", "J. Evans", 2009, "Trialities and exceptional Lie algebras: deconstructing the magic square",
     "", "0910.1828", "Triality as the thing the magic square is made of — the paper's §4 and §5 "
     "lean on it, and so does this site's square."),
    ("freudenthal1964", "H. Freudenthal", 1964, "Lie groups in the foundations of geometry",
     "Adv. Math. 1, 145–190", "", "One of the two people the magic square is named for."),
    ("furey2022", "N. Furey and M. J. Hughes", 2022, "Division algebraic symmetry breaking",
     "Phys. Lett. B 831", "2210.10126", "Symmetry breaking done with division algebras."),
    ("furey2025", "N. Furey and M. J. Hughes", 2025, "Three generations and a trio of trialities",
     "Phys. Lett. B 865", "2409.17948", "Three generations from three trialities — the idea this "
     "site's triality page is circling."),
    ("gillard2019", "A. B. Gillard and N. G. Gresnigt", 2019,
     "Three fermion generations with two unbroken gauge symmetries from the complex sedenions",
     "Eur. Phys. J. C 79 (446)", "1904.03186", "Someone did go past eight, on purpose."),
    ("kollross2020", "A. Kollross", 2020,
     "Octonions, triality, the exceptional Lie algebra F4, and polar actions on the Cayley hyperbolic plane",
     "Int. J. Math. 31 (07)", "1802.08075", "F4 and triality."),
    ("krasnov2022", "K. Krasnov", 2022, "Spin(11,3), particles, and octonions",
     "J. Math. Phys. 63 (031701)", "2104.01786", "A different signature, same octonions."),
    ("lisi2007", "A. G. Lisi", 2007, "An exceptionally simple theory of everything", "", "0711.0770",
     "The 2007 E8 paper. The particle assignment on this site's physics page is the one it made."),
    ("lisi2010", "A. G. Lisi", 2010, "An explicit embedding of gravity and the standard model in E8",
     "Representation Theory and Mathematical Physics, Contemp. Math. 557", "1006.4908",
     "The embedding written out."),
    ("lisi2015", "A. G. Lisi", 2015, "Lie group cosmology", "", "1506.08073",
     "The setting the 2026 paper puts its superconnection in."),
    ("lisi2024", "A. G. Lisi", 2024, "C, P, T, and triality", "", "2407.02497",
     "The quaternion group inside the CPT group, and its extension by triality."),
    ("lounesto2001", "P. Lounesto", 2001, "Clifford algebras and spinors", "Cambridge, 2nd ed.", "",
     "Reflections in a Clifford algebra, the standard account."),
    ("manogue2022", "C. A. Manogue, T. Dray and R. A. Wilson", 2022,
     "Octions: an E8 description of the standard model", "J. Math. Phys. 63 (081703)", "2204.05310",
     "Another E8 description."),
    ("perelman2021", "C. C. Perelman", 2021,
     "On Jordan-Clifford algebras, three fermion generations with Higgs fields and a "
     "SU(3)×SU(2)L×SU(2)R×U(1) model", "Adv. Appl. Clifford Algebr. 31 (53)", "",
     "Three generations from a Jordan-Clifford algebra."),
    ("porteous1995", "I. R. Porteous", 1995, "Clifford algebras and the classical groups",
     "Cambridge", "", "The other standard reference for reflections."),
    ("ramond2003", "P. Ramond", 2003, "Exceptional groups and physics", "Groupe 24 plenary talk",
     "hep-th/0301050", "The overview talk."),
    ("tits1966", "J. Tits", 1966,
     "Algèbres alternatives, algèbres de Jordan et algèbres de Lie exceptionnelles",
     "Nederl. Akad. Wetensch. Proc. Ser. A 69, 223–237", "",
     "The other person the magic square is named for."),
    ("vaibhav2023", "V. Vaibhav and T. P. Singh", 2023,
     "Left-right symmetric fermions and sterile neutrinos from complex split biquaternions and bioctonions",
     "Adv. Appl. Clifford Algebr. 33 (32)", "2108.01858", "Split algebras, put to work."),
    ("vinberg1976", "E. B. Vinberg", 1976, "The Weyl group of a graded Lie algebra",
     "Math. USSR-Izv. 10 (3)", "", "Where the Θ-groups on this site's E8 page come from. "
     "Russian original: Izv. Akad. Nauk SSSR Ser. Mat. 40 (3) (1976)."),
    ("wilson2023", "R. A. Wilson, T. Dray and C. A. Manogue", 2023,
     "An octonionic construction of E8 and the Lie algebra magic square", "Innov. Incidence Geom. 20",
     "2204.04996", "Building E8 out of octonions."),
    ("wilson2024", "R. A. Wilson", 2024,
     "On possible embeddings of the standard model of particle physics and gravity in E8", "",
     "2404.18938", "What can be embedded, carefully."),
    ("woit2021", "P. Woit", 2021, "Euclidean twistor unification", "", "2104.05099",
     "Twistors meet the same incidence relation triality produces."),
    ("wolf1968", "J. A. Wolf and A. Gray", 1968,
     "Homogeneous spaces defined by Lie group automorphisms. I", "J. Diff. Geom. 2, 77–114", "",
     "3-symmetric spaces — what a triality automorphism leaves behind."),
]

BY_ID = {s[0]: s for s in SOURCES}


def url(s):
    arx = s[5]
    if not arx:
        return ""
    return f"https://arxiv.org/abs/{arx}"


def cite_html(ids, E=None):
    import html as _h
    E = E or _h.escape
    out = []
    for i in ids:
        s = BY_ID[i]
        label = f"{s[1].split(' and ')[0].split(',')[0]} {s[2]}"
        u = url(s)
        out.append(f'<a class="cite" href="{E(u)}" rel="noopener">{E(label)}</a>' if u
                   else f'<span class="cite">{E(label)}</span>')
    return " ".join(out)
