#!/usr/bin/env python3
"""What the built site says, checked against what the algebra computed."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import algebra as al   # noqa: E402
import roots as rt     # noqa: E402

fails = []


def check(name, ok):
    print(f"  {'ok ' if ok else 'BAD'} {name}")
    if not ok:
        fails.append(name)


# the two check suites, again, on the way out the door
fa, _ = al.check_all(verbose=False)
fr, _ = rt.check_all(verbose=False)
check("algebra checks", fa == 0)
check("root-system checks", fr == 0)

facts = json.loads((ROOT / "build" / "facts.json").read_text())
check("facts: zero failing checks recorded", facts["checks"]["failures"] == 0)
check("facts: E8 has 240 roots", facts["systems"]["E8"]["roots"] == 240)
check("facts: E8 rings are eight of thirty",
      [n for _, n in facts["systems"]["E8"]["rings"]] == [30] * 8)
check("facts: triality split 84 + 78 + 78", facts["e8_z3"]["counts"] == [84, 78, 78])
check("facts: no bracket violations", facts["e8_z3"]["violations"] == 0)
check("facts: two-grading 120 + 128",
      facts["e8_two_grading"]["so16"] == 120 and facts["e8_two_grading"]["spinor"] == 128)
check("facts: seven Fano lines", len(facts["fano_lines"]) == 7)
check("facts: hero has 6720 edges", facts["hero_edges"] == 6720)
check("facts: magic square 7x7", len(facts["magic"]) == 7 and all(len(r) == 7 for r in facts["magic"]))
check("facts: e8 in the corner", facts["magic"][3][3]["dim"] == 248)

site = ROOT / "build" / "site"
pages = ["index.html", "numbers/index.html", "wheel/index.html", "triality/index.html",
         "square/index.html", "e8/index.html", "physics/index.html", "checks/index.html",
         "gallery/index.html", "credit/index.html", "404.html"]
for p in pages:
    check(f"page {p}", (site / p).exists())
for m in ("robots.txt", "sitemap.xml", "llms.txt", "humans.txt", "icon.svg", "fleet.json",
          "data/algebra.json", "data/roots.json", "data/facts.json",
          "img/hero.jpg", "img/card.jpg", "img/e8.svg", "img/fano.svg", "img/magic.svg"):
    check(f"file {m}", (site / m).exists())
for j in ("algebra.js", "multiply.js", "wheel.js", "triality.js", "shadow.js", "nav.js"):
    check(f"script {j}", (site / "js" / j).exists())

home = (site / "index.html").read_text(encoding="utf-8")
for must in ("arxiv.org/abs/2609.12112", "CC BY-NC-ND", "CC BY 4.0", "hongdam", "Lisi",
             "img/card.jpg", "248", "240"):
    check(f"front page names {must}", must in home)
credit = (site / "credit" / "index.html").read_text(encoding="utf-8")
refs = credit.split("<h2>The paper's references</h2>")[1].split("<h2>")[0]
check("credit page lists all 34 references", refs.count("<tr>") == 35)   # header + 34
check("credit page links the arXiv ones", refs.count("arxiv.org/abs/") == 25)
physics = (site / "physics" / "index.html").read_text(encoding="utf-8")
check("physics page carries the objection", "Distler" in physics)
for p in pages:
    if "/Users/" in (site / p).read_text(encoding="utf-8"):
        check(f"no host path in {p}", False)

if fails:
    print(f"FAILED: {fails}")
    sys.exit(1)
print("tests pass")
