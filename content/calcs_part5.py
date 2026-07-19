# -*- coding: utf-8 -*-
"""Batch 3 calculators: Loans, Income, Taxes & Shopping, Business."""

PART5 = [
    {
        "slug": "car-affordability-calculator",
        "emoji": "\U0001F697",
        "category": "Loans & Debt",
        "title": "Car Affordability Calculator — What Car Payment Can You Afford?",
        "h1": "Car Affordability Calculator",
        "blurb": "Turn a monthly budget into a realistic car price.",
        "meta_description": "Find out what car price you can afford from a monthly payment budget, down payment, loan term and rate — the reverse of a normal loan calculator.",
        "intro": "Instead of falling in love with a car and forcing the numbers, start from what you can comfortably pay each month. Enter your budget and this works backwards to a realistic car price — including your down payment.",
        "fields": [
            {"id": "payment", "label": "Comfortable monthly payment ($)", "value": 400},
            {"id": "down", "label": "Down payment / trade-in ($)", "value": 3000},
            {"id": "rate", "label": "Loan interest rate (%)", "value": 7.5, "step": 0.1},
            {"id": "years", "label": "Loan term (years)", "value": 5, "step": 0.5},
        ],
        "js": """
function calculate() {
  const pmt = val('payment'), down = val('down'), r = val('rate')/100, y = val('years');
  const i = r/12, n = Math.round(y*12);
  const loan = i > 0 ? pmt * (1 - Math.pow(1+i, -n)) / i : pmt * n;
  const price = loan + down;
  const totalPaid = pmt * n + down;
  const interest = totalPaid - price;
  show(`<div class="result-main">$${fmt(price,0)}<small>Car price you can afford at $${fmt(pmt,0)}/month</small></div>
  <table>
    <tr><td>Loan amount</td><td>$${fmt(loan,0)}</td></tr>
    <tr><td>Down payment</td><td>$${fmt(down,0)}</td></tr>
    <tr><td>Total interest over ${y} yrs</td><td>$${fmt(interest,0)}</td></tr>
    <tr><td>Total you'll pay</td><td>$${fmt(totalPaid,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Budget first, car second</h2>
<p>Dealerships love to negotiate on the monthly payment because it hides the real price — stretch the loan long enough and almost anything "fits." Flip the process: decide the payment you can genuinely afford, then let the math reveal the price range. This calculator does exactly that, discounting your monthly budget back into a loan amount and adding your down payment.</p>
<h2>The 20/4/10 guideline</h2>
<p>A widely used rule for buying a car sensibly: put at least <strong>20% down</strong>, finance for no more than <strong>4 years</strong>, and keep total transport costs (payment plus insurance) under <strong>10% of gross income</strong>. Longer loans (6–7 years) shrink the monthly payment but pile on interest and keep you "underwater" — owing more than the car is worth — for years.</p>
<h2>The costs beyond the payment</h2>
<ul>
<li><strong>Insurance:</strong> often $100–$200+ a month, and higher for newer or financed cars requiring full coverage.</li>
<li><strong>Fuel, maintenance, tyres:</strong> a real and recurring line item.</li>
<li><strong>Depreciation:</strong> new cars can lose 20%+ of their value in the first year — the largest hidden cost of all.</li>
</ul>
<p>Because of depreciation and lower prices, lightly-used cars (2–4 years old) often deliver far better value than new. Whatever you choose, financing a payment you can truly afford — rather than the biggest one a lender will approve — is what keeps a car an asset for living rather than a drag on your finances.</p>
""",
        "faqs": [
            ("How much should I put down on a car?", "Aim for at least 20%. A larger down payment reduces the loan, lowers interest, and helps you avoid owing more than the car is worth as it depreciates."),
            ("Is a longer loan term a good idea?", "Usually not. Longer terms lower the monthly payment but increase total interest and keep you underwater longer. Four years or less is a common guideline for financial health."),
            ("Does this include insurance and running costs?", "No — it covers only the financing. Budget separately for insurance, fuel, and maintenance, which together often rival the loan payment itself."),
        ],
    },
    {
        "slug": "credit-card-payoff-calculator",
        "emoji": "\U0001F4B3",
        "category": "Loans & Debt",
        "title": "Credit Card Payoff Calculator — Time and Interest to Clear a Balance",
        "h1": "Credit Card Payoff Calculator",
        "blurb": "How long to clear a card, and what interest costs you.",
        "meta_description": "See how long it takes to pay off a credit card and how much interest you'll pay, plus how much faster you finish by paying more than the minimum.",
        "intro": "Credit card interest is brutal precisely because balances linger. Enter your balance, rate and monthly payment to see the payoff time and interest cost — then try raising the payment to watch both numbers collapse.",
        "fields": [
            {"id": "balance", "label": "Card balance ($)", "value": 6000},
            {"id": "apr", "label": "Card APR (%)", "value": 22, "step": 0.1},
            {"id": "payment", "label": "Monthly payment ($)", "value": 250},
        ],
        "js": """
function payoff(bal, i, pmt) {
  if (pmt <= bal*i) return null;
  let months = 0, interest = 0;
  while (bal > 0 && months < 1200) { const int = bal*i; interest += int; bal = bal + int - pmt; months++; }
  return { months, interest };
}
function calculate() {
  const bal = val('balance'), i = val('apr')/100/12, pmt = val('payment');
  const res = payoff(bal, i, pmt);
  if (!res) { show(`<div class="result-main">Never at this rate<small>Your payment barely covers monthly interest ($${fmt(bal*i)}). Increase it to make progress.</small></div>`); return; }
  const yrs = Math.floor(res.months/12), mo = res.months%12;
  const dbl = payoff(bal, i, pmt*2);
  show(`<div class="result-main">${yrs}y ${mo}m<small>to clear $${fmt(bal,0)} &mdash; $${fmt(res.interest)} paid in interest</small></div>
  <table>
    <tr><td>Total interest</td><td>$${fmt(res.interest)}</td></tr>
    <tr><td>Total you'll repay</td><td>$${fmt(bal + res.interest)}</td></tr>
    <tr><td>If you paid double ($${fmt(pmt*2,0)})</td><td>${dbl ? Math.floor(dbl.months/12)+'y '+(dbl.months%12)+'m, save $'+fmt(res.interest-dbl.interest) : '—'}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why credit card debt feels like quicksand</h2>
<p>At a 22% APR, interest accrues at nearly 1.8% <em>per month</em> on your balance. Make only a small payment and much of it is eaten by interest, leaving the principal barely moving. This is why minimum payments can keep a balance alive for a decade and cost more in interest than the original purchases. The math isn't a trap set against you specifically — it's just compound interest running in the lender's favor.</p>
<h2>The single most powerful move</h2>
<p>Pay more than the minimum, and do it consistently. Notice the "if you paid double" line in your result — doubling the payment typically more than halves both the time and the total interest, because extra dollars attack principal directly and shrink every future interest charge. Even an extra $50–$100 a month produces outsized results.</p>
<h2>Faster routes when the rate is the problem</h2>
<ul>
<li><strong>0% balance transfer cards</strong> move the debt to an interest-free promo period (typically 12–21 months) for a one-time fee of ~3–5%. Powerful if you stop new spending and clear it before the promo ends.</li>
<li><strong>Personal consolidation loans</strong> at a lower fixed rate can slash interest while giving you a definite payoff date.</li>
<li><strong>A rate-reduction call</strong> to your issuer sometimes works for long-standing customers — a five-minute ask with no downside.</li>
</ul>
<h2>Stop the bleeding first</h2>
<p>No payoff plan survives new charges piling onto the balance. Pause using the card until it's cleared, build a small starter emergency fund so surprises don't land back on the card, and treat high-interest debt as the financial emergency it is — paying it off is a guaranteed, tax-free return equal to the APR, which almost no investment can match.</p>
""",
        "faqs": [
            ("Why does paying the minimum take so long?", "Minimum payments are calculated to be small (often 1–3% of the balance), so most of each payment covers interest rather than principal. The balance shrinks glacially, stretching payoff over years and multiplying total interest."),
            ("Should I pay off cards or save first?", "Build a small starter emergency fund (about $1,000) so a surprise doesn't send you back to the card, then attack high-interest debt aggressively. Paying off a 22% card is a guaranteed 22% return — better than any safe investment."),
            ("Do balance transfers hurt my credit?", "Opening a new card causes a small, temporary dip, but lowering your overall utilization by clearing the balance usually helps over time. The interest savings typically outweigh the minor short-term effect."),
        ],
    },
    {
        "slug": "debt-to-income-ratio-calculator",
        "emoji": "\u2696\uFE0F",
        "category": "Loans & Debt",
        "title": "Debt-to-Income Ratio Calculator — The Number Lenders Check",
        "h1": "Debt-to-Income (DTI) Calculator",
        "blurb": "The ratio lenders use to approve mortgages and loans.",
        "meta_description": "Calculate your debt-to-income ratio (DTI) from monthly debt payments and gross income — the key number mortgage and loan approvals depend on.",
        "intro": "Your debt-to-income ratio is the first thing a lender checks before approving a mortgage or loan. Enter your monthly debt payments and gross income to see your DTI and where you stand against common lending thresholds.",
        "fields": [
            {"id": "income", "label": "Gross monthly income ($)", "value": 6000, "hint": "before tax"},
            {"id": "housing", "label": "Housing payment (rent/mortgage) ($)", "value": 1500},
            {"id": "car", "label": "Car & other loan payments ($)", "value": 400},
            {"id": "cards", "label": "Minimum credit card payments ($)", "value": 150},
            {"id": "other", "label": "Other monthly debt ($)", "value": 0},
        ],
        "js": """
function calculate() {
  const inc = val('income');
  if (inc <= 0) { show('<div class="result-main">Enter your gross monthly income.</div>'); return; }
  const housing = val('housing');
  const totalDebt = housing + val('car') + val('cards') + val('other');
  const dti = totalDebt / inc * 100;
  const frontEnd = housing / inc * 100;
  let verdict;
  if (dti <= 36) verdict = 'Healthy — comfortably within most lending limits';
  else if (dti <= 43) verdict = 'Acceptable — near the common mortgage ceiling of 43%';
  else if (dti <= 50) verdict = 'High — many lenders will hesitate; focus on reducing debt';
  else verdict = 'Very high — approvals unlikely; prioritise paying down debt';
  show(`<div class="result-main">${fmt(dti,1)}%<small>${verdict}</small></div>
  <table>
    <tr><td>Total monthly debt</td><td>$${fmt(totalDebt,0)}</td></tr>
    <tr><td>Front-end ratio (housing only)</td><td>${fmt(frontEnd,1)}%</td></tr>
    <tr><td>Income free of debt</td><td>${fmt(100-dti,1)}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>What DTI is and why lenders obsess over it</h2>
<p>Debt-to-income ratio is your total monthly debt payments divided by your gross (pre-tax) monthly income. It's the clearest single signal of whether you can take on another payment without overstretching. Lenders use it because it predicts default risk better than income alone — a high earner drowning in payments is riskier than a modest earner with little debt.</p>
<h2>Front-end vs back-end</h2>
<ul>
<li><strong>Front-end ratio</strong> counts only housing costs. Many mortgage guidelines want this under ~28%.</li>
<li><strong>Back-end ratio</strong> (the main DTI here) counts <em>all</em> debt payments. The common conforming-mortgage ceiling is 43%, with the sweet spot at 36% or below.</li>
</ul>
<h2>What counts — and what doesn't</h2>
<p>Include: rent or mortgage, car loans, minimum credit card payments, student loans, personal loans, and other required debt. Exclude: utilities, groceries, insurance, subscriptions, and taxes — DTI measures <em>debt obligations</em>, not general living costs. Use the minimum required payment on revolving debt, since that's what lenders assume.</p>
<h2>Lowering your DTI</h2>
<p>Two levers: reduce debt or raise income. Paying off a small loan entirely removes its whole payment from the numerator and can noticeably drop your ratio — sometimes more effectively than chipping at a large balance. Avoid taking on new debt (or even large credit inquiries) in the months before a mortgage application, since lenders re-check DTI right up to closing. A DTI under 36% not only unlocks better loan terms; it's a sign your budget has genuine breathing room.</p>
""",
        "faqs": [
            ("What DTI do I need for a mortgage?", "Many conventional loans cap back-end DTI at 43%, though some programs allow higher with strong credit or reserves. Below 36% generally earns the best terms and widest approval odds."),
            ("Does DTI use gross or net income?", "Gross — your income before taxes and deductions. That's the figure lenders standardise on, so use pre-tax income for an accurate comparison to their thresholds."),
            ("Do utilities and insurance count?", "No. DTI includes only debt payments (loans, cards, mortgage/rent). Regular living expenses like utilities, groceries, and insurance are excluded."),
        ],
    },
    {
        "slug": "hourly-to-salary-calculator",
        "emoji": "\U0001F4C6",
        "category": "Income & Budgeting",
        "title": "Hourly to Salary Calculator — Annual Income from an Hourly Wage",
        "h1": "Hourly to Salary Calculator",
        "blurb": "Convert an hourly wage into weekly, monthly and yearly pay.",
        "meta_description": "Convert an hourly wage into annual, monthly and weekly salary based on your hours and weeks worked. Compare job offers on equal footing.",
        "intro": "Comparing an hourly job to a salaried offer? Convert your hourly wage into annual terms. Enter your rate, weekly hours and weeks worked per year to see the equivalent salary — before and adjusted for time off.",
        "fields": [
            {"id": "rate", "label": "Hourly wage ($)", "value": 25, "step": 0.5},
            {"id": "hours", "label": "Hours per week", "value": 40, "step": 0.5},
            {"id": "weeks", "label": "Weeks worked per year", "value": 50, "step": 1, "hint": "52 minus unpaid time off"},
        ],
        "js": """
function calculate() {
  const r = val('rate'), h = val('hours'), w = val('weeks');
  const annual = r * h * w;
  const fullYear = r * h * 52;
  show(`<div class="result-main">$${fmt(annual,0)} / year<small>at $${fmt(r)}/hr, ${h} hrs/week, ${w} weeks</small></div>
  <table>
    <tr><td>Monthly (gross)</td><td>$${fmt(annual/12,0)}</td></tr>
    <tr><td>Weekly (gross)</td><td>$${fmt(r*h,0)}</td></tr>
    <tr><td>If paid all 52 weeks</td><td>$${fmt(fullYear,0)}</td></tr>
    <tr><td>Quick rule (rate × 2000)</td><td>$${fmt(r*2000,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The conversion, and the quick trick</h2>
<p>Annual salary = hourly rate × hours per week × weeks worked. The handy shortcut for a standard full-time year (40 hours × ~50 weeks = 2,000 hours) is to <strong>multiply your hourly rate by 2,000</strong>: $25/hour ≈ $50,000/year. In reverse, divide a salary by 2,000 to estimate the hourly equivalent — a $60,000 salary is about $30/hour.</p>
<h2>Why "weeks worked" matters</h2>
<p>Hourly workers are usually paid only for hours actually worked, so unpaid time off directly reduces annual income. Salaried employees are typically paid across all 52 weeks including vacation. That difference — captured by the "weeks worked" field — is a real gap when comparing an hourly role to a salary. The "if paid all 52 weeks" line shows the ceiling if every week were compensated.</p>
<h2>Comparing offers fairly</h2>
<ul>
<li><strong>Benefits:</strong> salaried roles often include paid leave, health coverage, and retirement matching that hourly roles may not. Add their value before comparing.</li>
<li><strong>Overtime:</strong> hourly work may pay 1.5× beyond 40 hours — a premium salaried staff rarely get.</li>
<li><strong>Stability:</strong> salary smooths income across slow periods; hourly pay swings with available hours.</li>
</ul>
<p>All figures here are gross (pre-tax). Your take-home depends on your tax situation — use a take-home pay estimator for the net comparison that actually hits your bank account.</p>
""",
        "faqs": [
            ("How many hours are in a work year?", "A standard full-time year is about 2,080 hours (40 × 52) before time off, or roughly 2,000 working hours after typical vacation. The '× 2000' shortcut uses the latter for quick mental conversion."),
            ("Should I compare hourly and salary jobs on gross pay?", "Start with gross for an apples-to-apples base, then adjust for benefits, paid leave, overtime potential, and stability, which often differ significantly between hourly and salaried roles."),
            ("Does this account for taxes?", "No — it shows gross income. Net take-home depends on your country, filing status, and deductions; use a take-home pay calculator for the after-tax figure."),
        ],
    },
    {
        "slug": "rent-affordability-calculator",
        "emoji": "\U0001F3E1",
        "category": "Income & Budgeting",
        "title": "Rent Affordability Calculator — How Much Rent Can You Afford?",
        "h1": "Rent Affordability Calculator",
        "blurb": "A sensible rent range based on your income.",
        "meta_description": "Find how much rent you can afford using the 30% rule and your other debts. Get a comfortable monthly rent range based on your income.",
        "intro": "How much rent is too much? Enter your income and existing debts to get a comfortable rent range based on the widely-used 30% guideline — adjusted for the other commitments already claiming your paycheck.",
        "fields": [
            {"id": "income", "label": "Gross monthly income ($)", "value": 5000, "hint": "before tax"},
            {"id": "debts", "label": "Existing monthly debt payments ($)", "value": 500},
        ],
        "js": """
function calculate() {
  const inc = val('income'), debts = val('debts');
  if (inc <= 0) { show('<div class="result-main">Enter your gross monthly income.</div>'); return; }
  const rule30 = inc * 0.30;
  const conservative = inc * 0.25;
  const stretch = inc * 0.35;
  const dtiCap = inc * 0.43 - debts;
  const affordable = Math.max(0, Math.min(stretch, dtiCap));
  show(`<div class="result-main">$${fmt(rule30,0)} / month<small>The classic 30%-of-income rent target</small></div>
  <table>
    <tr><td>Conservative (25%)</td><td>$${fmt(conservative,0)}</td></tr>
    <tr><td>Comfortable (30%)</td><td>$${fmt(rule30,0)}</td></tr>
    <tr><td>Stretch ceiling (35%)</td><td>$${fmt(stretch,0)}</td></tr>
    <tr><td>Max once other debts counted</td><td>$${fmt(affordable,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The 30% rule</h2>
<p>The oldest guideline in renting: keep housing costs at or below <strong>30% of gross income</strong>. On a $5,000 monthly income that's $1,500. The rule persists because it usually leaves enough for savings, debt, and living once other essentials are covered. It's a starting point, not a law — but consistently blowing past it is the most common cause of a permanently tight budget.</p>
<h2>Why your other debts change the answer</h2>
<p>The 30% rule assumes typical debt levels. If you already carry heavy car or loan payments, the same rent becomes a squeeze. That's why this calculator also shows a ceiling based on a 43% total debt-to-income limit minus your existing payments — the same logic landlords and lenders use. The lower of "30% of income" and "what's left under the DTI cap" is your honest maximum.</p>
<h2>Costs renters forget</h2>
<ul>
<li><strong>Utilities</strong> (electricity, gas, water, internet) can add $150–$300+ monthly on top of rent.</li>
<li><strong>Renter's insurance</strong> — inexpensive but real.</li>
<li><strong>Upfront cash:</strong> most leases need first month plus a deposit (sometimes last month too), so budget 2–3× the monthly rent to move in.</li>
</ul>
<h2>When 30% is impossible</h2>
<p>In expensive cities, 30% may not rent anything livable, and many people spend 40–50% out of necessity. If that's you, protect savings at all costs (even 10%), consider roommates to split fixed costs, or weigh a longer commute against the rent difference. High rent relative to income is a structural signal — sometimes the real fix is location or housemates, not tighter budgeting.</p>
""",
        "faqs": [
            ("Is the 30% rule based on gross or net income?", "Traditionally gross (pre-tax) income, which is what landlords check. Budgeting against net income is stricter and safer, especially if your tax rate is high."),
            ("What if I can't find anything at 30%?", "In high-cost areas this is common. Prioritise keeping some savings, consider roommates to share fixed costs, and treat any rent above ~40% of income as a temporary situation to plan your way out of."),
            ("Do landlords have income requirements?", "Many require gross income of about 3× the monthly rent (equivalent to the 33% rule) and check your debt-to-income and credit. Meeting the 30% guideline usually clears these checks comfortably."),
        ],
    },
    {
        "slug": "sales-tax-calculator",
        "emoji": "\U0001F9FE",
        "category": "Taxes & Shopping",
        "title": "Sales Tax Calculator — Add or Remove Tax from a Price",
        "h1": "Sales Tax Calculator",
        "blurb": "Add sales tax to a price, or back it out of a total.",
        "meta_description": "Add sales tax to a price or extract the tax from a tax-inclusive total. Fast, accurate sales tax calculations for any rate.",
        "intro": "Add tax to a pre-tax price, or work out how much tax is hidden inside a total you've already been charged. Enter a price and rate, and choose which direction you need.",
        "fields": [
            {"id": "amount", "label": "Amount ($)", "value": 100},
            {"id": "rate", "label": "Sales tax rate (%)", "value": 8, "step": 0.01},
            {"id": "mode", "label": "The amount above is", "value": "pre", "type": "select",
             "options": [["pre", "a pre-tax price (add tax)"], ["incl", "a tax-included total (remove tax)"]]},
        ],
        "js": """
function calculate() {
  const a = val('amount'), r = val('rate')/100, mode = document.getElementById('mode').value;
  if (mode === 'pre') {
    const tax = a * r, total = a + tax;
    show(`<div class="result-main">$${fmt(total)}<small>Total including ${fmt(r*100,2)}% sales tax</small></div>
    <table><tr><td>Pre-tax price</td><td>$${fmt(a)}</td></tr>
    <tr><td>Sales tax</td><td>$${fmt(tax)}</td></tr>
    <tr><td>Total</td><td>$${fmt(total)}</td></tr></table>`);
  } else {
    const pre = a / (1 + r), tax = a - pre;
    show(`<div class="result-main">$${fmt(pre)}<small>Pre-tax price inside a $${fmt(a)} total</small></div>
    <table><tr><td>Pre-tax price</td><td>$${fmt(pre)}</td></tr>
    <tr><td>Sales tax portion</td><td>$${fmt(tax)}</td></tr>
    <tr><td>Total charged</td><td>$${fmt(a)}</td></tr></table>`);
  }
}
""",
        "body_html": """
<h2>Adding tax vs removing tax</h2>
<p>Adding tax is simple: multiply the price by the rate and add it on. <em>Removing</em> tax from a tax-inclusive total trips people up — you can't just subtract the rate. If a $108 total includes 8% tax, the pre-tax price isn't $99.36 (108 − 8%); it's $100, because the 8% was calculated on $100, not on $108. The correct formula divides: <code>pre-tax = total ÷ (1 + rate)</code>.</p>
<h2>When you need each direction</h2>
<ul>
<li><strong>Adding tax:</strong> budgeting a purchase, quoting a customer, checking a receipt total.</li>
<li><strong>Removing tax:</strong> expense reports and bookkeeping that need the pre-tax amount, or figuring out the "real" price of a tax-inclusive item.</li>
</ul>
<h2>A note on rates</h2>
<p>Sales tax varies enormously by location. In the US it's set by state, county, and city combined — so a single street can differ from the next town. Many US states also exempt groceries or clothing. Elsewhere, value-added tax (VAT) or goods-and-services tax (GST) is usually built into the displayed price rather than added at the register. Always use the rate that actually applies where the sale happens; this calculator handles any rate you enter.</p>
""",
        "faqs": [
            ("How do I remove sales tax from a total?", "Divide the total by (1 + tax rate). For 8% tax, divide by 1.08. Subtracting 8% from the total gives the wrong answer because the tax was based on the lower pre-tax price."),
            ("Why is sales tax different everywhere?", "In the US it's layered from state, county, and city rates, and some categories (like groceries) may be exempt. Always apply the combined rate for the exact location of the sale."),
            ("Is sales tax the same as VAT?", "They're similar consumption taxes but administered differently. VAT/GST is typically included in the shelf price and collected at each production stage; US sales tax is added at the final sale. Use the VAT calculator for inclusive-price countries."),
        ],
    },
    {
        "slug": "discount-calculator",
        "emoji": "\U0001F3F7\uFE0F",
        "category": "Taxes & Shopping",
        "title": "Discount Calculator — Sale Price and Money Saved",
        "h1": "Discount Calculator",
        "blurb": "Final price after a percentage off, and what you save.",
        "meta_description": "Calculate the sale price after a percentage discount and see how much you save. Handles stacked discounts and shows the effective total discount.",
        "intro": "See exactly what you'll pay after a discount — and what you actually save. Enter the original price and the percent off; optionally add a second discount to see how 'stacked' offers really combine.",
        "fields": [
            {"id": "price", "label": "Original price ($)", "value": 80},
            {"id": "off", "label": "Discount (%)", "value": 25, "step": 1},
            {"id": "off2", "label": "Extra discount on top (%, optional)", "value": 0, "step": 1, "hint": "applied after the first"},
        ],
        "js": """
function calculate() {
  const p = val('price'), d1 = val('off')/100, d2 = val('off2')/100;
  const after1 = p * (1 - d1);
  const final = after1 * (1 - d2);
  const saved = p - final;
  const effective = p > 0 ? saved / p * 100 : 0;
  let extra = '';
  if (d2 > 0) extra = `<tr><td>Effective total discount</td><td>${fmt(effective,1)}% (not ${fmt((d1+d2)*100,0)}%)</td></tr>`;
  show(`<div class="result-main">$${fmt(final)}<small>Final price &mdash; you save $${fmt(saved)}</small></div>
  <table>
    <tr><td>Original price</td><td>$${fmt(p)}</td></tr>
    <tr><td>You save</td><td>$${fmt(saved)} (${fmt(effective,1)}%)</td></tr>
    ${extra}
  </table>`);
}
""",
        "body_html": """
<h2>The math behind the sale tag</h2>
<p>Sale price = original × (1 − discount). A 25% discount on $80 leaves you paying $60 and saving $20. Simple enough — but retailers count on shoppers misjudging percentages, especially when discounts stack.</p>
<h2>Stacked discounts don't add up</h2>
<p>"25% off, then an extra 20% off" is <strong>not</strong> 45% off. The second discount applies to the already-reduced price: $80 → $60 → $48. That's a $32 saving, or 40% effective — not 45%. Stacked percentages always produce a smaller total discount than their sum, because each one works on a shrinking base. This calculator's "effective total discount" line shows the true figure so a clever-looking sign doesn't fool you.</p>
<h2>Smart-shopper checks</h2>
<ul>
<li><strong>Discount off what?</strong> A percentage off an inflated "original" price can beat a smaller discount off a fair one. Compare final prices, not percentages.</li>
<li><strong>Need vs deal.</strong> Saving 40% on something you wouldn't otherwise buy is spending 60%, not saving anything.</li>
<li><strong>Add tax back.</strong> The advertised sale price is usually pre-tax; the register total will be higher.</li>
</ul>
<p>The only number that matters at checkout is the final amount leaving your account. Percentages are marketing; the total is reality.</p>
""",
        "faqs": [
            ("How do I combine two discounts?", "Apply them one after another, not by adding. 20% then 10% means multiply by 0.8 then by 0.9 (0.72 total), giving a 28% effective discount — less than the 30% the numbers might suggest."),
            ("What does 'effective discount' mean?", "The single discount percentage that would produce the same final price as the stacked discounts. It's always less than the sum of the individual percentages."),
            ("Is the sale price before or after tax?", "Advertised discounts almost always apply to the pre-tax price. Sales tax is then added to the discounted amount at checkout, so your final total will be a bit higher than the sale price shown."),
        ],
    },
    {
        "slug": "tip-calculator",
        "emoji": "\U0001F37D\uFE0F",
        "category": "Taxes & Shopping",
        "title": "Tip Calculator — Gratuity and Bill Split",
        "h1": "Tip Calculator",
        "blurb": "Work out the tip and split a bill between people.",
        "meta_description": "Calculate a tip at any percentage and split the total between any number of people, with per-person amounts. Fast and simple.",
        "intro": "Figure out the tip and, if you're with others, split the whole bill evenly. Enter the bill, choose a tip percentage, and set how many people are sharing.",
        "fields": [
            {"id": "bill", "label": "Bill amount ($)", "value": 60},
            {"id": "tip", "label": "Tip (%)", "value": 18, "step": 1},
            {"id": "people", "label": "Split between (people)", "value": 2, "step": 1},
        ],
        "js": """
function calculate() {
  const bill = val('bill'), t = val('tip')/100, people = Math.max(1, Math.round(val('people')));
  const tip = bill * t, total = bill + tip;
  show(`<div class="result-main">$${fmt(total)}<small>Total with ${fmt(t*100,0)}% tip ($${fmt(tip)})</small></div>
  <table>
    <tr><td>Tip amount</td><td>$${fmt(tip)}</td></tr>
    <tr><td>Total bill</td><td>$${fmt(total)}</td></tr>
    <tr><td>Per person (${people})</td><td>$${fmt(total/people)}</td></tr>
    <tr><td>Tip per person</td><td>$${fmt(tip/people)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Quick tipping guide</h2>
<p>Tip = bill × percentage. In the US, restaurant tipping norms are roughly <strong>15% for adequate service, 18–20% for good, and 20%+ for excellent</strong>. A fast mental trick: 10% is the bill with the decimal moved one place left; double it for 20%, or add half of the 10% for 15%.</p>
<h2>Splitting the bill fairly</h2>
<p>This calculator divides the tipped total evenly across your group — the simplest approach for shared meals. For uneven orders, some prefer to tip on their own item subtotal, but an even split is faster and usually close enough among friends. Either way, tip on the pre-tax bill if you want to be precise, though many people simply tip on the total for ease.</p>
<h2>Tipping around the world</h2>
<ul>
<li><strong>United States:</strong> tipping is expected and part of service workers' income; 15–20% is standard.</li>
<li><strong>Europe:</strong> service is often included; rounding up or ~5–10% is generous.</li>
<li><strong>Japan and others:</strong> tipping can be unusual or even unwelcome.</li>
</ul>
<p>When traveling, a quick check of local custom avoids both under-tipping and needlessly overpaying. This tool works for any percentage, so it adapts to wherever you are.</p>
""",
        "faqs": [
            ("Should I tip on the pre-tax or post-tax amount?", "Technically the pre-tax bill reflects the service. In practice many people tip on the total for simplicity; the difference is small on a normal bill."),
            ("What's a standard restaurant tip in the US?", "15% for satisfactory service, 18–20% for good, and more for exceptional. In the US, tips are a significant part of servers' pay, so under-tipping for good service is discouraged."),
            ("How do I split a bill with different orders?", "This tool splits evenly, which suits most shared meals. For very uneven orders, calculate each person's tip on their own subtotal, or use the even split as a friendly approximation."),
        ],
    },
    {
        "slug": "vat-calculator",
        "emoji": "\U0001F9FE",
        "category": "Taxes & Shopping",
        "title": "VAT Calculator — Add or Remove Value-Added Tax",
        "h1": "VAT Calculator",
        "blurb": "Add VAT to a net price or extract it from a gross price.",
        "meta_description": "Add VAT to a net price or remove VAT from a gross (VAT-inclusive) price at any rate. Essential for invoicing, expenses and shopping in VAT countries.",
        "intro": "Work with value-added tax in either direction: add VAT to a net price, or pull the VAT out of a gross price that already includes it. Enter an amount and rate, and pick the direction.",
        "fields": [
            {"id": "amount", "label": "Amount ($/€/£)", "value": 100},
            {"id": "rate", "label": "VAT rate (%)", "value": 20, "step": 0.5},
            {"id": "mode", "label": "The amount above is", "value": "net", "type": "select",
             "options": [["net", "a net price (add VAT)"], ["gross", "a gross VAT-inclusive price (remove VAT)"]]},
        ],
        "js": """
function calculate() {
  const a = val('amount'), r = val('rate')/100, mode = document.getElementById('mode').value;
  if (mode === 'net') {
    const vat = a * r, gross = a + vat;
    show(`<div class="result-main">${fmt(gross)}<small>Gross price including ${fmt(r*100,1)}% VAT</small></div>
    <table><tr><td>Net price</td><td>${fmt(a)}</td></tr>
    <tr><td>VAT</td><td>${fmt(vat)}</td></tr>
    <tr><td>Gross price</td><td>${fmt(gross)}</td></tr></table>`);
  } else {
    const net = a / (1 + r), vat = a - net;
    show(`<div class="result-main">${fmt(net)}<small>Net price inside a ${fmt(a)} gross total</small></div>
    <table><tr><td>Net price</td><td>${fmt(net)}</td></tr>
    <tr><td>VAT portion</td><td>${fmt(vat)}</td></tr>
    <tr><td>Gross price</td><td>${fmt(a)}</td></tr></table>`);
  }
}
""",
        "body_html": """
<h2>Net, VAT, and gross</h2>
<p>VAT terminology: the <strong>net</strong> price is before tax, the <strong>VAT</strong> is the tax itself, and the <strong>gross</strong> price is net plus VAT — what the customer actually pays. Adding VAT multiplies the net by (1 + rate). Removing it <em>divides</em> the gross by (1 + rate): a £120 gross price at 20% VAT contains £100 net and £20 VAT, not £24, because the 20% was charged on £100.</p>
<h2>Why removing VAT matters for businesses</h2>
<p>VAT-registered businesses record the net amount as their cost or revenue and account for the VAT separately (reclaiming VAT paid on purchases, remitting VAT collected on sales). So extracting the net from a gross invoice is a daily bookkeeping task. Getting the division right — rather than naively subtracting the percentage — keeps your accounts and tax returns accurate.</p>
<h2>VAT vs US sales tax</h2>
<ul>
<li><strong>Displayed price:</strong> VAT is usually included on the shelf/label; US sales tax is added at checkout.</li>
<li><strong>Collection:</strong> VAT is collected at each stage of production with credits along the chain; sales tax is charged once at the final sale.</li>
<li><strong>Rates:</strong> VAT rates are often higher (commonly 15–25%) and may have reduced rates for essentials like food or books.</li>
</ul>
<p>Whatever the label on the tax, this calculator handles the arithmetic — just enter the correct rate for your country and choose whether you're adding or removing.</p>
""",
        "faqs": [
            ("How do I remove VAT from a price?", "Divide the gross (VAT-inclusive) price by (1 + VAT rate). At 20% VAT, divide by 1.2. Subtracting 20% overstates the VAT because it was calculated on the lower net price."),
            ("What's the difference between net and gross?", "Net is the price before VAT; gross is the price after VAT is added — the amount the customer pays. VAT is the difference between them."),
            ("Is VAT the same everywhere?", "No. Rates vary widely by country (commonly 15–25%), and many places apply reduced or zero rates to essentials. Always use the rate that applies to your specific transaction and location."),
        ],
    },
    {
        "slug": "freelance-hourly-rate-calculator",
        "emoji": "\U0001F9D1\u200D\U0001F4BB",
        "category": "Business",
        "title": "Freelance Rate Calculator — What to Charge Per Hour",
        "h1": "Freelance Hourly Rate Calculator",
        "blurb": "Turn a target income into the hourly rate you must charge.",
        "meta_description": "Calculate the freelance hourly rate you need from your income goal, business expenses, time off, and realistic billable hours. Stop underpricing your work.",
        "intro": "New freelancers routinely charge too little by copying an old salary's hourly rate — forgetting that they now pay their own taxes, benefits, and downtime. Enter your target income and realities to find the rate you actually need to charge.",
        "fields": [
            {"id": "income", "label": "Desired annual take-home ($)", "value": 60000},
            {"id": "expenses", "label": "Annual business expenses ($)", "value": 6000, "hint": "software, gear, insurance"},
            {"id": "tax", "label": "Tax + benefits set-aside (%)", "value": 30, "step": 1},
            {"id": "weeks", "label": "Working weeks per year", "value": 46, "step": 1, "hint": "52 minus holidays/sick"},
            {"id": "billable", "label": "Billable hours per week", "value": 25, "step": 1, "hint": "not every hour is billable"},
        ],
        "js": """
function calculate() {
  const income = val('income'), exp = val('expenses'), taxRate = val('tax')/100;
  const weeks = val('weeks'), billable = val('billable');
  const hours = weeks * billable;
  if (hours <= 0 || taxRate >= 1) { show('<div class="result-main">Check your inputs — hours and tax rate must be sensible.</div>'); return; }
  const grossNeeded = (income / (1 - taxRate)) + exp;
  const rate = grossNeeded / hours;
  show(`<div class="result-main">$${fmt(rate)} / hour<small>to net $${fmt(income,0)} after tax &amp; expenses</small></div>
  <table>
    <tr><td>Billable hours / year</td><td>${fmt(hours,0)}</td></tr>
    <tr><td>Gross revenue needed</td><td>$${fmt(grossNeeded,0)}</td></tr>
    <tr><td>Naive rate (income ÷ 2000)</td><td>$${fmt(income/2000)} — too low</td></tr>
    <tr><td>Suggested day rate (8h)</td><td>$${fmt(rate*8,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why freelancers underprice</h2>
<p>The classic mistake: "I made $60,000 as an employee, that's about $30/hour, so I'll charge $30." This ignores three brutal realities of self-employment: you now pay <strong>both halves of taxes</strong> and all your own benefits, you <strong>can't bill every hour</strong> (admin, sales, and marketing are unpaid), and you have <strong>no paid time off</strong>. Charging your old salary rate is a fast route to earning far less while working more.</p>
<h2>How the real rate is built</h2>
<p>This calculator works backwards from what you want to keep. It grosses up your target income to cover taxes and benefits, adds business expenses, then divides by your <em>billable</em> hours — not total hours. Compare the result to the "naive rate": the honest number is typically 50–100% higher. That gap is exactly what underpriced freelancers lose.</p>
<h2>Billable hours: the number that surprises people</h2>
<p>A 40-hour week rarely yields 40 billable hours. Between finding clients, invoicing, email, and admin, 20–30 billable hours is realistic for many solo freelancers. Fewer billable hours means each one must cost more to hit your goal — which is why "I'll just work more hours" isn't the same as "I'll earn more."</p>
<h2>Beyond the minimum</h2>
<ul>
<li><strong>This is your floor, not your price.</strong> It's the rate to break even on your goal — value-based pricing can go well above it.</li>
<li><strong>Raise rates with experience.</strong> Your first rate shouldn't be your rate three years and a portfolio later.</li>
<li><strong>Consider project pricing.</strong> Charging for outcomes rather than hours often pays better and rewards efficiency instead of penalising it.</li>
</ul>
<p>Price to sustain the business you actually run — taxes, gaps, downtime and all — not the salaried job you left behind.</p>
""",
        "faqs": [
            ("Why is my freelance rate so much higher than my old salary rate?", "Because it must cover self-employment taxes, your own benefits and time off, business expenses, and the many unpaid hours spent running the business. A rate 1.5–2× your old hourly salary is common just to match the same take-home."),
            ("What are 'billable hours'?", "Hours you can actually charge a client for. Time spent on marketing, admin, invoicing, and learning is real work but usually unpaid, so most freelancers bill only 50–70% of their working hours."),
            ("Should I charge hourly or per project?", "Project pricing often earns more because it's tied to the value delivered, not the time spent, and it rewards you for being efficient. Use this hourly figure as your cost floor when quoting projects."),
        ],
    },
]
