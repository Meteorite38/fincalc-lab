# -*- coding: utf-8 -*-
"""Social Security claiming-age break-even: 62 vs FRA vs 70 with exact SSA reduction/credit rules."""

SOCIALSECURITY = [
    {
        "slug": "social-security-break-even-calculator",
        "emoji": "\U0001F3DB",
        "category": "Retirement",
        "title": "Social Security Break-Even Calculator — Claim at 62, 67 or 70?",
        "h1": "Social Security Break-Even Calculator",
        "blurb": "Compare claiming at 62, full retirement age or 70 — and the age each choice pays off.",
        "meta_description": "Should you claim Social Security at 62, full retirement age, or 70? See your monthly benefit at each age using the SSA's exact reduction and delayed-credit rules, plus the break-even age for every pairing.",
        "intro": "Claim at 62 and checks start early but shrink permanently. Wait until 70 and each check is far bigger — but you give up years of payments. Enter the benefit from your Social Security statement and see the exact monthly amounts and the break-even age for each choice.",
        "fields": [
            {"id": "frabenefit", "label": "Monthly benefit at full retirement age ($)", "value": 2000, "hint": "from your SSA statement at ssa.gov/myaccount"},
            {"id": "fra", "label": "Your full retirement age", "type": "select", "value": "67",
             "options": [("67", "67 — born 1960 or later"),
                         ("66.83", "66 and 10 months — born 1959"),
                         ("66.67", "66 and 8 months — born 1958"),
                         ("66.5", "66 and 6 months — born 1957"),
                         ("66", "66 — born 1943-1954")]},
        ],
        "js": """
function ssFactor(claimAge, fra) {
  const m = Math.round((fra - claimAge) * 12);
  if (m > 0) {
    const first = Math.min(m, 36), extra = Math.max(0, m - 36);
    return 1 - first*(5/9)/100 - extra*(5/12)/100;   // SSA early-claim reduction
  }
  return 1 + (-m)*(2/3)/100;                          // delayed retirement credits to 70
}
function ageStr(a) {
  let y = Math.floor(a), mo = Math.round((a - y) * 12);
  if (mo === 12) { y += 1; mo = 0; }
  return mo > 0 ? y + 'y ' + mo + 'm' : y + '';
}
function breakEven(mA, ageA, mB, ageB) {
  // age where cumulative lifetime benefits are equal (B claims later with bigger checks)
  return (mB*ageB - mA*ageA) / (mB - mA);
}
function calculate() {
  const base = val('frabenefit');
  const fra = parseFloat(document.getElementById('fra').value);
  if (base <= 0) { show('<div class="result-main">Enter your benefit at full retirement age.</div>'); return; }
  const m62 = base * ssFactor(62, fra);
  const mFRA = base;
  const m70 = base * ssFactor(70, fra);
  const be1 = breakEven(m62, 62, mFRA, fra);
  const be2 = breakEven(mFRA, fra, m70, 70);
  const be3 = breakEven(m62, 62, m70, 70);
  const pctDown = (1 - m62/base) * 100, pctUp = (m70/base - 1) * 100;
  show(`<div class="result-main">$${fmt(m62,0)} vs $${fmt(mFRA,0)} vs $${fmt(m70,0)}<small>monthly at 62, ${ageStr(fra)} (FRA) and 70 &mdash; in today's dollars</small></div>
  <table>
    <tr><td>Claim at 62</td><td>$${fmt(m62,0)}/mo &mdash; a permanent ${fmt(pctDown,1)}% cut</td></tr>
    <tr><td>Claim at ${ageStr(fra)} (your FRA)</td><td>$${fmt(mFRA,0)}/mo &mdash; 100% of your earned benefit</td></tr>
    <tr><td>Claim at 70</td><td>$${fmt(m70,0)}/mo &mdash; a permanent ${fmt(pctUp,1)}% boost</td></tr>
    <tr><td colspan="2"><strong>Break-even ages (when waiting starts to win):</strong></td></tr>
    <tr><td>${ageStr(fra)} beats 62 if you live past</td><td>~age ${ageStr(be1)}</td></tr>
    <tr><td>70 beats ${ageStr(fra)} if you live past</td><td>~age ${ageStr(be2)}</td></tr>
    <tr><td>70 beats 62 if you live past</td><td>~age ${ageStr(be3)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How the claiming-age math works</h2>
<p>Social Security pays your full earned benefit — the amount on your SSA statement — at your <strong>full retirement age</strong> (67 for anyone born in 1960 or later). Claim earlier and the check is permanently reduced: <strong>5/9 of 1% per month</strong> for the first 36 months early, and 5/12 of 1% per month beyond that. With a FRA of 67, claiming at 62 means a <strong>30% permanent cut</strong>. Wait past FRA and you earn <strong>delayed retirement credits of 2/3 of 1% per month — 8% per year — until 70</strong>, so claiming at 70 with a FRA of 67 pays 124% of your base benefit. There is no benefit to waiting past 70.</p>
<h2>What "break-even" really means</h2>
<p>Claiming early gives you a head start of several years of smaller checks; claiming late gives you bigger checks that must catch up. The <strong>break-even age</strong> is where the two cumulative totals cross. With a $2,000 FRA benefit: age 67 overtakes 62 around <strong>age 78-79</strong>, and 70 overtakes 67 around <strong>age 82-83</strong>. Live shorter than the break-even and claiming early collected more; live longer and waiting wins — by an amount that keeps growing every year you live past it.</p>
<h2>Why the break-even number isn't the whole answer</h2>
<ul>
<li><strong>Longevity insurance:</strong> a 65-year-old man has roughly even odds of reaching 84, a woman 87 — past the typical break-evens. The bigger age-70 check is inflation-adjusted income you cannot outlive, which matters most precisely in the scenario where you live long and other savings run low.</li>
<li><strong>Survivor benefits:</strong> when one spouse dies, the survivor keeps the <em>larger</em> of the two checks. A higher earner delaying to 70 raises the income floor for whichever spouse lives longer — often the strongest argument for waiting even in average health.</li>
<li><strong>COLA doesn't change the ranking:</strong> annual cost-of-living adjustments scale all claiming ages proportionally, so the break-even logic in today's dollars still holds.</li>
<li><strong>The earnings test:</strong> claim before FRA while still working and benefits are temporarily withheld ($1 per $2 earned above roughly $23k/yr) — recalculated in your favor at FRA, but it undercuts the point of claiming early to spend the money.</li>
</ul>
<h2>Reasonable rules of thumb</h2>
<p><strong>Claim early</strong> if you genuinely need the income, your health or family history points to a shorter life, or you're the lower earner in a couple where the higher earner will delay. <strong>Delay toward 70</strong> if you're healthy, can bridge the gap from savings or work, or you're the higher earner in a couple. Test whether your savings can cover the bridge years with the <a href="/calculators/retirement-withdrawal-calculator/">retirement withdrawal calculator</a>, and see what your nest egg needs to be overall with the <a href="/calculators/fire-number-calculator/">FIRE number calculator</a> and <a href="/calculators/retirement-savings-calculator/">retirement savings calculator</a>.</p>
""",
        "faqs": [
            ("Is it better to take Social Security at 62 or 67?", "Purely on lifetime dollars, 67 wins if you live past roughly 78-79 (the break-even). But the answer also depends on whether you need the money now, your health, and spousal considerations — a higher-earning spouse delaying raises the survivor benefit for whoever lives longer."),
            ("How much does waiting from 62 to 70 increase my check?", "With a full retirement age of 67, the age-62 check is 70% of your base benefit and the age-70 check is 124% — so waiting the full eight years raises the monthly check by about 77% for life, plus inflation adjustments on the larger base."),
            ("Do delayed retirement credits keep growing after 70?", "No. Credits stop at 70, so waiting past 70 gives up money with no offsetting increase. If you're past 70 and haven't claimed, file immediately — SSA pays at most 6 months of retroactive benefits."),
            ("Will claiming early while working reduce my benefit?", "Before full retirement age, the earnings test withholds $1 of benefit per $2 earned above an annual limit (about $23,400 in 2025). Withheld amounts aren't lost — your benefit is recalculated upward at FRA — but it makes claiming early while working full-time largely pointless."),
        ],
    },
]
