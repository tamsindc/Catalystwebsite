#!/usr/bin/env python3
"""Build one static, search-friendly page per guide, plus a guide index, sitemap and robots.txt.

Reads data/workflows.js (made by build_recipes.py) and writes:
  guides/<id>.html   one page per guide
  guides/index.html  every guide, grouped by topic
  sitemap.xml, robots.txt

Run after build_recipes.py:  python3 scripts/build_pages.py
Set the live address with FISHPOND_URL (default https://thefishpond.online).
"""
import html, json, os, pathlib, re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = os.environ.get("FISHPOND_URL", "https://thefishpond.online").rstrip("/")
OUT = ROOT / "guides"

raw = (ROOT / "data" / "workflows.js").read_text()
data = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
items, built = data["items"], data["meta"]["built"]
e = lambda s: html.escape(str(s or ""), quote=True)
BRACKET = re.compile(r"\[([^\]\n]{1,140})\]")

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Atkinson+Hyperlegible:wght@400;700&display=swap">'
ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 200 200\'%3E%3Crect x=\'60\' y=\'60\' width=\'120\' height=\'110\' rx=\'18\' fill=\'%23fff\' stroke=\'%23f05a3c\' stroke-width=\'16\'/%3E%3Cpath d=\'M68 118 q12 -9 24 0 t24 0 t24 0 t24 0 V162 H68Z\' fill=\'%2313c4f2\'/%3E%3C/svg%3E">'

CSS = """:root{--ground:#fff;--tone:#eaf8fd;--tone2:#fff6d6;--ink:#0d1b33;--soft:#33445e;--cyan:#13c4f2;--deep:#06719a;--navy:#14307a;--yellow:#ffc21a;--orange-d:#c93d22;--display:"Baloo 2",system-ui,sans-serif;--text:"Atkinson Hyperlegible",system-ui,sans-serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ground);color:var(--ink);font:400 18px/1.6 var(--text)}
a{color:var(--deep)}
.wrap{max-width:820px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header.top{background:var(--cyan)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-block:14px}
.logo{font-family:var(--display);font-weight:800;font-size:26px;color:var(--navy);text-decoration:none}
.top nav{display:flex;gap:16px;flex-wrap:wrap}
.top nav a{color:var(--navy);font-weight:700;text-decoration:none}
main{padding-block:32px 56px;display:flex;flex-direction:column;gap:28px}
.crumb{font-size:15px;color:var(--soft)}
h1,h2,h3{font-family:var(--display);line-height:1.15;margin:0;color:var(--navy);text-wrap:balance}
h1{font-size:clamp(32px,6vw,46px);font-weight:800}
h2{font-size:28px}
.lede{font-size:21px;margin:10px 0 0;max-width:62ch}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.tags span{background:var(--tone);border-radius:10px;padding:4px 12px;font-weight:700;font-size:15px}
.cta{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;border-radius:999px;padding:14px 24px;font-weight:700;text-decoration:none;background:var(--orange-d);color:#fff}
.btn.alt{background:var(--tone);color:var(--ink)}
ol.steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:14px;counter-reset:s}
ol.steps li{background:var(--tone);border-radius:20px;padding:20px 22px;counter-increment:s}
ol.steps h3{font-size:22px}
ol.steps h3::before{content:counter(s) ". "}
ol.steps p{margin:6px 0 0}
.prompt{background:#fff;border-radius:14px;padding:14px 16px;margin-top:12px;white-space:pre-wrap;font-size:16px}
.prompt b{display:block;font-family:var(--display);color:var(--navy)}
.box{background:var(--tone2);border-radius:20px;padding:20px 22px}
.box p{margin:6px 0 0}
ul.tips{margin:6px 0 0;padding-left:20px}
.related{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.related a{background:var(--tone);border-radius:16px;padding:16px;text-decoration:none;color:var(--ink);font-weight:700}
.related small{display:block;font-weight:400;color:var(--soft)}
.topic{display:flex;flex-direction:column;gap:10px}
.topic ul{margin:0;padding-left:20px;columns:2 280px;column-gap:28px}
.topic li{break-inside:avoid;margin-bottom:6px}
footer{background:var(--navy);color:#fff}
footer .wrap{padding-block:28px;font-size:15px;display:flex;flex-direction:column;gap:6px}
footer a{color:#fff}
"""


def page(title, desc, path, body, extra_head=""):
    canon = f"{SITE}{path}"
    return f"""<!doctype html>
<html lang="en-GB"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article"><meta property="og:site_name" content="fishpond">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#14307a">
{ICON}{FONTS}
<link rel="stylesheet" href="/guides/guide.css">
{extra_head}
</head><body>
<header class="top"><div class="wrap"><a class="logo" href="/">fishpond</a>
<nav><a href="/guides/">All guides</a><a href="/#jobs">Your job</a><a href="/creators">Earn</a><a href="/rung">The Rung</a></nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><span>&copy; 2026 fishpond · Free, step-by-step AI guides for work and home.</span>
<span>Job guides are built with help from the O*NET database, US Department of Labor (CC BY 4.0). <a href="/privacy">Privacy</a></span></div></footer>
</body></html>
"""


by_cat = defaultdict(list)
for w in items:
    by_cat[w["cat"]].append(w)

OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.html"):
    old.unlink()
(OUT / "guide.css").write_text(CSS)

for w in items:
    steps_html, howto_steps = [], []
    for s in w["steps"]:
        pr = ""
        if s.get("p"):
            pr = f'<div class="prompt"><b>Prompt to copy</b>{e(s["p"])}</div>'
        steps_html.append(f'<li><h3>{e(s["h"])}</h3><p>{e(s["b"])}</p>{pr}</li>')
        howto_steps.append({"@type": "HowToStep", "name": s["h"], "text": (s["b"] + (" Prompt: " + s["p"] if s.get("p") else ""))[:1000]})
    tags = [w["job"] or w["cat"], w["lvl"], f'{w["mins"]} min'] + w["tools"][:4]
    tips = "".join(f"<li>{e(t)}</li>" for t in w.get("tips", []))
    rel = [x for x in by_cat[w["cat"]] if x["id"] != w["id"]][:4]
    rel_html = "".join(f'<a href="/guides/{x["id"]}">{e(x["t"])}<small>{x["mins"]} min</small></a>' for x in rel)
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": w["t"], "description": w["d"],
          "totalTime": f'PT{w["mins"]}M', "tool": [{"@type": "HowToTool", "name": t} for t in w["tools"]], "step": howto_steps}
    body = f"""
<p class="crumb"><a href="/guides/">Guides</a> › {e(w["cat"])}</p>
<div><h1>{e(w["t"])}</h1><p class="lede">{e(w["d"])}</p>
<div class="tags">{"".join(f"<span>{e(t)}</span>" for t in tags if t)}</div></div>
<div class="cta"><a class="btn" href="/#guide/{w["id"]}">Open the interactive guide</a><a class="btn alt" href="/guides/">Browse all guides</a></div>
<div class="box"><h2>When to use it</h2><p>{e(w["when"])}</p></div>
<section><h2>Step by step</h2><ol class="steps">{"".join(steps_html)}</ol></section>
{f'<div class="box"><h2>What you get</h2><p>{e(w["example"])}</p></div>' if w.get("example") else ""}
{f'<div class="box"><h2>Tips</h2><ul class="tips">{tips}</ul></div>' if tips else ""}
{f'<section><h2>More {e(w["cat"])} guides</h2><div class="related">{rel_html}</div></section>' if rel_html else ""}
"""
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    head = f'<script type="application/ld+json">{ld_json}</script>'
    (OUT / f'{w["id"]}.html').write_text(page(f'{w["t"]} | fishpond', w["d"][:160], f'/guides/{w["id"]}', body, head))

sections = []
for cat in sorted(by_cat):
    lis = "".join(f'<li><a href="/guides/{w["id"]}">{e(w["t"])}</a></li>' for w in sorted(by_cat[cat], key=lambda x: x["t"]))
    sections.append(f'<section class="topic"><h2>{e(cat)}</h2><ul>{lis}</ul></section>')
idx_body = f'<div><h1>All {len(items)} fishpond guides</h1><p class="lede">Free, step-by-step ways to use AI for real tasks at work and at home. No coding needed.</p></div>' + "".join(sections)
(OUT / "index.html").write_text(page(f"All {len(items)} AI guides for work and home | fishpond", "Browse every free fishpond guide: step-by-step AI workflows for email, meetings, money, jobs and everyday life.", "/guides/", idx_body))

urls = [("/", "1.0"), ("/guides/", "0.9"), ("/creators", "0.8"), ("/rung", "0.6")] + [(f'/guides/{w["id"]}', "0.7") for w in items]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"<url><loc>{SITE}{u}</loc><lastmod>{built}</lastmod><priority>{p}</priority></url>" for u, p in urls]
sm.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print(f"{len(items)} guide pages, index, sitemap ({len(urls)} urls) for {SITE}")
