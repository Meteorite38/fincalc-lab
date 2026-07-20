# -*- coding: utf-8 -*-
"""Batch 10 calculators: home sale net proceeds, blended debt interest rate."""

PART12 = [
    {
        "slug": "home-sale-proceeds-calculator",
        "emoji": "\U0001F3E1",
        "category": "Loans & Debt",
        "title": "Home Sale Proceeds Calculator — What You'll Actually Walk Away With",
        "h1": "Home Sale Proceeds Calculator",
        "blurb": "Your net cash after paying off the mortgage and selling costs.",
        "meta_description": "Calculate your net proceeds from selling a home: sale price minus mortgage payoff, agent commission, closing costs and repairs — the cash you actually keep.",
        "intro": "The sale price isn't what you pocket. Enter your numbers to see your true net proceeds after paying off the mortgage and covering the costs of selling.",
        "fields": [
            {"id": "price", "label": "Expected sale price ($)", "value": 450000},
            {"id": "payoff", "label": "Mortgage balance to pay off ($)", "value": 260000},
            {"id": "commission", "label": "Agent commission (%)", "value": 5, "step": 0.1, "hint": "often 5-6%, split between agents"},
            {"id": "closing", "label": "Seller closing costs (%)", "value": 1.5, "step": 0.1, "hint": "transfer tax, title, legal"},
            {"id": "repairs", "label": "Repairs / staging / concessions ($)", "value": 5000},
        ],
        "js": """
function calculate() {
  const price = val('price'), payoff = val('payoff'), comm = val('commission')/100, close = val('closing')/100, repairs = val('repairs');
  if (price <= 0) { show('<div class="result-main">Enter a sale price above zero.</div>'); return; }
  const commissionCost = price * comm;
  const closingCost = price * close;
  const totalCosts = commissionCost + closingCost + repairs;
  const net = price - payoff - totalCosts;
  const costPct = price>0 ? totalCosts/price*100 : 0;
  show(`<div class="result-main">$${fmt(net,0)}<small>Estimated net cash after payoff and selling costs</small></div>
  <table>
    <tr><td>Sale price</td><td>$${fmt(price,0)}</td></tr>
    <tr><td>Mortgage payoff</td><td>\\u2212$${fmt(payoff,0)}</td></tr>
    <tr><td>Agent commission</td><td>\\u2212$${fmt(commissionCost,0)}</td></tr>
    <tr><td>Closing costs</td><td>\\u2212$${fmt(closingCost,0)}</td></tr>
    <tr><td>Repairs / staging / concessions</td><td>\\u2212$${fmt(repairs,0)}</td></tr>
    <tr><td>Total cost of selling</td><td>$${fmt(totalCosts,0)} (${fmt(costPct,1)}% of price)</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why the sale price isn't the payday</h2>
<p>Sellers fixate on the sale price, but the number that lands in your bank account is <strong>net proceeds</strong> — what's left after paying off the mortgage and covering the surprisingly large costs of selling. The gap between "sold for $450,000" and "walked away with $161,000" catches many sellers off guard. This calculator makes it concrete.</p>
<h2>The costs of selling a home</h2>
<ul>
<li><strong>Agent commission</strong> — usually the biggest cost, often 5–6% of the sale price split between the buyer's and seller's agents. On a $450,000 home that's $22,500–$27,000.</li>
<li><strong>Closing costs</strong> — transfer taxes, title fees, attorney or escrow fees, and sometimes prorated property taxes; roughly 1–3% for the seller.</li>
<li><strong>Repairs, staging, and concessions</strong> — pre-sale fixes, staging, and credits you give the buyer after inspection.</li>
<li><strong>Mortgage payoff</strong> — not a "cost," but it comes straight out of the proceeds. Use your current balance, which may include a small amount of prorated interest.</li>
</ul>
<h2>A worked example</h2>
<p>Sell for $450,000 with $260,000 left on the mortgage, 5% commission ($22,500), 1.5% closing costs ($6,750), and $5,000 of repairs. Net proceeds are about <strong>$155,750</strong> — the sale "cost" roughly $34,250, or 7.6% of the price, before even counting the mortgage. Knowing this number is essential for planning your next purchase or move.</p>
<h2>How to use the result</h2>
<ul>
<li><strong>Plan your next down payment.</strong> Your net proceeds are what you can roll into the next home — feed the figure into our <a href="/calculators/house-down-payment-calculator/">down payment calculator</a>.</li>
<li><strong>Check you're not underwater.</strong> If payoff plus costs exceeds the sale price, you'd need to bring cash to closing. Selling early in a mortgage (when the balance is still high) makes this more likely.</li>
<li><strong>Negotiate commission.</strong> Commission is often negotiable, and even half a percent is real money on a large sale.</li>
</ul>
<p>This is an estimate — exact figures depend on your local taxes, contract, and final settlement statement — but it turns "how much will I actually get?" from a guess into a number you can plan around.</p>
""",
        "faqs": [
            ("How much does it cost to sell a house?", "Typically around 7–10% of the sale price once you add agent commission (5–6%), closing costs (1–3%), and any repairs or concessions — before the mortgage payoff. On a $450,000 home that's often $30,000–$45,000 in selling costs."),
            ("What are net proceeds?", "The cash you actually keep from a home sale: sale price minus your remaining mortgage balance, agent commission, closing costs, and any repairs or buyer concessions."),
            ("Can I end up owing money at closing?", "Yes, if your mortgage payoff plus selling costs exceeds the sale price — being 'underwater.' It's more likely early in a mortgage or after a price decline, and would require bringing cash to the closing table."),
        ],
    },
    {
        "slug": "blended-debt-rate-calculator",
        "emoji": "\U0001F9F5",
        "category": "Loans & Debt",
        "title": "Blended Interest Rate Calculator — Your True Average Debt Rate",
        "h1": "Blended Debt Interest Rate Calculator",
        "blurb": "Weighted-average interest rate across all your debts.",
        "meta_description": "Calculate the blended (weighted-average) interest rate across all your debts and total monthly interest — the real cost of your debt and where to attack first.",
        "intro": "When you owe on several debts at different rates, your true cost is the weighted average. Enter up to four debts to see your blended rate, total balance and monthly interest.",
        "fields": [
            {"id": "bal1", "label": "Debt 1 balance ($)", "value": 6000},
            {"id": "rate1", "label": "Debt 1 rate (%)", "value": 22, "step": 0.1},
            {"id": "bal2", "label": "Debt 2 balance ($)", "value": 15000},
            {"id": "rate2", "label": "Debt 2 rate (%)", "value": 6.5, "step": 0.1},
            {"id": "bal3", "label": "Debt 3 balance ($, 0 if none)", "value": 3000},
            {"id": "rate3", "label": "Debt 3 rate (%)", "value": 12, "step": 0.1},
            {"id": "bal4", "label": "Debt 4 balance ($, 0 if none)", "value": 0},
            {"id": "rate4", "label": "Debt 4 rate (%)", "value": 0, "step": 0.1},
        ],
        "js": """
function calculate() {
  const items = [[val('bal1'),val('rate1')],[val('bal2'),val('rate2')],[val('bal3'),val('rate3')],[val('bal4'),val('rate4')]].filter(x=>x[0]>0);
  const totalBal = items.reduce((s,x)=>s+x[0],0);
  if (totalBal <= 0) { show('<div class="result-main">Enter at least one debt balance above zero.</div>'); return; }
  const weighted = items.reduce((s,x)=>s + x[0]*x[1], 0) / totalBal;
  const annualInterest = items.reduce((s,x)=>s + x[0]*x[1]/100, 0);
  let highest = items.reduce((a,b)=> b[1]>a[1]?b:a, items[0]);
  show(`<div class="result-main">${fmt(weighted,2)}%<small>Your blended (weighted-average) interest rate across $${fmt(totalBal,0)} of debt</small></div>
  <table>
    <tr><td>Total debt</td><td>$${fmt(totalBal,0)}</td></tr>
    <tr><td>Blended annual rate</td><td>${fmt(weighted,2)}%</td></tr>
    <tr><td>Total interest per year</td><td>$${fmt(annualInterest,0)}</td></tr>
    <tr><td>Total interest per month</td><td>$${fmt(annualInterest/12,0)}</td></tr>
    <tr><td>Attack first (highest rate)</td><td>${fmt(highest[1],1)}% on $${fmt(highest[0],0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What a blended rate tells you</h2>
<p>If you carry several debts at different interest rates, no single rate describes your situation — but the <strong>weighted average</strong> does. It blends each debt's rate in proportion to its balance, giving you one honest number for the true cost of your debt. A big balance at a moderate rate can matter more than a small balance at a scary rate, and the blended figure captures exactly that.</p>
<h2>How it's calculated</h2>
<p>Multiply each balance by its rate, add those up, and divide by the total balance: <code>blended rate = Σ(balance × rate) ÷ Σ(balance)</code>. For example, $6,000 at 22%, $15,000 at 6.5%, and $3,000 at 12% blend to about 10.2% across $24,000 of debt — higher than the biggest balance's rate, dragged up by the expensive credit card.</p>
<h2>Why it's useful</h2>
<ul>
<li><strong>It reveals your real cost of debt.</strong> The total interest per month is money leaving your life for nothing — seeing it as one number is motivating.</li>
<li><strong>It benchmarks consolidation.</strong> A <a href="/calculators/debt-consolidation-calculator/">consolidation loan</a> only helps if its rate beats your blended rate <em>without</em> stretching the term too far. Now you have the number to compare against.</li>
<li><strong>It compares against investing.</strong> Paying off debt is a guaranteed return equal to its rate. If your blended rate exceeds what you'd realistically earn investing, paying down debt wins.</li>
</ul>
<h2>But pay off by rate, not by blend</h2>
<p>The blended rate measures your overall cost — but when <em>attacking</em> debt, target the <strong>highest-rate debt first</strong> (the avalanche method), regardless of the average. That minimizes total interest. The calculator flags your highest-rate debt as the place to start. Watching your blended rate fall as you eliminate the expensive debts is a satisfying way to track progress — plan the order with our <a href="/calculators/debt-snowball-vs-avalanche-calculator/">avalanche vs snowball calculator</a>.</p>
""",
        "faqs": [
            ("What is a blended interest rate?", "The weighted-average rate across all your debts, where each debt's rate counts in proportion to its balance. It gives one honest figure for your overall cost of debt, unlike looking at each rate separately."),
            ("How do I calculate my average debt interest rate?", "Multiply each balance by its rate, sum those products, and divide by your total balance. Larger balances influence the average more than smaller ones."),
            ("Should I pay off debt in order of the blended rate?", "No — pay off the highest-rate debt first (the avalanche method) to minimize total interest. The blended rate measures your overall cost; the highest individual rate tells you where to attack."),
        ],
    },
]
