# -*- coding: utf-8 -*-
"""Property tax calculator — effective-rate estimate with state presets, assessment vs market value, escrow monthly view."""

PROPTAX = [
    {
        "slug": "property-tax-calculator",
        "emoji": "\U0001F3E0",
        "category": "Mortgages & Home",
        "title": "Property Tax Calculator — Annual Bill, Monthly Escrow, and Your Effective Rate",
        "h1": "Property Tax Calculator",
        "blurb": "Annual bill and monthly escrow from home value and state — or your exact local rate.",
        "meta_description": "Free property tax calculator: estimate your annual property tax and monthly escrow from home value and state-level effective rates (NJ 2.2% to HI 0.3%), or enter your exact local millage. Includes assessment-ratio and homestead-exemption math.",
        "intro": "Property tax is the housing cost that never amortizes away — and the gap between states is enormous: the same $400,000 house owes about $1,300 a year in Hawaii and $9,000+ in New Jersey. This calculator estimates your bill from state-level effective rates or your exact local rate, and shows what it adds to the monthly payment.",
        "fields": [
            {"id": "value", "label": "Home market value ($)", "value": 400000},
            {"id": "state", "label": "State (median effective rate)", "type": "select", "value": "1.0",
             "options": [
                 ("0.29", "Hawaii — 0.29%"), ("0.41", "Alabama — 0.41%"), ("0.51", "Colorado / Nevada — ~0.5%"),
                 ("0.57", "Arizona / Utah — ~0.57%"), ("0.7", "California / Idaho — ~0.7%"),
                 ("0.8", "Virginia / NC / Georgia — ~0.8%"), ("0.9", "Florida / Washington / Oregon — ~0.9%"),
                 ("1.0", "National median — ~1.0%"), ("1.2", "Minnesota / Massachusetts — ~1.2%"),
                 ("1.4", "Michigan / Kansas / Ohio — ~1.4%"), ("1.6", "Pennsylvania / Iowa — ~1.6%"),
                 ("1.7", "Texas / Nebraska — ~1.7%"), ("1.9", "New York (upstate) / Wisconsin — ~1.9%"),
                 ("2.1", "Connecticut / New Hampshire — ~2.1%"), ("2.23", "New Jersey / Illinois — ~2.2%"),
             ]},
            {"id": "customrate", "label": "OR your exact local rate (%, 0 = use state)", "value": 0, "step": 0.01, "hint": "county assessor's effective rate if you know it"},
            {"id": "exempt", "label": "Homestead/other exemption ($ off assessed value)", "value": 0, "hint": "many states knock $25k-100k off for primary residences"},
            {"id": "growth", "label": "Expected annual increase (%)", "value": 3, "step": 0.5, "hint": "assessments and levies drift up — 2-5%/yr typical"},
        ],
        "js": """
function calculate() {
  const V = val('value'), custom = Math.max(0, val('customrate'))/100;
  const stateRate = parseFloat(document.getElementById('state').value)/100;
  const ex = Math.max(0, val('exempt')), g = Math.max(0, val('growth'))/100;
  if (V <= 0) { show('<div class="result-main">Enter a home value.</div>'); return; }
  const rate = custom > 0 ? custom : stateRate;
  const taxable = Math.max(0, V - ex);
  const annual = taxable * rate;
  const monthly = annual / 12;
  const in10 = annual * Math.pow(1 + g, 10);
  let total10 = 0;
  for (let y = 0; y < 10; y++) total10 += annual * Math.pow(1 + g, y);
  const exSave = ex * rate;
  show(`<div class="result-main">$${fmt(annual,0)}/year<small>&asymp; $${fmt(monthly,0)}/month into escrow &middot; ${fmt(rate*100,2)}% effective rate on $${fmt(taxable,0)}${ex > 0 ? ' (after $' + fmt(ex,0) + ' exemption)' : ''}</small></div>
  <table>
    <tr><td>Annual property tax</td><td>$${fmt(annual,0)}</td></tr>
    <tr><td>Monthly (what escrow adds to the payment)</td><td>$${fmt(monthly,0)}</td></tr>
    ${ex > 0 ? `<tr><td>Exemption saves</td><td>$${fmt(exSave,0)}/yr</td></tr>` : ''}
    <tr><td>Bill in 10 years at ${fmt(g*100,1)}%/yr growth</td><td>$${fmt(in10,0)}</td></tr>
    <tr><td>Total paid over the next decade</td><td>$${fmt(total10,0)}</td></tr>
    <tr><td>As % of a $${fmt(V,0)} home, per decade</td><td>${fmt(total10/V*100,1)}%</td></tr>
  </table>
  <p>Over 30 years of ownership this line quietly rivals the house price itself — and unlike the mortgage, it never pays off. Budgeting a purchase? Stack this on the loan payment with the <a href="/calculators/mortgage-calculator/">mortgage calculator</a> and check the whole burden against income in the <a href="/calculators/home-affordability-calculator/">affordability calculator</a>.</p>`);
}
""",
        "body_html": """
<h2>How the bill is actually computed</h2>
<p>Local governments set property tax in two steps: the <strong>assessed value</strong> (the assessor's estimate of your home's worth, sometimes multiplied by an assessment ratio — many states assess at a fraction of market value) and the <strong>millage rate</strong> (dollars of tax per $1,000 of assessed value, stacked across county, city, school district and special districts). Because ratios and millages vary wildly, the only portable comparison number is the <strong>effective rate</strong>: annual tax &divide; market value. That's what this calculator uses — the state presets are median effective rates, and the custom field accepts your county's exact figure (your last tax bill &divide; a realistic market value gives it to you in one division).</p>
<h2>Why identical houses owe wildly different taxes</h2>
<ul>
<li><strong>State and locality dominate.</strong> New Jersey's median effective rate (~2.2%) is more than seven times Hawaii's (~0.29%). Within states, school-district lines can move the bill 50% across a street.</li>
<li><strong>Caps and ratchets:</strong> California's Prop 13 caps assessment growth at 2%/year until sale — long-time owners pay a fraction of their new neighbor's bill on an identical house. Florida, Texas, Michigan and others cap annual increases for primary residences (10%, 3%, inflation). The cap resets at purchase: <strong>budget on the post-sale reassessment, not the seller's current bill</strong> — the #1 new-buyer surprise in capped states.</li>
<li><strong>Homestead exemptions</strong> knock a chunk off assessed value for primary residences — Texas $100,000 (school portion), Florida up to $50,000, many states $25,000-plus, with bigger cuts for seniors, veterans and disabled owners. They usually require a one-time application; forgetting it donates hundreds a year.</li>
<li><strong>Low sticker, high tax</strong> (and vice versa) changes affordability rankings: Texas has no income tax but ~1.7% property tax — a $400,000 Austin house carries a $560/month tax line. California's 0.7% effective rate softens its price shock slightly. Total cost of ownership is the only honest comparison.</li>
</ul>
<h2>Escrow: why your \"fixed\" mortgage payment rises</h2>
<p>Most lenders collect property tax monthly into an <strong>escrow account</strong> and pay the county for you — so the tax lives inside your mortgage payment. When the levy or assessment rises, the servicer recalculates: your \"fixed-rate\" payment climbs, sometimes with a catch-up for last year's shortfall stacked on top. A 30-year fixed mortgage fixes <em>principal and interest</em> only; the tax-and-insurance layer floats forever. This is also the part of the payment that survives the mortgage — a paid-off $400,000 house at 1.5% still costs $500/month to hold, which matters enormously for <a href="/calculators/retirement-withdrawal-calculator/">retirement cash-flow planning</a>.</p>
<h2>Appealing your assessment (worth more than it sounds)</h2>
<p>Assessments are mass-produced estimates, and error rates are material — studies routinely find 30-60% of appeals win some reduction. The process: check the assessor's record for factual errors (square footage, bedroom count, lot size), pull 3-5 recent comparable sales below your assessed value, and file within the appeal window (often 30-60 days after the notice). No lawyer needed at typical home values; the hearing is usually informal. A successful 10% cut on a $9,000 bill saves $900 <em>every year</em> until the next reassessment. If your notice jumped after a hot market cooled, the odds are especially good.</p>
<h2>The deduction fine print</h2>
<p>Property tax is deductible federally only within the <strong>SALT cap</strong> — state and local taxes (income + property combined) capped at $10,000 per return for most filers, and only if you itemize past the standard deduction. Practical upshot: in high-tax states the cap is often exhausted by income tax alone, making property tax effectively non-deductible; run your actual bracket in the <a href="/calculators/tax-bracket-calculator/">tax bracket calculator</a> before crediting the deduction in a buy-vs-rent decision (<a href="/calculators/rent-vs-buy-calculator/">the calculator</a> lets you toggle it).</p>
""",
        "faqs": [
            ("How is property tax calculated on a new purchase?", "In most places the sale itself triggers reassessment at or near your purchase price. Take the price, multiply by the local effective rate (county assessor sites publish it; ~1.0% is the national median), minus any homestead exemption you qualify for. In capped states (CA, FL, TX, MI), ignore the seller's current bill — their cap dies with the sale and yours restarts from the new assessment."),
            ("Why did my mortgage payment go up if my rate is fixed?", "The escrow portion moved. Your servicer collects property tax and insurance monthly and pays them for you; when the county raises the levy (or your assessment) or the insurer raises premiums, the escrow math is redone — often with a shortfall catch-up from the prior year stacked on. The P&I core of a fixed loan never changes; the wrapper around it floats."),
            ("Is it worth appealing my property tax assessment?", "Often, yes — appeals succeed at surprisingly high rates because assessments are mass-generated. The strongest cases: factual errors in the property record, comparable sales below your assessed value, or an assessment that didn't fall after a market dip. An hour of comp-gathering for a shot at cutting $500-1,500/year — recurring until reassessment — is excellent hourly pay."),
            ("Which states have the lowest and highest property taxes?", "Lowest effective rates: Hawaii (~0.29%), Alabama (~0.41%), Colorado, Nevada, Utah, Arizona (0.5-0.6%). Highest: New Jersey and Illinois (~2.2%), Connecticut and New Hampshire (~2.1%), Texas (~1.7%). But dollar bills depend on home values too — Hawaii's low rate on high prices still out-bills Alabama — and low-property-tax states often tax income or sales harder. Compare total tax burden for your situation, not one line."),
            ("Do I still pay property tax after the mortgage is paid off?", "Yes — forever. The county bills you directly (annually or semi-annually) once escrow ends; many owners keep a sinking fund transferring the monthly equivalent to savings so the bill never surprises. Unpaid property tax accrues liens and can ultimately force a sale, which is why 'paid-off house' never means 'free house' — it means P&I-free, with tax and insurance as the permanent floor."),
        ],
    },
]
