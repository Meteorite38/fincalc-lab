# -*- coding: utf-8 -*-
"""CD ladder calculator — builds the rung schedule, blended yield vs all-short/all-long, liquidity calendar."""

CDLADDER = [
    {
        "slug": "cd-ladder-calculator",
        "emoji": "\U0001FA9C",
        "category": "Savings & Investing",
        "title": "CD Ladder Calculator — Build the Rungs, See the Blended Yield",
        "h1": "CD Ladder Calculator",
        "blurb": "Split a lump sum into a CD ladder: rung schedule, blended APY, and what each year unlocks.",
        "meta_description": "Free CD ladder calculator: split your savings across 1-5 year CDs, see each rung's maturity date and interest, the ladder's blended APY, and how it compares to going all-short or all-long.",
        "intro": "A CD ladder solves the saver's dilemma — long CDs pay more but lock your money; short CDs stay liquid but pay less. Splitting the money across staggered maturities captures most of the long-term rate while freeing a rung every year. This calculator builds your ladder and prices it against the alternatives.",
        "fields": [
            {"id": "amount", "label": "Total to invest ($)", "value": 50000},
            {"id": "rungs", "label": "Number of rungs (years)", "type": "select", "value": "5",
             "options": [("3", "3-year ladder"), ("4", "4-year ladder"), ("5", "5-year ladder")]},
            {"id": "r1", "label": "1-year CD rate (%)", "value": 4.3, "step": 0.05},
            {"id": "r2", "label": "2-year CD rate (%)", "value": 4.0, "step": 0.05},
            {"id": "r3", "label": "3-year CD rate (%)", "value": 3.9, "step": 0.05},
            {"id": "r4", "label": "4-year CD rate (%)", "value": 3.85, "step": 0.05},
            {"id": "r5", "label": "5-year CD rate (%)", "value": 3.8, "step": 0.05},
        ],
        "js": """
function calculate() {
  const A = val('amount'), n = parseInt(document.getElementById('rungs').value, 10);
  const rates = [val('r1'), val('r2'), val('r3'), val('r4'), val('r5')].map(x => x/100);
  if (A <= 0) { show('<div class="result-main">Enter an amount to invest.</div>'); return; }
  const per = A / n;
  let rows = '', totalInterest = 0, weightedYrs = 0;
  const year = new Date().getFullYear();
  for (let k = 1; k <= n; k++) {
    const r = rates[k-1];
    const fv = per * Math.pow(1 + r, k);
    const interest = fv - per;
    totalInterest += interest;
    weightedYrs += k;
    rows += `<tr><td>Rung ${k}: $${fmt(per,0)} in a ${k}-year CD @ ${fmt(r*100,2)}%</td><td>matures ${year + k}</td><td>$${fmt(fv,0)} <small>(+$${fmt(interest,0)})</small></td></tr>`;
  }
  // blended simple annual yield across the ladder's average life
  const avgLife = weightedYrs / n;
  const blended = Math.pow((A + totalInterest) / A, 1 / avgLife) - 1;
  // alternatives over the same average life
  const allShort = A * (Math.pow(1 + rates[0], avgLife) - 1);
  const allLong = A * (Math.pow(1 + rates[n-1], avgLife) - 1);
  const ladderGain = totalInterest;
  show(`<div class="result-main">${fmt(blended*100,2)}% blended annual yield<small>$${fmt(totalInterest,0)} of total interest as the ${n} rungs mature &middot; one rung (~$${fmt(per,0)}+) unlocks every year</small></div>
  <table>
    <tr><th>Rung</th><th>Matures</th><th>Value at maturity</th></tr>
    ${rows}
  </table>
  <table>
    <tr><td>The ladder (average life ${fmt(avgLife,1)} yrs)</td><td><strong>$${fmt(ladderGain,0)}</strong> interest</td></tr>
    <tr><td>Everything in 1-year CDs, rolled (at today's ${fmt(rates[0]*100,2)}%)</td><td>$${fmt(allShort,0)} — full liquidity every year, but the rate floats with the market</td></tr>
    <tr><td>Everything in the ${n}-year CD</td><td>$${fmt(allLong,0)} — highest lock-in, zero access until ${year + n}</td></tr>
  </table>
  <p>After year ${n === 3 ? 3 : n}, the ladder becomes self-sustaining: each maturing rung rolls into a new ${n}-year CD at whatever rates then offer — from that point every dollar earns the long-term rate while a rung still frees up annually.</p>`);
}
""",
        "body_html": """
<h2>How a ladder works</h2>
<p>Split the money into equal rungs — $50,000 into five $10,000 pieces — and buy CDs maturing in 1, 2, 3, 4 and 5 years. Every year one rung matures. Spend it if life demands; otherwise roll it into a fresh <em>5-year</em> CD. After the initial build-out, the ladder reaches its steady state: <strong>every dollar is earning 5-year rates, yet a fifth of the money comes free every single year.</strong> That's the whole trick — long-term yield with short-term access, no forecasting required.</p>
<h2>When the yield curve is inverted (like now)</h2>
<p>The classic ladder assumes longer CDs pay more. Periodically the curve <strong>inverts</strong> — 1-year CDs out-yield 5-year ones, as the defaults in this calculator show — and the ladder looks silly on paper: why lock 3.8% for five years when 4.3% is available for one? The answer is what the ladder is <em>for</em>: the 1-year rate is only good for one year, and if rates fall you'll be rolling at 3%, then 2.5%. The 5-year rung locks today's rate against that future. An inverted curve is the market betting rates will drop — exactly the scenario where locked long rungs earn their keep. Ladders are a hedge against having to guess; that's the point.</p>
<h2>Building it: mechanics that matter</h2>
<ul>
<li><strong>Buy at multiple banks if it helps</strong> — the best 1-year and best 5-year rates are rarely at the same institution. Rate-shopping each rung separately can add 0.3-0.5% of blended yield. (Keep each bank under the $250,000 FDIC ceiling — per depositor, per bank.)</li>
<li><strong>Check early-withdrawal penalties before buying.</strong> Typical: 3-6 months of interest on short CDs, 6-12 months on long ones. A 5-year CD with a mild 6-month penalty is effectively a rate hedge with an escape hatch — sometimes worth breaking deliberately if rates spike.</li>
<li><strong>Mind the auto-renewal trap.</strong> Banks default maturing CDs into renewal at whatever their current (often mediocre) rate is, with a short 7-10 day grace window. Calendar every maturity date; the ladder only works if you actively re-shop each rung.</li>
<li><strong>Brokered CDs</strong> (bought through a brokerage account) put every bank's inventory in one screen and can be sold on a secondary market instead of paying penalties — at market price, which can mean a loss. Convenient for big ladders; check the <a href="/calculators/apy-calculator/">APY math</a> carefully since brokered CDs pay simple interest to a cash account rather than compounding.</li>
</ul>
<h2>What belongs in a ladder — and what doesn't</h2>
<p>CDs suit money with a <strong>known medium horizon</strong>: a house down payment three years out (pair with the <a href="/calculators/house-down-payment-calculator/">down payment calculator</a>), tuition due in stages, a car replacement fund, or the cash allocation of a retiree's <a href="/calculators/savings-runway-calculator/">spending runway</a>. The <a href="/calculators/emergency-fund-calculator/">emergency fund</a> mostly doesn't belong here — emergencies don't wait for maturity dates; keep that in a high-yield savings account, though some people ladder a <em>portion</em> once the liquid core is solid. And long-horizon money (10+ years) pays a heavy price for CD safety: at 4% vs the stock market's historical ~10%, $50,000 over 20 years grows to $110,000 instead of $336,000 — the <a href="/calculators/compound-interest-calculator/">compound interest calculator</a> makes the gap vivid. Match the tool to the horizon: ladders are for the middle distance.</p>
<h2>Ladder vs high-yield savings vs Treasuries</h2>
<p>Three fair competitors for the same dollars: <strong>High-yield savings</strong> — fully liquid, rate changes at the bank's whim; wins for horizons under a year. <strong>Treasury ladders</strong> — same structure using T-bills/notes: state-tax-free interest (material in high-tax states), no early-withdrawal penalty (sell anytime at market), and often comparable yields; the stronger choice for six-figure ladders if you're comfortable with a brokerage account. <strong>The CD ladder</strong> wins on simplicity, FDIC clarity, and — during promotions — the odd 5%+ special that beats everything. Whichever wrapper you choose, the real return after inflation is what compounds; the <a href="/calculators/real-return-calculator/">real return calculator</a> keeps that honest.</p>
""",
        "faqs": [
            ("What CD terms should a ladder use?", "The classic is five rungs of 1-5 years, renewing into 5-year CDs — a good default because 5-year rates capture most of the curve. Shorter 3-rung ladders (1/2/3yr) suit money needed sooner or savers wanting faster access to rate rises; some build 6-month mini-ladders for near-term cash. The structure matters more than the exact terms."),
            ("What happens when a CD in my ladder matures?", "You get a grace window (usually 7-10 days) to move the money penalty-free. Roll it into a new longest-term CD to maintain the ladder, spend it if that was the plan, or re-shop to a better bank — never let it auto-renew unexamined, since banks routinely renew at below-market rates."),
            ("Are CD ladders worth it when savings accounts pay the same?", "A top high-yield savings rate matching a 1-year CD is common at the top of a rate cycle — but the savings rate can drop next month, while each CD rung is contractual. The ladder isn't trying to beat today's savings rate; it's insuring years 2-5 against cuts. If rates rise instead, your maturing rung re-buys at the higher rate every year — that's the self-correcting design."),
            ("How is CD interest taxed?", "As ordinary income, in the year it's credited — even inside a multi-year CD you haven't touched (the bank 1099s the accrued interest annually). In taxable accounts at high brackets, Treasury ladders often win after tax since Treasury interest skips state income tax. CDs inside an IRA sidestep the annual-tax issue entirely."),
            ("Can I lose money in a CD?", "Not to market movement — principal plus stated interest is FDIC-insured up to $250,000 per depositor per bank. The two real risks are soft: early-withdrawal penalties can eat into principal-adjacent interest if you break a long CD early, and inflation can outrun the locked rate — a 4% CD during 6% inflation loses purchasing power while gaining dollars."),
        ],
    },
]
