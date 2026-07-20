# -*- coding: utf-8 -*-
"""Batch 12 calculators: capital gains tax, cost of waiting to invest."""

PART14 = [
    {
        "slug": "capital-gains-tax-calculator",
        "emoji": "\U0001F4C8",
        "category": "Taxes & Shopping",
        "title": "Capital Gains Tax Calculator — Tax on Investment Profit",
        "h1": "Capital Gains Tax Calculator",
        "blurb": "Estimate tax owed and net profit on an investment sale.",
        "meta_description": "Estimate the capital gains tax on selling an investment: your gain, the tax owed at your rate, and the net profit you keep. Works for any country's rate.",
        "intro": "Selling an investment for a profit usually triggers tax on the gain. Enter your purchase and sale details plus your capital gains tax rate to see the gain, the tax, and what you keep.",
        "fields": [
            {"id": "buy", "label": "Total purchase cost ($)", "value": 10000, "hint": "including fees (your cost basis)"},
            {"id": "sell", "label": "Total sale proceeds ($)", "value": 18000, "hint": "after selling fees"},
            {"id": "rate", "label": "Capital gains tax rate (%)", "value": 15, "step": 0.5, "hint": "your applicable rate"},
        ],
        "js": """
function calculate() {
  const buy = val('buy'), sell = val('sell'), rate = val('rate')/100;
  const gain = sell - buy;
  if (gain <= 0) {
    show(`<div class="result-main">$0 tax<small>No taxable gain — sale proceeds don't exceed your cost basis${gain<0?' (a $'+fmt(-gain,0)+' loss, which may offset other gains)':''}</small></div>
    <table><tr><td>Cost basis</td><td>$${fmt(buy,0)}</td></tr><tr><td>Sale proceeds</td><td>$${fmt(sell,0)}</td></tr><tr><td>Result</td><td>${gain<0?'Loss of $'+fmt(-gain,0):'No gain'}</td></tr></table>`);
    return;
  }
  const tax = gain * rate;
  const net = sell - tax;
  const netProfit = gain - tax;
  show(`<div class="result-main">$${fmt(tax,0)} tax<small>on a $${fmt(gain,0)} gain at ${fmt(rate*100,1)}%</small></div>
  <table>
    <tr><td>Capital gain</td><td>$${fmt(gain,0)}</td></tr>
    <tr><td>Tax owed</td><td>$${fmt(tax,0)}</td></tr>
    <tr><td>Profit after tax</td><td>$${fmt(netProfit,0)}</td></tr>
    <tr><td>Total cash you keep</td><td>$${fmt(net,0)}</td></tr>
    <tr><td>Effective tax on your profit</td><td>${fmt(rate*100,1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What capital gains tax is</h2>
<p>When you sell an investment — stocks, funds, property, crypto — for more than you paid, the profit is a <strong>capital gain</strong>, and most governments tax it. The tax applies only to the <em>gain</em>, not the whole sale amount: if you bought for $10,000 and sold for $18,000, only the $8,000 profit is taxed. Your original cost (including fees) is the "cost basis" that's subtracted first.</p>
<h2>Short-term vs long-term matters a lot</h2>
<p>Many tax systems reward patience. In the US, for example, assets held <strong>over a year</strong> qualify for lower "long-term" capital gains rates (often 0%, 15%, or 20% depending on income), while assets sold within a year are taxed as ordinary income at potentially much higher rates. That difference can be enormous — sometimes worth deliberately waiting past the one-year mark before selling. Because rates vary by country, holding period, and income, this calculator lets you enter <em>your</em> applicable rate.</p>
<h2>Ways to legally reduce the tax</h2>
<ul>
<li><strong>Hold longer</strong> where a lower long-term rate applies — patience is literally rewarded.</li>
<li><strong>Use tax-advantaged accounts.</strong> Gains inside retirement accounts (401(k), IRA, ISA, and equivalents) are typically tax-deferred or tax-free — one of the biggest reasons to invest there first, per the <a href="/articles/financial-order-of-operations/">order of operations</a>.</li>
<li><strong>Tax-loss harvesting.</strong> Selling a losing investment realizes a loss that can offset gains elsewhere, lowering your bill. This tool shows a loss when proceeds are below basis.</li>
<li><strong>Spread sales across tax years</strong> to stay in a lower bracket, where applicable.</li>
</ul>
<h2>Important caveats</h2>
<p>This is a simplified estimate. Real capital gains tax depends on your total income, filing status, holding period, local rules, allowances or exemptions, and sometimes a separate rate for different asset types. It doesn't account for tax-free allowances many countries provide. Treat the result as a planning guide, and consult a tax professional for a binding figure — but knowing the rough tax on a sale helps you decide <em>whether</em> and <em>when</em> to sell in the first place.</p>
""",
        "faqs": [
            ("How is capital gains tax calculated?", "It's your tax rate applied to the gain — the sale proceeds minus your cost basis (what you paid including fees). Only the profit is taxed, not the entire sale amount."),
            ("What's the difference between short-term and long-term gains?", "Many systems tax assets held over a year at lower long-term rates and assets sold within a year at higher ordinary-income rates. Holding past the long-term threshold can significantly cut the tax."),
            ("How can I reduce capital gains tax?", "Hold assets long enough to qualify for lower long-term rates, invest inside tax-advantaged accounts where gains are sheltered, offset gains with realized losses (tax-loss harvesting), and time sales across tax years where it keeps you in a lower bracket."),
        ],
    },
    {
        "slug": "cost-of-waiting-calculator",
        "emoji": "\u23F1\uFE0F",
        "category": "Savings & Investing",
        "title": "Cost of Waiting to Invest Calculator — The Price of Delay",
        "h1": "Cost of Waiting to Invest Calculator",
        "blurb": "How much delaying investing by a few years really costs.",
        "meta_description": "See how much waiting to start investing costs you. Compare starting now versus delaying a few years — the gap is bigger than almost anyone expects.",
        "intro": "\"I'll start investing next year\" is one of the most expensive sentences in personal finance. Enter your plan to see exactly what delaying by a few years costs your future self.",
        "fields": [
            {"id": "monthly", "label": "Monthly investment ($)", "value": 400},
            {"id": "rate", "label": "Expected annual return (%)", "value": 7, "step": 0.1},
            {"id": "years", "label": "Years until you'll need it", "value": 35, "step": 1},
            {"id": "delay", "label": "Years you delay starting", "value": 5, "step": 1},
        ],
        "js": """
function fvSeries(monthly, annual, years) {
  const i = annual/100/12, n = Math.round(years*12);
  return i>0 ? monthly*((Math.pow(1+i,n)-1)/i) : monthly*n;
}
function calculate() {
  const m = val('monthly'), r = val('rate'), total = val('years'), delay = Math.min(val('delay'), val('years'));
  if (total <= 0) { show('<div class="result-main">Enter a positive time horizon.</div>'); return; }
  const startNow = fvSeries(m, r, total);
  const startLater = fvSeries(m, r, total - delay);
  const cost = startNow - startLater;
  const extraContrib = m * 12 * delay;   // contributions skipped during delay
  show(`<div class="result-main">$${fmt(cost,0)}<small>The cost of waiting ${delay} year${delay==1?'':'s'} to start</small></div>
  <table>
    <tr><td>If you start now</td><td>$${fmt(startNow,0)}</td></tr>
    <tr><td>If you wait ${delay} year${delay==1?'':'s'}</td><td>$${fmt(startLater,0)}</td></tr>
    <tr><td>Difference (cost of delay)</td><td>$${fmt(cost,0)}</td></tr>
    <tr><td>Contributions you skipped</td><td>$${fmt(extraContrib,0)}</td></tr>
    <tr><td>Lost growth on top of that</td><td>$${fmt(Math.max(0,cost-extraContrib),0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why waiting is so expensive</h2>
<p>Delaying investing doesn't just cost you the contributions you skip — it costs you all the <em>growth</em> those early dollars would have generated, compounding for the entire rest of your timeline. And because the earliest dollars compound the longest, they're the most valuable ones of all. Skipping them is skipping your best years of growth.</p>
<h2>A striking example</h2>
<p>Invest $400/month at 7% for 35 years and you reach roughly $690,000. Wait just 5 years and invest for 30 instead, and you end with about $470,000. That 5-year delay cost around <strong>$220,000</strong> — even though you only "saved" $24,000 by not contributing during those years. The other ~$196,000 is pure lost growth. Waiting 5 years didn't cost 5 years of contributions; it cost a fortune in compounding.</p>
<h2>The lesson: start now, even small</h2>
<ul>
<li><strong>Time beats amount.</strong> Starting with a small amount today usually beats starting with a larger amount later, because compounding rewards duration more than size — the core lesson of <a href="/articles/how-compound-interest-builds-wealth/">compound interest</a>.</li>
<li><strong>Don't wait for the "right time" or more money.</strong> There's rarely a perfect moment, and the cost of waiting for one is enormous. Begin with whatever you can and increase it as income grows.</li>
<li><strong>Automate immediately.</strong> Set up an automatic monthly contribution into a low-cost <a href="/articles/index-funds-explained/">index fund</a> today, even a modest one, and raise it later. Getting started is the hard part; <a href="/articles/dollar-cost-averaging-explained/">dollar-cost averaging</a> handles the rest.</li>
</ul>
<h2>Turn the number into action</h2>
<p>Run your own delay through the calculator — the figure is usually shocking enough to end the procrastination. Then act on it the same day: open an account, set up a small automatic transfer, and let time start working <em>for</em> you instead of against you. The most expensive investing mistake isn't picking the wrong fund; it's not starting.</p>
""",
        "faqs": [
            ("How much does waiting to invest cost?", "Far more than the skipped contributions, because you also lose all the compounding growth those early dollars would have earned over your entire time horizon. Delaying 5 years can cost hundreds of thousands over a long career."),
            ("Is it better to start small now or wait until I can invest more?", "Almost always start now. Because the earliest dollars compound the longest, starting small immediately typically beats waiting to invest a larger amount later. You can increase contributions as your income grows."),
            ("What return should I assume?", "A diversified stock portfolio has historically returned around 7% a year before inflation over long periods. Use 6–7% for a realistic estimate, or lower for an inflation-adjusted figure."),
        ],
    },
]
