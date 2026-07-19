# -*- coding: utf-8 -*-
"""检查 dist/ 里所有站内链接 href="/..." 是否都指向真实生成的页面。"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")


def page_exists(path):
    path = path.split("#")[0].split("?")[0]
    if path in ("/", ""):
        return os.path.isfile(os.path.join(DIST, "index.html"))
    rel = path.strip("/")
    # /foo/  -> foo/index.html ; /foo.xml -> foo.xml ; /static/x -> static/x
    if os.path.isfile(os.path.join(DIST, rel)):
        return True
    if os.path.isfile(os.path.join(DIST, rel, "index.html")):
        return True
    return False


broken = {}
for root, _, files in os.walk(DIST):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(root, fn)
        html = open(fp, encoding="utf-8").read()
        for href in re.findall(r'href="(/[^"]*)"', html):
            if href.startswith("//"):
                continue
            if not page_exists(href):
                broken.setdefault(href, set()).add(os.path.relpath(fp, DIST))

if not broken:
    print("LINKS OK: every internal href resolves to a real page")
else:
    print(f"BROKEN internal links: {len(broken)}")
    for href, pages in sorted(broken.items()):
        sample = list(pages)[:3]
        print(f"  {href}   <- {len(pages)} page(s), e.g. {sample}")
import sys  # noqa: E402
sys.exit(1 if broken else 0)
