# -*- coding: utf-8 -*-
"""Batch 8 calculators: home affordability (28/36), rental property cap rate & cash-on-cash."""

PART10 = [
    {
        "slug": "home-affordability-calculator",
        "emoji": "\U0001F3E1",
        "category": "Mortgages & Home",
        "title": "Home Affordability Calculator — How Much House Can You Afford?",
        "h1": "Home Affordability Calculator",
        "blurb": "Max home price from your income using the 28/36 rule.",
        "meta_description": "Find how much house you can afford based on your income, debts, down payment and rate — using the lender-standard 28/36 rule. See your maximum price and payment.",
        "intro": "Lenders decide what you can borrow using debt-to-income ratios. Enter your income, existing debts, down payment and rate to see a sensible maximum home price via the classic 28/36 rule.",
        "fields": [
            {"id": "income", "label": "Gross annual income ($)", "value": 90000},
            {"id": "debts", "label": "Existing monthly debt payments ($)", "value": 400, "hint": "cars, student loans, min. card payments"},
            {"id": "down", "label": "Down payment saved ($)", "value": 60000},
            {"id": "rate", "label": "Mortgage interest rate (%)", "value": 6.5, "step": 0.05},
            {"id": "years", "label": "Mortgage term (years)", "value": 30, "step": 1},
            {"id": "taxins", "label": "Est. monthly tax + insurance ($)", "value": 450, "hint": "property tax + home insurance"},
        ],
        "js": """
function maxLoan(payment, i, n) {
  if (payment <= 0) return 0;
  return i > 0 ? payment * (1 - Math.pow(1 + i, -n)) / i : payment * n;
}
function calculate() {
  const inc = val('income'), debts = val('debts'), down = val('down');
  const i = val('rate')/100/12, n = Math.min(Math.round(val('years')*12), 1200), extras = val('taxins');
  const monthlyIncome = inc / 12;
  // 28% front-end: housing (PITI) cap
  const frontHousing = monthlyIncome * 0.28;
  // 36% back-end: all debt; housing cap = 36% - existing debts
  const backHousing = monthlyIncome * 0.36 - debts;
  const housingBudget = Math.max(0, Math.min(frontHousing, backHousing));
  const piBudget = Math.max(0, housingBudget - extras);  // principal+interest after tax/ins
  const loan = maxLoan(piBudget, i, n);
  const price = loan + down;
  const binding = frontHousing <= backHousing ? "28% housing rule" : "36% total-debt rule";
  show(`<div class="result-main">$${fmt(price, 0)}<small>Estimated maximum home price you can afford</small></div>
  <table>
    <tr><td>Max monthly housing budget (PITI)</td><td>$${fmt(housingBudget, 0)}</td></tr>
    <tr><td>Of which principal &amp; interest</td><td>$${fmt(piBudget, 0)}</td></tr>
    <tr><td>Supportable loan amount</td><td>$${fmt(loan, 0)}</td></tr>
    <tr><td>+ Your down payment</td><td>$${fmt(down, 0)}</td></tr>
    <tr><td>Limiting factor</td><td>${binding}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How lenders decide what you can borrow</h2>
<p>Mortgage affordability comes down to two debt-to-income ratios, together called the <strong>28/36 rule</strong>. Your total housing payment — principal, interest, property taxes and insurance (PITI) — should stay at or under <strong>28% of gross monthly income</strong> (the "front-end" ratio). And <em>all</em> your debt payments combined, housing included, should stay under <strong>36%</strong> (the "back-end" ratio). This calculator applies both and uses the lower ceiling, then works backward to a maximum home price.</p>
<h2>A worked example</h2>
<p>On $90,000 income ($7,500/month), 28% gives a $2,100 housing budget. With $400 of existing debt, the 36% rule allows $2,300 for housing — so the 28% rule binds at $2,100. Subtract ~$450 of taxes and insurance, leaving ~$1,650 for principal and interest. At 6.5% over 30 years that supports about a $261,000 loan; add a $60,000 down payment and you can afford roughly a <strong>$321,000 home</strong>.</p>
<h2>What "can afford" really means</h2>
<ul>
<li><strong>Borrowing max ≠ spending max.</strong> Lenders will often approve you at the top of these ratios; that doesn't mean you should buy there. Leaving room below the ceiling protects you from becoming "house-poor."</li>
<li><strong>Down payment matters twice.</strong> It raises the price you can afford <em>and</em>, at 20%+, avoids private mortgage insurance (PMI) — see the <a href="/calculators/house-down-payment-calculator/">down payment calculator</a>.</li>
<li><strong>Rate sensitivity is real.</strong> A one-point rate rise can cut your affordable price by tens of thousands, because it shrinks the loan a given payment supports.</li>
</ul>
<h2>Beyond the ratios</h2>
<p>The 28/36 rule ignores your actual life — childcare, irregular income, savings goals, or a long commute all argue for buying below the maximum. Treat the result as a ceiling set by lenders, then subtract a personal safety margin sized to your circumstances. Pair it with the full <a href="/calculators/mortgage-calculator/">mortgage calculator</a> to see the real monthly payment, and read <a href="/articles/how-much-house-can-you-afford/">how much house you can afford</a> for the deeper discussion.</p>
""",
        "faqs": [
            ("How much house can I afford on my income?", "A common guideline caps total housing costs at 28% of gross monthly income and all debt at 36%. On $90,000 income with modest debts, that supports roughly a $300,000–$325,000 home with a healthy down payment, depending on rates."),
            ("What is the 28/36 rule?", "A lending guideline: keep housing costs (principal, interest, taxes, insurance) under 28% of gross monthly income, and all debt payments combined under 36%. Lenders use the lower of the two as your ceiling."),
            ("Should I borrow the maximum I'm approved for?", "Usually not. Approval limits are ceilings, not targets. Buying below the maximum leaves room for savings, emergencies, and life changes, reducing the risk of being stretched too thin by housing costs."),
        ],
    },
    {
        "slug": "rental-property-calculator",
        "emoji": "\U0001F3D8\uFE0F",
        "category": "Business & Self-Employment",
        "title": "Rental Property Calculator — Cap Rate & Cash-on-Cash Return",
        "h1": "Rental Property ROI Calculator",
        "blurb": "Cap rate, cash flow and cash-on-cash return.",
        "meta_description": "Analyze a rental property: net operating income, cap rate, monthly cash flow and cash-on-cash return — the core numbers real estate investors use to judge a deal.",
        "intro": "Judge a rental deal like an investor. Enter the price, rent, expenses and financing to get the cap rate, monthly cash flow, and cash-on-cash return — the numbers that separate a good property from a money pit.",
        "fields": [
            {"id": "price", "label": "Purchase price ($)", "value": 300000},
            {"id": "rent", "label": "Monthly rent ($)", "value": 2400},
            {"id": "expenses", "label": "Monthly operating expenses ($)", "value": 700, "hint": "tax, insurance, maintenance, mgmt, vacancy"},
            {"id": "down", "label": "Down payment (%)", "value": 25, "step": 1},
            {"id": "rate", "label": "Mortgage rate (%)", "value": 7, "step": 0.05},
            {"id": "years", "label": "Mortgage term (years)", "value": 30, "step": 1},
        ],
        "js": """
function calculate() {
  const price = val('price'), rent = val('rent'), exp = val('expenses');
  const downPct = val('down')/100, i = val('rate')/100/12, n = Math.min(Math.round(val('years')*12), 1200);
  if (price <= 0) { show('<div class="result-main">Enter a purchase price above zero.</div>'); return; }
  const noiMonthly = rent - exp;
  const noiAnnual = noiMonthly * 12;
  const capRate = noiAnnual / price * 100;
  const downAmt = price * downPct;
  const loan = price - downAmt;
  const mortgage = i > 0 ? loan * i / (1 - Math.pow(1 + i, -n)) : (n>0 ? loan / n : 0);
  const cashFlow = noiMonthly - mortgage;
  const annualCF = cashFlow * 12;
  const invested = downAmt;  // simplified: down payment as cash invested
  const coc = invested > 0 ? annualCF / invested * 100 : 0;
  const oneP = rent / price * 100;
  show(`<div class="result-main">${fmt(capRate,2)}% cap rate<small>Cash-on-cash return: ${fmt(coc,1)}% \\u00b7 monthly cash flow: $${fmt(cashFlow,0)}</small></div>
  <table>
    <tr><td>Net operating income (annual)</td><td>$${fmt(noiAnnual,0)}</td></tr>
    <tr><td>Cap rate (NOI \\u00f7 price)</td><td>${fmt(capRate,2)}%</td></tr>
    <tr><td>Mortgage payment</td><td>$${fmt(mortgage,0)}/mo</td></tr>
    <tr><td>Monthly cash flow after mortgage</td><td>$${fmt(cashFlow,0)}</td></tr>
    <tr><td>Cash invested (down payment)</td><td>$${fmt(downAmt,0)}</td></tr>
    <tr><td>Cash-on-cash return</td><td>${fmt(coc,1)}%</td></tr>
    <tr><td>Rent-to-price ("1% rule")</td><td>${fmt(oneP,2)}% ${oneP>=1 ? '\\u2705 meets 1% rule' : 'below 1%'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The four numbers that judge a rental</h2>
<p>Real estate investors don't buy on gut feel — they run the numbers. Four metrics do most of the work, and this calculator computes them all:</p>
<ul>
<li><strong>Net Operating Income (NOI):</strong> annual rent minus operating expenses (taxes, insurance, maintenance, management, vacancy allowance) — but <em>before</em> the mortgage. It measures the property's own earning power.</li>
<li><strong>Cap rate:</strong> NOI ÷ purchase price. It's the unleveraged yield — what the property returns if you paid all cash. Lets you compare deals regardless of financing.</li>
<li><strong>Cash flow:</strong> what's left each month after the mortgage. Positive is the goal; negative means the property costs you money every month.</li>
<li><strong>Cash-on-cash return:</strong> annual cash flow ÷ cash actually invested (your down payment). It measures the return on <em>your money</em>, accounting for leverage.</li>
</ul>
<h2>Reading the results</h2>
<p>Cap rates vary by market — 4–5% in expensive coastal cities, 7–10%+ in higher-yield areas (usually with more risk or slower growth). Cash-on-cash return shows leverage at work: borrowing can amplify your return on invested cash, but it also amplifies losses and turns cash flow negative if rents dip or rates are high. A great deal typically shows a healthy cap rate <em>and</em> positive cash flow with a solid cash-on-cash return.</p>
<h2>Don't forget the expenses beginners miss</h2>
<p>The fastest way to fool yourself is to understate expenses. Rookies count taxes and insurance but forget <strong>maintenance, capital expenditures (roof, HVAC), property management, and vacancy</strong>. A common rule of thumb reserves ~50% of rent for operating expenses (excluding mortgage) over the long run. If a deal only works when you assume zero vacancy and no repairs, it doesn't work.</p>
<h2>Quick screens and deeper analysis</h2>
<p>The "1% rule" (monthly rent ≥ 1% of price) is a fast first-pass screen, not a guarantee — it's gotten hard to meet in many markets. Use it to filter, then run the full numbers here. And remember this tool covers the income side; total return also includes appreciation, loan paydown (your tenants building your equity), and tax benefits — real estate's returns come from several sources at once, which is both its appeal and its complexity.</p>
""",
        "faqs": [
            ("What is a good cap rate for rental property?", "It depends on the market and risk. Expensive, high-growth cities often see 4–5%; higher-yield markets 7–10%+. A higher cap rate means more income relative to price but often more risk or less appreciation. Compare within the same market."),
            ("What is cash-on-cash return?", "Your annual pre-tax cash flow divided by the actual cash you invested (mainly the down payment). It measures the return on your own money and reflects the effect of leverage, unlike the cap rate."),
            ("What is the 1% rule?", "A quick screen suggesting monthly rent should be at least 1% of the purchase price. It's a rough first filter, not a full analysis, and has become hard to meet in many markets — always run complete numbers before buying."),
        ],
    },
]
