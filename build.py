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
        out.append({
            "slug": meta.get("slug", fn[:-3]),
            "title": meta.get("title", fn[:-3]),
            "description": meta.get("description", ""),
            "date": meta.get("date", TODAY),
            "html": MD.convert(body),
        })
    return out


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

    print(f"OK: built {len(urls)} pages -> dist/")


def serve():
    import functools
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    with socketserver.TCPServer(("127.0.0.1", 8788), handler) as httpd:
        print("Preview at http://127.0.0.1:8788  (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    build()
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
