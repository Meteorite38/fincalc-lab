# -*- coding: utf-8 -*-
"""Self-employment tax — 92.35% base, SS wage-base cap with W-2 coordination, half-SE deduction, quarterlies."""

SETAX = [
    {
        "slug": "self-employment-tax-calculator",
        "emoji": "\U0001F9D1\u200D\U0001F4BB",
        "category": "Business",
        "title": "Self-Employment Tax Calculator 2025 — SE Tax + Quarterly Estimates",
        "h1": "Self-Employment Tax Calculator",
        "blurb": "SE tax, the half-deduction, income tax estimate and your quarterly payment.",
        "meta_description": "2025 self-employment tax calculator: the 15.3% SE tax with the Social Security wage-base cap and W-2 coordination, the half-SE deduction, estimated income tax, and what to send the IRS each quarter.",
        "intro": "Freelancers and side-hustlers pay both halves of Social Security and Medicare — the 15.3% self-employment tax — on top of income tax. Enter your profit (and any W-2 wages, which shrink the Social Security portion) to see the full bill and what each quarterly payment should be.",
        "fields": [
            {"id": "profit", "label": "Net self-employment profit ($/yr)", "value": 60000, "hint": "income minus business expenses"},
            {"id": "w2", "label": "W-2 wages this year ($)", "value": 0, "hint": "if you also have a day job"},
            {"id": "taxrate", "label": "Marginal income tax rate (%)", "value": 22, "step": 0.5, "hint": "see our tax bracket calculator"},
        ],
        "js": """
function calculate() {
  const profit = val('profit'), w2 = Math.max(0, val('w2')), t = val('taxrate')/100;
  if (profit <= 0) { show('<div class="result-main">Enter a net profit above zero.</div>'); return; }
  const SS_CAP = 176100;                       // 2025 Social Security wage base
  const base = profit * 0.9235;                // SE earnings subject to tax
  const ssRoom = Math.max(0, SS_CAP - w2);     // W-2 wages use up the cap first
  const ssTaxable = Math.min(base, ssRoom);
  const ssTax = ssTaxable * 0.124;
  const medTax = base * 0.029;
  const addMed = Math.max(0, base - Math.max(0, 200000 - w2)) * 0.009;
  const seTax = ssTax + medTax + addMed;
  const halfDeduct = (ssTax + medTax) / 2;
  const incomeTax = Math.max(0, (profit - halfDeduct)) * t;
  const total = seTax + incomeTax;
  const quarterly = total / 4;
  const eff = total / profit * 100;
  const capNote = ssTaxable < base ? `<tr><td>Social Security cap reached</td><td>only $${fmt(ssTaxable,0)} of $${fmt(base,0)} SE earnings hit the 12.4%</td></tr>` : '';
  show(`<div class="result-main">$${fmt(seTax,0)} SE tax + ~$${fmt(incomeTax,0)} income tax<small>set aside about $${fmt(quarterly,0)} per quarter (${fmt(eff,1)}% of profit overall)</small></div>
  <table>
    <tr><td>SE earnings base (profit &times; 92.35%)</td><td>$${fmt(base,0)}</td></tr>
    ${capNote}
    <tr><td>Social Security portion (12.4%)</td><td>$${fmt(ssTax,0)}</td></tr>
    <tr><td>Medicare portion (2.9%${addMed>0 ? ' + 0.9% additional' : ''})</td><td>$${fmt(medTax + addMed,0)}</td></tr>
    <tr><td><strong>Self-employment tax</strong></td><td><strong>$${fmt(seTax,0)}</strong></td></tr>
    <tr><td>Deductible half of SE tax</td><td>&minus;$${fmt(halfDeduct,0)} off taxable income</td></tr>
    <tr><td>Estimated federal income tax (${fmt(t*100,1)}% on profit after the half-deduction)</td><td>$${fmt(incomeTax,0)}</td></tr>
    <tr><td><strong>Total federal bill</strong></td><td><strong>$${fmt(total,0)}</strong> &middot; ${fmt(eff,1)}% of profit</td></tr>
    <tr><td>Suggested quarterly estimated payment</td><td>$${fmt(quarterly,0)} (due Apr 15, Jun 15, Sep 15, Jan 15)</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why self-employment tax exists (and why it stings)</h2>
<p>Employees split Social Security and Medicare with their employer: 7.65% withheld, 7.65% paid invisibly by the company. Work for yourself and you are both parties — <strong>12.4% Social Security plus 2.9% Medicare, a combined 15.3%</strong>, on top of ordinary income tax. It applies from the first dollar of profit (once you clear $400/year), which is why a modest side hustle can generate a surprising April bill if nothing was set aside.</p>
<h2>The three quirks the math has to get right</h2>
<ul>
<li><strong>The 92.35% base.</strong> SE tax isn't charged on all your profit — it's charged on 92.35% of it. That mirrors the employee world, where the employer's 7.65% share isn't part of the wages being taxed. Small mercy, but it's why the effective SE rate is 14.13% of profit, not 15.3%.</li>
<li><strong>The Social Security cap — and W-2 coordination.</strong> The 12.4% portion stops at the wage base ($176,100 in 2025). If you also have a day job, your W-2 wages use up that cap <em>first</em>, so high earners with side income may owe little or no Social Security on the side hustle — just Medicare, which never caps (and adds 0.9% above $200,000). Enter your W-2 wages above and the calculator handles it.</li>
<li><strong>Half is deductible.</strong> You deduct the employer-equivalent half of SE tax from taxable income (an above-the-line deduction — no itemizing needed). It doesn't reduce SE tax itself, but it trims the income tax bill on top.</li>
</ul>
<h2>Quarterly estimated taxes: the rhythm of self-employment</h2>
<p>No employer means no withholding, and the IRS doesn't wait until April: if you'll owe $1,000+, you're expected to prepay through <strong>quarterly estimated payments</strong> — due roughly April 15, June 15, September 15 and January 15. Underpay and you're charged interest-based penalties even if you settle in full at filing.</p>
<p>Two safe-harbor rules protect you: pay at least <strong>90% of this year's tax</strong>, or <strong>100% of last year's</strong> (110% if your AGI topped $150k). For stable earners, last year's number divided by four is the low-stress play. A practical system: skim a fixed percentage of every client payment — for most mid-bracket freelancers 25-30% covers SE plus income tax, which is exactly what this calculator's effective-rate line tells you — into a separate tax account, then pay quarterlies from there. Set your rates so tax is priced in from the start with the <a href="/calculators/freelance-hourly-rate-calculator/">freelance rate calculator</a>.</p>
<h2>Ways to legitimately shrink the bill</h2>
<ul>
<li><strong>Expenses first.</strong> SE tax is charged on <em>net</em> profit, so every legitimate business expense saves both income tax and 14.13% SE tax. Mid-bracket, each $100 of deductions saves roughly $36.</li>
<li><strong>Retirement plans for the self-employed.</strong> A solo 401(k) or SEP-IRA shelters far more than a regular IRA — up to $70,000 (2025) in a solo 401(k) between employee deferral and employer profit share. These cut income tax (not SE tax) — project the growth with the <a href="/calculators/401k-calculator/">401(k) calculator</a>.</li>
<li><strong>The S-corp question.</strong> Above roughly $80-100k of consistent profit, electing S-corp status and paying yourself a reasonable W-2 salary can move the remaining profit out of SE tax entirely. It adds payroll, a separate return and state fees — worth a professional's opinion, not a default.</li>
<li><strong>The QBI deduction.</strong> Most self-employed people currently deduct up to 20% of qualified business income for income-tax purposes (not SE tax) — another reason your true rate is lower than the sticker suggests.</li>
</ul>
<p>Estimate the income-tax side precisely with the <a href="/calculators/tax-bracket-calculator/">tax bracket calculator</a>, and see how the total load compares to employment with the <a href="/calculators/take-home-pay-calculator/">take-home pay calculator</a>.</p>
""",
        "faqs": [
            ("How much should I set aside for taxes as a freelancer?", "For most mid-bracket freelancers, 25-30% of net profit covers SE tax plus federal income tax; add your state's rate on top. This calculator's effective-rate line gives your personal number — skim that percentage of every payment into a separate account and quarterlies stop being scary."),
            ("Do I owe SE tax if freelancing is just a side gig?", "Yes — SE tax starts at $400 of annual net profit regardless of your day job. The silver lining: your W-2 wages use up the Social Security wage base first, so a well-paid employee's side income may owe only the 2.9% Medicare portion rather than the full 15.3%."),
            ("What happens if I skip quarterly estimated payments?", "The IRS charges an underpayment penalty that works like interest (currently ~8% annualized) on each quarter's shortfall — even if you pay everything at filing. Hitting a safe harbor (90% of this year or 100-110% of last year's tax) makes penalties disappear."),
            ("Does an LLC reduce self-employment tax?", "Not by itself — a single-member LLC is taxed exactly like a sole proprietor. The structure that changes SE tax is an S-corp election (through an LLC or corporation), which puts only your reasonable salary through payroll taxes. It has real costs and only pays off above roughly $80-100k of steady profit."),
        ],
    },
]
