# -*- coding: utf-8 -*-
"""Job offer comparison — total annual value (salary/bonus/match/PTO/insurance) plus true hourly pay including commute."""

JOBOFFER = [
    {
        "slug": "job-offer-comparison-calculator",
        "emoji": "\U0001F91D",
        "category": "Income & Budgeting",
        "title": "Job Offer Comparison Calculator — Total Value, Not Just Salary",
        "h1": "Job Offer Comparison Calculator",
        "blurb": "Two offers priced on everything: bonus, match, PTO, insurance, commute — and true hourly pay.",
        "meta_description": "Free job offer comparison calculator: compare two offers on total annual value — salary, bonus, 401(k) match, PTO worth, health insurance costs — plus the true hourly wage once commute time and work hours are counted.",
        "intro": "Two offers, one number each — and the bigger salary is routinely the worse deal once the 401(k) match, bonus, PTO, insurance premiums and a longer commute are priced. This calculator totals each offer's real annual value and computes the truest metric of all: what each job pays per hour of your life.",
        "fields": [
            {"id": "salA", "label": "Offer A: base salary ($/yr)", "value": 85000},
            {"id": "bonusA", "label": "Offer A: expected bonus (%)", "value": 5, "step": 0.5},
            {"id": "matchA", "label": "Offer A: 401(k) match (% of salary)", "value": 4, "step": 0.5},
            {"id": "ptoA", "label": "Offer A: PTO + holidays (days)", "value": 20, "step": 1},
            {"id": "insA", "label": "Offer A: your health premium ($/mo)", "value": 150, "hint": "your share, from the benefits summary"},
            {"id": "commuteA", "label": "Offer A: commute round-trip (min/day)", "value": 60, "step": 5, "hint": "0 if remote"},
            {"id": "salB", "label": "Offer B: base salary ($/yr)", "value": 92000},
            {"id": "bonusB", "label": "Offer B: expected bonus (%)", "value": 0, "step": 0.5},
            {"id": "matchB", "label": "Offer B: 401(k) match (% of salary)", "value": 0, "step": 0.5},
            {"id": "ptoB", "label": "Offer B: PTO + holidays (days)", "value": 12, "step": 1},
            {"id": "insB", "label": "Offer B: your health premium ($/mo)", "value": 350},
            {"id": "commuteB", "label": "Offer B: commute round-trip (min/day)", "value": 90, "step": 5},
        ],
        "js": """
function offerValue(sal, bonusPct, matchPct, pto, insMo, commuteMin) {
  const workDays = 260 - pto;
  const dailyPay = sal / 260;
  const bonus = sal * bonusPct / 100;
  const match = sal * matchPct / 100;
  const ptoValue = pto * dailyPay;           // paid days off, valued at the daily rate
  const insCost = insMo * 12;
  const total = sal + bonus + match - insCost;
  const hoursWorked = workDays * 8 + workDays * commuteMin / 60;
  const hourly = total / hoursWorked;
  return { total: total, bonus: bonus, match: match, ptoValue: ptoValue, insCost: insCost,
           hourly: hourly, hoursWorked: hoursWorked, workDays: workDays, commuteHrs: workDays * commuteMin / 60 };
}
function calculate() {
  const A = offerValue(val('salA'), val('bonusA'), val('matchA'), Math.round(val('ptoA')), val('insA'), val('commuteA'));
  const B = offerValue(val('salB'), val('bonusB'), val('matchB'), Math.round(val('ptoB')), val('insB'), val('commuteB'));
  if (val('salA') <= 0 || val('salB') <= 0) { show('<div class="result-main">Enter both base salaries.</div>'); return; }
  const dTotal = A.total - B.total, dHourly = A.hourly - B.hourly;
  const winner = dHourly > 0.05 ? 'A' : (dHourly < -0.05 ? 'B' : 'tie');
  const flip = (A.total > B.total) !== (A.hourly > B.hourly) && winner !== 'tie';
  show(`<div class="result-main">Offer ${winner === 'tie' ? 'A ≈ B' : winner + ' wins'}<small>$${fmt(A.hourly,2)}/hr vs $${fmt(B.hourly,2)}/hr of your actual time &middot; total value $${fmt(A.total,0)} vs $${fmt(B.total,0)}</small></div>
  <table>
    <tr><th></th><th>Offer A</th><th>Offer B</th></tr>
    <tr><td>Base salary</td><td>$${fmt(val('salA'),0)}</td><td>$${fmt(val('salB'),0)}</td></tr>
    <tr><td>Expected bonus</td><td>$${fmt(A.bonus,0)}</td><td>$${fmt(B.bonus,0)}</td></tr>
    <tr><td>401(k) match (free money)</td><td>$${fmt(A.match,0)}</td><td>$${fmt(B.match,0)}</td></tr>
    <tr><td>Health premiums (your share)</td><td>&minus;$${fmt(A.insCost,0)}</td><td>&minus;$${fmt(B.insCost,0)}</td></tr>
    <tr><td><strong>Total annual value</strong></td><td><strong>$${fmt(A.total,0)}</strong></td><td><strong>$${fmt(B.total,0)}</strong></td></tr>
    <tr><td>Paid days off (already inside salary)</td><td>${Math.round(val('ptoA'))} days (worth $${fmt(A.ptoValue,0)})</td><td>${Math.round(val('ptoB'))} days (worth $${fmt(B.ptoValue,0)})</td></tr>
    <tr><td>Hours: work + commute per year</td><td>${fmt(A.hoursWorked,0)} (${fmt(A.commuteHrs,0)} commuting)</td><td>${fmt(B.hoursWorked,0)} (${fmt(B.commuteHrs,0)} commuting)</td></tr>
    <tr><td><strong>True hourly rate</strong></td><td><strong>$${fmt(A.hourly,2)}</strong></td><td><strong>$${fmt(B.hourly,2)}</strong></td></tr>
  </table>
  <p>${flip
    ? `<strong>Note the flip:</strong> Offer ${A.total > B.total ? 'A' : 'B'} pays more per year, but Offer ${winner} pays more per hour of your life — the difference is PTO and commute. Decide which currency you're optimizing.`
    : (winner === 'tie'
      ? `Financially a coin flip — let the unpriceables decide: growth trajectory, manager quality, stability, and how each place felt.`
      : `Offer ${winner} leads on both totals and per-hour value${Math.abs(dTotal) > 3000 ? ' — a $' + fmt(Math.abs(dTotal),0) + '/yr gap that compounds with every future raise being a percentage of it' : ' — narrowly; the unpriceables should carry real weight'}.`)}</p>`);
}
""",
        "body_html": """
<h2>Why the salary number misleads</h2>
<p>Base salary is the loudest number and frequently the least decisive. A $92,000 offer with no match, thin PTO and a $350/month premium share is worth <em>less</em> per year than an $85,000 offer with a 4% match, 20 days off and cheap insurance — before counting a shorter commute. The components people skip: the <strong>401(k) match</strong> is literal free money (4% of $85k is $3,400/year — see <a href="/articles/401k-match-free-money/">why the match comes first</a>); <strong>health premium shares</strong> differ by $2,000-5,000/year between employers for similar coverage, and deductible/out-of-pocket differences can double that gap for families; an <strong>expected bonus</strong> is real but probabilistic — haircut it by how reliably it pays (ask the recruiter what last year's actual payout percentage was); and <strong>PTO</strong> is income you're paid while living — eight extra days is 3% of the year.</p>
<h2>The true-hourly-rate lens</h2>
<p>The second table row that changes decisions: divide each offer's total value by the hours it actually consumes — work hours <em>plus commute</em>, on the days you're not on PTO. A 45-minute-each-way commute is ~360 unpaid hours a year, an entire extra work-month and a half; a remote job's per-hour value routinely beats a 10%-higher in-office salary once those hours enter the denominator (the <a href="/calculators/commute-cost-calculator/">commute calculator</a> adds the driving <em>dollars</em> on top — fuel, wear and parking are their own $2,000-5,000). Per-hour framing also handles culture honestly: a \"$95k\" job whose real norm is 50-hour weeks pays 20% less per hour than the sticker suggested. Ask about actual hours in the interview — it's a compensation question wearing a culture costume.</p>
<h2>What this calculator deliberately leaves out</h2>
<ul>
<li><strong>Equity.</strong> RSUs can dwarf everything above — and deserve their own math with tenure and volatility haircuts; the <a href="/articles/rsus-and-tech-compensation-guide/">RSU guide</a> covers pricing them into an offer.</li>
<li><strong>Raise trajectory and title.</strong> A job paying $3k less but promoting in 18 months wins by year three — every future <a href="/calculators/pay-raise-calculator/">raise</a> compounds off the new base. Weight this heavily early-career.</li>
<li><strong>Stability and severance culture.</strong> A volatile employer's premium is partly risk compensation; discount accordingly.</li>
<li><strong>Retirement plan quality beyond the match</strong> — a plan with 0.8% target-date funds quietly claws back part of the match's value (<a href="/calculators/investment-fee-impact-calculator/">fee impact</a>).</li>
<li><strong>State taxes on a relocation</strong> — a $10k raise moving from Texas to California can net negative; run both versions through the <a href="/calculators/take-home-pay-calculator/">take-home calculator</a>.</li>
</ul>
<h2>Using the output to negotiate</h2>
<p>The gap this calculator surfaces is your negotiation script. If Offer A wins on total value but you prefer B's work, tell B specifically: \"A's package is worth about $4,000 more once the match and premiums are counted — can you close that?\" Concrete component math is far harder to wave off than \"I was hoping for more.\" Remember which levers move easiest: base salary is the stickiest; sign-on bonuses, extra PTO, a review-at-6-months clause, and remote days are routinely granted precisely because they're cheaper than base — but as this calculator shows, they're worth real dollars to <em>you</em>. And whichever offer wins, route the raise deliberately: the <a href="/articles/lifestyle-creep/">save-half-of-every-raise rule</a> is easiest to apply on day one of a new job, when the higher income hasn't become normal yet.</p>
""",
        "faqs": [
            ("How much is a 401(k) match actually worth?", "Face value plus compounding: a 4% match on $85,000 is $3,400/year of free money, and invested over a 30-year career that single year's match becomes ~$25,000. Between two offers, a match gap of 3-4% of salary routinely outweighs a $5,000 base-salary difference — especially since the match compounds while the salary difference gets taxed first."),
            ("How do I value PTO days when comparing offers?", "Each paid day off is worth your daily rate (salary ÷ 260 workdays) — about $327/day at $85,000. An offer with 8 more days effectively pays ~$2,600 more for the same annual output, and unlike bonus money it can't be discretionarily cancelled. Also check accrual vs grant, rollover rules, and whether 'unlimited PTO' comes with a norm of actually taking less."),
            ("Should I count the commute when comparing jobs?", "Yes, twice. As time: commute hours go in the denominator of your true hourly rate — 45 minutes each way is ~360 hours/year, so a shorter commute is a raise paid in life. As money: fuel, parking, wear and tolls add $2,000-5,000/year for typical car commutes. Remote and hybrid arrangements are compensation, not perks — price them like it."),
            ("How should I compare health insurance between two offers?", "Compare your premium share (monthly cost × 12), then the deductible and out-of-pocket max under realistic usage — a family that hits a $4,000 deductible yearly should add that to the 'cost' of the high-deductible offer, minus any employer HSA seed money (free dollars, and the HSA's triple tax advantage has real value). Benefits summaries make this a 10-minute comparison most candidates never do."),
            ("One offer pays more but the job seems worse — how do I decide?", "Price the gap per hour of your life (this calculator's last row), then ask whether the unpriceables — manager, growth, stress, meaning — are worth that hourly difference to you. A $4,000 annual gap is about $2/hour: many people happily 'pay' $2/hour for a better boss. The point of the math isn't to overrule your gut; it's to tell your gut the exact price of following it."),
        ],
    },
]
