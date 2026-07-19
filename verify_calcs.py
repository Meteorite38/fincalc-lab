# -*- coding: utf-8 -*-
"""
无浏览器计算器回归测试台。
对 CALCS 里每个计算器: 用默认输入在 Node 里跑一遍 calculate(), 校验 JS 语法与运行时无异常, 并打印结果文本。
用法: python verify_calcs.py
"""
import json
import os
import re
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
    if (f.isSelect) {
      const opts = f.options.map(o => ({ value: o.value, text: o.text }));
      return { value: String(f.value), options: opts, selectedIndex: f.selectedIndex };
    }
    return { value: String(f.value) };
  },
  addEventListener: function(){}
};
function fmt(x, dp = 2){ if(!isFinite(x)) return "\u2014"; return x.toLocaleString("en-US",{minimumFractionDigits:dp,maximumFractionDigits:dp}); }
function val(id){ return parseFloat(document.getElementById(id).value) || 0; }
function show(html){ __resultEl.innerHTML = html; }
%s
calculate();
console.log(__resultEl.innerHTML.replace(/<[^>]+>/g," | ").replace(/\s+/g," ").trim());
"""


def default_inputs(calc):
    d = {}
    for f in calc["fields"]:
        if f.get("type") == "select":
            opts = f["options"]
            chosen = str(f.get("value", opts[0][0]))
            idx = next((i for i, o in enumerate(opts) if str(o[0]) == chosen), 0)
            d[f["id"]] = {
                "isSelect": True,
                "value": chosen,
                "selectedIndex": idx,
                "options": [{"value": str(o[0]), "text": str(o[1])} for o in opts],
            }
        else:
            d[f["id"]] = {"value": f.get("value", 0)}
    return d


def main():
    ok, fail = 0, 0
    for c in CALCS:
        fields = default_inputs(c)
        js = STUB % (json.dumps(fields), c["js"])
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
            tf.write(js)
            path = tf.name
        try:
            r = subprocess.run(["node", path], capture_output=True, text=True, timeout=30, encoding="utf-8")
        finally:
            os.unlink(path)
        if r.returncode == 0 and r.stdout.strip():
            ok += 1
            out = r.stdout.strip()
            print(f"[PASS] {c['slug']:<42} -> {out[:90]}")
        else:
            fail += 1
            err = (r.stderr or r.stdout).strip().splitlines()
            msg = err[-1] if err else "no output"
            print(f"[FAIL] {c['slug']:<42} -> {msg[:140]}")
    print(f"\n==== {ok} passed, {fail} failed, {len(CALCS)} total ====")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
