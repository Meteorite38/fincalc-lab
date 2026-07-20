# -*- coding: utf-8 -*-
"""HELOC calculator — borrowing power from CLTV, interest-only vs repayment phase payments, payment-shock warning."""

HELOC = [
    {
        "slug": "heloc-calculator",
        "emoji": "\U0001F3E6",
        "category": "Loans & Debt",
        "title": "HELOC Calculator — Credit Line, Payments, and the Payment Shock",
        "h1": "HELOC Calculator",
        "blurb": "How big a credit line your equity supports, and payments in both phases — including the jump.",
        "meta_description": "Free HELOC calculator: see the credit line your home equity supports at 80-90% CLTV, the interest-only payment during the draw period, the amortizing payment after — and the payment shock between them.",
        "intro": "A HELOC looks cheap for exactly as long as the draw period lasts: interest-only payments on a variable rate. Then the repayment phase starts, principal comes due, and the monthly bill can jump 50% or more. This calculator sizes your line from your equity and shows both phases honestly.",
        "fields": [
            {"id": "value", "label": "Home value ($)", "value": 450000},
            {"id": "mortgage", "label": "Mortgage balance ($)", "value": 280000},
            {"id": "cltv", "label": "Lender's max combined LTV (%)", "value": 85, "step": 1, "hint": "most lenders allow 80-90%"},
            {"id": "draw", "label": "Amount you plan to borrow ($)", "value": 50000},
            {"id": "rate", "label": "HELOC interest rate (%)", "value": 8.5, "step": 0.05, "hint": "variable: prime + margin"},
            {"id": "ioyears", "label": "Draw period (years, interest-only)", "value": 10, "step": 1},
            {"id": "repayyears", "label": "Repayment period (years)", "value": 20, "step": 1},
        ],
        "js": """
function calculate() {
  const V = val('value'), M = val('mortgage'), cltv = val('cltv')/100, D = val('draw');
  const r = val('rate')/100/12, io = Math.max(0, Math.round(val('ioyears'))), rp = Math.max(1, Math.round(val('repayyears')));
  if (V <= 0) { show('<div class="result-main">Enter a home value.</div>'); return; }
  const maxLine = Math.max(0, V * cltv - M);
  if (maxLine <= 0) {
    show(`<div class="result-main">No HELOC room at ${fmt(cltv*100,0)}% CLTV<small>your mortgage ($${fmt(M,0)}) already exceeds ${fmt(cltv*100,0)}% of the home's value ($${fmt(V*cltv,0)})</small></div>
    <p>Lenders cap the mortgage <em>plus</em> the credit line at ${fmt(cltv*100,0)}% of value. You'd need the home to appraise above $${fmt(M/cltv,0)}, or the mortgage paid below $${fmt(V*cltv,0)}, before a line opens up.</p>`);
    return;
  }
  const borrow = Math.min(D, maxLine);
  const capped = D > maxLine;
  const ioPay = borrow * r;
  const n = rp * 12;
  const repPay = r > 0 ? borrow * r / (1 - Math.pow(1 + r, -n)) : borrow / n;
  const shock = ioPay > 0 ? (repPay / ioPay - 1) * 100 : 0;
  const ioInterest = ioPay * io * 12;
  const repInterest = repPay * n - borrow;
  const totalInterest = ioInterest + repInterest;
  const rateUp = r + 0.02/12;
  const ioPayUp = borrow * rateUp;
  show(`<div class="result-main">$${fmt(maxLine,0)} credit line available<small>at ${fmt(cltv*100,0)}% combined LTV on a $${fmt(V,0)} home with $${fmt(M,0)} owed</small></div>
  ${capped ? `<p><strong>Note:</strong> you wanted $${fmt(D,0)} but the line caps at $${fmt(maxLine,0)} — numbers below use the capped amount.</p>` : ''}
  <table>
    <tr><td>Draw period payment (interest-only, ${io} yrs)</td><td>$${fmt(ioPay,0)}/month on a $${fmt(borrow,0)} balance</td></tr>
    <tr><td><strong>Repayment period payment (${rp} yrs)</strong></td><td><strong>$${fmt(repPay,0)}/month</strong>${shock > 1 ? ` — a <strong>${fmt(shock,0)}% jump</strong>` : ''}</td></tr>
    <tr><td>Interest paid during draw period</td><td>$${fmt(ioInterest,0)} (buys down zero principal)</td></tr>
    <tr><td>Interest during repayment period</td><td>$${fmt(repInterest,0)}</td></tr>
    <tr><td><strong>Total interest, minimum payments only</strong></td><td><strong>$${fmt(totalInterest,0)}</strong> on $${fmt(borrow,0)} borrowed</td></tr>
    <tr><td>If the variable rate rises 2 points</td><td>draw-period payment becomes $${fmt(ioPayUp,0)}/month</td></tr>
  </table>
  <p>Paying only the interest-only minimum for all ${io} years means owing the full $${fmt(borrow,0)} when repayment starts. Adding principal early — even $${fmt(Math.ceil(borrow/(io*12)/50)*50,0)}/month — flattens the shock entirely.</p>`);
}
""",
        "body_html": """
<h2>How a HELOC actually works</h2>
<p>A home equity line of credit is a <strong>credit card secured by your house</strong>: a revolving line you can draw, repay and redraw. It runs in two phases. During the <strong>draw period</strong> (typically 10 years) you borrow as needed and the required payment is usually interest-only. Then the <strong>repayment period</strong> (10-20 years) begins: no new draws, and the balance amortizes into principal-plus-interest payments. The rate is almost always <strong>variable</strong> — prime plus a margin — so it moves with the Fed, in both directions, for the life of the line.</p>
<h2>How big a line you can get</h2>
<p>Lenders cap your mortgage plus the line at a <strong>combined loan-to-value (CLTV)</strong> — commonly 80-90% of appraised value. The formula is one line: home value &times; CLTV &minus; mortgage balance. A $450,000 home at 85% CLTV with $280,000 owed supports up to $102,500. What the lender approves also depends on credit score (mid-600s minimum at most banks, best pricing above 740) and a debt-to-income ratio that survives the new payment — check yours with the <a href="/calculators/debt-to-income-ratio-calculator/">DTI calculator</a>, and see your raw equity position in the <a href="/calculators/home-equity-calculator/">home equity calculator</a>.</p>
<h2>The payment shock, quantified</h2>
<p>The draw-period math lulls people. Interest-only on $50,000 at 8.5% is about $354 a month. When the repayment period starts, that same balance amortizing over 20 years costs about $434 — a 23% jump. Shorter repayment periods bite harder: over 15 years it's $492 (+39%), over 10 years $620 (+75%). And that assumes rates sat still for a decade, which variable rates don't. The classic HELOC casualty borrowed to the limit, paid the minimum for ten years, built zero principal, and met a 50%+ payment jump — this calculator's whole job is making that visible up front.</p>
<h2>HELOC vs the alternatives</h2>
<ul>
<li><strong>Home equity loan:</strong> same collateral, but a fixed lump sum at a fixed rate with level payments from day one. Better when the cost is known and one-time (a roof, a settled renovation bid). The HELOC wins for staged or uncertain costs — you pay interest only on what's drawn.</li>
<li><strong>Cash-out refinance:</strong> replaces the whole first mortgage. Made sense when rates were falling; with a 3% mortgage in hand and 6-7% refi rates, surrendering the old rate to touch equity is usually a bad trade — the HELOC leaves the first mortgage untouched.</li>
<li><strong>Personal loan:</strong> unsecured, so pricier (10-15%+) — but your house isn't collateral. For smaller amounts on shorter timelines, compare with the <a href="/calculators/loan-comparison-calculator/">loan comparison calculator</a>; the rate gap shrinks fast after fees.</li>
</ul>
<h2>What a HELOC is good for — and not</h2>
<p>The strong use cases share a trait: <strong>the money buys something durable or bridges a gap you can see across.</strong> Staged renovations that add value, a bridge between buying one house and selling another, an emergency backstop opened <em>before</em> it's needed (a $0-balance line costs little or nothing to keep open). The weak cases: consolidating card debt without fixing the spending that built it — the <a href="/calculators/debt-consolidation-calculator/">consolidation math</a> can look great right up until the cards refill and the debt is now attached to your house — and funding lifestyle spending on vacations or cars, which converts depreciating consumption into a lien on your home. The deduction rules follow the same logic: HELOC interest is only tax-deductible when the money <strong>buys, builds or substantially improves</strong> the home securing it.</p>
<h2>Costs and fine print worth reading</h2>
<ul>
<li><strong>Rate structure:</strong> your rate is prime + margin. The margin is negotiable and score-dependent; intro teaser rates often expire after 6-12 months.</li>
<li><strong>Floors and caps:</strong> most HELOCs have a lifetime cap (often 18%) and a floor below which the rate won't drop, whatever prime does.</li>
<li><strong>Fees:</strong> annual fees ($50-100), early-closure fees if you close within 2-3 years, and sometimes appraisal/origination costs — many lenders waive them; ask.</li>
<li><strong>Freeze risk:</strong> the lender can freeze or reduce the line if home values fall or your credit deteriorates — 2008's unpleasant surprise. An unused HELOC is a good backstop but shouldn't be your <em>only</em> emergency plan; size a cash cushion with the <a href="/calculators/emergency-fund-calculator/">emergency fund calculator</a>.</li>
<li><strong>Fixed-rate locks:</strong> many lenders let you convert chunks of the drawn balance to a fixed rate — useful hedge once a big draw is done.</li>
</ul>
""",
        "faqs": [
            ("Is HELOC interest tax-deductible?", "Only if the borrowed money buys, builds, or substantially improves the home that secures the line (and only within the overall $750,000 home-acquisition-debt cap, itemizing required). Renovation draws qualify; debt consolidation, tuition and car purchases don't. Keep records of what each draw funded."),
            ("What happens to my HELOC if home prices drop?", "The lender can freeze or reduce the unused portion of the line if the home's value falls significantly — they periodically re-check values by automated appraisal. Money already drawn stays borrowed on the original terms; it's the undrawn availability that can vanish exactly when you might want it."),
            ("Can I pay off a HELOC early?", "Yes — you can pay the balance down (or to zero) at any time without prepayment penalty on the balance itself. The only common gotcha is an early-closure fee ($200-500) if you fully close the line within the first 2-3 years; leaving it open at a zero balance usually avoids that."),
            ("HELOC or home equity loan for a renovation?", "Staged or uncertain costs favor the HELOC (draw as invoices arrive, pay interest only on what's out); a fixed bid favors the home equity loan (fixed rate, level payment, no rate risk). Many people use a HELOC during construction, then convert or refinance the final balance to a fixed rate."),
            ("Does opening a HELOC hurt my credit score?", "Modestly and briefly: a hard inquiry plus a new account. Ongoing, a HELOC is usually reported as an installment-style or home-equity line and most scoring models exclude it from the credit-card utilization ratio, so even a large draw doesn't crater the score the way a maxed card does. Payment history on it counts like any other loan."),
        ],
    },
]
