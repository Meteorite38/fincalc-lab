# -*- coding: utf-8 -*-
"""向 IndexNow(Bing/Yandex 等)主动推送站点全部 URL, 加速收录。无需任何登录。"""
import json
import re
import urllib.request

KEY = "a2fc473d104de2b06f0dc22da1af535f"
HOST = "fincalc-lab.pages.dev"
BASE = "https://" + HOST


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 FinCalcBot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


sitemap = fetch(BASE + "/sitemap.xml")
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)

payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": f"{BASE}/{KEY}.txt",
    "urlList": urls,
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=data,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow status:", r.status, r.reason, "| URLs submitted:", len(urls))
except urllib.error.HTTPError as e:
    print("IndexNow HTTP", e.code, e.reason, "| URLs:", len(urls))
    print(e.read().decode("utf-8", "replace")[:300])
