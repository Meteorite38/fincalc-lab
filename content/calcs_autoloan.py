# -*- coding: utf-8 -*-
"""Auto loan calculator — trade-in, sales tax rules, fees, negative equity roll-in."""

AUTOLOAN = [
    {
        "slug": "auto-loan-calculator",
        "emoji": "\U0001F697",
        "category": "Loans & Debt",
        "title": "Auto Loan Calculator — Payment With Trade-In, Tax & Fees",
        "h1": "Auto Loan Calculator",
        "blurb": "Monthly payment with trade-in value, sales tax, fees and any rolled-in loan balance.",
        "meta_description": "Free auto loan calculator with trade-in, sales tax and fees. See your real monthly payment, total interest, amount financed — and a warning if negative equity is rolled into the new loan.",
        "intro": "Dealer quotes rarely match the loan you actually sign, because sales tax, fees and your trade-in all change the amount financed. Enter the real numbers — including anything still owed on your trade — and see the true payment, total interest and total cost.",
        "fields": [
            {"id": "price", "label": "Vehicle price ($)", "value": 35000},
            {"id": "down", "label": "Cash down payment ($)", "value": 3000},
            {"id": "tradein", "label": "Trade-in value ($)", "value": 8000, "hint": "0 if no trade"},
            {"id": "tradeowed", "label": "Still owed on the trade-in ($)", "value": 5000},
            {"id": "taxrate", "label": "Sales tax rate (%)", "value": 7, "step": 0.1},
            {"id": "taxcredit", "label": "Tax charged on price minus trade-in?", "type": "select", "value": "yes",
             "options": [("yes", "Yes — my state gives a trade-in tax credit (most do)"),
                         ("no", "No — tax on the full price (e.g. CA, VA, HI, KY, MI, MD, DC)")]},
            {"id": "fees", "label": "Title, registration & doc fees ($)", "value": 600},
            {"id": "rate", "label": "Interest rate (APR %)", "value": 7.5, "step": 0.1},
            {"id": "months", "label": "Loan term (months)", "value": 60, "step": 12},
        ],
        "js": """
function calculate() {
  const price = val('price'), down = val('down'), tradeIn = val('tradein'), owed = val('tradeowed');
  const taxRate = val('taxrate')/100, fees = val('fees'), apr = val('rate')/100, n = Math.round(val('months'));
  if (price <= 0 || n <= 0) { show('<div class="result-main">Enter a vehicle price and loan term above zero.</div>'); return; }
  const credit = document.getElementById('taxcredit').value === 'yes';
  const taxable = credit ? Math.max(0, price - tradeIn) : price;
  const salesTax = taxable * taxRate;
  const equity = tradeIn - owed;                    // negative = rolled into the loan
  let financed = price + salesTax + fees - down - equity;
  financed = Math.max(0, financed);
  const i = apr/12;
  const pmt = financed > 0 ? (i > 0 ? financed*i/(1-Math.pow(1+i,-n)) : financed/n) : 0;
  const totalPaid = pmt*n;
  const interest = totalPaid - financed;
  const totalCost = price + salesTax + fees + interest;
  const negRow = equity < 0
    ? `<tr><td><strong>Negative equity rolled in</strong></td><td><strong>$${fmt(-equity,0)}</strong> — you're financing the old car's shortfall on top of the new one</td></tr>`
    : (tradeIn > 0 ? `<tr><td>Trade-in equity applied</td><td>$${fmt(equity,0)}</td></tr>` : '');
  const ltv = financed > 0 && price > 0 ? financed/price*100 : 0;
  const ltvNote = ltv > 100 ? ` &middot; you owe ${fmt(ltv,0)}% of the car's price from day one` : '';
  show(`<div class="result-main">$${fmt(pmt)} / month<small>for ${n} months at ${fmt(apr*100,2)}% APR</small></div>
  <table>
    <tr><td>Amount financed</td><td>$${fmt(financed,0)}${ltvNote}</td></tr>
    <tr><td>Sales tax${credit ? ' (on price minus trade-in)' : ' (on full price)'}</td><td>$${fmt(salesTax,0)}</td></tr>
    ${negRow}
    <tr><td>Total interest</td><td>$${fmt(interest,0)}</td></tr>
    <tr><td>Total of ${n} payments</td><td>$${fmt(totalPaid,0)}</td></tr>
    <tr><td>All-in cost (price + tax + fees + interest)</td><td>$${fmt(totalCost,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What actually determines your car payment</h2>
<p>Four things set the payment: the <strong>amount financed</strong>, the <strong>APR</strong>, the <strong>term</strong>, and nothing else. The amount financed is where most surprises hide. It isn't the sticker price — it's:</p>
<p><em>price + sales tax + fees &minus; cash down &minus; trade-in equity</em></p>
<p>If you still owe more on your trade-in than it's worth, that shortfall (<strong>negative equity</strong>) gets <em>added</em> to the new loan. That's how people end up owing 110% of a car's value the day they drive off — this calculator flags it whenever your inputs imply it.</p>
<h2>The trade-in sales-tax credit</h2>
<p>In most U.S. states you pay sales tax only on <em>price minus trade-in value</em>. Trading in an $8,000 car against a $35,000 purchase at 7% tax saves $560 — a real, often-forgotten part of the trade-in's value when you compare it against selling privately. A handful of places (California, Virginia, Hawaii, Kentucky, Michigan above a cap, Maryland, DC) tax the full price regardless; the calculator has a toggle for both rules.</p>
<h2>Term length: the payment trap</h2>
<p>Dealers sell payments, not prices. Stretching a $30,000 loan at 7.5% from 60 to 84 months drops the payment from about $601 to $461 — but raises total interest from roughly $6,068 to $8,690, and keeps you underwater (owing more than the car's falling value) far longer. A useful discipline is the <strong>20/4/10 rule</strong>: 20% down, no more than 4 years, and total vehicle costs under 10% of gross income. Check the affordability side with the <a href="/calculators/car-affordability-calculator/">car affordability calculator</a>.</p>
<h2>Where to actually save money</h2>
<ul>
<li><strong>Get pre-approved first.</strong> A credit-union or bank pre-approval sets a rate benchmark the dealer's finance office has to beat, turning "what payment do you want?" into a price negotiation.</li>
<li><strong>Negotiate the out-the-door price</strong>, not the monthly payment — the payment can be massaged with term length while the price quietly rises.</li>
<li><strong>Don't roll in negative equity</strong> if you can avoid it. If you must, keep the term short so you surface from being underwater sooner, and consider GAP coverage — after checking what your insurer charges versus the dealer.</li>
<li><strong>Skip financed add-ons.</strong> Paint protection and dealer extended warranties financed at 7%+ for years cost far more than their sticker.</li>
</ul>
<p>Deciding between leasing and buying? Run the numbers in the <a href="/calculators/lease-vs-buy-car-calculator/">lease vs buy calculator</a> or estimate a lease payment directly with the <a href="/calculators/car-lease-calculator/">car lease calculator</a>. And before committing, sanity-check the ongoing running costs with the <a href="/calculators/fuel-cost-calculator/">fuel cost calculator</a>.</p>
""",
        "faqs": [
            ("What credit score do I need for a good auto loan rate?", "Rates step up sharply as scores fall: prime borrowers (roughly 661+) see the advertised rates, while deep-subprime borrowers can pay 3-5x more. If your score is borderline, a co-signer or a few months of score repair often saves more than shopping ten dealerships."),
            ("Should I roll my old car loan into the new one?", "Avoid it if possible — you'd be paying interest on a car you no longer own and starting the new loan underwater. If it's unavoidable, roll in as little as possible, choose a shorter term, and consider GAP coverage so a totaled car doesn't leave you paying for two."),
            ("Is 0% dealer financing really free?", "Sometimes — but it usually replaces a cash rebate. If the choice is 0% APR or a $3,000 rebate, compare the interest you'd pay on a discounted loan (after the rebate) against $0 interest at full price. On smaller loans the rebate frequently wins."),
            ("How much should my down payment be?", "20% is the classic target: it covers first-year depreciation so you're never underwater, lowers the payment, and often gets a better rate. At minimum, cover tax and fees in cash so you're not financing pure paperwork."),
        ],
    },
]
