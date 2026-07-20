# -*- coding: utf-8 -*-
"""15-year vs 30-year mortgage — payment, total interest, and the invest-the-difference verdict."""

MORTGAGETERM = [
    {
        "slug": "15-vs-30-year-mortgage-calculator",
        "emoji": "\U0001F3E6",
        "category": "Mortgages & Home",
        "title": "15 vs 30 Year Mortgage Calculator — Which Should You Choose?",
        "h1": "15 vs 30 Year Mortgage Calculator",
        "blurb": "Compare payment, total interest, and investing the payment difference.",
        "meta_description": "Compare a 15-year vs 30-year mortgage: monthly payment, total interest saved, and whether investing the payment difference on a 30-year loan beats the guaranteed savings of a 15-year.",
        "intro": "A 15-year mortgage saves a fortune in interest but costs much more each month. A 30-year frees up cash you could invest. This calculator shows the payment and total interest for each — and settles the real debate by comparing net wealth after 30 years.",
        "fields": [
            {"id": "amount", "label": "Loan amount ($)", "value": 300000},
            {"id": "rate15", "label": "15-year interest rate (%)", "value": 5.75, "step": 0.05, "hint": "usually ~0.5-0.75% below the 30-yr"},
            {"id": "rate30", "label": "30-year interest rate (%)", "value": 6.5, "step": 0.05},
            {"id": "invreturn", "label": "Return if you invest the difference (%/yr)", "value": 7, "step": 0.1},
        ],
        "js": """
function amort(P, annual, years) {
  const i = annual/100/12, n = Math.round(years*12);
  return n > 0 ? (i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n) : 0;
}
function calculate() {
  const P = val('amount'), r15 = val('rate15'), r30 = val('rate30'), ir = val('invreturn')/100/12;
  if (P <= 0) { show('<div class="result-main">Enter a loan amount above zero.</div>'); return; }
  const pmt15 = amort(P, r15, 15), pmt30 = amort(P, r30, 30);
  const int15 = pmt15*180 - P, int30 = pmt30*360 - P;
  const diff = pmt15 - pmt30;   // extra the 15-yr costs each month
  // Fair 30-year comparison, both spending pmt15/month:
  //  A) 15-yr: house paid at yr15, then invest pmt15/mo for months 181-360
  let invA = 0;
  for (let m=1; m<=360; m++){ invA*=(1+ir); if (m>180) invA += pmt15; }
  //  B) 30-yr: invest (pmt15 - pmt30)/mo for all 360 months
  let invB = 0;
  for (let m=1; m<=360; m++){ invB = invB*(1+ir) + Math.max(0,diff); }
  const aWins = invA > invB;
  const gap = Math.abs(invA - invB);
  show(`<div class="result-main">$${fmt(int30-int15,0)} interest saved with 15-year<small>but it costs $${fmt(diff,0)} more per month</small></div>
  <table>
    <tr><td>15-year payment</td><td>$${fmt(pmt15)}/mo &middot; $${fmt(int15,0)} total interest</td></tr>
    <tr><td>30-year payment</td><td>$${fmt(pmt30)}/mo &middot; $${fmt(int30,0)} total interest</td></tr>
    <tr><td colspan="2"><strong>If you spend $${fmt(pmt15,0)}/mo either way, after 30 years:</strong></td></tr>
    <tr><td>15-yr then invest the freed payment</td><td>$${fmt(invA,0)} invested</td></tr>
    <tr><td>30-yr &amp; invest the difference now</td><td>$${fmt(invB,0)} invested</td></tr>
    <tr><td>Wealthier path (both own the home)</td><td>${aWins ? '15-year' : '30-year + invest'} by $${fmt(gap,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The trade-off in one sentence</h2>
<p>A 15-year mortgage charges a lower interest rate and slashes total interest, but the monthly payment is much higher. A 30-year mortgage has an affordable payment and frees up cash — but you pay far more interest over time and stay in debt twice as long. This calculator shows both numbers, then answers the question that actually matters: <strong>which leaves you wealthier after 30 years if you commit the same monthly cash either way?</strong></p>
<h2>The raw numbers</h2>
<p>On a $300,000 loan at 5.75% (15-year) vs 6.5% (30-year), the 15-year payment is roughly $2,490/month versus about $1,896 — nearly $600 more. But the 15-year borrower pays around $148,000 in total interest versus about $383,000 on the 30-year. That's roughly <strong>$235,000 of interest avoided</strong>, plus being mortgage-free 15 years sooner. Purely on interest, the 15-year is a landslide.</p>
<h2>The honest counterargument: invest the difference</h2>
<p>The 30-year's defenders make a fair point: its lower payment frees up ~$600/month that could be invested. If that money earns more than the mortgage rate, the 30-year borrower could come out ahead in total wealth despite paying more interest. This calculator tests that directly — it assumes you spend the <em>same</em> monthly amount either way (the higher 15-year payment), and compares two paths over 30 years:</p>
<ul>
<li><strong>15-year:</strong> pay it off in 15 years, then invest the (now freed-up) full payment for the remaining 15 years.</li>
<li><strong>30-year:</strong> invest the payment difference every month for the full 30 years.</li>
</ul>
<p>The winner depends heavily on your assumed investment return versus the rate gap. At high assumed returns (say 8–10%), investing the difference in the early years — when compounding has longest to work — often edges ahead. At modest returns (5–6%), the 15-year's guaranteed interest savings usually win. Because the 15-year's benefit is <em>certain</em> and the investment's is <em>expected</em>, many people rationally prefer the guaranteed path even when the projected numbers are close.</p>
<h2>Which should you choose?</h2>
<ul>
<li><strong>Choose the 15-year if:</strong> you can comfortably afford the higher payment, value guaranteed interest savings and being debt-free sooner, and worry you wouldn't actually invest the difference (most people don't).</li>
<li><strong>Choose the 30-year if:</strong> you want payment flexibility, will genuinely invest the difference (ideally automatically), or need the lower payment to keep housing costs within a safe share of income.</li>
<li><strong>A middle path:</strong> take the 30-year for flexibility but make extra principal payments toward a 15-year pace — see our <a href="/calculators/extra-mortgage-payment-calculator/">extra payment calculator</a>. You keep the option to fall back to the lower required payment in a tight month.</li>
</ul>
<p>Whatever the term, make sure the payment fits your budget first with the <a href="/calculators/home-affordability-calculator/">home affordability calculator</a>, and see the full monthly picture with the <a href="/calculators/mortgage-calculator/">mortgage calculator</a>.</p>
""",
        "faqs": [
            ("Is a 15-year mortgage worth the higher payment?", "If you can afford it comfortably, usually yes: you save a large amount of interest (often $200k+ on a typical loan), get a lower rate, and are debt-free in half the time. The catch is the higher payment, which must fit your budget without crowding out saving and emergencies."),
            ("Is it better to get a 30-year and invest the difference?", "It can be, if you actually invest the difference and earn more than the mortgage rate after tax. The 30-year's benefit is an expected (uncertain) investment return; the 15-year's is a guaranteed interest saving. Many people prefer the certainty — and most don't reliably invest the difference."),
            ("Can I pay off a 30-year mortgage in 15 years?", "Yes. Take the 30-year for its lower required payment, then make extra principal payments to match a 15-year schedule. You get most of the interest savings while keeping the flexibility to drop back to the lower payment if money gets tight."),
        ],
    },
]
