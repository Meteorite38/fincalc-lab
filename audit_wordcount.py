# -*- coding: utf-8 -*-
"""审计文章正文字数，找出可能偏薄(<600词)的内容。"""
import os
import re

d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content", "articles")
rows = []
for f in sorted(os.listdir(d)):
    if not f.endswith(".md"):
        continue
    t = open(os.path.join(d, f), encoding="utf-8").read()
    body = t.split("---", 2)[-1]
    wc = len(re.findall(r"[A-Za-z0-9']+", body))
    rows.append((wc, f))
rows.sort()
print("total articles", len(rows))
print("--- 12 shortest ---")
for wc, f in rows[:12]:
    print(f"{wc:5d}  {f}")
print("median", rows[len(rows) // 2][0])
print("under 600:", sum(1 for wc, _ in rows if wc < 600))
