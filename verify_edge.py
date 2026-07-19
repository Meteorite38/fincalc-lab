# -*- coding: utf-8 -*-
"""
边界值测试台: 用极端输入(全零/负数/超大)跑每个计算器, 捕捉 NaN / Infinity / undefined
泄漏到显示结果里的 bug。这些是最伤可信度的错误。
用法: python verify_edge.py
"""
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "content"))
from calcs_data import CALCS  # noqa: E402

STUB = r"""
const __fields = %s;
const __resultEl = { innerHTML: "", classList: { add: function(){} } };
const document = {
  getElementById: function(id){
    if (id === "result") return __resultEl;
    const f = __fields[id];
    if (!f) return { value: "" };
    if (f.isSelect) return { value: String(f.value), options: f.options.map(o=>({value:o.value,text:o.text})), selectedIndex: f.selectedIndex };
    return { value: String(f.value) };
  },
  addEventListener: function(){}
};
function fmt(x, dp = 2){ if(!isFinite(x)) return "\u2014"; return x.toLocaleString("en-US",{minimumFractionDigits:dp,maximumFractionDigits:dp}); }
function val(id){ return parseFloat(document.getElementById(id).value) || 0; }
function show(html){ __resultEl.innerHTML = html; }
try { %s
calculate();
console.log(__resultEl.innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim());
} catch(e){ console.log("EXCEPTION: " + e.message); }
"""

BAD = ("NaN", "Infinity", "undefined", "null", "$NaN", "NaN%")


def make_fields(calc, mode):
    d = {}
    for f in calc["fields"]:
        if f.get("type") == "select":
            opts = f["options"]
            chosen = str(f.get("value", opts[0][0]))
            idx = next((i for i, o in enumerate(opts) if str(o[0]) == chosen), 0)
            d[f["id"]] = {"isSelect": True, "value": chosen, "selectedIndex": idx,
                         "options": [{"value": str(o[0]), "text": str(o[1])} for o in opts]}
        else:
            if mode == "zero":
                v = 0
            elif mode == "neg":
                v = -5
            elif mode == "big":
                v = 1e12
            else:
                v = f.get("value", 0)
            d[f["id"]] = {"value": v}
    return d


def run(calc, fields):
    js = STUB % (json.dumps(fields), calc["js"])
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
        tf.write(js)
        path = tf.name
    try:
        r = subprocess.run(["node", path], capture_output=True, text=True, timeout=30, encoding="utf-8")
    finally:
        os.unlink(path)
    return (r.stdout or "").strip() + (("\n" + r.stderr.strip()) if r.stderr.strip() else "")


def main():
    issues = []
    for c in CALCS:
        for mode in ("zero", "neg", "big"):
            out = run(c, make_fields(c, mode))
            if out.startswith("EXCEPTION"):
                issues.append((c["slug"], mode, out[:120]))
                continue
            hits = [b for b in BAD if b in out]
            if hits:
                issues.append((c["slug"], mode, f"leaked {hits}: {out[:90]}"))
    if not issues:
        print("EDGE OK: no NaN/Infinity/undefined/exceptions across zero/neg/big inputs for all",
              len(CALCS), "calculators")
    else:
        print(f"FOUND {len(issues)} edge issues:")
        for slug, mode, msg in issues:
            print(f"  [{mode:>4}] {slug:<40} {msg}")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
