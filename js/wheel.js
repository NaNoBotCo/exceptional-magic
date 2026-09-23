// wheel.js — the Fano plane, drawn live; click two units to light the line they sit on.
(function () {
  const cv = document.getElementById("wheel");
  if (!cv) return;
  const base = document.body.dataset.base || "/";
  EM.load(base);
  const out = document.getElementById("wheelout");
  let A = null, lines = [], pos = {}, picked = [];
  const S = 460, R = 168;

  function layout() {
    const cx = S / 2, cy = S / 2 + 10;
    const corner = [-90, 30, 150].map(a => [cx + R * Math.cos(a * Math.PI / 180),
                                            cy + R * Math.sin(a * Math.PI / 180)]);
    const mid = [[0, 1], [1, 2], [2, 0]].map(([i, j]) =>
      [(corner[i][0] + corner[j][0]) / 2, (corner[i][1] + corner[j][1]) / 2]);
    const slots = [corner[0], corner[1], corner[2], mid[0], mid[1], mid[2], [cx, cy]];
    const geo = [[0, 3, 1], [1, 4, 2], [2, 5, 0], [0, 6, 4], [1, 6, 5], [2, 6, 3], [3, 4, 5]];
    const geoset = geo.map(t => t.slice().sort().join(","));
    const units = [1, 2, 3, 4, 5, 6, 7];
    // walk the labellings of the seven points until the table's lines are the drawn lines
    function search(rest, cur) {
      if (!rest.length) {
        const m = {}; cur.forEach((u, s) => m[u] = s);
        return lines.every(l => geoset.includes(l.map(u => m[u]).sort().join(","))) ? m : null;
      }
      for (let i = 0; i < rest.length; i++) {
        const m = search(rest.slice(0, i).concat(rest.slice(i + 1)), cur.concat([rest[i]]));
        if (m) return m;
      }
      return null;
    }
    const m = search(units, []);
    if (m) {
      const out2 = {};
      for (const u of units) out2[u] = slots[m[u]];
      return { pos: out2, slots, cx, cy, mid };
    }
    return null;
  }

  function draw() {
    const g = cv.getContext("2d");
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = S * dpr; cv.height = S * dpr;
    cv.style.width = "100%"; cv.style.maxWidth = S + "px";
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, S, S);
    const lit = picked.length === 2
      ? lines.find(l => l.includes(picked[0]) && l.includes(picked[1])) : null;

    g.lineWidth = 2.5;
    for (const l of lines) {
      const on = lit && l === lit;
      g.strokeStyle = on ? "#ffc247" : "#2c2c3a";
      const idx = l.map(u => L.slots.indexOf(L.pos[u]));
      if (idx.slice().sort().join(",") === "3,4,5") {
        const r = Math.hypot(L.slots[3][0] - L.cx, L.slots[3][1] - L.cy);
        g.beginPath(); g.arc(L.cx, L.cy, r, 0, 7); g.stroke();
      } else {
        // the two ends are the two points farthest apart
        const pts = idx.map(i => L.slots[i]);
        let best = null, bd = -1;
        for (const a of pts) for (const c of pts) {
          const dd = Math.hypot(a[0] - c[0], a[1] - c[1]);
          if (dd > bd) { bd = dd; best = [a, c]; }
        }
        g.beginPath();
        g.moveTo(best[0][0], best[0][1]);
        g.lineTo(best[1][0], best[1][1]);
        g.stroke();
      }
    }
    for (let u = 1; u <= 7; u++) {
      const [x, y] = L.pos[u];
      const on = picked.includes(u);
      g.beginPath(); g.arc(x, y, 17, 0, 7);
      g.fillStyle = "#0a0a10"; g.fill();
      g.strokeStyle = on ? "#ffc247" : (lit && lit.includes(u) ? "#ffc247" : "#5fd3c6");
      g.lineWidth = on ? 3.5 : 2.5; g.stroke();
      g.fillStyle = "#f2ede3"; g.font = "600 14px system-ui"; g.textAlign = "center";
      g.fillText("e" + u, x, y + 5);
    }
  }

  let L = null;
  function hit(ev) {
    const r = cv.getBoundingClientRect();
    const x = (ev.clientX - r.left) * S / r.width, y = (ev.clientY - r.top) * S / r.height;
    for (let u = 1; u <= 7; u++) {
      const [px, py] = L.pos[u];
      if (Math.hypot(px - x, py - y) < 22) return u;
    }
    return null;
  }

  cv.addEventListener("click", ev => {
    const u = hit(ev);
    if (!u) return;
    picked = picked.length === 2 ? [u] : picked.concat([u]);
    if (picked.length === 2 && picked[0] === picked[1]) picked = [picked[0]];
    report(); draw();
  });

  function report() {
    if (!out) return;
    if (picked.length < 2) { out.innerHTML = '<span class="k">pick two</span>'; return; }
    const [a, b] = picked;
    const p = A.mul(A.unit(a), A.unit(b));
    const k = p.findIndex(v => v !== 0);
    const line = lines.find(l => l.includes(a) && l.includes(b));
    out.innerHTML = `<div><span class="k">e${a} · e${b}</span> = <span class="v">${EM.show(p)}</span></div>` +
      `<div class="k">line (${line.join(" → ")}) — going with the arrows is a plus, ` +
      `against them a minus</div>` +
      `<div><span class="k">e${b} · e${a}</span> = <span class="v">${EM.show(A.mul(A.unit(b), A.unit(a)))}</span></div>`;
  }

  EM.ready(d => {
    A = EM.algebra("O");
    lines = d.fano;
    L = layout();
    if (!L) return;
    report(); draw();
    window.addEventListener("resize", draw);
  });
})();
