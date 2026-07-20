# -*- coding: utf-8 -*-
"""Move or stay (renters) — renewal increase vs all-in cost of moving, breakeven month, negotiation-value framing."""

MOVESTAY = [
    {
        "slug": "move-or-stay-calculator",
        "emoji": "\U0001F69A",
        "category": "Income & Budgeting",
        "title": "Move or Stay Calculator — Is the Rent Increase Worth Moving Over?",
        "h1": "Move or Stay Calculator",
        "blurb": "Renewal increase vs the true all-in cost of moving — breakeven month and the negotiation number.",
        "meta_description": "Free move-or-stay calculator for renters: compare the renewal increase against the full cost of moving — movers, deposits, overlap rent, fees, time off — with the breakeven month and the concession worth asking your landlord for.",
        "intro": "The renewal letter says +$150 a month and moving feels like the principled answer — until you price the truck, the deposit float, the overlap week, the application fees and two days off work. Moving has a fixed cost that a cheaper apartment repays only over time. This calculator finds the breakeven, and the number worth negotiating with instead.",
        "fields": [
            {"id": "current", "label": "Current rent ($/mo)", "value": 1600},
            {"id": "renewal", "label": "Renewal offer ($/mo)", "value": 1750},
            {"id": "newrent", "label": "Comparable place elsewhere ($/mo)", "value": 1600, "hint": "realistic listings, same quality band"},
            {"id": "movers", "label": "Movers / truck / supplies ($)", "value": 900},
            {"id": "fees", "label": "Application, admin & broker fees ($)", "value": 300, "hint": "$50-150 per application; broker fee where applicable"},
            {"id": "overlap", "label": "Overlap / double-rent days", "value": 7, "step": 1, "hint": "days paying both places"},
            {"id": "workdays", "label": "Unpaid days off to move", "value": 1, "step": 0.5},
            {"id": "dailypay", "label": "Your daily pay ($)", "value": 220, "hint": "for valuing the time off"},
            {"id": "horizon", "label": "Months you'd stay at the next place", "value": 24, "step": 1},
        ],
        "js": """
function calculate() {
  const cur = val('current'), ren = val('renewal'), nw = val('newrent');
  const movers = Math.max(0, val('movers')), fees = Math.max(0, val('fees'));
  const overlapDays = Math.max(0, val('overlap')), workdays = Math.max(0, val('workdays')), daily = Math.max(0, val('dailypay'));
  const H = Math.max(1, Math.round(val('horizon')));
  if (cur <= 0 || ren <= 0 || nw <= 0) { show('<div class="result-main">Enter all three rents.</div>'); return; }
  const overlapCost = nw / 30 * overlapDays;
  const timeCost = workdays * daily;
  const moveCost = movers + fees + overlapCost + timeCost;
  const monthlySave = ren - nw;
  const stayTotal = ren * H;
  const moveTotal = nw * H + moveCost;
  const diff = stayTotal - moveTotal;
  const breakeven = monthlySave > 0 ? Math.ceil(moveCost / monthlySave) : -1;
  const negotiate = monthlySave > 0 ? Math.max(0, ren - (nw + moveCost / H)) : 0;
  const verdict = monthlySave <= 0
    ? `Comparable places cost the same or more — staying wins outright, and the renewal ask is roughly market. Negotiate the extras (parking, a longer lease) rather than the headline rent.`
    : (breakeven > 0 && breakeven <= H
      ? `Moving pays for itself in <strong>month ${breakeven}</strong> and nets $${fmt(diff,0)} over ${H} months — the increase is genuinely above what the market charges.`
      : `Moving never breaks even inside your ${H}-month horizon — the $${fmt(moveCost,0)} of moving friction outweighs the $${fmt(monthlySave,0)}/month gap. Stay, but use the math below to negotiate.`);
  show(`<div class="result-main">${diff > 0 && monthlySave > 0 ? 'Moving saves $' + fmt(diff,0) : 'Staying saves $' + fmt(Math.max(0,-diff),0)}<small>over ${H} months, all-in &middot; true cost of the move: $${fmt(moveCost,0)}${breakeven > 0 && monthlySave > 0 ? ' &middot; breakeven month ' + breakeven : ''}</small></div>
  <table>
    <tr><th></th><th>Stay at renewal</th><th>Move</th></tr>
    <tr><td>Rent over ${H} months</td><td>$${fmt(stayTotal,0)}</td><td>$${fmt(nw*H,0)}</td></tr>
    <tr><td>Movers + supplies</td><td>—</td><td>$${fmt(movers,0)}</td></tr>
    <tr><td>Fees (application/admin/broker)</td><td>—</td><td>$${fmt(fees,0)}</td></tr>
    <tr><td>Overlap rent (${fmt(overlapDays,0)} days)</td><td>—</td><td>$${fmt(overlapCost,0)}</td></tr>
    <tr><td>Time off (${fmt(workdays,1)} day${workdays === 1 ? '' : 's'})</td><td>—</td><td>$${fmt(timeCost,0)}</td></tr>
    <tr><td><strong>Total</strong></td><td><strong>$${fmt(stayTotal,0)}</strong></td><td><strong>$${fmt(moveTotal,0)}</strong></td></tr>
  </table>
  <p>${verdict}</p>
  ${negotiate > 5 && monthlySave > 0 ? `<p><strong>The negotiation number:</strong> a renewal at <strong>$${fmt(ren - negotiate,0)}</strong> makes staying exactly as cheap as moving — that's your walk-away line. Landlords face their own turnover cost (vacancy, turnover prep, re-listing — commonly $2,000-4,000), so an ask $${fmt(Math.min(negotiate, ren-nw),0)} below the renewal offer is credible precisely because your leaving costs them real money too.</p>` : ''}`);
}
""",
        "body_html": """
<h2>Why moving costs more than the truck</h2>
<p>The visible bill — movers or a truck weekend — is usually the minority of the real cost. The stack: <strong>application and admin fees</strong> ($50-150 per application, often across several attempts; broker fees of a month's rent in some markets), <strong>deposit float</strong> (the new deposit is due weeks before the old one returns — a cash-flow squeeze even when it nets to zero, and old deposits come back imperfect more often than not), <strong>overlap rent</strong> (nobody moves at midnight on the 31st; a livable transition costs 3-10 days of double rent), <strong>time</strong> (packing, hunting, applications, the move itself — days of it, some unpaid), and the <strong>re-setup drift</strong> — curtains that don't fit, the new parking permit, utility connection fees. Summed honestly, a local move runs $1,500-3,500 for most renters. That's the fixed cost a cheaper apartment has to amortize — and why a $50 increase is almost never worth moving over, while a $250 one very often is.</p>
<h2>The landlord's math (your negotiation leverage)</h2>
<p>Turnover costs the landlord too: a vacant month ($1,600+ right there), turnover prep (paint, cleaning, small repairs — $500-1,500), re-listing effort or a leasing fee, and the risk the next tenant is worse. Total: commonly <strong>$2,000-4,000</strong> — which is exactly why retention discounts exist and why the first renewal letter is an opening bid, not a verdict. The strongest counter is specific: comparable listings at $X (bring links), your on-time payment history, and a concrete counteroffer near the walk-away number this calculator computes. Sweeteners that cost the landlord little — a 18-24 month lease at a smaller bump, a parking spot, a paint refresh — often bridge the last $50. The <a href="/calculators/rent-increase-calculator/">rent increase calculator</a> checks the ask against inflation for one more data point in the email.</p>
<h2>What the spreadsheet can't see</h2>
<p>Run the money honestly, then weigh the rest at full value: a shorter <a href="/calculators/commute-cost-calculator/">commute</a> is worth real dollars <em>and</em> real life; school zones, noise, safety, a building you've outgrown — all legitimate reasons to move at a financial loss or stay at one. The calculator's job is making the <em>price</em> of the choice visible, not making the choice. Two structural notes worth folding in: staying usually preserves <strong>leverage for next year</strong> (a tenant who just unpacked won't move over $100; landlords know), so a hard-negotiated renewal this year beats a soft one; and if rent keeps outrunning your income, the durable fix is the <a href="/calculators/rent-affordability-calculator/">affordability check</a> — and eventually the <a href="/calculators/rent-vs-buy-calculator/">rent vs buy question</a> — not annual moving roulette.</p>
<h2>If you do move: cutting the fixed cost</h2>
<ul>
<li><strong>Time the market:</strong> winter leases (Nov-Feb) list 3-7% below summer in most cities — the same apartment, cheaper, with a motivated landlord.</li>
<li><strong>Negotiate the new place too:</strong> ask for a free month on a 13-month lease (common on new buildings), waived admin fees, or included parking — concessions are standard in soft markets.</li>
<li><strong>Move mid-week, off-peak:</strong> movers quote 20-30% less Tuesday-Thursday and mid-month than on the month-end weekend everyone wants.</li>
<li><strong>Document the old place</strong> on the way out (video walkthrough, meter photos) — the cheapest insurance for getting the full deposit back on schedule.</li>
<li><strong>Purge before packing:</strong> every box not moved is money — and the <a href="/calculators/unit-price-calculator/">cost-per-use lens</a> applied to furniture usually shrinks the truck by a size.</li>
</ul>
""",
        "faqs": [
            ("How much does moving to a new apartment actually cost?", "For a typical local move, $1,500-3,500 all-in once you count movers or truck ($400-1,500), application/admin/broker fees ($100-2,000 by market), 3-10 days of overlap rent, deposit float, utility setup, and a day or two off work. The figure most people budget is just the truck — which is why increases that 'obviously justify moving' often don't."),
            ("Is a $150/month rent increase worth moving over?", "Only if a genuinely comparable place rents for meaningfully less and you'll stay long enough to repay the moving cost. At $150/month saved and $2,500 of moving cost, breakeven is 17 months — worth it on a 2+ year horizon, not for a one-year stay. If comparables cost the same as your renewal, the increase is the market and moving buys nothing."),
            ("How do I negotiate a rent renewal?", "Reply in writing with three things: comparable current listings (links, not vibes), your record as a tenant (on-time payments, no complaints), and a specific counteroffer — ideally near the number where staying equals moving, which this calculator computes. Offering a longer lease at a smaller increase is the highest-hit-rate trade because it directly attacks the landlord's turnover risk."),
            ("When is the cheapest time to sign a lease?", "Late fall through winter — demand bottoms, and effective rents (after concessions) run several percent below the summer peak. If your lease ends in July, one strategic move to a winter cycle (via a short renewal or an 18-month lease) can permanently shift you onto the cheaper calendar."),
            ("Should I stay just because moving is exhausting?", "The exhaustion is a real cost — this calculator literally prices your days off — but don't let it silently double every year. The failure mode is accepting increase after increase because 'moving is a hassle' until you're paying $300/month over market. Run the numbers annually; when the gap crosses breakeven inside 12-18 months, the hassle has become a subscription you're overpaying for."),
        ],
    },
]
