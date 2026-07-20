# -*- coding: utf-8 -*-
"""Withholding checkup — projects full-year withholding vs expected tax, refund/owe verdict, per-paycheck W-4 fix."""

WITHHOLDING = [
    {
        "slug": "tax-withholding-calculator",
        "emoji": "\U0001F9FE",
        "category": "Taxes & Shopping",
        "title": "Tax Withholding Calculator — Refund or Bill Coming? Fix It Now",
        "h1": "Tax Withholding Calculator",
        "blurb": "Project your year-end refund or bill from a pay stub, and the exact W-4 line that fixes it.",
        "meta_description": "Free tax withholding checkup: project your full-year federal withholding from one pay stub, compare it to your expected tax, see the refund or bill coming — and the exact extra-withholding amount to enter on your W-4 to fix it.",
        "intro": "One pay stub holds everything needed to predict next April: what's been withheld so far, what each check adds, and how many checks remain. Compare the projection to your expected tax and the surprise disappears — replaced by a single number to write on line 4(c) of a new W-4. This calculator does exactly that.",
        "fields": [
            {"id": "ytdwh", "label": "Federal tax withheld year-to-date ($)", "value": 6500, "hint": "from your latest pay stub"},
            {"id": "perpay", "label": "Federal withholding per paycheck ($)", "value": 250},
            {"id": "paysleft", "label": "Paychecks left this year", "value": 11, "step": 1},
            {"id": "expected", "label": "Expected total tax for the year ($)", "value": 11000, "hint": "use our tax bracket calculator, or last year's total tax as a proxy"},
            {"id": "otherwh", "label": "Other withholding/credits expected ($)", "value": 0, "hint": "spouse's job withholding, estimated payments, child tax credit not in the estimate"},
        ],
        "js": """
function calculate() {
  const ytd = Math.max(0, val('ytdwh')), per = Math.max(0, val('perpay'));
  const left = Math.max(0, Math.round(val('paysleft')));
  const tax = val('expected'), other = Math.max(0, val('otherwh'));
  if (tax <= 0) { show('<div class="result-main">Enter your expected total tax.</div>'); return; }
  const projected = ytd + per * left + other;
  const gap = projected - tax; // + refund, - owe
  const pct = Math.abs(gap) / tax * 100;
  const fixPer = left > 0 ? Math.abs(gap) / left : 0;
  const safeHarborNote = gap < 0 && Math.abs(gap) >= 1000;
  let verdict, advice;
  if (gap >= 0 && pct < 5) {
    verdict = `Nicely calibrated`;
    advice = `Projected withholding lands within 5% of the bill — no action needed. Revisit after any raise, bonus, or family change.`;
  } else if (gap > 0) {
    verdict = `~$${fmt(gap,0)} refund coming`;
    advice = `You're over-withholding by about $${fmt(gap/((ytd/per + left) || 1),0)} per paycheck — an interest-free loan to the IRS. To keep it instead: file a new W-4 claiming the credits/deductions you're entitled to (the refund becomes ~$${fmt(fixPer,0)} more take-home per remaining check). Redirect it somewhere useful — even a savings account beats a 0% loan to the government.`;
  } else {
    verdict = `~$${fmt(-gap,0)} bill coming in April`;
    advice = `Fix it before year-end: file a new W-4 with <strong>$${fmt(Math.ceil(fixPer),0)} on line 4(c)</strong> (extra withholding per paycheck) for the remaining ${left} checks. Withholding counts as paid evenly through the year, so a late-year fix can erase penalty exposure from earlier quarters${safeHarborNote ? ' — important here, since owing $1,000+ can trigger underpayment penalties' : ''}.`;
  }
  show(`<div class="result-main">${verdict}<small>projected withholding $${fmt(projected,0)} vs expected tax $${fmt(tax,0)}</small></div>
  <table>
    <tr><td>Withheld so far</td><td>$${fmt(ytd,0)}</td></tr>
    <tr><td>Coming: ${left} checks × $${fmt(per,0)}</td><td>$${fmt(per*left,0)}</td></tr>
    ${other > 0 ? `<tr><td>Other withholding / payments / credits</td><td>$${fmt(other,0)}</td></tr>` : ''}
    <tr><td><strong>Projected total</strong></td><td><strong>$${fmt(projected,0)}</strong></td></tr>
    <tr><td>Expected tax</td><td>$${fmt(tax,0)}</td></tr>
    <tr><td><strong>${gap >= 0 ? 'Refund' : 'Balance due'}</strong></td><td><strong>$${fmt(Math.abs(gap),0)}</strong> (${fmt(pct,1)}% ${gap >= 0 ? 'over' : 'under'})</td></tr>
  </table>
  <p>${advice}</p>`);
}
""",
        "body_html": """
<h2>Why withholding drifts off target</h2>
<p>The W-4 you filed on day one was a guess made by a formula that knows almost nothing about your year. It drifts wrong at predictable moments: a <strong>mid-year raise</strong> (withholding tables adjust, but not for the months already passed), a <strong>second job or side income</strong> (each employer withholds as if theirs is your only income, systematically under-collecting — self-employment income needs <a href="/calculators/quarterly-estimated-tax-calculator/">quarterly payments</a> on top), <strong>marriage or divorce</strong> (the married tables assume one income unless told otherwise — two earners both using them under-withhold, the classic newlywed surprise), a <strong>new child</strong> (worth $2,000 of credit the tables don't know about), and <strong>bonuses/RSUs</strong> withheld at the flat 22% supplemental rate — too much for the 12% bracket, way too little at 32%+ (the <a href="/calculators/bonus-tax-calculator/">bonus tax calculator</a> quantifies your gap).</p>
<h2>The one number you need: expected total tax</h2>
<p>This checkup compares projected withholding against expected tax — and the second number scares people unnecessarily. Two workable sources: <strong>last year's total tax</strong> (the "total tax" line on your 1040 — not the refund, not the payment) if your situation is similar, or a fresh estimate from the <a href="/calculators/tax-bracket-calculator/">tax bracket calculator</a> if income changed meaningfully. Don't chase precision — being within a few hundred dollars beats the average American's status quo by a mile, and you can re-run this in five minutes any payday.</p>
<h2>Reading the verdict honestly</h2>
<ul>
<li><strong>A big refund isn't a win.</strong> $3,600 back in April is $300 a month you earned and couldn't use — an interest-free loan to the Treasury while your credit card charged 25%. The average refund hovers around $3,000, which says most people run their withholding materially wrong in the government's favor. If the forced-savings effect is genuinely what keeps that money safe from you, fine — but an automatic transfer to a <a href="/calculators/savings-goal-calculator/">savings goal</a> does the same job and pays interest.</li>
<li><strong>A big bill is worse than a nuisance.</strong> Owe $1,000+ and underpayment penalties (interest at roughly 8% annualized, per quarter) can stack on top unless you hit a <a href="/calculators/quarterly-estimated-tax-calculator/">safe harbor</a>. The fix is cheap and the deadline is soft: because the IRS treats withholding as paid evenly across the year regardless of when it happened, extra withholding in October-December retroactively cures underpayment from February.</li>
<li><strong>The sweet spot is a small refund.</strong> Aiming for exactly zero risks tipping into penalty territory on a surprise; $200-500 of cushion costs almost nothing and absorbs estimation error.</li>
</ul>
<h2>How to actually fix it (the 2-minute W-4)</h2>
<p>The modern W-4 has no "allowances" — it works in dollars, which makes surgical fixes easy:</p>
<ul>
<li><strong>Under-withholding:</strong> take this calculator's per-check shortfall and enter it on <strong>line 4(c) — extra withholding</strong>. Done. It starts within a payroll cycle or two and you can zero it out in January.</li>
<li><strong>Over-withholding:</strong> claim what you're entitled to — dependents on line 3 ($2,000 per child), deductions beyond the standard on 4(b). Each $2,000 of annual reduction adds roughly $77 to a biweekly check.</li>
<li><strong>Two earners:</strong> check the box in Step 2(c) on <em>both</em> W-4s (it halves the brackets each employer assumes) — the single most-skipped fix for married under-withholding.</li>
<li><strong>Submit it to payroll, not the IRS</strong> — HR portal or a paper form; takes effect in 1-2 cycles. Verify on the next stub, and glance at the projection again after any income change. Your <a href="/calculators/take-home-pay-calculator/">take-home pay</a> shifts accordingly, so re-run the budget if the change is large.</li>
</ul>
""",
        "faqs": [
            ("How do I know my expected total tax for the year?", "Easiest proxy: last year's 'total tax' line from your 1040, if your life is similar. Income changed? Rebuild it: taxable income (gross minus pre-tax 401(k)/health premiums minus the standard deduction) through the tax bracket calculator, minus credits like $2,000 per child. Within a few hundred dollars is plenty accurate for setting withholding."),
            ("Is getting a tax refund actually bad?", "It's not a disaster — it's a 0% loan you made involuntarily. $3,000 back means $250/month you couldn't invest, pay debt with, or even bank at 4%. The counterargument is behavioral: if a refund is the only savings that survives your spending, the forced-saving value may exceed the lost interest. The better version is fixing the W-4 and automating the difference into savings the same day."),
            ("Can I change my W-4 at any time?", "Yes — as often as you like, effective within a payroll cycle or two. Common patterns: extra withholding via 4(c) for the last quarter to cure a shortfall, then a fresh W-4 in January; or updating immediately after marriage, a child, a raise, or a side income starting. Employers must implement a valid W-4; you never need to justify it."),
            ("Why do I owe when my only change was my spouse starting work?", "Each employer's tables assume their paycheck is the household's whole income, so both jobs withhold at rates appropriate for half your actual joint income. The cure is Step 2(c): check the two-jobs box on both W-4s, which makes each employer withhold on compressed brackets. For very unequal incomes, the IRS worksheet (or extra dollars on 4(c) at the higher-paying job) calibrates finer."),
            ("Does extra withholding late in the year avoid underpayment penalties?", "Yes — this is withholding's superpower over estimated payments. Estimated payments are credited when made (a December payment can't fix a June shortfall), but withholding is deemed paid evenly across all four quarters no matter when it happens. A big 4(c) bump in November, or heavy withholding on a December bonus, retroactively covers the whole year's timeline."),
        ],
    },
]
