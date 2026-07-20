# -*- coding: utf-8 -*-
"""Solo 401(k) vs SEP IRA — max contribution math for sole proprietors (employee deferral + employer share), catch-up, side-hustle case."""

SOLO401K = [
    {
        "slug": "solo-401k-vs-sep-ira-calculator",
        "emoji": "\U0001F9F0",
        "category": "Business & Self-Employment",
        "title": "Solo 401(k) vs SEP IRA Calculator — Which Shelters More of Your Profit?",
        "h1": "Solo 401(k) vs SEP IRA Calculator",
        "blurb": "Max contributions from your profit — and why the solo 401(k) usually wins.",
        "meta_description": "Free Solo 401(k) vs SEP IRA calculator for the self-employed: exact max contributions from your net profit (employee deferral + 25% employer share, SEP's 20% rule), the tax saved, and when each account wins.",
        "intro": "Self-employment's consolation prize is contribution room employees can only dream of — up to $70,000 a year of tax-advantaged space. But the two main vehicles fill that space very differently: the SEP IRA runs on one percentage, while the solo 401(k) stacks an employee deferral on top of the employer share. This calculator computes both maximums from your actual profit.",
        "fields": [
            {"id": "profit", "label": "Net self-employment profit ($)", "value": 80000, "hint": "Schedule C profit, before SE tax deduction"},
            {"id": "age", "label": "Your age", "value": 40, "step": 1, "hint": "50+ unlocks catch-up in the solo 401(k)"},
            {"id": "w2def", "label": "401(k) deferrals already made at a W-2 job ($)", "value": 0, "hint": "the employee deferral limit is shared across all plans"},
            {"id": "taxrate", "label": "Marginal tax rate (%)", "value": 24, "step": 0.5, "hint": "federal + state combined"},
        ],
        "js": """
function calculate() {
  const P = val('profit'), age = Math.round(val('age'));
  const w2 = Math.max(0, val('w2def')), t = val('taxrate')/100;
  if (P <= 0) { show('<div class="result-main">Enter your net self-employment profit.</div>'); return; }
  // 2025 limits
  const DEF_LIMIT = 23500, CATCHUP = age >= 50 ? (age >= 60 && age <= 63 ? 11250 : 7500) : 0;
  const TOTAL_CAP = 70000;
  const SS_CAP = 176100;
  // SE tax & half deduction (approx, under SS cap logic)
  const base = P * 0.9235;
  const ssPart = Math.min(base, SS_CAP) * 0.124;
  const medPart = base * 0.029;
  const seTax = ssPart + medPart;
  const halfSE = seTax / 2;
  const netEarned = P - halfSE; // compensation base for both plans
  // Employer share: 25% of (netEarned - employer contribution) => 20% of netEarned
  const employer = netEarned * 0.20;
  // SEP: employer share only
  const sep = Math.min(TOTAL_CAP, employer);
  // Solo 401k: employee deferral (shared limit with W-2) + catch-up + employer share, capped
  const defRoom = Math.max(0, DEF_LIMIT - w2);
  const deferral = Math.min(defRoom, netEarned);
  const catchup = age >= 50 ? Math.min(CATCHUP, Math.max(0, netEarned - deferral)) : 0;
  const solo = Math.min(TOTAL_CAP + (age >= 50 ? CATCHUP : 0), deferral + catchup + employer);
  const edge = solo - sep;
  const savSolo = solo * t, savSep = sep * t;
  show(`<div class="result-main">Solo 401(k): $${fmt(solo,0)} vs SEP IRA: $${fmt(sep,0)}<small>the solo 401(k) shelters <strong>$${fmt(edge,0)} more</strong> at $${fmt(P,0)} of profit${age >= 50 ? ' (incl. $' + fmt(catchup,0) + ' catch-up)' : ''}</small></div>
  <table>
    <tr><th></th><th>Solo 401(k)</th><th>SEP IRA</th></tr>
    <tr><td>Employee deferral${w2 > 0 ? ' (after $' + fmt(w2,0) + ' used at W-2 job)' : ''}</td><td>$${fmt(deferral,0)}${catchup > 0 ? ' + $' + fmt(catchup,0) + ' catch-up' : ''}</td><td>— none</td></tr>
    <tr><td>Employer share (~20% of net earnings)</td><td>$${fmt(employer,0)}</td><td>$${fmt(sep,0)}</td></tr>
    <tr><td><strong>Max contribution</strong></td><td><strong>$${fmt(solo,0)}</strong></td><td><strong>$${fmt(sep,0)}</strong></td></tr>
    <tr><td>Tax deferred at ${fmt(t*100,0)}%</td><td>$${fmt(savSolo,0)}</td><td>$${fmt(savSep,0)}</td></tr>
    <tr><td>% of profit sheltered</td><td>${fmt(solo/P*100,1)}%</td><td>${fmt(sep/P*100,1)}%</td></tr>
  </table>
  <p>${P < 100000
    ? `At $${fmt(P,0)} of profit the gap is huge in relative terms: the deferral lets the solo 401(k) shelter ${fmt(solo/P*100,0)}% of profit vs the SEP's ~18-19%. For side hustles and moderate profits, the solo 401(k) is rarely a close call${w2 >= DEF_LIMIT ? ' — though your W-2 deferrals have used the employee limit, narrowing the edge to the catch-up and employer share' : ''}.`
    : `At higher profits the employer share dominates and the two converge — by ~$${fmt(Math.round((TOTAL_CAP)/0.2/0.9*1000)/1000*1000,0)}+ of profit both hit the $${fmt(TOTAL_CAP,0)} cap${age >= 50 ? ' (the solo 401(k) still adds the $' + fmt(CATCHUP,0) + ' catch-up on top)' : ''}. Below that line, the deferral keeps the solo 401(k) ahead.`}</p>`);
}
""",
        "body_html": """
<h2>Same law, different engines</h2>
<p>Both accounts let a self-employed person play employer and employee at once — but only the solo 401(k) pays you for both roles. The <strong>SEP IRA</strong> takes a single employer contribution: 25% of W-2 wages, which for sole proprietors works out to <strong>~20% of net self-employment earnings</strong> (profit minus half the <a href="/calculators/self-employment-tax-calculator/">SE tax</a>) after the circular math. The <strong>solo 401(k)</strong> stacks two layers: an <strong>employee deferral</strong> — up to $23,500 in 2025, up to 100% of earnings — <em>plus</em> the same ~20% employer share, capped at $70,000 combined. At $50,000 of profit, that's roughly $9,200 (SEP) versus $32,700 (solo 401k) of deductible space. The deferral layer is the whole story at low and middle profits.</p>
<h2>Where each one wins</h2>
<ul>
<li><strong>Side hustlers and profits under ~$100k: solo 401(k), decisively.</strong> The deferral shelters the first dollars at 100%, so a $20,000 side profit can stash ~$18,000+ — the SEP manages ~$3,700. One caveat for moonlighters: the deferral limit is <em>shared across all your 401(k)s</em>, so if a W-2 day job already eats the $23,500, your solo plan is left with just the employer share (still matching the SEP) — enter your W-2 deferrals above and the calculator handles it.</li>
<li><strong>Profits above ~$350k: a tie on dollars.</strong> Both hit the $70,000 cap; the solo 401(k) still adds the age-50+ catch-up ($7,500, or $11,250 at ages 60-63) that SEPs simply don't have.</li>
<li><strong>Simplicity and flexibility: SEP.</strong> Opens in minutes at any brokerage, no annual filing ever, and — uniquely — can be opened and funded <em>after year-end</em>, up to your tax-filing deadline including extensions. A one-time windfall year discovered at tax time is the SEP's home turf.</li>
<li><strong>Features: solo 401(k).</strong> Roth deferrals (build tax-free money in fat years — weigh with the <a href="/calculators/roth-vs-traditional-401k-calculator/">Roth vs traditional calculator</a>), participant loans up to $50,000, and a big backdoor-Roth advantage: SEP balances are pre-tax IRA money that poisons the pro-rata calculation, while solo 401(k) balances don't count against it. High earners planning backdoor Roths should avoid carrying SEP balances at all.</li>
</ul>
<h2>The fine print that catches people</h2>
<ul>
<li><strong>Deadlines differ by layer.</strong> The solo 401(k) <em>plan</em> should exist by December 31 for full flexibility (SECURE 2.0 allows late setup for the employer share, and sole proprietors get until the filing deadline for the prior year's <em>first-year</em> deferral). Deferral elections are best made in the calendar year; employer shares can wait until filing. The SEP forgives all procrastination.</li>
<li><strong>Form 5500-EZ at $250k.</strong> Once solo 401(k) assets pass $250,000, a short annual form is due — trivial, but the penalty for forgetting is vicious ($250/day). SEPs never file.</li>
<li><strong>Employees change everything.</strong> Hire anyone eligible and the SEP must contribute the same percentage for them as for you; the solo 401(k) stops being 'solo' entirely. Both remain workable with a spouse on payroll — a legitimate way to double the household's sheltered space.</li>
<li><strong>The employer share needs profit.</strong> Both employer contributions are capped by the ~20% math — at low profit, the SEP's entire value proposition shrinks while the solo 401(k)'s deferral keeps working.</li>
</ul>
<h2>Sequencing it with the rest of the plan</h2>
<p>These accounts sit inside the bigger self-employment money loop: price your work so tax and retirement are funded (<a href="/calculators/freelance-hourly-rate-calculator/">freelance rate calculator</a>), skim for <a href="/calculators/quarterly-estimated-tax-calculator/">quarterly taxes</a> as revenue arrives, then fill retirement space in rough order — HSA if eligible (<a href="/calculators/hsa-calculator/">the triple advantage</a>), Roth IRA if under the income limits, then the solo 401(k)/SEP as profit allows. Every dollar contributed pre-tax also cuts this year's income tax at your marginal rate (check it against the <a href="/calculators/tax-bracket-calculator/">brackets</a>) — though not SE tax, which applies to profit before these deductions. Project what the sheltered money becomes with the <a href="/calculators/retirement-savings-calculator/">retirement savings calculator</a>.</p>
""",
        "faqs": [
            ("Can I have both a SEP IRA and a solo 401(k)?", "Technically yes, but generally pointless — contributions share the same employer-side limits, so you can't double-dip meaningfully (and using the IRS model SEP form alongside a 401(k) is prohibited). Pick one. The common migration is SEP → solo 401(k) as the backdoor-Roth or deferral advantages start to matter; you can roll the SEP balance into the solo 401(k) to clean up the pro-rata problem."),
            ("Can I contribute to a solo 401(k) if I also have a 401(k) at my day job?", "Yes — and it's one of the best moonlighter moves. The $23,500 employee deferral is shared across all plans, so whatever the day job used is gone, but the ~20%-of-net-earnings employer contribution from your side business stacks on top with its own $70,000 overall cap per unrelated employer. A maxed W-2 employee with $60k of side profit can still shelter ~$11,000 through the solo plan's employer share."),
            ("How much can I put in a SEP IRA with $100,000 of self-employment profit?", "About $18,600: the rule is 25% of compensation, but for sole proprietors compensation is profit minus half your SE tax minus the contribution itself — which collapses to roughly 20% of net earnings (~$92,900 here). The same $100,000 in a solo 401(k) supports about $42,100: $23,500 deferral plus the same ~$18,600 employer share."),
            ("Is the SEP or solo 401(k) contribution deadline more forgiving?", "The SEP wins on procrastination: it can be both opened and funded after year-end, up to your filing deadline including extensions — a discovery-at-tax-time option. Solo 401(k) employee deferrals really want the plan established and elections made by December 31 (with a first-year exception for sole proprietors under SECURE 2.0); the employer share can wait until filing like the SEP's."),
            ("Do these contributions reduce self-employment tax?", "No — SE tax is computed on net profit before retirement contributions, so the 15.3% applies regardless. What they cut is income tax: a $30,000 solo 401(k) contribution at a 24% marginal rate defers $7,200 of federal income tax. The only retirement-adjacent items that touch SE tax are business expense deductions that lower profit itself."),
        ],
    },
]
