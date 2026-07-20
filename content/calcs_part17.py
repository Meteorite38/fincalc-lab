# -*- coding: utf-8 -*-
"""Batch 15 calculators: savings runway (how long will money last), salary gross-up."""

PART17 = [
    {
        "slug": "savings-runway-calculator",
        "emoji": "\U0001F6E9\uFE0F",
        "category": "Budgeting & Life",
        "title": "Savings Runway Calculator — How Long Will Your Money Last?",
        "h1": "Savings Runway Calculator",
        "blurb": "Months your savings would cover with no income.",
        "meta_description": "Find out how many months your savings would last if your income stopped, based on your cash and monthly expenses. Know your financial runway.",
        "intro": "If your income stopped tomorrow, how long could you last? Enter your available savings and monthly expenses to see your financial runway — the cushion that turns a job loss into a manageable gap.",
        "fields": [
            {"id": "savings", "label": "Available savings / cash ($)", "value": 20000},
            {"id": "expenses", "label": "Monthly expenses ($)", "value": 3500},
            {"id": "income", "label": "Any remaining monthly income ($)", "value": 0, "hint": "partial work, benefits, partner"},
        ],
        "js": """
function calculate() {
  const savings = val('savings'), exp = val('expenses'), inc = val('income');
  const netBurn = exp - inc;
  if (netBurn <= 0) {
    show(`<div class="result-main">Indefinitely \\u2705<small>Your income of $${fmt(inc,0)} already covers expenses of $${fmt(exp,0)} \\u2014 savings aren't being drawn down</small></div>`);
    return;
  }
  const months = savings / netBurn;
  const yrs = Math.floor(months/12), mo = Math.round(months%12);
  let band;
  if (months < 1) band = 'Very thin \\u2014 building even one month of buffer is the priority';
  else if (months < 3) band = 'Thin \\u2014 aim to reach at least 3 months';
  else if (months < 6) band = 'Reasonable \\u2014 a solid start; 6 months is a common target';
  else band = 'Strong \\u2014 a healthy cushion of breathing room';
  show(`<div class="result-main">${fmt(months,1)} months<small>${yrs>0 ? '(about '+yrs+'y '+mo+'m) ' : ''}your savings would last at $${fmt(netBurn,0)}/month net</small></div>
  <table>
    <tr><td>Available savings</td><td>$${fmt(savings,0)}</td></tr>
    <tr><td>Net monthly burn</td><td>$${fmt(netBurn,0)}</td></tr>
    <tr><td>Runway</td><td>${fmt(months,1)} months</td></tr>
    <tr><td>Assessment</td><td>${band}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What "runway" means for a household</h2>
<p>Borrowed from the startup world, "runway" is how long you can keep going before the cash runs out. For a household it answers a reassuring, clarifying question: <strong>if my income stopped, how many months could I cover my expenses from savings?</strong> Knowing this number turns a vague fear of job loss into a concrete, manageable figure — and tells you exactly how much cushion you have to make decisions calmly.</p>
<h2>How it's calculated</h2>
<p>Runway is your available savings divided by your monthly net burn (expenses minus any income that would continue). $20,000 in savings with $3,500 of monthly expenses and no other income is about 5.7 months of runway. If a partner's income or partial work would continue, your net burn is lower and your runway stretches further — which is why the calculator lets you enter remaining income.</p>
<h2>Why knowing your runway matters</h2>
<ul>
<li><strong>It quantifies your safety net.</strong> This is the practical flip side of the [emergency fund](/calculators/emergency-fund-calculator/): the fund is the target to build; the runway is how long what you have would actually last.</li>
<li><strong>It informs big decisions.</strong> Enough runway gives you the freedom to leave a bad job, weather a layoff, take a career risk, or start a business without panic.</li>
<li><strong>It reveals urgency.</strong> A runway under a month or two is a clear signal to prioritize building a buffer above almost everything else.</li>
</ul>
<h2>How to extend your runway</h2>
<p>Two levers, both within your control:</p>
<ol>
<li><strong>Increase savings</strong> — the numerator. Every extra dollar saved adds directly to your runway. Automate it (see [how to stop living paycheck to paycheck](/articles/stop-living-paycheck-to-paycheck/)).</li>
<li><strong>Lower your essential burn</strong> — the denominator. Knowing your bare-bones "survival budget" (below your normal spending) means your runway in a real emergency is actually longer than this everyday figure suggests, since you'd cut discretionary costs.</li>
</ol>
<p>Aim to build toward at least 3–6 months of runway. Beyond the money, the peace of mind of knowing you have breathing room is one of the most valuable things savings can buy.</p>
""",
        "faqs": [
            ("How long should my savings last?", "A common target is 3–6 months of expenses in accessible savings — more if your income is variable or you have dependents. This calculator shows your actual runway based on your savings and monthly burn."),
            ("What's the difference between this and an emergency fund calculator?", "The emergency fund calculator sizes the target you should build (months × expenses). This runway calculator tells you how long the savings you already have would actually last if income stopped."),
            ("How can I make my savings last longer?", "Save more (raising the total) and lower your essential monthly expenses (reducing the burn rate). In a real emergency you'd cut discretionary spending, so your true runway is often longer than your everyday-budget figure suggests."),
        ],
    },
    {
        "slug": "salary-gross-up-calculator",
        "emoji": "\U0001F4B0",
        "category": "Income & Budgeting",
        "title": "Salary Gross-Up Calculator — What Salary for Your Target Take-Home",
        "h1": "Salary Gross-Up Calculator",
        "blurb": "The gross salary needed to net a target take-home.",
        "meta_description": "Work out the gross salary you need to reach a target take-home pay, given your tax and deduction rate. The reverse of a take-home pay calculator.",
        "intro": "Know how much you need to take home, and want to find the salary that delivers it? Enter your target net income and your deduction rate to work out the gross salary you'd need.",
        "fields": [
            {"id": "net", "label": "Target take-home (net) amount ($)", "value": 5000},
            {"id": "period", "label": "Per", "value": "month", "type": "select",
             "options": [["month", "Month"], ["year", "Year"]]},
            {"id": "deductions", "label": "Total deductions rate (%)", "value": 25, "step": 0.5, "hint": "tax + social + other, as % of gross"},
        ],
        "js": """
function calculate() {
  const net = val('net'), d = val('deductions')/100;
  const periodEl = document.getElementById('period');
  const period = periodEl ? periodEl.value : 'month';
  if (d >= 1) { show('<div class="result-main">Deductions can\\'t be 100% or more of gross.</div>'); return; }
  const grossPeriod = net / (1 - d);
  const grossAnnual = period === 'year' ? grossPeriod : grossPeriod * 12;
  const grossMonthly = grossAnnual / 12;
  const netAnnual = period === 'year' ? net : net * 12;
  show(`<div class="result-main">$${fmt(grossAnnual,0)} / year<small>Gross salary needed to take home $${fmt(net,0)} per ${period}</small></div>
  <table>
    <tr><td>Gross per year</td><td>$${fmt(grossAnnual,0)}</td></tr>
    <tr><td>Gross per month</td><td>$${fmt(grossMonthly,0)}</td></tr>
    <tr><td>Take-home per year</td><td>$${fmt(netAnnual,0)}</td></tr>
    <tr><td>Lost to deductions</td><td>$${fmt(grossAnnual-netAnnual,0)} (${fmt(d*100,1)}%)</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Working backwards from take-home</h2>
<p>Job offers and salaries are quoted in <em>gross</em> (pre-tax) terms, but you live on <em>net</em> (take-home) pay. So a natural question when planning your finances or evaluating an offer is the reverse of the usual one: "I need to take home $5,000 a month — what salary does that require?" This calculator answers it by "grossing up" your target net pay.</p>
<h2>How the gross-up works</h2>
<p>If deductions take a fraction <em>d</em> of your gross pay, then your take-home is <code>gross × (1 − d)</code>. Flip it to solve for gross: <code>gross = net ÷ (1 − d)</code>. If you want $5,000 net a month and 25% goes to tax and deductions, you need $5,000 ÷ 0.75 ≈ $6,667 gross a month, or about $80,000 a year. Notice the gross-up isn't simply "add 25%" — because the deduction applies to the larger gross figure, you need to divide, not multiply. (Adding 25% to $5,000 would give only $6,250, which nets less than you wanted.)</p>
<h2>Where this is useful</h2>
<ul>
<li><strong>Setting a salary target.</strong> If your budget needs a certain take-home, this tells you the salary to aim or negotiate for.</li>
<li><strong>Evaluating job offers or moves.</strong> Compare what gross salary a new role needs to match your current take-home, especially across places with different tax rates.</li>
<li><strong>Freelance and contract pricing.</strong> If you need a certain net income, grossing up shows what you must bill before tax and expenses — pair it with the [freelance rate calculator](/calculators/freelance-hourly-rate-calculator/).</li>
</ul>
<h2>Getting the deduction rate right</h2>
<p>The accuracy depends on your deduction rate. Use your <em>effective</em> rate — total deductions divided by gross — not your top tax bracket, which overstates it (see [marginal vs effective tax rate](/articles/marginal-vs-effective-tax-rate/)). Your last payslip or tax return gives the real figure. Remember tax is usually progressive, so a much higher target may face a higher effective rate than your current one. Use the standard [take-home pay calculator](/calculators/take-home-pay-calculator/) to check the net a given gross actually produces.</p>
""",
        "faqs": [
            ("How do I calculate the salary I need for a target take-home?", "Divide your target net pay by (1 minus your deduction rate). For $5,000 net a month at 25% deductions: $5,000 ÷ 0.75 ≈ $6,667 gross a month. Dividing, not adding a percentage, gives the correct figure."),
            ("Why can't I just add my tax rate to my target?", "Because the deduction applies to the larger gross amount, not your net target. Adding 25% to a net figure under-shoots; you must divide by (1 − rate) to gross up correctly."),
            ("What deduction rate should I use?", "Use your effective rate — total tax and deductions as a percentage of gross pay — from a recent payslip or tax return, not your top marginal bracket, which would overstate the deductions."),
        ],
    },
]
