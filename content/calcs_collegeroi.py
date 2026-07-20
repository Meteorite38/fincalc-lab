# -*- coding: utf-8 -*-
"""College/degree ROI — total cost incl. foregone earnings vs lifetime wage premium, breakeven age, loan-burden check."""

COLLEGEROI = [
    {
        "slug": "college-roi-calculator",
        "emoji": "\U0001F9E0",
        "category": "Everyday Math",
        "title": "College ROI Calculator — Is the Degree Worth the Price?",
        "h1": "College ROI Calculator",
        "blurb": "Degree cost plus foregone wages vs the earnings premium — breakeven age and lifetime value.",
        "meta_description": "Free college ROI calculator: total degree cost including foregone earnings vs the wage premium over a no-degree path — net lifetime value, the age the investment breaks even, and the debt-to-first-salary sanity check.",
        "intro": "A degree is an investment with a price (tuition plus the wages you don't earn while studying) and a return (the earnings premium over the path you'd take instead). For many degrees that return is spectacular; for some price-program combinations it never breaks even. This calculator runs your actual numbers instead of the averages.",
        "fields": [
            {"id": "tuition", "label": "All-in cost per year ($)", "value": 24000, "hint": "tuition + fees + room/board beyond what living anyway costs"},
            {"id": "years", "label": "Years to complete", "value": 4, "step": 1},
            {"id": "aid", "label": "Grants & scholarships per year ($)", "value": 6000, "hint": "free money only — not loans"},
            {"id": "nodegree", "label": "Salary without the degree ($/yr)", "value": 38000, "hint": "what you'd realistically earn instead"},
            {"id": "withdegree", "label": "Starting salary with the degree ($/yr)", "value": 62000, "hint": "realistic for the major — not the university brochure"},
            {"id": "growTo", "label": "Both paths' salary growth (%/yr)", "value": 3, "step": 0.1},
            {"id": "premiumgrow", "label": "Extra growth on the degree path (%/yr)", "value": 1, "step": 0.1, "hint": "degrees often raise the ceiling, not just the floor"},
            {"id": "loans", "label": "Student loans at graduation ($)", "value": 40000},
            {"id": "loanrate", "label": "Loan rate (%)", "value": 6.5, "step": 0.05},
        ],
        "js": """
function calculate() {
  const T = val('tuition'), yrs = Math.min(15, Math.max(1, Math.round(val('years')))), aid = Math.max(0, val('aid'));
  const s0 = val('nodegree'), s1 = val('withdegree');
  const g = val('growTo')/100, pg = Math.max(0, val('premiumgrow'))/100;
  const L = Math.max(0, val('loans')), lr = val('loanrate')/100/12;
  if (s0 < 0 || s1 <= 0) { show('<div class="result-main">Enter both salaries.</div>'); return; }
  const direct = (T - aid) * yrs;
  const foregone = (() => { let f = 0, s = s0; for (let y = 0; y < yrs; y++) { f += s; s *= (1 + g); } return f; })();
  const totalCost = direct + foregone;
  // loan interest over a 10-year standard payoff
  const n = 120;
  const pay = lr > 0 ? L * lr / (1 - Math.pow(1 + lr, -n)) : L / n;
  const loanInterest = L > 0 ? pay * n - L : 0;
  // simulate to age ~65: assume start at 18, degree path starts earning at 18+yrs
  const horizon = 47; // 18 -> 65
  let cumNo = 0, cumDeg = -direct - loanInterest, sNo = s0, sDeg = s1;
  let breakevenYear = -1;
  for (let y = 0; y < horizon; y++) {
    cumNo += sNo; sNo *= (1 + g);
    if (y >= yrs) { cumDeg += sDeg; sDeg *= (1 + g + pg); }
    if (breakevenYear < 0 && cumDeg >= cumNo) breakevenYear = y + 1;
  }
  const lifetime = cumDeg - cumNo;
  const ratio = s1 > 0 ? L / s1 : 0;
  const ratioNote = L === 0 ? 'debt-free — the strongest version of this plan'
    : (ratio <= 1 ? `${fmt(ratio*100,0)}% of first-year salary — inside the classic borrow-less-than-year-one rule`
    : `<strong>${fmt(ratio,1)}× first-year salary — beyond the borrow-under-1× guideline; this is where degrees stop paying</strong>`);
  show(`<div class="result-main">${lifetime > 0 ? '$' + fmt(lifetime,0) + ' lifetime edge' : '$' + fmt(-lifetime,0) + ' lifetime LOSS'}<small>degree path vs working path through age 65 &middot; ${breakevenYear > 0 ? 'breaks even around age ' + (18 + breakevenYear) : '<strong>never breaks even</strong> on these numbers'}</small></div>
  <table>
    <tr><td>Direct cost (${yrs} yrs × $${fmt(T - aid,0)} net of aid)</td><td>$${fmt(direct,0)}</td></tr>
    <tr><td>Foregone earnings while studying</td><td>$${fmt(foregone,0)} — the cost nobody prices</td></tr>
    <tr><td><strong>True investment</strong></td><td><strong>$${fmt(totalCost,0)}</strong></td></tr>
    <tr><td>Loan interest (10-yr payoff of $${fmt(L,0)})</td><td>$${fmt(loanInterest,0)}</td></tr>
    <tr><td>Year-1 premium</td><td>$${fmt(s1 - s0*Math.pow(1+g,yrs),0)}/yr, growing</td></tr>
    <tr><td>Debt vs first salary</td><td>${ratioNote}</td></tr>
    <tr><td>Cumulative advantage by 65</td><td>${lifetime > 0 ? '$' + fmt(lifetime,0) : '&minus;$' + fmt(-lifetime,0)}</td></tr>
  </table>
  <p>${lifetime > 0 && breakevenYear > 0 && (18 + breakevenYear) <= 35
    ? `Strong investment: the degree repays its full cost (including the invisible foregone wages) by ${18 + breakevenYear} and compounds from there.`
    : (lifetime > 0
      ? `It pays eventually — but a breakeven at ${18 + breakevenYear} leaves little margin for a wrong major, a fifth year, or a soft job market. Cheaper versions of the same credential (below) move this number fast.`
      : `On these numbers the working path wins outright. Before abandoning the degree idea, rerun with a cheaper route — community-college transfer, in-state tuition, more aid — which often flips the verdict without changing the credential.`)}</p>`);
}
""",
        "body_html": """
<h2>The cost side people undercount — and the return side they overcount</h2>
<p>The sticker price is the smaller half of the investment. Four years <em>not</em> earning a $38,000 salary is roughly $160,000 of foregone wages — usually more than net tuition at a public university. That's why this calculator counts both, and why finishing in four years instead of six is worth more than most scholarships (each extra year adds a year of cost <em>and</em> a year of missing pay). On the return side, the honest comparison is your realistic salary <em>for that major in that job market</em>, not the university's marketing average — engineering and nursing premiums are enormous; some majors' premiums are modest and arrive slowly. The degree also often changes the <em>slope</em>, not just the starting point — promotions, credential-gated roles, graduate options — which is what the \"extra growth\" input captures. Both effects are real; both deserve real numbers instead of vibes.</p>
<h2>The one-line debt rule</h2>
<p>Decades of outcomes compress into one guideline: <strong>total borrowing under your realistic first-year salary</strong>. At 1× or below, a standard 10-year payoff takes roughly 10% of gross — tight but livable. At 2×+, the payment crowds out saving, housing and risk-taking through the exact decade when <a href="/articles/how-to-build-wealth-in-your-20s-and-30s/">compounding matters most</a>. The rule also converts neatly into strategy: it says <em>which version</em> of a credential to buy. The $25,000-debt path to a nursing degree and the $120,000-debt path lead to the same license — the <a href="/calculators/student-loan-calculator/">loan payoff calculator</a> shows what each costs monthly, and the difference is a house down payment.</p>
<h2>Moving the ROI without changing the diploma</h2>
<ul>
<li><strong>Community college transfer:</strong> two years at ~$4,000 rolling into the state flagship's diploma — same final credential, roughly half the direct cost. The single biggest ROI lever available.</li>
<li><strong>In-state public vs private sticker:</strong> the median private premium rarely survives this calculator unless heavy aid closes the gap. Always compare <em>net</em> price after the aid letter, not sticker vs sticker.</li>
<li><strong>Finish on time.</strong> Six-year graduation is the silent ROI killer — a fifth year costs tuition plus a year of degree-level wages, easily $80,000+ of swing.</li>
<li><strong>AP/dual-enrollment credits, CLEP, summer courses</strong> shave semesters at trivial cost.</li>
<li><strong>Aid is negotiable:</strong> competing offers can be sent back to the preferred school's aid office; appeals succeed often enough to be worth an afternoon. Grants and scholarships change the math dollar-for-dollar (the <a href="/calculators/college-savings-calculator/">college savings calculator</a> handles the family-funding side).</li>
</ul>
<h2>When the working path honestly wins</h2>
<p>The comparison isn't degree vs nothing — it's degree vs <em>the best version of not-degree</em>: skilled trades (electricians and linemen out-earn many bachelor's holders, with paid apprenticeships instead of tuition), certifications and licensure programs measured in months, sales roles where output beats credentials, and military or employer-tuition routes that pay for later education. For a student lukewarm on academics staring at a 2×-salary debt load for a modest-premium major, the trades path frequently wins this calculator outright — earlier earnings, zero debt, and a decade's head start on <a href="/calculators/compound-interest-calculator/">compounding</a>. The credential question deserves the same discipline as any five-figure investment: run the numbers, compare the alternatives, and buy the cheapest version of the outcome you actually want.</p>
""",
        "faqs": [
            ("Is college still worth it financially?", "On average, strongly yes — the median bachelor's holder out-earns the median high-school path by roughly $1M+ over a career. But averages hide the distribution: the verdict depends on the major's realistic salary, the price paid, debt taken, and finishing on time. High-premium majors at in-state prices are among the best investments available; low-premium majors at private-sticker prices with 2× debt can genuinely never break even. That's why running your specific numbers beats quoting the average."),
            ("How much student debt is too much?", "The working rule: keep total borrowing under your realistic first-year salary — $60k expected salary, borrow under $60k. That keeps a standard 10-year payment near 10% of gross income. Past 1.5-2×, the payment starts dictating life choices (housing, saving, career risk) for a decade-plus, and income-driven plans that stretch the term multiply the interest."),
            ("Does the calculator account for the college experience, networking, or non-money value?", "No — deliberately. Those benefits are real but personal; pricing them is your call, not a formula's. What the calculator prevents is paying $150,000 for benefits you assumed were financial when they weren't. If the numbers say the degree loses $200k and you still want it, that's a legitimate values choice — made with open eyes, which is the whole point."),
            ("Is graduate school worth it?", "Same machine, sharper inputs: cost plus 2-6 years of foregone professional salary (much bigger than an 18-year-old's) versus the premium the credential actually gates. Professional degrees with licensure moats (medicine, law at strong schools, MBA into consulting/finance) often clear the bar; PhDs and master's degrees in fields that don't require them frequently don't. Employer tuition funding flips marginal cases to yes."),
            ("What about starting at community college?", "It's the highest-ROI move in the system for most students: two years at community-college prices, transfer, graduate with the four-year school's diploma — indistinguishable to employers — at roughly half the direct cost. The execution details that matter: confirmed articulation agreements (courses that actually transfer) and staying on the transfer timeline so the total stays at four years."),
        ],
    },
]
