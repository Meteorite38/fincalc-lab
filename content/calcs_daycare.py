# -*- coding: utf-8 -*-
"""Second income vs childcare — marginal-tax-aware breakeven on the second earner's job, career-cost framing both ways."""

DAYCARE = [
    {
        "slug": "daycare-vs-staying-home-calculator",
        "emoji": "\U0001F476",
        "category": "Income & Budgeting",
        "title": "Daycare vs Staying Home Calculator — What the Second Income Really Nets",
        "h1": "Daycare vs Staying Home Calculator",
        "blurb": "Second paycheck minus childcare, taxes and work costs — the honest hourly wage that's left.",
        "meta_description": "Free daycare vs staying home calculator: the second earner's income minus childcare for each kid, marginal taxes, commuting and work costs — the true net hourly wage, the breakeven salary, and the retirement/career value the math leaves out.",
        "intro": "When childcare costs rival a paycheck, families run the numbers on one parent staying home — usually on a napkin, usually wrong in both directions. The second income is taxed at the household's highest rates and childcare is paid from what's left; but quitting also pauses raises, retirement match and Social Security credits. This calculator does the napkin honestly, both sides.",
        "fields": [
            {"id": "salary", "label": "Second earner's salary ($/yr)", "value": 55000},
            {"id": "marginal", "label": "Household marginal tax rate on that income (%)", "value": 30, "step": 0.5, "hint": "federal + state + 7.65% FICA on the top dollars"},
            {"id": "kids", "label": "Children needing paid care", "value": 2, "step": 1},
            {"id": "costpk", "label": "Childcare cost per child ($/mo)", "value": 1300, "hint": "infant center care runs $1,000-2,500 by metro"},
            {"id": "fsa", "label": "Dependent-care FSA / tax credit value ($/yr)", "value": 1200, "hint": "FSA saves ~$1,500-2,000 at most incomes; credit if no FSA"},
            {"id": "workcosts", "label": "Work-related costs ($/mo)", "value": 350, "hint": "commute, parking, wardrobe, lunches, convenience meals"},
            {"id": "match", "label": "401(k) match being earned (%)", "value": 4, "step": 0.5, "hint": "% of salary the employer contributes"},
            {"id": "hours", "label": "Hours worked + commuted per week", "value": 45, "step": 1},
        ],
        "js": """
function calculate() {
  const S = val('salary'), t = val('marginal')/100;
  const kids = Math.max(0, Math.round(val('kids'))), cpk = Math.max(0, val('costpk'));
  const fsa = Math.max(0, val('fsa')), wc = Math.max(0, val('workcosts'));
  const matchPct = Math.max(0, val('match'))/100, hrs = Math.max(1, val('hours'));
  if (S <= 0) { show('<div class="result-main">Enter the second earner\\'s salary.</div>'); return; }
  const afterTax = S * (1 - t);
  const care = kids * cpk * 12 - fsa;
  const work = wc * 12;
  const net = afterTax - care - work;
  const match = S * matchPct;
  const netWithMatch = net + match;
  const weeks = 48;
  const hourly = net / (weeks * hrs);
  // breakeven salary: after-tax = care + work  =>  S* = (care+work)/(1-t)
  const breakeven = (care + work) / (1 - t);
  const carePct = afterTax > 0 ? care / afterTax * 100 : 0;
  const verdictLine = net > 8000
    ? `The job clears <strong>$${fmt(net,0)}/year</strong> after everything — real money, before counting the career and retirement value below.`
    : (net > 0
      ? `The job nets just <strong>$${fmt(net,0)}/year</strong> — about $${fmt(hourly,1)}/hour of actual time. The financial case now rests mostly on the long-term items below.`
      : `The job <strong>loses $${fmt(-net,0)}/year</strong> in cash terms right now. If working still wins, it wins on the long-term items below — worth pricing deliberately, not by default.`);
  show(`<div class="result-main">${net >= 0 ? '$' + fmt(net,0) + '/yr net from working' : '&minus;$' + fmt(-net,0) + '/yr — childcare exceeds the paycheck'}<small>= $${fmt(hourly,2)}/hour for ${hrs} hours a week of work + commute${match > 0 ? ' &middot; $' + fmt(netWithMatch,0) + ' counting the 401(k) match' : ''}</small></div>
  <table>
    <tr><td>Salary</td><td>$${fmt(S,0)}</td></tr>
    <tr><td>After ${fmt(t*100,0)}% marginal tax (second income stacks on the first)</td><td>$${fmt(afterTax,0)}</td></tr>
    <tr><td>Childcare: ${kids} × $${fmt(cpk,0)}/mo − $${fmt(fsa,0)} FSA/credit</td><td>&minus;$${fmt(care,0)} <small>(${fmt(carePct,0)}% of take-home)</small></td></tr>
    <tr><td>Work costs (commute, wardrobe, convenience)</td><td>&minus;$${fmt(work,0)}</td></tr>
    <tr><td><strong>Net cash from working</strong></td><td><strong>${net >= 0 ? '$' + fmt(net,0) : '&minus;$' + fmt(-net,0)}</strong></td></tr>
    <tr><td>+ 401(k) match (invisible but real)</td><td>$${fmt(match,0)}</td></tr>
    <tr><td>Breakeven salary at these costs</td><td>$${fmt(breakeven,0)} — below this, the job loses cash</td></tr>
  </table>
  <p>${verdictLine}</p>`);
}
""",
        "body_html": """
<h2>Why the napkin math is usually wrong (in both directions)</h2>
<p>The common version — "my salary minus daycare" — makes two opposite errors. It <strong>overstates the paycheck</strong>: a second income stacks on top of the first, so every dollar is taxed at the household's <em>highest</em> marginal rates (federal bracket + state + 7.65% FICA — often 30-40% all-in; check yours with the <a href="/calculators/tax-bracket-calculator/">bracket calculator</a>), and work itself costs money in commuting, wardrobe and the takeout that survival on two working parents' time requires (the <a href="/calculators/commute-cost-calculator/">commute calculator</a> prices the driving alone). But it also <strong>understates the job's value</strong>: the 401(k) match keeps compounding, Social Security credits keep accruing, health insurance may ride on the second job, and — the biggest omission — <em>childcare is temporary while career damage can be permanent</em>. This calculator handles the first error precisely and puts numbers around the second.</p>
<h2>The number the cash math can't show: career compounding</h2>
<p>Daycare for an infant costs brutal money for about four years, then kindergarten arrives and the cost collapses. A career pause works on the opposite schedule — its costs <em>start</em> small and compound. Research on career interruptions consistently finds re-entry wages 10-30% below the pre-exit path, with the gap persisting a decade or more: missed raises, missed promotions, skill and network decay, and re-entry friction all stack. A 30-year-old leaving a $55,000 job for five years doesn't lose 5 × $55,000; they lose those years <em>plus</em> the difference between their old trajectory and their re-entry salary for the following 15-20 years — often several hundred thousand dollars of lifetime earnings. None of that appears in a monthly cash comparison, which is why a job that "loses" $3,000 a year during the daycare window can still be the financially winning choice — you're paying $3,000/year to keep a compounding asset alive. The <a href="/calculators/salary-inflation-calculator/">salary trajectory math</a> makes the counterfactual vivid.</p>
<h2>What softens the cash squeeze while you decide</h2>
<ul>
<li><strong>Dependent-care FSA:</strong> $5,000 pre-tax through an employer plan saves $1,500-2,000 at typical brackets. No FSA? The child and dependent care credit covers 20-35% of up to $3,000/$6,000 of expenses.</li>
<li><strong>The 401(k) match is part of the wage.</strong> A 4% match on $55,000 is $2,200/year of instant-return compensation — count it (this calculator does), and if cash flow forces cuts, cut elsewhere before the match.</li>
<li><strong>Part-time and flexible middles exist.</strong> Three days a week often keeps the career alive at 60% of the childcare cost — the breakeven line in the results shows exactly how far hours can drop before the cash math flips. Remote work rewrites the work-cost line entirely.</li>
<li><strong>Nanny shares, in-home care, family help and staggered schedules</strong> all attack the per-child cost — at $800/month instead of $1,300, the entire verdict can flip.</li>
<li><strong>The spousal IRA</strong> keeps retirement compounding for a stay-home parent: the working spouse can fund a full <a href="/calculators/roth-ira-calculator/">Roth IRA</a> for the non-earner — do it in any stay-home scenario, or the retirement gap compounds silently.</li>
</ul>
<h2>If one parent does stay home</h2>
<p>Make the decision durable: keep the stay-home parent's <strong>professional pulse alive</strong> (certifications current, network warm, a small freelance thread — even a few billable hours a month changes re-entry odds materially); fund the <strong>spousal IRA</strong> every year; buy <strong>life and disability insurance on both parents</strong> — a stay-home parent's death would force paid childcare, which is exactly the six-figure need the <a href="/calculators/life-insurance-needs-calculator/">life insurance calculator</a> prices; and re-run this calculator annually — the verdict changes as kids age into school, and the family that re-decides on purpose each year beats the one that decided once by default. The household budget also deserves a rebuild for one income: the <a href="/calculators/budget-calculator/">budget calculator</a> handles the mechanics.</p>
<h2>What the money can't decide</h2>
<p>The spreadsheet's job is to make the <em>price</em> of each path honest — not to pick one. Wanting to be home with young kids is a legitimate terminal value that doesn't need a financial justification; loving a career (or needing its structure and identity) is equally legitimate and also doesn't. What the numbers prevent is the specific tragedy of a family choosing based on a wrong napkin — quitting a job that actually netted $12,000 plus a career, or grinding through a job that genuinely nets $2/hour out of unexamined momentum. Get the price right, then decide on your values.</p>
""",
        "faqs": [
            ("Is it worth working if daycare costs my whole paycheck?", "Sometimes yes — because the comparison isn't this year's cash, it's this year's cash plus the career trajectory, retirement match and Social Security credits the job keeps alive. Daycare costs fall off a cliff at kindergarten; career interruption costs compound for decades. A job that breaks even during the 3-4 expensive years often wins enormously over a 15-year horizon. That said, if the net is deeply negative and the career is easily resumable, staying home can be both the preferred and the cheaper path."),
            ("Why use the marginal tax rate instead of the average rate?", "Because household income stacks. The first earner's salary fills the lower brackets; every dollar of the second salary is taxed from where the first left off — at the household's highest combined rate (federal + state + FICA), often 30-40%. Using the second earner's solo average rate makes the paycheck look 15-20% bigger than what actually lands in the account."),
            ("Does staying home hurt Social Security benefits?", "It can. Benefits are computed on your highest 35 earning years — zeros averaged in for stay-home years lower the eventual check, and a shorter record can matter for disability coverage rules. A few years rarely moves it dramatically, but a decade does. The spousal benefit (up to 50% of the working spouse's) provides a floor for long stay-home careers."),
            ("What's a dependent care FSA and should we use it?", "An employer benefit letting you pay up to $5,000/year of childcare with pre-tax dollars — saving roughly your marginal rate (~$1,500-2,000 for most). It beats the childcare tax credit at most middle incomes and above (you generally can't double-dip the same dollars). Enroll during open season; the money is use-it-or-lose-it, but childcare spending is the most predictable expense a family has."),
            ("How should we count the stay-home parent's unpaid work?", "For this decision, count it as the childcare cost you no longer pay — that's already in the math. The broader replacement value (cooking, logistics, care) is real but symmetrical: it exists in both scenarios, just performed at different hours. What deserves explicit pricing is the insurance angle — a stay-home parent's death or disability creates an immediate five-figure annual childcare need, which is why insuring both parents is non-negotiable."),
        ],
    },
]
