# -*- coding: utf-8 -*-
"""Life insurance needs calculator — DIME + income-replacement hybrid, offsets existing coverage/assets, term-length suggestion."""

LIFEINS = [
    {
        "slug": "life-insurance-needs-calculator",
        "emoji": "\U0001F6E1\uFE0F",
        "category": "Budgeting & Life",
        "title": "Life Insurance Needs Calculator — How Much Coverage, Really?",
        "h1": "Life Insurance Needs Calculator",
        "blurb": "Coverage sized from your debts, income, kids and savings — not a salesperson's rule of thumb.",
        "meta_description": "Free life insurance needs calculator using the DIME method plus income replacement: debts, mortgage, years of income, college costs — minus what you already have. Get a coverage number and a term length, not a sales pitch.",
        "intro": "\u201cTen times your salary\u201d is a slogan, not an analysis. The real question is what your dependents would need to stay housed, fed and on track if your income vanished — minus what savings and existing coverage already handle. This calculator does that arithmetic and suggests a term length to match.",
        "fields": [
            {"id": "income", "label": "Your annual after-tax income ($)", "value": 60000},
            {"id": "years", "label": "Years your family would need it replaced", "value": 15, "step": 1, "hint": "until youngest child is independent, typically"},
            {"id": "mortgage", "label": "Mortgage balance ($)", "value": 250000},
            {"id": "debts", "label": "Other debts ($)", "value": 25000, "hint": "car loans, cards, student loans"},
            {"id": "kids", "label": "Children needing future college funds", "value": 2, "step": 1},
            {"id": "college", "label": "College fund per child ($)", "value": 80000, "step": 1000, "hint": "~4-yr public in-state today"},
            {"id": "final", "label": "Final expenses ($)", "value": 15000, "hint": "funeral, medical, legal"},
            {"id": "savings", "label": "Savings & investments that would be available ($)", "value": 80000, "hint": "exclude retirement money you'd want preserved"},
            {"id": "existing", "label": "Life insurance you already have ($)", "value": 100000, "hint": "e.g. group coverage through work"},
        ],
        "js": """
function calculate() {
  const inc = val('income'), yrs = Math.max(0, Math.round(val('years')));
  const mort = val('mortgage'), debts = val('debts');
  const kids = Math.max(0, Math.round(val('kids'))), col = val('college');
  const fin = val('final'), sav = val('savings'), have = val('existing');
  // income replaced as an annuity: invested lump sum earning ~5%, drawn down over the years, ~2.5% inflation -> ~2.5% real
  const rReal = 0.025;
  const incomeNeed = yrs > 0 ? inc * (1 - Math.pow(1 + rReal, -yrs)) / rReal : 0;
  const collegeNeed = kids * col;
  const gross = incomeNeed + mort + debts + collegeNeed + fin;
  const offsets = sav + have;
  const need = gross - offsets;
  const rounded = Math.max(0, Math.ceil(need / 50000) * 50000);
  const multiple = inc > 0 ? need / inc : 0;
  const term = Math.min(30, Math.max(10, Math.ceil(yrs / 5) * 5));
  if (need <= 0) {
    show(`<div class="result-main">You may already be covered<small>resources ($${fmt(offsets,0)}) meet or exceed the estimated need ($${fmt(gross,0)})</small></div>
    <table>
      <tr><td>Income replacement (${yrs} yrs of $${fmt(inc,0)})</td><td>$${fmt(incomeNeed,0)}</td></tr>
      <tr><td>Mortgage + other debts</td><td>$${fmt(mort + debts,0)}</td></tr>
      <tr><td>College (${kids} × $${fmt(col,0)})</td><td>$${fmt(collegeNeed,0)}</td></tr>
      <tr><td>Final expenses</td><td>$${fmt(fin,0)}</td></tr>
      <tr><td>Total need</td><td>$${fmt(gross,0)}</td></tr>
      <tr><td>Minus savings + existing coverage</td><td>&minus;$${fmt(offsets,0)}</td></tr>
    </table>
    <p>Double-check the two big assumptions: would you really want your family to spend down that $${fmt(sav,0)} of savings, and does the group policy at work survive a job change? If either answer is no, rerun without it.</p>`);
    return;
  }
  show(`<div class="result-main">~$${fmt(rounded,0)} of coverage<small>a ${term}-year level term policy fits the ${yrs}-year need window</small></div>
  <table>
    <tr><td>Income replacement (${yrs} yrs of $${fmt(inc,0)}, invested at ~2.5% real)</td><td>$${fmt(incomeNeed,0)}</td></tr>
    <tr><td>Mortgage payoff</td><td>$${fmt(mort,0)}</td></tr>
    <tr><td>Other debts</td><td>$${fmt(debts,0)}</td></tr>
    <tr><td>College (${kids} × $${fmt(col,0)})</td><td>$${fmt(collegeNeed,0)}</td></tr>
    <tr><td>Final expenses</td><td>$${fmt(fin,0)}</td></tr>
    <tr><td><strong>Total need</strong></td><td><strong>$${fmt(gross,0)}</strong></td></tr>
    <tr><td>Minus available savings</td><td>&minus;$${fmt(sav,0)}</td></tr>
    <tr><td>Minus existing coverage</td><td>&minus;$${fmt(have,0)}</td></tr>
    <tr><td><strong>Coverage gap</strong></td><td><strong>$${fmt(need,0)}</strong> (&asymp; ${fmt(multiple,1)}× income)</td></tr>
  </table>
  <p>Rounded to $${fmt(rounded,0)} — insurers price in $50,000-250,000 bands, and the next band up is often nearly free. A healthy 35-year-old typically pays roughly $${fmt(rounded/1000000*30,0)}-$${fmt(rounded/1000000*40,0)}/month per ${term}-year term at this size (smokers and older applicants more).</p>`);
}
""",
        "body_html": """
<h2>Why "10x your salary" gets it wrong in both directions</h2>
<p>Salary multiples ignore everything that actually determines the need: a 55-year-old with grown kids, a paid-off house and $800,000 saved may need <em>zero</em> life insurance at 10&times; salary; a 32-year-old with three toddlers, a new mortgage and thin savings may need 15-20&times;. The number that matters is the <strong>gap between what your dependents would need and what already exists to meet it</strong>. That's what this calculator computes — a version of the DIME method (Debt, Income, Mortgage, Education) with two upgrades: income replacement is priced as an invested annuity rather than a raw multiplication, and existing resources are subtracted instead of ignored.</p>
<h2>The five inputs that matter</h2>
<ul>
<li><strong>Income replacement</strong> is usually the biggest block. The lump sum needed is less than salary &times; years because the payout gets invested and drawn down — $60,000 a year for 15 years needs about $743,000 at a 2.5% real return, not $900,000. Use after-tax income (death benefits are income-tax-free), and count the years until your youngest would be independent.</li>
<li><strong>Mortgage payoff</strong> is a choice: clearing it outright means the survivor's biggest fixed cost disappears, buying enormous breathing room. Alternatively, keep a cheap mortgage and size income replacement to cover the payment — a lower total either way, but most families sleep better with the payoff.</li>
<li><strong>Other debts</strong> — car loans, cards, private student loans (federal loans die with you; private ones with a cosigner don't).</li>
<li><strong>College</strong> at roughly $80,000-100,000 per child for in-state public today (see the <a href="/calculators/college-savings-calculator/">college savings calculator</a> for your own number).</li>
<li><strong>Offsets:</strong> liquid savings your family would genuinely use, plus existing coverage. Be honest about both — retirement accounts your spouse shouldn't be forced to raid at 40 don't belong here, and group life through work typically vanishes when the job does.</li>
</ul>
<h2>Term vs whole life, in one paragraph</h2>
<p>For covering a need that <em>ends</em> — kids grow up, mortgages amortize, savings compound — <strong>level term insurance</strong> is the right tool: a fixed premium for 10-30 years, pure protection, no investment component, priced at a fraction of permanent coverage. A healthy 35-year-old buys $500,000 of 20-year term for roughly $20-30 a month; the same death benefit in whole life runs $400-500. The consensus advice is <em>buy term and invest the difference</em> — the full argument, including the narrow cases where permanent insurance earns its cost, is in our <a href="/articles/do-you-need-life-insurance/">life insurance guide</a>. What the premium difference compounds into over 25 years is exactly the kind of question the <a href="/calculators/compound-interest-calculator/">compound interest calculator</a> answers.</p>
<h2>Matching the term length</h2>
<p>Pick the term to outlive the need, with margin. Youngest child is 3 and independent at 22 → a 20-year term covers it. Mortgage has 25 years left and the payoff matters to you → 25 or 30 years. The failure mode to avoid is a 10-year term that expires at 45 with kids still at home — re-qualifying then, a decade older and with whatever health history has accumulated, costs multiples of the original premium. If needs taper rather than end abruptly, <strong>laddering</strong> works well: e.g. $500,000 of 10-year + $500,000 of 20-year term costs meaningfully less than $1M of 20-year, and matches coverage to a shrinking gap.</p>
<h2>Who needs coverage on them — and who doesn't</h2>
<ul>
<li><strong>A non-earning or lower-earning spouse still needs coverage</strong> if their death would force paid childcare, or the survivor to cut hours. Full-time childcare for two kids runs $2,000-3,500/month in much of the country — that's a $300,000-500,000 need nobody prices until it happens.</li>
<li><strong>Single people with no dependents</strong> generally need only final-expense-level coverage, if that. Same for retirees whose kids are launched and whose spouse is provided for by assets — insurance is for dependents, not for leaving a score.</li>
<li><strong>Children</strong> don't need life insurance; nobody depends on their income. The marketing suggesting otherwise is selling something else.</li>
<li><strong>Business owners and cosigned debts</strong> are the special cases — buy-sell agreements and cosigner protection legitimately call for policies outside this calculator's family math.</li>
</ul>
<h2>Keeping the premium honest</h2>
<p>Life insurance is one of the most shopped-out financial products: identical coverage varies 30-50% between insurers because each prices health classes differently. Get quotes from several carriers (independent brokers and comparison sites do this in one pass), don't smoke, and apply sooner rather than later — every birthday nudges the premium up 5-8%, and premiums lock for the whole term. Once the policy is in force, fold it into the budget with the <a href="/calculators/budget-calculator/">budget calculator</a> and revisit the coverage number at every major life event: new child, new house, big raise, or a spouse leaving work.</p>
""",
        "faqs": [
            ("Is the group life insurance from my job enough?", "Usually not by itself — employer coverage is typically 1-2× salary, a fraction of what a family with young kids needs, and it almost never follows you out the door. Treat it as a bonus layer on top of an individually owned term policy sized to the real gap, not as the plan."),
            ("Should I insure a stay-at-home parent?", "Yes. Their death creates large new costs — childcare, household logistics, possibly the surviving parent cutting hours — even though no salary disappears. A common sizing: enough to cover full-time childcare until the youngest is in middle school, often $250,000-500,000 of cheap term."),
            ("Do I need life insurance if I have no kids and no spouse?", "Generally no — life insurance protects people who depend on your income. Exceptions: cosigned private debts (the cosigner keeps owing), a business partner, or supporting aging parents. Otherwise, the premium does more good in your investment account."),
            ("Is a life insurance payout taxed?", "Death benefits are free of federal income tax to the beneficiary, which is why this calculator uses after-tax income for replacement. (Estate tax only enters for estates above the federal exemption — $13.99M per person in 2025 — and even then only when the policy is owned inside the estate.)"),
            ("What happens when my term ends and I still want coverage?", "Most term policies convert to annually-renewing coverage at steep, rising rates — effectively a signal to stop. If you've saved along the way, the need has usually shrunk to zero by then; that's the design. If you anticipate needing coverage past the term (dependent with special needs, late-in-life kids), buy a longer term or a laddered stack now, while health is on your side."),
        ],
    },
]
