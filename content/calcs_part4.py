# -*- coding: utf-8 -*-
"""Batch 2 calculators: more Savings/Investing, Retirement, and Net worth."""

PART4 = [
    {
        "slug": "roi-calculator",
        "emoji": "\U0001F4B9",
        "category": "Savings & Investing",
        "title": "ROI Calculator — Return on Investment (Simple & Annualized)",
        "h1": "ROI Calculator",
        "blurb": "Total and annualized return on any investment or project.",
        "meta_description": "Calculate return on investment (ROI) from cost and final value, including total ROI, net profit and an annualized rate for fair comparison across time periods.",
        "intro": "ROI answers the simplest money question: for every dollar I put in, how much did I get back? Enter what you invested, what it became, and how long you held it — you get both the headline ROI and the annualized rate that makes different investments comparable.",
        "fields": [
            {"id": "cost", "label": "Amount invested ($)", "value": 5000},
            {"id": "final", "label": "Final value / amount returned ($)", "value": 8000},
            {"id": "years", "label": "Holding period (years)", "value": 3, "step": 0.1},
        ],
        "js": """
function calculate() {
  const c = val('cost'), f = val('final'), y = val('years');
  if (c <= 0) { show('<div class="result-main">Amount invested must be above zero.</div>'); return; }
  const profit = f - c;
  const roi = profit / c * 100;
  const ann = y > 0 ? (Math.pow(f / c, 1 / y) - 1) * 100 : NaN;
  show(`<div class="result-main">${fmt(roi)}%<small>Total ROI &mdash; net ${profit >= 0 ? 'profit' : 'loss'} of $${fmt(Math.abs(profit))}</small></div>
  <table>
    <tr><td>Net profit</td><td>$${fmt(profit)}</td></tr>
    <tr><td>Money multiple</td><td>${fmt(f / c)}x</td></tr>
    <tr><td>Annualized ROI (${fmt(y,1)} yr)</td><td>${isFinite(ann) ? fmt(ann) + '%' : '—'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Simple ROI vs annualized ROI</h2>
<p><strong>Simple ROI</strong> = (final value − cost) ÷ cost. It's the total percentage gain over the whole holding period, ignoring how long that took. A 60% ROI sounds great — but 60% over one year and 60% over ten years are wildly different investments.</p>
<p><strong>Annualized ROI</strong> fixes this by converting the total return into a per-year rate using compounding: <code>(final ÷ cost)<sup>1/years</sup> − 1</code>. That 60% total becomes 60%/year over one year, but only about 4.8%/year over ten. Always compare investments on the annualized figure.</p>
<h2>What to include in "cost"</h2>
<p>Real ROI counts every dollar the investment required, not just the sticker price: purchase cost, fees, commissions, renovation or setup costs, and ongoing expenses. Leaving these out inflates ROI and is the most common way people fool themselves about a deal's quality.</p>
<h2>Where ROI is used — and its blind spots</h2>
<ul>
<li><strong>Business projects:</strong> "this $5,000 software will save $8,000" is a 60% ROI decision.</li>
<li><strong>Marketing:</strong> revenue generated per dollar of ad spend.</li>
<li><strong>Investments:</strong> though for cash-flowing assets, annualized ROI (or IRR) beats simple ROI.</li>
</ul>
<p>ROI's blind spot is <em>risk and time</em>. It says nothing about how likely the return was, or the volatility along the way. A 40% ROI from a government bond and a 40% ROI from a lottery-like startup are not equivalent, even though the number is identical. Use ROI to rank comparable options, not to justify taking on wildly different risks.</p>
""",
        "faqs": [
            ("What is a good ROI?", "It depends entirely on the asset class and risk. Long-run stock market ROI has averaged roughly 7–10% annualized; a business project might target 20%+ to justify the effort and risk. 'Good' means beating your alternatives at a similar risk level."),
            ("Can ROI be negative?", "Yes — if the final value is less than the amount invested, ROI is negative, representing a loss on your capital."),
            ("Why is my annualized ROI so much lower than simple ROI?", "Because compounding spreads the gain across years. A large total return earned slowly is a modest annual rate. This is exactly why annualized figures prevent long, mediocre investments from looking impressive."),
        ],
    },
    {
        "slug": "rule-of-72-calculator",
        "emoji": "\u23F3",
        "category": "Savings & Investing",
        "title": "Rule of 72 Calculator — How Long to Double Your Money",
        "h1": "Rule of 72 Calculator",
        "blurb": "Estimate doubling time from an interest or growth rate.",
        "meta_description": "Use the Rule of 72 to estimate how many years it takes to double your money at a given rate — plus the exact doubling time for comparison.",
        "intro": "The Rule of 72 is the most useful piece of mental math in finance: divide 72 by your annual return, and you get roughly how many years it takes to double your money. Enter a rate to see the estimate — and how close it is to the exact answer.",
        "fields": [
            {"id": "rate", "label": "Annual return / interest rate (%)", "value": 8, "step": 0.1},
            {"id": "amount", "label": "Starting amount ($, optional)", "value": 10000},
        ],
        "js": """
function calculate() {
  const r = val('rate'), a = val('amount');
  if (r <= 0) { show('<div class="result-main">Enter a rate above zero.</div>'); return; }
  const rule = 72 / r;
  const exact = Math.log(2) / Math.log(1 + r / 100);
  let rows = `<tr><td>Rule of 72 estimate</td><td>${fmt(rule,1)} years</td></tr>
    <tr><td>Exact doubling time</td><td>${fmt(exact,1)} years</td></tr>`;
  if (a > 0) {
    rows += `<tr><td>${a.toLocaleString()} doubles to</td><td>$${fmt(a*2,0)} in ~${fmt(rule,1)} yrs</td></tr>
    <tr><td>Quadruples (2 doublings)</td><td>$${fmt(a*4,0)} in ~${fmt(rule*2,1)} yrs</td></tr>`;
  }
  show(`<div class="result-main">~${fmt(rule,1)} years<small>to double at ${fmt(r,1)}% per year</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>Why 72?</h2>
<p>The exact doubling time comes from logarithms: <code>ln(2) ÷ ln(1 + rate)</code>. That's not something you can do in your head. The number 72 is a clever approximation — it divides cleanly by 2, 3, 4, 6, 8, 9 and 12, and it's most accurate for rates in the 6–10% range that matter most to investors. At 8%, the rule says 9 years; the exact answer is 9.01. Remarkably close for mental math.</p>
<h2>Everyday uses</h2>
<ul>
<li><strong>Investing:</strong> at an 8% average return, money doubles roughly every 9 years — so a 27-year horizon means about three doublings, an 8x increase.</li>
<li><strong>Inflation, in reverse:</strong> at 3% inflation, prices double (your money's purchasing power halves) in about 24 years. At 6%, just 12.</li>
<li><strong>Debt, as a warning:</strong> a 24% credit card balance left unpaid doubles what you owe in about 3 years.</li>
</ul>
<h2>Accuracy and limits</h2>
<p>For higher rates the rule drifts: at 20%, it estimates 3.6 years vs an exact 3.8. Some people switch to 70 for continuous compounding or 69.3 for maximum precision, but 72 wins on mental-math convenience. The bigger caveat: real investments don't return a steady rate — they average one out through violent ups and downs. The Rule of 72 tells you what a smooth average implies, which is a planning guide, not a prediction of any single year.</p>
""",
        "faqs": [
            ("Is the Rule of 72 accurate?", "Very accurate for rates between about 5% and 12% — usually within a fraction of a year. It drifts wider at very high or very low rates, where you should use the exact formula shown above."),
            ("Can I use it for inflation?", "Yes. Dividing 72 by the inflation rate estimates how long until your money's purchasing power halves — a sobering way to see why idle cash loses value."),
            ("What rate should I assume for investing?", "Historically diversified stocks have averaged roughly 7–10% before inflation. Using a conservative 7% (a ~10-year double) keeps expectations realistic."),
        ],
    },
    {
        "slug": "present-value-calculator",
        "emoji": "\U0001F550",
        "category": "Savings & Investing",
        "title": "Present Value Calculator — What Future Money Is Worth Today",
        "h1": "Present Value Calculator",
        "blurb": "Discount a future sum back to today's dollars.",
        "meta_description": "Calculate the present value of a future amount using a discount rate — understand the time value of money and compare payouts across different dates.",
        "intro": "A dollar tomorrow is worth less than a dollar today. Present value tells you exactly how much less: enter a future amount, a discount rate and the years until you receive it, to see what that money is worth in today's terms.",
        "fields": [
            {"id": "future", "label": "Future amount ($)", "value": 50000},
            {"id": "rate", "label": "Discount rate (%)", "value": 6, "step": 0.1, "hint": "your required return or opportunity cost"},
            {"id": "years", "label": "Years until received", "value": 10, "step": 0.5},
        ],
        "js": """
function calculate() {
  const fv = val('future'), r = val('rate') / 100, y = val('years');
  const pv = fv / Math.pow(1 + r, y);
  const discount = fv - pv;
  show(`<div class="result-main">$${fmt(pv)}<small>Today's value of $${fmt(fv,0)} received in ${fmt(y,1)} years</small></div>
  <table>
    <tr><td>Value lost to discounting</td><td>$${fmt(discount)}</td></tr>
    <tr><td>Discount factor</td><td>${fmt(pv / fv, 3)}</td></tr>
    <tr><td>Each future dollar is worth today</td><td>$${fmt(pv / fv, 3)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The time value of money</h2>
<p>Money available now is worth more than the same amount later, for three reasons: you could invest it and earn a return, inflation erodes future purchasing power, and future payments carry the risk they never arrive. Present value (PV) quantifies all of this in one number using the formula <code>PV = FV ÷ (1 + r)<sup>years</sup></code>, where <em>r</em> is the discount rate.</p>
<h2>Choosing a discount rate</h2>
<p>The discount rate is the return you could otherwise earn on your money — your opportunity cost. Use a low rate (3–4%) if your alternative is safe savings; a higher rate (8–10%+) if you'd otherwise invest in stocks or fund a business. The higher the rate, the more aggressively future money is discounted: at 10%, $50,000 in ten years is worth only about $19,300 today; at 3%, about $37,200. The rate choice dominates the answer.</p>
<h2>Where present value decides real questions</h2>
<ul>
<li><strong>Lump sum vs installments:</strong> is a $500,000 lottery lump sum better than $700,000 paid over 20 years? PV settles it.</li>
<li><strong>Pension or buyout offers:</strong> comparing a one-time payout against a future stream.</li>
<li><strong>Business investment:</strong> a project's future cash flows are only worth their combined present value today — the basis of net present value (NPV) analysis.</li>
</ul>
<p>The intuition to keep: whenever someone offers you money in the future, mentally discount it. Distant promises are worth less than their face value, and the longer the wait or the higher your opportunity cost, the bigger the discount.</p>
""",
        "faqs": [
            ("What's the difference between present value and future value?", "Future value grows today's money forward at a rate; present value discounts tomorrow's money back. They're inverse operations using the same rate and time period."),
            ("What discount rate should I use?", "Your opportunity cost — the return you'd realistically earn on the money elsewhere. There's no universal 'correct' rate; it reflects your alternatives and risk tolerance, which is why PV analysis always states its rate."),
            ("Does this handle a stream of payments?", "This tool discounts a single future sum. For a series of payments, you present-value each one and sum them (the basis of annuity and NPV calculations)."),
        ],
    },
    {
        "slug": "dividend-income-calculator",
        "emoji": "\U0001FA99",
        "category": "Savings & Investing",
        "title": "Dividend Income Calculator — Annual Payout & Yield",
        "h1": "Dividend Income Calculator",
        "blurb": "Annual dividend income, yield and reinvested growth.",
        "meta_description": "Calculate annual dividend income from your portfolio value and dividend yield, including monthly income and a projection of dividend growth over time.",
        "intro": "Estimate the income a dividend portfolio produces. Enter your investment amount and the average dividend yield to see annual and monthly income — plus how reinvesting and dividend growth compound the payout over time.",
        "fields": [
            {"id": "amount", "label": "Portfolio value ($)", "value": 100000},
            {"id": "yield", "label": "Average dividend yield (%)", "value": 3.5, "step": 0.1},
            {"id": "growth", "label": "Annual dividend growth (%)", "value": 5, "step": 0.1, "hint": "how fast payouts rise"},
            {"id": "years", "label": "Years to project", "value": 10, "step": 1},
        ],
        "js": """
function calculate() {
  const p = val('amount'), y = val('yield') / 100, g = val('growth') / 100, n = val('years');
  const annual = p * y;
  const future = annual * Math.pow(1 + g, n);
  const yieldOnCost = future / p * 100;
  show(`<div class="result-main">$${fmt(annual)} / year<small>$${fmt(annual/12)} per month at ${fmt(y*100,1)}% yield</small></div>
  <table>
    <tr><td>Annual income now</td><td>$${fmt(annual)}</td></tr>
    <tr><td>Annual income in ${n} yrs (payout growth only)</td><td>$${fmt(future)}</td></tr>
    <tr><td>Yield on cost in ${n} yrs</td><td>${fmt(yieldOnCost,1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How dividend income works</h2>
<p>Dividend-paying companies distribute part of their profits to shareholders, usually quarterly. Your annual income is simply <code>portfolio value × dividend yield</code>. A $100,000 portfolio yielding 3.5% produces $3,500 a year, about $290 a month — income you receive without selling any shares.</p>
<h2>Two engines of dividend growth</h2>
<p>This calculator shows the effect of <strong>dividend growth</strong> — healthy companies tend to raise their payouts over time. At 5% annual growth, that $3,500 becomes about $5,700 in ten years <em>from the same shares</em>, lifting your "yield on cost" well above the starting yield. The second engine, not shown here, is <strong>reinvestment</strong>: using dividends to buy more shares, which then pay their own dividends. Combined, the two produce the powerful compounding that dividend-growth investors rely on.</p>
<h2>Reality checks</h2>
<ul>
<li><strong>Yield traps:</strong> an unusually high yield (say 8%+) often signals a falling share price and a dividend at risk of being cut. Sustainable yields matter more than headline ones.</li>
<li><strong>Taxes:</strong> dividends are typically taxable in the year received (rates vary by country and account type), which reduces the cash you keep.</li>
<li><strong>Not guaranteed:</strong> dividends can be reduced or eliminated in hard times. Diversification across many payers reduces the impact of any single cut.</li>
</ul>
<p>Dividend investing appeals to those who want a growing income stream and psychological staying power in downturns — but total return (price growth plus dividends) is what ultimately builds wealth, so don't chase yield at the expense of quality.</p>
""",
        "faqs": [
            ("Is dividend yield the same as total return?", "No. Yield is only the income portion. Total return also includes share price appreciation (or loss). A 3% yield with 5% price growth is an 8% total return."),
            ("How often are dividends paid?", "Most companies pay quarterly, some monthly or semi-annually. This calculator works in annual terms; divide by 12 for a rough monthly figure."),
            ("What is 'yield on cost'?", "Your current annual dividend divided by your original investment. As companies raise payouts, yield on cost climbs even though the market yield stays similar — a key reward of long-term dividend-growth holding."),
        ],
    },
    {
        "slug": "net-worth-calculator",
        "emoji": "\U0001F4CB",
        "category": "Budgeting & Life",
        "title": "Net Worth Calculator — Assets Minus Liabilities",
        "h1": "Net Worth Calculator",
        "blurb": "Add up what you own, subtract what you owe.",
        "meta_description": "Calculate your net worth by totalling assets and subtracting liabilities. The single number that tracks your true financial progress over time.",
        "intro": "Net worth is the one number that captures your whole financial picture: everything you own minus everything you owe. Fill in your assets and debts to see where you stand — then track it over time, because the trend matters far more than the snapshot.",
        "fields": [
            {"id": "cash", "label": "Cash & savings ($)", "value": 15000},
            {"id": "investments", "label": "Investments & retirement ($)", "value": 40000},
            {"id": "property", "label": "Property & vehicles ($)", "value": 250000},
            {"id": "other_assets", "label": "Other assets ($)", "value": 5000},
            {"id": "mortgage", "label": "Mortgage & property loans ($)", "value": 180000},
            {"id": "other_debt", "label": "Other debts (cards, loans) ($)", "value": 12000},
        ],
        "js": """
function calculate() {
  const assets = val('cash') + val('investments') + val('property') + val('other_assets');
  const debts = val('mortgage') + val('other_debt');
  const nw = assets - debts;
  const liquid = val('cash') + val('investments');
  show(`<div class="result-main">$${fmt(nw,0)}<small>Net worth &mdash; total assets minus total debts</small></div>
  <table>
    <tr><td>Total assets</td><td>$${fmt(assets,0)}</td></tr>
    <tr><td>Total liabilities</td><td>$${fmt(debts,0)}</td></tr>
    <tr><td>Liquid net worth (cash + investments − debt)</td><td>$${fmt(liquid - debts,0)}</td></tr>
    <tr><td>Debt as % of assets</td><td>${assets > 0 ? fmt(debts/assets*100,0) : '—'}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What net worth really measures</h2>
<p>Net worth = total assets − total liabilities. It cuts through income and lifestyle to show what you'd actually have if you sold everything and paid off every debt. Someone earning $200,000 with a negative net worth is, financially, behind a $60,000 earner who owns their modest home outright. Income is the engine; net worth is the odometer.</p>
<h2>Counting assets honestly</h2>
<ul>
<li><strong>Liquid assets:</strong> cash, savings, and investments you could access relatively quickly.</li>
<li><strong>Property:</strong> your home and vehicles at realistic resale value, not what you paid or hope to get.</li>
<li><strong>Retirement accounts:</strong> count them, but remember they may carry taxes or penalties on early access.</li>
</ul>
<p>Be conservative. Inflating asset values just flatters a number that's most useful when it's honest.</p>
<h2>Liquid net worth — the tougher, truer figure</h2>
<p>Your home is usually your largest asset but the hardest to spend; you can't sell a bedroom to cover an emergency. That's why <em>liquid</em> net worth (cash and investments minus debts) often matters more day to day. A large net worth that's almost entirely home equity can coexist with a genuine cash crunch.</p>
<h2>The habit that builds wealth</h2>
<p>Calculate net worth on the same date every quarter and record it. The absolute value matters less than the direction and slope. Rising steadily means your financial system is working; flat or falling despite good income exposes lifestyle inflation or hidden debt. This single tracked number is the most honest scorecard in personal finance.</p>
""",
        "faqs": [
            ("Should I include my home in net worth?", "Yes — at a realistic market value, with the mortgage counted as a liability. Just remember home equity is illiquid, which is why many people also track 'liquid net worth' separately."),
            ("Is a negative net worth bad?", "Common and not necessarily alarming — recent graduates with student loans often start negative. What matters is the trajectory: moving toward and past zero over time is the goal."),
            ("How often should I calculate it?", "Quarterly is plenty for most people. Monthly can feel noisy due to market swings; annually can miss course-correction opportunities. The key is consistency of date and method."),
        ],
    },
    {
        "slug": "401k-calculator",
        "emoji": "\U0001F3E6",
        "category": "Retirement",
        "title": "401(k) Calculator — Retirement Growth with Employer Match",
        "h1": "401(k) Calculator",
        "blurb": "Project 401(k) growth including the employer match.",
        "meta_description": "Project your 401(k) balance at retirement including your contributions, employer match and investment growth — and see how much the match adds over a career.",
        "intro": "Your 401(k) has a feature almost nothing else offers: free money from your employer's match. Enter your salary, contribution rate and match to project your balance at retirement — and see just how much the match alone is worth.",
        "fields": [
            {"id": "salary", "label": "Annual salary ($)", "value": 70000},
            {"id": "contrib", "label": "Your contribution (% of salary)", "value": 10, "step": 0.5},
            {"id": "match", "label": "Employer match (% of salary)", "value": 4, "step": 0.5, "hint": "e.g. 100% match up to 4%"},
            {"id": "balance", "label": "Current 401(k) balance ($)", "value": 25000},
            {"id": "rate", "label": "Expected annual return (%)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Years until retirement", "value": 30, "step": 1},
        ],
        "js": """
function calculate() {
  const s = val('salary'), cr = val('contrib')/100, m = val('match')/100;
  const P = val('balance'), r = val('rate')/100, y = val('years');
  const annualContrib = s * cr, annualMatch = s * m;
  const total = annualContrib + annualMatch;
  const i = r/12, n = y*12, pmt = total/12, growth = Math.pow(1+i,n);
  const fv = P*growth + (i>0 ? pmt*(growth-1)/i : pmt*n);
  const matchOnly = i>0 ? (annualMatch/12)*(growth-1)/i : (annualMatch/12)*n;
  show(`<div class="result-main">$${fmt(fv,0)}<small>Projected 401(k) at retirement (${y} years)</small></div>
  <table>
    <tr><td>Your yearly contribution</td><td>$${fmt(annualContrib,0)}</td></tr>
    <tr><td>Employer match yearly</td><td>$${fmt(annualMatch,0)} (free money)</td></tr>
    <tr><td>Value from the match alone</td><td>$${fmt(matchOnly,0)}</td></tr>
    <tr><td>Total contributed over career</td><td>$${fmt(P + total*y,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The employer match is a 100% instant return</h2>
<p>If your employer matches 100% of contributions up to, say, 4% of salary, every dollar you put in (up to that limit) is immediately doubled. No investment on earth reliably offers a guaranteed 100% return — turning down a full match is leaving free salary on the table. The first rule of retirement saving is: <strong>contribute at least enough to capture the entire match.</strong></p>
<h2>How the projection works</h2>
<p>The calculator combines your contribution and the employer match into monthly deposits, then compounds them plus your current balance at your expected return until retirement. Notice the "value from the match alone" line — over a 30-year career, an employer match can quietly grow into hundreds of thousands of dollars you never earned at work.</p>
<h2>Levers that matter</h2>
<ul>
<li><strong>Start early.</strong> Because of compounding, contributions in your 20s do far more work than the same dollars in your 50s.</li>
<li><strong>Raise the rate over time.</strong> Bumping your contribution 1% each raise is nearly painless and dramatically changes the outcome.</li>
<li><strong>Mind the fees.</strong> Fund expense ratios silently reduce your return; low-cost index options often serve well.</li>
</ul>
<h2>Important caveats</h2>
<p>Projections assume a steady average return; real markets deliver that average through sharp swings. Contribution limits apply (set annually by the IRS), and traditional 401(k) withdrawals are taxed as income in retirement, while Roth 401(k) contributions are taxed now and withdrawn tax-free later. Treat the result as a realistic planning estimate, not a promise.</p>
""",
        "faqs": [
            ("How much should I contribute to my 401(k)?", "At minimum, enough to capture the full employer match. Many planners suggest working toward 15% of salary (including the match) for a traditional retirement age; start where you can and increase with raises."),
            ("What return rate is realistic?", "A diversified stock-heavy portfolio has historically averaged around 7–10% before inflation over long periods. Using 6–7% keeps projections conservative; retirees often shift toward lower-return, lower-risk mixes near retirement."),
            ("Traditional or Roth 401(k)?", "Traditional lowers taxes now and is taxed at withdrawal; Roth is taxed now and withdrawn tax-free. Roth often favors those expecting higher future tax rates or with a long horizon; many people split contributions between both."),
        ],
    },
    {
        "slug": "roth-ira-calculator",
        "emoji": "\U0001F4B0",
        "category": "Retirement",
        "title": "Roth IRA Calculator — Tax-Free Retirement Growth",
        "h1": "Roth IRA Calculator",
        "blurb": "Project tax-free Roth IRA growth from regular contributions.",
        "meta_description": "Project the tax-free value of a Roth IRA from annual contributions and expected returns, and see how much of the balance is growth you'll never pay tax on.",
        "intro": "A Roth IRA's superpower is that qualified withdrawals in retirement are completely tax-free — including all the growth. Enter your contributions and expected return to see the balance you could build, and how much of it is untaxed gains.",
        "fields": [
            {"id": "balance", "label": "Current Roth balance ($)", "value": 5000},
            {"id": "annual", "label": "Annual contribution ($)", "value": 7000, "hint": "2024 limit is $7,000 under age 50"},
            {"id": "rate", "label": "Expected annual return (%)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Years of contributing", "value": 30, "step": 1},
        ],
        "js": """
function calculate() {
  const P = val('balance'), c = val('annual'), r = val('rate')/100, y = val('years');
  const i = r/12, n = y*12, pmt = c/12, growth = Math.pow(1+i,n);
  const fv = P*growth + (i>0 ? pmt*(growth-1)/i : pmt*n);
  const contributed = P + c*y;
  const gains = fv - contributed;
  show(`<div class="result-main">$${fmt(fv,0)}<small>Tax-free at retirement after ${y} years</small></div>
  <table>
    <tr><td>Total contributed</td><td>$${fmt(contributed,0)}</td></tr>
    <tr><td>Investment growth (all tax-free)</td><td>$${fmt(gains,0)}</td></tr>
    <tr><td>Growth as share of balance</td><td>${fv>0 ? fmt(gains/fv*100,0) : '—'}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why "tax-free" is such a big deal</h2>
<p>In a Roth IRA you contribute money you've already paid tax on. In exchange, qualified withdrawals in retirement — contributions <em>and</em> all investment growth — come out completely tax-free. Look at the "investment growth" line in your result: over decades, the majority of a Roth balance is typically gains, and in a Roth you never pay a cent of tax on them. In a regular taxable account, those same gains would be taxed.</p>
<h2>Roth vs Traditional in one sentence</h2>
<p>Pay tax now (Roth) or pay tax later (Traditional). Roth wins if you expect to be in the same or a higher tax bracket in retirement — which describes many young savers whose income (and tax rate) will rise. Traditional wins if you're in a high bracket now and expect a lower one later. Splitting contributions hedges the bet.</p>
<h2>Rules worth knowing</h2>
<ul>
<li><strong>Contribution limits</strong> are set annually (e.g. $7,000 in 2024, plus a $1,000 catch-up at 50+). This calculator assumes a constant contribution; adjust as limits rise.</li>
<li><strong>Income limits</strong> can reduce or block direct Roth contributions at higher incomes.</li>
<li><strong>Flexibility:</strong> your <em>contributions</em> (not earnings) can generally be withdrawn anytime without penalty, making the Roth unusually flexible — though raiding it sacrifices the tax-free growth that makes it valuable.</li>
<li><strong>No required withdrawals</strong> during the original owner's lifetime, unlike traditional accounts.</li>
</ul>
<h2>The takeaway</h2>
<p>A Roth IRA is one of the most powerful wealth tools available to ordinary savers precisely because of that tax-free growth line. Maxing it out each year, invested in low-cost diversified funds and left alone for decades, is a quietly spectacular strategy. As always, the projection assumes a steady average return that real markets deliver only in the long run.</p>
""",
        "faqs": [
            ("What's the Roth IRA contribution limit?", "It's set annually. For 2024 it's $7,000 (under 50) or $8,000 (50+). Limits rise over time, so revisit the figure each year and adjust the calculator."),
            ("Are withdrawals really tax-free?", "Qualified withdrawals are — generally once you're 59½ and the account has been open five years. Your own contributions can usually be withdrawn anytime tax- and penalty-free; earnings withdrawn early may be taxed and penalized."),
            ("Roth or Traditional IRA — which is better?", "Roth favors those who expect equal or higher tax rates in retirement (often younger savers). Traditional favors high earners wanting a deduction now. Many people contribute to both to diversify their future tax exposure."),
        ],
    },
]
