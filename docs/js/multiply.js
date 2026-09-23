// multiply.js — multiply two elements and watch the laws come apart.
(function () {
  const root = document.getElementById("mul");
  if (!root) return;
  const base = document.body.dataset.base || "/";
  EM.load(base);
  const pick = { a: 1, b: 2, c: 4, tag: "O" };

  function el(id) { return root.querySelector(id); }

  function render() {
    EM.ready(() => {
      const A = EM.algebra(pick.tag);
      const n = A.n;
      if (pick.a >= n) pick.a = n - 1;
      if (pick.b >= n) pick.b = n - 1;
      if (pick.c >= n) pick.c = n - 1;
      for (const key of ["a", "b", "c"]) {
        const box = el("#u" + key);
        box.innerHTML = "";
        for (let i = 0; i < n; i++) {
          const btn = document.createElement("button");
          btn.textContent = "e" + i;
          btn.className = key === "b" ? "b" : "";
          btn.setAttribute("aria-pressed", pick[key] === i ? "true" : "false");
          btn.onclick = () => { pick[key] = i; render(); };
          box.appendChild(btn);
        }
      }
      const x = A.unit(pick.a), y = A.unit(pick.b), z = A.unit(pick.c);
      const xy = A.mul(x, y), yx = A.mul(y, x);
      const comm = EM.commutator(A, x, y);
      const asso = EM.associator(A, x, y, z);
      const lines = [];
      lines.push(`<div><span class="k">e${pick.a} · e${pick.b}</span> = <span class="v">${EM.show(xy)}</span></div>`);
      lines.push(`<div><span class="k">e${pick.b} · e${pick.a}</span> = <span class="v">${EM.show(yx)}</span>` +
        (EM.isZero(comm) ? ` <span class="good">— same both ways</span>`
          : ` <span class="bad">— the other way round</span>`) + `</div>`);
      lines.push(`<div><span class="k">(e${pick.a}e${pick.b})e${pick.c}</span> = <span class="v">` +
        `${EM.show(A.mul(xy, z))}</span></div>`);
      lines.push(`<div><span class="k">e${pick.a}(e${pick.b}e${pick.c})</span> = <span class="v">` +
        `${EM.show(A.mul(x, A.mul(y, z)))}</span>` +
        (EM.isZero(asso) ? ` <span class="good">— agrees</span>`
          : ` <span class="bad">— disagrees, and that is the octonions for you</span>`) + `</div>`);
      const nx = A.form(x, x), ny = A.form(y, y), nxy = A.form(xy, xy);
      lines.push(`<div><span class="k">|e${pick.a}e${pick.b}|² = |e${pick.a}|²|e${pick.b}|²</span> → ` +
        `<span class="v">${nxy} = ${nx} × ${ny}</span>` +
        (nxy === nx * ny ? ` <span class="good">✓</span>` : ` <span class="bad">✗</span>`) + `</div>`);
      el("#mulout").innerHTML = lines.join("");
    });
  }

  root.querySelectorAll("[data-alg]").forEach(b => {
    b.onclick = () => {
      pick.tag = b.dataset.alg;
      root.querySelectorAll("[data-alg]").forEach(o =>
        o.setAttribute("aria-pressed", o === b ? "true" : "false"));
      render();
    };
  });
  const roll = el("#roll");
  if (roll) roll.onclick = () => {
    EM.ready(() => {
      const n = EM.algebra(pick.tag).n;
      pick.a = 1 + Math.floor(Math.random() * (n - 1));
      do { pick.b = 1 + Math.floor(Math.random() * (n - 1)); } while (pick.b === pick.a && n > 2);
      do { pick.c = 1 + Math.floor(Math.random() * (n - 1)); } while ((pick.c === pick.a || pick.c === pick.b) && n > 3);
      render();
    });
  };
  render();
})();
