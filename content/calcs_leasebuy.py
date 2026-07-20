# -*- coding: utf-8 -*-
"""Lease vs Buy a Car — head-to-head cost comparison over a chosen ownership horizon."""

LEASEBUY = [
    {
        "slug": "lease-vs-buy-car-calculator",
        "emoji": "\U0001F697",
        "category": "Loans & Debt",
        "title": "Lease vs Buy a Car Calculator — Which Is Cheaper?",
        "h1": "Lease vs Buy a Car Calculator",
        "blurb": "Compare the true cost of leasing vs buying over the years you keep it.",
        "meta_description": "Compare leasing vs buying a car by true net cost over the years you'll keep it — including the resale value you keep when you buy. See which is cheaper and by how much.",
        "intro": "Leasing looks cheaper month to month, but buying leaves you owning an asset. This calculator compares the real net cost of each over the years you plan to keep the car, so you can see which actually wins — and by how much.",
        "fields": [
            {"id": "price", "label": "Car price ($)", "value": 35000},
            {"id": "keep", "label": "Years you'll keep the car", "value": 6, "step": 1},
            {"id": "resalepct", "label": "Resale value after those years (% of price)", "value": 45, "step": 1, "hint": "typical: ~45% after 6 years"},
            {"id": "down", "label": "Down payment if buying ($)", "value": 5000},
            {"id": "rate", "label": "Loan interest rate (%)", "value": 7, "step": 0.1},
            {"id": "loanyears", "label": "Loan term (years)", "value": 5, "step": 1},
            {"id": "lease", "label": "Lease payment ($/month)", "value": 400},
            {"id": "leasefees", "label": "Lease upfront + fees over the period ($)", "value": 3000, "hint": "down payment, acquisition & disposition fees"},
        ],
        "js": """
function calculate() {
  const price = val('price'), keep = Math.min(val('keep'), 40), resale = price * val('resalepct')/100;
  const down = val('down'), i = val('rate')/100/12, ly = Math.min(val('loanyears'), 40);
  const lease = val('lease'), leaseFees = val('leasefees');
  if (price <= 0 || keep <= 0) { show('<div class="result-main">Enter a car price and how long you\\'ll keep it.</div>'); return; }
  const P = Math.max(0, price - down), n = Math.round(ly*12), months = Math.round(keep*12);
  const pmt = n > 0 ? (i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n) : 0;
  let bal = P, paid = 0;
  for (let m = 1; m <= months; m++) {
    if (bal <= 0) break;
    const int = bal * i; let principal = pmt - int;
    if (principal > bal) principal = bal;
    bal -= principal; paid += (principal + int);
  }
  const remaining = Math.max(0, bal);
  const buyNet = down + paid + remaining - resale;
  const leaseNet = leaseFees + lease * months;
  const diff = Math.abs(buyNet - leaseNet);
  const buyWins = buyNet < leaseNet;
  show(`<div class="result-main">${buyWins ? 'Buying' : 'Leasing'} is cheaper by $${fmt(diff,0)}<small>over ${keep} years, net of the resale value you keep when buying</small></div>
  <table>
    <tr><td><strong>Buy</strong> \\u2014 net cost over ${keep} yrs</td><td>$${fmt(buyNet,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Down + payments made</td><td>$${fmt(down + paid,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Loan still owed at year ${keep}</td><td>$${fmt(remaining,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Minus resale value kept</td><td>\\u2212$${fmt(resale,0)}</td></tr>
    <tr><td><strong>Lease</strong> \\u2014 net cost over ${keep} yrs</td><td>$${fmt(leaseNet,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Monthly \\u00d7 ${months}</td><td>$${fmt(lease*months,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Upfront + fees</td><td>$${fmt(leaseFees,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why the monthly payment lies</h2>
<p>Lease payments are almost always lower than loan payments on the same car, which makes leasing look cheaper. But that comparison is rigged: a lease payment buys you nothing but temporary use, while a loan payment builds equity in an asset you keep. To compare fairly you have to look at <strong>net cost over the whole period you'll keep the car</strong> — and credit buying with the resale value you walk away with. That's exactly what this calculator does.</p>
<h2>How the comparison works</h2>
<p>For <strong>buying</strong>, it adds up your down payment plus every loan payment you make during the years you keep the car, adds any loan balance still owed at the end, then <em>subtracts</em> the car's resale value (which is yours to sell or keep driving). For <strong>leasing</strong>, it adds every lease payment over the same period plus upfront fees — and credits you nothing at the end, because you hand the car back. The lower net cost wins.</p>
<h2>The decisive factor: how long you keep it</h2>
<p>Time is what flips the answer. Leases are structured to cover a car's steepest depreciation years, so over a single 3-year lease term the gap can be small. But buyers win big when they <strong>keep the car well beyond the loan payoff</strong> — those are years of payment-free driving while the leaser is still making payments forever. Set the "years you'll keep the car" high and buying usually pulls ahead; set it to a short churn cycle and leasing narrows or wins.</p>
<h2>When leasing can still make sense</h2>
<ul>
<li><strong>You want a new car every 2–3 years</strong> and value that over cost — leasing removes resale hassle.</li>
<li><strong>Business use</strong> where lease payments may be deductible (check with a tax professional).</li>
<li><strong>You drive low mileage</strong> and stay within lease limits, avoiding per-mile penalties.</li>
</ul>
<h2>When buying almost always wins</h2>
<ul>
<li><strong>You keep cars a long time.</strong> The longer you drive a paid-off car, the more buying dominates.</li>
<li><strong>You drive a lot.</strong> Leases charge steep per-mile fees over the limit; ownership doesn't care.</li>
<li><strong>You want to build wealth.</strong> A paid-off car is an asset and frees up cash flow — money that can compound instead of vanishing into perpetual payments.</li>
</ul>
<p>Whatever the result here, remember the biggest lever isn't lease-vs-buy at all — it's <a href="/calculators/car-affordability-calculator/">how much car you buy in the first place</a>. Pair this with our <a href="/calculators/car-lease-calculator/">lease payment</a> and <a href="/articles/how-much-to-spend-on-a-car/">how much to spend on a car</a> guides.</p>
""",
        "faqs": [
            ("Is it cheaper to lease or buy a car?", "Over the long run, buying and keeping a car is almost always cheaper, because you eventually stop making payments and keep an asset with resale value. Leasing can be competitive only if you replace the car every few years and value having a new one."),
            ("Why does this calculator subtract resale value?", "Because when you buy, the car is yours to sell or keep driving at the end of the period — that residual value is real money that offsets your cost. A lease returns the car, so you get nothing back. Ignoring resale would unfairly favor leasing."),
            ("What resale percentage should I use?", "A typical car retains very roughly 45% of its price after 6 years, though it varies widely by model — some hold value far better. Check resale estimates for the specific car; models that hold value strengthen the case for buying."),
        ],
    },
]
