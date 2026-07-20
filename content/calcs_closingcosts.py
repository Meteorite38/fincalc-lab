# -*- coding: utf-8 -*-
"""Closing costs calculator — itemized buyer-side estimate by fee family, cash-to-close, and points/credits trade-off."""

CLOSING = [
    {
        "slug": "closing-costs-calculator",
        "emoji": "\U0001F511",
        "category": "Loans & Debt",
        "title": "Closing Costs Calculator — What You'll Actually Pay at the Table",
        "h1": "Closing Costs Calculator",
        "blurb": "Itemized buyer closing costs and total cash to close — lender, title, escrow and prepaids.",
        "meta_description": "Free closing costs calculator: itemized estimate of lender fees, title insurance, appraisal, escrow prepaids and transfer taxes — plus total cash needed at closing on top of your down payment.",
        "intro": "Closing costs are the least transparent part of buying a home: a dozen fees from four different parties, most quoted only after you're emotionally committed. Typical total: 2-5% of the loan. This calculator itemizes a realistic estimate and answers the question that actually matters — how much cash you need at the table.",
        "fields": [
            {"id": "price", "label": "Home price ($)", "value": 400000},
            {"id": "downpct", "label": "Down payment (%)", "value": 10, "step": 0.5},
            {"id": "rate", "label": "Mortgage rate (%)", "value": 6.5, "step": 0.01},
            {"id": "state", "label": "Transfer tax & recording level", "type": "select", "value": "med",
             "options": [("low", "Low-tax state (~0.1% — e.g. TX, MO, IN)"), ("med", "Typical (~0.5%)"), ("high", "High-tax metro (1.5%+ — e.g. NY, PA, WA, DE)")]},
            {"id": "points", "label": "Discount points purchased", "value": 0, "step": 0.25, "hint": "1 point = 1% of loan, buys ~0.25% off the rate"},
            {"id": "credit", "label": "Seller or lender credits ($)", "value": 0, "hint": "negotiated credits toward your costs"},
        ],
        "js": """
function calculate() {
  const price = val('price'), dpct = Math.min(100, Math.max(0, val('downpct')))/100;
  const rate = val('rate')/100, pts = Math.max(0, val('points')), credit = Math.max(0, val('credit'));
  const lvl = document.getElementById('state').value;
  if (price <= 0) { show('<div class="result-main">Enter a home price.</div>'); return; }
  const down = price * dpct, L = price - down;
  // lender fees
  const origination = Math.max(995, L * 0.005);
  const underwriting = 550;
  const pointsCost = L * pts / 100;
  // third-party
  const appraisal = price > 1000000 ? 800 : 550;
  const creditReport = 65, floodCert = 20, taxService = 85;
  // title & escrow (scale with price)
  const lenderTitle = Math.max(500, price * 0.0022);
  const ownerTitle = Math.max(600, price * 0.0026);
  const settlement = 450 + price * 0.0005;
  const recording = 150;
  // government
  const xferRate = lvl === 'low' ? 0.001 : (lvl === 'high' ? 0.015 : 0.005);
  const transfer = price * xferRate;
  // prepaids & escrow reserves
  const taxRate = 0.011, insRate = 0.0035;
  const prepaidIns = price * insRate;                 // first year up front
  const escrowTax = price * taxRate / 12 * 4;         // ~4 months reserves
  const escrowIns = prepaidIns / 12 * 2;
  const perDiem = L * rate / 365;
  const prepaidInterest = perDiem * 15;               // mid-month close
  const lenderFees = origination + underwriting + pointsCost;
  const thirdParty = appraisal + creditReport + floodCert + taxService;
  const titleFees = lenderTitle + ownerTitle + settlement + recording;
  const prepaids = prepaidIns + escrowTax + escrowIns + prepaidInterest;
  const total = lenderFees + thirdParty + titleFees + transfer + prepaids - credit;
  const cashToClose = down + total;
  const pctOfLoan = total / L * 100;
  show(`<div class="result-main">~$${fmt(Math.max(0,total),0)} in closing costs<small>${fmt(pctOfLoan,1)}% of the $${fmt(L,0)} loan &middot; total cash to close: <strong>$${fmt(Math.max(0,cashToClose),0)}</strong> including the $${fmt(down,0)} down payment</small></div>
  <table>
    <tr><td><strong>Lender fees</strong> — origination, underwriting${pts > 0 ? `, ${pts} point${pts === 1 ? '' : 's'}` : ''}</td><td>$${fmt(lenderFees,0)}</td></tr>
    <tr><td><strong>Third-party</strong> — appraisal, credit report, flood cert, tax service</td><td>$${fmt(thirdParty,0)}</td></tr>
    <tr><td><strong>Title &amp; escrow</strong> — lender's + owner's title insurance, settlement, recording</td><td>$${fmt(titleFees,0)}</td></tr>
    <tr><td><strong>Government</strong> — transfer tax &amp; stamps (${fmt(xferRate*100,2)}%)</td><td>$${fmt(transfer,0)}</td></tr>
    <tr><td><strong>Prepaids &amp; escrow</strong> — 1st-yr insurance, ~4 mo tax reserves, ${15} days interest</td><td>$${fmt(prepaids,0)}</td></tr>
    ${credit > 0 ? `<tr><td>Seller / lender credits</td><td>&minus;$${fmt(credit,0)}</td></tr>` : ''}
    <tr><td><strong>Estimated closing costs</strong></td><td><strong>$${fmt(Math.max(0,total),0)}</strong></td></tr>
    <tr><td>+ Down payment</td><td>$${fmt(down,0)}</td></tr>
    <tr><td><strong>Cash to close</strong></td><td><strong>$${fmt(Math.max(0,cashToClose),0)}</strong></td></tr>
  </table>
  <p>Roughly $${fmt(prepaids,0)} of this isn't a fee at all — prepaid insurance, tax escrow and interest are your own future bills paid early. The negotiable money lives in the lender and title lines: $${fmt(lenderFees + titleFees,0)} here.</p>`);
}
""",
        "body_html": """
<h2>Where the money actually goes</h2>
<p>"Closing costs" bundles four unrelated bills into one scary number. <strong>Lender fees</strong> (origination, underwriting, points) pay for making the loan — typically 0.5-1% of it. <strong>Third-party services</strong> (appraisal ~$550, credit report, flood certification) are mostly fixed-price and non-negotiable. <strong>Title and escrow</strong> — the two title insurance policies, settlement agent, recording — scale with the price and vary enormously by state. <strong>Government transfer taxes</strong> range from trivial (Texas: none) to brutal (NYC, Philadelphia, Seattle: 1.5-3%+). And then there are <strong>prepaids</strong>, which aren't fees at all: your first year of homeowners insurance, a few months of property-tax escrow, and interest from closing day to month-end — money you'd owe anyway, just collected early. Separating the categories matters because only some of them can be shopped or negotiated.</p>
<h2>The Loan Estimate: your comparison weapon</h2>
<p>Within three business days of applying, every lender must send a standardized <strong>Loan Estimate</strong> — same three pages, same line items, by law. Page 2 splits costs into sections A (the lender's own fees — compare these hardest), B (required services the lender picks), and C (<strong>services you can shop for</strong> — title insurance and settlement are the big ones). Collect Loan Estimates from 2-3 lenders in the same week and the differences leap out: identical rates can hide a $2,000 gap in section A. At closing, the final <strong>Closing Disclosure</strong> must reconcile against the estimate — lender fees legally can't rise at all, and most shopped services are capped at 10% aggregate increase. Combine this with rate shopping via the <a href="/calculators/loan-comparison-calculator/">loan comparison calculator</a> and the <a href="/calculators/mortgage-points-calculator/">points break-even</a>.</p>
<h2>What's negotiable (more than you think)</h2>
<ul>
<li><strong>Origination and underwriting fees</strong> — banks waive or discount these routinely for strong applicants, especially with a competing Loan Estimate in hand.</li>
<li><strong>Owner's title insurance</strong> — premiums are regulated in some states and pure list-price in others; independent title companies often beat the agent's default referral by hundreds. Ask for the "reissue rate" if the home changed hands within the last ~10 years — commonly 25-40% off.</li>
<li><strong>Seller credits</strong> — in a balanced or buyer's market, asking the seller to cover 1-3% of costs is standard practice. Conventional loans cap seller credits at 3% (under 10% down), 6% (10-25% down); the credit often costs the seller less than an equivalent price cut would save you monthly.</li>
<li><strong>Lender credits</strong> — the reverse of points: accept a slightly higher rate (+0.125-0.25%) and the lender pays part of your costs. Worth it when cash is tight or you expect to refinance within a few years anyway.</li>
</ul>
<h2>Budgeting: the cash-to-close surprise</h2>
<p>The number that derails first-time buyers isn't the down payment — it's everything stacked on top. A 10%-down purchase of a $400,000 home needs $40,000 down <em>plus</em> $10,000-14,000 at the table, and the earnest-money deposit (1-3%) has to be liquid weeks earlier. Lenders also want to see <strong>reserves</strong> — often 2 months of payments still in the bank <em>after</em> closing. Practical sequence: size the down payment with the <a href="/calculators/house-down-payment-calculator/">down payment calculator</a>, add this calculator's estimate, add two months of the payment from the <a href="/calculators/mortgage-calculator/">mortgage calculator</a>, and that's the real savings target before house-hunting starts. If the down payment lands under 20%, price the <a href="/calculators/pmi-calculator/">PMI</a> into the monthly budget too.</p>
<h2>Refinance closing costs work the same way</h2>
<p>A refinance re-runs most of this list — origination, appraisal, title (lender's policy only), recording — typically <strong>2-3% of the loan</strong>, with two mercies: no transfer tax in most states, and no owner's title policy needed. Since the whole point of refinancing is saving money, the costs must be recovered by the monthly savings; the <a href="/calculators/mortgage-refinance-calculator/">refinance calculator</a> computes that break-even month directly. Beware "no-closing-cost" refinances — the costs are real, just rolled into the rate or balance; fine if you'll move soon, expensive if you stay 20 years.</p>
""",
        "faqs": [
            ("How much are closing costs on a $400,000 house?", "Typically $8,000-18,000 for a buyer (2-5% of the loan), with the spread driven mostly by state transfer taxes and title insurance rates. In Texas or Missouri expect the low end; in New York, Pennsylvania, Washington or Delaware the government line alone can add 1.5-3% of the price. Prepaid insurance and tax escrow — your own future bills — are usually a quarter to a third of the total."),
            ("Can closing costs be rolled into the mortgage?", "On a purchase, generally no for conventional loans — costs must be paid at the table (seller and lender credits are the workarounds). On a refinance, yes: most lenders let you finance the costs into the new balance, which preserves cash but accrues interest on the fees for the life of the loan. USDA and VA purchases allow limited financing of specific fees."),
            ("Who pays closing costs — buyer or seller?", "Both, different bills. Buyers pay lender, title, escrow and prepaid items (2-5% of the loan). Sellers traditionally pay the agent commissions plus, depending on local custom, the owner's title policy and part of the transfer tax. Almost everything is negotiable in the purchase contract — in soft markets, seller credits covering 1-3% of the buyer's costs are routine."),
            ("Why did my cash-to-close change between the Loan Estimate and closing?", "The usual movers are the prepaid and escrow lines — the exact per-diem interest depends on your closing date, and the tax escrow depends on the county's billing calendar. Lender fees can't legally increase from the Loan Estimate, and shopped third-party services are capped at 10% aggregate. Compare the two documents line by line; the CFPB's rules make any true fee increase the lender's problem, not yours."),
            ("Are closing costs tax-deductible?", "Mostly no. The exceptions: discount points on a purchase are deductible (immediately, if you itemize and meet the tests), prepaid mortgage interest is deductible like any mortgage interest, and property taxes paid at closing count toward the SALT deduction. Appraisal, title, origination and transfer fees aren't deductible — but they do add to your cost basis, trimming future capital gains when you sell."),
        ],
    },
]
