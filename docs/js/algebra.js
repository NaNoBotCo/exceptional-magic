// algebra.js — the same multiplication tables the figures were drawn from, loaded
// from data/algebra.json so the page and the pictures cannot drift apart.
window.EM = (function () {
  let D = null;
  const waiting = [];

  function ready(fn) { D ? fn(D) : waiting.push(fn); }

  function load(base) {
    fetch(base + "data/algebra.json").then(r => r.json()).then(d => {
      D = d;
      waiting.splice(0).forEach(fn => fn(D));
    }).catch(() => {});
  }

  function algebra(tag) {
    const t = D.tables[tag];
    const n = t.n;
    return {
      n, tag, sig: t.sig,
      mul(x, y) {
        const out = new Array(n).fill(0);
        for (let a = 0; a < n; a++) {
          if (!x[a]) continue;
          for (let b = 0; b < n; b++) {
            if (!y[b]) continue;
            const [s, c] = t.table[a][b];
            out[c] += s * x[a] * y[b];
          }
        }
        return out;
      },
      conj(x) { return x.map((v, i) => (i ? -v : v)); },
      form(x, y) { let s = 0; for (let i = 0; i < n; i++) s += t.sig[i] * x[i] * y[i]; return s; },
      unit(i) { const v = new Array(n).fill(0); v[i] = 1; return v; }
    };
  }

  // a, b -> a*b - b*a  and  (ab)c - a(bc)
  function commutator(A, x, y) { return sub(A.mul(x, y), A.mul(y, x)); }
  function associator(A, x, y, z) { return sub(A.mul(A.mul(x, y), z), A.mul(x, A.mul(y, z))); }
  function sub(a, b) { return a.map((v, i) => v - b[i]); }
  function isZero(v) { return v.every(x => Math.abs(x) < 1e-9); }

  function show(v, opts) {
    const o = opts || {};
    const parts = [];
    v.forEach((c, i) => {
      if (Math.abs(c) < 1e-9) return;
      const mag = Math.abs(c) === 1 ? "" : String(Math.abs(c));
      const nm = i === 0 ? (mag || "1") : mag + "e" + i;
      parts.push((c < 0 ? "−" : (parts.length ? "+" : "")) + nm);
    });
    if (!parts.length) return "0";
    return parts.join(" ").replace(/([−+])\s/g, "$1 ");
  }

  return { load, ready, algebra, commutator, associator, isZero, show, sub,
           data: () => D };
})();
