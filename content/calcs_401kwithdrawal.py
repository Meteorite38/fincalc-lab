# -*- coding: utf-8 -*-
"""401(k) early withdrawal calculator — tax + 10% penalty bite, what survives, and the future value sacrificed."""

K401WD = [
    {
        "slug": "401k-early-withdrawal-calculator",
        "emoji": "\U0001F6A8",
        "category": "Retirement",
        "title": "401(k) Early Withdrawal Calculator — The True Cost of Cashing Out",
        "h1": "401(k) Early Withdrawal Calculator",
        "blurb": "Taxes, the 10% penalty, what lands in your account — and what it would have become.",
        "meta_description": "Free 401(k) early withdrawal calculator: federal and state tax plus the 10% penalty, the cash you'd actually keep, and what the balance would have grown to by retirement. Includes penalty exceptions and the loan alternative.",
        "intro": "Cashing out a 401(k) early is the most expensive way to get money that most people ever encounter: taxes and penalty routinely eat 30-45% up front, and the real bill — decades of lost compounding — is bigger still. Sometimes it's still the right call. This calculator prices it honestly so you decide with open eyes.",
        "fields": [
            {"id": "amount", "label": "Amount to withdraw ($)", "value": 30000},
            {"id": "fed", "label": "Federal marginal tax rate (%)", "value": 22, "step": 0.5, "hint": "the withdrawal stacks on top of your income"},
            {"id": "state", "label": "State income tax rate (%)", "value": 5, "step": 0.1},
            {"id": "age", "label": "Your age", "value": 35, "step": 1},
            {"id": "exception", "label": "Penalty exception applies?", "type": "select", "value": "no",
             "options": [("no", "No — standard early withdrawal"), ("55", "Rule of 55 (left job at 55+)"), ("other", "Other exception (disability, medical, etc.)")]},
            {"id": "years", "label": "Years until retirement", "value": 30, "step": 1},
            {"id": "ret", "label": "Return the money would have earned (%)", "value": 7, "step": 0.1},
        ],
        "js": """
function calculate() {
  const W = val('amount'), tf = val('fed')/100, ts = Math.max(0, val('state'))/100;
  const age = Math.round(val('age')), exc = document.getElementById('exception').value;
  const yrs = Math.max(0, Math.round(val('years'))), r = val('ret')/100;
  if (W <= 0) { show('<div class="result-main">Enter a withdrawal amount.</div>'); return; }
  const penaltyFree = age >= 59.5 || exc !== 'no';
  const pen = penaltyFree ? 0 : W * 0.10;
  const fedTax = W * tf, stTax = W * ts;
  const totalCost = fedTax + stTax + pen;
  const keep = W - totalCost;
  const costPct = totalCost / W * 100;
  const fv = W * Math.pow(1 + r, yrs);
  const needGross = penaltyFree ? keep / (1 - tf - ts) : keep / (1 - tf - ts - 0.10);
  show(`<div class="result-main">$${fmt(keep,0)} actually reaches you<small>from a $${fmt(W,0)} withdrawal — ${fmt(costPct,1)}% lost to ${penaltyFree ? 'taxes' : 'taxes + penalty'} up front</small></div>
  <table>
    <tr><td>Federal income tax (${fmt(tf*100,0)}%)</td><td>&minus;$${fmt(fedTax,0)}</td></tr>
    <tr><td>State income tax (${fmt(ts*100,1)}%)</td><td>&minus;$${fmt(stTax,0)}</td></tr>
    <tr><td>Early-withdrawal penalty ${penaltyFree ? '(waived' + (age >= 59.5 ? ' — over 59\u00bd' : (exc === '55' ? ' — rule of 55' : ' — exception')) + ')' : '(10%)'}</td><td>${penaltyFree ? '$0' : '&minus;$' + fmt(pen,0)}</td></tr>
    <tr><td><strong>You keep</strong></td><td><strong>$${fmt(keep,0)}</strong></td></tr>
    <tr><td>What $${fmt(W,0)} would be worth in ${yrs} years at ${fmt(r*100,1)}%</td><td><strong>$${fmt(fv,0)}</strong> — the real price of this withdrawal</td></tr>
    <tr><td>Withdrawal needed to net $${fmt(keep,0)} (grossing up)</td><td>$${fmt(needGross,0)}</td></tr>
  </table>
  <p>${penaltyFree
    ? `No penalty applies, but the compounding cost stands: every $1,000 taken today is ~$${fmt(Math.pow(1+r,yrs)*1000,0)} missing at retirement.`
    : `Put differently: to hold $${fmt(keep,0)} in hand you're spending $${fmt(W,0)} of retirement money that would have become $${fmt(fv,0)}. That's the comparison to make against every alternative — a 401(k) loan, a 0% card, even a personal loan at 12%.`}</p>`);
}
""",
        "body_html": """
<h2>Why the bite is bigger than people expect</h2>
<p>An early 401(k) withdrawal is hit three times. It's <strong>ordinary income</strong> — stacked on top of your salary, taxed at your marginal rate, and sometimes big enough to push you into the next bracket (check where yours sits with the <a href="/calculators/tax-bracket-calculator/">tax bracket calculator</a>). It owes <strong>state income tax</strong> in most states. And under 59&frac12;, the IRS adds a <strong>10% penalty</strong> on the full amount. A 22%-bracket earner in a 5%-tax state loses 37 cents of every dollar before the money arrives. The plan will typically withhold a flat 20% for federal — often <em>less</em> than you actually owe, creating a second unpleasant surprise at filing.</p>
<h2>The penalty has more exceptions than people think</h2>
<ul>
<li><strong>Rule of 55:</strong> leave your job (quit, fired, laid off — any reason) in or after the year you turn 55, and withdrawals <em>from that employer's plan</em> are penalty-free. It doesn't cover IRAs or old 401(k)s left at previous employers — a reason not to roll everything into an IRA right before an early retirement at 55-59.</li>
<li><strong>SEPP / 72(t):</strong> commit to "substantially equal periodic payments" for 5+ years (or until 59&frac12;, whichever is later) and any account can pay out penalty-free at any age. Rigid — breaking the schedule triggers retroactive penalties — but it's the standard early-retiree bridge.</li>
<li><strong>Hardship-adjacent exceptions:</strong> total disability, unreimbursed medical expenses above 7.5% of AGI, a QDRO in divorce, death (heirs), terminal illness, and — new under SECURE 2.0 — a $1,000/year emergency withdrawal, $22,000 for federally declared disasters, and domestic-abuse victim withdrawals. Each has fine print; the penalty vanishes but ordinary income tax always remains.</li>
<li><strong>What doesn't qualify:</strong> buying a house and paying tuition are IRA exceptions, <em>not</em> 401(k) ones — a detail that catches people who assume the accounts share rules.</li>
</ul>
<h2>The alternatives, ranked</h2>
<p>Before cashing out, walk down this list — each rung is usually cheaper than the one below:</p>
<ul>
<li><strong>401(k) loan:</strong> borrow up to 50% of the vested balance (max $50,000), pay yourself back with interest through payroll. No tax, no penalty, no credit check. The risks: leave the job and the balance typically comes due by the tax deadline (or converts to a taxed withdrawal), and the borrowed money misses market growth while out.</li>
<li><strong>0% balance transfer or personal loan:</strong> a 12% personal loan looks expensive until you price the withdrawal above at 37%+ plus lost compounding — run the <a href="/calculators/balance-transfer-calculator/">balance transfer math</a> if it's card debt you're solving.</li>
<li><strong>Roth IRA contributions</strong> (if you have them): contributions — not earnings — come out tax- and penalty-free at any age, making the Roth a de facto deep emergency fund.</li>
<li><strong>The withdrawal</strong> — last, and ideally only for genuine crisis, not for consumption or even debt consolidation that a loan could handle.</li>
</ul>
<h2>The cash-out-at-job-change epidemic</h2>
<p>The most common early withdrawal isn't a crisis — it's the path of least resistance when changing jobs: the old plan mails paperwork, the balance is $8,000, and "just send me a check" feels tidy. Roughly 40% of job-changers cash out some or all of their 401(k), and balances under $10,000 are the most likely to be taken — precisely the money with the most decades left to compound. A $8,000 cash-out at 30 nets maybe $5,000 after taxes and penalty, and costs roughly $60,000 of age-65 wealth at 7%. The right move takes one phone call: a <strong>direct rollover</strong> to the new employer's plan or an IRA — trustee-to-trustee, never a check made out to you (that route triggers 20% withholding and a 60-day deadline). Model what staying invested does with the <a href="/calculators/401k-calculator/">401(k) calculator</a>.</p>
<h2>If you're going to do it anyway</h2>
<p>Sometimes the honest answer is yes — eviction beats optimization. Minimize the damage: withdraw the minimum, not a round number "while you're at it." Time it into a low-income year if any flexibility exists (between jobs often qualifies — the bracket math can cut the tax cost by a third). Check every exception above first. Ask about a hardship withdrawal only after pricing the loan. Set withholding realistically so April doesn't bring a second bill. And afterwards, rebuild deliberately — restart contributions at least to the employer match, then work the <a href="/calculators/emergency-fund-calculator/">emergency fund</a> back up so the next crisis doesn't reach the retirement account.</p>
""",
        "faqs": [
            ("How much tax will I pay on a $10,000 early 401(k) withdrawal?", "Typically $3,000-4,500 all-in: your federal marginal rate (say 22%), state tax (0-10%), plus the 10% penalty if no exception applies. The plan usually withholds a flat 20% federal — if your true combined rate is higher, you'll owe the difference at filing. And the deeper cost: $10,000 removed at 35 is roughly $76,000 missing at 65 at a 7% return."),
            ("Does the 10% penalty apply after I turn 59½?", "No — 59½ ends the penalty for all 401(k) and IRA withdrawals (ordinary income tax still applies to pre-tax money). Before that, exceptions include the rule of 55 (job separation at 55+, that employer's plan only), SEPP/72(t) schedules, disability, major medical costs, QDROs, and several SECURE 2.0 carve-outs like the $1,000 emergency withdrawal."),
            ("Is a 401(k) loan better than a withdrawal?", "Almost always, if your job is stable: no tax, no penalty, and the interest goes back into your own account. The real risks are leaving (or losing) the job — the outstanding balance typically becomes due quickly, and unpaid amounts convert into a taxed, penalized withdrawal — plus the borrowed dollars missing any market gains while out. Cap it at what you can repay within a year or two."),
            ("What happens to my 401(k) if I just leave it when changing jobs?", "Balances over $7,000 can stay in the old plan indefinitely (fine if the plan is good); $1,000-7,000 can be force-rolled into an IRA; under $1,000 can be cashed out and mailed to you with taxes withheld. The clean move is a direct rollover to the new plan or an IRA — it takes one call, avoids all taxes, and keeps the compounding intact."),
            ("Do hardship withdrawals avoid the penalty?", "Mostly no — 'hardship' lets you access the money while employed (the plan's rules), but the 10% penalty still applies unless a separate IRS exception (like medical costs above 7.5% of AGI) covers it. Ordinary income tax applies regardless. Hardship withdrawal ≠ penalty-free withdrawal — the two lists are different, which surprises a lot of people at tax time."),
        ],
    },
]
