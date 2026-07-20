# -*- coding: utf-8 -*-
"""PMI calculator — monthly cost, automatic-termination vs borrower-requested cancellation dates, appreciation-accelerated path."""

PMI = [
    {
        "slug": "pmi-calculator",
        "emoji": "\U0001F6AA",
        "category": "Loans & Debt",
        "title": "PMI Calculator — Cost Per Month and Exactly When It Ends",
        "h1": "PMI Calculator",
        "blurb": "Your monthly PMI, total cost, and the three dates it can end — including the appreciation shortcut.",
        "meta_description": "Free PMI calculator: monthly private mortgage insurance cost, the automatic termination date at 78% LTV, when you can request cancellation at 80% — and how home appreciation moves that date years earlier.",
        "intro": "PMI is the fee for buying with less than 20% down — typically $30-70 a month per $100,000 borrowed, protecting the lender, not you. But it isn't forever: federal law sets two end dates, and home appreciation often unlocks a third, much earlier one. This calculator prices your PMI and maps all three exits.",
        "fields": [
            {"id": "price", "label": "Home price ($)", "value": 400000},
            {"id": "down", "label": "Down payment ($)", "value": 20000},
            {"id": "rate", "label": "Mortgage rate (%)", "value": 6.5, "step": 0.01},
            {"id": "term", "label": "Loan term (years)", "value": 30, "step": 1},
            {"id": "pmirate", "label": "PMI rate (% of loan per year)", "value": 0.6, "step": 0.05, "hint": "0.3-0.8% typical with good credit; up to 1.5% below 680"},
            {"id": "appr", "label": "Expected home appreciation (%/yr)", "value": 3, "step": 0.1},
        ],
        "js": """
function calculate() {
  const price = val('price'), down = val('down');
  const r = val('rate')/100/12, yrs = Math.min(50, Math.max(1, Math.round(val('term')))), n = yrs*12;
  const pmiR = Math.max(0, val('pmirate'))/100, g = val('appr')/100;
  if (price <= 0 || down < 0 || down >= price) { show('<div class="result-main">Enter a home price and a down payment smaller than it.</div>'); return; }
  const L = price - down;
  const ltv0 = L / price * 100;
  if (ltv0 <= 80) {
    show(`<div class="result-main">No PMI required<small>your down payment is ${fmt(100-ltv0,1)}% — at or above the 20% threshold, conventional loans carry no mortgage insurance</small></div>`);
    return;
  }
  const pay = r > 0 ? L * r / (1 - Math.pow(1 + r, -n)) : L / n;
  const pmiMo = L * pmiR / 12;
  // amortize; track three exits
  let bal = L, mAuto = -1, mReq = -1, mAppr = -1;
  for (let m = 1; m <= n; m++) {
    bal -= (pay - bal * r);
    if (mAuto < 0 && bal <= price * 0.78) mAuto = m;
    if (mReq < 0 && bal <= price * 0.80) mReq = m;
    if (mAppr < 0) {
      const vNow = price * Math.pow(1 + g, m / 12);
      // servicer current-value rules: 75% LTV for loans 2-5 yrs old, 80% after 5 yrs; under 2 yrs rarely allowed
      const needLtv = m >= 60 ? 0.80 : 0.75;
      if (m >= 24 && bal <= vNow * needLtv) mAppr = m;
    }
  }
  if (mAuto < 0) mAuto = n;
  if (mReq < 0) mReq = n;
  const fmtM = (m) => `${Math.floor(m/12)} yr ${m%12} mo`;
  const costAuto = pmiMo * mAuto, costReq = pmiMo * mReq;
  const apprRow = (g > 0 && mAppr > 0 && mAppr < mReq)
    ? `<tr><td><strong>Appreciation shortcut</strong> — reappraisal at ${fmt(g*100,1)}%/yr growth</td><td><strong>${fmtM(mAppr)}</strong> &middot; PMI paid: $${fmt(pmiMo*mAppr,0)} (saves $${fmt(costReq - pmiMo*mAppr,0)} vs waiting)</td></tr>`
    : '';
  show(`<div class="result-main">$${fmt(pmiMo,0)}/month PMI<small>${fmt(pmiR*100,2)}% per year on a $${fmt(L,0)} loan — ${fmt(ltv0,1)}% starting LTV</small></div>
  <table>
    <tr><td>Mortgage payment (P&amp;I)</td><td>$${fmt(pay,0)}/month &middot; $${fmt(pay + pmiMo,0)} with PMI</td></tr>
    <tr><td>Request cancellation at 80% LTV (original value)</td><td>${fmtM(mReq)} &middot; PMI paid by then: $${fmt(costReq,0)}</td></tr>
    <tr><td>Automatic termination at 78% LTV</td><td>${fmtM(mAuto)} &middot; PMI paid by then: $${fmt(costAuto,0)}</td></tr>
    ${apprRow}
    <tr><td>PMI as an effective cost of the missing down payment</td><td>${fmt(pmiMo*12 / Math.max(1, price*0.2 - down) * 100,1)}% per year on the $${fmt(Math.max(0, price*0.2 - down),0)} gap</td></tr>
  </table>
  <p>${(g > 0 && mAppr > 0 && mAppr < mReq)
    ? `At ${fmt(g*100,1)}%/yr appreciation, a <strong>reappraisal around ${fmtM(mAppr)}</strong> beats waiting for the amortization schedule — a $400-600 appraisal fee vs $${fmt(costReq - pmiMo*mAppr,0)} of avoided premiums.`
    : `Extra principal payments pull both dates closer — every dollar of prepayment is a dollar less the 80% threshold has to wait for; the <a href="/calculators/extra-mortgage-payment-calculator/">extra payment calculator</a> shows the effect.`}</p>`);
}
""",
        "body_html": """
<h2>What PMI is — and what it isn't</h2>
<p>Private mortgage insurance protects the <strong>lender</strong> against loss if a low-down-payment loan defaults; the borrower pays the premium and receives nothing but loan approval. That approval has value — PMI is the price of buying now instead of after years of saving toward 20% (a timeline the <a href="/calculators/house-down-payment-calculator/">down payment calculator</a> makes concrete). The premium runs <strong>0.3% to 1.5% of the loan per year</strong> depending mostly on credit score and LTV: a 760-score borrower putting 10% down might pay 0.3-0.5%; a 650 score with 5% down can pay triple that. On a $380,000 loan at 0.6%, that's $190 a month — real money, but not the villain it's often made out to be.</p>
<h2>The three ways PMI ends</h2>
<ul>
<li><strong>Borrower-requested cancellation at 80% LTV (original value).</strong> Under the federal Homeowners Protection Act, when your balance amortizes to 80% of the <em>original</em> purchase price (or appraised value at closing, if lower), you can request cancellation in writing — good payment history required, and the request is yours to make, not the servicer's to volunteer.</li>
<li><strong>Automatic termination at 78% LTV.</strong> If you never ask, the servicer must drop PMI when the balance hits 78% of original value on the amortization schedule (and the loan is current). With 10% down at today's rates, that's typically year 5-7; with 3-5% down, year 8-11.</li>
<li><strong>The appreciation shortcut.</strong> Most servicers will also cancel based on <em>current</em> value with a new appraisal: commonly 75% LTV if the loan is 2-5 years old, 80% after 5 years (exactly the thresholds this calculator applies). In a market rising 4-5% a year, a 10%-down buyer can hit 75% of current value by year 2-3 — years ahead of the schedule, for the cost of a $400-600 appraisal.</li>
</ul>
<h2>Reframing the cost: PMI as a loan rate on the gap</h2>
<p>Here's the calculation that changes minds. PMI isn't really a fee on your whole mortgage — it's the cost of borrowing the down payment you don't have. Put 5% down instead of 20% and the "missing" 15% ($60,000 on a $400,000 house) costs you, say, $190 &times; 12 = $2,280 a year: an effective <strong>3.8% interest rate on that gap</strong> — often cheaper than the years of rent paid while saving it, and far cheaper than most people assume. The calculator's last row prices your own gap. The corollary: draining the emergency fund to dodge PMI is usually the worse trade — check what cushion you need first with the <a href="/calculators/emergency-fund-calculator/">emergency fund calculator</a>.</p>
<h2>Ways to skip or shed PMI</h2>
<ul>
<li><strong>Lender-paid PMI (LPMI):</strong> the lender "waives" PMI for a ~0.25-0.5 point higher rate — permanent, baked into the rate for the life of the loan. Usually loses to borrower-paid PMI that cancels in year 4-7, unless you'll sell quickly.</li>
<li><strong>Piggyback 80/10/10:</strong> a second loan (often a <a href="/calculators/heloc-calculator/">HELOC</a>) covers part of the down payment, keeping the first mortgage at 80%. Works when the second loan's rate is modest; compare total monthly cost, not just the PMI line.</li>
<li><strong>Prepay principal early.</strong> Every extra dollar shortens the runway to 80%. Small consistent prepayments in the first years often pull cancellation forward by 12-24 months.</li>
<li><strong>Watch the market.</strong> If nearby comps are up 10%+ since purchase, call the servicer and ask their current-value cancellation rules before spending on the appraisal — requirements vary by servicer and by how long you've had the loan.</li>
<li><strong>FHA is a different animal:</strong> FHA mortgage insurance (MIP) can't be cancelled at 80% — with under 10% down it lasts the life of the loan, and the standard exit is <a href="/calculators/mortgage-refinance-calculator/">refinancing into a conventional loan</a> once equity reaches 20%.</li>
</ul>
<h2>The calendar-reminder move</h2>
<p>Servicers profit from inertia: automatic termination at 78% is the law's backstop, but the 80% request date arrives 1-2 years earlier and requires you to act. When you close on a low-down-payment loan, set two reminders — one at the projected 80% date from this calculator, one annually to sanity-check local prices against the appreciation shortcut. Ten minutes of paperwork routinely saves $2,000-5,000 of premiums; fold the freed-up cash into the payment itself and the <a href="/calculators/amortization-schedule-calculator/">amortization schedule</a> compresses further.</p>
""",
        "faqs": [
            ("How much is PMI per month?", "Roughly $30-125 per $100,000 borrowed per month, set mainly by credit score and down payment size: strong credit with 10-15% down lands near the bottom of that range (0.3-0.5%/yr); scores under 680 with 3-5% down reach 1-1.5%/yr. It's charged on the loan balance, so the dollar amount is fixed at origination and drops only when PMI is recalculated or removed."),
            ("Can I cancel PMI without refinancing?", "Yes — that's the point of the Homeowners Protection Act. At 80% LTV against original value you can request cancellation in writing; at 78% it must drop automatically. And most servicers allow earlier cancellation against current appraised value (75-80% LTV depending on loan age). Refinancing is only the necessary route for FHA loans with permanent MIP."),
            ("Does PMI cover me if I can't pay my mortgage?", "No — it reimburses the lender's losses after your default and foreclosure. You pay the premium, the lender holds the protection. Borrower-side protection comes from an emergency fund and, where it makes sense, disability or life insurance sized to the mortgage."),
            ("Is PMI tax-deductible?", "The federal PMI deduction expired after tax year 2021 and hasn't been renewed as of 2025, so for most borrowers it's not deductible. Even in the years it existed, it phased out above ~$100k of AGI. Treat PMI as a pure cost when running the numbers."),
            ("Should I make a bigger down payment just to avoid PMI?", "Run PMI as an interest rate on the down-payment gap (this calculator's last row). If the effective rate is 3-5% and cancellable within a few years, stretching to 20% by draining savings — or delaying the purchase years while renting — is often the more expensive choice. If the rate computes to 8%+ (small down payment, weak credit), waiting or a piggyback structure deserves a look."),
        ],
    },
]
