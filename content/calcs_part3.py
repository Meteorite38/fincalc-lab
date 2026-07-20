# -*- coding: utf-8 -*-
"""Income & Budgeting + Business calculators"""

PART3 = [
    {
        "slug": "salary-to-hourly-calculator",
        "emoji": "\U0001F4B0",
        "category": "Salary & Work",
        "title": "Salary to Hourly Calculator — What You Really Earn Per Hour",
        "h1": "Salary to Hourly Calculator",
        "blurb": "Convert annual salary to hourly, weekly and monthly pay.",
        "meta_description": "Convert an annual salary into hourly, weekly and monthly pay — including an honest hourly rate that counts overtime and commuting time.",
        "intro": "Convert a salary into its hourly equivalent — and, more interestingly, into your \"true\" hourly rate once unpaid overtime and commuting are counted. The second number is the one worth negotiating over.",
        "fields": [
            {"id": "salary", "label": "Annual salary ($)", "value": 65000},
            {"id": "hours", "label": "Official hours per week", "value": 40, "step": 0.5},
            {"id": "weeks", "label": "Working weeks per year", "value": 50, "step": 1, "hint": "52 minus vacation"},
            {"id": "extra", "label": "Unpaid extra hours per week (overtime + commute)", "value": 7, "step": 0.5},
        ],
        "js": """
function calculate() {
  const s = val('salary'), h = val('hours'), w = val('weeks'), e = val('extra');
  if (h <= 0 || w <= 0) { show('<div class="result-main">Hours and weeks must be above zero.</div>'); return; }
  const hourly = s / (h * w);
  const trueHourly = s / ((h + e) * w);
  show(`<div class="result-main">$${fmt(hourly)} / hour<small>Official rate at ${h} hours, ${w} weeks a year</small></div>
  <table>
    <tr><td>Monthly (gross)</td><td>$${fmt(s / 12)}</td></tr>
    <tr><td>Weekly (gross)</td><td>$${fmt(s / w)}</td></tr>
    <tr><td>True hourly incl. ${fmt(e, 1)} unpaid hours/week</td><td>$${fmt(trueHourly)}</td></tr>
    <tr><td>Pay cut hidden in those unpaid hours</td><td>${fmt((1 - trueHourly / hourly) * 100, 1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The basic conversion</h2>
<p>Hourly rate = salary ÷ (hours per week × weeks per year). A $65,000 salary at 40 hours and 50 working weeks is $32.50 an hour. Quick rule of thumb for US-style 2,000-hour years: hourly ≈ salary ÷ 2,000, so every $2,000 of salary is about $1 an hour.</p>
<h2>Why the "true hourly rate" matters more</h2>
<p>Salaried work quietly absorbs time that hourly work bills for: staying late, answering evening messages, commuting. Add a typical 7 unpaid hours a week to the example above and the true rate drops to about $27.70 — a 15% invisible pay cut. This number is the honest basis for comparing a salaried offer against contract work, a job closer to home, or remote work.</p>
<h2>Using it in decisions</h2>
<ul>
<li><strong>Comparing offers:</strong> a $70,000 job with a 90-minute round-trip commute can pay a lower true rate than $63,000 within walking distance.</li>
<li><strong>Freelance pricing:</strong> to match a salary, a contractor typically needs 1.3–1.5× the equivalent hourly rate to cover self-employment taxes, insurance and unpaid gaps between projects.</li>
<li><strong>Overtime culture:</strong> if the unpaid-hours field is uncomfortable to fill honestly, that is information too.</li>
</ul>
""",
        "faqs": [
            ("Is this before or after tax?",
             "Before tax. Take-home pay depends on your country, state and deductions; gross figures are the standard basis for comparing jobs and rates."),
            ("How many working weeks should I use?",
             "52 minus your vacation and public holidays. In the US, 50 is typical (two weeks off); in much of Europe 46–47 reflects five to six weeks of leave."),
            ("Does the calculator handle part-time work?",
             "Yes — just set your actual weekly hours. The math is identical; only the inputs change."),
        ],
    },
    {
        "slug": "take-home-pay-calculator",
        "emoji": "\U0001F9FE",
        "category": "Salary & Work",
        "title": "Take-Home Pay Estimator — From Gross to Net Salary",
        "h1": "Take-Home Pay Estimator",
        "blurb": "Estimate net monthly pay from gross salary and tax rates.",
        "meta_description": "Estimate your net take-home pay from gross salary using your effective tax rate and deductions. Understand the difference between marginal and effective tax rates.",
        "intro": "Enter your gross salary and the percentages taken by tax and other deductions. The calculator shows monthly take-home pay. Because tax systems vary by country and personal situation, this is a transparent estimator you control — not a black box claiming false precision.",
        "fields": [
            {"id": "gross", "label": "Gross annual salary ($)", "value": 70000},
            {"id": "taxrate", "label": "Effective income tax rate (%)", "value": 18, "step": 0.5, "hint": "total tax \u00f7 income, not your top bracket"},
            {"id": "social", "label": "Social security / pension contributions (%)", "value": 8, "step": 0.5},
            {"id": "other", "label": "Other deductions ($/month)", "value": 150, "hint": "health premiums, union dues, etc."},
        ],
        "js": """
function calculate() {
  const g = val('gross'), t = val('taxrate') / 100, s = val('social') / 100, o = val('other');
  const netAnnual = g * (1 - t - s) - o * 12;
  if (netAnnual < 0) { show('<div class="result-main">Deductions exceed the salary — check the percentages.</div>'); return; }
  show(`<div class="result-main">$${fmt(netAnnual / 12)} / month<small>Estimated take-home pay</small></div>
  <table>
    <tr><td>Gross monthly</td><td>$${fmt(g / 12)}</td></tr>
    <tr><td>Income tax</td><td>\u2212$${fmt(g * t / 12)}</td></tr>
    <tr><td>Social contributions</td><td>\u2212$${fmt(g * s / 12)}</td></tr>
    <tr><td>Other deductions</td><td>\u2212$${fmt(o)}</td></tr>
    <tr><td>Share of gross you keep</td><td>${fmt(netAnnual / g * 100, 1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Marginal vs effective tax rate — the classic confusion</h2>
<p>Your <strong>marginal rate</strong> is the tax on your next dollar; your <strong>effective rate</strong> is total tax divided by total income, and it is always lower in a progressive system because early slices of income are taxed lightly or not at all. "I'm in the 24% bracket" does <em>not</em> mean 24% of your salary disappears — a single US filer at $70,000 pays an effective federal rate closer to 13–15%. Use the effective rate here.</p>
<h2>Finding your real numbers</h2>
<ul>
<li><strong>Last year's tax return</strong> is the gold standard: total tax ÷ total income = effective rate.</li>
<li><strong>A recent payslip</strong> works too: identify each deduction line and convert it to a percentage of gross.</li>
<li><strong>Moving or changing jobs?</strong> Look up the destination country's or state's typical burden for your income level, then refine after the first payslip.</li>
</ul>
<h2>What to do with the result</h2>
<p>Budgets built on gross pay fail immediately. Anchor your rent, loan and savings decisions to the net figure. A common allocation for the net amount is 50% needs / 30% wants / 20% savings and debt — see our <a href="/calculators/budget-calculator/">50/30/20 budget calculator</a> to split it automatically.</p>
""",
        "faqs": [
            ("Why not calculate the exact tax for my country?",
             "Exact tax depends on filing status, dependents, deductions, credits and local rules that change yearly. Tools that promise exactness for every reader quietly go stale. This estimator makes the assumptions visible and editable, which is more honest and more portable."),
            ("What effective rate should I guess if I have no history?",
             "Very roughly: US single filers at average incomes often land at 12–20% federal-plus-state; much of Western Europe lands at 25–40% including social charges. Adjust after your first real payslip."),
            ("Are bonuses taxed differently?",
             "They are often withheld at a higher flat rate during the year, but at filing time they are ordinary income in most systems — the effective-rate approach here handles them fine over a full year."),
        ],
    },
    {
        "slug": "budget-calculator",
        "emoji": "\U0001F4B8",
        "category": "Budgeting & Life",
        "title": "50/30/20 Budget Calculator — Needs, Wants, Savings",
        "h1": "50/30/20 Budget Calculator",
        "blurb": "Split your take-home pay into needs, wants and savings.",
        "meta_description": "Apply the 50/30/20 rule to your monthly take-home pay: how much for needs, wants, and savings or debt. Adjustable percentages for your situation.",
        "intro": "The 50/30/20 rule is the most durable budgeting shortcut: 50% of take-home pay for needs, 30% for wants, 20% for savings and extra debt payments. Enter your net income — and adjust the split if your circumstances demand it.",
        "fields": [
            {"id": "income", "label": "Monthly take-home pay ($)", "value": 4500},
            {"id": "needs", "label": "Needs (%)", "value": 50, "step": 1},
            {"id": "wants", "label": "Wants (%)", "value": 30, "step": 1},
            {"id": "save", "label": "Savings & debt (%)", "value": 20, "step": 1},
        ],
        "js": """
function calculate() {
  const inc = val('income'), n = val('needs'), w = val('wants'), s = val('save');
  const total = n + w + s;
  const warn = Math.abs(total - 100) > 0.01 ? `<p style="color:#b45309;font-weight:600">Your percentages add to ${fmt(total, 0)}% — adjust to reach 100%.</p>` : '';
  show(`${warn}<div class="result-main">$${fmt(inc * s / 100)} / month to savings<small>at ${s}% of take-home pay</small></div>
  <table>
    <tr><td>Needs (rent, groceries, utilities, minimum debt payments)</td><td>$${fmt(inc * n / 100)}</td></tr>
    <tr><td>Wants (dining out, subscriptions, travel, hobbies)</td><td>$${fmt(inc * w / 100)}</td></tr>
    <tr><td>Savings &amp; extra debt payments</td><td>$${fmt(inc * s / 100)}</td></tr>
    <tr><td>Savings per year at this rate</td><td>$${fmt(inc * s / 100 * 12, 0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What counts as a need, a want, a saving?</h2>
<p><strong>Needs</strong> are expenses you cannot pause without consequences: housing, utilities, groceries, insurance, transport to work, minimum debt payments. <strong>Wants</strong> are everything you enjoy but could cut in a bad month: restaurants, streaming, travel, upgraded anything. <strong>Savings</strong> covers emergency-fund building, investing, retirement contributions and debt payments beyond the minimum. The honest test for "need vs want": what would you actually do if your income dropped 30% next month?</p>
<h2>When to bend the rule</h2>
<ul>
<li><strong>High-rent cities:</strong> needs may genuinely consume 60%+. Shrink wants first, protect at least 10% savings, and treat the imbalance as a signal about housing cost, not a personal failure.</li>
<li><strong>High incomes:</strong> letting wants scale with income is how six-figure households end up saving nothing. Consider capping wants in dollars and pushing the surplus percentage into savings.</li>
<li><strong>Aggressive goals:</strong> early-retirement savers invert the rule entirely — 50% to savings is common in that community. The framework is a starting grid, not a ceiling.</li>
</ul>
<h2>Making it operational</h2>
<p>Percentages become real when they become transfers. On payday, move the savings share to a separate account automatically, keep needs in the main account, and put wants on a dedicated card or account — when it is empty, wants are done for the month. That single structure replaces most of the discipline budgeting usually demands.</p>
""",
        "faqs": [
            ("Is 50/30/20 based on gross or net income?",
             "Net — your take-home pay after taxes and payroll deductions. If retirement contributions already come out of your paycheck, you can count them toward the 20% and apply the rule to what remains."),
            ("Where do debt payments go?",
             "Minimum required payments are needs — missing them has consequences. Anything you pay above the minimum is building your net worth, so it belongs in the savings category."),
            ("Is 20% savings enough?",
             "It is a solid default for someone starting in their 20s or 30s aiming at a traditional retirement age. Starting later, or aiming earlier, needs more — run our retirement calculator to see what your target actually requires."),
        ],
    },
    {
        "slug": "emergency-fund-calculator",
        "emoji": "\U0001F6DF",
        "category": "Budgeting & Life",
        "title": "Emergency Fund Calculator — Your Target and Timeline",
        "h1": "Emergency Fund Calculator",
        "blurb": "Size your emergency fund and see how long it takes to build.",
        "meta_description": "Calculate how big your emergency fund should be based on your essential expenses and job stability, and how many months it will take to save it.",
        "intro": "An emergency fund is insurance you sell to yourself: cash that turns a job loss or a broken boiler from a crisis into an inconvenience. Enter your essential monthly costs and how much you can save, and get your target and timeline.",
        "fields": [
            {"id": "expenses", "label": "Essential monthly expenses ($)", "value": 2800, "hint": "needs only, not wants"},
            {"id": "months", "label": "Months of coverage", "value": 6, "step": 1, "type": "select",
             "options": [["3", "3 months — dual income, stable jobs"], ["6", "6 months — standard recommendation"], ["9", "9 months — freelance or single income"], ["12", "12 months — very variable income"]]},
            {"id": "saved", "label": "Already saved ($)", "value": 3000},
            {"id": "monthly", "label": "Monthly saving toward the fund ($)", "value": 400},
        ],
        "js": """
function calculate() {
  const exp = val('expenses'), m = val('months'), saved = val('saved'), pmt = val('monthly');
  const target = exp * m;
  const gap = target - saved;
  if (gap <= 0) {
    show(`<div class="result-main">Fully funded \u2705<small>Target $${fmt(target, 0)} — you have $${fmt(saved, 0)}</small></div>`);
    return;
  }
  const t = pmt > 0 ? Math.ceil(gap / pmt) : null;
  show(`<div class="result-main">$${fmt(target, 0)}<small>Your emergency fund target (${m} months × $${fmt(exp, 0)})</small></div>
  <table>
    <tr><td>Still to save</td><td>$${fmt(gap, 0)}</td></tr>
    <tr><td>Current progress</td><td>${fmt(saved / target * 100, 0)}%</td></tr>
    <tr><td>Time to full at $${fmt(pmt, 0)}/month</td><td>${t ? t + ' months (' + fmt(t / 12, 1) + ' years)' : 'set a monthly amount'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How many months do you actually need?</h2>
<p>The classic advice is three to six months of <em>essential</em> expenses. The right number tracks your income risk: a dual-income household of civil servants can hold less; a single-income freelancer in a cyclical industry should hold more. Two questions cut through it: <em>how long would a realistic job search take?</em> and <em>how many people depend on this income?</em></p>
<h2>Essential expenses, not total spending</h2>
<p>Fund the survival version of your life, not the current version: housing, utilities, groceries, insurance, transport, minimum debt payments. Most households find essentials are 60–75% of normal spending. Using total spending inflates the target and delays the moment the fund actually protects you.</p>
<h2>Where to keep it</h2>
<ul>
<li><strong>High-yield savings account</strong> — the default answer: instant access, deposit-insured, currently earning meaningful interest.</li>
<li><strong>Not the stock market</strong> — the one guarantee about emergencies is bad timing; a 30% drawdown the month you lose your job defeats the purpose.</li>
<li><strong>Not your checking account</strong> — visible money gets spent. A separate account at a separate bank adds useful friction.</li>
</ul>
<h2>Building it without stalling other goals</h2>
<p>A practical sequence: save a starter $1,000–$2,000 first (covers most single emergencies), then split spare cash between high-interest debt and the fund until you hit one month of expenses, then grind to the full target. Windfalls — tax refunds, bonuses, side income — are emergency-fund rocket fuel precisely because they were never in the monthly budget.</p>
""",
        "faqs": [
            ("Should I pause investing to build the fund?",
             "Up to your first month of expenses, usually yes — except don't leave employer retirement matching on the table, which is an instant 50–100% return. After a month is banked, running the fund and investing in parallel is reasonable."),
            ("What officially counts as an emergency?",
             "Unexpected, necessary, urgent — job loss, medical bills, essential repairs. A sale is none of the three. Some households write the rules down when calm to remove debate later."),
            ("Should the fund grow over time?",
             "Yes, quietly. Revisit the target when rent rises, a child arrives or income structure changes. A once-a-year check keeps it honest without turning it into a hobby."),
        ],
    },
    {
        "slug": "inflation-calculator",
        "emoji": "\U0001F388",
        "category": "Budgeting & Life",
        "title": "Inflation Calculator — Future Purchasing Power",
        "h1": "Inflation Calculator",
        "blurb": "See what today's money will be worth in the future.",
        "meta_description": "Calculate how inflation erodes purchasing power: what today's amount will be worth in the future, and what future costs today's prices imply.",
        "intro": "Inflation is compound interest working against you. Enter an amount, a rate and a horizon to see what today's money will actually buy in the future — a number every long-term plan should be built on.",
        "fields": [
            {"id": "amount", "label": "Amount today ($)", "value": 50000},
            {"id": "rate", "label": "Expected annual inflation (%)", "value": 2.5, "step": 0.1},
            {"id": "years", "label": "Years", "value": 20, "step": 1},
        ],
        "js": """
function calculate() {
  const a = val('amount'), r = val('rate') / 100, y = val('years');
  const future = a / Math.pow(1 + r, y);
  const needed = a * Math.pow(1 + r, y);
  show(`<div class="result-main">$${fmt(future, 0)}<small>What $${fmt(a, 0)} today will buy in ${y} years at ${fmt(r * 100, 1)}% inflation</small></div>
  <table>
    <tr><td>Purchasing power lost</td><td>${fmt((1 - future / a) * 100, 1)}%</td></tr>
    <tr><td>Amount needed in ${y} years to match today's $${fmt(a, 0)}</td><td>$${fmt(needed, 0)}</td></tr>
    <tr><td>Prices multiply by</td><td>${fmt(needed / a)}x</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The math of shrinking money</h2>
<p>At inflation rate <em>r</em>, the purchasing power of a fixed amount after <em>t</em> years is <code>Value ÷ (1+r)<sup>t</sup></code>. At 2.5% — near many central banks' targets — $50,000 buys only about $30,500 worth of today's goods in 20 years. At 5%, it is roughly $18,800. Small-looking rates compound into large erosion because inflation never takes a year off.</p>
<h2>Why this matters for your plans</h2>
<ul>
<li><strong>Retirement targets:</strong> "I need $1 million" is incomplete without asking <em>in whose dollars?</em> A million in 30 years at 2.5% inflation is about $477,000 today. Plan in real terms or plan twice.</li>
<li><strong>Cash holdings:</strong> money earning 0.1% in a checking account loses purchasing power every single day. The gap between your interest rate and inflation is your real return — often negative for idle cash.</li>
<li><strong>Salary negotiations:</strong> a raise below inflation is a pay cut with better marketing. Anchor negotiations to real, inflation-adjusted terms.</li>
</ul>
<h2>What rate should you assume?</h2>
<p>Most developed-economy central banks target about 2%; the long-run US average since 1926 is a bit above 3%, with violent exceptions (the 1970s, 2021–2023). For planning, 2.5–3% is a defensible baseline, and testing your plan at 4–5% shows how fragile it is to bad decades. The point of the exercise is not prediction — it is making sure your plan survives realistic futures.</p>
""",
        "faqs": [
            ("Is inflation the same for everyone?",
             "No. Official CPI tracks an average basket; your personal rate depends on what you buy. Renters in hot cities, or households with heavy healthcare or education costs, often experience above-headline inflation. Treat CPI as a floor for planning, not gospel."),
            ("How do I protect savings from inflation?",
             "Historically: assets whose income can grow — broad stock indexes, inflation-linked bonds (like TIPS), and property — have outpaced inflation over long horizons, at the cost of volatility. Fixed-rate cash and long fixed-rate bonds are the most exposed."),
            ("Why does the calculator show two numbers?",
             "They answer mirror-image questions: what will today's money be worth later (deflating), and how much will you need later to match today's spending (inflating). Retirement planning mostly needs the second."),
        ],
    },
    {
        "slug": "break-even-point-calculator",
        "emoji": "\u2696\uFE0F",
        "category": "Business & Self-Employment",
        "title": "Break-Even Point Calculator — Units and Revenue to Profit",
        "h1": "Break-Even Point Calculator",
        "blurb": "How many sales cover your costs — the first business question.",
        "meta_description": "Calculate your break-even point in units and revenue from fixed costs, price and variable cost per unit. Includes contribution margin explained.",
        "intro": "Before profit projections and growth plans comes one blunt question: how much do you have to sell just to cover costs? Enter your fixed costs, unit price and unit variable cost to find out.",
        "fields": [
            {"id": "fixed", "label": "Fixed costs per month ($)", "value": 5000, "hint": "rent, salaries, software, insurance"},
            {"id": "price", "label": "Selling price per unit ($)", "value": 40},
            {"id": "varcost", "label": "Variable cost per unit ($)", "value": 15, "hint": "materials, packaging, payment fees"},
        ],
        "js": """
function calculate() {
  const f = val('fixed'), p = val('price'), v = val('varcost');
  const cm = p - v;
  if (cm <= 0) { show('<div class="result-main">Price does not exceed variable cost — every sale loses money. Raise the price or cut unit costs.</div>'); return; }
  const units = f / cm;
  show(`<div class="result-main">${fmt(units, 0)} units / month<small>to break even ($${fmt(units * p, 0)} of revenue)</small></div>
  <table>
    <tr><td>Contribution margin per unit</td><td>$${fmt(cm)} (${fmt(cm / p * 100, 0)}% of price)</td></tr>
    <tr><td>Per day (30-day month)</td><td>${fmt(units / 30, 1)} units</td></tr>
    <tr><td>Profit at 2× break-even volume</td><td>$${fmt(f, 0)} / month</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The idea: contribution margin</h2>
<p>Each sale contributes <em>price minus variable cost</em> toward your fixed costs — that difference is the <strong>contribution margin</strong>. Break-even is simply fixed costs divided by contribution margin per unit. Selling $40 products that cost $15 to deliver, each sale contributes $25; with $5,000 of monthly fixed costs, you need 200 sales a month before profit exists.</p>
<h2>Getting the cost split right</h2>
<ul>
<li><strong>Fixed costs</strong> don't move with volume: rent, salaries, software subscriptions, insurance, loan payments.</li>
<li><strong>Variable costs</strong> scale with each unit: materials, packaging, shipping, payment-processing fees, sales commissions, per-order labor.</li>
<li><strong>Gray areas</strong> (marketing, utilities) go wherever they honestly behave in your business. When unsure, treating a cost as fixed gives the more conservative break-even.</li>
</ul>
<h2>What to do with the number</h2>
<p>Compare break-even volume with realistic market demand — 200 units a month means nothing until you ask whether 7 sales a day is plausible for your channel. Then use the calculator as a sandbox: a $5 price rise cuts the example's break-even from 200 to 167 units; trimming $5 of unit cost does the same. Price changes usually move break-even more than heroic cost-cutting does.</p>
<h2>The margin of safety</h2>
<p>Once selling above break-even, the gap between actual sales and break-even sales — the <em>margin of safety</em> — tells you how much demand can fall before losses start. Selling 260 units against a 200-unit break-even means a 23% cushion. Thin cushions argue for building cash reserves before scaling spending.</p>
""",
        "faqs": [
            ("Does break-even include my own salary?",
             "It should. Founders who exclude their own pay are subsidizing the business with free labor and overstating its health. Add at least a survival salary to fixed costs; the honest break-even is higher but real."),
            ("How does this work for services instead of products?",
             "Define a unit as a billable hour, a project or a client-month. Price is what you charge for it; variable cost is what delivering one more of it costs you (subcontractors, tools billed per client, transaction fees)."),
            ("My break-even looks impossible. Now what?",
             "Three levers, in usual order of power: raise prices (small increases move the number a lot), redesign delivery to cut variable cost, and only then attack fixed costs. If no combination produces a plausible volume, the model — not the effort — is the problem."),
        ],
    },
    {
        "slug": "profit-margin-calculator",
        "emoji": "\U0001F4C9",
        "category": "Business & Self-Employment",
        "title": "Profit Margin Calculator — Gross Margin & Markup",
        "h1": "Profit Margin Calculator",
        "blurb": "Margin, markup and profit from cost and price.",
        "meta_description": "Calculate gross profit margin and markup from cost and selling price — and stop confusing the two. Includes pricing guidance by industry.",
        "intro": "Margin and markup are the most-confused pair in small-business pricing — mixing them up quietly destroys profitability. Enter cost and price to get both, correctly.",
        "fields": [
            {"id": "cost", "label": "Cost per unit ($)", "value": 24},
            {"id": "price", "label": "Selling price per unit ($)", "value": 40},
        ],
        "js": """
function calculate() {
  const c = val('cost'), p = val('price');
  if (p <= 0) { show('<div class="result-main">Price must be above zero.</div>'); return; }
  const profit = p - c;
  const margin = profit / p * 100;
  const markup = c > 0 ? profit / c * 100 : Infinity;
  show(`<div class="result-main">${fmt(margin, 1)}% margin<small>$${fmt(profit)} gross profit per unit</small></div>
  <table>
    <tr><td>Markup on cost</td><td>${fmt(markup, 1)}%</td></tr>
    <tr><td>Profit per unit</td><td>$${fmt(profit)}</td></tr>
    <tr><td>Units for $1,000 of gross profit</td><td>${profit > 0 ? fmt(1000 / profit, 0) : '—'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Margin vs markup, settled</h2>
<p><strong>Margin</strong> is profit as a share of <em>price</em>: (price − cost) ÷ price. <strong>Markup</strong> is profit as a share of <em>cost</em>: (price − cost) ÷ cost. A $24 cost sold at $40 is a 40% margin but a 67% markup — same transaction, different denominators. The dangerous mistake runs one way: a shop owner who wants a 50% margin and therefore "adds 50%" to cost gets only a 33% margin and wonders where the profit went.</p>
<h2>Pricing for a target margin</h2>
<p>To hit margin <em>m</em>, divide — don't multiply: <code>Price = Cost ÷ (1 − m)</code>. For a 50% margin on a $24 cost: 24 ÷ 0.5 = $48, not $36. This one formula is worth more than most pricing courses.</p>
<h2>What is a "good" margin?</h2>
<p>Entirely industry-dependent. Grocery retail survives on 1–3% net margins through volume; software and digital products run 70–90% gross margins; restaurants typically land at 3–9% net after labor and rent. Compare yourself with your industry, not with headlines. Two universal rules: know your margin on every product (many businesses lose money on some items without noticing), and remember gross margin still has to cover all fixed costs before anything is truly profit — our <a href="/calculators/break-even-point-calculator/">break-even calculator</a> picks up exactly there.</p>
""",
        "faqs": [
            ("Which costs belong in 'cost per unit'?",
             "For gross margin: direct costs of the product — purchase or manufacturing cost, inbound shipping, packaging, payment fees. Rent and salaries stay out; they belong to the fixed-cost side of a break-even analysis."),
            ("Why do retailers talk about 'keystone' pricing?",
             "Keystone means doubling cost (100% markup, 50% margin) — a traditional retail default. It is a starting point, not a law; competitive categories run thinner, and unique or service-heavy products can run much thicker."),
            ("Can margin exceed 100%?",
             "Margin cannot — it is capped below 100% because price is the denominator. Markup can be any size: sell a $5 item for $50 and the markup is 900% while the margin is 90%."),
        ],
    },
]
