# -*- coding: utf-8 -*-
"""RSU tax calculator — vest-day ordinary income, 22%/37% supplemental withholding gap, sell-vs-hold framing."""

RSU = [
    {
        "slug": "rsu-tax-calculator",
        "emoji": "\U0001F4E6",
        "category": "Salary & Work",
        "title": "RSU Tax Calculator — The Withholding Gap That Ambushes Tech Workers",
        "h1": "RSU Tax Calculator",
        "blurb": "Vest-day tax at your real bracket vs the 22% withheld — and the April surprise in between.",
        "meta_description": "Free RSU tax calculator: vesting shares are ordinary income taxed at your marginal rate, but withheld at a flat 22%. See the true tax, the shares sold to cover, the year-end shortfall — and what selling vs holding actually changes.",
        "intro": "RSUs have a simple tax story everyone manages to get wrong: vested shares are ordinary income at your marginal rate, but payroll withholds a flat 22% — and for the six-figure tech incomes that receive RSUs, the real rate is often 32-37%. The gap becomes an April bill nobody budgeted. This calculator computes your vest, the shortfall, and the sell-or-hold math.",
        "fields": [
            {"id": "shares", "label": "Shares vesting", "value": 400, "step": 1},
            {"id": "price", "label": "Share price at vest ($)", "value": 150, "step": 0.01},
            {"id": "marginal", "label": "Your marginal tax rate (%)", "value": 35, "step": 0.5, "hint": "federal bracket + state on your top dollars"},
            {"id": "whrate", "label": "Withholding rate applied (%)", "value": 22, "step": 0.5, "hint": "22% federal supplemental (37% above $1M) — check your stub for state extra"},
            {"id": "fica", "label": "Include 7.65% FICA in withholding?", "type": "select", "value": "yes",
             "options": [("yes", "Yes — under the SS wage cap"), ("med", "Medicare only (1.45%) — over the cap")]},
        ],
        "js": """
function calculate() {
  const n = Math.max(0, Math.round(val('shares'))), p = val('price');
  const tm = val('marginal')/100, wr = val('whrate')/100;
  const ficaSel = document.getElementById('fica').value;
  const ficaRate = ficaSel === 'yes' ? 0.0765 : 0.0145;
  const V = n * p;
  if (V <= 0) { show('<div class="result-main">Enter shares and a vest price.</div>'); return; }
  const trueTax = V * tm;
  const wh = V * (wr + ficaRate);
  const sharesSold = Math.ceil(n * (wr + ficaRate));
  const sharesKept = n - Math.ceil(n * (wr + ficaRate));
  const gap = trueTax + V * ficaRate - wh; // income tax gap (FICA withheld correctly)
  const incomeGap = V * tm - V * wr;
  show(`<div class="result-main">${incomeGap > 0 ? '$' + fmt(incomeGap,0) + ' under-withheld' : 'Withholding roughly covers it'}<small>$${fmt(V,0)} of ordinary income at vest &middot; ~${Math.ceil(n * (wr + ficaRate))} of ${n} shares auto-sold to cover withholding</small></div>
  <table>
    <tr><td>Vest value (${n} × $${fmt(p,2)})</td><td>$${fmt(V,0)} — added to W-2 wages</td></tr>
    <tr><td>True tax at your ${fmt(tm*100,0)}% marginal rate</td><td>$${fmt(trueTax,0)} income tax + $${fmt(V*ficaRate,0)} FICA</td></tr>
    <tr><td>Withheld (${fmt(wr*100,0)}% + ${fmt(ficaRate*100,2)}% FICA)</td><td>$${fmt(wh,0)} — via ~${Math.ceil(n * (wr + ficaRate))} shares sold at vest</td></tr>
    <tr><td><strong>Income-tax shortfall</strong></td><td><strong>${incomeGap > 0 ? '$' + fmt(incomeGap,0) + ' — due at filing (or via extra withholding now)' : '$0'}</strong></td></tr>
    <tr><td>Shares landing in your account</td><td>~${sharesKept} shares (worth $${fmt(sharesKept*p,0)} at vest)</td></tr>
    <tr><td>Set-aside per future vest at these numbers</td><td>${fmt(Math.max(0,(tm - wr))*100,1)}% of each vest's value</td></tr>
  </table>
  <p>${incomeGap > 0
    ? `Fix options: sell ${Math.ceil(incomeGap/p)} more shares at vest and park the cash for taxes, add extra <a href="/calculators/tax-withholding-calculator/">W-4 withholding</a> (it counts as paid evenly all year), or make a <a href="/calculators/quarterly-estimated-tax-calculator/">quarterly estimated payment</a> for the vest quarter.`
    : `Your withholding rate covers the bracket — the remaining decision is purely the hold-vs-sell one below.`}</p>`);
}
""",
        "body_html": """
<h2>How RSUs are actually taxed (simpler than feared)</h2>
<p>Restricted stock units have none of the exotic tax character of options: <strong>on vest day, the market value of the vested shares is ordinary income</strong> — added to your W-2, taxed exactly like salary, subject to Social Security (under the wage cap) and Medicare. There's no election to make, no AMT interaction, nothing to time. If 400 shares vest at $150, you earned $60,000 that day, full stop. Your cost basis in the shares becomes $150 — <strong>only growth after vest is capital gain</strong>. The complexity people feel isn't the tax rule; it's the two operational gaps below.</p>
<h2>Gap #1: the withholding shortfall</h2>
<p>Employers withhold RSU income at the IRS flat supplemental rate — <strong>22%</strong> (37% only above $1M of supplemental wages) — usually by auto-selling a slice of the vest ("sell-to-cover"). But RSU recipients earning $200-500k sit in the 32-35% federal brackets plus state tax. On a $60,000 vest for a 35%-bracket earner, withholding covers $13,200 of a $21,000 income-tax bill — a <strong>$7,800 hole per vest</strong>, times four vests a year, discovered the following April, sometimes with an underpayment penalty attached. The fixes are mechanical: a per-vest set-aside (this calculator's last row), extra salary withholding via <a href="/calculators/tax-withholding-calculator/">W-4 line 4(c)</a> — which counts as paid evenly across the year no matter when it happens — or <a href="/calculators/quarterly-estimated-tax-calculator/">quarterly estimated payments</a>. The same 22%-vs-bracket logic applies to cash bonuses (<a href="/calculators/bonus-tax-calculator/">bonus calculator</a>); RSUs just involve bigger numbers more often.</p>
<h2>Gap #2: holding by default</h2>
<p>After sell-to-cover, the remaining shares sit in your brokerage account — and inertia holds them. Recognize what holding is: <strong>there is no tax benefit to holding a vested RSU.</strong> The income tax was charged at vest either way; holding only changes what happens to growth (long-term capital gains after a year) versus decline (a capital loss capped at $3,000/year of deductibility against income). The clarifying question: <em>if the company paid this vest in cash, would you buy your employer's stock with all of it?</em> If not, holding the shares is the same decision wearing camouflage. And the concentration risk is correlated: the scenario where the stock drops 40% has meaningful overlap with the scenario where layoffs hit — income and portfolio failing together (the <a href="/articles/diversification-explained/">diversification logic</a> applies double to employer stock). The standard playbook — sell on vest, pay the tax gap, invest the rest in <a href="/articles/index-funds-explained/">broad index funds</a> — is boring precisely because it's right for most people. A deliberate, sized position (5-10% of net worth, chosen on purpose) is defensible; 60% of net worth in employer stock by inertia is not a strategy.</p>
<h2>Vest-day mechanics worth knowing</h2>
<ul>
<li><strong>Sell-to-cover is the default</strong>, not the only option — some plans allow paying withholding in cash (keeping all shares) or selling everything at vest. Same-day sales have essentially zero capital gain: proceeds ≈ basis.</li>
<li><strong>The W-2 does the reporting.</strong> Vest income appears in Box 1 automatically. What trips people is the 1099-B from the broker showing the sale with a <em>missing or zero basis</em> — file it uncorrected and you'll pay income tax on the same dollars twice. The basis is the vest-day value; brokers list it in the \"supplemental\" section.</li>
<li><strong>Vests can't be timed, but sales can.</strong> If you do hold, the one-year clock from vest converts further growth to long-term rates (0/15/20%). This only matters for the <em>growth</em>, not the vest value — don't let a $2,000 rate difference on gains hold a $60,000 concentrated position hostage.</li>
<li><strong>Quiet periods and 10b5-1 plans:</strong> employees with material information face trading windows; auto-sale-on-vest elections and 10b5-1 plans execute regardless — one more argument for the automatic sell.</li>
<li><strong>Job change or layoff:</strong> unvested RSUs are typically forfeited — they're compensation for future service, not property. Factor that into offer comparisons: a $150k salary + $100k/yr vesting schedule is not $250k of certainty (the <a href="/calculators/take-home-pay-calculator/">take-home calculator</a> handles the cash; discount the equity by your tenure odds).</li>
</ul>
<h2>Fitting RSUs into the plan</h2>
<p>Treat vests as what they are — <strong>lumpy salary</strong> — and route them like a raise rather than a windfall: tax set-aside first, then the same priority order as any dollar (match, <a href="/calculators/hsa-calculator/">HSA</a>, debt, index funds — the <a href="/articles/financial-order-of-operations/">order of operations</a>). Households whose RSUs are a large income share should budget on salary alone and treat vests as acceleration — grant values reset, stocks swing, and a lifestyle built on peak-vest income is the tech-industry version of the <a href="/articles/lifestyle-creep/">lifestyle creep</a> trap.</p>
""",
        "faqs": [
            ("Do I pay taxes twice on RSUs?", "No — but sloppy filing can. Vest value is taxed once as W-2 income. When you later sell, only growth beyond the vest-day price is capital gain. The double-tax trap is the broker's 1099-B reporting zero basis for sell-to-cover or later sales: enter the correct vest-day basis (from the supplemental broker statement) or you'll re-pay income tax on money already taxed."),
            ("Should I sell RSUs immediately when they vest?", "For most people, yes — the tax was charged at vest regardless, so holding is simply choosing to invest that cash in your employer's stock. The test: would you buy that much company stock with a cash bonus? Holding also stacks portfolio risk on employment risk. Sell-on-vest, cover the withholding gap, diversify the rest is the standard answer; a deliberately-sized small position is a reasonable exception."),
            ("Why did my RSUs push me into owing taxes in April?", "The flat 22% supplemental withholding is below the 32-37% marginal rates most RSU recipients actually pay, so each vest under-withholds by 10-15 points — $6,000-9,000 per $60,000 vest. Fixes: set aside the gap in cash at each vest, add extra W-4 withholding (counts as evenly paid all year), or pay quarterly estimates. High earners should also check the 110% safe harbor to avoid penalties."),
            ("Are RSUs taxed differently from stock options?", "Completely. RSUs: ordinary income at vest, no elections, no AMT. ISOs: no regular tax at exercise but potential AMT, capital-gains treatment if holding periods are met. NSOs: ordinary income on the exercise spread. RSUs are the simple one — the planning is cash management (the withholding gap) and concentration (sell vs hold), not tax structuring."),
            ("What happens to my RSUs if I leave the company?", "Vested shares are yours — they're just stock. Unvested RSUs are almost always forfeited at departure, though treatment varies for retirement, disability, death, or acquisition (accelerated vesting clauses). Check your grant agreement before timing a resignation: leaving three weeks before a large vest is a very expensive scheduling mistake."),
        ],
    },
]
