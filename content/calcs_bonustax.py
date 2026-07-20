# -*- coding: utf-8 -*-
"""Bonus tax calculator — 22%/37% supplemental withholding vs actual marginal-rate liability, FICA with caps."""

BONUSTAX = [
    {
        "slug": "bonus-tax-calculator",
        "emoji": "\U0001F4B0",
        "category": "Salary & Work",
        "title": "Bonus Tax Calculator — What You'll Actually Take Home",
        "h1": "Bonus Tax Calculator",
        "blurb": "Bonus withholding (22% federal + FICA + state) and what you truly owe at tax time.",
        "meta_description": "How much tax comes out of a bonus? See the flat 22% federal supplemental withholding, Social Security and Medicare, state tax, your take-home amount — and whether you'll get some back at filing.",
        "intro": "Bonuses aren't taxed at a special punitive rate — they're just withheld differently: a flat 22% federal rate plus payroll and state taxes. Your real tax depends on your bracket, so the paycheck stub and the truth can differ by thousands. This calculator shows both.",
        "fields": [
            {"id": "bonus", "label": "Bonus amount ($)", "value": 10000},
            {"id": "marginal", "label": "Your marginal tax rate (%)", "value": 24, "step": 0.5, "hint": "see our tax bracket calculator"},
            {"id": "state", "label": "State withholding on bonuses (%)", "value": 5, "step": 0.1, "hint": "0 in no-income-tax states"},
            {"id": "ytd", "label": "Wages so far this year, before the bonus ($)", "value": 90000, "hint": "affects Social Security cap"},
        ],
        "js": """
function calculate() {
  const B = val('bonus'), tm = val('marginal')/100, ts = Math.max(0, val('state'))/100, ytd = Math.max(0, val('ytd'));
  if (B <= 0) { show('<div class="result-main">Enter a bonus amount above zero.</div>'); return; }
  const SS_CAP = 176100;
  const fedWH = Math.min(B, 1000000)*0.22 + Math.max(0, B - 1000000)*0.37;
  const ssBase = Math.min(B, Math.max(0, SS_CAP - ytd));
  const ss = ssBase * 0.062;
  const med = B*0.0145 + Math.max(0, (ytd + B) - 200000 > 0 ? Math.min(B, ytd + B - 200000) : 0)*0.009;
  const st = B * ts;
  const totalWH = fedWH + ss + med + st;
  const takeHome = B - totalWH;
  const whPct = totalWH/B*100;
  const trueFed = B * tm;
  const diff = fedWH - trueFed;
  const settleRow = Math.abs(diff) < 1
    ? '<tr><td>At tax time</td><td>withholding roughly matches your bracket — no big swing</td></tr>'
    : (diff > 0
      ? `<tr><td>At tax time</td><td>~$${fmt(diff,0)} over-withheld comes <strong>back as refund</strong> (your ${fmt(tm*100,0)}% bracket &lt; 22% flat rate)</td></tr>`
      : `<tr><td>At tax time</td><td>you'll owe ~$${fmt(-diff,0)} more (your ${fmt(tm*100,0)}% bracket &gt; 22% flat withholding)</td></tr>`);
  const ssNote = ssBase < B ? ` (only $${fmt(ssBase,0)} still under the $${fmt(SS_CAP,0)} cap)` : '';
  show(`<div class="result-main">$${fmt(takeHome,0)} lands in your account<small>$${fmt(totalWH,0)} withheld (${fmt(whPct,1)}%) from a $${fmt(B,0)} bonus</small></div>
  <table>
    <tr><td>Federal supplemental withholding (22%${B > 1000000 ? ' / 37% above $1M' : ''})</td><td>$${fmt(fedWH,0)}</td></tr>
    <tr><td>Social Security (6.2%)${ssNote}</td><td>$${fmt(ss,0)}</td></tr>
    <tr><td>Medicare (1.45%${(ytd + B) > 200000 ? ' + 0.9% additional' : ''})</td><td>$${fmt(med,0)}</td></tr>
    <tr><td>State withholding (${fmt(ts*100,1)}%)</td><td>$${fmt(st,0)}</td></tr>
    <tr><td><strong>Total withheld</strong></td><td><strong>$${fmt(totalWH,0)}</strong></td></tr>
    <tr><td>True federal cost at your ${fmt(tm*100,0)}% bracket</td><td>$${fmt(trueFed,0)}</td></tr>
    ${settleRow}
  </table>`);
}
""",
        "body_html": """
<h2>The myth: "bonuses are taxed at 40%"</h2>
<p>Bonuses are taxed as <strong>ordinary income</strong> — same brackets, same rules, as if the money had been salary. What's different is the <em>withholding</em>. Employers using the standard percentage method hold back a flat <strong>22% federal</strong> on supplemental wages (37% on any amount over $1 million in a year), plus Social Security, Medicare and state tax. Stack those and 30-40% of the bonus never reaches your account — which <em>feels</em> like a special bonus tax. It isn't. Withholding is a deposit, not a price: the real bill is settled by your bracket at filing.</p>
<h2>Refund or bill? Depends which side of 22% you're on</h2>
<ul>
<li><strong>Bracket below 22%</strong> (income mostly in the 10-12% brackets): the flat 22% over-withholds — the difference comes back as a refund at filing.</li>
<li><strong>In the 22% bracket:</strong> withholding roughly matches reality.</li>
<li><strong>Bracket above 22%</strong> (24, 32, 35, 37%): the flat rate <em>under</em>-withholds. A $50,000 bonus for a 35%-bracket earner leaves a $6,500 federal gap to settle at tax time — worth planning for, and occasionally worth a quarterly estimated payment to dodge an underpayment penalty. Find your bracket with the <a href="/calculators/tax-bracket-calculator/">tax bracket calculator</a>.</li>
</ul>
<h2>The payroll-tax fine print</h2>
<p>Two details this calculator handles that most bonus articles skip: <strong>Social Security stops at the wage base</strong> ($176,100 in 2025) — if your regular pay has already crossed it, a year-end bonus owes no 6.2% at all, which is why December bonuses often net more than March ones. And <strong>Medicare never stops</strong> — 1.45% always, plus 0.9% additional once total wages pass $200,000.</p>
<h2>The aggregate method (why your stub might differ)</h2>
<p>Some employers add the bonus to a regular paycheck and withhold as if you earned that combined amount every period — the <strong>aggregate method</strong>. A $10,000 bonus landing in a single pay period can then be withheld at 30%+ federal, as though you made $260,000 a year. Nothing is lost — the excess returns at filing — but the take-home shock is real. If the stub looks brutal, this is usually why.</p>
<h2>Making more of a bonus stick</h2>
<ul>
<li><strong>Divert some to the 401(k).</strong> Most plans let you set a separate bonus deferral percentage. Money routed there skips federal and state income tax entirely (not FICA) — a 32%-bracket earner keeps $320 of every $1,000 sheltered instead of about $580 after taxes. Check the growth effect in the <a href="/calculators/401k-calculator/">401(k) calculator</a>.</li>
<li><strong>Feed the HSA</strong> if you're eligible — the only account that also dodges payroll tax when funded through payroll; see the <a href="/calculators/hsa-calculator/">HSA calculator</a>.</li>
<li><strong>Pre-commit the windfall.</strong> The classic split: some to high-interest debt (<a href="/calculators/pay-off-debt-vs-invest-calculator/">debt vs invest calculator</a>), some to the emergency fund, a slice for fun. A plan made before the money lands beats one made after.</li>
</ul>
""",
        "faqs": [
            ("Why was my bonus taxed at almost 40%?", "You're seeing withholding, not tax: 22% federal supplemental rate + 6.2% Social Security + 1.45% Medicare + state tax easily reaches 35%+. Your actual tax is set by your bracket at filing — if that's below the withholding rate, the difference comes back as a refund."),
            ("Will I get some of my bonus withholding back?", "If your marginal bracket is under 22% (or the aggregate method over-withheld), yes — it returns as a refund when you file. If you're in the 24%+ brackets, the flat 22% actually under-withholds and you may owe more in April instead."),
            ("Can I avoid taxes on a bonus by putting it in my 401(k)?", "You can avoid income tax (federal and usually state) on whatever portion you defer, up to the annual limit — but not Social Security and Medicare. Many payroll systems have a separate 'bonus deferral %' setting; it's the single biggest lever for keeping more of a bonus."),
            ("Are commissions and severance taxed like bonuses?", "Yes — commissions, severance, back pay, and vested RSU value are all 'supplemental wages' under the same rules: flat 22% federal withholding (37% above $1M cumulative), full FICA, and true liability determined by your ordinary bracket at filing."),
        ],
    },
]
