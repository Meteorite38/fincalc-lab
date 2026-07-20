# -*- coding: utf-8 -*-
"""Balance transfer calculator — 0% promo vs staying put, transfer fee math, payoff-within-promo target payment."""

BALXFER = [
    {
        "slug": "balance-transfer-calculator",
        "emoji": "\U0001F4B3",
        "category": "Debt & Credit",
        "title": "Balance Transfer Calculator — Is the 0% Offer Worth the Fee?",
        "h1": "Balance Transfer Calculator",
        "blurb": "0% promo vs staying put — fee included, with the payment that clears it in time.",
        "meta_description": "Free balance transfer calculator: compare a 0% APR offer (with its 3-5% transfer fee) against staying on your current card. See total interest both ways, the break-even, and the exact monthly payment that zeroes the balance before the promo ends.",
        "intro": "A 0% balance transfer can wipe out years of credit card interest — or just add a 3-5% fee to debt you still won't pay off. The difference is arithmetic: fee versus interest saved, and whether your monthly payment actually clears the balance before the promo rate expires. This calculator runs both futures side by side.",
        "fields": [
            {"id": "balance", "label": "Credit card balance to transfer ($)", "value": 6000},
            {"id": "apr", "label": "Current card APR (%)", "value": 24.99, "step": 0.01},
            {"id": "fee", "label": "Balance transfer fee (%)", "value": 3, "step": 0.5, "hint": "typically 3-5% of the amount moved"},
            {"id": "promo", "label": "0% promo period (months)", "value": 15, "step": 1, "hint": "commonly 12, 15, 18 or 21"},
            {"id": "gotoapr", "label": "APR after the promo ends (%)", "value": 27.99, "step": 0.01, "hint": "the 'go-to' rate in the offer"},
            {"id": "payment", "label": "What you'll pay per month ($)", "value": 300},
        ],
        "js": """
function simulate(startBal, monthlyRates, pay) {
  // monthlyRates: function(monthIndex) -> monthly rate; returns {months, interest} or null if payment too small
  let b = startBal, interest = 0, m = 0;
  while (b > 0.005 && m < 600) {
    const i = b * monthlyRates(m);
    if (pay <= i && monthlyRates(m) > 0) return null;
    interest += i;
    b = b + i - pay;
    m++;
  }
  return m >= 600 ? null : { months: m, interest: interest };
}
function calculate() {
  const B = val('balance'), aprM = val('apr')/100/12, feePct = Math.max(0, val('fee'))/100;
  const promo = Math.max(0, Math.round(val('promo'))), gotoM = val('gotoapr')/100/12, pay = val('payment');
  if (B <= 0 || pay <= 0) { show('<div class="result-main">Enter a balance and a monthly payment above zero.</div>'); return; }
  const stay = simulate(B, () => aprM, pay);
  const fee = B * feePct;
  const xferBal = B + fee;
  const xfer = simulate(xferBal, (m) => m < promo ? 0 : gotoM, pay);
  const clearPay = promo > 0 ? xferBal / promo : xferBal;
  if (!stay) {
    show(`<div class="result-main">$${fmt(pay,0)}/month never clears this card<small>at ${fmt(aprM*1200,2)}% APR the interest alone is $${fmt(B*aprM,0)}/month — a 0% transfer isn't optional, it's a lifeline</small></div>
    <p>On the transfer card, $${fmt(pay,0)}/month ${xfer ? `pays off the $${fmt(xferBal,0)} (balance + $${fmt(fee,0)} fee) in <strong>${xfer.months} months</strong> with $${fmt(xfer.interest,0)} of post-promo interest` : 'still is not enough once the promo ends — raise the payment'}.
    To finish <strong>inside the ${promo}-month 0% window</strong> and pay no interest at all, pay <strong>$${fmt(clearPay,0)}/month</strong>.</p>`);
    return;
  }
  if (!xfer) {
    show(`<div class="result-main">Payment too small for the transfer to work<small>$${fmt(pay,0)}/month can't outrun the ${fmt(gotoM*1200,2)}% go-to APR after month ${promo}</small></div>
    <p>Staying put costs $${fmt(stay.interest,0)} in interest over ${stay.months} months. For the transfer to beat that, pay at least $${fmt(clearPay,0)}/month — that clears the full $${fmt(xferBal,0)} within the promo window with zero interest.</p>`);
    return;
  }
  const xferTotal = xfer.interest + fee;
  const saved = stay.interest - xferTotal;
  const inPromo = xfer.months <= promo;
  const verdict = saved > 0
    ? `Transfer wins: <strong>$${fmt(saved,0)} saved</strong>`
    : `Staying put wins by $${fmt(-saved,0)} — the fee outweighs the interest saved at this payment level`;
  show(`<div class="result-main">${saved > 0 ? '$' + fmt(saved,0) + ' saved by transferring' : 'Keep the current card'}<small>fee of $${fmt(fee,0)} vs $${fmt(stay.interest,0)} interest if you stay — net ${saved > 0 ? 'savings' : 'loss'} $${fmt(Math.abs(saved),0)}</small></div>
  <table>
    <tr><th></th><th>Stay on current card</th><th>Transfer to 0% card</th></tr>
    <tr><td>Interest paid</td><td>$${fmt(stay.interest,0)}</td><td>$${fmt(xfer.interest,0)}${inPromo ? ' (cleared inside the promo)' : ' (after promo ends)'}</td></tr>
    <tr><td>Transfer fee</td><td>—</td><td>$${fmt(fee,0)}</td></tr>
    <tr><td><strong>Total cost</strong></td><td><strong>$${fmt(stay.interest,0)}</strong></td><td><strong>$${fmt(xferTotal,0)}</strong></td></tr>
    <tr><td>Debt-free in</td><td>${stay.months} months</td><td>${xfer.months} months</td></tr>
    <tr><td>Verdict</td><td colspan="2">${verdict}</td></tr>
  </table>
  <p>${inPromo
    ? `Your $${fmt(pay,0)}/month clears the balance in month ${xfer.months} — <strong>inside the 0% window</strong>, so the fee is the only cost.`
    : `Heads up: at $${fmt(pay,0)}/month about $${fmt(Math.max(0, xferBal - pay*promo),0)} will still be owed when the promo ends and the ${fmt(gotoM*1200,2)}% go-to rate kicks in. To finish inside the window, pay <strong>$${fmt(clearPay,0)}/month</strong>.`}</p>`);
}
""",
        "body_html": """
<h2>The trade: one fee now instead of interest every month</h2>
<p>A balance transfer moves debt from a card charging 20-30% APR to a new card charging <strong>0% for a promotional window</strong> — usually 12 to 21 months — in exchange for a one-time fee of 3-5% of the amount moved. On a $6,000 balance at 25% APR, interest runs about $125 a month; a 3% fee is $180 once. If the transfer buys you even two months of avoided interest, you're ahead — <em>provided the balance actually shrinks during the window</em>.</p>
<h2>The one number that decides everything</h2>
<p>Divide the transferred balance (including the fee) by the promo length. That's the monthly payment that reaches zero the month the 0% rate dies. $6,180 over 15 months is <strong>$412/month</strong>. Pay that and the fee is your only cost. Pay half of it and you'll face the leftover at the card's go-to rate — typically 25-30%, often <em>higher</em> than the card you left. The calculator shows this target payment for your numbers; treat it as the real price of admission before you apply.</p>
<h2>Traps that turn a good deal bad</h2>
<ul>
<li><strong>New purchases usually aren't 0%.</strong> Many transfer cards charge full APR on new spending — and until the promo balance is paid, payments often go to the 0% portion first (minimums, at least). Use the transfer card for the old debt only; put daily spending elsewhere.</li>
<li><strong>One late payment can void the promo.</strong> Card agreements commonly allow the issuer to cancel the 0% rate after a missed payment. Set up autopay for at least the minimum on day one.</li>
<li><strong>The clock starts at account opening</strong>, not when the transfer posts. Transfers can take 1-2 weeks; keep paying the old card until you see the balance move, or a late fee lands on top of everything.</li>
<li><strong>Deferred interest is a different product.</strong> Store-card "no interest if paid in full" offers charge back <em>all</em> the interest from day one if any balance survives the window. True bank balance-transfer cards don't do this — but read which one you're holding.</li>
<li><strong>The debt spiral risk is behavioral.</strong> The classic failure: transfer the balance, feel relief, and run the old card back up. Now there are two balances. Close or freeze the old card if that pattern sounds familiar.</li>
</ul>
<h2>Balance transfer vs the alternatives</h2>
<p>A transfer is one of three standard moves against card debt. A <strong>consolidation loan</strong> (fixed rate, fixed term — modeled in the <a href="/calculators/debt-consolidation-calculator/">debt consolidation calculator</a>) suits balances too large to clear in 18 months, trading 0% for certainty. <strong>Aggressive paydown in place</strong> — ordered by the <a href="/calculators/debt-snowball-vs-avalanche-calculator/">snowball vs avalanche calculator</a> — avoids new credit entirely. If you're juggling several cards, transfers help most when the weighted rate across them is high and the total is clearable within a promo window. And after the dust settles, the <a href="/calculators/credit-card-payoff-calculator/">credit card payoff calculator</a> keeps the remaining plan honest.</p>
<h2>What it does to your credit score</h2>
<p>Short term: a hard inquiry (a few points, fades in months) and a new account lowering your average age. Working in your favor: the new card's credit line drops your overall <a href="/calculators/credit-utilization-calculator/">utilization ratio</a> — often the bigger effect. The score dip is usually modest and temporary; carrying 25% APR debt for years is the costlier problem. One practical note: issuers rarely approve transfers between their own cards (Chase to Chase won't fly), and transfer limits may be below your full balance — moving <em>part</em> of the debt still helps, just run the numbers on the remainder.</p>
""",
        "faqs": [
            ("Is a balance transfer fee ever waived?", "A few cards offer no-fee transfers (often credit-union cards, or intro no-fee windows in the first 60 days), but they usually pair with shorter 0% periods. A 3% fee with 18 months at 0% frequently beats a no-fee card with 6 months — total cost over the whole payoff is what matters, which is exactly what this calculator compares."),
            ("Does transferring a balance hurt my credit score?", "Slightly and briefly: a hard inquiry and a new account each shave a few points. But the added credit line typically lowers your utilization ratio, which helps. Most people who pay the debt down see their score higher within a few months than where it started."),
            ("Can I transfer a balance between two cards from the same bank?", "Almost never — issuers block transfers between their own products, since they'd be paying themselves. Pick a card from a different bank than the one holding your debt."),
            ("What happens if I don't pay it off before the 0% period ends?", "The leftover balance starts accruing at the card's go-to APR (often 25-30%) from that point forward. With a true balance-transfer card there's no retroactive interest — that 'charge it all back' behavior belongs to deferred-interest store financing, a different product. Still, the go-to rate is usually worse than what you left, so plan the payment to finish inside the window."),
            ("How much can I actually transfer?", "Up to the new card's transfer limit, which is often 75-100% of the credit line — and the line itself depends on your income and score. If approval comes in below your balance, transfer what you can: cutting the 25% APR portion of your debt in half still saves real money."),
        ],
    },
]
