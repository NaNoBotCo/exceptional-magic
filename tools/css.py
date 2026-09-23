# -*- coding: utf-8 -*-
"""css.py — one stylesheet, inlined into every page. No web font, no request out.

The three accents are the three triality eigenspaces: amber stands still, teal turns
one way, rose turns the other. They mean the same thing on every page and in every
figure.
"""

CSS = """
:root{
 --bg:#0a0a10;--bg2:#0f0f18;--panel:#14141f;--ink:#f2ede3;--mute:#9d9689;--line:#2c2c3a;
 --chip:#1b1b28;--c0:#ffc247;--c1:#5fd3c6;--c2:#ff7ab6;--violet:#b79cff;--focus:#ffc247;
 --display:"Avenir Next Condensed","Arial Narrow",Impact,system-ui,sans-serif;
 --body:"Avenir Next",Avenir,"Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;
 --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
 color-scheme:dark;
}
*{box-sizing:border-box}
html{font-size:19px;scroll-behavior:smooth;background:var(--bg)}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);line-height:1.62;
 -webkit-text-size-adjust:100%}
a{color:var(--c0);text-decoration-thickness:.08em;text-underline-offset:.18em}
a:hover{color:#ffd98a}
a:focus-visible,button:focus-visible,select:focus-visible,summary:focus-visible,input:focus-visible{
 outline:3px solid var(--focus);outline-offset:2px;border-radius:5px}
img,canvas,svg{max-width:100%}img{height:auto}
.sr{position:absolute;left:-999px;top:0;background:var(--c0);color:#000;padding:.4rem .8rem;z-index:99}
.sr:focus{left:.5rem;top:.5rem}

header.top{border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30;
 background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px)}
header.top .in{max-width:72rem;margin:0 auto;padding:.5rem 1rem;display:flex;gap:.4rem 1.1rem;
 align-items:center;flex-wrap:wrap}
.brand{font-family:var(--display);font-weight:800;font-size:1.2rem;letter-spacing:.03em;
 text-transform:uppercase;text-decoration:none;color:var(--ink);white-space:nowrap;display:flex;
 align-items:center;gap:.5rem}
.brand i{width:.85rem;height:.85rem;border-radius:50%;background:var(--c0);display:inline-block;
 box-shadow:0 0 0 3px rgba(255,194,71,.18),6px -6px 0 -2px var(--c1),-6px 6px 0 -2px var(--c2)}
header.top nav{display:flex;gap:.1rem .8rem;flex-wrap:wrap;font-size:.72rem;text-transform:uppercase;
 letter-spacing:.08em;font-weight:700}
header.top nav a{text-decoration:none;color:var(--mute);padding:.15rem 0}
header.top nav a:hover,header.top nav a[aria-current]{color:var(--ink);box-shadow:inset 0 -3px 0 var(--c0)}
main{max-width:72rem;margin:0 auto;padding:1rem 1rem 5rem}
footer.bot{border-top:1px solid var(--line);margin-top:3rem;background:var(--bg2)}
footer.bot .in{max-width:72rem;margin:0 auto;padding:1.4rem 1rem 3rem;font-size:.8rem;color:var(--mute)}
footer.bot a{color:var(--mute)}footer.bot p{max-width:none}
.fleet{margin:.6rem 0 0;line-height:1.9}.fleet a{margin-right:.55rem;white-space:nowrap}
.support{margin:.45rem 0 0}.support a{margin-right:.5rem}

h1{font-family:var(--display);font-size:clamp(2.4rem,7.5vw,5rem);line-height:.94;margin:.3rem 0 .4rem;
 font-weight:800;letter-spacing:-.005em;text-transform:uppercase}
h1 .kind{display:block;font-size:clamp(.6rem,1.5vw,.72rem);color:var(--c0);letter-spacing:.34em;
 margin-bottom:.55rem;font-weight:800}
h2{font-family:var(--display);font-size:clamp(1.5rem,3.4vw,2rem);margin:2.6rem 0 .6rem;font-weight:800;
 text-transform:uppercase;border-bottom:2px solid var(--line);padding-bottom:.25rem}
h2 small{font-family:var(--body);font-size:.55em;color:var(--mute);text-transform:none;
 letter-spacing:0;font-weight:400;margin-left:.6rem}
h3{font-family:var(--display);font-size:1.2rem;margin:1.7rem 0 .3rem;font-weight:800;text-transform:uppercase}
.lede{font-size:clamp(1.12rem,2.4vw,1.35rem);max-width:44rem;margin:.5rem 0 1.1rem}
.mute{color:var(--mute)}.small{font-size:.82rem}
p{margin:.65rem 0;max-width:44rem}
.prose p,.prose ul,.prose ol{max-width:44rem}
.prose li{margin:.35rem 0}
.prose strong{color:var(--c0);font-weight:700}
blockquote{margin:1rem 0;padding:.6rem 0 .6rem 1rem;border-left:3px solid var(--c1);color:var(--ink);
 max-width:44rem;font-style:normal}
blockquote cite{display:block;margin-top:.4rem;color:var(--mute);font-size:.82rem;font-style:normal}

.grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));margin:1rem 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:.9rem 1rem;
 text-decoration:none;color:var(--ink);display:block}
a.card:hover{border-color:var(--c0)}
.card h3{margin:.1rem 0 .3rem}
.card p{margin:.2rem 0;font-size:.88rem;color:var(--mute)}
.fig{margin:1.6rem 0;background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:.7rem}
.fig img{display:block;margin:0 auto;border-radius:6px}
.fig figcaption{color:var(--mute);font-size:.82rem;margin:.6rem .2rem 0;max-width:46rem}
.fig.plain{background:none;border:none;padding:0}
.hero{position:relative;border-radius:12px;overflow:hidden;border:1px solid var(--line);margin:.6rem 0 1.4rem}
.hero img{display:block;width:100%}

table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.88rem}
th,td{text-align:left;padding:.42rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mute);font-weight:700;font-size:.74rem;text-transform:uppercase;letter-spacing:.06em}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;font-family:var(--mono)}
.wrap{overflow-x:auto}
code,kbd{font-family:var(--mono);font-size:.86em;background:var(--chip);padding:.1rem .3rem;border-radius:4px}
pre{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:.8rem 1rem;
 overflow-x:auto;font-size:.82rem}
pre code{background:none;padding:0}
.eq{font-family:var(--mono);background:var(--panel);border-left:3px solid var(--c0);padding:.7rem 1rem;
 margin:1rem 0;overflow-x:auto;font-size:.92rem;max-width:44rem}
.eq b{color:var(--c0);font-weight:600}
.cite{font-size:.78em;color:var(--c1);text-decoration:none;border-bottom:1px dotted var(--c1);
 white-space:nowrap;margin-left:.2em}
.cite:hover{color:var(--c1)}
.tag{display:inline-block;background:var(--chip);border:1px solid var(--line);border-radius:999px;
 padding:.1rem .6rem;font-size:.72rem;color:var(--mute);margin:0 .25rem .3rem 0}
.tag.c0{border-color:var(--c0);color:var(--c0)}
.tag.c1{border-color:var(--c1);color:var(--c1)}
.tag.c2{border-color:var(--c2);color:var(--c2)}

.tool{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:1rem;margin:1.4rem 0}
.tool h3{margin-top:0}
.tool .row{display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin:.5rem 0}
.tool label{font-size:.8rem;color:var(--mute);text-transform:uppercase;letter-spacing:.06em;font-weight:700}
button,select,input[type=text]{font:inherit;font-size:.9rem;background:var(--chip);color:var(--ink);
 border:1px solid var(--line);border-radius:7px;padding:.35rem .7rem;cursor:pointer}
button:hover,select:hover{border-color:var(--c0)}
button.go{background:var(--c0);color:#0a0a10;border-color:var(--c0);font-weight:700}
.out{font-family:var(--mono);font-size:.9rem;background:#0b0b12;border:1px solid var(--line);
 border-radius:8px;padding:.7rem .9rem;margin:.6rem 0 0;overflow-x:auto;line-height:1.8}
.out .k{color:var(--mute)}
.out .v{color:var(--c1)}
.out .bad{color:var(--c2)}
.out .good{color:var(--c0)}
.units{display:flex;gap:.3rem;flex-wrap:wrap}
.units button{min-width:2.9rem;text-align:center;font-family:var(--mono)}
.units button[aria-pressed=true]{background:var(--c0);color:#0a0a10;border-color:var(--c0);font-weight:700}
.units button.b[aria-pressed=true]{background:var(--c1);border-color:var(--c1)}
canvas{display:block;margin:0 auto;max-width:100%;height:auto;touch-action:pan-y}

.square{border-collapse:separate;border-spacing:3px;font-size:.78rem;width:auto;min-width:100%}
.square td,.square th{border:none;padding:.4rem .3rem;text-align:center;border-radius:6px}
.square td{background:var(--panel);border:1px solid var(--line)}
.square td b{display:block;font-size:1.02rem;color:var(--ink)}
.square td span{color:var(--mute);font-family:var(--mono);font-size:.72rem}
.square td.big{border-color:var(--c0)}
.square td.big b{color:var(--c0)}
.square td.e7{border-color:var(--c1)}.square td.e7 b{color:var(--c1)}
.square td.e6{border-color:var(--c2)}.square td.e6 b{color:var(--c2)}
.square td.f4{border-color:var(--violet)}.square td.f4 b{color:var(--violet)}
.square th{color:var(--mute)}

ul.ticks{list-style:none;padding-left:0}
ul.ticks li{padding-left:1.4rem;position:relative}
ul.ticks li:before{content:"✓";position:absolute;left:0;color:var(--c1);font-weight:700}
ul.checks{list-style:none;padding-left:0;font-family:var(--mono);font-size:.78rem;columns:2;
 column-gap:2rem;max-width:none}
ul.checks li{break-inside:avoid;color:var(--mute);margin:.15rem 0}
ul.checks li b{color:var(--c1);font-weight:400}
@media (max-width:48rem){ul.checks{columns:1}}
.kv{display:grid;grid-template-columns:auto 1fr;gap:.2rem 1rem;font-size:.86rem;max-width:44rem}
.kv dt{color:var(--mute)}.kv dd{margin:0}
.note{border:1px solid var(--line);border-left:3px solid var(--c2);background:var(--bg2);
 border-radius:0 8px 8px 0;padding:.7rem 1rem;margin:1.2rem 0;font-size:.9rem;max-width:46rem}
.note b{color:var(--c2)}
.credit{border:1px solid var(--c1);border-radius:10px;padding:1rem 1.2rem;margin:1.6rem 0;
 background:color-mix(in srgb,var(--c1) 6%,var(--panel));max-width:46rem}
.credit a{color:var(--c1)}
.credit h3{margin-top:0;color:var(--c1)}
.gallery{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr))}
.gallery a{display:block;background:var(--panel);border:1px solid var(--line);border-radius:10px;
 padding:.6rem;text-decoration:none;color:var(--mute);font-size:.8rem}
.gallery a:hover{border-color:var(--c0)}
.gallery img{border-radius:6px;display:block;width:100%;background:var(--bg)}
"""
