// shadow.js — the root systems, projected onto the plane their Coxeter element turns.
// The points come from data/roots.json, computed by tools/roots.py.
(function () {
  const cv = document.getElementById("shadow");
  if (!cv) return;
  const base = document.body.dataset.base || "/";
  let DATA = null, name = cv.dataset.system || "E8", mode = "z3", spin = 0, edges = true;
  let raf = null, turning = false;
  const info = document.getElementById("shadowinfo");
  const C = ["#ffc247", "#5fd3c6", "#ff7ab6"];

  fetch(base + "data/roots.json").then(r => r.json()).then(d => { DATA = d; draw(); });

  function draw() {
    if (!DATA) return;
    const S = cv.clientWidth || 600;
    const g = cv.getContext("2d");
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = S * dpr; cv.height = S * dpr; cv.style.height = S + "px";
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.fillStyle = "#0a0a10"; g.fillRect(0, 0, S, S);
    const d = DATA[name];
    const R = S / 2 - 22, cx = S / 2, cy = S / 2;
    const co = Math.cos(spin), si = Math.sin(spin);
    const P = d.pts.map(([x, y]) => [cx + R * (x * co - y * si), cy - R * (x * si + y * co)]);

    const colour = i => {
      if (mode === "z3" && d.z3) return C[d.z3[i]];
      if (mode === "two" && d.whole) return d.whole[i] ? "#5fd3c6" : "#ff7ab6";
      return "#ffc247";
    };

    if (edges && d.edges.length <= 8000) {
      g.lineWidth = 1;
      for (const [i, j] of d.edges) {
        g.strokeStyle = colour(i) + "18";
        g.beginPath(); g.moveTo(P[i][0], P[i][1]); g.lineTo(P[j][0], P[j][1]); g.stroke();
      }
    }
    const r = d.n > 120 ? 3.4 : (d.n > 40 ? 4.6 : 6);
    for (let i = 0; i < P.length; i++) {
      g.beginPath(); g.arc(P[i][0], P[i][1], r, 0, 7);
      g.fillStyle = colour(i); g.fill();
    }
    if (info) {
      const parts = [`<b>${name}</b> · ${d.n} roots · rank ${d.rank} · ` +
        `${d.n + d.rank} dimensions · ${d.h}-fold`];
      if (mode === "z3" && d.z3) {
        const cnt = [0, 0, 0]; d.z3.forEach(k => cnt[k]++);
        parts.push(`<span style="color:${C[0]}">${cnt[0]} still</span> · ` +
          `<span style="color:${C[1]}">${cnt[1]} one way</span> · ` +
          `<span style="color:${C[2]}">${cnt[2]} the other</span>`);
      }
      if (mode === "two" && d.whole) {
        const w = d.whole.reduce((a, b) => a + b, 0);
        parts.push(`<span style="color:#5fd3c6">${w} + 8 = ${w + 8} in so(16)</span> · ` +
          `<span style="color:#ff7ab6">${d.whole.length - w} in the spinor</span>`);
      }
      info.innerHTML = parts.join("<br>");
    }
  }

  function tick() {
    if (!turning) return;
    spin += 0.004;
    draw();
    raf = requestAnimationFrame(tick);
  }

  document.querySelectorAll("[data-sys]").forEach(b => b.onclick = () => {
    name = b.dataset.sys;
    document.querySelectorAll("[data-sys]").forEach(o =>
      o.setAttribute("aria-pressed", o === b ? "true" : "false"));
    draw();
  });
  document.querySelectorAll("[data-mode]").forEach(b => b.onclick = () => {
    mode = b.dataset.mode;
    document.querySelectorAll("[data-mode]").forEach(o =>
      o.setAttribute("aria-pressed", o === b ? "true" : "false"));
    draw();
  });
  const sp = document.getElementById("spin");
  if (sp) sp.onclick = () => {
    turning = !turning;
    sp.textContent = turning ? "stop" : "turn it";
    sp.setAttribute("aria-pressed", turning ? "true" : "false");
    if (turning) tick(); else cancelAnimationFrame(raf);
  };
  const ed = document.getElementById("edges");
  if (ed) ed.onclick = () => {
    edges = !edges;
    ed.setAttribute("aria-pressed", edges ? "true" : "false");
    ed.textContent = edges ? "lines on" : "lines off";
    draw();
  };
  window.addEventListener("resize", draw);
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches && sp) sp.hidden = true;
})();
