# -*- coding: utf-8 -*-
"""HSA triple tax advantage — growth projection plus what the same dollars do in a 401(k)/taxable account."""

HSA = [
    {
        "slug": "hsa-calculator",
        "emoji": "\U0001FA79",
        "category": "Retirement",
        "title": "HSA Calculator — The Triple Tax Advantage, Quantified",
        "h1": "HSA Calculator",
        "blurb": "Project your HSA and see the triple tax advantage vs a 401(k) or taxable account.",
        "meta_description": "Free HSA calculator: project your health savings account balance and quantify the triple tax advantage — the same contribution in an HSA vs a traditional 401(k) vs a taxable account, side by side.",
        "intro": "The HSA is the only account in the U.S. tax code where money can go in untaxed, grow untaxed, and come out untaxed. This calculator projects your balance and shows exactly what the triple tax advantage is worth against the same dollars in a 401(k) or a taxable account.",
        "fields": [
            {"id": "balance", "label": "Current HSA balance ($)", "value": 3000},
            {"id": "contrib", "label": "Annual contribution ($)", "value": 4300, "hint": "2025 limits: $4,300 single / $8,550 family"},
            {"id": "spend", "label": "Spent on medical costs each year ($)", "value": 500, "hint": "withdrawals for care along the way"},
            {"id": "ret", "label": "Annual return (%)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Years until retirement", "value": 25, "step": 1},
            {"id": "taxrate", "label": "Marginal tax rate (%)", "value": 24, "step": 0.5},
        ],
        "js": """
function calculate() {
  const B0 = val('balance'), C = val('contrib'), S = val('spend');
  const r = val('ret')/100, yrs = Math.min(100, Math.round(val('years'))), t = val('taxrate')/100;
  if (yrs <= 0 || (B0 <= 0 && C <= 0)) { show('<div class="result-main">Enter a balance or contribution, and years above zero.</div>'); return; }
  const net = C - S;
  // HSA: pre-tax in, tax-free growth, tax-free out (qualified)
  let hsa = B0;
  for (let y = 0; y < yrs; y++) hsa = hsa*(1+r) + net;
  hsa = Math.max(0, hsa);
  // Traditional 401(k): same pre-tax dollars, taxed on withdrawal
  let k401 = B0;
  for (let y = 0; y < yrs; y++) k401 = k401*(1+r) + net;
  const k401After = Math.max(0, k401) * (1 - t);
  // Taxable: contributions are after-tax dollars, returns dragged ~15%
  const rTax = r*0.85;
  let taxable = B0*(1-t);
  for (let y = 0; y < yrs; y++) taxable = taxable*(1+rTax) + net*(1-t);
  taxable = Math.max(0, taxable);
  const fica = C * 0.0765;
  show(`<div class="result-main">$${fmt(hsa,0)}<small>tax-free HSA balance after ${yrs} years (spending $${fmt(S,0)}/yr on care along the way)</small></div>
  <table>
    <tr><td><strong>HSA — spendable on medical, tax-free</strong></td><td><strong>$${fmt(hsa,0)}</strong></td></tr>
    <tr><td>Same dollars in a traditional 401(k), after ${fmt(t*100,0)}% tax</td><td>$${fmt(k401After,0)}</td></tr>
    <tr><td>Same dollars in a taxable account</td><td>$${fmt(taxable,0)}</td></tr>
    <tr><td>Triple-tax edge vs 401(k)</td><td>$${fmt(Math.max(0,hsa-k401After),0)}</td></tr>
    <tr><td>Triple-tax edge vs taxable</td><td>$${fmt(Math.max(0,hsa-taxable),0)}</td></tr>
    <tr><td>Bonus: payroll (FICA) tax avoided per year${net < C ? '' : ''}</td><td>$${fmt(fica,0)} if contributed through payroll</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The only triple-tax-free account in the code</h2>
<p>Every other tax-advantaged account makes you pick one tax break. Traditional 401(k)s and IRAs skip tax going in but tax every dollar coming out. Roth accounts tax the money first and never again. The <strong>HSA does all three</strong>: contributions are deductible (and skip Social Security/Medicare payroll tax too, if made through payroll), growth is never taxed, and withdrawals for qualified medical expenses are tax-free at any age. For a 24%-bracket earner contributing through payroll, roughly 31.65 cents of every HSA dollar is tax that never gets paid — before compounding even starts.</p>
<h2>Who can contribute</h2>
<p>You need to be enrolled in a qualifying <strong>high-deductible health plan (HDHP)</strong> — for 2025, a deductible of at least $1,650 (self) / $3,300 (family) with capped out-of-pocket maximums — and have no disqualifying other coverage (including Medicare, a general-purpose FSA, or being claimed as a dependent). Contribution limits for 2025 are <strong>$4,300 for self-only coverage and $8,550 for family</strong>, plus a $1,000 catch-up from age 55. The limits cover employer contributions too — many employers seed a few hundred dollars, which is free money on top of the tax break.</p>
<h2>The strategy that turns an HSA into a super-IRA</h2>
<p>Most people treat the HSA as a medical checking account: money in, money out at the pharmacy. The optimizer's move is different:</p>
<ul>
<li><strong>Max the contribution</strong> every year you're HDHP-eligible.</li>
<li><strong>Invest the balance</strong> (most custodians allow it above a small cash floor — often $1,000-2,000) rather than leaving it in cash earning nothing.</li>
<li><strong>Pay routine medical costs out of pocket</strong> if you can afford to, letting the HSA compound untouched.</li>
<li><strong>Keep the receipts.</strong> There's no deadline for reimbursing yourself: a $2,000 medical bill from 2026 can justify a tax-free $2,000 withdrawal in 2046, after the money has tripled. Decades of saved receipts become an anytime, any-reason tax-free withdrawal right.</li>
</ul>
<p>From <strong>age 65</strong>, the trapdoor opens further: non-medical withdrawals are allowed with ordinary income tax but no penalty — making the worst-case HSA exactly as good as a traditional IRA, and the medical-case strictly better. Given that a 65-year-old couple is projected to need six figures for healthcare in retirement, "I might not have enough medical expenses" is rarely a real risk.</p>
<h2>Watch-outs</h2>
<ul>
<li><strong>Non-qualified withdrawals before 65</strong> cost income tax plus a 20% penalty — the HSA is a terrible emergency fund. Build a real one first with the <a href="/calculators/emergency-fund-calculator/">emergency fund calculator</a>.</li>
<li><strong>The HDHP itself must make sense.</strong> If you have high, predictable medical costs, a low-deductible plan can beat the HDHP + HSA combination even after the tax breaks — compare total premiums plus expected out-of-pocket costs, not just the tax perk.</li>
<li><strong>Cash-parking kills the magic.</strong> An uninvested HSA earning 0.1% is just a slightly awkward checking account. The triple advantage compounds only if the money is invested.</li>
<li><strong>State quirks:</strong> California and New Jersey don't recognize HSA deductions for state income tax and tax the account's earnings; the federal breaks still apply.</li>
</ul>
<h2>Where the HSA fits in the priority order</h2>
<p>A common-sense funding order for retirement dollars: 401(k) up to the employer match (free money first — see the <a href="/calculators/401k-calculator/">401(k) calculator</a>), then max the HSA, then Roth/traditional contributions per your tax situation (the <a href="/calculators/roth-vs-traditional-401k-calculator/">Roth vs traditional calculator</a> settles that one), then back to the 401(k) limit. Check what the whole stack produces with the <a href="/calculators/retirement-savings-calculator/">retirement savings calculator</a>.</p>
""",
        "faqs": [
            ("Can I use HSA money for anything at 65?", "Yes — after 65, non-medical withdrawals are taxed as ordinary income with no penalty, exactly like a traditional IRA. Medical withdrawals stay completely tax-free. That asymmetry is why the HSA is often called the best retirement account: its worst case matches a traditional IRA and its likely case beats it."),
            ("Should I spend from my HSA or pay medical bills out of pocket?", "If cash flow allows, pay out of pocket and let the HSA stay invested — you can reimburse yourself for documented expenses in any future year, tax-free, after decades of compounding. Keep the receipts (photos/scans in cloud storage are fine)."),
            ("What happens to my HSA if I change jobs or health plans?", "The account is yours forever — it's not tied to the employer, and there's nothing to roll over or forfeit. Losing HDHP coverage only stops new contributions; the existing balance keeps growing and remains spendable on qualified expenses tax-free."),
            ("Do HSA contributions really avoid Social Security and Medicare tax?", "Contributions made through your employer's payroll (a Section 125 plan) skip the 7.65% FICA tax as well as income tax — a break even 401(k) contributions don't get. Direct contributions you make outside payroll are income-tax-deductible but don't avoid FICA."),
        ],
    },
]
