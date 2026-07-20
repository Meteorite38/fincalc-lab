# -*- coding: utf-8 -*-
"""Pension lump sum vs annuity — implied return to match the pension (money's-worth), portfolio survival framing."""

PENSIONLUMP = [
    {
        "slug": "pension-lump-sum-vs-annuity-calculator",
        "emoji": "\U0001F3DB\uFE0F",
        "category": "Retirement",
        "title": "Pension Lump Sum vs Annuity Calculator — Which Offer Is Worth More?",
        "h1": "Pension Lump Sum vs Annuity Calculator",
        "blurb": "The return your lump sum must earn to match the pension checks — the one number that decides.",
        "meta_description": "Free pension lump sum vs annuity calculator: computes the internal rate of return the lump sum must earn to replicate the monthly pension for your life expectancy — plus payout ratios and inflation erosion, so you can judge the buyout offer.",
        "intro": "A pension buyout offer compresses a lifetime of monthly checks into one number — and the company making the offer profits when you take it cheap. The honest test: what return would the lump sum have to earn to pay you the same checks for as long as you're likely to live? This calculator computes that hurdle rate and both futures.",
        "fields": [
            {"id": "lump", "label": "Lump sum offered ($)", "value": 300000},
            {"id": "monthly", "label": "Monthly pension if you decline ($)", "value": 2000, "hint": "single-life or joint amount, as offered"},
            {"id": "age", "label": "Your age when payments start", "value": 65, "step": 1},
            {"id": "lifeexp", "label": "Plan to age", "value": 90, "step": 1, "hint": "65-year-olds: ~50% odds of reaching 85-88; plan past the average"},
            {"id": "ret", "label": "Return you'd earn investing the lump (%)", "value": 5.5, "step": 0.1, "hint": "balanced portfolio, after fees"},
            {"id": "cola", "label": "Pension COLA (%/yr)", "value": 0, "step": 0.5, "hint": "most private pensions: 0 — no inflation adjustment"},
        ],
        "js": """
function calculate() {
  const L = val('lump'), M = val('monthly'), a0 = Math.round(val('age'));
  const aEnd = Math.max(a0 + 1, Math.round(val('lifeexp')));
  const r = val('ret')/100, cola = Math.max(0, val('cola'))/100;
  if (L <= 0 || M <= 0) { show('<div class="result-main">Enter the lump sum and the monthly pension.</div>'); return; }
  const months = (aEnd - a0) * 12;
  // total nominal payout
  let totalPay = 0, pmt = M;
  for (let m = 0; m < months; m++) { totalPay += pmt; if ((m+1) % 12 === 0) pmt *= (1 + cola); }
  // IRR: rate at which lump exactly funds the stream. bisection on monthly rate
  const pvAt = (rm) => {
    let pv = 0, p = M;
    for (let m = 0; m < months; m++) { pv += p / Math.pow(1 + rm, m + 1); if ((m+1) % 12 === 0) p *= (1 + cola); }
    return pv;
  };
  let lo = 0, hi = 0.02;
  if (pvAt(0) < L) { lo = -0.005; hi = 0; } // lump bigger than undiscounted stream (rare)
  for (let i = 0; i < 60; i++) { const mid = (lo + hi) / 2; if (pvAt(mid) > L) lo = mid; else hi = mid; }
  const irr = Math.pow(1 + (lo + hi) / 2, 12) - 1;
  // simulate taking the lump, investing at r, drawing the pension amount
  let bal = L, p2 = M, ranOutAge = null;
  for (let m = 0; m < months; m++) {
    bal = bal * (1 + r/12) - p2;
    if ((m+1) % 12 === 0) p2 *= (1 + cola);
    if (bal <= 0 && ranOutAge === null) { ranOutAge = a0 + Math.floor((m+1)/12); break; }
  }
  const payout = M * 12 / L * 100;
  const verdict = irr > r + 0.01
    ? `The pension is the stronger offer: matching it requires <strong>${fmt(irr*100,2)}%</strong> every year to age ${aEnd} — more than the ${fmt(r*100,1)}% you expect to earn. Guaranteed checks winning by that margin are hard to beat${cola === 0 ? ', though inflation (below) is the caveat' : ''}.`
    : (irr < r - 0.01
      ? `The lump sum is the stronger offer: the pension is only "paying" an implied <strong>${fmt(irr*100,2)}%</strong> — below the ${fmt(r*100,1)}% you can reasonably expect. Take the money, invest it, and keep the flexibility and the inheritance.`
      : `Genuinely close: the implied return (<strong>${fmt(irr*100,2)}%</strong>) sits near your expected ${fmt(r*100,1)}%. Let the soft factors decide — health, spouse protection, inflation, and how much you value never managing the money.`);
  show(`<div class="result-main">${fmt(irr*100,2)}% required return<small>what the $${fmt(L,0)} must earn, every year to age ${aEnd}, to replicate the $${fmt(M,0)}/month pension</small></div>
  <table>
    <tr><td>Annual payout rate (year-1 pension &divide; lump)</td><td>${fmt(payout,1)}% <small>(rule of thumb: ~6%+ favors the pension at 65)</small></tr>
    <tr><td>Total checks to age ${aEnd}${cola > 0 ? ' (with ' + fmt(cola*100,1) + '% COLA)' : ''}</td><td>$${fmt(totalPay,0)}</td></tr>
    <tr><td>Invest the lump at ${fmt(r*100,1)}%, draw the same checks</td><td>${ranOutAge ? '<strong>money runs out at age ' + ranOutAge + '</strong>' : 'survives to ' + aEnd + ' with $' + fmt(Math.max(0,bal),0) + ' left for heirs'}</td></tr>
    ${cola === 0 ? `<tr><td>What $${fmt(M,0)} buys in 20 years at 2.5% inflation</td><td>~$${fmt(M/Math.pow(1.025,20),0)} of today's purchasing power — fixed pensions shrink in real terms</td></tr>` : ''}
  </table>
  <p>${verdict}</p>`);
}
""",
        "body_html": """
<h2>The one number that cuts through the fog</h2>
<p>Comparing $300,000 today against $2,000 a month for life is comparing apples to a subscription. The clean translation is the <strong>implied return</strong> (an internal rate of return): the annual yield the lump sum would have to generate, every year until your planning age, to write you the same checks. If that hurdle is 6.5% and your realistic after-fee expectation for a retirement portfolio is 5-5.5%, the pension is paying you more than the market plausibly will — decline the buyout. If the hurdle is 3.5%, the offer is generous (or the pension small); take the money. Everything else — payout ratios, break-even ages — is this number wearing different clothes.</p>
<h2>Why the deck is often stacked toward "take the lump"</h2>
<p>Companies offer buyouts to shed pension liability, and the offer is calculated under IRS-prescribed rates — when interest rates are high, the mandated present value shrinks, so <strong>lump sums offered in high-rate years are systematically smaller</strong> relative to the checks they replace. The offer letter also frames the number to look enormous ($300,000!) against a modest-sounding monthly figure, exploiting the well-documented tendency to undervalue annuities. And the risk transfer is total: decline the buyout and longevity risk, market risk and management burden stay with the plan; accept it and all three are yours. None of this means the lump is wrong — it means the burden of proof sits on the buyout, and the implied return is how you check it.</p>
<h2>What favors the pension (annuity)</h2>
<ul>
<li><strong>You (or your spouse) might live long.</strong> The pension pays until death — the scenario that bankrupts self-managed money is exactly the one where the annuity shines. A 65-year-old couple has better-than-even odds one of them reaches 90.</li>
<li><strong>The implied return beats your honest portfolio expectation</strong> — commonly the case for long-tenured employees whose formulas were set in generous eras.</li>
<li><strong>You want a guaranteed income floor.</strong> Pension + Social Security covering the baseline budget converts the rest of the portfolio into genuinely spendable, risk-tolerant money — and neutralizes <a href="/articles/sequence-of-returns-risk/">sequence-of-returns risk</a> on the necessities.</li>
<li><strong>Behavioral honesty:</strong> if a six-figure account would get raided for kitchens, kids and market panics, the pension's inaccessibility is a feature. PBGC insurance backstops private pensions (up to ~$7,100/month at 65 for single-employer plans in 2025), so "the company might fail" is a smaller risk than it sounds — below that ceiling.</li>
</ul>
<h2>What favors the lump sum</h2>
<ul>
<li><strong>Health or family history points shorter.</strong> The annuity's value collapses if payments stop early; the lump is inheritable — roll it to an IRA and it passes to heirs, while most single-life pensions die with you.</li>
<li><strong>No or weak survivor benefit.</strong> Joint-and-survivor options cut the check 10-20%; if the pension is single-life and your spouse would be stranded, the lump (or the lump + a term policy sized with the <a href="/calculators/life-insurance-needs-calculator/">life insurance calculator</a>) can protect them better.</li>
<li><strong>No COLA.</strong> Most private pensions are frozen nominal — at 2.5% inflation, the check loses ~40% of its purchasing power over 20 years. A portfolio can at least try to grow; the <a href="/calculators/inflation-calculator/">inflation calculator</a> shows the erosion.</li>
<li><strong>The implied return is low</strong> and you have the discipline (or an advisor) to invest the rollover sensibly — model the drawdown with the <a href="/calculators/retirement-withdrawal-calculator/">withdrawal calculator</a>.</li>
</ul>
<h2>Practical notes before you sign anything</h2>
<p><strong>Roll, don't cash.</strong> A lump sum taken as a check is ordinary income in one year — a six-figure tax detonation plus <a href="/calculators/401k-early-withdrawal-calculator/">early-withdrawal penalty</a> if you're under 59&frac12;. A direct rollover to an IRA is tax-free and preserves every option. <strong>Price the annuity externally:</strong> get a quote for a commercial single-premium immediate annuity paying the same monthly amount — if insurers charge more than your lump offer, the pension is underpriced (keep it); if they charge less, the buyout is rich. <strong>Decide jointly:</strong> the survivor-benefit election is usually irrevocable and requires spousal consent for good reason. And remember the decision isn't all-or-nothing at the household level — many couples keep one pension as the income floor and roll the other, and coordinate the whole stack with the <a href="/calculators/social-security-break-even-calculator/">Social Security claiming decision</a>, which is itself the cheapest inflation-adjusted annuity money can't buy more of.</p>
""",
        "faqs": [
            ("Is there a rule of thumb for judging a lump sum offer?", "The payout ratio: first-year pension divided by the lump. At 65, offers below ~5.5-6% generally favor taking the pension (the checks are cheap to decline); above ~7%, the annuity is hard to replicate and worth keeping. But the implied-return calculation this tool runs is strictly better — the rule of thumb ignores COLAs, start ages and your actual planning horizon."),
            ("What happens to my pension if the company goes bankrupt?", "Private single-employer pensions are insured by the PBGC up to a cap — about $7,100/month for a 65-year-old single-life annuity in 2025 (lower for early retirement or survivor options). Benefits under the cap have historically been paid in full. If your check would exceed the cap, bankruptcy risk becomes a real argument for the lump sum; below it, much less so."),
            ("Can I take the lump sum and buy my own annuity?", "Yes — that's the cleanest market test. Get SPIA quotes for the same monthly income: if $280,000 buys what your $300,000 lump replaces, take the lump, spend $280,000 on the annuity (or don't), and pocket the difference. If it costs $340,000, your pension is underpriced — keep it. Quotes are free and this comparison takes an afternoon."),
            ("How is the survivor benefit decision related?", "Declining the buyout usually means choosing single-life (bigger check, stops at your death) vs joint-and-survivor (10-20% smaller, continues for your spouse). If you take the smaller joint check, you're effectively buying life insurance from the pension plan; occasionally buying term insurance with the single-life difference protects the spouse more cheaply — but only while insurable, and the pension's version never lapses."),
            ("Do I owe tax on a pension lump sum?", "Not if it's directly rolled into an IRA or 401(k) — the rollover is tax-free and the money keeps growing tax-deferred until withdrawal (then taxed as ordinary income, with RMDs eventually applying). Taken as cash, the entire amount is taxable income that year, usually at painfully stacked rates, plus a 10% penalty under 59½. Virtually everyone who takes the lump should roll it."),
        ],
    },
]
