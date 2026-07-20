# -*- coding: utf-8 -*-
"""2025 federal tax bracket calculator — progressive math, marginal vs effective, bracket-by-bracket table."""

TAXBRACKET = [
    {
        "slug": "tax-bracket-calculator",
        "emoji": "\U0001F9FE",
        "category": "Taxes & Shopping",
        "title": "Tax Bracket Calculator 2025 — Marginal vs Effective Rate",
        "h1": "Tax Bracket Calculator (2025)",
        "blurb": "Your marginal bracket, effective rate and tax bill under the 2025 federal brackets.",
        "meta_description": "Free 2025 federal tax bracket calculator: see your marginal bracket, true effective rate, and exactly how much tax each bracket takes — single, married filing jointly, or head of household.",
        "intro": "\u201cI'm in the 22% bracket\u201d doesn't mean you pay 22%. Only the dollars inside that bracket do — the rest are taxed at lower rates. Enter your income and see your real federal bill: total tax, marginal rate, effective rate, and what each bracket actually takes.",
        "fields": [
            {"id": "gross", "label": "Gross annual income ($)", "value": 80000},
            {"id": "status", "label": "Filing status", "type": "select", "value": "single",
             "options": [("single", "Single"),
                         ("mfj", "Married filing jointly"),
                         ("hoh", "Head of household")]},
            {"id": "pretax", "label": "Pre-tax contributions ($/yr)", "value": 6000, "hint": "401(k), traditional IRA, HSA, etc."},
            {"id": "extradeduct", "label": "Deductions beyond the standard ($)", "value": 0, "hint": "0 for most people"},
        ],
        "js": """
const BRACKETS = {
  single: { std: 15000, rows: [[0,.10],[11925,.12],[48475,.22],[103350,.24],[197300,.32],[250525,.35],[626350,.37]] },
  mfj:    { std: 30000, rows: [[0,.10],[23850,.12],[96950,.22],[206700,.24],[394600,.32],[501050,.35],[751600,.37]] },
  hoh:    { std: 22500, rows: [[0,.10],[17000,.12],[64850,.22],[103350,.24],[197300,.32],[250500,.35],[626350,.37]] }
};
function calculate() {
  const gross = val('gross'), pretax = val('pretax'), extra = val('extradeduct');
  const cfg = BRACKETS[document.getElementById('status').value] || BRACKETS.single;
  if (gross <= 0) { show('<div class="result-main">Enter your gross income.</div>'); return; }
  const taxable = Math.max(0, gross - Math.max(0,pretax) - cfg.std - Math.max(0,extra));
  const rows = cfg.rows;
  let tax = 0, marginal = 0, detail = '';
  for (let k = 0; k < rows.length; k++) {
    const lo = rows[k][0], rate = rows[k][1];
    const hi = k+1 < rows.length ? rows[k+1][0] : Infinity;
    if (taxable <= lo) break;
    const amt = Math.min(taxable, hi) - lo;
    const t = amt * rate;
    tax += t; marginal = rate;
    detail += `<tr><td>${fmt(rate*100,0)}% bracket ($${fmt(lo,0)}${isFinite(hi) ? '–$'+fmt(hi,0) : '+'})</td><td>$${fmt(amt,0)} taxed &rarr; $${fmt(t,0)}</td></tr>`;
  }
  const effTaxable = taxable > 0 ? tax/taxable*100 : 0;
  const effGross = tax/gross*100;
  show(`<div class="result-main">$${fmt(tax,0)} federal income tax<small>marginal bracket ${fmt(marginal*100,0)}% &middot; effective rate ${fmt(effGross,1)}% of gross income</small></div>
  <table>
    <tr><td>Taxable income (after $${fmt(cfg.std,0)} standard deduction${pretax>0 ? ' + pre-tax contributions' : ''}${extra>0 ? ' + extra deductions' : ''})</td><td>$${fmt(taxable,0)}</td></tr>
    ${detail}
    <tr><td><strong>Total federal income tax</strong></td><td><strong>$${fmt(tax,0)}</strong></td></tr>
    <tr><td>Effective rate on taxable income</td><td>${fmt(effTaxable,1)}%</td></tr>
    <tr><td>Effective rate on gross income</td><td>${fmt(effGross,1)}%</td></tr>
    <tr><td>Income after federal tax</td><td>$${fmt(gross - tax,0)} <em>(before FICA &amp; state tax)</em></td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How tax brackets actually work</h2>
<p>The United States taxes income <strong>progressively</strong>: each bracket's rate applies only to the dollars <em>inside</em> that bracket. A single filer with $65,000 of taxable income in 2025 pays 10% on the first $11,925, 12% on the next $36,550, and 22% only on the last $16,525 — about $9,214 in total, an effective rate of roughly 14% of taxable income, even though they're \u201cin the 22% bracket.\u201d</p>
<p>This kills the most expensive myth in personal finance: <strong>\u201ca raise could push me into a higher bracket and cost me money.\u201d</strong> Impossible. Crossing a bracket line taxes only the dollars above the line at the higher rate; every dollar below keeps its old rate. A raise always increases take-home pay. (Benefit cliffs — income limits for credits and subsidies — are a separate, real phenomenon, but that's not the bracket system.)</p>
<h2>Marginal vs effective: which number to use when</h2>
<ul>
<li><strong>Marginal rate</strong> — what your <em>next</em> dollar is taxed at. Use it for decisions at the margin: is overtime worth it, how much does a 401(k) contribution save, should this year's bonus be deferred, Roth vs traditional. A $1,000 traditional 401(k) contribution in the 22% bracket saves $220 now — exactly why the <a href="/calculators/roth-vs-traditional-401k-calculator/">Roth vs traditional calculator</a> asks for your marginal rate.</li>
<li><strong>Effective rate</strong> — your total tax divided by income; what you actually pay overall. Use it for budgeting and for judging headlines about who pays what. It's always well below your marginal rate, because your first dollars ride the low brackets and the standard deduction is taxed at 0%.</li>
</ul>
<h2>The standard deduction is a 0% bracket</h2>
<p>For 2025 the standard deduction is <strong>$15,000 single / $30,000 married filing jointly / $22,500 head of household</strong>. That's income taxed at zero before the brackets even start — a married couple earning $75,000 with $10,000 of 401(k) contributions has only $35,000 of taxable income, landing mostly in the 10-12% brackets. About 9 in 10 filers take the standard deduction rather than itemizing; unless your mortgage interest, state taxes (capped at $10k... rising under recent law changes) and charitable giving clearly exceed it, the standard deduction wins.</p>
<h2>Legal ways to shrink the bill</h2>
<ul>
<li><strong>Pre-tax retirement and health contributions</strong> — 401(k), traditional IRA (income limits apply), and HSA contributions all come off the top at your marginal rate. Maxing a 401(k) ($23,500) in the 24% bracket cuts the federal bill by $5,640; see the full effect in the <a href="/calculators/401k-calculator/">401(k) calculator</a> and <a href="/calculators/hsa-calculator/">HSA calculator</a>.</li>
<li><strong>Credits beat deductions.</strong> A deduction removes income from tax; a credit removes dollars from the bill. The child tax credit ($2,000/child), education credits and the saver's credit are worth checking every year.</li>
<li><strong>Long-term capital gains ride separate, lower brackets</strong> (0/15/20%) — one reason holding investments over a year matters; see the <a href="/calculators/capital-gains-tax-calculator/">capital gains calculator</a>.</li>
</ul>
<h2>What this calculator deliberately leaves out</h2>
<p>This tool computes <strong>federal income tax on ordinary income</strong>. It excludes FICA payroll taxes (7.65% on most wages — see your full paycheck picture in the <a href="/calculators/take-home-pay-calculator/">take-home pay calculator</a>), state income tax (0% to ~13% depending on state), the alternative minimum tax, and phase-outs of specific credits. Treat the output as the federal core of your tax picture, not a filing-ready return.</p>
""",
        "faqs": [
            ("Does moving into a higher tax bracket reduce my take-home pay?", "No. Bracket rates apply only to the dollars above each threshold, so a raise is always a net gain. Someone crossing from the 12% into the 22% bracket pays 22% only on the few dollars over the line — everything below keeps its lower rate."),
            ("Why is my effective rate so much lower than my bracket?", "Because your income fills the cheap brackets first: the standard deduction is taxed at 0%, then 10%, then 12%, and so on. Only your top slice pays your marginal rate, so the blended average — the effective rate — lands far below it."),
            ("Do these brackets include Social Security and Medicare taxes?", "No. FICA (6.2% Social Security up to the wage cap + 1.45% Medicare, matched by your employer) is a separate flat levy on wages, on top of income tax. A 22%-bracket employee's true marginal rate on wages is closer to 30% once FICA is included."),
            ("Should I use my marginal or effective rate for retirement planning?", "Marginal for contribution decisions (that's the rate a traditional 401(k) contribution avoids today) and something closer to an effective rate for withdrawals in retirement — withdrawals fill the empty low brackets from the bottom up. Using marginal for both is the classic error that overstates the Roth case."),
        ],
    },
]
