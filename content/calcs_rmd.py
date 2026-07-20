# -*- coding: utf-8 -*-
"""RMD calculator — SECURE 2.0 start ages (73/75 by birth year), IRS Uniform Lifetime Table, multi-year projection."""

RMD = [
    {
        "slug": "rmd-calculator",
        "emoji": "\U0001F4C5",
        "category": "Retirement",
        "title": "RMD Calculator — Required Minimum Distributions Under SECURE 2.0",
        "h1": "RMD Calculator",
        "blurb": "Your required minimum distribution by birth year, plus a year-by-year projection.",
        "meta_description": "Free RMD calculator using the IRS Uniform Lifetime Table and SECURE 2.0 start ages (73 or 75 by birth year). See your first required minimum distribution, the 25% penalty at stake, and a year-by-year projection.",
        "intro": "Once you hit your RMD age, the IRS requires you to start draining pre-tax retirement accounts — and the penalty for missing a distribution is 25% of the shortfall. This calculator finds your start age under SECURE 2.0, your first RMD, and projects the next two decades of withdrawals.",
        "fields": [
            {"id": "birthyear", "label": "Year you were born", "value": 1958, "step": 1},
            {"id": "balance", "label": "Pre-tax retirement balance today ($)", "value": 500000, "hint": "traditional IRA + 401(k)/403(b) + SEP/SIMPLE"},
            {"id": "ret", "label": "Expected annual return (%)", "value": 5, "step": 0.1},
        ],
        "js": """
const RMD_D = {72:27.4,73:26.5,74:25.5,75:24.6,76:23.7,77:22.9,78:22.0,79:21.1,80:20.2,81:19.4,82:18.5,83:17.7,84:16.8,85:16.0,86:15.2,87:14.4,88:13.7,89:12.9,90:12.2,91:11.5,92:10.8,93:10.1,94:9.5,95:8.9,96:8.4,97:7.8,98:7.3,99:6.8,100:6.4,101:6.0,102:5.6,103:5.2,104:4.9,105:4.6,106:4.3,107:4.1,108:3.9,109:3.7,110:3.5,111:3.4,112:3.3,113:3.1,114:3.0,115:2.9,116:2.8,117:2.7,118:2.5,119:2.3,120:2.0};
function calculate() {
  const by = Math.round(val('birthyear')), B0 = val('balance'), r = val('ret')/100;
  if (by < 1900 || by > 2005 || B0 <= 0) { show('<div class="result-main">Enter a birth year (1900–2005) and a balance above zero.</div>'); return; }
  const rmdAge = by <= 1950 ? 72 : (by <= 1959 ? 73 : 75);
  const nowYear = new Date().getFullYear();
  const curAge = nowYear - by;
  const startAge = Math.max(rmdAge, curAge);
  const startYear = by + startAge;
  let bal = B0;
  for (let a = curAge; a < startAge; a++) bal *= (1 + r);
  const horizon = Math.min(20, 121 - startAge);
  let rows = '', firstRmd = 0, firstPct = 0, totalRmd = 0;
  let b = bal;
  for (let k = 0; k < horizon; k++) {
    const age = startAge + k;
    const d = RMD_D[Math.min(age, 120)];
    const rmd = b / d;
    if (k === 0) { firstRmd = rmd; firstPct = 100 / d; }
    totalRmd += rmd;
    const endBal = Math.max(0, (b - rmd) * (1 + r));
    if (k < 12 || k === horizon - 1) rows += `<tr><td>${startYear + k} — age ${age}</td><td>${d.toFixed(1)}</td><td>$${fmt(rmd,0)}</td><td>$${fmt(endBal,0)}</td></tr>`;
    else if (k === 12) rows += `<tr><td colspan="4" style="text-align:center">&hellip;</td></tr>`;
    b = endBal;
  }
  const lead = startAge > curAge
    ? `Your first RMD lands in <strong>${startYear}</strong>, the year you turn ${startAge}: about <strong>$${fmt(firstRmd,0)}</strong> from a projected $${fmt(bal,0)} balance`
    : `Your ${startYear} RMD is about <strong>$${fmt(firstRmd,0)}</strong> — ${fmt(firstPct,2)}% of the balance`;
  show(`<div class="result-main">$${fmt(firstRmd,0)}<small>first-year required distribution &middot; RMDs start at age ${rmdAge} for those born ${by <= 1950 ? 'in 1950 or earlier' : (by <= 1959 ? '1951–1959' : '1960 or later')}</small></div>
  <p>${lead}. Miss it and the IRS penalty is <strong>$${fmt(firstRmd*0.25,0)}</strong> (25% of the shortfall; 10% if corrected within two years).</p>
  <table>
    <tr><th>Year</th><th>IRS divisor</th><th>RMD</th><th>Year-end balance</th></tr>
    ${rows}
    <tr><td><strong>Total forced out over ${horizon} years</strong></td><td></td><td><strong>$${fmt(totalRmd,0)}</strong></td><td></td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What an RMD actually is</h2>
<p>Traditional IRAs and pre-tax 401(k)s grew tax-deferred for decades — the required minimum distribution is how the IRS finally collects. Starting at your RMD age, you must withdraw a minimum amount from pre-tax retirement accounts every year and pay ordinary income tax on it. The formula is simple: <strong>the account balance on December 31 of the previous year, divided by the IRS Uniform Lifetime Table factor for your age</strong>. At 73 the divisor is 26.5, so a $500,000 balance forces out about $18,868 — roughly 3.8%. The percentage climbs every year: about 5% at 80, 8% at 90, 11% at 95.</p>
<h2>When you start: 73 or 75, by birth year</h2>
<p>SECURE 2.0 staggered the start age. Born <strong>1951–1959</strong>: RMDs begin the year you turn <strong>73</strong>. Born <strong>1960 or later</strong>: they begin at <strong>75</strong>. (Born 1950 or earlier, you're already under the old rules.) One quirk worth knowing: your <em>first</em> RMD can be delayed until April 1 of the following year — but the second one is still due that same December 31, so delaying stacks two taxable distributions into one year. Usually a mistake unless your income is unusually high in the first year.</p>
<h2>Which accounts owe RMDs</h2>
<ul>
<li><strong>Owe RMDs:</strong> traditional IRA, SEP and SIMPLE IRAs, pre-tax 401(k)/403(b)/457(b), and inherited versions of all of these (on separate, often harsher schedules).</li>
<li><strong>No RMDs:</strong> Roth IRAs during the owner's lifetime — and since 2024, <strong>Roth 401(k)s are exempt too</strong>.</li>
<li><strong>Aggregation:</strong> multiple IRAs can be totaled and the combined RMD taken from any one of them. Workplace plans don't get that courtesy — each 401(k) must pay out its own RMD separately. (If you're still working at RMD age, the current employer's plan is usually deferred until you retire.)</li>
</ul>
<h2>The real problem: RMDs as a tax time bomb</h2>
<p>RMDs are taxed as ordinary income whether you need the money or not. Large pre-tax balances can force six-figure distributions that push you into higher brackets, make up to 85% of Social Security taxable, and trigger Medicare IRMAA surcharges (an extra $1,000–5,000+ per year in premiums). Check what your projected RMD does to your bracket with the <a href="/calculators/tax-bracket-calculator/">tax bracket calculator</a>. Three standard defusal tools:</p>
<ul>
<li><strong>Roth conversions in the gap years.</strong> Between retirement and RMD age, income is often low — converting pre-tax money to Roth at 12–22% beats being forced out at 24–32% later. Each dollar converted shrinks every future RMD.</li>
<li><strong>QCDs from age 70&frac12;.</strong> Qualified charitable distributions send IRA money directly to charity — up to $108,000 per person in 2025 — counting toward the RMD without ever appearing in taxable income. Strictly better than donating cash if you give at all.</li>
<li><strong>Spend pre-tax first.</strong> Many retirees preserve the IRA and live on taxable savings, unintentionally maximizing future RMDs. Drawing pre-tax money early at low brackets — sized with the <a href="/calculators/retirement-withdrawal-calculator/">retirement withdrawal calculator</a> — often lowers lifetime tax.</li>
</ul>
<h2>What this calculator assumes</h2>
<p>Projections grow your balance at the return you set, subtract each year's RMD, and apply the current Uniform Lifetime Table (the one in effect since 2022) — the table used by account owners whose spouse is not both the sole beneficiary and more than 10 years younger; that situation uses a more generous joint-life table. Inherited accounts follow different rules entirely (most non-spouse heirs must empty the account within 10 years). Timing your RMDs alongside Social Security matters too — the <a href="/calculators/social-security-break-even-calculator/">break-even calculator</a> shows why many delay benefits while spending down the IRA.</p>
""",
        "faqs": [
            ("What happens if I miss my RMD?", "The penalty is 25% of the amount you failed to withdraw (reduced from 50% by SECURE 2.0), and it drops to 10% if you fix the shortfall within roughly two years and file Form 5329. The IRS can waive it entirely for reasonable cause — but the cleanest fix is a calendar reminder each December."),
            ("Do Roth accounts have RMDs?", "Roth IRAs never do during your lifetime. Roth 401(k)s used to, but SECURE 2.0 eliminated their RMDs starting in 2024 — so there's no longer a reason to roll a Roth 401(k) to an IRA just to dodge distributions. Inherited Roth accounts do have distribution requirements for heirs."),
            ("Can I take my RMD as stock instead of cash?", "Yes — it's called an in-kind distribution: shares move from the IRA to a taxable brokerage account, and their market value on the day of transfer counts as the RMD and as taxable income. Useful when you don't want to sell a position, though you'll still need cash from somewhere to pay the tax."),
            ("Does the RMD force me to spend the money?", "No — it only forces the money out of the tax-deferred wrapper. You can reinvest it in a taxable brokerage account the same day. The requirement is that it leaves the IRA and gets taxed, not that you consume it."),
            ("How are RMDs calculated if my spouse is much younger?", "If your spouse is both your sole beneficiary and more than 10 years younger, you use the Joint Life and Last Survivor Table instead of the Uniform Lifetime Table — the divisors are larger, so the required withdrawals are smaller. Everyone else uses the uniform table this calculator applies."),
        ],
    },
]
