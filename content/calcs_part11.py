# -*- coding: utf-8 -*-
"""Batch 9 calculators: mortgage points, loan comparison, latte factor, salary inflation."""

PART11 = [
    {
        "slug": "mortgage-points-calculator",
        "emoji": "\U0001F4CD",
        "category": "Loans & Debt",
        "title": "Mortgage Points Calculator — Should You Buy Discount Points?",
        "h1": "Mortgage Points Calculator",
        "blurb": "Whether paying points to lower your rate pays off.",
        "meta_description": "See whether buying mortgage discount points is worth it: the upfront cost, monthly savings, and break-even point where paying points starts to pay off.",
        "intro": "Discount points let you pay cash upfront to lower your mortgage rate. Whether that's smart depends entirely on how long you keep the loan. Enter the numbers to find your break-even point.",
        "fields": [
            {"id": "loan", "label": "Loan amount ($)", "value": 300000},
            {"id": "years", "label": "Loan term (years)", "value": 30, "step": 1},
            {"id": "rate", "label": "Rate without points (%)", "value": 6.75, "step": 0.05},
            {"id": "points", "label": "Points purchased", "value": 2, "step": 0.25, "hint": "1 point = 1% of loan"},
            {"id": "reduction", "label": "Rate cut per point (%)", "value": 0.25, "step": 0.05, "hint": "typically ~0.25% per point"},
        ],
        "js": """
function pmt(P, annualPct, n) { const i = annualPct/100/12; return i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n; }
function calculate() {
  const P = val('loan'), n = Math.min(Math.round(val('years')*12),1200);
  const rate = val('rate'), pts = val('points'), red = val('reduction');
  if (P<=0 || n<=0) { show('<div class="result-main">Enter a loan amount and term above zero.</div>'); return; }
  const cost = P * pts/100;
  const newRate = Math.max(0, rate - pts*red);
  const base = pmt(P, rate, n), lower = pmt(P, newRate, n);
  const monthlySave = base - lower;
  if (monthlySave <= 0) { show('<div class="result-main">These points don\\'t lower the payment — check the rate cut per point.</div>'); return; }
  const breakeven = cost / monthlySave;
  const lifeSave = monthlySave*n - cost;
  show(`<div class="result-main">${fmt(breakeven,0)} months to break even<small>Paying $${fmt(cost,0)} up front for a ${fmt(rate,3)}% \\u2192 ${fmt(newRate,3)}% rate</small></div>
  <table>
    <tr><td>Upfront cost of points</td><td>$${fmt(cost,0)}</td></tr>
    <tr><td>Monthly payment saving</td><td>$${fmt(monthlySave)}</td></tr>
    <tr><td>Break-even</td><td>${fmt(breakeven/12,1)} years</td></tr>
    <tr><td>Net saving if you keep the full term</td><td>$${fmt(lifeSave,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What discount points are</h2>
<p>A mortgage "discount point" costs 1% of your loan amount and buys a lower interest rate — typically around 0.25% off per point, though it varies by lender. On a $300,000 loan, one point costs $3,000. You're essentially <strong>pre-paying interest</strong> in a lump sum to get a smaller rate for the life of the loan.</p>
<h2>It all comes down to break-even</h2>
<p>Points are worth it only if you keep the loan long enough for the monthly savings to repay their upfront cost. The math is simple: <code>break-even months = cost of points ÷ monthly savings</code>. If two points cost $6,000 and save $95/month, you break even in about 63 months (5.3 years). Stay past that and points win; sell or refinance sooner and you've lost money.</p>
<h2>When points make sense</h2>
<ul>
<li><strong>You'll keep the mortgage a long time</strong> — well beyond break-even. The longer you hold, the more the lower rate compounds in your favor.</li>
<li><strong>You have spare cash</strong> that isn't better used on the down payment (to avoid PMI) or higher-return goals.</li>
<li><strong>Rates are unlikely to fall soon</strong> — otherwise you might refinance before break-even and waste the points.</li>
</ul>
<h2>When to skip them</h2>
<ul>
<li><strong>You might move or refinance</strong> within a few years — you won't recoup the cost.</li>
<li><strong>The cash is better spent</strong> reaching 20% down (removing PMI often beats buying points) or clearing higher-rate debt.</li>
<li><strong>You're stretching to afford the home</strong> — paying points drains the reserves you'll want for emergencies.</li>
</ul>
<h2>The bottom line</h2>
<p>Points are a bet that you'll stay put. Run your break-even, compare it honestly to how long you realistically expect to keep the loan, and remember the alternatives — a bigger down payment or simply keeping the cash. If you'll hold the mortgage for the long haul and have money to spare, points can be a solid, low-risk saving; otherwise, keep your cash. Pair this with the <a href="/calculators/mortgage-calculator/">mortgage calculator</a> to see the full payment picture.</p>
""",
        "faqs": [
            ("What is a mortgage point?", "A discount point costs 1% of the loan amount and lowers your interest rate, typically by about 0.25% per point. It's a way to pre-pay interest upfront in exchange for a smaller rate over the life of the loan."),
            ("Are mortgage points worth it?", "Only if you keep the loan past the break-even point (upfront cost ÷ monthly savings). Stay longer and points save money; move or refinance sooner and you lose money. They suit long-term holders with spare cash."),
            ("Is buying points better than a bigger down payment?", "Often not. Reaching 20% down to eliminate private mortgage insurance frequently saves more than points, and keeps you from over-borrowing. Compare both uses of the cash before deciding."),
        ],
    },
    {
        "slug": "loan-comparison-calculator",
        "emoji": "\u2696\uFE0F",
        "category": "Loans & Debt",
        "title": "Loan Comparison Calculator — Compare Two Loan Offers",
        "h1": "Loan Comparison Calculator",
        "blurb": "Put two loan offers side by side to see the real cost.",
        "meta_description": "Compare two loan offers side by side: monthly payment, total interest and total cost, so you can see which loan is genuinely cheaper — not just the lower payment.",
        "intro": "A lower monthly payment doesn't mean a cheaper loan. Enter two offers to compare their real cost — monthly payment, total interest, and total repaid — side by side.",
        "fields": [
            {"id": "amount", "label": "Loan amount ($)", "value": 25000},
            {"id": "rateA", "label": "Offer A — rate (%)", "value": 7.5, "step": 0.1},
            {"id": "yearsA", "label": "Offer A — term (years)", "value": 4, "step": 1},
            {"id": "rateB", "label": "Offer B — rate (%)", "value": 6.9, "step": 0.1},
            {"id": "yearsB", "label": "Offer B — term (years)", "value": 6, "step": 1},
        ],
        "js": """
function pay(P, annualPct, yrs) { const i = annualPct/100/12, n = Math.min(Math.round(yrs*12),1200); const p = i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n; return {p, n, total: p*n, interest: p*n - P}; }
function calculate() {
  const P = val('amount');
  if (P<=0) { show('<div class="result-main">Enter a loan amount above zero.</div>'); return; }
  const A = pay(P, val('rateA'), val('yearsA')), B = pay(P, val('rateB'), val('yearsB'));
  const cheaper = A.interest < B.interest ? 'A' : (B.interest < A.interest ? 'B' : 'tie');
  const diff = Math.abs(A.interest - B.interest);
  show(`<div class="result-main">${cheaper==='tie' ? 'Both cost the same' : 'Offer '+cheaper+' costs $'+fmt(diff,0)+' less'}<small>in total interest over the life of the loan</small></div>
  <table>
    <tr><td></td><td><strong>Offer A</strong></td><td><strong>Offer B</strong></td></tr>
    <tr><td>Monthly payment</td><td>$${fmt(A.p)}</td><td>$${fmt(B.p)}</td></tr>
    <tr><td>Total interest</td><td>$${fmt(A.interest,0)}</td><td>$${fmt(B.interest,0)}</td></tr>
    <tr><td>Total repaid</td><td>$${fmt(A.total,0)}</td><td>$${fmt(B.total,0)}</td></tr>
    <tr><td>Term</td><td>${(A.n/12).toFixed(0)} yrs</td><td>${(B.n/12).toFixed(0)} yrs</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why the lower payment can be the worse deal</h2>
<p>Lenders love to advertise the monthly payment because it's the number that feels affordable. But a lower payment often just means a <em>longer term</em> — and stretching a loan over more years piles on interest even at a similar or lower rate. The only fair comparison is <strong>total interest</strong> and total amount repaid, which this calculator puts side by side.</p>
<h2>A worked example</h2>
<p>Borrow $25,000. Offer A is 7.5% over 4 years (~$605/month, ~$4,050 interest). Offer B is 6.9% over 6 years (~$425/month, ~$5,600 interest). Offer B has the lower rate <em>and</em> the lower payment — yet it costs about $1,550 more in total, because you're borrowing for two extra years. The "better-looking" offer is the more expensive one.</p>
<h2>What to compare, and what to watch</h2>
<ul>
<li><strong>Total interest and total repaid</strong> — the true cost. Prioritise these over the monthly payment.</li>
<li><strong>APR, not just the rate</strong> — APR folds in mandatory fees, so it's a fairer rate comparison. Origination fees can make a "lower rate" cost more.</li>
<li><strong>Term trade-off</strong> — a shorter term means higher payments but far less interest. Choose the shortest term whose payment you can comfortably afford.</li>
<li><strong>Prepayment penalties</strong> — a loan you can overpay freely is more valuable; check before signing.</li>
</ul>
<h2>How to use the result</h2>
<p>If your goal is the lowest total cost, pick the offer with the least total interest you can afford the payment on. If cash flow is tight, you might knowingly accept more total interest for a lower payment — but make that trade with eyes open, seeing exactly what the flexibility costs. Either way, decide on the full numbers, not the headline payment.</p>
""",
        "faqs": [
            ("How do I compare two loans fairly?", "Compare total interest and total amount repaid, not just the monthly payment. A lower payment often means a longer term and more total interest. Also compare APR rather than the headline rate, since APR includes mandatory fees."),
            ("Why does a lower monthly payment cost more?", "Because the payment is usually lowered by extending the term. Borrowing over more years accrues more interest, so a smaller payment can hide a larger total cost."),
            ("Should I always pick the shortest term?", "Financially, shorter terms cost less interest — so choose the shortest term whose payment you can comfortably afford. If cash flow is tight, a longer term is a valid trade, as long as you know the extra total cost."),
        ],
    },
    {
        "slug": "latte-factor-calculator",
        "emoji": "\u2615",
        "category": "Savings & Investing",
        "title": "Latte Factor Calculator — What Small Daily Spending Really Costs",
        "h1": "Latte Factor Calculator",
        "blurb": "What a small recurring spend could grow to if invested.",
        "meta_description": "See what a small recurring expense — a daily coffee, subscription or habit — could grow to if you invested it instead. The eye-opening math of the 'latte factor'.",
        "intro": "Small recurring expenses feel trivial, but invested over years they add up to startling sums. Enter a regular spend to see what it could become if invested instead.",
        "fields": [
            {"id": "amount", "label": "Amount per occurrence ($)", "value": 5},
            {"id": "freq", "label": "How often?", "value": "365", "type": "select",
             "options": [["365", "Every day"], ["260", "Every weekday"], ["52", "Weekly"], ["12", "Monthly"]]},
            {"id": "years", "label": "Years", "value": 30, "step": 1},
            {"id": "rate", "label": "Expected annual return (%)", "value": 7, "step": 0.1},
        ],
        "js": """
function calculate() {
  const amt = val('amount'), perYear = parseFloat(document.getElementById('freq').value), y = val('years'), r = val('rate')/100;
  const annual = amt * perYear;
  const monthly = annual / 12, i = r/12, n = Math.round(y*12);
  const fv = i>0 ? monthly*((Math.pow(1+i,n)-1)/i) : monthly*n;
  const spent = annual * y;
  show(`<div class="result-main">$${fmt(fv,0)}<small>if you invested it instead over ${y} years at ${fmt(r*100,1)}%</small></div>
  <table>
    <tr><td>Cost per year</td><td>$${fmt(annual,0)}</td></tr>
    <tr><td>Total spent over ${y} years</td><td>$${fmt(spent,0)}</td></tr>
    <tr><td>If invested — future value</td><td>$${fmt(fv,0)}</td></tr>
    <tr><td>Investment growth on top of deposits</td><td>$${fmt(fv-spent,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The idea behind the "latte factor"</h2>
<p>Popularized by author David Bach, the latte factor is the idea that small, habitual purchases — the daily coffee, the barely-used subscription, the impulse snack — quietly cost a fortune over a lifetime, especially when you count the returns that money could have earned instead. It's not really about coffee; it's about noticing where money leaks and what those leaks are truly worth.</p>
<h2>The eye-opening math</h2>
<p>A $5 daily coffee is $1,825 a year. Spent, it's gone. But invested at a 7% return for 30 years, those same daily $5 grow to roughly <strong>$185,000</strong> — because the deposits keep <a href="/articles/how-compound-interest-builds-wealth/">compounding</a> year after year. The gap between "spent" and "invested" is the hidden cost of the habit, and it's often shockingly large.</p>
<h2>How to use this — and how not to</h2>
<p>The point isn't to never enjoy anything. A $5 coffee that genuinely brightens your day may be worth it. The point is <strong>intentionality</strong>: know what a recurring expense really costs so you can decide if it's worth that price. Run your own habits through the calculator and you'll usually find one or two that you'd happily trade for a six-figure future balance — and others you'll keep, guilt-free, because now you've chosen them on purpose.</p>
<h2>The bigger lesson</h2>
<ul>
<li><strong>Recurring beats one-time.</strong> A single purchase is minor; a <em>daily</em> one is a subscription to poverty or wealth, depending on direction. Focus on habits, not one-offs.</li>
<li><strong>Redirect, don't just cut.</strong> The magic only happens if the money you don't spend actually gets invested (ideally <a href="/articles/dollar-cost-averaging-explained/">automatically</a>). Cutting a habit and spending it elsewhere changes nothing.</li>
<li><strong>Big rocks matter more.</strong> Housing, transport, and food dwarf lattes. Apply the same "what could this be worth invested?" lens to the large recurring costs for the biggest wins.</li>
</ul>
<p>Used well, the latte factor isn't about deprivation — it's a lens that turns invisible small spending into a conscious choice between a habit today and a much larger sum tomorrow.</p>
""",
        "faqs": [
            ("What is the latte factor?", "A concept popularized by David Bach: small, recurring expenses add up to large sums over time, especially counting the investment returns that money could have earned. It's about noticing money leaks, not literally quitting coffee."),
            ("Does giving up coffee really make me rich?", "Not by itself — but the math shows a $5 daily habit invested at 7% for 30 years could grow to around $185,000. The real lesson is intentionality and redirecting saved money into investments, including bigger expenses than coffee."),
            ("What return should I assume?", "A diversified stock portfolio has historically returned around 7% a year before inflation over long periods. Use 6–7% for a realistic long-run estimate; lower if you want an inflation-adjusted figure."),
        ],
    },
    {
        "slug": "salary-inflation-calculator",
        "emoji": "\U0001F4C9",
        "category": "Income & Budgeting",
        "title": "Salary Inflation Calculator — Has Your Pay Kept Up?",
        "h1": "Salary Inflation Calculator",
        "blurb": "Whether your salary has kept pace with inflation.",
        "meta_description": "Find out whether your salary has kept up with inflation: what your old salary is worth in today's money, and the raise you'd need just to break even.",
        "intro": "A salary that stays flat is really a pay cut, because inflation erodes what it buys. Enter an old salary and your current one to see whether you've actually gained ground.",
        "fields": [
            {"id": "oldsalary", "label": "Salary a few years ago ($)", "value": 55000},
            {"id": "cursalary", "label": "Current salary ($)", "value": 62000},
            {"id": "years", "label": "Years between them", "value": 5, "step": 1},
            {"id": "inflation", "label": "Average annual inflation (%)", "value": 3.5, "step": 0.1},
        ],
        "js": """
function calculate() {
  const oldS = val('oldsalary'), cur = val('cursalary'), y = val('years'), inf = val('inflation')/100;
  if (oldS<=0) { show('<div class="result-main">Enter your earlier salary above zero.</div>'); return; }
  const needed = oldS * Math.pow(1+inf, y);   // what old salary must become to hold value
  const realNow = cur / Math.pow(1+inf, y);   // current salary in old-year money
  const gapPct = (cur - needed) / needed * 100;
  const verdict = cur >= needed ? 'Ahead of inflation \\u2705 — real raise' : 'Behind inflation — a real-terms pay cut';
  show(`<div class="result-main">${gapPct>=0?'+':''}${fmt(gapPct,1)}% real change<small>${verdict}</small></div>
  <table>
    <tr><td>To just keep pace, you'd need</td><td>$${fmt(needed,0)}</td></tr>
    <tr><td>Your current salary</td><td>$${fmt(cur,0)}</td></tr>
    <tr><td>Difference vs breaking even</td><td>${cur>=needed?'+':''}$${fmt(cur-needed,0)}</td></tr>
    <tr><td>Current salary in ${y}-years-ago money</td><td>$${fmt(realNow,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why a flat salary is a pay cut</h2>
<p>If prices rise 3.5% a year and your salary doesn't move, you can buy less each year — your <em>real</em> income falls even though the number on your contract is unchanged. To simply hold your ground, your pay has to rise at least as fast as inflation. This calculator shows whether it has, by comparing your current salary to what your old salary would need to be today just to break even.</p>
<h2>A worked example</h2>
<p>Suppose you earned $55,000 five years ago and now earn $62,000 — a 12.7% raise that feels decent. But at 3.5% average inflation, $55,000 would need to be about $65,300 today just to buy the same things. So despite the raise, your purchasing power has actually <strong>fallen about 5%</strong>. The headline increase masked a real-terms cut.</p>
<h2>What to do with this</h2>
<ul>
<li><strong>Benchmark raises against inflation, not zero.</strong> A "3% raise" in a 4% inflation year is a real pay cut. Any pay negotiation should start from the inflation figure and add real value on top.</li>
<li><strong>Track it over time.</strong> Small annual shortfalls compound. A few years of below-inflation raises quietly erode your standard of living even as your salary "grows."</li>
<li><strong>Use it in negotiations.</strong> Framing a request as "cost-of-living adjustment plus recognition of my expanded role" is far stronger than a round number — see our <a href="/calculators/pay-raise-calculator/">pay raise calculator</a> to model the ask.</li>
</ul>
<h2>The bigger picture</h2>
<p>Inflation is a quiet force that works against savers and wage-earners alike. The same logic that erodes a flat salary erodes idle cash — which is why keeping money invested (earning a return above inflation) matters, and why your <a href="/calculators/real-return-calculator/">real return</a> is the number that counts. Whether you're evaluating a job offer or your career trajectory, always translate the raise into real, after-inflation terms before deciding how good it really is.</p>
""",
        "faqs": [
            ("How do I know if my raise beat inflation?", "Grow your old salary by the inflation rate over the period. If your current salary is higher than that figure, you gained real purchasing power; if it's lower, you had a real-terms pay cut despite the raise."),
            ("What inflation rate should I use?", "Use the average annual inflation over the period in question — often 2–4% in normal times, higher in inflationary periods. Official consumer price index (CPI) figures are a reasonable basis."),
            ("My salary rose but I feel poorer — why?", "Because prices rose faster than your pay. A larger salary number can still buy less if inflation outpaced your raises. Purchasing power, not the headline figure, is what determines how well off you actually are."),
        ],
    },
]
