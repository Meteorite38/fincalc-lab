# -*- coding: utf-8 -*-
"""Savings & Investing calculators"""

PART1 = [
    {
        "slug": "compound-interest-calculator",
        "emoji": "\U0001F4C8",
        "category": "Savings & Investing",
        "title": "Compound Interest Calculator — See How Your Money Grows",
        "h1": "Compound Interest Calculator",
        "blurb": "Project how savings grow with monthly deposits and compounding.",
        "meta_description": "Free compound interest calculator with monthly contributions. See your future balance, total deposits and interest earned, with the formula explained step by step.",
        "intro": "Enter a starting amount, an optional monthly deposit, an interest rate and a time horizon. The calculator projects your future balance and shows exactly how much of it comes from interest rather than your own deposits.",
        "fields": [
            {"id": "principal", "label": "Starting amount ($)", "value": 10000},
            {"id": "monthly", "label": "Monthly deposit ($)", "value": 200},
            {"id": "rate", "label": "Annual interest rate (%)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Years", "value": 20, "step": 1},
        ],
        "js": """
function calculate() {
  const P = val('principal'), pmt = val('monthly'), r = val('rate') / 100, y = val('years');
  const i = r / 12, n = y * 12;
  const growth = Math.pow(1 + i, n);
  const fv = P * growth + (i > 0 ? pmt * (growth - 1) / i : pmt * n);
  const deposited = P + pmt * n;
  const interest = fv - deposited;
  show(`<div class="result-main">$${fmt(fv)}<small>Projected balance after ${y} years</small></div>
  <table>
    <tr><td>Total you deposited</td><td>$${fmt(deposited)}</td></tr>
    <tr><td>Interest earned</td><td>$${fmt(interest)}</td></tr>
    <tr><td>Interest share of final balance</td><td>${fmt(fv > 0 ? interest / fv * 100 : 0, 1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How compound interest works</h2>
<p>Compound interest means you earn interest not only on the money you deposit, but also on the interest that money has already earned. Each period, the interest is added to your balance, and the next period's interest is calculated on that larger balance. Over short periods the effect is modest; over decades it is dramatic — which is why starting early matters more than starting big.</p>
<h2>The formula this calculator uses</h2>
<p>With monthly compounding and monthly deposits made at the end of each month, the future value is:</p>
<p><code>FV = P·(1+i)<sup>n</sup> + PMT·[((1+i)<sup>n</sup> − 1) / i]</code></p>
<ul>
<li><strong>P</strong> — your starting amount</li>
<li><strong>PMT</strong> — your monthly deposit</li>
<li><strong>i</strong> — the monthly rate (annual rate ÷ 12)</li>
<li><strong>n</strong> — the number of months</li>
</ul>
<h2>A worked example</h2>
<p>Suppose you start with $10,000, add $200 every month, and earn 7% a year for 20 years. Your own deposits total $58,000. The projected balance is roughly $143,000 — meaning around $85,000, well over half of the final amount, is interest you never had to deposit. Run the same numbers over 10 years instead and interest makes up only about a third of the result. Time is the main ingredient.</p>
<h2>Tips for using the result</h2>
<ul>
<li><strong>Use a realistic rate.</strong> A high-yield savings account might pay 4–5%; a diversified stock portfolio has historically averaged around 7–10% before inflation, but with large year-to-year swings.</li>
<li><strong>Think in real terms.</strong> Subtract expected inflation (around 2–3%) from your rate to see growth in today's purchasing power. Our <a href="/calculators/inflation-calculator/">inflation calculator</a> can help.</li>
<li><strong>Consistency beats timing.</strong> The monthly deposit term usually ends up contributing more than the starting lump sum for ordinary savers.</li>
</ul>
""",
        "faqs": [
            ("How often does this calculator compound interest?",
             "Monthly. Deposits are assumed to be made at the end of each month, which is the most common convention for savings calculators. Real accounts may compound daily or annually; the difference is usually small."),
            ("Is the interest rate before or after inflation?",
             "The rate you enter is the nominal rate, before inflation. To estimate growth in today's purchasing power, enter your expected rate minus expected inflation (for example 7% minus 2.5% = 4.5%)."),
            ("Does the calculator account for taxes or fees?",
             "No. Interest, dividends and capital gains may be taxable depending on your country and account type, and funds may charge fees. Treat the result as a gross, pre-tax estimate."),
        ],
    },
    {
        "slug": "savings-goal-calculator",
        "emoji": "\U0001F3AF",
        "category": "Savings & Investing",
        "title": "Savings Goal Calculator — How Much to Save Each Month",
        "h1": "Savings Goal Calculator",
        "blurb": "Find the exact monthly saving needed to hit a target amount.",
        "meta_description": "Work out how much you need to save every month to reach any savings goal, taking interest into account. Free, instant and private.",
        "intro": "Tell the calculator what you are saving for, what you already have, and how long you have. It returns the monthly amount that gets you there, including the help you get from interest along the way.",
        "fields": [
            {"id": "goal", "label": "Savings goal ($)", "value": 30000},
            {"id": "current", "label": "Already saved ($)", "value": 5000},
            {"id": "years", "label": "Time to reach the goal (years)", "value": 5, "step": 0.5},
            {"id": "rate", "label": "Annual interest rate (%)", "value": 4, "step": 0.1},
        ],
        "js": """
function calculate() {
  const goal = val('goal'), P = val('current'), y = val('years'), r = val('rate') / 100;
  const i = r / 12, n = Math.round(y * 12);
  if (n <= 0) { show('<div class="result-main">Please enter a time horizon above zero.</div>'); return; }
  const growth = Math.pow(1 + i, n);
  const fromCurrent = P * growth;
  let msg;
  if (fromCurrent >= goal) {
    msg = `<div class="result-main">$0.00<small>Your current savings alone should reach $${fmt(fromCurrent)} — the goal is already covered.</small></div>`;
  } else {
    const pmt = i > 0 ? (goal - fromCurrent) * i / (growth - 1) : (goal - fromCurrent) / n;
    const deposited = P + pmt * n;
    msg = `<div class="result-main">$${fmt(pmt)} / month<small>Needed to reach $${fmt(goal, 0)} in ${y} years</small></div>
    <table>
      <tr><td>Growth of what you already have</td><td>$${fmt(fromCurrent)}</td></tr>
      <tr><td>Total you will deposit overall</td><td>$${fmt(deposited)}</td></tr>
      <tr><td>Interest doing the rest</td><td>$${fmt(goal - deposited > 0 ? goal - deposited : 0)}</td></tr>
    </table>`;
  }
  show(msg);
}
""",
        "body_html": """
<h2>Why work backwards from the goal?</h2>
<p>Most people save whatever is left at the end of the month — and the amount is usually disappointing. Flipping the question to "how much do I need to put away each month?" turns a vague hope into a concrete, automatable number. Once you know the figure, you can set up an automatic transfer on payday and stop relying on willpower.</p>
<h2>How the math works</h2>
<p>The calculator first grows your existing savings forward: money you already have will compound until the deadline. Whatever gap remains must be covered by monthly deposits, and the required deposit is the annuity payment that future-values to that gap:</p>
<p><code>PMT = (Goal − P·(1+i)<sup>n</sup>) · i / ((1+i)<sup>n</sup> − 1)</code></p>
<p>where <em>i</em> is the monthly rate and <em>n</em> the number of months. If your current savings alone will out-grow the goal, the answer is simply zero.</p>
<h2>A worked example</h2>
<p>You want $30,000 for a house deposit in 5 years, already have $5,000, and your savings account pays 4%. Your $5,000 grows to about $6,100 on its own. The remaining $23,900 gap needs roughly $360 a month. Without any interest you would need about $415 a month — the account is quietly covering the difference.</p>
<h2>Making the number stick</h2>
<ul>
<li><strong>Automate it.</strong> Schedule the transfer for the day after payday, so the goal is funded before spending starts.</li>
<li><strong>Revisit yearly.</strong> Rates change and goals drift. Re-run the calculation once a year and adjust.</li>
<li><strong>Keep goal money separate.</strong> A dedicated account reduces the temptation to raid it, and makes progress visible.</li>
</ul>
""",
        "faqs": [
            ("What interest rate should I use for a short-term goal?",
             "For goals under five years, most people keep the money in cash-like products, so use your actual savings account or money-market rate (often 3–5%). Avoid assuming stock-market returns for money you will need soon."),
            ("What if I can't afford the monthly amount shown?",
             "You have three levers: extend the deadline, lower the goal, or raise the return (which usually means more risk). Even a small extension often reduces the monthly figure noticeably because both time and compounding work for you."),
            ("Does the calculator assume deposits at the start or end of the month?",
             "End of month, the standard convention. If you deposit at the start of each month you will finish slightly ahead of the goal — a pleasant rounding error in your favor."),
        ],
    },
    {
        "slug": "retirement-savings-calculator",
        "emoji": "\U0001F334",
        "category": "Retirement",
        "title": "Retirement Savings Calculator — Will You Have Enough?",
        "h1": "Retirement Savings Calculator",
        "blurb": "Project your nest egg and the income it could support.",
        "meta_description": "Estimate your retirement nest egg from your age, savings and monthly contributions — and see the annual income it could support using the 4% rule.",
        "intro": "Enter your age, what you have saved, and what you add each month. The calculator projects your balance at retirement and translates it into a sustainable annual income using the widely-cited 4% guideline.",
        "fields": [
            {"id": "age", "label": "Current age", "value": 30, "step": 1},
            {"id": "retire", "label": "Planned retirement age", "value": 65, "step": 1},
            {"id": "current", "label": "Current retirement savings ($)", "value": 25000},
            {"id": "monthly", "label": "Monthly contribution ($)", "value": 500},
            {"id": "rate", "label": "Expected annual return (%)", "value": 7, "step": 0.1},
        ],
        "js": """
function calculate() {
  const age = val('age'), retire = val('retire');
  const P = val('current'), pmt = val('monthly'), r = val('rate') / 100;
  const yrs = retire - age;
  if (yrs <= 0) { show('<div class="result-main">Retirement age must be greater than current age.</div>'); return; }
  const i = r / 12, n = yrs * 12, growth = Math.pow(1 + i, n);
  const fv = P * growth + (i > 0 ? pmt * (growth - 1) / i : pmt * n);
  const annual = fv * 0.04;
  show(`<div class="result-main">$${fmt(fv, 0)}<small>Projected nest egg at age ${retire} (${yrs} years of saving)</small></div>
  <table>
    <tr><td>Sustainable annual income (4% rule)</td><td>$${fmt(annual, 0)}</td></tr>
    <tr><td>That is per month</td><td>$${fmt(annual / 12, 0)}</td></tr>
    <tr><td>Total you will contribute</td><td>$${fmt(P + pmt * n, 0)}</td></tr>
    <tr><td>Growth doing the heavy lifting</td><td>$${fmt(fv - P - pmt * n, 0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What this calculator tells you</h2>
<p>Retirement planning boils down to two questions: <em>how big will my pot be?</em> and <em>what income can that pot safely pay me?</em> The first part is a compound-growth projection of your current savings plus monthly contributions. The second uses the "4% rule" — a rule of thumb from the well-known Trinity study suggesting that withdrawing about 4% of your starting balance each year, adjusted for inflation, has historically lasted through a 30-year retirement.</p>
<h2>A worked example</h2>
<p>A 30-year-old with $25,000 saved, contributing $500 a month at a 7% average return, would project to roughly $1.05 million by 65. The 4% guideline turns that into about $42,000 of first-year income, or $3,500 a month — before any state pension or social security is added on top.</p>
<h2>How to read the result honestly</h2>
<ul>
<li><strong>It is a projection, not a promise.</strong> Markets do not deliver smooth 7% years; they deliver −20% and +30% years that average out. The longer your horizon, the more reasonable an average becomes.</li>
<li><strong>Inflation matters.</strong> $1 million in 35 years buys much less than today. For a today's-money view, use a real return (nominal minus ~2.5% inflation) — around 4–5% instead of 7%.</li>
<li><strong>The 4% rule is a starting point.</strong> Retiring earlier than 60, or retiring into a market crash, argues for 3–3.5%; flexibility to cut spending in bad years argues you can afford more.</li>
</ul>
<h2>Levers that move the needle most</h2>
<p>Run the calculator a few times and you will notice a pattern: adding years helps more than adding dollars. Delaying retirement from 60 to 65 often grows the pot by 40–50% because contributions keep flowing in while the largest balance of your life keeps compounding. The second-strongest lever is the contribution rate early in your career — money invested in your 20s and 30s does double or triple duty compared with money invested in your 50s.</p>
""",
        "faqs": [
            ("What rate of return should I assume?",
             "A diversified global stock portfolio has historically returned around 7–10% a year before inflation over long periods. Mixed stock/bond portfolios land lower. Using 6–7% nominal, or 4–5% if you want an inflation-adjusted answer, is a common conservative choice."),
            ("Does this include social security or state pensions?",
             "No. The result is only the income from your own savings. Any state pension, employer pension or annuity income stacks on top of the figure shown, so your total retirement income will typically be higher."),
            ("Is the 4% rule safe?",
             "It is a historical guideline, not a guarantee. It assumed a 30-year retirement and a US stock/bond portfolio. Longer retirements or expensive market conditions at your retirement date may call for a lower withdrawal rate, while flexibility in spending lets many retirees safely take more in good years."),
        ],
    },
    {
        "slug": "investment-return-calculator",
        "emoji": "\U0001F4CA",
        "category": "Savings & Investing",
        "title": "CAGR Calculator — Annualized Investment Return",
        "h1": "Investment Return (CAGR) Calculator",
        "blurb": "Turn a total gain into an honest annualized return.",
        "meta_description": "Calculate the compound annual growth rate (CAGR) of any investment from its starting value, ending value and holding period. Compare investments fairly.",
        "intro": "\"My stock doubled\" means little without knowing how long it took. CAGR — compound annual growth rate — converts any total gain into a per-year rate, so investments held for different periods can be compared on equal footing.",
        "fields": [
            {"id": "initial", "label": "Starting value ($)", "value": 10000},
            {"id": "final", "label": "Ending value ($)", "value": 18000},
            {"id": "years", "label": "Holding period (years)", "value": 6, "step": 0.1},
        ],
        "js": """
function calculate() {
  const a = val('initial'), b = val('final'), y = val('years');
  if (a <= 0 || y <= 0) { show('<div class="result-main">Starting value and years must be above zero.</div>'); return; }
  const total = (b - a) / a * 100;
  const cagr = (Math.pow(b / a, 1 / y) - 1) * 100;
  show(`<div class="result-main">${fmt(cagr)}% / year<small>Compound annual growth rate over ${y} years</small></div>
  <table>
    <tr><td>Total return</td><td>${fmt(total)}%</td></tr>
    <tr><td>Money multiple</td><td>${fmt(b / a)}x</td></tr>
    <tr><td>Rule-of-72 doubling time at this rate</td><td>${cagr > 0 ? fmt(72 / cagr, 1) + ' years' : '—'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What CAGR actually measures</h2>
<p>CAGR answers the question: <em>what steady annual rate would have turned my starting value into my ending value over this period?</em> Real investments never grow steadily, but expressing the messy path as one smooth rate makes results comparable — a 6-year investment against a 3-year one, a stock against a fund, or your own portfolio against an index.</p>
<p><code>CAGR = (Ending ÷ Starting)<sup>1/years</sup> − 1</code></p>
<h2>A worked example</h2>
<p>$10,000 growing to $18,000 over 6 years is an 80% total return. Naively dividing by six suggests "13.3% a year", but that ignores compounding. The true annualized rate is about 10.3% — noticeably lower, because each year's growth builds on the previous year's larger base. This is exactly why sales pitches love quoting total returns and honest analysis prefers CAGR.</p>
<h2>Common uses</h2>
<ul>
<li><strong>Comparing funds or stocks</strong> held over different time spans.</li>
<li><strong>Checking a sales claim.</strong> "We tripled investors' money" over 15 years is a 7.6% CAGR — decent, not spectacular.</li>
<li><strong>Business metrics.</strong> Revenue or user CAGR across multiple years is standard in financial analysis and pitch decks.</li>
</ul>
<h2>Limits worth knowing</h2>
<p>CAGR ignores everything that happened between the two endpoints — volatility, drawdowns, and any deposits or withdrawals along the way. If you added money during the period, CAGR will overstate your skill; for portfolios with cash flows, a money-weighted return (IRR) is the fairer measure. And two investments with the same CAGR can carry very different risk: 10% a year with a smooth ride is not the same experience as 10% with a 50% crash in the middle.</p>
""",
        "faqs": [
            ("What is the difference between CAGR and average annual return?",
             "The arithmetic average of yearly returns overstates growth because it ignores compounding and volatility drag. A portfolio that gains 50% then loses 50% has an average return of 0% but has actually lost 25% of its value. CAGR reflects what really happened to your money."),
            ("Can CAGR be negative?",
             "Yes. If the ending value is below the starting value, CAGR is negative — it is the steady annual rate of decline that produces the observed loss."),
            ("Does CAGR account for deposits and withdrawals?",
             "No. It assumes a single lump sum at the start and no cash flows until the end. If you contributed along the way, use a money-weighted return (IRR/XIRR in a spreadsheet) for an accurate personal return."),
        ],
    },
]
