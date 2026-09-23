// triality.js — T(v, psi, chi) worked out three ways on numbers you can change.
(function () {
  const root = document.getElementById("tri");
  if (!root) return;
  const base = document.body.dataset.base || "/";
  EM.load(base);
  let tag = "O";
  let v = [], p = [], c = [];

  function rand(n) { return Array.from({ length: n }, () => Math.floor(Math.random() * 7) - 3); }

  function T(A, v, p, c) { return A.form(A.conj(c), A.mul(v, p)); }

  function draw() {
    EM.ready(() => {
      const A = EM.algebra(tag);
      if (v.length !== A.n) { v = rand(A.n); p = rand(A.n); c = rand(A.n); }
      const t1 = T(A, v, p, c), t2 = T(A, p, c, v), t3 = T(A, c, v, p);
      const same = t1 === t2 && t2 === t3;
      // a reflection through a unit: T should come back with the other sign
      const u = A.unit(1 + Math.floor(Math.random() * (A.n - 1)));
      const v2 = A.mul(A.mul(u, A.conj(v)), u).map(x => -x);
      const p2 = A.mul(A.conj(u), A.conj(c));
      const c2 = A.mul(A.conj(p), A.conj(u));
      const tr = T(A, v2, p2, c2);
      root.querySelector("#triout").innerHTML = [
        `<div><span class="k">v&nbsp;&nbsp;&nbsp;=</span> <span class="v">${EM.show(v)}</span></div>`,
        `<div><span class="k">ψ&nbsp;&nbsp;&nbsp;=</span> <span class="v">${EM.show(p)}</span></div>`,
        `<div><span class="k">χ&nbsp;&nbsp;&nbsp;=</span> <span class="v">${EM.show(c)}</span></div>`,
        `<hr style="border:0;border-top:1px solid #2c2c3a;margin:.5rem 0">`,
        `<div><span class="k">T(v, ψ, χ)</span> = <span class="good">${t1}</span></div>`,
        `<div><span class="k">T(ψ, χ, v)</span> = <span class="good">${t2}</span></div>`,
        `<div><span class="k">T(χ, v, ψ)</span> = <span class="good">${t3}</span></div>`,
        `<div>${same ? '<span class="good">— all three the same. Shuffle the three and nothing moves.</span>'
          : '<span class="bad">— these should agree; something is wrong</span>'}</div>`,
        `<hr style="border:0;border-top:1px solid #2c2c3a;margin:.5rem 0">`,
        `<div><span class="k">after a reflection through e${u.findIndex(x => x)}</span> = ` +
        `<span class="v">${tr}</span> ${tr === -t1 ? '<span class="good">— the same size, the other sign</span>'
          : '<span class="bad">— expected ' + (-t1) + '</span>'}</div>`
      ].join("");
    });
  }

  root.querySelector("#triroll").onclick = () => {
    EM.ready(() => { const n = EM.algebra(tag).n; v = rand(n); p = rand(n); c = rand(n); draw(); });
  };
  root.querySelectorAll("[data-alg]").forEach(b => {
    b.onclick = () => {
      tag = b.dataset.alg;
      root.querySelectorAll("[data-alg]").forEach(o =>
        o.setAttribute("aria-pressed", o === b ? "true" : "false"));
      v = [];
      draw();
    };
  });
  draw();
})();
