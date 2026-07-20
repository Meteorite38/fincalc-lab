# -*- coding: utf-8 -*-
"""
FinCalc Lab - static site generator
Usage: python build.py          -> renders site into dist/
       python build.py serve    -> build + local preview at http://localhost:8788
"""
import http.server
import json
import os
import shutil
import socketserver
import sys
import datetime

import markdown
from jinja2 import Environment, FileSystemLoader

# ------------------------------------------------- site config
SITE_NAME = "FinCalc Lab"
SITE_TAGLINE = "Free, fast and honest financial calculators"
SITE_URL = "https://fincalc-lab.pages.dev"  # 买好域名后改成正式域名再重新构建
CONTACT_EMAIL = "contact@fincalclab.com"   # 上线前改成你的真实邮箱
INDEXNOW_KEY = "a2fc473d104de2b06f0dc22da1af535f"  # IndexNow 密钥, 用于向 Bing/Yandex 主动推送收录
CURRENT_YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")

sys.path.insert(0, os.path.join(HERE, "content"))
from calcs_data import CALCS  # noqa: E402

MD = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])

env = Environment(loader=FileSystemLoader(os.path.join(HERE, "templates")), autoescape=False)
env.globals.update(
    site_name=SITE_NAME,
    site_tagline=SITE_TAGLINE,
    site_url=SITE_URL,
    contact_email=CONTACT_EMAIL,
    year=CURRENT_YEAR,
)


def write(path, html):
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


def load_md_dir(folder):
    """Read content/<folder>/*.md with simple 'key: value' frontmatter block."""
    out = []
    d = os.path.join(HERE, "content", folder)
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        raw = open(os.path.join(d, fn), encoding="utf-8").read()
        meta = {}
        body = raw
        if raw.startswith("---"):
            _, fm, body = raw.split("---", 2)
            for line in fm.strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
        MD.reset()
        html = MD.convert(body)
        toc_tokens = getattr(MD, "toc_tokens", [])
        out.append({
            "slug": meta.get("slug", fn[:-3]),
            "title": meta.get("title", fn[:-3]),
            "description": meta.get("description", ""),
            "date": meta.get("date", TODAY),
            "html": html,
            "toc": MD.toc if len(toc_tokens) >= 3 else "",
        })
    return out


STOPWORDS = set(
    "the a an and or of to for in on with your you it is are how what why when "
    "that this from as at be by can do does your yours will not no vs your his her "
    "into out over more most than then them they their our we us if but so about "
    "calculator guide money finance financial pay payment rate really actually".split()
)


def _tokens(*parts):
    text = " ".join(p for p in parts if p).lower()
    words = "".join(c if c.isalnum() else " " for c in text).split()
    return {w for w in words if len(w) > 3 and w not in STOPWORDS}


def compute_related(articles):
    """Attach relevance-matched related calculators and guides to each article."""
    def calc_text(c):
        body = c.get("body_html", "")
        # strip tags so we match words, not markup
        body = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in body)
        faqs = " ".join(q + " " + a for q, a in c.get("faqs", []))
        return _tokens(c["h1"], c.get("blurb", ""), c.get("category", ""),
                       c.get("meta_description", ""), c.get("intro", ""), body, faqs)

    calc_tokens = [(c, calc_text(c)) for c in CALCS]
    art_tokens = [(a, _tokens(a["title"], a.get("description", ""), a["slug"].replace("-", " ")))
                  for a in articles]
    for a, atok in art_tokens:
        cs = sorted(calc_tokens, key=lambda ct: len(atok & ct[1]), reverse=True)
        top_calcs = [c for c, t in cs if atok & t][:6]
        if len(top_calcs) < 6:
            have = {c["slug"] for c in top_calcs}
            top_calcs += [c for c in CALCS if c["slug"] not in have][: 6 - len(top_calcs)]
        a["related_calcs"] = top_calcs
        gs = sorted((x for x in art_tokens if x[0]["slug"] != a["slug"]),
                    key=lambda gt: len(atok & gt[1]), reverse=True)
        a["related_guides"] = [g for g, t in gs if atok & t][:4]

    # for each calculator: relevance-matched related calculators and guides
    for c, ctok in calc_tokens:
        others = [(o, t) for o, t in calc_tokens if o["slug"] != c["slug"]]
        same_cat = [o for o, t in others if o["category"] == c["category"]]
        ranked = sorted(others, key=lambda ot: (ot[0]["category"] == c["category"],
                                                len(ctok & ot[1])), reverse=True)
        rel = []
        seen = set()
        for o, t in ranked:
            if o["slug"] not in seen:
                rel.append(o)
                seen.add(o["slug"])
            if len(rel) >= 6:
                break
        c["related_calcs"] = rel
        gs = sorted(art_tokens, key=lambda gt: len(ctok & gt[1]), reverse=True)
        c["related_guides"] = [g for g, t in gs if ctok & t][:4]


def faq_jsonld(calc):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in calc["faqs"]
        ],
    }, ensure_ascii=False)


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(HERE, "static"), os.path.join(DIST, "static"))

    articles = load_md_dir("articles")
    pages = load_md_dir("pages")
    compute_related(articles)
    urls = []

    # calculators
    calc_tpl = env.get_template("calc.html")
    for idx, c in enumerate(CALCS):
        # deterministically surface 3 different guides per calculator for internal linking variety
        related_articles = [articles[(idx + k) % len(articles)] for k in range(min(3, len(articles)))] if articles else []
        html = calc_tpl.render(c=c, calcs=CALCS, articles=articles,
                               related_articles=related_articles, jsonld=faq_jsonld(c))
        write(f"calculators/{c['slug']}/index.html", html)
        urls.append(f"calculators/{c['slug']}/")

    # articles
    art_tpl = env.get_template("article.html")
    for a in articles:
        html = art_tpl.render(a=a, calcs=CALCS, articles=articles)
        write(f"articles/{a['slug']}/index.html", html)
        urls.append(f"articles/{a['slug']}/")

    # legal / static pages
    page_tpl = env.get_template("page.html")
    for p in pages:
        html = page_tpl.render(p=p, calcs=CALCS)
        write(f"{p['slug']}/index.html", html)
        urls.append(f"{p['slug']}/")

    # calculators directory page
    write("calculators/index.html", env.get_template("calc_index.html").render(calcs=CALCS, articles=articles))
    urls.append("calculators/")

    # guides directory page
    write("guides/index.html", env.get_template("guides_index.html").render(calcs=CALCS, articles=articles))
    urls.append("guides/")

    # compare hub page — head-to-head decision tools
    by_slug = {c["slug"]: c for c in CALCS}

    def _cmp_group(label, pairs):
        items = [{"calc": by_slug[s], "question": q} for s, q in pairs if s in by_slug]
        return {"label": label, "items": items}

    compare_groups = [
        _cmp_group("Housing", [
            ("rent-vs-buy-calculator", "Is renting really throwing money away — or is buying the costlier path in your city?"),
            ("15-vs-30-year-mortgage-calculator", "Guaranteed interest savings vs investing the payment difference — which builds more wealth?"),
            ("mortgage-points-calculator", "Pay points up front for a lower rate, or keep the cash — when do you break even?"),
            ("mortgage-refinance-calculator", "Does refinancing actually save money after closing costs, and how soon?"),
            ("biweekly-mortgage-calculator", "Biweekly payments vs monthly — how much time and interest do they really cut?"),
        ]),
        _cmp_group("Cars", [
            ("lease-vs-buy-car-calculator", "Lease payments vs ownership costs minus resale value — which is cheaper over your horizon?"),
            ("auto-loan-calculator", "What does the loan really cost once trade-in, tax rules and fees are included?"),
        ]),
        _cmp_group("Debt vs investing", [
            ("pay-off-debt-vs-invest-calculator", "Extra money each month: kill the debt first, or invest and pay the minimum?"),
            ("debt-snowball-vs-avalanche-calculator", "Smallest-balance-first motivation vs highest-rate-first math — what does each cost?"),
            ("loan-comparison-calculator", "Two loan offers, different rates and fees — which is genuinely cheaper?"),
            ("debt-consolidation-calculator", "Keep juggling separate debts, or roll them into one loan — what changes?"),
        ]),
        _cmp_group("Retirement", [
            ("roth-vs-traditional-401k-calculator", "Pay tax now (Roth) or later (traditional) — which leaves more spendable income?"),
            ("social-security-break-even-calculator", "Claim at 62, full retirement age or 70 — where's the break-even for each?"),
            ("cost-of-waiting-calculator", "Start investing now vs in five years — what does waiting actually cost?"),
        ]),
    ]
    compare_flat = [it["calc"] for g in compare_groups for it in g["items"]]
    write("compare/index.html", env.get_template("compare.html").render(
        calcs=CALCS, articles=articles, groups=compare_groups, flat=compare_flat))
    urls.append("compare/")

    # home
    write("index.html", env.get_template("home.html").render(calcs=CALCS, articles=articles))
    urls.insert(0, "")

    # 404
    write("404.html", env.get_template("notfound.html").render(calcs=CALCS))

    # sitemap + robots
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{SITE_URL}/{u}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

    # IndexNow key file (lets us push new URLs to Bing/Yandex without any login)
    write(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)

    # RSS feed of guides (newest first)
    def esc(s):
        return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;"))

    arts_sorted = sorted(articles, key=lambda a: a["date"], reverse=True)
    items = []
    for a in arts_sorted:
        link = f"{SITE_URL}/articles/{a['slug']}/"
        pub = f"{a['date']}T09:00:00+00:00"
        items.append(
            f"    <item><title>{esc(a['title'])}</title>"
            f"<link>{link}</link><guid>{link}</guid>"
            f"<pubDate>{pub}</pubDate>"
            f"<description>{esc(a['description'])}</description></item>"
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>\n'
        f"  <title>{SITE_NAME} — Money Guides</title>\n"
        f"  <link>{SITE_URL}/guides/</link>\n"
        f"  <description>{SITE_TAGLINE}. Plain-English personal finance guides.</description>\n"
        "  <language>en</language>\n"
        + "\n".join(items) + "\n</channel></rss>\n"
    )
    write("rss.xml", rss)

    print(f"OK: built {len(urls)} pages -> dist/")


def serve():
    import functools
    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    for port in range(8788, 8798):  # if 8788 is busy, try the next few ports
        try:
            with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
                print(f"Preview at http://127.0.0.1:{port}  (Ctrl+C to stop)")
                httpd.serve_forever()
            return
        except OSError:
            print(f"Port {port} busy, trying {port + 1}...")
    print("All ports 8788-8797 are busy. Close other preview servers and retry.")


if __name__ == "__main__":
    build()
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
