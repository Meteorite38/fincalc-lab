# -*- coding: utf-8 -*-
"""Batch 5 calculators: APY, real return, retirement withdrawal, student loan,
fuel, unit price, car lease, annuity payout."""

PART7 = [
    {
        "slug": "apy-calculator",
        "emoji": "\U0001F501",
        "category": "Savings & Investing",
        "title": "APY Calculator — Convert APR to Effective Annual Yield",
        "h1": "APY Calculator",
        "blurb": "Turn a nominal rate + compounding into true APY.",
        "meta_description": "Convert a nominal interest rate (APR) and compounding frequency into the effective annual yield (APY) so you can compare savings accounts fairly.",
        "intro": "Two accounts with the same nominal rate can pay different amounts depending on how often they compound. Enter a rate and compounding frequency to get the true effective annual yield (APY).",
        "fields": [
            {"id": "rate", "label": "Nominal annual rate / APR (%)", "value": 5, "step": 0.01},
            {"id": "freq", "label": "Compounding frequency", "value": "12", "type": "select",
             "options": [["1", "Annually"], ["2", "Semiannually"], ["4", "Quarterly"], ["12", "Monthly"], ["365", "Daily"]]},
            {"id": "amount", "label": "Deposit amount ($, optional)", "value": 10000},
        ],
        "js": """
function calculate() {
  const r = val('rate')/100, n = parseFloat(document.getElementById('freq').value), a = val('amount');
  const apy = Math.pow(1 + r/n, n) - 1;
  const gap = apy*100 - r*100;
  let rows = `<tr><td>Nominal rate (APR)</td><td>${fmt(r*100,2)}%</td></tr>
    <tr><td>Effective yield (APY)</td><td>${fmt(apy*100,2)}%</td></tr>
    <tr><td>Compounding boost</td><td>+${fmt(gap,2)}%</td></tr>`;
  if (a > 0) rows += `<tr><td>One year's interest on $${fmt(a,0)}</td><td>$${fmt(a*apy)}</td></tr>`;
  show(`<div class="result-main">${fmt(apy*100,2)}%<small>True APY at ${document.getElementById('freq').options[document.getElementById('freq').selectedIndex].text.toLowerCase()} compounding</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>APR vs APY in one line</h2>
<p>APR is the stated ("nominal") yearly rate; APY is what you actually earn once compounding is included. Because interest earns interest between compounding dates, <strong>APY is always equal to or higher than APR</strong> — and the more frequently it compounds, the bigger the gap. The formula: <code>APY = (1 + APR/n)<sup>n</sup> − 1</code>, where <em>n</em> is the number of compounding periods per year.</p>
<h2>Why frequency matters</h2>
<p>A 5% nominal rate becomes 5.00% APY compounded annually, 5.09% quarterly, 5.12% monthly, and 5.13% daily. The differences look tiny, but they're free money — and over large balances or many years they add up. Crucially, this is why you should <strong>compare savings accounts by APY, not the headline rate</strong>: a slightly lower nominal rate that compounds daily can beat a higher one that compounds annually.</p>
<h2>The marketing angle</h2>
<p>Banks advertise <strong>APY</strong> on savings because it's the larger, more attractive number. Lenders advertise <strong>APR</strong> on debt because it's the smaller one — so your credit card's real cost (its APY) is higher than the rate on the statement. Knowing how to convert between them means neither side's marketing can mislead you. See our <a href="/articles/apr-vs-apy-explained/">full APR vs APY guide</a> for the deeper explanation.</p>
""",
        "faqs": [
            ("Is APY always higher than APR?", "Yes, unless interest compounds exactly once a year, in which case they're equal. Any more frequent compounding makes APY larger, because interest starts earning interest sooner."),
            ("Which should I use to compare savings accounts?", "APY. It reflects real earnings including compounding, so it's the only fair basis for comparison. Two accounts with the same nominal rate but different compounding frequencies have different APYs."),
            ("Does more frequent compounding make a big difference?", "The jump from annual to daily compounding is modest at normal rates (a fraction of a percent), but it's still free money, and it grows with larger balances, higher rates, and longer time horizons."),
        ],
    },
    {
        "slug": "real-return-calculator",
        "emoji": "\U0001F4C9",
        "category": "Savings & Investing",
        "title": "Real Return Calculator — Investment Return After Inflation",
        "h1": "Real Rate of Return Calculator",
        "blurb": "What your return is really worth after inflation.",
        "meta_description": "Calculate your real (inflation-adjusted) rate of return from a nominal return and inflation rate — the number that reflects true growth in purchasing power.",
        "intro": "Earning 7% means little if inflation is 5%. The real return strips out inflation to show how much your purchasing power actually grew. Enter your nominal return and the inflation rate.",
        "fields": [
            {"id": "nominal", "label": "Nominal return (%)", "value": 7, "step": 0.1},
            {"id": "inflation", "label": "Inflation rate (%)", "value": 3, "step": 0.1},
            {"id": "amount", "label": "Amount invested ($, optional)", "value": 10000},
            {"id": "years", "label": "Years (optional)", "value": 20, "step": 1},
        ],
        "js": """
function calculate() {
  const nom = val('nominal')/100, inf = val('inflation')/100, a = val('amount'), y = val('years');
  const real = (1 + nom)/(1 + inf) - 1;
  const approx = nom - inf;
  let rows = `<tr><td>Real return (exact)</td><td>${fmt(real*100,2)}%</td></tr>
    <tr><td>Quick estimate (nominal − inflation)</td><td>${fmt(approx*100,2)}%</td></tr>`;
  if (a > 0 && y > 0) {
    const nominalFV = a*Math.pow(1+nom,y), realFV = a*Math.pow(1+real,y);
    rows += `<tr><td>Nominal value in ${y} yrs</td><td>$${fmt(nominalFV,0)}</td></tr>
    <tr><td>Value in today's money</td><td>$${fmt(realFV,0)}</td></tr>`;
  }
  show(`<div class="result-main">${fmt(real*100,2)}%<small>Real return after ${fmt(inf*100,1)}% inflation</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>Nominal vs real return</h2>
<p>Your <strong>nominal return</strong> is the headline number your investment earns. Your <strong>real return</strong> subtracts inflation to reveal the growth in actual buying power. The precise formula isn't simple subtraction — it's <code>(1 + nominal) ÷ (1 + inflation) − 1</code> — though "nominal minus inflation" is a close-enough estimate at low rates. A 7% return with 3% inflation is a real return of about 3.9%, not exactly 4%.</p>
<h2>Why it changes the whole picture</h2>
<p>Real return is the honest measure of whether you're getting richer. Consider the trap of "safe" cash: a savings account paying 2% while inflation runs 4% has a <strong>negative real return</strong> of about −1.9% — your money grows on paper but buys less each year. Feeling safe while quietly losing purchasing power is one of the most common financial mistakes.</p>
<h2>Planning in real terms</h2>
<ul>
<li><strong>Retirement:</strong> a projected $1 million decades away is worth far less in today's money. Planning with a real return (say 4–5% instead of 7%) gives targets in purchasing power you can actually understand.</li>
<li><strong>Historical context:</strong> long-run stock real returns have averaged roughly 6–7%; bonds much lower; cash near zero or negative. These real figures, not nominal ones, are what compound your standard of living.</li>
<li><strong>Debt cuts both ways:</strong> inflation quietly erodes the real value of fixed-rate debt, which is why a low fixed-rate mortgage feels cheaper over time.</li>
</ul>
<p>Whenever someone quotes a return, mentally subtract inflation. The difference between nominal and real is the difference between looking richer and being richer.</p>
""",
        "faqs": [
            ("What is a real rate of return?", "Your investment return after adjusting for inflation — the growth in actual purchasing power. It's calculated as (1 + nominal) ÷ (1 + inflation) − 1, roughly nominal minus inflation."),
            ("Can real return be negative?", "Yes. If inflation exceeds your nominal return — common for cash in high-inflation periods — your real return is negative and your money loses purchasing power despite growing in dollar terms."),
            ("Why not just subtract inflation from my return?", "Simple subtraction is a good approximation at low rates but slightly overstates the real return. The exact formula divides by (1 + inflation), which matters more when rates are high."),
        ],
    },
    {
        "slug": "retirement-withdrawal-calculator",
        "emoji": "\U0001F3D6\uFE0F",
        "category": "Retirement",
        "title": "Retirement Withdrawal Calculator — How Long Will Savings Last?",
        "h1": "Retirement Withdrawal Calculator",
        "blurb": "How long a nest egg lasts at a given withdrawal.",
        "meta_description": "See how long your retirement savings will last based on your balance, monthly withdrawals and expected return — and what the 4% rule implies for your nest egg.",
        "intro": "Will your savings outlast your retirement? Enter your nest egg, the monthly income you want to draw, and an expected return to see how many years the money lasts.",
        "fields": [
            {"id": "balance", "label": "Retirement savings ($)", "value": 1000000},
            {"id": "withdrawal", "label": "Monthly withdrawal ($)", "value": 4000},
            {"id": "rate", "label": "Expected annual return (%)", "value": 5, "step": 0.1},
        ],
        "js": """
function calculate() {
  let bal = val('balance'); const w = val('withdrawal'), i = val('rate')/100/12;
  const startBal = bal;
  let months = 0;
  while (bal > 0 && months < 1200) { bal = bal*(1+i) - w; months++; }
  const rule4 = startBal * 0.04 / 12;
  if (months >= 1200) {
    show(`<div class="result-main">Essentially forever<small>At $${fmt(w,0)}/mo and ${fmt(i*1200,1)}% return, growth outpaces withdrawals</small></div>
    <table><tr><td>4% rule monthly income</td><td>$${fmt(rule4,0)}</td></tr>
    <tr><td>Your withdrawal vs 4% rule</td><td>${fmt(w/rule4*100,0)}%</td></tr></table>`);
    return;
  }
  const yrs = Math.floor(months/12), mo = months%12;
  show(`<div class="result-main">${yrs} years ${mo} months<small>Until $${fmt(startBal,0)} runs out at $${fmt(w,0)}/month</small></div>
  <table>
    <tr><td>Annual withdrawal</td><td>$${fmt(w*12,0)} (${fmt(w*12/startBal*100,1)}% of balance)</td></tr>
    <tr><td>4% rule "safe" monthly income</td><td>$${fmt(rule4,0)}</td></tr>
    <tr><td>Your rate vs 4% rule</td><td>${fmt(w/rule4*100,0)}% of it</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The retirement math that keeps people up at night</h2>
<p>The saving phase asks "how big a nest egg can I build?" The spending phase asks the scarier question: "will it last?" This calculator simulates your balance month by month — growing with returns, shrinking with withdrawals — until it either runs dry or clearly outlasts any reasonable retirement.</p>
<h2>The 4% rule</h2>
<p>The famous guideline from the Trinity study suggests that withdrawing about <strong>4% of your starting balance per year</strong> (then adjusting for inflation) has historically lasted through a 30-year retirement. On $1 million that's $40,000/year, about $3,333/month. Withdraw much more and you risk running out; withdraw less and you'll likely die with a large balance. The calculator shows how your chosen withdrawal compares to this benchmark.</p>
<h2>The variables that make or break it</h2>
<ul>
<li><strong>Withdrawal rate is king.</strong> The gap between a 4% and a 6% withdrawal is the difference between "lasts forever" and "gone in ~20 years."</li>
<li><strong>Sequence-of-returns risk:</strong> a market crash <em>early</em> in retirement is far more dangerous than the same crash later, because you're selling assets while they're down. Average returns hide this danger — real retirees should keep a cash buffer to avoid selling into downturns.</li>
<li><strong>Inflation:</strong> this tool uses a flat withdrawal; in reality your spending needs rise with inflation, which shortens how long the money lasts. Using a lower "real" return (say 4–5%) partly accounts for this.</li>
</ul>
<h2>Flexibility is the safety net</h2>
<p>The 4% rule assumes rigid spending. Retirees who can trim withdrawals in bad market years — skipping the inflation raise, or cutting discretionary spending — dramatically improve the odds their money lasts. Treat the result here as a planning guide, not a guarantee, and build in the flexibility to spend less when markets demand it.</p>
""",
        "faqs": [
            ("What is the 4% rule?", "A guideline suggesting you can withdraw 4% of your starting retirement balance in year one, then adjust for inflation, with a high chance the money lasts 30 years. It's a starting point, not a guarantee."),
            ("What is sequence-of-returns risk?", "The danger that poor market returns early in retirement deplete your savings faster, because you're withdrawing while asset values are low. The same returns in a different order can produce very different outcomes."),
            ("Should I withdraw a fixed amount or a percentage?", "Fixed withdrawals are predictable but riskier in downturns. Percentage-based or flexible withdrawals (cutting back in bad years) adapt to markets and make savings last longer, at the cost of variable income."),
        ],
    },
    {
        "slug": "student-loan-calculator",
        "emoji": "\U0001F393",
        "category": "Loans & Debt",
        "title": "Student Loan Calculator — Payment, Payoff and Interest",
        "h1": "Student Loan Calculator",
        "blurb": "Monthly payment and total interest on student debt.",
        "meta_description": "Calculate your student loan monthly payment, total interest, and how much faster you finish by paying extra each month.",
        "intro": "See what your student loans really cost. Enter your balance, interest rate and repayment term for the monthly payment and total interest — then try an extra payment to see how much sooner you're free.",
        "fields": [
            {"id": "balance", "label": "Total loan balance ($)", "value": 30000},
            {"id": "rate", "label": "Interest rate (%)", "value": 6, "step": 0.1},
            {"id": "years", "label": "Repayment term (years)", "value": 10, "step": 1},
            {"id": "extra", "label": "Extra monthly payment ($)", "value": 0},
        ],
        "js": """
function payoff(P, i, pmt) {
  if (pmt <= P*i) return null;
  let bal = P, months = 0, interest = 0;
  while (bal > 0 && months < 1200) { const int = bal*i; interest += int; bal = bal + int - pmt; months++; }
  return { months, interest };
}
function calculate() {
  const P = val('balance'), i = val('rate')/100/12, y = val('years'), extra = val('extra');
  const n = y*12;
  const base = i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n;
  const totalInterest = base*n - P;
  let rows = `<tr><td>Monthly payment</td><td>$${fmt(base)}</td></tr>
    <tr><td>Total interest</td><td>$${fmt(totalInterest)}</td></tr>
    <tr><td>Total repaid</td><td>$${fmt(base*n)}</td></tr>`;
  if (extra > 0) {
    const fast = payoff(P, i, base + extra);
    if (fast) {
      const yrs = Math.floor(fast.months/12), mo = fast.months%12;
      rows += `<tr><td>With +$${fmt(extra,0)}/mo</td><td>${yrs}y ${mo}m, save $${fmt(totalInterest - fast.interest)}</td></tr>`;
    }
  }
  show(`<div class="result-main">$${fmt(base)} / month<small>for ${y} years at ${fmt(i*1200,1)}%</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>What drives the cost</h2>
<p>Student loans amortize like any other fixed loan: a level monthly payment split between interest and principal. Two levers dominate the total cost — the <strong>interest rate</strong> and the <strong>term</strong>. A $30,000 loan at 6% over 10 years costs about $9,967 in interest; stretch it to 20 years and the payment drops but total interest more than doubles. Longer terms ease monthly cash flow at a steep long-run price.</p>
<h2>The power of extra payments</h2>
<p>Because interest accrues on the balance, every extra dollar toward principal removes all the future interest that dollar would have generated. Try the extra-payment field: even a modest additional amount can cut months off the loan and save meaningful interest. Ask your servicer to apply extra payments to <em>principal</em>, not toward future installments, or the benefit is lost.</p>
<h2>Fixed vs variable, and repayment plans</h2>
<ul>
<li><strong>Fixed-rate</strong> loans (this calculator's model) keep the same payment for the life of the loan — predictable and safest.</li>
<li><strong>Income-driven plans</strong> (common for government loans) cap payments at a share of income and may forgive remaining balances after many years, but often increase total interest paid.</li>
<li><strong>Refinancing</strong> can lower a high rate, but refinancing federal loans into private ones usually forfeits protections like income-driven plans and forgiveness — weigh carefully.</li>
</ul>
<h2>Where student debt fits in your plan</h2>
<p>Low-rate student loans (say under 5%) are often worth paying on schedule while you invest and build an emergency fund. Higher-rate loans deserve more aggressive payoff. Whatever the rate, always capture any employer retirement match first — a 50–100% instant return beats prepaying almost any loan.</p>
""",
        "faqs": [
            ("Should I pay off student loans early or invest?", "Compare the loan rate to your expected after-tax investment return. High-rate loans (roughly 6%+) usually favor faster payoff; low-rate loans can be paid on schedule while you invest. Always take a full employer match first."),
            ("Do extra payments really help?", "Yes — extra amounts applied to principal remove future interest and shorten the loan. Confirm your servicer applies them to principal rather than crediting future payments."),
            ("Should I refinance federal student loans?", "Refinancing can lower your rate, but moving federal loans to a private lender gives up protections like income-driven repayment and potential forgiveness. Only refinance federal loans if you're confident you won't need those benefits."),
        ],
    },
    {
        "slug": "fuel-cost-calculator",
        "emoji": "\u26FD",
        "category": "Everyday Math",
        "title": "Fuel Cost Calculator — Trip and Annual Driving Cost",
        "h1": "Fuel Cost Calculator",
        "blurb": "Cost of a trip, and yearly fuel spend.",
        "meta_description": "Calculate the fuel cost of a trip from distance, fuel efficiency and fuel price, plus your estimated annual fuel spend. Works with MPG or L/100km.",
        "intro": "Estimate what a drive costs in fuel — handy for road trips, commutes, or comparing cars. Enter the distance, your vehicle's efficiency, and the fuel price.",
        "fields": [
            {"id": "distance", "label": "Trip distance", "value": 300},
            {"id": "efficiency", "label": "Fuel efficiency (miles per gallon)", "value": 30, "step": 0.1, "hint": "or km per unit — keep units consistent"},
            {"id": "price", "label": "Fuel price (per gallon)", "value": 3.5, "step": 0.01},
            {"id": "annual", "label": "Annual distance driven (optional)", "value": 12000, "step": 100},
        ],
        "js": """
function calculate() {
  const d = val('distance'), e = val('efficiency'), p = val('price'), yr = val('annual');
  if (e <= 0) { show('<div class="result-main">Fuel efficiency must be above zero.</div>'); return; }
  const fuelUsed = d / e, cost = fuelUsed * p;
  let rows = `<tr><td>Fuel used</td><td>${fmt(fuelUsed,2)} gallons</td></tr>
    <tr><td>Cost per mile</td><td>$${fmt(p/e,3)}</td></tr>`;
  if (yr > 0) rows += `<tr><td>Estimated annual fuel cost</td><td>$${fmt(yr/e*p,0)}</td></tr>
    <tr><td>Per month</td><td>$${fmt(yr/e*p/12,0)}</td></tr>`;
  show(`<div class="result-main">$${fmt(cost)}<small>Fuel cost for a ${fmt(d,0)}-mile trip</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>The simple formula</h2>
<p>Fuel cost = (distance ÷ efficiency) × price per unit. Divide the trip distance by your miles-per-gallon (or km per litre) to get fuel used, then multiply by the price. A 300-mile trip in a 30-MPG car at $3.50/gallon uses 10 gallons and costs $35. Keep your units consistent — miles with MPG and price per gallon, or kilometres with your local equivalents.</p>
<h2>Cost per mile: the number that compares cars</h2>
<p>Dividing price by efficiency gives cost per mile — a clean way to compare vehicles or plan budgets. At $3.50/gallon, a 30-MPG car costs about 12¢/mile in fuel; a 20-MPG SUV costs 17.5¢; a 45-MPG hybrid just 7.8¢. Over 12,000 miles a year, that spread is hundreds of dollars — and it compounds over the years you own the vehicle.</p>
<h2>Beyond the pump price</h2>
<ul>
<li><strong>Fuel is only part of driving cost.</strong> Insurance, maintenance, tyres, and depreciation often exceed fuel — factor them in when comparing cars or commutes.</li>
<li><strong>Efficiency varies with conditions.</strong> Highway driving, gentle acceleration, and proper tyre pressure improve real-world MPG; city stop-and-go and heavy loads worsen it.</li>
<li><strong>Commute math:</strong> a longer commute to a cheaper home has a real, recurring fuel (and time) cost worth putting a number on before you decide.</li>
</ul>
<p>For electric vehicles the same logic applies with cost per kWh and miles per kWh — the per-mile figure is usually much lower, which is a core part of the EV value case alongside their higher purchase price.</p>
""",
        "faqs": [
            ("How do I calculate fuel cost for a trip?", "Divide the distance by your vehicle's fuel efficiency to get fuel used, then multiply by the fuel price. For example, 300 miles ÷ 30 MPG = 10 gallons × $3.50 = $35."),
            ("Can I use this with litres and kilometres?", "Yes — just keep units consistent. Enter distance in km, efficiency in km per litre, and price per litre. The math works identically; only the labels differ."),
            ("Does fuel cost include all driving costs?", "No. Fuel is only one part. Insurance, maintenance, tyres, and depreciation frequently cost more than fuel, so include them when comparing vehicles or commutes."),
        ],
    },
    {
        "slug": "unit-price-calculator",
        "emoji": "\U0001F6D2",
        "category": "Everyday Math",
        "title": "Unit Price Calculator — Compare Which Package Is Cheaper",
        "h1": "Unit Price Calculator",
        "blurb": "Find the real cost per unit and the better deal.",
        "meta_description": "Compare two package sizes by cost per unit to find the genuinely cheaper option. Stop being fooled by bigger packages that cost more per unit.",
        "intro": "Bigger isn't always cheaper. Enter the price and size of two options to see the cost per unit for each — and which one is actually the better deal.",
        "fields": [
            {"id": "price1", "label": "Option A price ($)", "value": 4.50},
            {"id": "size1", "label": "Option A size (units)", "value": 500},
            {"id": "price2", "label": "Option B price ($)", "value": 7.20},
            {"id": "size2", "label": "Option B size (units)", "value": 900},
        ],
        "js": """
function calculate() {
  const p1 = val('price1'), s1 = val('size1'), p2 = val('price2'), s2 = val('size2');
  if (s1 <= 0 || s2 <= 0) { show('<div class="result-main">Sizes must be above zero.</div>'); return; }
  const u1 = p1/s1, u2 = p2/s2;
  const cheaper = u1 < u2 ? 'A' : (u2 < u1 ? 'B' : 'Tie');
  const save = Math.abs(u1 - u2) / Math.max(u1, u2) * 100;
  show(`<div class="result-main">Option ${cheaper}${cheaper !== 'Tie' ? ' is cheaper' : ''}<small>${cheaper !== 'Tie' ? fmt(save,1) + '% less per unit' : 'Both cost the same per unit'}</small></div>
  <table>
    <tr><td>Option A cost per unit</td><td>$${fmt(u1,4)}</td></tr>
    <tr><td>Option B cost per unit</td><td>$${fmt(u2,4)}</td></tr>
    <tr><td>Better value</td><td>Option ${cheaper}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why unit price beats sticker price</h2>
<p>The only fair way to compare two package sizes is <strong>cost per unit</strong> — price divided by size. Stores rely on shoppers assuming the bigger pack is always cheaper per unit, but that's frequently false. "Bulk" and "family size" packages sometimes cost <em>more</em> per unit than the standard size, betting you won't do the division. This calculator does it for you.</p>
<h2>The bigger-package trap</h2>
<p>Consider 500 units for $4.50 (0.9¢ each) versus 900 units for $7.20 (0.8¢ each) — here the larger pack genuinely wins. But swap in 900 units for $8.50 and the small pack is cheaper per unit despite looking like worse value. Always compare the per-unit figure, not the total price or the vague sense that "more must be better."</p>
<h2>Smart-shopping caveats</h2>
<ul>
<li><strong>Waste kills bulk savings.</strong> A cheaper-per-unit giant package is no bargain if half spoils or goes unused. Cost per unit <em>you actually use</em> is the real metric.</li>
<li><strong>Check the store's shelf label,</strong> which often shows unit price — but verify it, as units (per 100g vs per item) can differ between products and mislead.</li>
<li><strong>Loyalty and sales</strong> can flip the answer temporarily; a smaller pack on sale may beat the usual bulk winner.</li>
</ul>
<p>Two seconds of division at the shelf, repeated across a lifetime of grocery trips, quietly adds up to real money — and immunizes you against packaging that's designed to look like a deal.</p>
""",
        "faqs": [
            ("How do I compare prices of different sizes?", "Divide each item's price by its size to get cost per unit, then compare those figures. The lower cost per unit is the better value regardless of which package is bigger or has the lower sticker price."),
            ("Is the bigger package always cheaper per unit?", "No. Larger 'bulk' or 'family' sizes sometimes cost more per unit than standard sizes. Always calculate cost per unit rather than assuming bigger means cheaper."),
            ("What if the units are different (grams vs count)?", "Convert to the same unit before comparing, or compare only like-for-like. Store shelf labels sometimes use different bases (per 100g vs per item), which can make comparisons misleading."),
        ],
    },
    {
        "slug": "car-lease-calculator",
        "emoji": "\U0001F5DD\uFE0F",
        "category": "Loans & Debt",
        "title": "Car Lease Calculator — Estimate Your Monthly Lease Payment",
        "h1": "Car Lease Calculator",
        "blurb": "Estimate a monthly lease payment from the key terms.",
        "meta_description": "Estimate a car lease monthly payment from vehicle price, residual value, lease term and money factor — and understand what you're really paying for.",
        "intro": "Leasing pays for a car's depreciation plus finance charges, not the whole car. Enter the price, expected residual value, term and money factor for an estimated monthly payment.",
        "fields": [
            {"id": "price", "label": "Negotiated vehicle price ($)", "value": 35000},
            {"id": "down", "label": "Down payment / incentives ($)", "value": 2000},
            {"id": "residual", "label": "Residual value at lease end ($)", "value": 21000, "hint": "what it's worth when returned"},
            {"id": "months", "label": "Lease term (months)", "value": 36, "step": 1},
            {"id": "mf", "label": "Money factor", "value": 0.0025, "step": 0.0001, "hint": "APR ÷ 2400; 0.0025 ≈ 6% APR"},
        ],
        "js": """
function calculate() {
  const price = val('price'), down = val('down'), residual = val('residual'), n = val('months'), mf = val('mf');
  const cap = price - down;
  const depreciation = (cap - residual) / n;
  const financeCharge = (cap + residual) * mf;
  const payment = depreciation + financeCharge;
  const apr = mf * 2400;
  if (payment < 0) { show('<div class="result-main">Check inputs — residual exceeds the financed amount.</div>'); return; }
  show(`<div class="result-main">$${fmt(payment)} / month<small>Estimated lease payment (before tax) for ${n} months</small></div>
  <table>
    <tr><td>Depreciation portion</td><td>$${fmt(depreciation)}/mo</td></tr>
    <tr><td>Finance charge (≈${fmt(apr,1)}% APR)</td><td>$${fmt(financeCharge)}/mo</td></tr>
    <tr><td>Total of payments</td><td>$${fmt(payment*n,0)}</td></tr>
    <tr><td>Total cost incl. down payment</td><td>$${fmt(payment*n + down,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What a lease actually pays for</h2>
<p>When you lease, you don't pay for the whole car — only its <strong>depreciation</strong> during your term (the value it loses) plus a <strong>finance charge</strong>. That's why lease payments are lower than loan payments on the same car: you're financing perhaps $14,000 of value lost, not the full $35,000. At lease end you return the car (worth its "residual value") and walk away, or buy it for that residual.</p>
<h2>Decoding the money factor</h2>
<p>The <strong>money factor</strong> is the lease's interest rate in disguise. Convert it to a familiar APR by multiplying by 2,400: a 0.0025 money factor is roughly 6% APR. Dealers sometimes quote the money factor hoping you won't translate it — always convert and compare it to normal loan rates. A high money factor is expensive interest wearing an unfamiliar costume.</p>
<h2>The residual value lever</h2>
<p>A higher residual means the car keeps more value, so you pay for less depreciation and your payment drops. Cars that hold value well (strong resale reputations) often lease more cheaply than their price suggests, while fast-depreciating models lease expensively. The residual is set by the leasing company, not negotiable — but it explains why two similarly-priced cars can have very different lease payments.</p>
<h2>Lease vs buy, briefly</h2>
<ul>
<li><strong>Leasing</strong> means lower payments, a new car every few years, and warranty coverage — but perpetual payments and no ownership, plus mileage limits and wear charges.</li>
<li><strong>Buying</strong> costs more monthly but ends in an owned asset and payment-free years, usually the cheaper path if you keep cars a long time.</li>
</ul>
<p>This is an estimate; real leases add taxes, fees, and mileage terms. But knowing the depreciation and finance components — and converting that money factor to an APR — puts you far ahead of the average lessee at the dealership.</p>
""",
        "faqs": [
            ("What is a money factor?", "The lease's interest rate expressed as a small decimal. Multiply it by 2,400 to get the approximate APR — a 0.0025 money factor is about 6%. Always convert it to compare against normal loan rates."),
            ("Why are lease payments lower than loan payments?", "Because a lease only finances the car's depreciation during your term plus finance charges, not its full price. You're paying for the value used, not the whole vehicle."),
            ("Is leasing cheaper than buying?", "Leasing usually has lower monthly payments but never ends in ownership, so over many years buying and keeping a car is typically cheaper. Leasing suits those who want a new car every few years and predictable costs."),
        ],
    },
    {
        "slug": "annuity-payout-calculator",
        "emoji": "\U0001F4B5",
        "category": "Retirement",
        "title": "Annuity Payout Calculator — Monthly Income from a Lump Sum",
        "h1": "Annuity Payout Calculator",
        "blurb": "Monthly income a lump sum can pay over a period.",
        "meta_description": "Calculate the monthly income a lump sum can provide over a set number of years at a given return — the payout phase of an annuity or drawdown.",
        "intro": "How much guaranteed monthly income can a lump sum produce? Enter the amount, an expected return, and how many years you want it to last for the level monthly payout.",
        "fields": [
            {"id": "principal", "label": "Lump sum ($)", "value": 500000},
            {"id": "rate", "label": "Expected annual return (%)", "value": 4, "step": 0.1},
            {"id": "years", "label": "Payout period (years)", "value": 25, "step": 1},
        ],
        "js": """
function calculate() {
  const P = val('principal'), i = val('rate')/100/12, n = val('years')*12;
  const pmt = i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n;
  const total = pmt*n;
  show(`<div class="result-main">$${fmt(pmt)} / month<small>for ${val('years')} years from $${fmt(P,0)}</small></div>
  <table>
    <tr><td>Total paid out</td><td>$${fmt(total,0)}</td></tr>
    <tr><td>Of which is growth</td><td>$${fmt(total-P,0)}</td></tr>
    <tr><td>Annual income</td><td>$${fmt(pmt*12,0)}</td></tr>
    <tr><td>As % of lump sum / year</td><td>${fmt(pmt*12/P*100,1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Turning savings into income</h2>
<p>Building a nest egg is half the journey; the other half is converting it into a reliable income. This calculator finds the level monthly payment a lump sum can sustain over a fixed period while the remaining balance keeps earning a return — the same math behind fixed-period annuities and structured drawdowns. Notice the "of which is growth" line: because the unpaid balance keeps working, the total paid out exceeds the original lump sum.</p>
<h2>The trade-off: certainty vs flexibility</h2>
<p>A <strong>fixed-period payout</strong> gives a predictable income but ends when the term does — you must outlive it carefully or pair it with other income. A <strong>lifetime annuity</strong> (bought from an insurer) instead pays until you die, transferring longevity risk to the insurer, but you give up the lump sum and control. Self-managed drawdown (keeping the money invested and withdrawing flexibly) offers the most control and upside but no guarantee it lasts — the risk explored in our <a href="/calculators/retirement-withdrawal-calculator/">retirement withdrawal calculator</a>.</p>
<h2>What the return assumption does</h2>
<ul>
<li><strong>Higher assumed return → higher payout,</strong> but also more risk that reality falls short. Conservative retirees use lower rates (3–4%) for safety.</li>
<li><strong>Inflation isn't included</strong> in a level payout — $2,600/month feels smaller each year as prices rise. Consider whether you need rising income, which lowers the starting figure.</li>
<li><strong>Taxes</strong> apply to most retirement income; the figures here are pre-tax.</li>
</ul>
<h2>Using the number</h2>
<p>This is a planning estimate, not a product quote. Real annuities carry fees and specific terms, and self-managed drawdown returns vary year to year. But seeing that, say, $500,000 at 4% supports roughly $2,600/month for 25 years turns an abstract nest-egg target into a concrete lifestyle question — and helps you judge whether your savings goal actually matches the retirement you want.</p>
""",
        "faqs": [
            ("How much monthly income will my savings provide?", "It depends on the amount, the return earned, and how long it must last. This calculator computes the level monthly payment that draws a lump sum down to zero over your chosen period while the balance keeps earning."),
            ("Is this the same as buying an annuity?", "The math mirrors a fixed-period annuity's payout, but a real insurance annuity includes fees, guarantees, and sometimes lifetime payments. Use this as a planning estimate, not a product quote."),
            ("Does the payout account for inflation?", "No — it's a level (fixed) monthly amount, which loses purchasing power over time. If you want income that rises with inflation, the starting payment would be lower. Use a conservative real return to approximate this."),
        ],
    },
]
