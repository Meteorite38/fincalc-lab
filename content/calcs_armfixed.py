# -*- coding: utf-8 -*-
"""ARM vs fixed mortgage — month-by-month simulation over the buyer's real horizon, plus a 2/2/5-cap worst case."""

ARMFIXED = [
    {
        "slug": "arm-vs-fixed-mortgage-calculator",
        "emoji": "\u2696\uFE0F",
        "category": "Mortgages & Home",
        "title": "ARM vs Fixed Mortgage Calculator — Priced Over Your Real Horizon",
        "h1": "ARM vs Fixed Mortgage Calculator",
        "blurb": "ARM discount vs 30-year fixed over your real horizon — with the cap-out worst case.",
        "meta_description": "Free ARM vs fixed-rate mortgage calculator: compare a 5/6, 7/6 or 10/6 ARM against a 30-year fixed over the years you actually expect to keep the loan. Includes the worst-case path under standard 2/2/5 rate caps.",
        "intro": "The ARM discount is real money — often half a point or more — but it has an expiry date. Whether the gamble pays depends almost entirely on one input lenders can't know: how long you'll actually keep the loan. This calculator prices both loans over your real horizon, your own rate guess, and the contractual worst case.",
        "fields": [
            {"id": "loan", "label": "Loan amount ($)", "value": 400000},
            {"id": "fixedrate", "label": "30-year fixed rate offered (%)", "value": 6.6, "step": 0.01},
            {"id": "armrate", "label": "ARM intro rate (%)", "value": 5.9, "step": 0.01},
            {"id": "fixedper", "label": "ARM fixed period", "type": "select", "value": "7",
             "options": [("3", "3 years (3/6 ARM)"), ("5", "5 years (5/6 ARM)"), ("7", "7 years (7/6 ARM)"), ("10", "10 years (10/6 ARM)")]},
            {"id": "adjrate", "label": "Your guess: rate after adjustment (%)", "value": 7.0, "step": 0.05, "hint": "what the ARM resets to, on average"},
            {"id": "horizon", "label": "Years you expect to keep this loan", "value": 8, "step": 1, "hint": "sell or refinance ends the loan"},
        ],
        "js": """
function simLoan(P, n, rateFn, months) {
  // rateFn(month) -> annual rate; returns {paid, balance, firstPay, lastPay}
  let bal = P, paid = 0, firstPay = 0, lastPay = 0;
  let curRate = rateFn(0), pay = pmt(bal, curRate, n);
  firstPay = pay;
  for (let m = 0; m < months && bal > 0.005; m++) {
    const rNow = rateFn(m);
    if (rNow !== curRate) { curRate = rNow; pay = pmt(bal, curRate, n - m); }
    const i = bal * curRate / 12;
    const prin = Math.min(bal, pay - i);
    paid += i + prin;
    bal -= prin;
    lastPay = pay;
  }
  return { paid: paid, balance: Math.max(0, bal), firstPay: firstPay, lastPay: lastPay };
}
function pmt(P, annual, nLeft) {
  const r = annual / 12;
  if (nLeft <= 0) return P;
  return r > 0 ? P * r / (1 - Math.pow(1 + r, -nLeft)) : P / nLeft;
}
function calculate() {
  const P = val('loan'), rF = val('fixedrate')/100, rA0 = val('armrate')/100;
  const fp = parseInt(document.getElementById('fixedper').value, 10) * 12;
  const rAdj = val('adjrate')/100;
  const hz = Math.min(30, Math.max(1, Math.round(val('horizon')))) * 12;
  if (P <= 0 || rF <= 0 || rA0 <= 0) { show('<div class="result-main">Enter a loan amount and both rates.</div>'); return; }
  const N = 360;
  const fixed = simLoan(P, N, () => rF, hz);
  const arm = simLoan(P, N, (m) => m < fp ? rA0 : rAdj, hz);
  // worst case under 2/2/5 caps: +2 at first reset, +2 each year after, lifetime cap intro+5
  const capMax = rA0 + 0.05;
  const worstFn = (m) => {
    if (m < fp) return rA0;
    const yearsIn = Math.floor((m - fp) / 12);
    return Math.min(capMax, rA0 + 0.02 + 0.02 * yearsIn);
  };
  const worst = simLoan(P, N, worstFn, hz);
  const costF = fixed.paid + fixed.balance - P;
  const costA = arm.paid + arm.balance - P;
  const costW = worst.paid + worst.balance - P;
  const diff = costF - costA;
  const diffW = costF - costW;
  const introSave = fixed.firstPay - arm.firstPay;
  const soldInIntro = hz <= fp;
  const verdict = soldInIntro
    ? `You plan to be out before the ARM ever adjusts — the ARM wins by <strong>$${fmt(diff,0)}</strong> with no rate risk on your timeline (the risk is your timeline changing).`
    : (diff > 0 && diffW > 0
      ? `The ARM wins even if rates cap out: <strong>$${fmt(diff,0)}</strong> ahead at your guess, still $${fmt(diffW,0)} ahead in the worst case.`
      : (diff > 0
        ? `At your rate guess the ARM saves <strong>$${fmt(diff,0)}</strong> — but a cap-out flips it to <strong>$${fmt(-diffW,0)} behind</strong>. You're being paid $${fmt(introSave,0)}/month to carry that tail risk.`
        : `The fixed loan wins by <strong>$${fmt(-diff,0)}</strong> at your own rate guess — at these numbers the ARM discount doesn't survive the adjustment.`));
  show(`<div class="result-main">${diff > 0 ? 'ARM ahead by $' + fmt(diff,0) : 'Fixed ahead by $' + fmt(-diff,0)}<small>true cost over ${Math.round(hz/12)} years — interest paid, after crediting each loan's remaining balance</small></div>
  <table>
    <tr><th></th><th>30-yr fixed @ ${fmt(rF*100,2)}%</th><th>${fp/12}/6 ARM @ ${fmt(rA0*100,2)}%</th></tr>
    <tr><td>Monthly payment, years 1–${fp/12}</td><td>$${fmt(fixed.firstPay,0)}</td><td>$${fmt(arm.firstPay,0)} <small>(&minus;$${fmt(introSave,0)})</small></td></tr>
    ${soldInIntro ? '' : `<tr><td>Payment after adjustment (your guess ${fmt(rAdj*100,2)}%)</td><td>$${fmt(fixed.firstPay,0)}</td><td>$${fmt(arm.lastPay,0)}</td></tr>`}
    <tr><td>Interest cost over ${Math.round(hz/12)} yrs</td><td>$${fmt(costF,0)}</td><td>$${fmt(costA,0)}</td></tr>
    <tr><td>Loan balance left at year ${Math.round(hz/12)}</td><td>$${fmt(fixed.balance,0)}</td><td>$${fmt(arm.balance,0)}</td></tr>
    <tr><td>Worst case (2/2/5 caps, rate → ${fmt(capMax*100,2)}%)</td><td>—</td><td>$${fmt(costW,0)} cost &middot; payment up to $${fmt(worst.lastPay,0)}</td></tr>
  </table>
  <p>${verdict}</p>`);
}
""",
        "body_html": """
<h2>What the ARM discount is actually buying</h2>
<p>A 7/6 ARM quoted half a point below the 30-year fixed isn't generosity — it's a trade. The lender gives up income in the first seven years in exchange for handing you the interest-rate risk afterward. The fixed-rate borrower pays a premium for certainty they may never use: <strong>the median mortgage lasts roughly 7-10 years</strong> before a sale or refinance ends it. That's the whole decision in one sentence — if your realistic horizon fits inside the ARM's fixed period, the discount is nearly free money; if you might stay past it, you're short volatility and should know the worst case before signing.</p>
<h2>Reading an ARM quote: 7/6, margins, and 2/2/5</h2>
<ul>
<li><strong>7/6 ARM</strong> = rate fixed for 7 years, then adjusts every 6 months. Modern ARMs adjust off <strong>SOFR plus a margin</strong> (typically 2.5-3%): index moves, your rate follows.</li>
<li><strong>Caps come as three numbers</strong>, e.g. 2/2/5: the first adjustment can't move more than 2 points, each later adjustment 2 points (per year), and the lifetime cap is 5 points above the start rate. A 5.9% ARM can therefore legally reach 10.9% — that's the number to stress-test, and the worst-case row in this calculator walks that exact path.</li>
<li><strong>Today's ARMs are not 2008's.</strong> The toxic features — negative amortization, interest-only teasers, prepayment penalties, qualification at the teaser rate — were regulated away. Lenders now underwrite you at the fully-indexed rate. The product is honest; the risk is just visible now instead of hidden.</li>
</ul>
<h2>How to think about the horizon input</h2>
<p>It's the input that decides everything, so pressure-test it. "We'll move in five years" is a plan, not a fact — job changes fall through, school districts grow on you, and 2021-2023 taught everyone that refinancing out of an ARM assumes rates will cooperate. A useful discipline: take the ARM only if <em>both</em> futures are acceptable — the one where you sell on schedule and pocket the savings, and the one where you're still in the house at the cap-out payment. If the second future breaks the budget, the fixed premium is cheap insurance. Run the payment you'd face against your income with the <a href="/calculators/home-affordability-calculator/">home affordability calculator</a>.</p>
<h2>Banking the difference (the version that actually wins)</h2>
<p>The ARM saves money in two channels during the intro period: the lower payment, and faster principal paydown (same payment arithmetic, lower rate — more of each dollar hits principal). The disciplined play is to <strong>keep paying the fixed-loan payment on the ARM</strong>: the extra $150-200 a month goes straight to principal, shrinking the balance the adjustment will eventually apply to. Done consistently over a 7-year intro period, this cuts thousands off the worst case — the <a href="/calculators/extra-mortgage-payment-calculator/">extra payment calculator</a> shows the mechanics. The undisciplined play — absorbing the lower payment into lifestyle — leaves you with the full balance and the full rate risk.</p>
<h2>Where each loan wins</h2>
<ul>
<li><strong>ARM favors:</strong> short expected tenure (starter home, likely relocation), high current rate environments where the discount is fat and future refinancing is plausible, borrowers with the income cushion to absorb the cap-out payment, and jumbo borrowers (ARM discounts run larger above conforming limits).</li>
<li><strong>Fixed favors:</strong> the forever home, tight budgets where a $700 payment jump is unaffordable rather than unpleasant, low-rate environments (locking cheap money for 30 years is a gift), and anyone who values never thinking about SOFR again.</li>
<li><strong>Either way</strong>, compare the whole offer, not just the rate — points and fees shift the math; the <a href="/calculators/mortgage-points-calculator/">points calculator</a> and <a href="/calculators/loan-comparison-calculator/">loan comparison calculator</a> handle those trades. And if you're weighing loan <em>length</em> rather than rate type, that's the <a href="/calculators/15-vs-30-year-mortgage-calculator/">15 vs 30 year question</a>.</li>
</ul>
""",
        "faqs": [
            ("What happens when my ARM adjusts?", "The rate resets to the index (SOFR for modern ARMs) plus your contractual margin, limited by the caps — and the loan re-amortizes: your new payment is whatever pays off the remaining balance over the remaining term at the new rate. Nothing requires action from you, but the reset notice arrives months in advance, which is the natural moment to compare refinancing."),
            ("Can I refinance an ARM before it adjusts?", "Yes — modern conforming ARMs have no prepayment penalty, so you can refinance into a fixed loan (or sell) any time. The catch is that refinancing needs rates, home equity and your credit to all cooperate at that future date. Treat 'I'll just refi' as a hope, not a plan — the worst-case row exists because sometimes none of the three cooperate."),
            ("Are ARMs dangerous like they were in 2008?", "The 2008 damage came from features that no longer exist in mainstream lending: teaser rates lenders qualified you at, negative amortization, and interest-only periods that hid the true cost. Post-2014 rules require underwriting at the fully-indexed rate with full documentation. Today's ARM risk is transparent — the caps spell out the exact worst case, which this calculator prices."),
            ("Why is the ARM rate sometimes barely below the fixed rate?", "The discount widens and narrows with the yield curve. When short and long rates are close (a flat curve), lenders gain little from the ARM structure and the discount shrinks — sometimes to nothing, occasionally inverting. When the gap is under ~0.25%, the fixed loan's certainty usually wins by default; the discount just isn't paying you enough to carry the risk."),
            ("Do ARM caps limit my payment or just the rate?", "The standard caps (like 2/2/5) limit the interest rate. The payment then follows from re-amortization, so a 2-point rate jump on a large balance can still raise the payment 15-25%. Payment-cap ARMs — which limited the payment while letting interest accrue — were the negative-amortization products regulators eliminated; you won't see them from mainstream lenders."),
        ],
    },
]
