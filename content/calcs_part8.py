# -*- coding: utf-8 -*-
"""Batch 6 calculators: FIRE number, Coast FIRE, millionaire, future value,
investment fee impact, extra mortgage payment, biweekly mortgage, pay raise,
startup runway, payback period."""

PART8 = [
    {
        "slug": "fire-number-calculator",
        "emoji": "\U0001F525",
        "category": "Retirement",
        "title": "FIRE Number Calculator — How Much to Retire Early",
        "h1": "FIRE Number Calculator",
        "blurb": "Your target nest egg for financial independence.",
        "meta_description": "Calculate your FIRE number — the savings needed for financial independence — from your annual expenses and safe withdrawal rate, plus how many years until you reach it.",
        "intro": "Financial independence means your investments can cover your living costs indefinitely. Enter your annual spending and a safe withdrawal rate to get your FIRE number, then see how long it takes to get there.",
        "fields": [
            {"id": "expenses", "label": "Annual expenses in retirement ($)", "value": 40000},
            {"id": "swr", "label": "Safe withdrawal rate (%)", "value": 4, "step": 0.1, "hint": "4% is the common default"},
            {"id": "current", "label": "Current invested savings ($)", "value": 100000},
            {"id": "monthly", "label": "Monthly contribution ($)", "value": 2000},
            {"id": "rate", "label": "Expected annual return (%)", "value": 7, "step": 0.1},
        ],
        "js": """
function calculate() {
  const exp = val('expenses'), swr = val('swr')/100, P = val('current'), pmt = val('monthly'), r = val('rate')/100/12;
  if (swr <= 0) { show('<div class="result-main">Enter a withdrawal rate above zero.</div>'); return; }
  const fire = exp / swr;
  let rows = `<tr><td>Multiple of expenses</td><td>${fmt(1/swr,1)}x annual spending</td></tr>`;
  if (P >= fire) {
    show(`<div class="result-main">$${fmt(fire,0)}<small>You've already reached financial independence \\u2705</small></div><table>${rows}</table>`);
    return;
  }
  let bal = P, months = 0;
  while (bal < fire && months < 1200) { bal = bal*(1+r) + pmt; months++; }
  const yrs = Math.floor(months/12), mo = months%12;
  rows += `<tr><td>Still needed</td><td>$${fmt(fire - P,0)}</td></tr>
    <tr><td>Time to FIRE</td><td>${months>=1200 ? 'over 100 years — raise savings' : yrs+' years '+mo+' months'}</td></tr>
    <tr><td>Monthly income it funds</td><td>$${fmt(fire*swr/12,0)}</td></tr>`;
  show(`<div class="result-main">$${fmt(fire,0)}<small>Your FIRE number at a ${fmt(swr*100,1)}% withdrawal rate</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>What is a FIRE number?</h2>
<p>FIRE — Financial Independence, Retire Early — is the point where your invested assets are large enough that a safe annual withdrawal covers your living costs forever. The core formula is beautifully simple: <code>FIRE number = annual expenses ÷ safe withdrawal rate</code>. At the common 4% rate that's <strong>25 times your annual spending</strong>. Spend $40,000 a year and you need about $1,000,000.</p>
<h2>Where the 4% comes from</h2>
<p>The 4% rule descends from the Trinity study, which found that withdrawing 4% of a starting portfolio (adjusted for inflation) survived 30 years in almost all historical periods. Early retirees planning for 40–50 year horizons often use a more conservative 3–3.5%, which raises the target to 28–33x expenses. Lower the withdrawal rate in the calculator and watch the FIRE number climb — that's the price of extra safety over a longer retirement.</p>
<h2>Two levers, both powerful</h2>
<ul>
<li><strong>Spending is the master variable.</strong> Because the target is a multiple of expenses, cutting $5,000 of annual spending lowers your FIRE number by $125,000 (at 4%) — and simultaneously frees cash to invest. Frugality works on both sides of the equation.</li>
<li><strong>Savings rate sets the timeline.</strong> The single biggest determinant of <em>how soon</em> you reach FIRE is the percentage of income you save. A 50% savings rate gets most people there in around 17 years regardless of income level.</li>
</ul>
<h2>Beyond the number</h2>
<p>Reaching your FIRE number gives you options, not obligations — many "retire" into work they actually enjoy. Pair this with our <a href="/calculators/retirement-withdrawal-calculator/">withdrawal calculator</a> to stress-test how long the money lasts, and mind sequence-of-returns risk in the early years. FIRE is less about never working again and more about never <em>having</em> to.</p>
""",
        "faqs": [
            ("How is a FIRE number calculated?", "Divide your expected annual expenses by your safe withdrawal rate. At the common 4% rate, that's 25 times your annual spending. Spending $40,000/year implies a $1,000,000 target."),
            ("Is the 4% rule safe for early retirement?", "It was designed for a 30-year retirement. For the 40–50 year horizons common in early retirement, many use a more conservative 3–3.5%, which raises the target to roughly 28–33x annual expenses."),
            ("What matters more, income or savings rate?", "Savings rate. Because FIRE timing depends on the gap between what you earn and what you spend, a high savings rate reaches independence quickly at almost any income level."),
        ],
    },
    {
        "slug": "coast-fire-calculator",
        "emoji": "\U0001F3C4",
        "category": "Retirement",
        "title": "Coast FIRE Calculator — When You Can Stop Saving",
        "h1": "Coast FIRE Calculator",
        "blurb": "The amount that grows to retirement with no new savings.",
        "meta_description": "Calculate your Coast FIRE number — the amount that, left untouched, grows to fund retirement without further contributions — and whether you've hit it.",
        "intro": "Coast FIRE is the moment your existing investments will grow to fund retirement on their own, even if you never save another dollar. Enter your details to see your Coast FIRE number and whether you've reached it.",
        "fields": [
            {"id": "age", "label": "Current age", "value": 30, "step": 1},
            {"id": "retire", "label": "Traditional retirement age", "value": 65, "step": 1},
            {"id": "target", "label": "Nest egg needed at retirement ($)", "value": 1000000},
            {"id": "current", "label": "Current invested savings ($)", "value": 120000},
            {"id": "rate", "label": "Expected real annual return (%)", "value": 5, "step": 0.1, "hint": "after inflation"},
        ],
        "js": """
function calculate() {
  const age = val('age'), retire = val('retire'), target = val('target'), P = val('current'), r = val('rate')/100;
  const yrs = retire - age;
  if (yrs <= 0) { show('<div class="result-main">Retirement age must be beyond current age.</div>'); return; }
  const coast = target / Math.pow(1+r, yrs);
  const projected = P * Math.pow(1+r, yrs);
  let rows = `<tr><td>Coast FIRE number at age ${age}</td><td>$${fmt(coast,0)}</td></tr>
    <tr><td>Your savings will grow to</td><td>$${fmt(projected,0)}</td></tr>
    <tr><td>Growth years remaining</td><td>${yrs}</td></tr>`;
  if (P >= coast) {
    show(`<div class="result-main">Coast FIRE reached \\u2705<small>Your $${fmt(P,0)} should grow to $${fmt(projected,0)} by ${retire} with no new saving</small></div><table>${rows}</table>`);
  } else {
    rows += `<tr><td>Still needed to coast</td><td>$${fmt(coast - P,0)}</td></tr>`;
    show(`<div class="result-main">$${fmt(coast,0)}<small>Reach this and you can stop saving for retirement</small></div><table>${rows}</table>`);
  }
}
""",
        "body_html": """
<h2>The idea behind Coast FIRE</h2>
<p>Full FIRE means saving enough to live off your investments now. <strong>Coast FIRE</strong> is a gentler milestone: the point where your current portfolio, left alone to compound, will grow into a full retirement nest egg by traditional retirement age — <em>without any further contributions</em>. Once you "coast," you only need to earn enough to cover today's expenses; your retirement is already handled by compounding.</p>
<h2>The math</h2>
<p>Work backwards from your retirement target using compound growth: <code>Coast number = target ÷ (1 + return)<sup>years</sup></code>. A 30-year-old wanting $1,000,000 at 65, assuming a 5% real return, needs only about $181,000 invested today to coast. That figure is far smaller than the final target because 35 years of compounding does the heavy lifting.</p>
<h2>Why it's liberating</h2>
<ul>
<li><strong>It reframes the finish line.</strong> Reaching Coast FIRE early (often in your 30s) means you can downshift to lower-paying but more enjoyable work, take career risks, or go part-time — because you no longer <em>need</em> to save for old age.</li>
<li><strong>It rewards starting young.</strong> The earlier you front-load savings, the longer compounding runs and the smaller your coast number. This is the strongest possible argument for investing aggressively in your 20s.</li>
<li><strong>Use real returns.</strong> Because the target is in future dollars, use an inflation-adjusted (real) return like 5% rather than a nominal 7–8%, so the answer stays in today's purchasing power.</li>
</ul>
<p>Coast FIRE pairs naturally with the <a href="/calculators/fire-number-calculator/">full FIRE number calculator</a>: reach Coast FIRE first, then decide whether to keep pushing for full independence or simply enjoy the freedom of no longer having to save.</p>
""",
        "faqs": [
            ("What is Coast FIRE?", "The point where your current investments will grow to fund retirement by themselves, with no further contributions. After reaching it, you only need to earn enough to cover current expenses."),
            ("How is the Coast FIRE number calculated?", "Divide your retirement target by (1 + expected real return) raised to the number of years until retirement. It's the present value today that compounds into your goal."),
            ("Should I use nominal or real returns?", "Real (inflation-adjusted) returns, since your retirement target is a future amount. Using a real return like 5% keeps the answer expressed in today's purchasing power."),
        ],
    },
    {
        "slug": "millionaire-calculator",
        "emoji": "\U0001F4B0",
        "category": "Savings & Investing",
        "title": "Millionaire Calculator — How Long to Save $1 Million",
        "h1": "Millionaire Calculator",
        "blurb": "Years to reach $1,000,000 (or any target).",
        "meta_description": "Find out how long it takes to become a millionaire based on your current savings, monthly contributions and expected return — or set any savings target.",
        "intro": "How long until you hit seven figures? Enter what you have, what you add each month, and your expected return to see how many years to reach $1,000,000 — or any target you choose.",
        "fields": [
            {"id": "target", "label": "Target amount ($)", "value": 1000000},
            {"id": "current", "label": "Current savings ($)", "value": 25000},
            {"id": "monthly", "label": "Monthly contribution ($)", "value": 1000},
            {"id": "rate", "label": "Expected annual return (%)", "value": 8, "step": 0.1},
        ],
        "js": """
function calculate() {
  const target = val('target'), P = val('current'), pmt = val('monthly'), r = val('rate')/100/12;
  if (P >= target) { show(`<div class="result-main">Already there \\u2705<small>Your savings already exceed $${fmt(target,0)}</small></div>`); return; }
  let bal = P, months = 0, contributed = P;
  while (bal < target && months < 1200) { bal = bal*(1+r) + pmt; contributed += pmt; months++; }
  if (months >= 1200) { show('<div class="result-main">Over 100 years<small>Increase your contribution or return to reach the goal sooner</small></div>'); return; }
  const yrs = Math.floor(months/12), mo = months%12;
  show(`<div class="result-main">${yrs} years ${mo} months<small>to reach $${fmt(target,0)}</small></div>
  <table>
    <tr><td>You will have contributed</td><td>$${fmt(contributed,0)}</td></tr>
    <tr><td>Growth (interest earned)</td><td>$${fmt(target - contributed,0)}</td></tr>
    <tr><td>Growth as share of total</td><td>${fmt((target-contributed)/target*100,0)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The path to a million</h2>
<p>Becoming a millionaire is far less about a big income and far more about time, consistency, and compound growth. This calculator simulates your balance month by month until it hits your target. Try it and notice something striking: for most realistic scenarios, a large chunk of the final million is <strong>growth you never deposited</strong> — the market doing the work while you keep contributing.</p>
<h2>Time is the hidden ingredient</h2>
<p>The relationship between contribution and timeline isn't linear. Someone investing $1,000/month at 8% reaches $1M in about 25–26 years. Doubling to $2,000/month doesn't halve the time — it cuts it to about 19 years — because in the early scenario, compounding contributes more of the total. The lesson: <strong>starting earlier often beats contributing more</strong>, because it gives growth more time to dwarf your deposits.</p>
<h2>Realistic assumptions</h2>
<ul>
<li><strong>Return:</strong> a diversified stock portfolio has historically returned ~7–10% before inflation. Using 7–8% is reasonable; remember real (after-inflation) growth is a few points lower, so tomorrow's million buys less than today's.</li>
<li><strong>Consistency beats timing.</strong> Automatic monthly investing (dollar-cost averaging) removes the temptation to time the market and keeps the compounding streak unbroken.</li>
<li><strong>Fees matter.</strong> A 1% annual fee can delay your millionaire date by years — see our <a href="/calculators/investment-fee-impact-calculator/">investment fee impact calculator</a>.</li>
</ul>
<p>The number isn't magic — a million isn't what it once was — but the exercise reveals the real engine of wealth: modest, automatic, relentless investing over decades.</p>
""",
        "faqs": [
            ("How long does it take to save $1 million?", "It depends on your starting amount, monthly contribution and return. As a rough guide, $1,000/month at 8% reaches $1M in about 25 years; higher contributions or returns shorten that considerably."),
            ("Does starting early really matter that much?", "Enormously. Because compounding grows with time, money invested in your 20s does far more work than the same amount invested in your 40s. Starting earlier often beats contributing more later."),
            ("Is $1 million enough to retire?", "It depends on your spending. At a 4% withdrawal rate, $1M supports about $40,000/year. Use our FIRE number calculator to translate your own expenses into a target."),
        ],
    },
    {
        "slug": "future-value-calculator",
        "emoji": "\U0001F52E",
        "category": "Savings & Investing",
        "title": "Future Value Calculator — What Your Money Will Grow To",
        "h1": "Future Value Calculator",
        "blurb": "Grow a lump sum plus deposits to a future value.",
        "meta_description": "Calculate the future value of a lump sum and regular contributions at a given interest rate and time horizon, with the growth broken out from your deposits.",
        "intro": "Future value tells you what money today, plus any regular additions, will be worth later once it earns interest. Enter a starting amount, optional monthly deposits, a rate and a time horizon.",
        "fields": [
            {"id": "principal", "label": "Present amount ($)", "value": 10000},
            {"id": "monthly", "label": "Monthly deposit ($)", "value": 0},
            {"id": "rate", "label": "Annual interest rate (%)", "value": 6, "step": 0.1},
            {"id": "years", "label": "Years", "value": 15, "step": 1},
        ],
        "js": """
function calculate() {
  const P = val('principal'), pmt = val('monthly'), i = val('rate')/100/12, n = val('years')*12;
  const growth = Math.pow(1+i, n);
  const fv = P*growth + (i>0 ? pmt*(growth-1)/i : pmt*n);
  const deposited = P + pmt*n;
  show(`<div class="result-main">$${fmt(fv,2)}<small>Future value after ${val('years')} years</small></div>
  <table>
    <tr><td>Total deposited</td><td>$${fmt(deposited,0)}</td></tr>
    <tr><td>Interest earned</td><td>$${fmt(fv - deposited,0)}</td></tr>
    <tr><td>Growth multiple</td><td>${fmt(deposited>0 ? fv/deposited : 0,2)}x</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Future value, plainly</h2>
<p>Future value (FV) answers "what will this be worth later?" It's the mirror image of <a href="/calculators/present-value-calculator/">present value</a>, which asks "what is a future amount worth today?" The core relationship for a lump sum is <code>FV = PV × (1 + rate)<sup>periods</sup></code>; add regular contributions and you layer an annuity on top. This calculator handles both at once.</p>
<h2>A worked example</h2>
<p>$10,000 today at 6% for 15 years grows to about $24,000 — more than doubling with no further deposits. Add $200/month and the future value jumps past $80,000, of which roughly $46,000 is your deposits and $34,000 is pure growth. The longer the horizon, the more the growth portion dominates: that crossover, where interest out-earns your contributions, is the whole point of investing early.</p>
<h2>Where you'll use it</h2>
<ul>
<li><strong>Goal planning:</strong> project what a house deposit, education fund, or retirement pot will be worth on a target date.</li>
<li><strong>Comparing options:</strong> FV lets you compare a lump sum today against a stream of future payments on equal footing.</li>
<li><strong>Reality-checking promises:</strong> any "double your money" claim implies a specific rate and time — FV lets you verify whether it's plausible or hype.</li>
</ul>
<h2>One caution: inflation</h2>
<p>Future value is a <em>nominal</em> figure. $80,000 in 15 years won't buy what $80,000 buys today. To see the result in today's purchasing power, use a real (inflation-adjusted) rate — subtract expected inflation from your return before entering it, or run the nominal answer through our <a href="/calculators/inflation-calculator/">inflation calculator</a>.</p>
""",
        "faqs": [
            ("What is future value?", "The value that a present amount, plus any regular contributions, will grow to over time at a given interest rate. It's calculated as present value × (1 + rate) raised to the number of periods, plus the future value of any deposits."),
            ("What's the difference between future and present value?", "Future value projects today's money forward in time; present value discounts a future amount back to today. They're inverse operations using the same interest rate."),
            ("Does future value account for inflation?", "Not by default — it's a nominal figure. To express the result in today's purchasing power, use a real (after-inflation) interest rate instead of the nominal rate."),
        ],
    },
    {
        "slug": "investment-fee-impact-calculator",
        "emoji": "\U0001FAA4",
        "category": "Savings & Investing",
        "title": "Investment Fee Impact Calculator — What Fees Really Cost",
        "h1": "Investment Fee Impact Calculator",
        "blurb": "How much a fund's annual fee costs you over time.",
        "meta_description": "See how much an annual investment fee (expense ratio) really costs over decades — often tens or hundreds of thousands in lost growth. Compare a low-fee vs high-fee fund.",
        "intro": "A 1% fee sounds trivial, but compounded over decades it can quietly consume a huge share of your returns. Enter your investment details and two fee levels to see the true lifetime cost.",
        "fields": [
            {"id": "principal", "label": "Starting amount ($)", "value": 10000},
            {"id": "monthly", "label": "Monthly contribution ($)", "value": 500},
            {"id": "rate", "label": "Gross annual return (%)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Years", "value": 30, "step": 1},
            {"id": "fee1", "label": "Low fee / expense ratio (%)", "value": 0.05, "step": 0.01},
            {"id": "fee2", "label": "High fee / expense ratio (%)", "value": 1.0, "step": 0.01},
        ],
        "js": """
function fv(P, pmt, annual, years) {
  const i = annual/100/12, n = years*12, g = Math.pow(1+i, n);
  return P*g + (i>0 ? pmt*(g-1)/i : pmt*n);
}
function calculate() {
  const P = val('principal'), pmt = val('monthly'), r = val('rate'), y = val('years'), f1 = val('fee1'), f2 = val('fee2');
  const low = fv(P, pmt, r - f1, y);
  const high = fv(P, pmt, r - f2, y);
  const cost = low - high;
  show(`<div class="result-main">$${fmt(cost,0)}<small>Extra cost of the ${fmt(f2,2)}% fee vs ${fmt(f1,2)}% over ${y} years</small></div>
  <table>
    <tr><td>Ending value at ${fmt(f1,2)}% fee</td><td>$${fmt(low,0)}</td></tr>
    <tr><td>Ending value at ${fmt(f2,2)}% fee</td><td>$${fmt(high,0)}</td></tr>
    <tr><td>Lost to the higher fee</td><td>$${fmt(cost,0)} (${fmt(low>0?cost/low*100:0,1)}%)</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why a "small" fee isn't small</h2>
<p>Fund fees (expense ratios) are charged on your <em>entire balance</em> every year, and the money they take can no longer compound. So a 1% fee doesn't cost you 1% — it costs you 1% plus all the growth that 1% would have generated for the rest of your investing life. Over decades, that compounding-in-reverse turns a tiny percentage into a life-changing sum.</p>
<h2>The eye-watering example</h2>
<p>Invest $10,000 plus $500/month for 30 years at a 7% gross return. In a near-free index fund (0.05% fee) you end with roughly $610,000. In an actively managed fund charging 1%, you end with about $505,000. That 0.95% difference quietly cost you around <strong>$105,000 — roughly a fifth of your potential nest egg</strong> — for no guaranteed benefit. This is why fee awareness is one of the highest-return "skills" in personal finance.</p>
<h2>What to watch for</h2>
<ul>
<li><strong>Expense ratios:</strong> broad index funds and ETFs now charge as little as 0.03–0.10%. Actively managed funds often charge 0.5–1.5% and rarely beat the index after fees.</li>
<li><strong>Advisory fees:</strong> a 1% "assets under management" fee stacks <em>on top</em> of fund fees — run both combined through this tool to see the real drag.</li>
<li><strong>Hidden costs:</strong> trading costs, loads (sales charges), and account fees add further drag. Low-cost, broadly diversified index funds sidestep most of them.</li>
</ul>
<p>You can't control the market's returns, but you can control your fees — and this is one of the few financial decisions with a near-guaranteed payoff. Minimizing costs is quietly one of the most reliable ways to end up with more.</p>
""",
        "faqs": [
            ("How much do investment fees really cost?", "Far more than the headline percentage, because fees are charged annually on your whole balance and rob you of future compounding. A 1% fee versus a 0.05% fee can cost 15–25% of your final balance over several decades."),
            ("What is a good expense ratio?", "For broad index funds, 0.03–0.20% is excellent and widely available. Anything above ~0.5% deserves scrutiny, and actively managed funds charging 1%+ rarely justify the cost after fees."),
            ("Do advisory fees count too?", "Yes. A 1% advisory fee is charged on top of the underlying fund fees, so your total drag might be 1.5% or more. Add both together to see the true long-term impact."),
        ],
    },
    {
        "slug": "extra-mortgage-payment-calculator",
        "emoji": "\U0001F3E1",
        "category": "Loans & Debt",
        "title": "Extra Mortgage Payment Calculator — Save Interest and Years",
        "h1": "Extra Mortgage Payment Calculator",
        "blurb": "How extra payments cut mortgage interest and time.",
        "meta_description": "See how much interest you save and how many years you cut off your mortgage by paying a little extra each month toward principal.",
        "intro": "Adding even a small amount to each mortgage payment can save years and tens of thousands in interest. Enter your loan and an extra monthly amount to see the impact.",
        "fields": [
            {"id": "balance", "label": "Mortgage balance ($)", "value": 300000},
            {"id": "rate", "label": "Interest rate (%)", "value": 6.5, "step": 0.05},
            {"id": "years", "label": "Years remaining", "value": 30, "step": 1},
            {"id": "extra", "label": "Extra monthly payment ($)", "value": 200},
        ],
        "js": """
function payoff(P, i, pmt) {
  if (pmt <= P*i) return null;
  let bal = P, months = 0, interest = 0;
  while (bal > 0 && months < 1200) { const int = bal*i; interest += int; bal = bal + int - pmt; months++; }
  return { months, interest };
}
function calculate() {
  const P = val('balance'), i = val('rate')/100/12, n = val('years')*12, extra = val('extra');
  const base = i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n;
  const b = payoff(P, i, base), f = payoff(P, i, base + extra);
  if (!b || !f) { show('<div class="result-main">Check your inputs.</div>'); return; }
  const monthsSaved = b.months - f.months;
  const yS = Math.floor(monthsSaved/12), mS = monthsSaved%12;
  show(`<div class="result-main">$${fmt(b.interest - f.interest,0)} saved<small>and ${yS}y ${mS}m off your mortgage with +$${fmt(extra,0)}/mo</small></div>
  <table>
    <tr><td>Normal payment</td><td>$${fmt(base)}/mo</td></tr>
    <tr><td>New payment</td><td>$${fmt(base+extra)}/mo</td></tr>
    <tr><td>Interest without extra</td><td>$${fmt(b.interest,0)}</td></tr>
    <tr><td>Interest with extra</td><td>$${fmt(f.interest,0)}</td></tr>
    <tr><td>Payoff time</td><td>${Math.floor(f.months/12)}y ${f.months%12}m (was ${Math.floor(b.months/12)}y ${b.months%12}m)</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why extra principal is so powerful</h2>
<p>A mortgage front-loads interest: in the early years, most of each payment covers interest and only a sliver reduces the balance. Every extra dollar you send goes <strong>entirely to principal</strong>, permanently removing all the future interest that dollar would have accrued. Because the effect compounds over the remaining decades, small extra payments produce outsized savings.</p>
<h2>A concrete example</h2>
<p>On a $300,000 mortgage at 6.5% over 30 years, the normal payment is about $1,896. Add just $200/month and you'll pay the loan off roughly <strong>6 years early and save over $100,000 in interest</strong>. The extra $200 isn't earning a return in the usual sense — it's guaranteeing you avoid 6.5% interest, a risk-free return most investments can't promise.</p>
<h2>Ways to add extra</h2>
<ul>
<li><strong>Fixed monthly extra</strong> (this calculator) — simplest and easiest to automate.</li>
<li><strong>Biweekly payments</strong> — paying half the payment every two weeks sneaks in one extra full payment per year; see our <a href="/calculators/biweekly-mortgage-calculator/">biweekly mortgage calculator</a>.</li>
<li><strong>Lump sums</strong> — applying tax refunds or bonuses directly to principal.</li>
</ul>
<h2>Should you? The trade-off</h2>
<p>Prepaying a mortgage is a guaranteed return equal to your rate — compelling when rates are high. But weigh it against alternatives: capture any employer retirement match first, clear higher-rate debt (credit cards) before the mortgage, and keep an emergency fund, since money sent to the mortgage is hard to get back. Confirm your lender applies extra payments to principal, and check for any (rare) prepayment penalty.</p>
""",
        "faqs": [
            ("How much can extra mortgage payments save?", "Often tens of thousands in interest and several years off the loan. On a typical 30-year mortgage, an extra $200/month can save 5–7 years and $100,000+ in interest, depending on the rate and balance."),
            ("Is it better to pay extra on the mortgage or invest?", "It depends on your mortgage rate versus expected after-tax investment returns. Paying down a mortgage is a guaranteed return equal to the rate; investing may earn more but with risk. Clear higher-rate debt and capture retirement matches first."),
            ("Do I need to tell my lender the extra is for principal?", "Yes — specify that extra amounts go toward principal, or some servicers apply them to future payments instead, which doesn't shorten the loan. Also confirm there's no prepayment penalty."),
        ],
    },
    {
        "slug": "biweekly-mortgage-calculator",
        "emoji": "\U0001F5D3\uFE0F",
        "category": "Loans & Debt",
        "title": "Biweekly Mortgage Calculator — Pay Off Your Home Sooner",
        "h1": "Biweekly Mortgage Calculator",
        "blurb": "How biweekly payments shorten your mortgage.",
        "meta_description": "See how switching to biweekly mortgage payments sneaks in one extra payment a year, cutting years off your loan and saving thousands in interest.",
        "intro": "Paying half your mortgage every two weeks results in 26 half-payments — one extra full payment each year — without feeling it. See how much time and interest that saves.",
        "fields": [
            {"id": "balance", "label": "Mortgage balance ($)", "value": 300000},
            {"id": "rate", "label": "Interest rate (%)", "value": 6.5, "step": 0.05},
            {"id": "years", "label": "Loan term (years)", "value": 30, "step": 1},
        ],
        "js": """
function payoff(P, i, pmt) {
  if (pmt <= P*i) return null;
  let bal = P, months = 0, interest = 0;
  while (bal > 0 && months < 1200) { const int = bal*i; interest += int; bal = bal + int - pmt; months++; }
  return { months, interest };
}
function calculate() {
  const P = val('balance'), i = val('rate')/100/12, n = val('years')*12;
  const monthly = i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n;
  const base = payoff(P, i, monthly);
  const extraMonthly = monthly / 12;  // one extra payment/year spread across 12 months
  const bw = payoff(P, i, monthly + extraMonthly);
  if (!base || !bw) { show('<div class="result-main">Check your inputs.</div>'); return; }
  const saved = base.months - bw.months;
  show(`<div class="result-main">${Math.floor(saved/12)}y ${saved%12}m sooner<small>and $${fmt(base.interest - bw.interest,0)} interest saved with biweekly payments</small></div>
  <table>
    <tr><td>Monthly payment</td><td>$${fmt(monthly)}</td></tr>
    <tr><td>Biweekly payment (half)</td><td>$${fmt(monthly/2)} every 2 weeks</td></tr>
    <tr><td>Effective extra per year</td><td>$${fmt(monthly,0)} (one payment)</td></tr>
    <tr><td>Payoff: monthly vs biweekly</td><td>${Math.floor(base.months/12)}y vs ${Math.floor(bw.months/12)}y ${bw.months%12}m</td></tr>
    <tr><td>Total interest saved</td><td>$${fmt(base.interest - bw.interest,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The trick behind biweekly payments</h2>
<p>There are 52 weeks in a year, so paying <strong>half your mortgage payment every two weeks</strong> means 26 half-payments — equal to 13 full monthly payments instead of 12. That one extra payment per year goes straight to principal, and because it happens every year, it quietly shaves years off a 30-year loan and saves a large amount of interest. The clever part: split into biweekly chunks, the extra payment barely registers in your budget.</p>
<h2>How much it saves</h2>
<p>On a $300,000 mortgage at 6.5% over 30 years, switching to biweekly payments pays the loan off roughly <strong>4–5 years early</strong> and saves tens of thousands in interest — purely from timing, without consciously "finding" extra money. This calculator models the effect by adding one extra monthly payment per year to the schedule.</p>
<h2>Important cautions</h2>
<ul>
<li><strong>Beware paid "biweekly programs."</strong> Some lenders or third parties charge setup and per-payment fees to administer this. Don't pay for it — the identical result comes free from simply adding 1/12 of a payment to your monthly amount, or making one extra payment yourself each year.</li>
<li><strong>Confirm principal application.</strong> The savings only materialize if the extra goes to principal and the lender actually credits payments biweekly rather than holding them.</li>
<li><strong>Same math, your control.</strong> If your lender won't do true biweekly for free, use our <a href="/calculators/extra-mortgage-payment-calculator/">extra payment calculator</a> and add the equivalent amount monthly — you keep full control and pay no fees.</li>
</ul>
<p>Biweekly payments are a painless behavioral hack: same money, better timing, meaningfully faster freedom from your mortgage.</p>
""",
        "faqs": [
            ("How do biweekly mortgage payments work?", "You pay half your monthly payment every two weeks. Since there are 26 two-week periods a year, you make the equivalent of 13 monthly payments instead of 12 — one extra payment annually, applied to principal."),
            ("How much do biweekly payments save?", "Typically 4–6 years and tens of thousands in interest on a 30-year mortgage, depending on the rate and balance, all from the single extra payment each year going to principal."),
            ("Should I pay for a biweekly payment program?", "No. Lenders or third parties sometimes charge fees to set this up, but you can achieve the same result for free by adding 1/12 of a payment to your monthly amount or making one extra payment yourself each year."),
        ],
    },
    {
        "slug": "pay-raise-calculator",
        "emoji": "\U0001F4C8",
        "category": "Income & Budgeting",
        "title": "Pay Raise Calculator — New Salary After a Percentage Raise",
        "h1": "Pay Raise Calculator",
        "blurb": "New pay after a raise, and if it beats inflation.",
        "meta_description": "Calculate your new salary after a percentage or flat raise, the extra per paycheck, and whether the raise actually beats inflation in real terms.",
        "intro": "See what a raise really means: your new salary, the increase per month, and — crucially — whether it's a real raise or just keeping up with inflation.",
        "fields": [
            {"id": "salary", "label": "Current annual salary ($)", "value": 60000},
            {"id": "raisepct", "label": "Raise (%)", "value": 4, "step": 0.1},
            {"id": "raiseflat", "label": "Or flat raise amount ($, optional)", "value": 0},
            {"id": "inflation", "label": "Current inflation rate (%)", "value": 3, "step": 0.1},
        ],
        "js": """
function calculate() {
  const s = val('salary'), pct = val('raisepct')/100, flat = val('raiseflat'), inf = val('inflation')/100;
  const increase = flat > 0 ? flat : s*pct;
  const newSalary = s + increase;
  const effPct = s>0 ? increase/s*100 : 0;
  const realPct = effPct - inf*100;
  show(`<div class="result-main">$${fmt(newSalary,0)}<small>New salary — up $${fmt(increase,0)} (${fmt(effPct,1)}%)</small></div>
  <table>
    <tr><td>Extra per month (gross)</td><td>$${fmt(increase/12,0)}</td></tr>
    <tr><td>Extra per paycheck (biweekly)</td><td>$${fmt(increase/26,0)}</td></tr>
    <tr><td>Raise vs inflation (${fmt(inf*100,1)}%)</td><td>${realPct>=0 ? '+' : ''}${fmt(realPct,1)}% real</td></tr>
    <tr><td>Verdict</td><td>${realPct>=0 ? 'A real raise \\u2705' : 'Below inflation — a real-terms pay cut'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What a raise is really worth</h2>
<p>A raise has two numbers: the headline increase, and the part that actually improves your life after inflation. This calculator shows both. Enter a percentage or a flat dollar amount, and it computes your new salary, the extra per paycheck, and the <strong>real</strong> raise — what's left once inflation is subtracted.</p>
<h2>The inflation reality check</h2>
<p>If you get a 3% raise while inflation runs 3%, your salary rose but your <em>purchasing power</em> didn't move — you're running to stand still. A 2% raise during 4% inflation is actually a real-terms pay cut of about 2%, even though your paycheck grew. This is the single most important lens for evaluating a raise, and the one most people skip. A "raise" that trails inflation is management giving you less while sounding generous.</p>
<h2>Using it in negotiations</h2>
<ul>
<li><strong>Anchor to real terms.</strong> Frame requests around beating inflation plus rewarding your added value — "a 3% cost-of-living adjustment plus 4% for my expanded role."</li>
<li><strong>Compounding careers:</strong> raises build on each other. Negotiating an extra 2% today lifts every future raise and bonus that's calculated as a percentage of salary — worth far more than 2% over a career.</li>
<li><strong>Total comp:</strong> remember bonuses, equity, retirement matching and benefits; a modest base raise with a better match can beat a bigger raise alone.</li>
</ul>
<p>Whether you're evaluating an offer or preparing to ask, translating the percentage into real, after-inflation terms turns a vague "is this good?" into a clear answer.</p>
""",
        "faqs": [
            ("How do I calculate my new salary after a raise?", "Multiply your current salary by the raise percentage and add it to your salary — or add a flat raise amount directly. A 4% raise on $60,000 adds $2,400, for a new salary of $62,400."),
            ("What is a 'real' raise?", "Your raise percentage minus inflation. If you get 4% while inflation is 3%, your real raise is about 1% — that's the actual gain in purchasing power. A raise below inflation is a real-terms pay cut."),
            ("Why does negotiating a small extra percentage matter so much?", "Because future raises, bonuses and retirement matches are often calculated as a percentage of salary, a higher base compounds over your entire career — making a small increase today worth far more over time."),
        ],
    },
    {
        "slug": "startup-runway-calculator",
        "emoji": "\U0001F680",
        "category": "Business",
        "title": "Startup Runway Calculator — How Many Months of Cash Left",
        "h1": "Startup Runway Calculator",
        "blurb": "Months of cash left from burn rate and balance.",
        "meta_description": "Calculate your startup's runway in months from cash on hand, monthly revenue and expenses — plus the revenue needed to reach break-even.",
        "intro": "Runway is how long your startup survives at the current burn rate. Enter your cash, monthly revenue and monthly costs to see how many months you have and what it takes to reach break-even.",
        "fields": [
            {"id": "cash", "label": "Cash in the bank ($)", "value": 200000},
            {"id": "revenue", "label": "Monthly revenue ($)", "value": 15000},
            {"id": "expenses", "label": "Monthly expenses ($)", "value": 45000},
            {"id": "growth", "label": "Monthly revenue growth (%)", "value": 8, "step": 0.5},
        ],
        "js": """
function calculate() {
  const cash = val('cash'), rev0 = val('revenue'), exp = val('expenses'), g = val('growth')/100;
  const burn = exp - rev0;
  if (burn <= 0) { show(`<div class="result-main">Profitable now \\u2705<small>Revenue already covers expenses — net $${fmt(rev0-exp,0)}/mo</small></div>`); return; }
  const flatRunway = cash / burn;
  // simulate with growth
  let bal = cash, rev = rev0, months = 0, breakeven = null;
  while (bal > 0 && months < 600) {
    if (rev >= exp) { breakeven = months; break; }
    bal += rev - exp; rev *= (1+g); months++;
    if (bal <= 0) break;
  }
  let rows = `<tr><td>Monthly burn (now)</td><td>$${fmt(burn,0)}</td></tr>
    <tr><td>Flat runway (no growth)</td><td>${fmt(flatRunway,1)} months</td></tr>`;
  if (breakeven !== null) {
    rows += `<tr><td>Break-even reached in</td><td>${breakeven} months (if cash lasts)</td></tr>`;
  } else {
    rows += `<tr><td>Break-even</td><td>Not reached before cash runs out</td></tr>`;
  }
  rows += `<tr><td>Revenue needed to break even</td><td>$${fmt(exp,0)}/mo (${fmt(rev0>0?exp/rev0:0,1)}x current)</td></tr>`;
  const label = breakeven !== null && months >= breakeven ? 'reach profitability' : 'runway at current burn';
  show(`<div class="result-main">${fmt(flatRunway,1)} months<small>of cash at the current burn rate</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>Runway: the number that governs everything</h2>
<p>Runway is how many months your company can operate before the cash runs out. The basic formula is <code>runway = cash ÷ monthly burn</code>, where burn is expenses minus revenue. It's the most important number for any pre-profit startup because it dictates your deadline: raise more money, reach profitability, or wind down — all before runway hits zero.</p>
<h2>Burn rate, gross vs net</h2>
<p><strong>Gross burn</strong> is total monthly spend; <strong>net burn</strong> is spend minus revenue — the true rate your bank balance falls. A company spending $45,000 with $15,000 of revenue has a net burn of $30,000; with $200,000 in the bank, that's a flat runway of about 6.7 months. Revenue growth extends this, which is why the calculator also simulates growing revenue toward break-even.</p>
<h2>The 18-month rule of thumb</h2>
<ul>
<li><strong>Raise for ~18 months.</strong> A common target is enough cash to run 18 months: roughly 12 to hit the next milestone and 6 to raise the next round. Under ~6 months of runway, you're in the danger zone where fundraising leverage collapses.</li>
<li><strong>Growth changes the math.</strong> If revenue is climbing fast enough to reach break-even before cash runs out, you may never need another raise — the ideal outcome. If not, you're racing a clock.</li>
<li><strong>Cutting burn buys time asymmetrically.</strong> Reducing burn extends runway immediately and permanently; it's usually faster and more certain than hoping revenue spikes.</li>
</ul>
<h2>Watch the trend, not just the number</h2>
<p>Track runway monthly. A stable or lengthening runway means growth is outpacing spend; a shrinking one is an early warning long before the crisis. Pair this with a <a href="/calculators/break-even-point-calculator/">break-even analysis</a> to know exactly how much revenue turns the burn positive.</p>
""",
        "faqs": [
            ("How is startup runway calculated?", "Divide your cash on hand by your net monthly burn (expenses minus revenue). $200,000 in cash with a $30,000 net burn gives about 6.7 months of runway at the current rate."),
            ("What is a healthy amount of runway?", "Many investors suggest raising enough for about 18 months — roughly a year to hit your next milestone plus six months to close the next round. Under six months, fundraising leverage weakens sharply."),
            ("What's the difference between gross and net burn?", "Gross burn is your total monthly spending; net burn subtracts revenue, showing how fast your cash balance actually declines. Net burn is the figure that determines runway."),
        ],
    },
    {
        "slug": "payback-period-calculator",
        "emoji": "\u23F3",
        "category": "Business",
        "title": "Payback Period Calculator — How Fast an Investment Pays Back",
        "h1": "Payback Period Calculator",
        "blurb": "Time for an investment to recoup its cost.",
        "meta_description": "Calculate the payback period — how long it takes for an investment's cash inflows to recover its initial cost — plus a simple ROI on the full holding period.",
        "intro": "The payback period is how long an investment takes to earn back its cost. Enter the upfront cost and the cash it returns each period to see when you break even.",
        "fields": [
            {"id": "cost", "label": "Initial investment ($)", "value": 50000},
            {"id": "cashflow", "label": "Cash returned per year ($)", "value": 15000},
            {"id": "life", "label": "Investment lifespan (years)", "value": 6, "step": 1},
        ],
        "js": """
function calculate() {
  const cost = val('cost'), cf = val('cashflow'), life = val('life');
  if (cf <= 0) { show('<div class="result-main">Annual cash flow must be above zero.</div>'); return; }
  const payback = cost / cf;
  const totalReturn = cf * life;
  const netProfit = totalReturn - cost;
  const roi = cost>0 ? netProfit/cost*100 : 0;
  let verdict;
  if (payback > life) verdict = 'Never pays back within its lifespan \\u26A0\\uFE0F';
  else if (payback <= life/2) verdict = 'Fast payback — attractive';
  else verdict = 'Pays back, but late in its life';
  show(`<div class="result-main">${fmt(payback,1)} years<small>to recover the $${fmt(cost,0)} investment</small></div>
  <table>
    <tr><td>Payback in months</td><td>${fmt(payback*12,0)} months</td></tr>
    <tr><td>Total cash over ${life} years</td><td>$${fmt(totalReturn,0)}</td></tr>
    <tr><td>Net profit over lifespan</td><td>$${fmt(netProfit,0)}</td></tr>
    <tr><td>Total ROI</td><td>${fmt(roi,0)}%</td></tr>
    <tr><td>Verdict</td><td>${verdict}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What the payback period tells you</h2>
<p>The payback period is the time it takes for an investment's cash returns to recover its upfront cost: <code>payback = initial cost ÷ annual cash flow</code>. A $50,000 machine that generates $15,000 a year pays back in about 3.3 years. It's the simplest, most intuitive investment metric — a direct answer to "how long until I get my money back?" — which is why business owners and individuals reach for it first.</p>
<h2>Why shorter is safer</h2>
<p>A shorter payback means less time your capital is at risk and sooner it's free to redeploy. Two investments returning the same total can differ sharply in risk: one that pays back in 2 years is far safer than one taking 6, because the future is uncertain and money recovered sooner can be reinvested. Many businesses set a maximum acceptable payback (say 3 years) as a quick screening rule before deeper analysis.</p>
<h2>The metric's blind spots</h2>
<ul>
<li><strong>It ignores everything after payback.</strong> An investment that pays back in 4 years then gushes cash for 20 more looks worse, by payback alone, than one that pays back in 3 years and immediately dies. Always consider total lifetime return too — this calculator shows both.</li>
<li><strong>It ignores the time value of money.</strong> Simple payback treats a dollar in year 5 as equal to a dollar today. For big or long-dated decisions, discounted methods like <a href="/calculators/present-value-calculator/">present value</a> or net present value give a truer picture.</li>
<li><strong>It assumes steady cash flows.</strong> Real returns are lumpy; use it as a first-pass screen, not the final word.</li>
</ul>
<p>Use payback period as a fast, honest gut check — then confirm big decisions with ROI over the full lifespan and, where the stakes justify it, a discounted-cash-flow analysis.</p>
""",
        "faqs": [
            ("How do you calculate payback period?", "Divide the initial investment by the annual cash flow it produces. A $50,000 investment returning $15,000 a year has a payback period of about 3.3 years."),
            ("Is a shorter payback period better?", "Generally yes — it means your money is at risk for less time and is recovered sooner to reinvest. But payback ignores returns after break-even, so also weigh the total lifetime return."),
            ("What are the limitations of payback period?", "It ignores cash flows after the payback point and the time value of money, and assumes steady returns. Use it as a quick screen, then confirm major decisions with ROI and discounted-cash-flow methods like NPV."),
        ],
    },
]
