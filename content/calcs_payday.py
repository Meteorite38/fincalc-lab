# -*- coding: utf-8 -*-
"""Payday loan true cost — fee-to-APR conversion, rollover spiral simulation, ranked cheaper alternatives."""

PAYDAY = [
    {
        "slug": "payday-loan-calculator",
        "emoji": "\u26A0\uFE0F",
        "category": "Debt & Credit",
        "title": "Payday Loan Calculator — The Real APR and the Rollover Spiral",
        "h1": "Payday Loan Calculator",
        "blurb": "What the fee works out to as an APR, what rollovers cost, and every cheaper alternative ranked.",
        "meta_description": "Free payday loan calculator: convert the fee into its true APR (typically 300-600%), simulate the rollover spiral that traps most borrowers, and compare every cheaper alternative — PALs, payment plans, even credit card cash advances.",
        "intro": "A \u201c$15 per $100\u201d payday loan sounds like 15%. Over two weeks, it's a 391% APR — and the industry's own economics depend on borrowers who can't pay on time and roll over, paying the fee again and again on the same principal. This calculator shows the true rate, prices the spiral, and ranks the alternatives.",
        "fields": [
            {"id": "amount", "label": "Amount borrowed ($)", "value": 400},
            {"id": "fee", "label": "Fee per $100 borrowed ($)", "value": 15, "step": 1, "hint": "$10-30 typical; state caps vary"},
            {"id": "term", "label": "Loan term (days)", "value": 14, "step": 1},
            {"id": "rolls", "label": "Times you might roll it over", "value": 4, "step": 1, "hint": "the average borrower re-borrows for ~5 months"},
        ],
        "js": """
function calculate() {
  const A = val('amount'), feeper = Math.max(0, val('fee'));
  const days = Math.max(1, Math.round(val('term'))), rolls = Math.max(0, Math.round(val('rolls')));
  if (A <= 0) { show('<div class="result-main">Enter an amount borrowed.</div>'); return; }
  const fee = A * feeper / 100;
  const apr = (fee / A) * (365 / days) * 100;
  const totalFees = fee * (1 + rolls);
  const monthsTrapped = Math.round((days * (1 + rolls)) / 30 * 10) / 10;
  const feePctOfLoan = totalFees / A * 100;
  // alternatives on the same amount & timeline
  const altDays = days * (1 + rolls);
  const cardAdv = A * 0.05 + A * 0.29 * altDays / 365; // 5% fee + ~29% APR
  const pal = A * 0.28 * altDays / 365; // federal credit union PAL cap 28%
  const persLoan = A * 0.12 * Math.max(altDays, 90) / 365; // small personal loan ~12%, min 3-mo
  show(`<div class="result-main">${fmt(apr,0)}% APR<small>a $${fmt(fee,0)} fee on $${fmt(A,0)} for ${days} days &middot; roll it ${rolls}× and the fees hit <strong>$${fmt(totalFees,0)}</strong> — ${fmt(feePctOfLoan,0)}% of what you borrowed</small></div>
  <table>
    <tr><td>Due on payday</td><td>$${fmt(A + fee,0)} (${days} days from now)</td></tr>
    <tr><td>Fee as an annual rate</td><td><strong>${fmt(apr,0)}% APR</strong> — card debt is ~25%, personal loans ~12%</td></tr>
    <tr><td>After ${rolls} rollover${rolls === 1 ? '' : 's'} (~${monthsTrapped} months)</td><td>$${fmt(totalFees,0)} of fees paid, <strong>still owing the full $${fmt(A,0)}</strong></td></tr>
  </table>
  <table>
    <tr><th>Same $${fmt(A,0)} for ~${Math.round(altDays)} days via&hellip;</th><th>Approx. cost</th></tr>
    <tr><td>Credit union PAL (28% APR cap)</td><td>$${fmt(pal,0)}</td></tr>
    <tr><td>Small personal loan (~12%)</td><td>$${fmt(persLoan,0)}</td></tr>
    <tr><td>Credit card cash advance (5% fee + ~29%)</td><td>$${fmt(cardAdv,0)} — bad, and still ${cardAdv < totalFees ? fmt(totalFees/cardAdv,1) + '× cheaper' : 'comparable'}</td></tr>
    <tr><td>The payday loan</td><td><strong>$${fmt(totalFees,0)}</strong></td></tr>
  </table>
  <p>The two-week structure is the product: the fee looks small against payday, but most borrowers can't spare $${fmt(A + fee,0)} from one check — so they pay $${fmt(fee,0)} to push it back, again and again. Pricing it as an APR is what breaks the illusion.</p>`);
}
""",
        "body_html": """
<h2>How the fee becomes 391%</h2>
<p>The arithmetic is one line: a $15-per-$100 fee over 14 days is 15% &times; (365 &divide; 14) &asymp; <strong>391% annualized</strong>. State-capped \"cheap\" versions at $10 run ~260%; the $25-30 end passes 650%. The industry objects that APR is unfair for a two-week product — which would be true if the product lasted two weeks. It doesn't: regulators' own data shows <strong>the typical borrower stays in payday debt about five months of the year</strong>, re-paying the fee every cycle while the principal never shrinks. Over the loan's <em>actual</em> life, APR is exactly the right lens — and by that lens this is the most expensive legal credit in America.</p>
<h2>The rollover spiral, mechanically</h2>
<p>Borrow $400 against next Friday's check because this week came up short. Friday arrives; repaying $460 would leave the <em>next</em> week short — so you pay the $60 fee alone and roll the $400. Nothing was repaid; the meter reset. Four rollovers in, you've paid $300 of fees and owe exactly what you started with. The structural trap: the loan is due in full on a date chosen for the lender's collection convenience (payday), not sized to what the borrower's budget can actually release per cycle. Installment structures — even expensive ones — amortize; payday loans just reset. That's why the CFPB found the majority of loans go to borrowers in sequences of 10+, and why lenders cluster where <a href="/articles/stop-living-paycheck-to-paycheck/">paycheck-to-paycheck</a> households live.</p>
<h2>The alternatives, best to worst</h2>
<ul>
<li><strong>Ask the biller first.</strong> Utilities, hospitals, landlords and even the IRS run payment plans — usually free or near-free. A five-minute call routinely beats 391%.</li>
<li><strong>Credit union PALs:</strong> federal credit unions offer Payday Alternative Loans — $200-2,000, APR capped at 28%, small application fee, membership sometimes same-day. The purpose-built replacement.</li>
<li><strong>Employer advances and EWA apps:</strong> earned-wage-access tools front money you've already worked for at low or tip-based cost; many payroll departments still do old-fashioned advances free.</li>
<li><strong>A small personal loan or 0% card offer</strong> for slightly larger needs — see the <a href="/calculators/loan-comparison-calculator/">loan comparison calculator</a>.</li>
<li><strong>A credit card — even a cash advance.</strong> Carrying a balance at 25% or an advance at ~29%+5% is bad money management and <em>still several times cheaper</em> than the spiral. When the honest choice is bad vs catastrophic, take bad.</li>
<li><strong>Genuinely last resorts</strong> — pawn (loses the item, not the credit score), asking family with a written plan — both still cheaper than sequence #6 of a payday loan.</li>
</ul>
<h2>If you're already in the spiral</h2>
<p>Three exits, in order of preference. <strong>Check your state's rules</strong> — many mandate free extended payment plans (EPPs) that convert the balance into installments at no extra fee; lenders don't advertise this, so ask in writing. <strong>Refinance the balance away</strong> — a PAL or small personal loan that pays off the payday lender converts 400% into 28% overnight; the <a href="/calculators/debt-consolidation-calculator/">consolidation calculator</a> shows the effect. <strong>Prioritize ruthlessly</strong> — payday loans are unsecured: they can't evict you, repossess the car, or cut the power. Rent, utilities, food, transport and secured debts come first; a defaulted payday loan is collections and credit damage, which is survivable — a lost home isn't. Then rebuild the buffer that prevents the next one: the <a href="/calculators/emergency-fund-calculator/">emergency fund calculator</a> sizes it, and even $500 breaks most cycles, since the median payday loan is under $400.</p>
<h2>The buffer is the real fix</h2>
<p>Payday loans are a symptom: cash-flow volatility with zero margin. The durable exit is boring — a starter emergency fund (even tiny), bills moved to align with paydays (most billers will shift due dates on request), a <a href="/calculators/budget-calculator/">budget</a> that sees the shortfall coming two weeks early, and where possible attacking the income side. None of that helps on the Tuesday the car dies — that's what the alternatives list is for — but every $100 of buffer built afterward permanently retires a future $60 fee. At the rates involved, <strong>building your own float is the highest-return investment available to anyone living check to check</strong>.</p>
""",
        "faqs": [
            ("Why is the APR so high if the fee is only $15?", "Because the fee covers only 14 days. Annualized — the only way to compare against cards (25%) or personal loans (12%) — $15 per $100 per two weeks is 391%. And since the average borrower re-borrows for months, the annualized rate reflects what people actually pay, not a theoretical worst case."),
            ("Do payday loans build credit?", "No — payday lenders don't report on-time payments to the major bureaus, so repaying perfectly builds nothing. Defaults, however, get sold to collectors who do report. It's the worst of both worlds: no upside for paying, full downside for not. A credit-builder loan or secured card does the credit-building job at a tiny fraction of the cost."),
            ("Can a payday lender garnish my wages or arrest me?", "No arrest — debtors' prisons don't exist, and threatening jail violates federal collection law. Garnishment requires them to sue and win first, which many don't pursue on small balances. What they will do: hammer the debit authorization you signed (racking up your bank's NSF fees — revoke it in writing with your bank if needed), sell to collectors, and damage your credit. Unpleasant, but survivable — unlike skipping rent to pay them."),
            ("What's an extended payment plan (EPP)?", "In many states, payday lenders must offer — free, if you ask before default — a conversion of your balance into several equal installments with no new fees. It's the single cheapest exit from a rollover cycle, and it's deliberately under-advertised. Ask for it in writing, citing your state's rule; the lender's license depends on complying."),
            ("Are online payday loans different from storefront ones?", "Often worse: rates at the high end, aggressive auto-debit practices, and some operate through tribal or offshore structures claiming exemption from state caps — enforcement against them is harder. Some states' caps make storefront loans merely expensive; unlicensed online lenders can be predatory without limit. If it's not licensed in your state, the loan may even be legally void — check your regulator's list before borrowing, or better, use a PAL."),
        ],
    },
]
