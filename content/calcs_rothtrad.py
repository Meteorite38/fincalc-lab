# -*- coding: utf-8 -*-
"""Traditional vs Roth 401(k)/IRA — fair same-budget math plus the max-out reality."""

ROTHTRAD = [
    {
        "slug": "roth-vs-traditional-401k-calculator",
        "emoji": "\u2696\ufe0f",
        "category": "Retirement",
        "title": "Roth vs Traditional 401(k) Calculator — Which Leaves You More?",
        "h1": "Roth vs Traditional 401(k) Calculator",
        "blurb": "Compare after-tax retirement income from pre-tax vs Roth contributions.",
        "meta_description": "Roth or traditional 401(k)? Compare what each leaves you after tax in retirement — using a fair same-budget comparison or the max-out scenario where the traditional tax savings are invested on the side.",
        "intro": "Traditional contributions skip tax now and pay it in retirement; Roth pays tax now and never again. Which wins depends almost entirely on your tax rate today versus in retirement — plus one subtlety when you're maxing out the account. This calculator shows both, honestly.",
        "fields": [
            {"id": "contrib", "label": "Annual contribution budget ($)", "value": 10000, "hint": "pre-tax dollars you can commit each year"},
            {"id": "nowtax", "label": "Marginal tax rate now (%)", "value": 24, "step": 0.5},
            {"id": "rettax", "label": "Expected marginal tax rate in retirement (%)", "value": 18, "step": 0.5},
            {"id": "ret", "label": "Annual return (%)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Years until retirement", "value": 30, "step": 1},
            {"id": "mode", "label": "Comparison type", "type": "select", "value": "fair",
             "options": [("fair", "Same pre-tax budget (the fair math)"),
                         ("maxout", "Same dollar amount into the account (maxing out)")]},
        ],
        "js": """
function calculate() {
  const C = val('contrib'), tNow = val('nowtax')/100, tRet = val('rettax')/100;
  const r = val('ret')/100, yrs = Math.round(val('years'));
  if (C <= 0 || yrs <= 0) { show('<div class="result-main">Enter a contribution and years above zero.</div>'); return; }
  const F = r > 0 ? (Math.pow(1+r, yrs) - 1)/r : yrs;          // FV factor, end-of-year deposits
  const rSide = r * 0.85;                                       // taxable side account: ~15% drag on returns
  const Fside = rSide > 0 ? (Math.pow(1+rSide, yrs) - 1)/rSide : yrs;
  const mode = document.getElementById('mode').value;
  let trad, roth, note;
  if (mode === 'fair') {
    trad = C * F * (1 - tRet);
    roth = C * (1 - tNow) * F;
    note = 'Both paths give up the same take-home pay today.';
  } else {
    trad = C * F * (1 - tRet) + C * tNow * Fside;
    roth = C * F;
    note = 'Both put $' + fmt(C,0) + '/yr into the account; the traditional path also invests its tax savings in a taxable account (' + fmt(rSide*100,1) + '% after-drag return).';
  }
  const rothWins = roth > trad;
  const gap = Math.abs(roth - trad);
  const pct = trad > 0 ? gap/Math.min(roth,trad)*100 : 0;
  show(`<div class="result-main">${rothWins ? 'Roth' : 'Traditional'} leaves you $${fmt(gap,0)} more<small>spendable in retirement after ${yrs} years &mdash; ${note}</small></div>
  <table>
    <tr><td>Traditional &mdash; after-tax value</td><td>$${fmt(trad,0)}</td></tr>
    <tr><td>Roth &mdash; after-tax value</td><td>$${fmt(roth,0)}</td></tr>
    <tr><td>Advantage</td><td>${rothWins ? 'Roth' : 'Traditional'} by ${fmt(pct,1)}%</td></tr>
    <tr><td>Rate today vs in retirement</td><td>${fmt(tNow*100,1)}% now vs ${fmt(tRet*100,1)}% later ${tNow > tRet ? '&mdash; favors traditional' : (tNow < tRet ? '&mdash; favors Roth' : '&mdash; a wash on the fair math')}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The one-sentence rule</h2>
<p>With the same pre-tax budget, <strong>traditional wins if your tax rate in retirement is lower than today's; Roth wins if it's higher; they tie exactly if it's the same.</strong> That's not an opinion — it's algebra. A dollar taxed at rate <em>t</em> grows to the same amount whether the tax comes out before or after compounding: <em>C·(1&minus;t)·growth = C·growth·(1&minus;t)</em>. Everything else about the decision is a forecast of those two tax rates.</p>
<h2>So why does Roth so often win in practice?</h2>
<ul>
<li><strong>The contribution cap doesn't care about tax.</strong> The 401(k) limit ($23,500 in 2025) is the same for both types. Maxing out a Roth stuffs more <em>after-tax</em> value inside the tax shelter than maxing out a traditional — switch this calculator to the max-out mode to see it. The traditional path only keeps pace if you faithfully invest the tax savings on the side, and the side account suffers tax drag every year.</li>
<li><strong>Marginal in, (mostly) average out.</strong> Contributions save tax at your top marginal rate, but withdrawals fill the empty lower brackets first — the standard deduction and 10-12% brackets. Many retirees' <em>effective</em> rate on traditional withdrawals lands well below their working marginal rate, which pushes the other way, toward traditional. The honest answer uses both effects.</li>
<li><strong>RMDs and flexibility.</strong> Traditional accounts force required minimum distributions from your mid-70s, taxed whether you need the money or not. Roth 401(k)s can be rolled to a Roth IRA with no RMDs, no tax on withdrawal, and tax-free inheritance for heirs.</li>
<li><strong>Rate risk runs asymmetric.</strong> If tax law shifts, current statutory rates are historically low; locking today's known rate (Roth) hedges against future increases better than betting on future cuts.</li>
</ul>
<h2>Practical guidance by situation</h2>
<ul>
<li><strong>Early career / low bracket (10-12%):</strong> Roth, almost always. You're prepaying tax at a rate you may never see again.</li>
<li><strong>Peak earning years (32%+):</strong> traditional usually wins — you're very likely to withdraw at a lower rate than you're deferring at.</li>
<li><strong>The murky middle (22-24%):</strong> genuinely close. Splitting contributions — or defaulting to traditional while doing Roth conversions in low-income years — hedges the forecast.</li>
<li><strong>Any employer match is always pre-tax</strong> (it goes in traditional regardless), so choosing Roth for your own contributions automatically builds a mix.</li>
</ul>
<p>Project the actual balances with the <a href="/calculators/401k-calculator/">401(k) calculator</a> and <a href="/calculators/roth-ira-calculator/">Roth IRA calculator</a>, check what your withdrawals could sustainably be with the <a href="/calculators/retirement-withdrawal-calculator/">retirement withdrawal calculator</a>, and see how tax rates change your take-home today with the <a href="/calculators/take-home-pay-calculator/">take-home pay calculator</a>.</p>
""",
        "faqs": [
            ("Should I split between Roth and traditional?", "Splitting is a legitimate hedge when you can't confidently predict your retirement bracket — common in the 22-24% brackets. You'll retire with both a taxable and a tax-free bucket, which also lets you manage your taxable income year by year in retirement."),
            ("Does the employer match go into the Roth side?", "No. Matching dollars are always pre-tax (traditional), even if your own contributions are Roth. Under SECURE 2.0 some plans now offer Roth matching if the employer opts in, but the default remains pre-tax — so most Roth contributors end up with a mix automatically."),
            ("What if tax rates go up for everyone?", "Broad rate increases favor Roth: you prepaid at the old, lower rate. Traditional contributions bet that your personal rate falls in retirement by more than any legislated increases. That asymmetry is one reason many planners lean Roth when the fair-math comparison is close."),
            ("Is the Roth 401(k) limit really the same as traditional?", "Yes — $23,500 (2025) either way, plus catch-ups from age 50. That's the max-out subtlety: $23,500 of Roth is worth more after tax than $23,500 of traditional, because the Roth version has already paid its tax bill outside the cap."),
        ],
    },
]
