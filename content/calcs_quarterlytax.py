# -*- coding: utf-8 -*-
"""Quarterly estimated taxes — safe harbor (100%/110% prior-year) vs 90% current-year, per-quarter schedule with due dates."""

QUARTERLY = [
    {
        "slug": "quarterly-estimated-tax-calculator",
        "emoji": "\U0001F5D3\uFE0F",
        "category": "Taxes & Shopping",
        "title": "Quarterly Estimated Tax Calculator — Safe Harbor, Not Guesswork",
        "h1": "Quarterly Estimated Tax Calculator",
        "blurb": "Your four payment amounts and due dates — safe-harbor prior-year method vs 90% of this year.",
        "meta_description": "Free quarterly estimated tax calculator for freelancers and the self-employed: compare the safe-harbor method (100%/110% of last year's tax) against 90% of this year's projection, get four payment amounts with due dates, and dodge the underpayment penalty.",
        "intro": "The IRS wants tax as income arrives, not in one April lump — and if withholding isn't doing it, quarterly estimated payments must. The good news: you don't have to forecast your income perfectly. The safe-harbor rules let you lock in penalty-proof payments from one number you already know: last year's tax. This calculator builds both schedules.",
        "fields": [
            {"id": "lastyear", "label": "Total tax on last year's return ($)", "value": 18000, "hint": "Form 1040 line 22 minus refundable credits — the 'total tax' line"},
            {"id": "agi", "label": "Last year's AGI ($)", "value": 110000, "hint": "over $150k triggers the 110% safe harbor"},
            {"id": "expected", "label": "This year's expected total tax ($)", "value": 24000, "hint": "estimate — SE tax + income tax on all income"},
            {"id": "withheld", "label": "Tax already withheld this year ($)", "value": 4000, "hint": "from a W-2 job, spouse's job, etc."},
            {"id": "paid", "label": "Estimated payments already made this year ($)", "value": 0},
            {"id": "quarters", "label": "Quarters remaining (including this one)", "type": "select", "value": "4",
             "options": [("4", "4 — starting fresh (Q1 due Apr 15)"), ("3", "3 — starting with Q2 (Jun 15)"), ("2", "2 — starting with Q3 (Sep 15)"), ("1", "1 — only Q4 left (Jan 15)")]},
        ],
        "js": """
function calculate() {
  const LY = val('lastyear'), agi = val('agi'), TY = val('expected');
  const WH = Math.max(0, val('withheld')), paid = Math.max(0, val('paid'));
  const qLeft = parseInt(document.getElementById('quarters').value, 10);
  if (LY < 0 || TY <= 0) { show('<div class="result-main">Enter last year\\'s tax and this year\\'s expected tax.</div>'); return; }
  const shMult = agi > 150000 ? 1.10 : 1.00;
  const safeHarbor = LY * shMult;
  const target90 = TY * 0.90;
  const needSH = Math.max(0, safeHarbor - WH - paid);
  const need90 = Math.max(0, target90 - WH - paid);
  const perSH = needSH / qLeft, per90 = need90 / qLeft;
  const cheaper = Math.min(needSH, need90);
  const useSH = needSH <= need90;
  const aprilGap = TY - Math.max(safeHarbor, WH + paid + (useSH ? needSH : need90));
  const dues = ['Apr 15', 'Jun 15', 'Sep 15', 'Jan 15 (next year)'];
  const startIdx = 4 - qLeft;
  let rows = '';
  for (let i = startIdx; i < 4; i++) {
    rows += `<tr><td>Q${i+1} — due ${dues[i]}</td><td>$${fmt(useSH ? perSH : per90,0)}</td></tr>`;
  }
  show(`<div class="result-main">$${fmt(cheaper / qLeft,0)} per quarter<small>${useSH ? 'safe-harbor method (' + fmt(shMult*100,0) + '% of last year\\'s tax) — penalty-proof regardless of what you earn' : '90%-of-this-year method — cheaper than your safe harbor'}</small></div>
  <table>
    <tr><th>Remaining payment</th><th>Amount</th></tr>
    ${rows}
  </table>
  <table>
    <tr><td>Safe harbor target (${fmt(shMult*100,0)}% × $${fmt(LY,0)})</td><td>$${fmt(safeHarbor,0)} — still owed: $${fmt(needSH,0)}</td></tr>
    <tr><td>90% of this year's $${fmt(TY,0)}</td><td>$${fmt(target90,0)} — still owed: $${fmt(need90,0)}</td></tr>
    <tr><td>Method this schedule uses</td><td><strong>${useSH ? 'Safe harbor' : '90% of current year'}</strong> (the cheaper penalty-proof path)</td></tr>
    ${aprilGap > 0 ? `<tr><td>Expected balance due next April (no penalty)</td><td>$${fmt(aprilGap,0)} — set it aside; safe harbor defers it, doesn't erase it</td></tr>` : `<tr><td>Expected refund/overpayment at filing</td><td>$${fmt(-aprilGap,0)}</td></tr>`}
  </table>
  <p>${useSH && TY > safeHarbor ? `Income jumping this year? The safe harbor is your friend: pay $${fmt(perSH,0)}/quarter and the extra $${fmt(aprilGap,0)} isn't due until April — an interest-free deferral the rules explicitly allow.` : (!useSH ? `Income dropping this year? Paying 90% of the current year beats matching last year's bigger bill — just re-run the estimate each quarter so the projection stays honest.` : `Either method works; the schedule above uses the cheaper one.`)}</p>`);
}
""",
        "body_html": """
<h2>Who actually has to pay quarterly</h2>
<p>The rule: if you'll owe <strong>$1,000 or more</strong> at filing after withholding and credits, the IRS expects payments through the year. In practice that catches freelancers and the <a href="/calculators/self-employment-tax-calculator/">self-employed</a>, landlords, investors with meaningful dividends or gains, retirees between pensions and RMD withholding, and increasingly W-2 employees with a side income their day-job withholding doesn't cover. The system's logic is simple — employees pay as they earn via withholding, so everyone else must too, in four installments: <strong>April 15, June 15, September 15, and January 15</strong>. (Note the rhythm: Q2 is only two months after Q1. It surprises everyone once.)</p>
<h2>Safe harbor: the rule that makes forecasting optional</h2>
<p>You're penalty-proof if your combined withholding + estimated payments reach <em>any</em> of these by the deadlines:</p>
<ul>
<li><strong>100% of last year's total tax</strong> (110% if last year's AGI topped $150,000) — the <em>prior-year safe harbor</em>, and the workhorse: last year's tax is a known number sitting on your filed return, so divide by four and you're done. Your income can double this year and no penalty applies; the extra tax is simply due in April.</li>
<li><strong>90% of this year's tax</strong> — the <em>current-year method</em>, cheaper when income is falling, but it requires an honest running projection.</li>
<li><strong>Owe under $1,000</strong> at filing — the de minimis exit.</li>
</ul>
<p>The strategy writes itself: <strong>income rising → pay the prior-year safe harbor</strong> (smaller checks now, interest-free deferral of the growth); <strong>income falling → pay 90% of the current year</strong> (why match last year's bigger bill?). This calculator runs both and picks the cheaper penalty-proof schedule.</p>
<h2>What the penalty actually is</h2>
<p>Miss the marks and the "penalty" is really interest — the federal short-term rate plus 3 points (recently ~8% annualized), computed per quarter from each due date until paid. On a $4,000 quarterly shortfall that's roughly $80 per quarter of delay: not catastrophic, but a pointless leak. Two structural quirks matter. First, the penalty is <strong>per-quarter</strong>, so a huge January payment doesn't cure a missed April one — timing counts, not just the annual total. Second, <strong>withholding is treated as if paid evenly through the year</strong> regardless of when it actually happened — which enables the cleanest catch-up trick in the tax code: a December bonus withholding bump or a year-end 401(k)-to-Roth conversion with heavy withholding retroactively "spreads" across all four quarters. A W-4 adjustment in October can erase an underpayment from March; a <a href="/calculators/bonus-tax-calculator/">bonus's</a> 22% withholding sometimes does it automatically.</p>
<h2>Building the number: don't forget both taxes</h2>
<p>Freelancers underpay most often because they estimate only income tax. Self-employment profit owes <strong>two stacked taxes</strong>: SE tax (~14.1% effective after the deductions — the <a href="/calculators/self-employment-tax-calculator/">SE tax calculator</a> computes it exactly) plus ordinary income tax at your <a href="/calculators/tax-bracket-calculator/">marginal bracket</a>. A 22%-bracket freelancer's true marginal rate on the next $1,000 of profit is roughly 36%, before state tax. The workable habit: transfer a fixed percentage of every client payment — 30-35% for most brackets — into a separate tax savings account the day it arrives, then pay quarterlies from that account. The <a href="/calculators/freelance-hourly-rate-calculator/">freelance rate calculator</a> bakes this into pricing so the tax money was never "yours" to miss.</p>
<h2>Mechanics and edge cases</h2>
<ul>
<li><strong>Pay online, skip the vouchers:</strong> IRS Direct Pay (free bank transfer) or your IRS online account takes two minutes; EFTPS suits scheduled recurring payments. States run parallel systems with their own quarterly schedules — budget both.</li>
<li><strong>Uneven income?</strong> The <em>annualized income installment method</em> (Form 2210 Schedule AI) matches payments to when income actually arrived — a lifesaver for seasonal businesses or a Q4 windfall, at the cost of real paperwork.</li>
<li><strong>First year self-employed?</strong> If last year's tax was near zero (student, sabbatical), the prior-year safe harbor can be absurdly cheap — even $0 if you had no tax liability last year. Legal, but remember April: the full current-year bill still lands then.</li>
<li><strong>Married with a W-2 spouse?</strong> Raising the spouse's withholding is often simpler than quarterlies — same credit, zero deadlines, and the even-spreading rule works in your favor.</li>
</ul>
""",
        "faqs": [
            ("What happens if I just skip quarterly payments and pay everything in April?", "You'll owe an underpayment penalty — effectively interest at roughly 8% annualized, computed per quarter from each missed due date. On a $20,000 tax bill paid entirely in April, that's typically $700-900 of pure waste. The fix costs nothing: four scheduled payments hitting either safe harbor, or a late-year withholding bump that the even-spreading rule backdates."),
            ("Why is the second quarterly payment due in June, not July?", "The IRS 'quarters' are 3, 2, 3 and 4 months long: Q1 covers Jan-Mar (due Apr 15), Q2 covers only Apr-May (due Jun 15), Q3 covers Jun-Aug (due Sep 15), Q4 covers Sep-Dec (due Jan 15). The June date catches nearly every first-year freelancer. Calendar all four dates now — they don't move except for weekends."),
            ("Do I need to pay quarterly if I also have a W-2 job?", "Only if your withholding won't cover the extra income's tax. Two clean fixes: file a new W-4 adding extra withholding per paycheck (withholding counts as evenly paid all year, so even a late-year change can cure earlier quarters), or make estimated payments for the side income. For modest side income, the W-4 route is usually less hassle."),
            ("What if my income is impossible to predict?", "Use the prior-year safe harbor — that's what it's for. Pay 100% (or 110%) of last year's known tax in four equal installments and no penalty can touch you, no matter what you earn. Keep saving a percentage of each payment received so April's true-up is funded. Alternatively, the annualized method matches payments to actual income per quarter at the cost of Form 2210 paperwork."),
            ("Are state estimated taxes separate?", "Yes — most states with income tax run their own quarterly system with similar (not always identical) safe harbors and due dates, paid through the state's own portal. California, for instance, front-loads its schedule (30%/40%/0%/30%). If you owe federal quarterlies, assume you owe state ones too until verified."),
        ],
    },
]
