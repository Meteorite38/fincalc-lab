# -*- coding: utf-8 -*-
"""Batch 7 calculators: amortization schedule, debt consolidation, home equity (HELOC),
savings rate, EBITDA, rent increase."""

PART9 = [
    {
        "slug": "amortization-schedule-calculator",
        "emoji": "\U0001F4C5",
        "category": "Mortgages & Home",
        "title": "Amortization Schedule Calculator — Year-by-Year Loan Breakdown",
        "h1": "Amortization Schedule Calculator",
        "blurb": "Yearly principal vs interest breakdown of any loan.",
        "meta_description": "Generate a year-by-year amortization schedule for any loan or mortgage: see how each year's payments split between principal and interest, and the falling balance.",
        "intro": "An amortization schedule shows exactly how a loan is paid off over time — how much of each year goes to interest versus principal, and how the balance falls. Enter your loan details for a full yearly breakdown.",
        "fields": [
            {"id": "amount", "label": "Loan amount ($)", "value": 300000},
            {"id": "rate", "label": "Annual interest rate (%)", "value": 6.5, "step": 0.05},
            {"id": "years", "label": "Loan term (years)", "value": 30, "step": 1},
        ],
        "js": """
function calculate() {
  const P = val('amount'), i = val('rate')/100/12;
  const n = Math.min(Math.round(val('years')*12), 1200);  // cap at 100 years to stay safe
  if (P <= 0 || n <= 0) { show('<div class="result-main">Enter a loan amount and term above zero.</div>'); return; }
  if (val('years') > 100) { show('<div class="result-main">Please enter a term of 100 years or less.</div>'); return; }
  const pmt = i>0 ? P*i/(1-Math.pow(1+i,-n)) : P/n;
  let bal = P, rows = '', yearInt = 0, yearPrin = 0, totalInt = 0;
  const yearsN = Math.ceil(n/12);
  let table = `<table><tr><td><strong>Year</strong></td><td><strong>Principal</strong></td><td><strong>Interest</strong></td><td><strong>Balance</strong></td></tr>`;
  for (let m = 1; m <= n; m++) {
    const int = bal * i; const prin = pmt - int;
    bal -= prin; yearInt += int; yearPrin += prin; totalInt += int;
    if (m % 12 === 0 || m === n) {
      table += `<tr><td>${Math.ceil(m/12)}</td><td>$${fmt(yearPrin,0)}</td><td>$${fmt(yearInt,0)}</td><td>$${fmt(Math.max(bal,0),0)}</td></tr>`;
      yearInt = 0; yearPrin = 0;
    }
  }
  table += `</table>`;
  show(`<div class="result-main">$${fmt(pmt)} / month<small>Total interest over ${val('years')} years: $${fmt(totalInt,0)}</small></div>${table}`);
}
""",
        "body_html": """
<h2>What amortization actually means</h2>
<p>To amortize a loan is to pay it off through regular equal payments, each split between interest on the remaining balance and repayment of the principal. Early on, the balance is large, so most of your payment is interest and little touches the principal. As the balance shrinks, the split flips — later payments are almost all principal. The schedule above makes this shift visible year by year.</p>
<h2>The front-loaded interest surprise</h2>
<p>On a $300,000 mortgage at 6.5% over 30 years, look at the first year versus the last. In year one, roughly $19,000 of your ~$22,750 in payments goes to interest and only ~$3,400 reduces the balance. By the final year it's the reverse. This is why paying a 30-year mortgage for five years barely dents the balance — and why refinancing resets you to the interest-heavy start of a fresh schedule.</p>
<h2>How to use the schedule</h2>
<ul>
<li><strong>See your equity build.</strong> The balance column shows what you still owe; subtract it from the property value to track home equity over time.</li>
<li><strong>Understand extra payments.</strong> Any extra principal payment permanently removes the interest on that amount for the rest of the schedule — try our <a href="/calculators/extra-mortgage-payment-calculator/">extra payment calculator</a> to see the effect.</li>
<li><strong>Compare loans honestly.</strong> Two loans with the same payment can have very different total interest depending on term and rate — the schedule totals reveal the real cost.</li>
</ul>
<h2>Beyond mortgages</h2>
<p>The same math governs car loans, student loans, and personal loans. Any fixed-rate, fixed-term loan follows an amortization schedule — knowing how to read one turns an opaque monthly bill into a transparent plan you can see the end of.</p>
""",
        "faqs": [
            ("What is an amortization schedule?", "A table showing how each loan payment over time is divided between interest and principal, and how the remaining balance declines. It reveals that early payments are mostly interest and later ones mostly principal."),
            ("Why is so much of my early payment interest?", "Because interest is charged on the outstanding balance, which is largest at the start. As you pay down the principal, the interest portion of each payment shrinks and the principal portion grows."),
            ("Does refinancing restart amortization?", "Yes. A new loan begins a fresh schedule at the interest-heavy start, which is why refinancing late in a loan's life can increase total interest even at a lower rate unless you also shorten the term."),
        ],
    },
    {
        "slug": "debt-consolidation-calculator",
        "emoji": "\U0001F9EE",
        "category": "Debt & Credit",
        "title": "Debt Consolidation Calculator — Compare Combining Your Debts",
        "h1": "Debt Consolidation Calculator",
        "blurb": "See if one consolidated loan beats your current debts.",
        "meta_description": "Compare your current debts against a single consolidation loan: new monthly payment, total interest, and whether consolidating actually saves you money.",
        "intro": "Consolidating several debts into one loan can lower your payment and simplify life — but only if the numbers work. Enter your current debt and a consolidation offer to compare honestly.",
        "fields": [
            {"id": "balance", "label": "Total current debt balance ($)", "value": 25000},
            {"id": "currentpmt", "label": "Current total monthly payment ($)", "value": 850},
            {"id": "avgrate", "label": "Current average interest rate (%)", "value": 19, "step": 0.1},
            {"id": "newrate", "label": "Consolidation loan rate (%)", "value": 11, "step": 0.1},
            {"id": "newterm", "label": "Consolidation term (years)", "value": 4, "step": 1},
            {"id": "fee", "label": "Consolidation fee ($, optional)", "value": 0},
        ],
        "js": """
function payoffMonths(P, i, pmt) {
  if (pmt <= P*i) return null;
  let bal = P, m = 0, interest = 0;
  while (bal > 0 && m < 1200) { const int = bal*i; interest += int; bal = bal + int - pmt; m++; }
  return { months: m, interest };
}
function calculate() {
  const P = val('balance'), curPmt = val('currentpmt'), curI = val('avgrate')/100/12;
  const newI = val('newrate')/100/12, n = Math.round(val('newterm')*12), fee = val('fee');
  const cur = payoffMonths(P, curI, curPmt);
  const newLoan = P + fee;
  const newPmt = newI>0 ? newLoan*newI/(1-Math.pow(1+newI,-n)) : newLoan/n;
  const newInterest = newPmt*n - newLoan + fee;
  if (!cur) { show('<div class="result-main">Your current payment barely covers interest — almost any consolidation helps. Enter a realistic current payment.</div>'); return; }
  const saving = cur.interest - newInterest;
  show(`<div class="result-main">${saving>=0 ? '$'+fmt(saving,0)+' saved' : '$'+fmt(-saving,0)+' more'}<small>in total interest by consolidating${saving>=0 ? '' : ' — costs more overall'}</small></div>
  <table>
    <tr><td>New monthly payment</td><td>$${fmt(newPmt)} (was $${fmt(curPmt,0)})</td></tr>
    <tr><td>Current payoff / interest</td><td>${(cur.months/12).toFixed(1)} yrs, $${fmt(cur.interest,0)}</td></tr>
    <tr><td>Consolidated payoff / interest</td><td>${(n/12).toFixed(1)} yrs, $${fmt(newInterest,0)}</td></tr>
    <tr><td>Monthly cash-flow change</td><td>${newPmt<=curPmt ? '$'+fmt(curPmt-newPmt,0)+' freed up' : '$'+fmt(newPmt-curPmt,0)+' more'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What consolidation really does</h2>
<p>Debt consolidation replaces several debts — often high-rate credit cards — with a single new loan, ideally at a lower rate. The appeal is real: one payment instead of many, a lower interest rate, and often a lower monthly payment. But two traps hide in the details, and this calculator exposes both: the <strong>term</strong> and the <strong>fee</strong>.</p>
<h2>The lower-payment illusion</h2>
<p>A consolidation loan often lowers your monthly payment mainly by <em>stretching the term</em>. A lower rate spread over more years can still cost more total interest than your current debts would. Always compare total interest, not just the monthly payment — a smaller payment for twice as long is frequently a worse deal dressed up as relief. The calculator shows both numbers side by side so you can't be fooled.</p>
<h2>When consolidation genuinely wins</h2>
<ul>
<li><strong>The rate drop is large</strong> (e.g. from 19% cards to an 11% personal loan) and the term isn't dramatically longer.</li>
<li><strong>Fees are modest.</strong> Balance-transfer or origination fees (often 3–5%) eat into savings — the calculator lets you include them.</li>
<li><strong>You stop adding new debt.</strong> Consolidation only works if you don't run the cards back up. Otherwise you end up with the loan <em>and</em> new card balances — the most common way consolidation backfires.</li>
</ul>
<h2>Alternatives to weigh</h2>
<p>Before consolidating, compare a <a href="/calculators/debt-snowball-vs-avalanche-calculator/">structured payoff plan</a> (avalanche/snowball) on your existing debts, and a 0% balance-transfer card if you can clear the balance within the promo window. Consolidation is a tool, not a cure — the behavior that created the debt matters more than the loan that refinances it.</p>
""",
        "faqs": [
            ("Does debt consolidation save money?", "Only if the new loan's total interest is lower than your current debts' — which requires a meaningfully lower rate without a much longer term. A lower monthly payment alone can still mean paying more overall."),
            ("Why might consolidation cost more?", "Because it often lowers the payment by extending the term. A lower rate over more years can produce more total interest, and origination or balance-transfer fees add to the cost."),
            ("Is consolidation a good idea?", "It can be, when the rate drop is large, fees are small, and you stop taking on new debt. If you keep using the paid-off cards, you'll end up worse off — behavior matters more than the loan."),
        ],
    },
    {
        "slug": "home-equity-calculator",
        "emoji": "\U0001F3E6",
        "category": "Mortgages & Home",
        "title": "Home Equity Calculator — How Much You Can Borrow (HELOC)",
        "h1": "Home Equity Calculator",
        "blurb": "Your home equity and borrowable amount at a target LTV.",
        "meta_description": "Calculate your home equity and how much you could borrow with a home equity loan or HELOC, based on your home value, mortgage balance and the lender's loan-to-value limit.",
        "intro": "Home equity is the part of your home you truly own. Enter your home's value, your mortgage balance, and a lender loan-to-value limit to see your equity and how much you could potentially borrow.",
        "fields": [
            {"id": "value", "label": "Current home value ($)", "value": 450000},
            {"id": "mortgage", "label": "Mortgage balance owed ($)", "value": 260000},
            {"id": "ltv", "label": "Lender max loan-to-value (%)", "value": 85, "step": 1, "hint": "commonly 80-90%"},
        ],
        "js": """
function calculate() {
  const v = val('value'), m = val('mortgage'), ltv = val('ltv')/100;
  if (v <= 0) { show('<div class="result-main">Enter a home value above zero.</div>'); return; }
  const equity = v - m;
  const equityPct = equity / v * 100;
  const maxBorrowTotal = v * ltv;
  const available = Math.max(0, maxBorrowTotal - m);
  show(`<div class="result-main">$${fmt(available,0)}<small>Estimated borrowable equity at ${val('ltv')}% LTV</small></div>
  <table>
    <tr><td>Your home equity</td><td>$${fmt(equity,0)} (${fmt(equityPct,0)}% of value)</td></tr>
    <tr><td>Max total debt at ${val('ltv')}% LTV</td><td>$${fmt(maxBorrowTotal,0)}</td></tr>
    <tr><td>Less current mortgage</td><td>\\u2212$${fmt(m,0)}</td></tr>
    <tr><td>Available to borrow</td><td>$${fmt(available,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Equity vs borrowable equity</h2>
<p>Your <strong>home equity</strong> is simply your home's value minus what you owe: a $450,000 home with a $260,000 mortgage means $190,000 of equity. But lenders won't let you borrow all of it. They cap your <em>combined</em> borrowing at a loan-to-value (LTV) limit — often 80–90% of the home's value. Borrowable equity is that ceiling minus your existing mortgage, which is usually less than your raw equity.</p>
<h2>The LTV math</h2>
<p>At an 85% LTV limit on a $450,000 home, total allowed debt is $382,500. Subtract the $260,000 mortgage and about <strong>$122,500</strong> is available through a home equity loan or line of credit (HELOC) — not the full $190,000 of equity. The lower the LTV limit (the more conservative the lender), the less you can tap. Lenders keep this cushion so they're protected if home prices fall.</p>
<h2>Home equity loan vs HELOC</h2>
<ul>
<li><strong>Home equity loan:</strong> a lump sum at a fixed rate, repaid over a set term — predictable, good for one-time costs.</li>
<li><strong>HELOC:</strong> a revolving credit line you draw from as needed, usually variable-rate — flexible, but payments and rates can rise.</li>
</ul>
<h2>Borrow against your home carefully</h2>
<p>Because these loans are secured by your house, the rates are lower than credit cards — but the stakes are far higher: default can mean foreclosure. Sensible uses include value-adding home improvements or consolidating higher-rate debt at a lower secured rate. Risky uses include funding lifestyle spending or depreciating purchases. You're converting hard-won equity back into debt, so the reason had better be worth putting your home on the line.</p>
""",
        "faqs": [
            ("How much home equity can I borrow?", "Typically your home's value times the lender's LTV limit (often 80–90%), minus your current mortgage balance. That's usually less than your total equity, because lenders keep a cushion."),
            ("What's the difference between a home equity loan and a HELOC?", "A home equity loan gives a fixed lump sum at a fixed rate; a HELOC is a revolving, usually variable-rate credit line you draw from as needed. Loans suit one-time costs; HELOCs suit ongoing or uncertain needs."),
            ("Is borrowing against home equity safe?", "It offers lower rates than unsecured debt, but the loan is secured by your home, so defaulting risks foreclosure. Use it for value-adding or rate-lowering purposes, not lifestyle spending."),
        ],
    },
    {
        "slug": "savings-rate-calculator",
        "emoji": "\U0001F4B9",
        "category": "Savings & Investing",
        "title": "Savings Rate Calculator — What Percentage of Income You Save",
        "h1": "Savings Rate Calculator",
        "blurb": "Your savings rate and what it means for freedom.",
        "meta_description": "Calculate your savings rate — the percentage of income you save — and see roughly how many years until financial independence, the number that matters most.",
        "intro": "Your savings rate — the share of take-home pay you keep — is the single strongest predictor of how fast you build wealth. Enter your income and savings to find yours and what it implies.",
        "fields": [
            {"id": "income", "label": "Monthly take-home income ($)", "value": 5000},
            {"id": "saved", "label": "Monthly amount saved/invested ($)", "value": 1250},
        ],
        "js": """
function calculate() {
  const inc = val('income'), saved = val('saved');
  if (inc <= 0) { show('<div class="result-main">Enter income above zero.</div>'); return; }
  const rate = saved / inc * 100;
  // rough years-to-FI assuming 5% real return, 4% withdrawal, starting from zero
  const r = 0.05, wr = 0.04, sr = Math.min(Math.max(saved/inc, 0.0001), 0.999);
  const spend = 1 - sr;
  const target = spend / wr;  // in units of annual income
  let bal = 0, yrs = 0;
  while (bal < target && yrs < 200) { bal = bal*(1+r) + sr; yrs++; }
  let band;
  if (rate >= 50) band = 'Exceptional — on a fast track to financial independence';
  else if (rate >= 20) band = 'Strong — comfortably ahead of most households';
  else if (rate >= 10) band = 'Solid start — a common recommended minimum';
  else if (rate > 0) band = 'Below target — worth pushing higher when you can';
  else band = 'Not saving yet — the first goal is to get above zero';
  show(`<div class="result-main">${fmt(rate,1)}%<small>of your take-home pay is being saved</small></div>
  <table>
    <tr><td>Saved per year</td><td>$${fmt(saved*12,0)}</td></tr>
    <tr><td>Spent per year</td><td>$${fmt((inc-saved)*12,0)}</td></tr>
    <tr><td>Rough years to financial independence</td><td>${yrs>=200 ? 'raise the rate to make progress' : '≈ '+yrs+' years'}</td></tr>
    <tr><td>Assessment</td><td>${band}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why savings rate rules everything</h2>
<p>Most people obsess over investment returns and ignore the variable they fully control: their savings rate. Yet the percentage of income you save is the dominant factor in how quickly you reach financial independence — far more than your salary or a percentage point of return. The reason is elegant: a higher savings rate simultaneously lowers the expenses you'll need to fund <em>and</em> raises the pile funding them.</p>
<h2>The math that surprises people</h2>
<p>Starting from zero, at a 5% real return, the approximate time to financial independence is set almost entirely by savings rate:</p>
<ul>
<li><strong>10% saved</strong> → roughly 50 years</li>
<li><strong>20% saved</strong> → roughly 32 years</li>
<li><strong>50% saved</strong> → roughly 17 years</li>
<li><strong>65% saved</strong> → roughly 10 years</li>
</ul>
<p>Income barely appears in this relationship. A modest earner saving 50% reaches independence decades before a high earner saving 10% — because the high earner's lifestyle costs so much to sustain. This is the core insight behind the <a href="/articles/fire-movement-explained/">FIRE movement</a>.</p>
<h2>How to compute yours honestly</h2>
<p>Savings rate = amount saved ÷ take-home income. Count all real saving: retirement contributions, investments, extra debt principal, and cash added to savings. Be honest about "saving" that's really just a checking-account balance you'll spend next month. Many people are surprised their true rate is lower than they assumed — which is exactly why measuring it is the first step to improving it.</p>
<h2>Moving the number</h2>
<p>Because it's a ratio, you can raise your savings rate from both sides: earn more (and avoid lifestyle inflation) or spend less. The biggest levers are usually the big three — housing, transport, and food — not small indulgences. Even a 5-percentage-point increase, sustained, pulls your independence date forward by years. Pair this with the <a href="/calculators/budget-calculator/">50/30/20 budget</a> to find the room.</p>
""",
        "faqs": [
            ("What is a good savings rate?", "10% is a common minimum, 20% is strong, and 50%+ puts you on a fast track to financial independence. The right target depends on your goals, but higher is almost always better — and the number matters more than your income."),
            ("Why does savings rate matter more than income?", "Because it sets both how much you need (by defining your spending) and how fast you accumulate it. A high earner who spends most of it can retire later than a modest earner who saves half."),
            ("What counts toward my savings rate?", "All genuine saving: retirement contributions, investments, extra debt principal payments, and cash truly set aside. Money that sits in checking to be spent next month doesn't count."),
        ],
    },
    {
        "slug": "ebitda-calculator",
        "emoji": "\U0001F4D0",
        "category": "Business",
        "title": "EBITDA Calculator — Operating Profitability at a Glance",
        "h1": "EBITDA Calculator",
        "blurb": "EBITDA and margin from your income statement.",
        "meta_description": "Calculate EBITDA (earnings before interest, taxes, depreciation and amortization) and EBITDA margin from your financials — a standard measure of operating profitability.",
        "intro": "EBITDA strips out financing, tax and accounting effects to show a business's core operating profitability. Enter your figures to get EBITDA and the margin used in valuations and comparisons.",
        "fields": [
            {"id": "revenue", "label": "Revenue ($)", "value": 2000000},
            {"id": "netincome", "label": "Net income ($)", "value": 180000},
            {"id": "interest", "label": "Interest expense ($)", "value": 60000},
            {"id": "taxes", "label": "Taxes ($)", "value": 70000},
            {"id": "da", "label": "Depreciation & amortization ($)", "value": 120000},
        ],
        "js": """
function calculate() {
  const rev = val('revenue'), ni = val('netincome'), i = val('interest'), t = val('taxes'), da = val('da');
  const ebit = ni + i + t;
  const ebitda = ebit + da;
  const margin = rev>0 ? ebitda/rev*100 : 0;
  show(`<div class="result-main">$${fmt(ebitda,0)}<small>EBITDA &mdash; ${fmt(margin,1)}% EBITDA margin</small></div>
  <table>
    <tr><td>Net income</td><td>$${fmt(ni,0)}</td></tr>
    <tr><td>+ Interest</td><td>$${fmt(i,0)}</td></tr>
    <tr><td>+ Taxes</td><td>$${fmt(t,0)}</td></tr>
    <tr><td>= EBIT (operating profit)</td><td>$${fmt(ebit,0)}</td></tr>
    <tr><td>+ Depreciation &amp; amortization</td><td>$${fmt(da,0)}</td></tr>
    <tr><td>= EBITDA</td><td>$${fmt(ebitda,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What EBITDA measures</h2>
<p>EBITDA — Earnings Before Interest, Taxes, Depreciation and Amortization — tries to show how profitable a company's core operations are, before the effects of how it's financed (interest), where it's taxed (taxes), and non-cash accounting charges (depreciation and amortization). You build it up from net income by adding those four items back: <code>EBITDA = Net income + Interest + Taxes + D&A</code>.</p>
<h2>Why analysts love it (and why to be careful)</h2>
<p>Because it removes financing and tax differences, EBITDA lets you compare the operating performance of companies with different debt levels, tax situations, or asset bases — which is why it's central to valuations (businesses are often priced as a multiple of EBITDA) and lending covenants. The <strong>EBITDA margin</strong> (EBITDA ÷ revenue) shows operating profitability as a percentage, useful for tracking trends and comparing peers.</p>
<h2>The famous criticism</h2>
<p>Warren Buffett and Charlie Munger have derided EBITDA because it ignores two very real costs. Depreciation reflects that assets wear out and must eventually be replaced — pretending that isn't a cost ("earnings before the bad stuff," critics quip) can flatter capital-intensive businesses. And ignoring interest hides the burden of real debt that must be serviced. EBITDA is a useful lens, not a measure of actual cash you can spend.</p>
<h2>Use it alongside other numbers</h2>
<ul>
<li><strong>Compare with net income and free cash flow</strong> to see what EBITDA leaves out — a company with high EBITDA but weak cash flow deserves scrutiny.</li>
<li><strong>Watch the margin trend</strong> over time; a rising EBITDA margin signals improving operating efficiency.</li>
<li><strong>Mind capital intensity.</strong> For asset-heavy businesses, the excluded depreciation is a genuine ongoing cost, so EBITDA overstates sustainable profit more than it does for asset-light firms.</li>
</ul>
""",
        "faqs": [
            ("How is EBITDA calculated?", "Start with net income and add back interest, taxes, and depreciation & amortization. Equivalently, EBITDA = operating profit (EBIT) + depreciation & amortization."),
            ("What is a good EBITDA margin?", "It varies widely by industry — software firms may exceed 30–40%, while low-margin sectors run in single digits. Compare against industry peers and track the trend rather than using a universal benchmark."),
            ("Why is EBITDA criticized?", "Because it ignores real costs: depreciation reflects assets that wear out and need replacing, and excluding interest hides the burden of debt. High EBITDA can mask weak actual cash flow, so it shouldn't be used alone."),
        ],
    },
    {
        "slug": "rent-increase-calculator",
        "emoji": "\U0001F4C8",
        "category": "Budgeting & Life",
        "title": "Rent Increase Calculator — New Rent and Percentage Change",
        "h1": "Rent Increase Calculator",
        "blurb": "New rent after an increase, and if it's fair.",
        "meta_description": "Calculate your new rent after a percentage or dollar increase, the extra you'll pay per year, and how the increase compares to inflation.",
        "intro": "Got a rent increase notice? Enter your current rent and the increase to see the new amount, the annual cost, and whether it's in line with inflation or steep.",
        "fields": [
            {"id": "rent", "label": "Current monthly rent ($)", "value": 1800},
            {"id": "pct", "label": "Increase (%)", "value": 5, "step": 0.1},
            {"id": "flat", "label": "Or flat increase ($/month, optional)", "value": 0},
            {"id": "inflation", "label": "Current inflation rate (%)", "value": 3, "step": 0.1},
        ],
        "js": """
function calculate() {
  const rent = val('rent'), pct = val('pct')/100, flat = val('flat'), inf = val('inflation');
  const inc = flat > 0 ? flat : rent*pct;
  const newRent = rent + inc;
  const effPct = rent>0 ? inc/rent*100 : 0;
  let verdict;
  if (effPct <= inf) verdict = 'At or below inflation — a relatively normal increase';
  else if (effPct <= inf + 3) verdict = 'Above inflation — worth a polite negotiation';
  else verdict = 'Well above inflation — steep; negotiate or compare alternatives';
  show(`<div class="result-main">$${fmt(newRent,0)} / month<small>New rent — up $${fmt(inc,0)} (${fmt(effPct,1)}%)</small></div>
  <table>
    <tr><td>Extra per month</td><td>$${fmt(inc,0)}</td></tr>
    <tr><td>Extra per year</td><td>$${fmt(inc*12,0)}</td></tr>
    <tr><td>Increase vs inflation (${fmt(inf,1)}%)</td><td>${effPct>inf ? '+' : ''}${fmt(effPct-inf,1)}% real</td></tr>
    <tr><td>Assessment</td><td>${verdict}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Reading a rent increase clearly</h2>
<p>A rent increase notice usually states either a percentage or a dollar amount. This calculator converts between them, shows your new rent, and — most usefully — compares the increase to inflation. That comparison is the key context: an increase roughly at the inflation rate is your landlord holding real rent steady, while an increase well above inflation is a real-terms rise in what you pay.</p>
<h2>What's a "normal" increase?</h2>
<p>There's no universal rule, but a useful frame: increases near the inflation rate (often 2–4%) are common and hard to argue with. Increases several points above inflation are worth questioning — especially if you're a reliable, long-term tenant, which has real value to a landlord who'd otherwise face vacancy, turnover costs, and the uncertainty of a new renter. A $90/month increase is $1,080 a year, so even "small" percentages add up.</p>
<h2>Negotiating, briefly</h2>
<ul>
<li><strong>Know your leverage.</strong> Good payment history, low-maintenance tenancy, and local vacancy rates all strengthen your case. Turnover is expensive for landlords.</li>
<li><strong>Anchor to data.</strong> Cite comparable local rents and the inflation rate; propose a specific lower number rather than just objecting.</li>
<li><strong>Offer something back.</strong> A longer lease commitment in exchange for a smaller increase can suit both sides.</li>
<li><strong>Check local rules.</strong> Some areas cap increases or require notice periods — know your rights before negotiating.</li>
<li><strong>Price the move-out threat honestly.</strong> The <a href="/calculators/move-or-stay-calculator/">move or stay calculator</a> compares the renewal against the true all-in cost of moving — and computes the exact renewal rent at which staying equals leaving, which is the strongest number to negotiate from.</li>
</ul>
<h2>The bigger budget picture</h2>
<p>Housing is most people's largest expense, so a rent rise ripples through everything. Re-run your numbers with the <a href="/calculators/rent-affordability-calculator/">rent affordability calculator</a> to check the new rent still fits comfortably within your income — and if it pushes past a healthy share of take-home pay, that's a signal to negotiate harder or weigh alternatives.</p>
""",
        "faqs": [
            ("How do I calculate a rent increase?", "Multiply your current rent by the percentage increase and add it, or add a flat dollar amount. A 5% increase on $1,800 rent adds $90, for a new rent of $1,890."),
            ("Is my rent increase reasonable?", "Compare it to inflation. Increases near the inflation rate (2–4%) are common; those well above it are worth negotiating, particularly if you're a reliable long-term tenant whose turnover would cost the landlord."),
            ("Can I negotiate a rent increase?", "Often, yes. Strong payment history, comparable local rents, and offering a longer lease all help. Some regions also cap increases or mandate notice, so check your local tenant rules first."),
        ],
    },
]
