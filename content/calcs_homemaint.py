# -*- coding: utf-8 -*-
"""Home maintenance budget — age/climate/size-adjusted 1-2% rule, component sinking-fund schedule, monthly set-aside."""

HOMEMAINT = [
    {
        "slug": "home-maintenance-budget-calculator",
        "emoji": "\U0001F528",
        "category": "Mortgages & Home",
        "title": "Home Maintenance Budget Calculator — The Cost Nobody Puts in the Mortgage Math",
        "h1": "Home Maintenance Budget Calculator",
        "blurb": "Your realistic annual maintenance number — age, climate and size adjusted — as a monthly set-aside.",
        "meta_description": "Free home maintenance budget calculator: the 1-2% rule adjusted for home age, climate and size, a component-by-component replacement schedule (roof, HVAC, water heater), and the monthly sinking-fund transfer that makes $9,000 roof years boring.",
        "intro": "Maintenance is the housing cost that hides between the big years: $80 filter months, then a $9,000 roof. Averaged honestly it runs 1-2% of home value every year — but your number depends on the home's age, your climate, and whether a big component is due. This calculator personalizes the budget and turns it into a monthly transfer.",
        "fields": [
            {"id": "value", "label": "Home value ($)", "value": 400000},
            {"id": "age", "label": "Home age (years)", "value": 25, "step": 1},
            {"id": "sqft", "label": "Size (sq ft)", "value": 1900, "step": 50},
            {"id": "climate", "label": "Climate stress", "type": "select", "value": "mid",
             "options": [("mild", "Mild (coastal CA, PNW)"), ("mid", "Moderate (most of the US)"), ("harsh", "Harsh (freeze-thaw, hail, humidity, salt air)")]},
            {"id": "condition", "label": "Recent condition", "type": "select", "value": "avg",
             "options": [("new", "Renovated / major systems new"), ("avg", "Average — mixed ages"), ("worn", "Deferred maintenance to catch up on")]},
        ],
        "js": """
function calculate() {
  const V = val('value'), age = Math.max(0, Math.round(val('age'))), sqft = Math.max(300, val('sqft'));
  const climate = document.getElementById('climate').value;
  const cond = document.getElementById('condition').value;
  if (V <= 0) { show('<div class="result-main">Enter a home value.</div>'); return; }
  let pct = 0.01;
  pct += age < 10 ? -0.002 : (age < 25 ? 0.001 : (age < 50 ? 0.004 : 0.007));
  pct += climate === 'mild' ? -0.001 : (climate === 'harsh' ? 0.003 : 0);
  pct += cond === 'new' ? -0.003 : (cond === 'worn' ? 0.005 : 0);
  pct = Math.max(0.005, Math.min(0.025, pct));
  // blend value-based with sqft-based ($4-6/sqft/yr modern estimate) for high-value-land markets
  const byValue = V * pct;
  const bySqft = sqft * 5;
  const annual = (byValue + bySqft) / 2;
  const monthly = annual / 12;
  const rows = [
    ['Roof (asphalt)', 20, 12000], ['HVAC / furnace + AC', 17, 9000], ['Water heater', 11, 1800],
    ['Exterior paint / siding refresh', 9, 5000], ['Appliance rotation (each ~12 yr)', 4, 1200],
    ['Windows (as a set)', 30, 15000], ['Driveway / concrete', 28, 5000],
  ].map(([name, life, cost]) => `<tr><td>${name}</td><td>~${life} yrs</td><td>$${fmt(cost,0)} &rarr; $${fmt(cost/life/12,0)}/mo</td></tr>`).join('');
  show(`<div class="result-main">$${fmt(monthly,0)}/month<small>&asymp; $${fmt(annual,0)}/year (${fmt(annual/V*100,2)}% of home value) — auto-transfer it to a dedicated savings account</small></div>
  <table>
    <tr><td>Value-based estimate (${fmt(pct*100,2)}% for age/climate/condition)</td><td>$${fmt(byValue,0)}/yr</td></tr>
    <tr><td>Size-based estimate ($5/sq ft)</td><td>$${fmt(bySqft,0)}/yr</td></tr>
    <tr><td><strong>Blended budget</strong></td><td><strong>$${fmt(annual,0)}/yr &middot; $${fmt(monthly,0)}/mo</strong></td></tr>
  </table>
  <p>Where the money eventually goes — the component clock that explains the average:</p>
  <table>
    <tr><th>Component</th><th>Typical life</th><th>Cost &rarr; monthly reserve</th></tr>
    ${rows}
  </table>
  <p>${age >= 20 && cond !== 'new'
    ? `At ${age} years old, this home is inside the replacement window for 2-3 major components — if the roof or HVAC hasn't been done, expect the <em>lumpy</em> version of this average soon and consider front-loading the fund for a year.`
    : `A newer or renovated home runs below the long-run average for now — bank the quiet years anyway; the average always arrives eventually.`}</p>`);
}
""",
        "body_html": """
<h2>Why 1-2% — and why your number isn't the average</h2>
<p>The classic guideline says budget <strong>1% of home value per year</strong> for maintenance and repairs, stretching toward 2% for older homes. The logic isn't that every year costs that — it's that <em>component replacement clocks</em> average out to it: a $12,000 roof every 20 years is $600/year; a $9,000 HVAC every 17 is $530; water heater, paint, appliances, gutters, the annual parade of small fixes — stack the reserves and a typical home lands at 1-1.5% of value. Your personal rate moves with three things this calculator adjusts for: <strong>age</strong> (a 5-year-old home coasts on new components; a 50-year-old one is on its second or third cycle of everything), <strong>climate</strong> (freeze-thaw, hail, humidity and salt air all shorten component lives), and <strong>condition</strong> (a just-renovated home has its clocks reset; deferred maintenance is a debt with its own interest). In high-land-value markets (where a $900,000 house is mostly lot), the percentage overstates costs — that's why the calculator blends in a per-square-foot estimate, since roofs are priced by area, not by ZIP-code prestige.</p>
<h2>The sinking fund is the entire strategy</h2>
<p>Maintenance ruins budgets not because it's large but because it's <strong>lumpy</strong> — years of $600, then an $11,000 summer. The fix is mechanical: a dedicated high-yield savings account, an automatic monthly transfer of this calculator's number, and a rule that home repairs come from it and nothing else does. Now the roof year is boring — the money was collected $250 at a time across a decade. This is a <a href="/articles/sinking-funds-saving-for-big-purchases/">sinking fund</a> doing exactly what sinking funds do, and it belongs in the budget as a fixed line, not as an aspiration (the <a href="/calculators/budget-calculator/">budget calculator</a> treats it as a bill, which is correct). Two boundary rules keep it honest: the <a href="/calculators/emergency-fund-calculator/">emergency fund</a> is for income shocks, not water heaters — a component failing on schedule is not an emergency, it's an appointment; and renovations/upgrades are a separate goal — the maintenance fund keeps the house working, not remodeled.</p>
<h2>Spending it well: the maintenance hierarchy</h2>
<ul>
<li><strong>Prevention is the highest-return tier:</strong> gutter cleaning, HVAC filters and annual service, caulk and grout, tree limbs off the roof, water heater flushes. A few hundred a year here prevents four-figure failures — water intrusion alone causes a huge share of expensive damage, and almost all of it starts as a $150 gutter or caulk fix.</li>
<li><strong>Repair-vs-replace has a rule of thumb:</strong> multiply the repair quote by the component's age, divide by expected life — if repair cost &times; age &gt; 50% of replacement &times; life remaining, replace. A $700 compressor repair on a 15-year-old AC is usually money thrown at a dying unit.</li>
<li><strong>Timing beats urgency pricing:</strong> replace a 19-year-old roof on <em>your</em> schedule (three quotes, off-season) rather than after the leak (tarps, water damage, whoever can come Tuesday). The fund is what buys that timing.</li>
<li><strong>Some years, spend down deliberately:</strong> if the balance grows past ~2 big-component costs, the excess can flow to other goals — the fund is a buffer, not a hoard.</li>
</ul>
<h2>Where this fits in the buying decision</h2>
<p>Maintenance is the third leg of the true monthly cost of ownership — payment (<a href="/calculators/mortgage-calculator/">mortgage calculator</a>), taxes and insurance (<a href="/calculators/property-tax-calculator/">property tax calculator</a>), then this. A $2,400 P&amp;I payment on an older home in a harsh climate is really a $3,200+ commitment once taxes and a realistic maintenance reserve are stacked — which is exactly the stress-test the <a href="/calculators/home-affordability-calculator/">affordability calculator</a> runs and the <a href="/calculators/rent-vs-buy-calculator/">rent-vs-buy comparison</a> depends on (renters famously never see this line; owners who ignore it meet it as credit card debt). Budgeting it before the offer is what separates a house that fits from one that slowly doesn't.</p>
""",
        "faqs": [
            ("How much should I budget for home maintenance per month?", "Take 1% of home value plus $5 per square foot, average the two, divide by 12 — for a typical $400,000, 1,900 sq ft home that's around $280-320/month, more for older homes or harsh climates. The exact number matters less than the mechanism: an automatic monthly transfer to a dedicated account, so the eventual roof year is pre-funded."),
            ("Is the 1% rule realistic with today's prices?", "As a long-run average, yes for most markets — but it understates costs for older homes (closer to 2%) and overstates them where land dominates the price (use the per-square-foot blend instead). Labor inflation has pushed component costs up, which is why this calculator blends $5/sq ft rather than the older $2-3 figures still quoted around the internet."),
            ("Should maintenance money come out of my emergency fund?", "No — keep them separate. The emergency fund covers income shocks (job loss, medical); maintenance is a predictable cost that merely arrives irregularly, which is exactly what a sinking fund handles. Mixing them means a roof replacement leaves you exposed to a layoff the same year — the two risks you least want stacked."),
            ("What are the most expensive things that will need replacing?", "The big five: roof ($8,000-20,000, ~20-25 years), HVAC ($7,000-14,000, ~15-20 years), windows as a set ($10,000-25,000, ~25-35 years), siding/exterior ($8,000-20,000, ~25-40 years), and water/sewer line surprises ($3,000-15,000, no schedule). A pre-purchase inspection that ages each of these is effectively a discount negotiation checklist — a roof with 3 years left is a $10,000 price conversation."),
            ("Do condos need a maintenance budget too?", "A smaller personal one (interior systems, appliances, in-unit HVAC — often $50-150/month) — but the building's share arrives as HOA dues and, when reserves are thin, special assessments that can hit five figures. Before buying, read the reserve study: a well-funded HOA is prepaid maintenance; an underfunded one is a deferred bill with your name partially on it."),
        ],
    },
]
