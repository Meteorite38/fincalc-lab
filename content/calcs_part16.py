# -*- coding: utf-8 -*-
"""Batch 14 calculators: credit utilization, required return to hit a goal."""

PART16 = [
    {
        "slug": "credit-utilization-calculator",
        "emoji": "\U0001F4B3",
        "category": "Loans & Debt",
        "title": "Credit Utilization Calculator — The Ratio That Moves Your Score",
        "h1": "Credit Utilization Calculator",
        "blurb": "Your credit utilization ratio and its score impact.",
        "meta_description": "Calculate your credit utilization ratio — balances divided by limits — and see how it affects your credit score, plus the target to aim for.",
        "intro": "Credit utilization is one of the biggest factors in your credit score. Enter your total balances and limits to see your ratio and how it's likely helping or hurting your score.",
        "fields": [
            {"id": "balance", "label": "Total credit card balances ($)", "value": 2400},
            {"id": "limit", "label": "Total credit limits ($)", "value": 10000},
        ],
        "js": """
function calculate() {
  const bal = val('balance'), lim = val('limit');
  if (lim <= 0) { show('<div class="result-main">Enter your total credit limit above zero.</div>'); return; }
  const util = bal / lim * 100;
  let band, advice;
  if (util <= 10) { band = 'Excellent'; advice = 'Ideal range \\u2014 this helps your score the most.'; }
  else if (util <= 30) { band = 'Good'; advice = 'Within the recommended limit; aim under 10% for the best effect.'; }
  else if (util <= 50) { band = 'Fair'; advice = 'Above the 30% guideline \\u2014 paying this down should lift your score.'; }
  else { band = 'High'; advice = 'Well above 30% \\u2014 this is likely dragging your score down noticeably.'; }
  const to30 = Math.max(0, bal - lim*0.30);
  const to10 = Math.max(0, bal - lim*0.10);
  show(`<div class="result-main">${fmt(util,1)}%<small>Credit utilization \\u2014 ${band}</small></div>
  <table>
    <tr><td>Total balances</td><td>$${fmt(bal,0)}</td></tr>
    <tr><td>Total limits</td><td>$${fmt(lim,0)}</td></tr>
    <tr><td>Utilization</td><td>${fmt(util,1)}%</td></tr>
    <tr><td>Pay down to reach 30%</td><td>${to30>0 ? '$'+fmt(to30,0) : 'already under 30% \\u2705'}</td></tr>
    <tr><td>Pay down to reach 10%</td><td>${to10>0 ? '$'+fmt(to10,0) : 'already under 10% \\u2705'}</td></tr>
    <tr><td>Assessment</td><td>${advice}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What credit utilization is</h2>
<p>Credit utilization is the percentage of your available credit you're currently using: <code>utilization = balances ÷ credit limits × 100</code>. If you owe $2,400 across cards with $10,000 of total limits, your utilization is 24%. It's calculated both per-card and overall, and it's one of the most powerful factors in your credit score — typically around <strong>30% of the score</strong>, second only to payment history (see [what affects your credit score](/articles/what-affects-your-credit-score/)).</p>
<h2>Why lenders care</h2>
<p>High utilization signals risk: someone using most of their available credit looks financially stretched and more likely to miss payments. Low utilization signals control. Because it's such a strong signal, utilization can swing your score significantly — and unlike most factors, it can change fast, since it updates whenever balances are reported.</p>
<h2>The targets to aim for</h2>
<ul>
<li><strong>Under 30%</strong> — the widely-cited maximum. Above this, your score usually takes a hit.</li>
<li><strong>Under 10%</strong> — the sweet spot. The lowest utilization (while still using cards) tends to maximize this part of your score.</li>
<li><strong>Not 0%</strong> — showing a small balance that you pay off is generally slightly better than showing zero everywhere, which can look like inactivity.</li>
</ul>
<h2>How to lower it fast</h2>
<p>Utilization is one of the quickest score levers because it responds immediately to balance changes:</p>
<ul>
<li><strong>Pay down balances</strong> — the direct route. The calculator shows exactly how much to pay to reach 30% and 10%.</li>
<li><strong>Pay before the statement closes.</strong> Card issuers report the statement balance, so paying down *before* the statement date lowers the utilization that gets reported — even if you'd pay it off anyway.</li>
<li><strong>Request a credit-limit increase.</strong> A higher limit lowers utilization instantly without changing your spending (just don't spend more to match).</li>
<li><strong>Keep old cards open.</strong> Closing a card removes its limit, which *raises* your utilization — usually keep them open, per [how to build credit](/articles/how-to-build-credit/).</li>
</ul>
<h2>The bottom line</h2>
<p>Credit utilization is the rare credit factor you can improve in a single billing cycle. Keep it under 30% always, aim for under 10% before applying for anything important (a mortgage, car loan, or new card), and use the "pay before the statement date" trick to control what's reported. It's one of the easiest, fastest ways to protect and boost your score.</p>
""",
        "faqs": [
            ("What is a good credit utilization ratio?", "Keep it under 30% of your total limits, and ideally under 10% for the best score impact. Very low utilization (but not zero across all cards) tends to maximize this part of your score."),
            ("How do I lower my credit utilization?", "Pay down balances, pay before the statement closes (since the statement balance is what's reported), request higher credit limits, and keep old cards open to preserve your total available credit."),
            ("Does credit utilization affect my score quickly?", "Yes — it's one of the fastest-moving factors, updating whenever your balances are reported. Paying down a balance can improve your score within one or two billing cycles."),
        ],
    },
    {
        "slug": "required-return-calculator",
        "emoji": "\U0001F3AF",
        "category": "Savings & Investing",
        "title": "Required Return Calculator — What Rate You Need to Hit Your Goal",
        "h1": "Required Return Calculator",
        "blurb": "The annual return needed to reach a target on time.",
        "meta_description": "Find the annual investment return you'd need to reach a financial goal, given your starting amount, monthly contributions and timeline — and whether it's realistic.",
        "intro": "Know your goal, your timeline, and how much you can invest? This calculator finds the annual return you'd need to get there — and tells you whether that's realistic or wishful.",
        "fields": [
            {"id": "target", "label": "Goal amount ($)", "value": 500000},
            {"id": "current", "label": "Current savings ($)", "value": 50000},
            {"id": "monthly", "label": "Monthly contribution ($)", "value": 600},
            {"id": "years", "label": "Years to reach it", "value": 20, "step": 1},
        ],
        "js": """
function fv(P, pmt, annualPct, years) {
  const i = annualPct/100/12, n = Math.round(years*12);
  const g = Math.pow(1+i, n);
  return i === 0 ? P + pmt*n : P*g + pmt*(g-1)/i;
}
function calculate() {
  const target = val('target'), P = val('current'), pmt = val('monthly'), y = val('years');
  if (y <= 0) { show('<div class="result-main">Enter a time horizon above zero.</div>'); return; }
  const contribTotal = P + pmt*y*12;
  // bisection on annual rate 0%..60%
  let lo = -50, hi = 60;
  if (fv(P, pmt, hi, y) < target) { show(`<div class="result-main">Out of realistic range<small>Even a 60% annual return wouldn't reach $${fmt(target,0)} \\u2014 increase contributions or time</small></div>`); return; }
  if (fv(P, pmt, 0, y) >= target) {
    show(`<div class="result-main">0% needed \\u2705<small>Your contributions alone reach $${fmt(target,0)} \\u2014 no growth required</small></div>
    <table><tr><td>Total you'll contribute</td><td>$${fmt(contribTotal,0)}</td></tr></table>`);
    return;
  }
  for (let k = 0; k < 100; k++) { const mid = (lo+hi)/2; if (fv(P, pmt, mid, y) < target) lo = mid; else hi = mid; }
  const rate = (lo+hi)/2;
  let verdict;
  if (rate <= 5) verdict = 'Very achievable \\u2014 within reach of conservative investing';
  else if (rate <= 8) verdict = 'Realistic \\u2014 in line with long-run stock market averages';
  else if (rate <= 12) verdict = 'Ambitious \\u2014 above typical averages; possible but not guaranteed';
  else verdict = 'Unrealistic \\u2014 higher than markets reliably deliver; adjust the plan';
  show(`<div class="result-main">${fmt(rate,1)}% / year<small>Annual return needed to reach $${fmt(target,0)} in ${y} years</small></div>
  <table>
    <tr><td>Total you'll contribute</td><td>$${fmt(contribTotal,0)}</td></tr>
    <tr><td>Growth required on top</td><td>$${fmt(target-contribTotal,0)}</td></tr>
    <tr><td>Required annual return</td><td>${fmt(rate,1)}%</td></tr>
    <tr><td>Reality check</td><td>${verdict}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Working backwards from your goal</h2>
<p>Most calculators start with a return and project a result. This one flips it: you set the goal, the timeline, and what you can invest, and it solves for the <strong>annual return you'd need</strong> to get there. That's powerful, because it turns a wish into a testable question — <em>is the return I need actually realistic?</em></p>
<h2>Why the reality check matters</h2>
<p>The value here isn't just the number — it's the honesty. If the calculator says you need 4% a year, that's very achievable and your plan is sound. If it says you need 15%, that's a warning: no investment reliably delivers that, so betting on it means gambling. A required return above roughly 10% is a signal to change the plan, not to chase riskier assets hoping they deliver.</p>
<h2>What counts as realistic</h2>
<ul>
<li><strong>Under ~5%</strong> — achievable even with conservative, lower-risk investing.</li>
<li><strong>5–8%</strong> — in line with long-run diversified [stock market](/articles/index-funds-explained/) averages (about 7% real historically). A reasonable plan.</li>
<li><strong>8–12%</strong> — ambitious; above typical averages. Possible in good decades but not something to count on.</li>
<li><strong>Over 12%</strong> — unrealistic as a plan. Markets don't reliably deliver this, and needing it means the goal, timeline, or contributions must change.</li>
</ul>
<h2>If the required return is too high</h2>
<p>You have three honest levers, none of which involve gambling on a miracle return:</p>
<ol>
<li><strong>Contribute more</strong> each month — the most reliable fix, and it lowers the return you need.</li>
<li><strong>Extend the timeline</strong> — more years means [compounding](/articles/how-compound-interest-builds-wealth/) does more of the work, dropping the required return.</li>
<li><strong>Lower the goal</strong> to something the math supports.</li>
</ol>
<p>Chasing a high required return by piling into risky assets is how people lose money. Adjust the inputs you control instead, and build a plan around a return the market can actually provide.</p>
""",
        "faqs": [
            ("What return do I need to reach my goal?", "It depends on your starting amount, monthly contributions, timeline and target. This calculator solves for the exact annual return required — and tells you whether that rate is realistic given historical market averages."),
            ("What's a realistic investment return to plan around?", "A diversified stock portfolio has historically averaged about 7% a year after inflation over long periods. Planning around 5–8% is reasonable; needing more than ~10% is a sign to adjust your contributions, timeline, or goal rather than chase risk."),
            ("What if the required return is unrealistically high?", "Change the inputs you control: contribute more, extend your timeline, or lower the goal. Relying on an unrealistically high return means gambling — adjust the plan so a normal market return gets you there."),
        ],
    },
]
