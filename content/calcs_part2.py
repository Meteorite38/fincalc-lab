# -*- coding: utf-8 -*-
"""Loans & Debt calculators"""

PART2 = [
    {
        "slug": "loan-payment-calculator",
        "emoji": "\U0001F4B3",
        "category": "Debt & Credit",
        "title": "Loan Payment Calculator — Monthly Payment & Total Interest",
        "h1": "Loan Payment Calculator",
        "blurb": "Monthly payment, total interest and cost of any amortized loan.",
        "meta_description": "Calculate the monthly payment on any personal, auto or student loan, plus total interest paid over the life of the loan. Free and instant.",
        "intro": "Enter the amount you want to borrow, the interest rate and the term. The calculator returns your fixed monthly payment and — the number lenders emphasize less — the total interest you will hand over by the end.",
        "fields": [
            {"id": "amount", "label": "Loan amount ($)", "value": 20000},
            {"id": "rate", "label": "Annual interest rate (%)", "value": 8.5, "step": 0.1},
            {"id": "years", "label": "Loan term (years)", "value": 5, "step": 0.5},
        ],
        "js": """
function calculate() {
  const P = val('amount'), r = val('rate') / 100, y = val('years');
  const i = r / 12, n = Math.round(y * 12);
  if (P <= 0 || n <= 0) { show('<div class="result-main">Amount and term must be above zero.</div>'); return; }
  const pmt = i > 0 ? P * i / (1 - Math.pow(1 + i, -n)) : P / n;
  const total = pmt * n, interest = total - P;
  show(`<div class="result-main">$${fmt(pmt)} / month<small>Fixed payment for ${n} months</small></div>
  <table>
    <tr><td>Total of all payments</td><td>$${fmt(total)}</td></tr>
    <tr><td>Total interest</td><td>$${fmt(interest)}</td></tr>
    <tr><td>Interest as share of amount borrowed</td><td>${fmt(interest / P * 100, 1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How loan payments are calculated</h2>
<p>Nearly all personal, auto and student loans are <em>amortized</em>: you pay a fixed amount each month, and each payment is split between interest on the remaining balance and repayment of the balance itself. Early payments are interest-heavy; late payments are mostly principal. The fixed payment comes from the standard amortization formula:</p>
<p><code>PMT = P · i / (1 − (1+i)<sup>−n</sup>)</code></p>
<p>where <em>P</em> is the amount borrowed, <em>i</em> the monthly rate and <em>n</em> the number of payments.</p>
<h2>A worked example</h2>
<p>Borrow $20,000 at 8.5% for 5 years and the payment is about $410 a month. Sixty payments of $410 add up to roughly $24,600 — so the loan costs about $4,600 in interest, or 23% of what you borrowed. Stretch the same loan to 7 years and the payment falls to about $317, but total interest climbs past $6,600. Longer terms buy breathing room at a real price.</p>
<h2>Reading the trade-offs</h2>
<ul>
<li><strong>Term is the biggest lever on total cost.</strong> Shorter terms mean higher payments but dramatically less interest.</li>
<li><strong>Rate shopping pays.</strong> On a $20,000/5-year loan, each percentage point of rate is roughly $550 of lifetime interest.</li>
<li><strong>Watch for fees.</strong> Origination fees effectively raise your rate. Compare loans by APR, which folds mandatory fees in, not the headline rate alone.</li>
</ul>
""",
        "faqs": [
            ("Why does my lender quote a different payment?",
             "Small differences usually come from fees rolled into the balance, payment timing, or daily rather than monthly interest accrual. Large differences deserve a question to the lender — ask for the amortization schedule."),
            ("Can I lower the total interest after taking the loan?",
             "Usually yes, by paying extra toward principal. Even modest extra payments early in the term cut total interest meaningfully, because interest accrues on a smaller balance from then on. Check that your loan has no prepayment penalty."),
            ("Is this calculator suitable for mortgages?",
             "The math is identical, and it will give the correct principal-and-interest payment. For a fuller housing picture including taxes and insurance, use our dedicated mortgage calculator."),
        ],
    },
    {
        "slug": "mortgage-calculator",
        "emoji": "\U0001F3E0",
        "category": "Mortgages & Home",
        "title": "Mortgage Calculator — Monthly Payment with Taxes & Insurance",
        "h1": "Mortgage Calculator",
        "blurb": "Full monthly housing cost: loan, property tax and insurance.",
        "meta_description": "Estimate your true monthly mortgage payment including principal, interest, property tax and home insurance. See total interest over the life of the loan.",
        "intro": "A mortgage payment is more than the loan itself. This calculator combines principal and interest with property tax and insurance to show the real monthly number a lender will assess — and what the house costs you over the full term.",
        "fields": [
            {"id": "price", "label": "Home price ($)", "value": 350000},
            {"id": "down", "label": "Down payment ($)", "value": 70000},
            {"id": "rate", "label": "Interest rate (%)", "value": 6.5, "step": 0.05},
            {"id": "years", "label": "Term (years)", "value": 30, "step": 1},
            {"id": "tax", "label": "Property tax ($/year)", "value": 4200, "hint": "often 1-2% of home value"},
            {"id": "ins", "label": "Home insurance ($/year)", "value": 1500},
        ],
        "js": """
function calculate() {
  const price = val('price'), down = val('down'), r = val('rate') / 100, y = val('years');
  const P = price - down;
  if (P <= 0) { show('<div class="result-main">Down payment covers the full price — no loan needed.</div>'); return; }
  const i = r / 12, n = y * 12;
  const pi = i > 0 ? P * i / (1 - Math.pow(1 + i, -n)) : P / n;
  const extras = (val('tax') + val('ins')) / 12;
  const totalInterest = pi * n - P;
  const ltv = P / price * 100;
  show(`<div class="result-main">$${fmt(pi + extras)} / month<small>Including property tax and insurance</small></div>
  <table>
    <tr><td>Principal &amp; interest</td><td>$${fmt(pi)}</td></tr>
    <tr><td>Property tax + insurance</td><td>$${fmt(extras)}</td></tr>
    <tr><td>Loan amount (LTV ${fmt(ltv, 0)}%)</td><td>$${fmt(P, 0)}</td></tr>
    <tr><td>Total interest over ${y} years</td><td>$${fmt(totalInterest, 0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What is in a mortgage payment?</h2>
<p>Lenders talk about <strong>PITI</strong>: Principal, Interest, Taxes, Insurance. Principal and interest repay the loan; property tax and homeowner's insurance are usually collected monthly into an escrow account and paid on your behalf. Buyers who budget only for principal and interest routinely underestimate their housing cost by 20–30%.</p>
<h2>A worked example</h2>
<p>A $350,000 home with $70,000 down (20%) leaves a $280,000 loan. At 6.5% over 30 years, principal and interest run about $1,770 a month. Add typical tax and insurance and the real monthly cost is roughly $2,245. Over the full term the interest alone comes to about $357,000 — more than the original loan. That is not a scam; it is what three decades of borrowing costs at these rates.</p>
<h2>Levers worth testing in the calculator</h2>
<ul>
<li><strong>Down payment.</strong> Below 20% down, most US lenders add private mortgage insurance (PMI), often 0.5–1.5% of the loan per year — not included above, so treat sub-20% results as optimistic.</li>
<li><strong>Rate.</strong> On a $280,000 loan, one percentage point changes the payment by roughly $180 a month and lifetime interest by about $65,000.</li>
<li><strong>Term.</strong> A 15-year loan roughly halves total interest but raises the monthly payment by 30–40%.</li>
</ul>
<h2>How much house can you afford?</h2>
<p>A common guideline is that total housing costs should stay under 28% of gross monthly income, and all debt payments combined under 36%. Work backwards: if your household earns $8,000 a month, 28% is $2,240 — about the payment in the example above. Guidelines are not laws, but exceeding them consistently is the most common way buyers become house-poor.</p>
""",
        "faqs": [
            ("Does this calculator include PMI?",
             "No. Private mortgage insurance applies to many loans with less than 20% down and typically costs 0.5–1.5% of the loan balance per year. If you are putting less down, mentally add that to the result or increase the insurance field."),
            ("Are property taxes really that predictable?",
             "They change with local rates and reassessments, usually annually. The calculator treats them as constant, which is fine for comparing scenarios, but expect the escrow portion of your payment to drift upward over the years."),
            ("Fixed or variable rate — which does this model?",
             "Fixed. Variable/adjustable mortgages start with a fixed period and then reset periodically; no single calculation can promise their lifetime cost. If you are considering one, stress-test the payment at 2–3 percentage points above the intro rate."),
        ],
    },
    {
        "slug": "loan-payoff-calculator",
        "emoji": "\U0001F680",
        "category": "Debt & Credit",
        "title": "Loan Payoff Calculator — Extra Payments, Time & Interest Saved",
        "h1": "Loan Payoff Calculator",
        "blurb": "See how extra monthly payments shorten a loan and cut interest.",
        "meta_description": "Find out how much faster your loan disappears and how much interest you save by paying extra each month. Works for mortgages, auto and personal loans.",
        "intro": "Already have a loan? Enter the balance, rate and current payment, then test what an extra monthly amount does. The answer is usually more motivating than people expect.",
        "fields": [
            {"id": "balance", "label": "Current balance ($)", "value": 15000},
            {"id": "rate", "label": "Annual interest rate (%)", "value": 9, "step": 0.1},
            {"id": "payment", "label": "Current monthly payment ($)", "value": 320},
            {"id": "extra", "label": "Extra payment per month ($)", "value": 100},
        ],
        "js": """
function payoffMonths(P, i, pmt) {
  if (pmt <= P * i) return null; // payment doesn't cover interest
  let bal = P, months = 0, interest = 0;
  while (bal > 0 && months < 1200) {
    const int = bal * i;
    interest += int;
    bal = bal + int - pmt;
    months++;
  }
  return { months: months, interest: interest };
}
function calculate() {
  const P = val('balance'), i = val('rate') / 100 / 12, pmt = val('payment'), extra = val('extra');
  const base = payoffMonths(P, i, pmt);
  if (!base) { show('<div class="result-main">Your payment does not cover monthly interest — the balance would grow forever. Increase the payment.</div>'); return; }
  const fast = payoffMonths(P, i, pmt + extra);
  const yearsBase = Math.floor(base.months / 12), remBase = base.months % 12;
  const yearsFast = Math.floor(fast.months / 12), remFast = fast.months % 12;
  show(`<div class="result-main">${base.months - fast.months} months sooner<small>and $${fmt(base.interest - fast.interest)} of interest saved</small></div>
  <table>
    <tr><td>Payoff at current payment</td><td>${yearsBase}y ${remBase}m, $${fmt(base.interest)} interest</td></tr>
    <tr><td>Payoff with extra $${fmt(extra, 0)}</td><td>${yearsFast}y ${remFast}m, $${fmt(fast.interest)} interest</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why extra payments punch above their weight</h2>
<p>Every extra dollar goes straight to principal, and interest is charged on principal. So an extra payment doesn't just shrink the balance once — it shrinks every future month's interest charge. The effect compounds in reverse, which is why even $50–$100 a month visibly shortens most loans.</p>
<h2>A worked example</h2>
<p>A $15,000 balance at 9% with a $320 payment takes about 4 years 8 months to clear and costs roughly $3,300 in interest. Add $100 a month and it is gone in about 3 years 6 months with around $2,400 of interest — a year of your life and about $900 back, in exchange for a sacrifice most budgets can absorb.</p>
<h2>Where extra payments rank against other uses of money</h2>
<ul>
<li><strong>Beat the guaranteed rate test.</strong> Paying down a 9% loan is a guaranteed, tax-free 9% return. Very few investments can promise that.</li>
<li><strong>But keep an emergency fund first.</strong> Money sent to the loan is hard to get back. Three to six months of expenses in cash comes before aggressive prepayment.</li>
<li><strong>Check for prepayment penalties.</strong> Rare on modern personal loans, still occasionally present on mortgages. A quick look at your agreement settles it.</li>
</ul>
<h2>Getting the payment applied correctly</h2>
<p>Tell your lender that extra amounts should be applied to <em>principal</em>, not held as a credit toward next month's payment. Most banking apps have an explicit "pay extra principal" option; using it is the difference between actually shortening the loan and merely prepaying future bills.</p>
""",
        "faqs": [
            ("Is it better to pay extra monthly or one lump sum per year?",
             "Mathematically, sooner is better: twelve monthly $100 payments beat a single $1,200 payment at year-end, because principal drops earlier. In practice the difference is small — pick whichever pattern you will actually stick to."),
            ("Should I pay off my loan early or invest instead?",
             "Compare the loan rate with what you realistically expect after tax from investing. High-rate debt (credit cards, most personal loans) almost always wins. For low-rate mortgages, investing may come out ahead, at the cost of certainty — paying down debt is the guaranteed option."),
            ("Why does the calculator cap at 100 years?",
             "If a payment barely exceeds the monthly interest, payoff times explode. The cap keeps the simulation honest; if you hit it, the practical answer is that the payment needs to rise."),
        ],
    },
    {
        "slug": "debt-snowball-vs-avalanche-calculator",
        "emoji": "\U0001F9CA",
        "category": "Debt & Credit",
        "title": "Debt Avalanche vs Snowball — Which Saves You More?",
        "h1": "Debt Avalanche vs Snowball Calculator",
        "blurb": "Compare the two classic payoff strategies on your own debts.",
        "meta_description": "Enter up to three debts and compare the avalanche (highest rate first) and snowball (smallest balance first) payoff methods: time, interest and the real difference.",
        "intro": "List up to three debts and your total monthly budget for them. The calculator simulates both classic strategies — avalanche (highest interest rate first) and snowball (smallest balance first) — and shows exactly what choosing one over the other costs or saves.",
        "fields": [
            {"id": "b1", "label": "Debt 1 balance ($)", "value": 6000},
            {"id": "r1", "label": "Debt 1 rate (%)", "value": 22, "step": 0.1},
            {"id": "b2", "label": "Debt 2 balance ($)", "value": 3000},
            {"id": "r2", "label": "Debt 2 rate (%)", "value": 12, "step": 0.1},
            {"id": "b3", "label": "Debt 3 balance ($, 0 if none)", "value": 1200},
            {"id": "r3", "label": "Debt 3 rate (%)", "value": 7, "step": 0.1},
            {"id": "budget", "label": "Total monthly budget for debts ($)", "value": 400},
        ],
        "js": """
function simulate(debts, budget, order) {
  let ds = debts.map(d => ({ bal: d.bal, rate: d.rate })).filter(d => d.bal > 0);
  let months = 0, interest = 0;
  while (ds.length > 0 && months < 1200) {
    months++;
    for (const d of ds) { const int = d.bal * d.rate / 12; d.bal += int; interest += int; }
    ds.sort(order);
    let pay = budget;
    for (const d of ds) { const p = Math.min(pay, d.bal); d.bal -= p; pay -= p; if (pay <= 0) break; }
    ds = ds.filter(d => d.bal > 0.005);
  }
  return months >= 1200 ? null : { months: months, interest: interest };
}
function calculate() {
  const debts = [
    { bal: val('b1'), rate: val('r1') / 100 },
    { bal: val('b2'), rate: val('r2') / 100 },
    { bal: val('b3'), rate: val('r3') / 100 },
  ];
  const budget = val('budget');
  const minInterest = debts.reduce((s, d) => s + d.bal * d.rate / 12, 0);
  if (budget <= minInterest) { show('<div class="result-main">Your budget does not cover the first month\\'s interest ($' + fmt(minInterest) + '). The balances would grow — increase the budget.</div>'); return; }
  const av = simulate(debts, budget, (a, b) => b.rate - a.rate);
  const sn = simulate(debts, budget, (a, b) => a.bal - b.bal);
  if (!av || !sn) { show('<div class="result-main">Payoff exceeds 100 years — increase the budget.</div>'); return; }
  const diff = sn.interest - av.interest;
  show(`<div class="result-main">Avalanche saves $${fmt(Math.abs(diff))}<small>${diff >= 0 ? 'versus snowball, with the same monthly budget' : 'less than snowball here — rare, driven by rounding; they are effectively tied'}</small></div>
  <table>
    <tr><td>Avalanche (highest rate first)</td><td>${av.months} months, $${fmt(av.interest)} interest</td></tr>
    <tr><td>Snowball (smallest balance first)</td><td>${sn.months} months, $${fmt(sn.interest)} interest</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The two strategies in one minute</h2>
<p>Both methods have you pay minimums on everything and throw every spare dollar at one target debt. They differ only in the target: <strong>avalanche</strong> attacks the highest interest rate first, which is mathematically optimal; <strong>snowball</strong> attacks the smallest balance first, which produces quick wins that keep people motivated. The best strategy on paper is worthless if you abandon it in month three — which is the honest case for snowball.</p>
<h2>How big is the difference, really?</h2>
<p>Usually smaller than the internet argues about. With the example debts ($6,000 at 22%, $3,000 at 12%, $1,200 at 7%) and $400 a month, avalanche saves roughly a few hundred dollars and finishes about the same time as snowball. The gap grows when rate differences are extreme or balances are large; it shrinks toward zero when rates are similar. Run your own numbers — that is what the calculator is for.</p>
<h2>Practical playbook</h2>
<ul>
<li><strong>List every debt</strong> with balance, rate and minimum payment. Visibility alone changes behavior.</li>
<li><strong>Automate minimums</strong> so a missed payment never adds fees to the pile.</li>
<li><strong>Pick a method and stay put.</strong> Switching strategies mid-way costs more than either choice.</li>
<li><strong>Consider a 0% balance transfer or consolidation loan</strong> if your credit allows — lowering the rate beats optimizing the order of expensive debts.</li>
</ul>
""",
        "faqs": [
            ("Which method should I choose?",
             "If you are confident you will stick to the plan, avalanche — it is never worse mathematically. If you have started and quit debt plans before, snowball's early wins have real behavioral value that can outweigh a modest interest cost."),
            ("What about minimum payments on each debt?",
             "For simplicity the calculator pools your entire budget and pays debts in strategy order, which closely approximates real minimum-plus-extra behavior for typical consumer debts. The strategy comparison — the point of the tool — is unaffected."),
            ("My budget can't cover the interest. Now what?",
             "That means balances grow no matter the order. Priorities shift: call lenders about hardship plans, look into consolidation at a lower rate, and treat any high-rate compounding debt as an emergency to stop growing first."),
        ],
    },
]
