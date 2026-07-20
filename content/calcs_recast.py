# -*- coding: utf-8 -*-
"""Mortgage recast calculator — lump sum re-amortization vs same-money prepayment vs refinance, payment relief focus."""

RECAST = [
    {
        "slug": "mortgage-recast-calculator",
        "emoji": "\U0001F4C9",
        "category": "Loans & Debt",
        "title": "Mortgage Recast Calculator — Lower the Payment, Keep the Rate",
        "h1": "Mortgage Recast Calculator",
        "blurb": "What a lump sum + re-amortization does to your payment — vs just prepaying, vs refinancing.",
        "meta_description": "Free mortgage recast calculator: apply a lump sum, re-amortize the balance over the remaining term, and see the new lower payment. Compares recasting against plain extra-payment prepayment and shows when each wins.",
        "intro": "A recast is the least-known move in the mortgage playbook: pay a lump sum toward principal, pay a ~$250 fee, and the lender re-computes your payment on the smaller balance — same rate, same payoff date, permanently lower monthly bill. No appraisal, no credit check, no closing costs. This calculator shows what your lump sum buys.",
        "fields": [
            {"id": "balance", "label": "Current mortgage balance ($)", "value": 350000},
            {"id": "rate", "label": "Interest rate (%)", "value": 6.0, "step": 0.01},
            {"id": "left", "label": "Years left on the loan", "value": 25, "step": 1},
            {"id": "lump", "label": "Lump sum to apply ($)", "value": 50000},
            {"id": "fee", "label": "Recast fee ($)", "value": 250, "hint": "typically $150-500"},
        ],
        "js": """
function calculate() {
  const B = val('balance'), r = val('rate')/100/12, yrs = Math.max(1, Math.round(val('left'))), n = yrs*12;
  const L = val('lump'), fee = Math.max(0, val('fee'));
  if (B <= 0 || L <= 0) { show('<div class="result-main">Enter a balance and a lump sum.</div>'); return; }
  if (L >= B) { show('<div class="result-main">The lump sum pays the loan off entirely — no recast needed, just request a payoff quote.</div>'); return; }
  const pay = (P, m) => r > 0 ? P * r / (1 - Math.pow(1 + r, -m)) : P / m;
  const oldPay = pay(B, n);
  const newBal = B - L;
  const newPay = pay(newBal, n);
  const relief = oldPay - newPay;
  // Option B: same lump as prepayment, keep old payment -> earlier payoff
  let bal = newBal, m2 = 0, intPre = 0;
  while (bal > 0.005 && m2 < n) { const i = bal * r; intPre += i; bal = bal + i - oldPay; m2++; }
  const monthsSaved = n - m2;
  // total interest each path
  const intRecast = newPay * n - newBal;
  const intOld = oldPay * n - B;
  const intPrepay = intPre;
  const payback = relief > 0 ? fee / relief : 0;
  show(`<div class="result-main">$${fmt(newPay,0)}/month after recasting<small>down from $${fmt(oldPay,0)} — <strong>$${fmt(relief,0)}/month of permanent relief</strong> for a $${fmt(fee,0)} fee (pays for itself in ${payback < 1 ? 'under a month' : fmt(Math.ceil(payback),0) + ' month' + (Math.ceil(payback) === 1 ? '' : 's')})</small></div>
  <table>
    <tr><th></th><th>Do nothing</th><th>Recast</th><th>Prepay, keep old payment</th></tr>
    <tr><td>Monthly payment</td><td>$${fmt(oldPay,0)}</td><td><strong>$${fmt(newPay,0)}</strong></td><td>$${fmt(oldPay,0)}</td></tr>
    <tr><td>Payoff date</td><td>${yrs} years</td><td>${yrs} years (unchanged)</td><td><strong>${Math.floor(m2/12)} yr ${m2%12} mo (${Math.floor(monthsSaved/12)} yr ${monthsSaved%12} mo sooner)</strong></td></tr>
    <tr><td>Interest from here</td><td>$${fmt(intOld,0)}</td><td>$${fmt(intRecast,0)}</td><td><strong>$${fmt(intPrepay,0)}</strong></td></tr>
    <tr><td>Interest saved vs doing nothing</td><td>—</td><td>$${fmt(intOld - intRecast,0)}</td><td><strong>$${fmt(intOld - intPrepay,0)}</strong></td></tr>
  </table>
  <p>Same $${fmt(L,0)} either way — the choice is what it buys: the <strong>recast buys monthly breathing room</strong> ($${fmt(relief,0)}/month you're no longer obligated to pay), the <strong>prepayment buys time and interest</strong> ($${fmt(intPrepay > 0 ? (intOld - intPrepay) - (intOld - intRecast) : 0,0)} more interest saved, ${Math.floor(monthsSaved/12)}+ years earlier freedom). Cash-flow stress favors the recast; wealth-maximizing favors the prepayment.</p>`);
}
""",
        "body_html": """
<h2>Recast vs refinance vs prepay: three tools, three jobs</h2>
<p>People conflate three distinct moves. A <strong>refinance</strong> replaces the loan — new rate, new term, 2-3% closing costs, full underwriting; it's the tool when <em>rates have dropped</em> (run the <a href="/calculators/mortgage-refinance-calculator/">refinance break-even</a>). A <strong>prepayment</strong> shrinks the balance while keeping the payment — the payoff date moves closer and lifetime interest falls the most; it's the tool for <em>getting debt-free faster</em> (the <a href="/calculators/extra-mortgage-payment-calculator/">extra payment calculator</a> models it). A <strong>recast</strong> shrinks the balance and re-spreads it over the <em>original</em> remaining term — the payoff date stays put, but the required monthly payment drops permanently; it's the tool for <em>monthly cash-flow relief without touching a great rate</em>. Crucially, the recast keeps your 3% pandemic-era rate intact — which a refinance would destroy.</p>
<h2>When a recast is exactly right</h2>
<ul>
<li><strong>You sold your old house after buying the new one.</strong> The classic case: you closed on the new home with a small down payment, the old home's sale lands $150,000 later, and you want the new mortgage payment sized as if you'd had that money at closing. A recast does precisely that — no refinance, no rate risk.</li>
<li><strong>A windfall arrived and cash flow is the constraint.</strong> Inheritance, bonus, RSU vesting: if the goal is a lighter monthly obligation (new baby, one income for a while, starting a business), the recast converts the lump sum into permanent monthly relief at almost zero cost.</li>
<li><strong>Your rate is below market.</strong> Refinancing to lower the payment would surrender the low rate; recasting lowers the payment while keeping it. In a 6-7% world, homeowners holding 2.5-3.5% mortgages should treat recasting as the default way to restructure.</li>
<li><strong>You want optionality, not obligation.</strong> After a recast, nothing stops you from paying the <em>old</em> amount voluntarily — the extra goes to principal and you land near the prepayment outcome anyway. The recast lowers the floor; you choose the ceiling. That asymmetry — lower required payment, same allowed payment — is why a recast is rarely a mistake if the fee is small.</li>
</ul>
<h2>The fine print</h2>
<ul>
<li><strong>Eligibility:</strong> conventional (Fannie/Freddie) loans generally allow recasting; <strong>FHA, VA and USDA loans don't</strong>, and jumbo policies vary by servicer. Call and ask for a "loan modification recast" or "re-amortization."</li>
<li><strong>Minimums:</strong> most servicers want $5,000-10,000 of principal reduction (some just require any lump plus the fee).</li>
<li><strong>Fee:</strong> typically $150-500 — compare that to $6,000-10,000 of refinance closing costs for the same payment-lowering job.</li>
<li><strong>Timing:</strong> the servicer re-amortizes after the lump posts; expect the new payment 1-2 statements later. Keep paying the old amount until it's official.</li>
<li><strong>No cash out, no rate change, no term change:</strong> a recast only ever lowers the payment on the existing structure. If you want a different rate or term, that's a refinance conversation.</li>
</ul>
<h2>The math worth staring at</h2>
<p>The counterintuitive part: <strong>recasting saves less interest than prepaying the identical sum</strong> — the table above shows why. Prepayment keeps your payment high, so the freed-up interest compounds into faster principal destruction; recasting hands that savings back to you as monthly cash instead. Neither is "better" — they're different assets. $50,000 recast into a $316/month payment cut is buying an annuity; $50,000 prepaid at 6% is earning a guaranteed 6% return (the logic of the <a href="/calculators/pay-off-debt-vs-invest-calculator/">debt vs invest comparison</a> applies directly — a below-market mortgage rate weakens the prepayment case and strengthens investing the lump instead). If the mortgage rate is high and cash flow is fine: prepay. Rate low, cash flow tight: recast. Rate low, cash flow fine: consider investing the lump and doing neither.</p>
""",
        "faqs": [
            ("Does a recast change my interest rate or payoff date?", "Neither. The rate is untouched and the payoff date stays exactly where it was — the smaller balance is simply re-spread over the same remaining months, which is what drops the payment. That's the defining difference from refinancing (new rate, new term) and from prepaying (same payment, earlier payoff)."),
            ("Can any mortgage be recast?", "Conventional loans backed by Fannie Mae or Freddie Mac generally can, for a $150-500 fee after a minimum principal payment (often $5,000-10,000). FHA, VA and USDA loans cannot be recast — for those, the options are prepaying (keeps the payment, shortens the loan) or refinancing. Jumbo loans depend on the servicer's policy."),
            ("Is recasting better than refinancing to lower my payment?", "If your rate is at or below market, almost always — a recast costs ~$250 and keeps the rate, versus thousands in closing costs and a new (likely higher) rate. Refinancing only wins the payment-lowering contest when rates have dropped meaningfully below what you're paying, or you need cash out or a term change, which a recast can't do."),
            ("Why did my payment barely drop after my recast?", "Payment relief scales with the share of the balance you paid off. A $20,000 lump on a $400,000 balance is 5% — so the payment falls roughly 5%, maybe $120 on a $2,400 payment. For dramatic relief you need a dramatic principal cut (the post-home-sale recast works because it's often 20-40% of the balance). Run the exact numbers before paying the fee."),
            ("Should I recast or just invest the lump sum?", "Compare the mortgage rate to what the money could earn. Recasting a 3% mortgage 'earns' 3% guaranteed plus cash-flow relief; a diversified portfolio has historically earned more over long horizons, with risk. High rate (6.5%+): the recast/prepay side strengthens. Low rate with solid cash flow: investing the lump usually builds more wealth — the debt-vs-invest calculator makes the comparison concrete."),
        ],
    },
]
