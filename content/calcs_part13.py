# -*- coding: utf-8 -*-
"""Batch 11 calculators: borrowing power (how much can I borrow), college savings."""

PART13 = [
    {
        "slug": "how-much-can-i-borrow-calculator",
        "emoji": "\U0001F3E6",
        "category": "Loans & Debt",
        "title": "How Much Can I Borrow? — Borrowing Power Calculator",
        "h1": "How Much Can I Borrow Calculator",
        "blurb": "Max loan a monthly payment can support.",
        "meta_description": "Work out how much you can borrow from the monthly payment you can afford, the interest rate and the term — the reverse of a loan payment calculator.",
        "intro": "Instead of starting with a loan amount, start with the payment you can comfortably afford. Enter it with a rate and term to see the maximum loan it supports.",
        "fields": [
            {"id": "payment", "label": "Monthly payment you can afford ($)", "value": 1500},
            {"id": "rate", "label": "Interest rate (%)", "value": 6.5, "step": 0.05},
            {"id": "years", "label": "Loan term (years)", "value": 30, "step": 1},
        ],
        "js": """
function calculate() {
  const pmt = val('payment'), i = val('rate')/100/12, n = Math.min(Math.round(val('years')*12), 1200);
  if (pmt <= 0 || n <= 0) { show('<div class="result-main">Enter a payment and term above zero.</div>'); return; }
  const loan = i > 0 ? pmt * (1 - Math.pow(1+i, -n)) / i : pmt * n;
  const total = pmt * n, interest = total - loan;
  show(`<div class="result-main">$${fmt(loan,0)}<small>Maximum loan a $${fmt(pmt,0)}/month payment supports at ${fmt(i*1200,2)}% over ${val('years')} years</small></div>
  <table>
    <tr><td>Monthly payment</td><td>$${fmt(pmt)}</td></tr>
    <tr><td>Total you'd repay</td><td>$${fmt(total,0)}</td></tr>
    <tr><td>Total interest</td><td>$${fmt(interest,0)}</td></tr>
    <tr><td>Interest as share of loan</td><td>${fmt(loan>0?interest/loan*100:0,0)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Start with the payment, not the price</h2>
<p>Most loan calculators ask "how much do you want to borrow?" But the smarter question is "what payment can I comfortably afford?" — and then work backward to the loan that fits. This calculator does exactly that reverse calculation, turning an affordable monthly payment into a maximum borrowing amount.</p>
<h2>The math</h2>
<p>It's the amortization formula solved for the loan amount: <code>Loan = Payment × (1 − (1+i)<sup>−n</sup>) ÷ i</code>, where <em>i</em> is the monthly rate and <em>n</em> the number of payments. A $1,500 payment at 6.5% over 30 years supports about a $237,000 loan; the same payment over 15 years supports only about $172,000 — a shorter term buys less because more of each payment goes to principal.</p>
<h2>How to use it wisely</h2>
<ul>
<li><strong>Set the payment from your budget, not the maximum.</strong> A lender's approval is a ceiling, not a target. Base the payment on what leaves room for savings and life — ideally within the <a href="/articles/how-much-house-can-you-afford/">28/36 guideline</a>.</li>
<li><strong>Rate sensitivity is large.</strong> Because you're fixing the payment, a higher rate directly shrinks how much you can borrow. When rates rise, the same payment buys a noticeably smaller loan — which is how rates cool housing demand.</li>
<li><strong>For a home, remember the extras.</strong> Property tax, insurance, and maintenance sit on top of principal and interest, so leave room for them — see the full <a href="/calculators/mortgage-calculator/">mortgage calculator</a> and <a href="/calculators/home-affordability-calculator/">home affordability calculator</a>.</li>
</ul>
<h2>Why payment-first is healthier</h2>
<p>Deciding "I can afford $1,500/month" and finding the loan that fits protects you from the classic trap of falling for a purchase and then stretching the payment to match. Anchor on the payment your budget genuinely supports, and let the loan size follow — not the other way around.</p>
""",
        "faqs": [
            ("How much can I borrow with a given payment?", "It depends on the interest rate and term. Higher rates and shorter terms reduce how much a given payment supports. As an example, $1,500/month at 6.5% over 30 years supports roughly a $237,000 loan."),
            ("Should I borrow the maximum a payment allows?", "Base your payment on what your budget comfortably supports after savings and other goals — not the maximum a lender approves. Borrowing to the ceiling leaves no room for surprises."),
            ("Why does a shorter term let me borrow less?", "Because with a shorter term, more of each payment goes to principal rather than stretching interest over many years, so the same payment supports a smaller loan — while saving you a lot of total interest."),
        ],
    },
    {
        "slug": "college-savings-calculator",
        "emoji": "\U0001F393",
        "category": "Savings & Investing",
        "title": "College Savings Calculator — How Much to Save for Education",
        "h1": "College Savings Calculator",
        "blurb": "Projected education cost and the monthly saving to fund it.",
        "meta_description": "Estimate the future cost of a college education with tuition inflation, and the monthly amount you need to save now to fund it given your expected return.",
        "intro": "Education costs rise faster than general inflation, so starting early matters. Enter today's annual cost and your timeline to see the projected total and the monthly saving needed.",
        "fields": [
            {"id": "cost", "label": "Annual cost today ($)", "value": 25000},
            {"id": "startyears", "label": "Years until study starts", "value": 15, "step": 1},
            {"id": "studyyears", "label": "Years of study", "value": 4, "step": 1},
            {"id": "edinf", "label": "Education cost inflation (%)", "value": 5, "step": 0.1, "hint": "often 4-6%, above general inflation"},
            {"id": "current", "label": "Already saved ($)", "value": 5000},
            {"id": "rate", "label": "Expected annual return (%)", "value": 6, "step": 0.1},
        ],
        "js": """
function calculate() {
  const cost = val('cost');
  const n1 = Math.min(Math.max(0, Math.round(val('startyears'))), 60);
  const sy = Math.min(Math.max(1, Math.round(val('studyyears'))), 12);
  const g = val('edinf')/100, current = val('current'), r = val('rate')/100;
  let total = 0;
  for (let k = 0; k < sy; k++) total += cost * Math.pow(1+g, n1 + k);
  const fvCurrent = current * Math.pow(1+r, n1);
  const gap = Math.max(0, total - fvCurrent);
  const i = r/12, months = n1*12;
  const monthly = months > 0 ? (i>0 ? gap * i / (Math.pow(1+i, months) - 1) : gap/months) : gap;
  let rows = `<tr><td>Projected total cost (${sy} yrs)</td><td>$${fmt(total,0)}</td></tr>
    <tr><td>First-year cost when study starts</td><td>$${fmt(cost*Math.pow(1+g,n1),0)}</td></tr>
    <tr><td>Growth of what you've saved</td><td>$${fmt(fvCurrent,0)}</td></tr>
    <tr><td>Remaining to fund</td><td>$${fmt(gap,0)}</td></tr>`;
  if (n1 <= 0) {
    show(`<div class="result-main">$${fmt(total,0)}<small>Projected total cost — study starts now, so fund from savings/income</small></div><table>${rows}</table>`);
    return;
  }
  show(`<div class="result-main">$${fmt(monthly,0)} / month<small>to save for ${sy} years of study starting in ${n1} years</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>Why education costs need their own plan</h2>
<p>College and university costs have historically risen <strong>faster than general inflation</strong> — often 4–6% a year versus ~2–3% for everything else. That gap compounds brutally over the 10–18 years between a child's birth and their enrollment, which is why "we'll figure it out later" so often turns into loans. This calculator projects the real future cost and the monthly saving that funds it.</p>
<h2>How the projection works</h2>
<p>Each future year of study is today's cost grown by education inflation to the year it's incurred, then summed across the years of study. Your existing savings are grown forward at your expected return, and the remaining gap is converted into the level monthly contribution needed to reach it. Because your savings keep earning during the study years too, the estimate is deliberately a touch conservative — a small safety margin rather than a shortfall.</p>
<h2>Levers that make it achievable</h2>
<ul>
<li><strong>Time is everything.</strong> Starting when a child is born versus at age 10 can cut the required monthly saving by more than half, because <a href="/articles/how-compound-interest-builds-wealth/">compounding</a> has far longer to work.</li>
<li><strong>Use tax-advantaged education accounts</strong> where available (such as 529 plans in the US) — tax-free growth for education dramatically improves the outcome.</li>
<li><strong>You don't have to fund 100%.</strong> Many families aim to cover a portion, with the rest coming from current income, scholarships, work, or student aid. Set a realistic target percentage and plan for that.</li>
<li><strong>Invest for growth early, de-risk near the end.</strong> With a long horizon, stock-heavy <a href="/articles/index-funds-explained/">index funds</a> suit the early years; shift toward safer holdings as enrollment approaches so a crash can't derail the fund — the same <a href="/articles/stocks-vs-bonds-asset-allocation/">allocation</a> logic as retirement.</li>
</ul>
<h2>Keep it in perspective</h2>
<p>The projected numbers can look daunting because education inflation is relentless — but broken into a monthly amount started early, the goal is usually far more reachable than the scary total suggests. And funding education is a balance: never sacrifice your own <a href="/calculators/retirement-savings-calculator/">retirement</a> saving entirely for it, since students have borrowing options that retirees do not. Fund education alongside, not instead of, your own future.</p>
""",
        "faqs": [
            ("How much should I save for my child's education?", "It depends on the type of school, your timeline, and how much of the cost you want to cover. This calculator projects the inflated future cost and the monthly saving to reach it. Starting early dramatically lowers the monthly amount needed."),
            ("Why use a higher inflation rate for education?", "Education costs have historically risen faster than general inflation — often 4–6% a year. Using a higher rate reflects that reality; using the general inflation rate would understate the future cost."),
            ("Should I prioritize education savings over retirement?", "Generally no. Students can borrow or earn for education, but no one can borrow for your retirement. Fund your own retirement first or alongside education savings, not entirely in place of it."),
        ],
    },
]
