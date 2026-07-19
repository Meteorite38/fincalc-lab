# -*- coding: utf-8 -*-
"""抓取线上 sitemap 全部 URL, 检查状态码与关键内容, 报告任何异常。"""
import re
import urllib.request

BASE = "https://fincalc-lab.pages.dev"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "FinCalcHealth/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")


status, sitemap = get(BASE + "/sitemap.xml")
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
print(f"Sitemap URLs: {len(urls)}")

problems = []
calc_no_result = []
checked = 0
for u in urls:
    try:
        code, html = get(u)
        checked += 1
        if code != 200:
            problems.append(f"{code} {u}")
            continue
        if "/calculators/" in u:
            # calc pages must have the interactive box and a calculate() script
            if 'id="calc"' not in html or "function calculate()" not in html:
                calc_no_result.append(u)
        # crude JSON-LD sanity: balanced braces in each ld+json block
        for block in re.findall(r'application/ld\+json">(.*?)</script>', html, re.S):
            if block.count("{") != block.count("}"):
                problems.append(f"JSONLD-brace-mismatch {u}")
                break
    except Exception as e:  # noqa: BLE001
        problems.append(f"ERR {type(e).__name__} {u}")

print(f"Checked: {checked}")
print(f"Calc pages missing interactive box: {len(calc_no_result)}")
for c in calc_no_result:
    print("   ", c)
print(f"Problems: {len(problems)}")
for p in problems:
    print("   ", p)
print("HEALTHCHECK DONE" if not problems and not calc_no_result else "HEALTHCHECK FOUND ISSUES")
