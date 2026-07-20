# -*- coding: utf-8 -*-
"""校验 dist/ 所有页面里的 <script type=application/ld+json> 块都是合法 JSON。"""
import json
import os
import re
import sys

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
bad = []
checked = 0
for root, _, files in os.walk(DIST):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        html = open(os.path.join(root, fn), encoding="utf-8").read()
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            checked += 1
            try:
                json.loads(block)
            except Exception as e:  # noqa: BLE001
                bad.append((os.path.relpath(os.path.join(root, fn), DIST), str(e)[:80]))

print(f"JSON-LD blocks checked: {checked}")
if bad:
    print(f"INVALID: {len(bad)}")
    for p, e in bad[:20]:
        print("  ", p, "->", e)
    sys.exit(1)
print("JSON-LD OK: all blocks parse")
