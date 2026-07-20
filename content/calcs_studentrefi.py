# -*- coding: utf-8 -*-
"""Student loan refinance — old vs new payment/interest, federal-protection warning gate, same-payment early-payoff mode."""

STUDENTREFI = [
    {
        "slug": "student-loan-refinance-calculator",
        "emoji": "\U0001F393",
        "category": "Debt & Credit",
        "title": "Student Loan Refinance Calculator — Savings vs What You Give Up",
        "h1": "Student Loan Refinance Calculator",
        "blurb": "New rate vs old: monthly and lifetime savings — and the federal protections a refi permanently burns.",
        "meta_description": "Free student loan refinance calculator: compare your current balance and rate against a refinance offer — monthly payment, total interest, keep-paying-the-same payoff acceleration — plus the federal protections refinancing permanently gives up.",
        "intro": "Refinancing student debt is a clean trade on private loans and a one-way door on federal ones: a lower rate saves real interest, but refinancing federal loans permanently surrenders income-driven plans, forgiveness tracks and hardship pauses. This calculator prices both sides — the savings and the exit.",
        "fields": [
            {"id": "balance", "label": "Current balance ($)", "value": 40000},
            {"id": "oldrate", "label": "Current rate (%)", "value": 6.8, "step": 0.01},
            {"id": "oldyears", "label": "Years left at current pace", "value": 10, "step": 1},
            {"id": "newrate", "label": "Refinance offer rate (%)", "value": 5.2, "step": 0.01},
            {"id": "newyears", "label": "New loan term (years)", "value": 10, "step": 1},
            {"id": "fedtype", "label": "Are these federal loans?", "type": "select", "value": "yes",
             "options": [("yes", "Yes — federal (Direct/FFEL)"), ("no", "No — already private")]},
        ],
        "js": """
function calculate() {
  const B = val('balance'), r1 = val('oldrate')/100/12, y1 = Math.max(1, Math.round(val('oldyears')));
  const r2 = val('newrate')/100/12, y2 = Math.max(1, Math.round(val('newyears')));
  const fed = document.getElementById('fedtype').value === 'yes';
  if (B <= 0) { show('<div class="result-main">Enter a balance.</div>'); return; }
  const n1 = y1*12, n2 = y2*12;
  const pay = (P, r, n) => r > 0 ? P * r / (1 - Math.pow(1 + r, -n)) : P / n;
  const p1 = pay(B, r1, n1), p2 = pay(B, r2, n2);
  const int1 = p1*n1 - B, int2 = p2*n2 - B;
  const saveMo = p1 - p2, saveTotal = int1 - int2;
  // mode 3: refinance but keep paying the OLD payment -> early payoff
  let bal = B, m3 = 0, int3 = 0;
  if (p1 > B * r2) {
    while (bal > 0.005 && m3 < 600) { const i = bal*r2; int3 += i; bal = bal + i - p1; m3++; }
  } else { m3 = -1; }
  const fedWarn = fed ? `<p><strong>Before anything else:</strong> refinancing federal loans is irreversible — see the protections you'd surrender below. The savings math has to be large enough to buy out that insurance, not just positive.</p>` : '';
  show(`<div class="result-main">${saveTotal > 0 ? '$' + fmt(saveTotal,0) + ' less interest' : '$' + fmt(-saveTotal,0) + ' MORE interest'}<small>$${fmt(p2,0)}/month vs $${fmt(p1,0)} now ${saveMo > 0 ? '(&minus;$' + fmt(saveMo,0) + '/mo)' : '(+$' + fmt(-saveMo,0) + '/mo)'} &middot; ${fmt(val('oldrate'),2)}% &rarr; ${fmt(val('newrate'),2)}%</small></div>
  ${fedWarn}
  <table>
    <tr><th></th><th>Keep current loan</th><th>Refinance (${y2}-yr)</th><th>Refi + keep old payment</th></tr>
    <tr><td>Monthly payment</td><td>$${fmt(p1,0)}</td><td>$${fmt(p2,0)}</td><td>$${fmt(p1,0)}</td></tr>
    <tr><td>Payoff in</td><td>${y1} yrs</td><td>${y2} yrs</td><td>${m3 > 0 ? Math.floor(m3/12) + ' yr ' + (m3%12) + ' mo' : '—'}</td></tr>
    <tr><td>Total interest</td><td>$${fmt(int1,0)}</td><td>$${fmt(int2,0)}</td><td>${m3 > 0 ? '$' + fmt(int3,0) : '—'}</td></tr>
    <tr><td>Interest saved</td><td>—</td><td>${saveTotal > 0 ? '$' + fmt(saveTotal,0) : '&minus;$' + fmt(-saveTotal,0)}</td><td>${m3 > 0 ? '<strong>$' + fmt(int1-int3,0) + '</strong>' : '—'}</td></tr>
  </table>
  <p>${y2 > y1 && saveMo > 0 && saveTotal < 0
    ? `Classic stretch trap: the payment falls $${fmt(saveMo,0)}/month but the longer term costs $${fmt(-saveTotal,0)} more overall. If cash-flow relief is the goal, fine — but it's a term change wearing a rate change's clothes.`
    : (m3 > 0 && int1-int3 > saveTotal
      ? `The quiet winner is column three: refinance at ${fmt(val('newrate'),2)}% but keep paying your current $${fmt(p1,0)} — debt-free ${Math.floor((n2-m3)/12) > 0 ? Math.floor((n2-m3)/12) + '+ years early' : 'months early'} and $${fmt(int1-int3,0)} of interest saved, with no lifestyle change at all.`
      : `Rate down, same-or-shorter term: a clean win of $${fmt(saveTotal,0)}${fed ? ' — if it clears the federal-protection hurdle below' : '.'}`)}</p>`);
}
""",
        "body_html": """
<h2>The trade in one sentence</h2>
<p>A student loan refinance is a new private loan that pays off the old ones — you win if the new rate is meaningfully lower <em>and</em> you don't need what the old loans provided. For loans that are <strong>already private</strong>, that second clause is nearly empty: shop rate against rate, mind the term-stretch trap, done. For <strong>federal loans</strong>, the second clause is everything — a refinance is the permanent, irreversible sale of an insurance policy most borrowers don't notice they own until they need it.</p>
<h2>What refinancing federal loans burns, specifically</h2>
<ul>
<li><strong>Income-driven repayment.</strong> Federal plans cap payments at 10-20% of discretionary income and float with your life — job loss, pay cut, new baby, the payment adjusts. Private lenders expect the contractual amount regardless.</li>
<li><strong>Forgiveness tracks.</strong> PSLF wipes remaining balances after 10 years of public-service payments; IDR plans forgive after 20-25. A teacher, nurse, government lawyer or nonprofit worker refinancing out of PSLF can incinerate five or six figures of future forgiveness for a 1.5-point rate cut.</li>
<li><strong>Deferment, forbearance, and mass relief.</strong> Federal loans paused interest-free for three-plus years during COVID; private refis kept billing. Unemployment deferment, cancer deferment, death/disability discharge — the federal system absorbs catastrophe in ways private contracts mostly don't.</li>
</ul>
<p>The working rule: <strong>refinance federal loans only if</strong> your income is high and stable, your emergency fund is real (<a href="/calculators/emergency-fund-calculator/">size it first</a>), no forgiveness track applies to your career, and the savings are large enough to pay for surrendering all of the above — a 0.5-point cut isn't; two-plus points on a big balance might be.</p>
<h2>The three moves, priced</h2>
<p>The calculator's table shows the full menu. <strong>Rate-for-rate</strong> (same term, lower rate) is the clean win — every saved dollar is real. <strong>The stretch</strong> (lower payment via a longer term) is cash-flow relief, not savings — often the right call during tight years, but name it honestly: at a lower rate over more years, total interest can still rise. <strong>The quiet winner</strong> for most strong-credit borrowers is column three: refinance to the lower rate, keep paying the old amount. The payment you're already used to becomes an accelerator — typical result on a $40,000 balance: debt-free 1-2 years early and thousands saved, with zero lifestyle change. It's the same principle as the <a href="/calculators/extra-mortgage-payment-calculator/">mortgage extra-payment math</a>, applied automatically.</p>
<h2>Getting the best offer</h2>
<ul>
<li><strong>Rates are credit-priced:</strong> the advertised "from 4.5%" belongs to 780-score borrowers with high incomes; real offers spread 2-3 points by credit tier. A qualified <strong>cosigner</strong> typically cuts 0.5-1.5 points — with the caveat that they're fully liable (look for cosigner-release terms after 12-36 clean payments).</li>
<li><strong>Shop 3-5 lenders in a two-week window</strong> — prequalification soft-pulls don't touch your score, and the hard pulls that follow count as one inquiry within the window. Compare APR (student refis rarely have origination fees, but verify) using the <a href="/calculators/loan-comparison-calculator/">loan comparison calculator</a>.</li>
<li><strong>Variable-rate offers</strong> price ~0.5-1 point below fixed. On a 5-year aggressive payoff, the gamble can pay; on a 15-year term it's carrying rate risk you're not paid enough to hold. Most borrowers should take fixed and sleep.</li>
<li><strong>Re-refinancing is allowed.</strong> Private-to-private refis can repeat whenever rates drop or your credit improves — there's no loyalty prize. Rate-check annually; the second refinance takes an hour.</li>
</ul>
<h2>Who shouldn't refinance at all</h2>
<p>Anyone pursuing <strong>PSLF or IDR forgiveness</strong> — the forgiveness usually dwarfs any rate savings. Anyone whose <strong>income wobbles</strong> — the federal safety net is worth more than 2 points to a freelancer or seasonal worker (the <a href="/calculators/quarterly-estimated-tax-calculator/">variable-income crowd</a> knows who they are). Anyone with <strong>weak credit right now</strong> — offers won't beat current federal rates (recent federal loans at 4-5% often can't be beaten privately at all); build the score first with <a href="/articles/how-to-build-credit/">on-time history</a>, refi later. And anyone counting on <strong>employer repayment benefits or state programs</strong> tied to loan type. For everyone else, run this calculator's three columns against the <a href="/calculators/student-loan-calculator/">baseline payoff plan</a> — the difference between a marketing pitch and a decision is exactly that table.</p>
""",
        "faqs": [
            ("Can I refinance federal student loans back into the federal system later?", "No — this is the door that only swings one way. A private refinance pays off the federal loans, and the federal terms (IDR, PSLF, deferments, discharge rules) die with them; there's no mechanism to return. Federal consolidation (a Direct Consolidation Loan) is the federal-side alternative that preserves protections but doesn't lower the rate — it averages your existing rates."),
            ("Does refinancing student loans hurt my credit?", "Briefly and mildly: a hard inquiry or two (rate-shopping within ~14 days counts as one) and a new account lowering average age — a few points, recovering within months. On-time payments on the new loan then build history like any installment loan. The score impact is a rounding error next to the interest math; decide on the rates."),
            ("Should I refinance to a variable rate?", "Only if you'll pay the loan off fast (roughly 5 years or less) and could absorb the payment if rates rose 2-3 points. Variable offers start ~0.5-1 point below fixed and reprice with the market — a good bet on a short runway, an unpaid risk on a long one. If the variable-vs-fixed choice is what makes the refi attractive, the refi probably isn't attractive."),
            ("Is there any reason to refinance if the new rate is barely lower?", "On private loans, small cuts still add up on big balances — 0.5% on $80,000 is $400/year, and refinancing is usually free, so even modest wins are wins (and repeatable). On federal loans, no: a small cut can't buy out the protections you'd surrender. Save the federal refi decision for large, life-is-stable rate gaps."),
            ("Can I refinance just some of my loans?", "Yes, and it's often the smart structure: refinance the high-rate private loans (or, for the high-income-stable crowd, the high-rate federal ones) while leaving low-rate or forgiveness-track loans untouched. Lenders let you pick which loans the refi pays off. A split keeps the federal safety net on part of the balance while cutting the rate where it costs most."),
        ],
    },
]
