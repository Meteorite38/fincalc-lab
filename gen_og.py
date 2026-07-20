# -*- coding: utf-8 -*-
"""生成 Open Graph 分享大图(1200x630) -> static/og/。
一张默认站点图 + 每个计算器分类一张, 供社交/搜索预览卡使用。纯 PIL 离线绘制。"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "static", "og")
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 630
INK = (20, 33, 61)
ACCENT = (11, 110, 79)
GOLD = (252, 163, 17)
LIGHT = (233, 238, 243)


def font(size, bold=True):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def gradient_bg():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(INK[0] + (8 - INK[0]) * t)
        g = int(INK[1] + (40 - INK[1]) * t)
        b = int(INK[2] + (34 - INK[2]) * t)
        d.line([(0, y), (W, y)], fill=(max(0, r), max(0, g), max(0, b)))
    return img


def make(filename, title, subtitle, tag):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    # accent bar
    d.rectangle([0, 0, W, 12], fill=ACCENT)
    d.rectangle([0, H - 12, W, H], fill=GOLD)
    # brand: drawn logo mark (mini bar chart) + wordmark
    d.rounded_rectangle([70, 60, 126, 116], radius=12, fill=ACCENT)
    bx = [82, 98, 114]
    bh = [30, 44, 22]
    for x, h in zip(bx, bh):
        d.rectangle([x, 104 - h, x + 8, 104], fill=(255, 255, 255))
    d.text((142, 66), "FinCalc Lab", font=font(40), fill=(255, 255, 255))
    # tag pill
    tf = font(26)
    tw = d.textlength(tag, font=tf)
    d.rounded_rectangle([70, 150, 70 + tw + 44, 200], radius=25, fill=ACCENT)
    d.text((92, 160), tag, font=tf, fill=(255, 255, 255))
    # title (wrap)
    tfont = font(70)
    words = title.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=tfont) > W - 140 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    lines.append(cur)
    y = 250
    for ln in lines[:3]:
        d.text((70, y), ln, font=tfont, fill=(255, 255, 255))
        y += 82
    # subtitle
    d.text((70, min(y + 10, H - 110)), subtitle, font=font(30, bold=False), fill=LIGHT)
    img.save(os.path.join(OUT, filename), "PNG")
    return filename


made = []
made.append(make("default.png", "Free financial calculators that just work",
                 "No sign-up. Nothing tracked. The math, explained.", "110 calculators \u00b7 70 guides"))
made.append(make("calculators.png", "Financial calculators with the math explained",
                 "Savings, loans, retirement, tax, business & more", "Free tools"))
made.append(make("guides.png", "Plain-English money guides",
                 "Investing, debt, retirement & budgeting explained", "Guides"))

cats = {
    "Mortgages & Home": ("Mortgage & home calculators", "Payments, refinancing, equity & buying costs"),
    "Savings & Investing": ("Savings & investing calculators", "Compound interest, goals, returns & fees"),
    "Retirement": ("Retirement calculators", "401(k), FIRE, Social Security & withdrawals"),
    "Debt & Credit": ("Debt & credit calculators", "Payoff plans, consolidation & credit health"),
    "Budgeting & Life": ("Budgeting & life calculators", "Budgets, emergency funds & life decisions"),
    "Salary & Work": ("Salary & work calculators", "Take-home pay, raises, bonuses & offers"),
    "Taxes & Shopping": ("Tax & shopping calculators", "Brackets, withholding, sales tax & tips"),
    "Business & Self-Employment": ("Business & self-employment calculators", "Freelance rates, SE tax, margins & runway"),
    "Cars & Commuting": ("Car & commuting calculators", "Loans, leases, true costs & fuel"),
}
for cat, (t, s) in cats.items():
    slug = cat.lower().replace(" & ", "-").replace(" ", "-")
    made.append(make(f"cat-{slug}.png", t, s, "Free tools"))

print("OK: generated", len(made), "OG images ->", OUT)
for m in made:
    print("  ", m)
