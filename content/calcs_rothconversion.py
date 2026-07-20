# -*- coding: utf-8 -*-
"""Roth conversion calculator — convert now at today's rate vs stay traditional, pay-tax-from-outside vs from-conversion, RMD linkage."""

ROTHCONV = [
    {
        "slug": "roth-conversion-calculator",
        "emoji": "\U0001F504",
        "category": "Retirement",
        "title": "Roth Conversion Calculator — Pay Tax Now or Let the IRA Ride?",
        "h1": "Roth Conversion Calculator",
        "blurb": "Convert at today's tax rate vs staying traditional — final spendable wealth, both ways.",
        "meta_description": "Free Roth conversion calculator: compare converting IRA money at today's marginal rate against leaving it traditional and paying tax at withdrawal. Handles paying the tax from outside cash vs from the conversion itself, with early-withdrawal penalty.",
        "intro": "A Roth conversion is a bet on tax rates: pay the IRS today at a rate you know, or decades from now at a rate you don't. The math has a clean answer once you pin down three things — today's marginal rate, your future rate, and where the conversion tax money comes from. This calculator runs the full comparison.",
        "fields": [
            {"id": "amount", "label": "Amount to convert ($)", "value": 50000},
            {"id": "tnow", "label": "Marginal tax rate on the conversion (%)", "value": 22, "step": 0.5, "hint": "the conversion stacks on top of your other income"},
            {"id": "tfut", "label": "Expected tax rate in retirement (%)", "value": 24, "step": 0.5, "hint": "rate you'd pay on traditional withdrawals later"},
            {"id": "years", "label": "Years until withdrawal", "value": 20, "step": 1},
            {"id": "ret", "label": "Annual return (%)", "value": 7, "step": 0.1},
            {"id": "paytax", "label": "How will you pay the conversion tax?", "type": "select", "value": "outside",
             "options": [("outside", "From savings outside the IRA"), ("inside", "Withheld from the conversion itself")]},
            {"id": "under59", "label": "Are you under 59\u00bd?", "type": "select", "value": "no",
             "options": [("no", "No"), ("yes", "Yes")]},
        ],
        "js": """
function calculate() {
  const C = val('amount'), tn = val('tnow')/100, tf = val('tfut')/100;
  const yrs = Math.min(60, Math.max(0, Math.round(val('years')))), r = val('ret')/100;
  const payOutside = document.getElementById('paytax').value === 'outside';
  const young = document.getElementById('under59').value === 'yes';
  if (C <= 0) { show('<div class="result-main">Enter an amount to convert.</div>'); return; }
  const g = Math.pow(1 + r, yrs);
  const tax = C * tn;
  const dragG = Math.pow(1 + r * 0.85, yrs); // taxable account: ~15% drag on returns
  let rothFinal, note;
  if (payOutside) {
    rothFinal = C * g;
    note = `full $${fmt(C,0)} goes to the Roth; the $${fmt(tax,0)} tax bill is paid from taxable savings`;
  } else {
    const penalty = young ? tax * 0.10 : 0;
    const toRoth = C - tax - penalty;
    rothFinal = Math.max(0, toRoth) * g;
    note = `$${fmt(tax,0)} withheld for tax${young ? ` plus a $${fmt(penalty,0)} early-withdrawal penalty on the withheld portion` : ''}, so only $${fmt(C - tax - penalty,0)} reaches the Roth`;
  }
  // No-conversion benchmark: money stays traditional; if paying outside, that cash instead grows in a taxable account
  let tradFinal = C * g * (1 - tf);
  if (payOutside) tradFinal += tax * dragG;
  const diff = rothFinal - tradFinal;
  const breakevenTf = payOutside ? (1 - (rothFinal - tax * dragG) / (C * g)) : (1 - rothFinal / (C * g));
  const verdict = Math.abs(diff) < C * 0.005
    ? 'Essentially a wash at these rates — other factors (RMDs, heirs, flexibility) should decide'
    : (diff > 0 ? `Converting wins by <strong>$${fmt(diff,0)}</strong>` : `Staying traditional wins by <strong>$${fmt(-diff,0)}</strong>`);
  show(`<div class="result-main">${diff > 0 ? '$' + fmt(diff,0) + ' ahead by converting' : (diff < -C*0.005 ? '$' + fmt(-diff,0) + ' ahead by NOT converting' : 'Too close to call')}<small>spendable after ${yrs} years: $${fmt(rothFinal,0)} converted vs $${fmt(tradFinal,0)} traditional</small></div>
  <table>
    <tr><td>Convert now: Roth value in ${yrs} years (tax-free)</td><td>$${fmt(rothFinal,0)}</td></tr>
    <tr><td>Don't convert: traditional after ${fmt(tf*100,1)}% tax${payOutside ? ' + the tax money grown in a taxable account' : ''}</td><td>$${fmt(tradFinal,0)}</td></tr>
    <tr><td>Verdict</td><td>${verdict}</td></tr>
    <tr><td>Conversion tax due next April</td><td>$${fmt(tax,0)} (${note})</td></tr>
    <tr><td>Break-even future tax rate</td><td>${fmt(Math.max(0,breakevenTf)*100,1)}% — retire above it and converting wins</td></tr>
  </table>
  ${payOutside ? '' : `<p><strong>Paying tax from the conversion is expensive${young ? ' — especially under 59\u00bd' : ''}.</strong> Rerun with "from savings outside" to see the difference; the gap is the hidden cost of shrinking the tax-free bucket.</p>`}`);
}
""",
        "body_html": """
<h2>What a conversion actually does</h2>
<p>A Roth conversion moves money from a traditional IRA (or old 401(k)) into a Roth IRA. The converted amount is added to your taxable income this year — taxed at your marginal rate — and in exchange it grows tax-free forever, escapes <a href="/calculators/rmd-calculator/">required minimum distributions</a>, and passes to heirs income-tax-free. There are no income limits and no cap: anyone can convert any amount in any year. The only question is whether the tax rate you lock in today beats the rate you'd otherwise pay later.</p>
<h2>The core rule: it's (almost) all about the two rates</h2>
<p>If your conversion is taxed at 22% today and withdrawals would have been taxed at 24% later, converting wins. Flip the rates and it loses. Equal rates: a near-wash — the commutative property of multiplication, since C &times; (1&minus;t) &times; growth equals C &times; growth &times; (1&minus;t). What tilts the balance beyond the headline rates:</p>
<ul>
<li><strong>Paying the tax from outside cash is a stealth contribution.</strong> When the tax bill comes from a taxable brokerage account, the full pre-tax amount ends up in the Roth. You've effectively moved money from a taxed account into a never-taxed one — value the standard rate comparison misses. This calculator credits the no-convert scenario with that same cash growing (with dividend/capital-gains drag) to keep the fight fair.</li>
<li><strong>The conversion itself can push you into higher brackets.</strong> A $100,000 conversion doesn't all get taxed at your current rate — it stacks on top of your income and climbs the ladder. Check where the top of your current bracket sits with the <a href="/calculators/tax-bracket-calculator/">tax bracket calculator</a> and size conversions to fill, not overflow, the bracket.</li>
<li><strong>Future RMDs are the hidden tax raiser.</strong> Large traditional balances force out taxable income at 73/75 whether you need it or not — pushing up your rate, taxing more Social Security, and triggering Medicare IRMAA surcharges. Conversions shrink that time bomb; the <a href="/calculators/rmd-calculator/">RMD calculator</a> shows how big yours is.</li>
</ul>
<h2>The gap years: prime conversion season</h2>
<p>The classic window is <strong>between retirement and RMD age</strong>: salary has stopped, Social Security may be delayed, and taxable income collapses — sometimes to the 10-12% brackets. Converting six figures over several of those years at 12-22% instead of eventually withdrawing at 24-32% is one of the highest-value moves in retirement planning. A common tactic is <strong>bracket-filling</strong>: each December, convert exactly enough to reach the top of your target bracket, no further, and repeat annually.</p>
<h2>Rules that bite</h2>
<ul>
<li><strong>Conversions are irreversible.</strong> Recharacterization (the undo button) was abolished in 2018. Convert only what you're sure about.</li>
<li><strong>Each conversion starts its own 5-year clock</strong> for penalty-free access to that converted principal before 59&frac12;. This is the engine of the "Roth conversion ladder" early retirees use: convert in year 1, spend penalty-free in year 6, repeat annually.</li>
<li><strong>Under 59&frac12;, don't pay tax from the conversion.</strong> The withheld portion counts as an early distribution — income tax <em>plus</em> the 10% penalty on money that never reaches the Roth. Pay from outside cash or wait.</li>
<li><strong>IRMAA look-back:</strong> Medicare premiums two years from now are set by this year's income. A big conversion at 63+ can raise your 65-year-old self's premiums by thousands. Still often worth it — but budget for it.</li>
<li><strong>The pro-rata rule</strong> applies if you have both deductible and non-deductible IRA money: conversions draw proportionally from both, so the tax bill may differ from the naive calculation.</li>
</ul>
<h2>Who usually shouldn't convert</h2>
<p>Converting at your career-peak marginal rate (32-37%) to avoid a likely-lower retirement rate is paying a premium to dodge a discount. Same if you'll retire in a no-income-tax state but convert while living in California. And if the only way to pay the tax is from the IRA itself while under 59&frac12;, the penalty usually kills the deal. For the contribution-stage version of this decision — where new savings should go — use the <a href="/calculators/roth-vs-traditional-401k-calculator/">Roth vs traditional 401(k) calculator</a>; for what the whole retirement stack produces, the <a href="/calculators/retirement-savings-calculator/">retirement savings calculator</a>.</p>
""",
        "faqs": [
            ("Is there a limit on how much I can convert to a Roth?", "No — conversions have no dollar cap and no income limit (those apply to contributions, not conversions). The practical limit is tax: every converted dollar is ordinary income this year, so large conversions climb into higher brackets. Most planners convert in annual slices sized to fill a target bracket."),
            ("When is the deadline for a Roth conversion?", "December 31 of the tax year — not April 15. A conversion executed in January 2026 is 2026 income, taxed on the return you file in 2027. There's no 'prior-year conversion' the way there is for contributions."),
            ("Do I owe the conversion tax immediately?", "It's due with that year's taxes, but if the conversion is large you may need an estimated payment in the quarter it happens to avoid an underpayment penalty — withholding from paychecks often doesn't cover a five-figure conversion. A December conversion with a January 15 estimated payment is a common pattern."),
            ("What's a backdoor Roth and is it the same thing?", "It uses the same conversion mechanism: contribute after-tax dollars to a traditional IRA (no income limit), then convert to Roth almost immediately. Since the contribution was never deducted, the conversion is nearly tax-free — unless you hold other pre-tax IRA money, in which case the pro-rata rule taxes a proportional slice. It's the standard Roth access route for high earners above the contribution income limits."),
            ("Does a Roth conversion make sense in a market downturn?", "Often, yes — converting after a 25% drop moves the same number of shares at a 25% smaller tax bill, and the recovery then happens inside the tax-free account. The rate math still has to work, but downturns make good conversions better."),
        ],
    },
]
