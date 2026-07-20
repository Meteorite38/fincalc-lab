# -*- coding: utf-8 -*-
"""Rent vs Buy a Home — total net cost comparison over a chosen horizon,
including equity, appreciation, ownership costs and the opportunity cost of the down payment."""

RENTBUY = [
    {
        "slug": "rent-vs-buy-calculator",
        "emoji": "\U0001F3E1",
        "category": "Loans & Debt",
        "title": "Rent vs Buy Calculator — Should You Rent or Buy a Home?",
        "h1": "Rent vs Buy a Home Calculator",
        "blurb": "Compare renting vs buying by true net cost over the years you'll stay.",
        "meta_description": "Compare renting vs buying a home by total net cost over the years you'll stay — including mortgage, appreciation, equity, ownership costs and the opportunity cost of your down payment.",
        "intro": "Buying builds equity but ties up cash and adds costs renters never pay. This calculator compares the true net cost of renting vs buying over the years you plan to stay, so you can see which comes out ahead — and by how much.",
        "fields": [
            {"id": "price", "label": "Home price ($)", "value": 350000},
            {"id": "stay", "label": "Years you'll stay", "value": 7, "step": 1},
            {"id": "downpct", "label": "Down payment (%)", "value": 20, "step": 1},
            {"id": "rate", "label": "Mortgage rate (%)", "value": 6.5, "step": 0.05},
            {"id": "term", "label": "Mortgage term (years)", "value": 30, "step": 1},
            {"id": "apprec", "label": "Home appreciation (%/yr)", "value": 3, "step": 0.1},
            {"id": "owncost", "label": "Tax + insurance + maintenance (%/yr of value)", "value": 2, "step": 0.1},
            {"id": "rent", "label": "Monthly rent ($)", "value": 2000},
            {"id": "rentgrow", "label": "Rent increase (%/yr)", "value": 3, "step": 0.1},
            {"id": "invreturn", "label": "Return if you invest the down payment (%/yr)", "value": 5, "step": 0.1},
        ],
        "js": """
function calculate() {
  const price = val('price'), stay = Math.min(Math.max(val('stay'),0), 40);
  const down = price * val('downpct')/100, loan = Math.max(0, price - down);
  const i = val('rate')/100/12, term = Math.min(Math.max(val('term'),0), 40);
  const appr = val('apprec')/100, own = val('owncost')/100;
  const rent0 = val('rent'), rg = val('rentgrow')/100, inv = val('invreturn')/100;
  if (price <= 0 || stay <= 0) { show('<div class="result-main">Enter a home price and how long you\\'ll stay.</div>'); return; }
  const n = Math.round(term*12), months = Math.round(stay*12);
  const pmt = n > 0 ? (i>0 ? loan*i/(1-Math.pow(1+i,-n)) : loan/n) : 0;
  // amortize over the stay
  let bal = loan, piPaid = 0;
  for (let m=1; m<=months; m++){ if(bal<=0) break; const int=bal*i; let pr=pmt-int; if(pr>bal) pr=bal; bal-=pr; piPaid+=(pr+int); }
  const remaining = Math.max(0, bal);
  // ownership costs: tax/ins/maintenance on the (appreciating) home value, summed yearly
  let ownCosts = 0, hv = price;
  for (let y=0; y<stay; y++){ ownCosts += hv * own; hv *= (1+appr); }
  const closing = price * 0.02;              // buy-side closing costs
  const futureValue = price * Math.pow(1+appr, stay);
  const saleNet = futureValue * 0.94;        // ~6% selling costs
  const equityRecovered = saleNet - remaining;
  const buyNet = down + closing + piPaid + ownCosts - equityRecovered;
  // rent: growing annual rent summed over the stay
  let rentTotal = 0, r = rent0*12;
  for (let y=0; y<stay; y++){ rentTotal += r; r *= (1+rg); }
  const invGain = down * (Math.pow(1+inv, stay) - 1);   // opportunity: renter invests the down payment
  const rentNet = rentTotal - invGain;
  const buyWins = buyNet < rentNet;
  const diff = Math.abs(buyNet - rentNet);
  show(`<div class="result-main">${buyWins ? 'Buying' : 'Renting'} is cheaper by $${fmt(diff,0)}<small>total net cost over ${stay} years</small></div>
  <table>
    <tr><td><strong>Buy</strong> — net cost over ${stay} yrs</td><td>$${fmt(buyNet,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Down + closing</td><td>$${fmt(down+closing,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Mortgage paid</td><td>$${fmt(piPaid,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Tax/insurance/upkeep</td><td>$${fmt(ownCosts,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Minus equity at sale</td><td>\\u2212$${fmt(equityRecovered,0)}</td></tr>
    <tr><td><strong>Rent</strong> — net cost over ${stay} yrs</td><td>$${fmt(rentNet,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Total rent paid</td><td>$${fmt(rentTotal,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Minus investing the down payment</td><td>\\u2212$${fmt(invGain,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why "rent is throwing money away" is wrong</h2>
<p>The instinct that renting wastes money while buying builds wealth is only half true. Buying does build equity — but it also carries big costs renters never pay: closing costs, property tax, insurance, maintenance, and the <strong>opportunity cost</strong> of locking a large down payment into a house instead of investing it. A fair comparison has to weigh all of these over the years you'll actually stay. This calculator does exactly that and reports the net cost of each path.</p>
<h2>What goes into each side</h2>
<p><strong>Buying</strong> totals your down payment and closing costs, every mortgage payment during your stay, and ongoing tax/insurance/maintenance — then subtracts the equity you recover when you sell (the appreciated home value, minus selling costs and any remaining loan). <strong>Renting</strong> totals your rent over the same years (growing each year), then subtracts the investment gains you'd earn by putting the down payment you didn't spend into the market instead. Whichever ends with the lower net cost wins.</p>
<h2>The break-even horizon</h2>
<p>The single biggest factor is <strong>how long you stay</strong>. Buying has large upfront and exit costs (closing plus ~6% selling costs), so over a short stay those fixed costs dominate and renting usually wins. The longer you stay, the more those one-time costs spread out and the more equity and appreciation accumulate — tilting the math toward buying. Most buyers need roughly <strong>five years or more</strong> in the home for buying to pay off, though it depends heavily on your local rent-to-price ratio, appreciation and rates. Try dropping "years you'll stay" to 3 and raising it to 10 to see the answer flip.</p>
<h2>The assumptions that swing the result</h2>
<ul>
<li><strong>Appreciation.</strong> Higher home appreciation favors buying; flat or falling prices favor renting. Don't assume boom-era numbers — 2–4% a year is a sober long-run figure.</li>
<li><strong>Investment return.</strong> This is the renter's secret weapon: a down payment invested at 5–7% is real money working for you. The higher this rate, the better renting looks.</li>
<li><strong>Rent growth vs ownership costs.</strong> Fast-rising rents punish renters; high property taxes and maintenance punish owners.</li>
</ul>
<h2>Beyond the numbers</h2>
<p>Money isn't the whole story. Buying offers stability, control, and a forced-savings discipline; renting offers flexibility, no maintenance risk, and mobility for your career. If the costs are close, those lifestyle factors should decide. But run the numbers first — pair this with our <a href="/articles/renting-vs-buying-a-home/">renting vs buying guide</a>, the <a href="/calculators/home-affordability-calculator/">home affordability calculator</a>, and the <a href="/calculators/mortgage-calculator/">mortgage calculator</a> to see the full picture.</p>
""",
        "faqs": [
            ("Is it better to rent or buy a home?", "It depends mainly on how long you'll stay, local prices and rents, appreciation, and what you'd earn investing the down payment instead. Short stays usually favor renting because of buying's high upfront and selling costs; longer stays favor buying as equity and appreciation build."),
            ("How many years until buying beats renting?", "Often around five years, but it varies widely. Areas with high prices relative to rent, high transaction costs, or low appreciation push the break-even point later; cheap-to-buy, fast-appreciating markets bring it earlier. Use the calculator with your real numbers."),
            ("Why does the calculator subtract investment gains from renting?", "Because a renter can invest the money a buyer ties up in a down payment. Those investment gains are a real financial benefit of renting, so ignoring them would unfairly favor buying. It's the opportunity cost that makes the comparison honest."),
        ],
    },
]
