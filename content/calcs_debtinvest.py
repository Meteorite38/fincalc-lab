# -*- coding: utf-8 -*-
"""Pay Off Debt vs Invest — net-worth comparison of two uses for spare monthly cash."""

DEBTINVEST = [
    {
        "slug": "pay-off-debt-vs-invest-calculator",
        "emoji": "\u2696\uFE0F",
        "category": "Debt & Credit",
        "title": "Pay Off Debt vs Invest Calculator — Which Builds More Wealth?",
        "h1": "Pay Off Debt vs Invest Calculator",
        "blurb": "Should spare cash attack debt or go into investments? Compare net worth.",
        "meta_description": "Should you pay off debt or invest? This calculator compares your net worth after paying extra toward debt vs investing that money, so you can see which builds more wealth.",
        "intro": "You have some spare cash each month. Attack the debt, or invest it? This calculator runs both strategies month by month and compares the net worth (investments minus remaining debt) each leaves you with — the honest way to settle the debate.",
        "fields": [
            {"id": "balance", "label": "Debt balance ($)", "value": 20000},
            {"id": "rate", "label": "Debt interest rate (%)", "value": 7, "step": 0.1},
            {"id": "minpay", "label": "Minimum / current monthly payment ($)", "value": 400},
            {"id": "extra", "label": "Extra cash available per month ($)", "value": 300},
            {"id": "invreturn", "label": "Expected investment return (%/yr)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Comparison horizon (years)", "value": 10, "step": 1},
        ],
        "js": """
function calculate() {
  const B0 = val('balance'), dr = val('rate')/100/12, MP = val('minpay'), E = val('extra');
  const ir = val('invreturn')/100/12, H = Math.round(Math.min(Math.max(val('years'),0),50)*12);
  if (B0 <= 0 || H <= 0) { show('<div class="result-main">Enter a debt balance and a horizon above zero.</div>'); return; }
  if (MP <= B0*dr) { show('<div class="result-main">Your minimum payment barely covers interest — increase it so the debt can actually shrink.</div>'); return; }

  // Strategy A: throw MP+E at the debt; once cleared, invest the whole freed-up amount
  let bal = B0, inv = 0;
  for (let m=1; m<=H; m++) {
    inv *= (1+ir);
    let cash = MP + E;
    if (bal > 0) { const int = bal*dr; bal += int; const pay = Math.min(cash, bal); bal -= pay; cash -= pay; }
    if (cash > 0) inv += cash;   // leftover (after debt gone) is invested
  }
  const netA = inv - Math.max(0, bal);

  // Strategy B: pay only the minimum, invest the extra; once debt is gone the freed
  // minimum payment is invested too (same total monthly cash flow as strategy A).
  let balB = B0, invB = 0;
  for (let m=1; m<=H; m++) {
    invB *= (1+ir);
    let cash = E;
    if (balB > 0) { const int = balB*dr; balB += int; const pay = Math.min(MP, balB); balB -= pay; }
    else { cash += MP; }
    invB += cash;
  }
  const netB = invB - Math.max(0, balB);

  const aWins = netA > netB;
  const diff = Math.abs(netA - netB);
  show(`<div class="result-main">${aWins ? 'Paying off debt first' : 'Investing the extra'} wins by $${fmt(diff,0)}<small>higher net worth after ${val('years')} years</small></div>
  <table>
    <tr><td><strong>Debt first</strong> (extra \\u2192 debt, then invest)</td><td>net worth $${fmt(netA,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Investments built</td><td>$${fmt(inv,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Debt remaining</td><td>$${fmt(Math.max(0,bal),0)}</td></tr>
    <tr><td><strong>Invest first</strong> (min on debt, invest extra)</td><td>net worth $${fmt(netB,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Investments built</td><td>$${fmt(invB,0)}</td></tr>
    <tr><td>&nbsp;&nbsp;Debt remaining</td><td>$${fmt(Math.max(0,balB),0)}</td></tr>
    <tr><td>Rule of thumb</td><td>debt rate ${fmt(val('rate'),1)}% vs return ${fmt(val('invreturn'),1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The core trade-off</h2>
<p>Every extra dollar has two competing homes. Put it toward debt and you earn a <strong>guaranteed, risk-free return equal to the debt's interest rate</strong> — paying off an 8% loan is exactly as good as a guaranteed 8% investment. Put it into the market instead and you earn an <em>expected</em> return that's usually higher over the long run, but uncertain and taxable. This calculator settles the argument by simulating both strategies month by month and comparing the net worth — investments minus any remaining debt — each leaves you with.</p>
<h2>How to read the result</h2>
<p>The math almost always follows one simple rule: <strong>compare the debt's interest rate to your expected after-tax investment return.</strong></p>
<ul>
<li><strong>High-rate debt (credit cards, ~15–25%):</strong> paying it off wins decisively. Almost nothing reliably beats a guaranteed 20% return, which is why clearing expensive debt is treated as an emergency.</li>
<li><strong>Low-rate debt (a ~3–4% mortgage or subsidised student loan):</strong> investing usually builds more wealth over long horizons, because expected market returns comfortably exceed the interest you'd save.</li>
<li><strong>The middle (~5–8%):</strong> it's close, and the "right" answer depends on your assumed return, taxes and time horizon — exactly what you can test above.</li>
</ul>
<h2>Why the guaranteed vs expected distinction matters</h2>
<p>Paying down debt delivers a <em>certain</em> outcome; investing delivers a <em>probable</em> one. Two people with identical numbers can rightly choose differently based on risk tolerance. The debt payoff is the lower-stress, lower-variance option; investing has higher expected wealth but real downside risk and requires you to actually stay invested through crashes. The calculator shows the expected-value winner — you weigh the certainty premium yourself.</p>
<h2>What the simple comparison leaves out</h2>
<ul>
<li><strong>Employer retirement match comes first.</strong> A 50–100% match beats paying off any debt — always capture it before either strategy. See the <a href="/articles/financial-order-of-operations/">financial order of operations</a>.</li>
<li><strong>Emergency fund first.</strong> Without cash reserves, a surprise expense lands on high-rate debt and undoes your progress.</li>
<li><strong>Taxes and behaviour.</strong> Investment returns may be taxed; debt payoff is tax-free. And guaranteed progress keeps some people motivated in a way volatile markets don't.</li>
</ul>
<p>Pair this with our <a href="/calculators/loan-payoff-calculator/">debt payoff</a> and <a href="/calculators/investment-return-calculator/">investment return</a> calculators, and the <a href="/articles/good-debt-vs-bad-debt/">good debt vs bad debt</a> guide, to decide with the full picture.</p>
""",
        "faqs": [
            ("Should I pay off debt or invest?", "Compare the debt's interest rate to your expected after-tax investment return. High-rate debt (like credit cards) should be paid off first — it's a guaranteed high return. Low-rate debt (like a cheap mortgage) can often be paid on schedule while you invest, since expected returns exceed the interest saved."),
            ("Is paying off debt a 'guaranteed return'?", "Yes. Eliminating a loan at 8% interest saves you 8% a year with certainty and no tax — equivalent to a guaranteed, risk-free 8% investment. Very few investments can promise that, which is why high-rate debt payoff is so attractive."),
            ("What should I do before either?", "Capture any employer retirement match (an instant 50–100% return) and build a small emergency fund first. Both come ahead of the debt-vs-invest decision, because they protect you from taking on new high-rate debt."),
        ],
    },
]
