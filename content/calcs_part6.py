# -*- coding: utf-8 -*-
"""Batch 4 calculators: more savings, loans, income, business, everyday math."""

PART6 = [
    {
        "slug": "simple-interest-calculator",
        "emoji": "\U0001F4D0",
        "category": "Savings & Investing",
        "title": "Simple Interest Calculator — Interest Without Compounding",
        "h1": "Simple Interest Calculator",
        "blurb": "Interest on principal only, no compounding.",
        "meta_description": "Calculate simple interest on a principal amount over time — the interest used by many short-term loans, bonds and promissory notes. See total interest and final balance.",
        "intro": "Simple interest is charged only on the original principal, never on accumulated interest. It's the basis of many short-term loans and bonds. Enter the amount, rate and time to see the interest and final total.",
        "fields": [
            {"id": "principal", "label": "Principal amount ($)", "value": 10000},
            {"id": "rate", "label": "Annual interest rate (%)", "value": 5, "step": 0.1},
            {"id": "years", "label": "Time (years)", "value": 3, "step": 0.1},
        ],
        "js": """
function calculate() {
  const p = val('principal'), r = val('rate')/100, y = val('years');
  const interest = p * r * y;
  const total = p + interest;
  show(`<div class="result-main">$${fmt(interest)}<small>Simple interest over ${fmt(y,1)} years</small></div>
  <table>
    <tr><td>Principal</td><td>$${fmt(p)}</td></tr>
    <tr><td>Total interest</td><td>$${fmt(interest)}</td></tr>
    <tr><td>Final balance</td><td>$${fmt(total)}</td></tr>
    <tr><td>Interest per year</td><td>$${fmt(p*r)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Simple vs compound interest</h2>
<p>Simple interest uses one clean formula: <code>Interest = Principal × Rate × Time</code>. It's charged only on the original principal — the interest never earns interest of its own. That makes it easy to calculate and predictable, but it also means it grows far slower than compound interest over long periods.</p>
<p>On $10,000 at 5% for 3 years, simple interest is a flat $1,500 ($500 per year). Compound interest on the same terms would be slightly more (~$1,576) because each year's interest joins the balance. Over 3 years the gap is small; over 30 years it becomes enormous — which is why compounding is a saver's friend and simple interest is often a borrower's.</p>
<h2>Where simple interest is actually used</h2>
<ul>
<li><strong>Short-term and personal loans</strong> — many are quoted with simple interest on the principal.</li>
<li><strong>Car loans</strong> in some markets accrue simple interest daily on the outstanding balance.</li>
<li><strong>Bonds</strong> typically pay simple interest (coupons) on their face value.</li>
<li><strong>Promissory notes and informal loans</strong> between people often use simple interest for its transparency.</li>
</ul>
<h2>A borrower's advantage</h2>
<p>With a simple-interest loan, paying early genuinely helps: because interest often accrues daily on the remaining balance, every extra payment reduces future interest immediately. Contrast this with pre-computed interest loans, where the total interest is fixed upfront and early payoff saves less. If you have a simple-interest loan, paying a little extra whenever you can is a reliable way to cut its total cost.</p>
""",
        "faqs": [
            ("What's the formula for simple interest?", "Interest = Principal × Rate × Time, where rate is the annual decimal rate and time is in years. The interest is the same each period because it's always based on the original principal."),
            ("Is simple or compound interest better for me?", "As a saver, you want compound (your interest earns interest). As a borrower, simple interest is usually cheaper because the balance you owe doesn't compound against you."),
            ("Do most savings accounts use simple interest?", "No — savings accounts almost always compound (daily or monthly). Simple interest is more common in certain loans, bonds, and short-term instruments."),
        ],
    },
    {
        "slug": "cd-calculator",
        "emoji": "\U0001F3E6",
        "category": "Savings & Investing",
        "title": "CD Calculator — Certificate of Deposit Maturity Value",
        "h1": "CD Calculator",
        "blurb": "Maturity value and interest earned on a CD.",
        "meta_description": "Calculate the maturity value and interest of a certificate of deposit (CD) from your deposit, APY and term, with compounding handled automatically.",
        "intro": "A certificate of deposit locks your money for a fixed term in exchange for a guaranteed rate. Enter your deposit, the APY and the term to see exactly what it will be worth at maturity.",
        "fields": [
            {"id": "deposit", "label": "Initial deposit ($)", "value": 10000},
            {"id": "apy", "label": "APY (%)", "value": 4.5, "step": 0.01},
            {"id": "months", "label": "Term (months)", "value": 12, "step": 1},
        ],
        "js": """
function calculate() {
  const p = val('deposit'), apy = val('apy')/100, m = val('months');
  const years = m / 12;
  const maturity = p * Math.pow(1 + apy, years);
  const interest = maturity - p;
  show(`<div class="result-main">$${fmt(maturity)}<small>Value at maturity after ${m} months</small></div>
  <table>
    <tr><td>Initial deposit</td><td>$${fmt(p)}</td></tr>
    <tr><td>Interest earned</td><td>$${fmt(interest)}</td></tr>
    <tr><td>Effective total return</td><td>${p>0 ? fmt(interest/p*100,2) : '—'}%</td></tr>
    <tr><td>Approx. monthly interest</td><td>$${fmt(interest/m)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How CDs work</h2>
<p>A certificate of deposit (called a term deposit or fixed deposit in many countries) pays a fixed, guaranteed rate in return for you agreeing not to touch the money for a set term — commonly 3 months to 5 years. Because the bank can count on the funds, CDs usually pay more than an ordinary savings account. Since the APY already reflects compounding, this calculator applies it over your term to give the maturity value.</p>
<h2>The trade-off: rate for access</h2>
<p>The catch is liquidity. Withdraw before maturity and you'll typically pay an early-withdrawal penalty — often several months of interest — that can wipe out much of your gain. CDs suit money you know you won't need until a specific date: a planned purchase, an emergency-fund tier you won't touch, or the safe portion of a portfolio.</p>
<h2>Strategies worth knowing</h2>
<ul>
<li><strong>CD laddering:</strong> split money across CDs of staggered maturities (say 1, 2, 3, 4, 5 years). One matures each year, giving regular access while most of your money earns the higher long-term rates.</li>
<li><strong>Rate environment matters:</strong> lock in long terms when rates are high; stay short when you expect rates to rise, so you can reinvest sooner.</li>
<li><strong>Compare APY, not the nominal rate</strong> — APY includes compounding and is the honest basis for comparing CDs across banks.</li>
</ul>
<h2>Safety</h2>
<p>In many countries CDs held at insured banks are protected up to a limit (e.g. FDIC insurance in the US), making them one of the safest places to earn a return. That safety is exactly why their rate, while better than checking, trails riskier investments like stocks over the long run. A CD is a place to preserve money with a modest guaranteed gain — not to grow wealth aggressively.</p>
""",
        "faqs": [
            ("What happens if I withdraw from a CD early?", "You typically pay an early-withdrawal penalty, often equal to several months of interest. For longer terms the penalty is larger. Only put money in a CD that you're confident you won't need before maturity."),
            ("Is a CD better than a savings account?", "CDs usually pay a higher rate in exchange for locking up your money. If you need flexible access, a high-yield savings account is better; if you have money earmarked for a future date, a CD earns more."),
            ("What is CD laddering?", "Splitting your money across CDs with staggered maturity dates so one matures periodically. It balances earning higher long-term rates with keeping regular access to a portion of your funds."),
        ],
    },
    {
        "slug": "house-down-payment-calculator",
        "emoji": "\U0001F511",
        "category": "Mortgages & Home",
        "title": "Down Payment Calculator — Save for a Home Deposit",
        "h1": "House Down Payment Calculator",
        "blurb": "Down payment amount and monthly saving to reach it.",
        "meta_description": "Calculate the down payment you need for a home at any percentage, plus how much to save each month to reach it by your target date.",
        "intro": "See how much you need for a home down payment — and the monthly saving that gets you there by your target. Enter the home price, your target percentage, and your timeline.",
        "fields": [
            {"id": "price", "label": "Home price ($)", "value": 350000},
            {"id": "percent", "label": "Down payment (%)", "value": 20, "step": 1},
            {"id": "saved", "label": "Already saved ($)", "value": 15000},
            {"id": "months", "label": "Months until you buy", "value": 36, "step": 1},
        ],
        "js": """
function calculate() {
  const price = val('price'), pct = val('percent')/100, saved = val('saved'), m = Math.max(1, val('months'));
  const target = price * pct;
  const closing = price * 0.03;
  const gap = Math.max(0, target - saved);
  const monthly = gap / m;
  show(`<div class="result-main">$${fmt(target,0)}<small>${val('percent')}% down payment on a $${fmt(price,0)} home</small></div>
  <table>
    <tr><td>Still to save</td><td>$${fmt(gap,0)}</td></tr>
    <tr><td>Save per month (${m} mo)</td><td>$${fmt(monthly,0)}</td></tr>
    <tr><td>Est. closing costs (~3%)</td><td>$${fmt(closing,0)} extra</td></tr>
    <tr><td>Total cash needed to buy</td><td>$${fmt(target + closing,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How much down payment do you need?</h2>
<p>The classic target is <strong>20% of the home price</strong>, because it lets you avoid private mortgage insurance (PMI) in many markets and secures better loan terms. But it's not mandatory — many first-time buyers put down far less (often 5–10%), accepting PMI and a larger loan in exchange for buying sooner. This calculator works for any percentage so you can compare scenarios.</p>
<h2>Don't forget closing costs</h2>
<p>The down payment isn't the only cash you need at the table. <strong>Closing costs</strong> — lender fees, title, appraisal, taxes, and more — typically add 2–5% of the price (this tool estimates 3%). On a $350,000 home that's around $10,500 on top of the down payment. Budgeting only for the down payment is a common way buyers get caught short right before closing.</p>
<h2>20% vs less: the real trade-off</h2>
<ul>
<li><strong>20% down:</strong> no PMI, smaller loan, lower monthly payment, more equity from day one — but it takes longer to save and ties up more cash.</li>
<li><strong>Less than 20%:</strong> buy sooner and keep cash liquid, but pay PMI (often 0.5–1.5% of the loan yearly) and carry a bigger balance.</li>
</ul>
<p>A balanced approach many advisors favor: arrive with a solid down payment <em>and</em> a preserved emergency fund, rather than draining every dollar into equity you can't easily access. Home equity doesn't fix a broken furnace — cash does.</p>
<h2>Saving the gap</h2>
<p>Once you know the monthly figure, automate it into a separate high-yield savings account so it grows a little while you save and stays out of spending reach. Windfalls — bonuses, tax refunds, gifts — are down-payment accelerators precisely because they were never in your monthly budget.</p>
""",
        "faqs": [
            ("Do I really need 20% down?", "No, but it helps. 20% avoids PMI and improves your rate. Many buyers put down less and pay PMI to buy sooner — a valid choice if you keep an emergency fund and can afford the higher payment."),
            ("What are closing costs?", "Fees paid at the completion of a home purchase — lender charges, title, appraisal, taxes, and more — typically 2–5% of the price. They're separate from and on top of your down payment."),
            ("Where should I keep my down payment savings?", "In a safe, liquid, interest-bearing account like a high-yield savings account — not the stock market, since a downturn right before you buy could shrink the funds you're counting on."),
        ],
    },
    {
        "slug": "mortgage-refinance-calculator",
        "emoji": "\U0001F504",
        "category": "Mortgages & Home",
        "title": "Refinance Calculator — Should You Refinance Your Mortgage?",
        "h1": "Mortgage Refinance Calculator",
        "blurb": "Monthly savings and break-even point of refinancing.",
        "meta_description": "See if refinancing your mortgage is worth it: compare your current payment to a new one, and find the break-even point where closing costs are recovered.",
        "intro": "Refinancing can lower your payment — but closing costs mean it only pays off if you stay long enough to recover them. Enter your current loan and the new offer to see your monthly savings and break-even point.",
        "fields": [
            {"id": "balance", "label": "Remaining loan balance ($)", "value": 250000},
            {"id": "current_pmt", "label": "Current monthly payment (P&I) ($)", "value": 1580},
            {"id": "new_rate", "label": "New interest rate (%)", "value": 5.5, "step": 0.05},
            {"id": "new_years", "label": "New loan term (years)", "value": 30, "step": 1},
            {"id": "closing", "label": "Refinance closing costs ($)", "value": 5000},
        ],
        "js": """
function calculate() {
  const b = val('balance'), cur = val('current_pmt'), r = val('new_rate')/100, y = val('new_years'), cost = val('closing');
  const i = r/12, n = y*12;
  const newPmt = i>0 ? b*i/(1-Math.pow(1+i,-n)) : b/n;
  const savings = cur - newPmt;
  if (savings <= 0) {
    show(`<div class="result-main">$${fmt(newPmt)} / mo new payment<small>This refinance does not lower your monthly payment (it may still shorten your term).</small></div>`);
    return;
  }
  const breakeven = cost / savings;
  show(`<div class="result-main">$${fmt(savings)} / month saved<small>New payment $${fmt(newPmt)} vs current $${fmt(cur)}</small></div>
  <table>
    <tr><td>Break-even point</td><td>${fmt(breakeven,1)} months (${fmt(breakeven/12,1)} yrs)</td></tr>
    <tr><td>Savings in year 1 (after costs)</td><td>$${fmt(savings*12 - cost,0)}</td></tr>
    <tr><td>Savings over 5 years</td><td>$${fmt(savings*60 - cost,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The refinance decision in one number</h2>
<p>Refinancing replaces your existing mortgage with a new one — usually to grab a lower rate and shrink your payment. But it isn't free: closing costs (often $3,000–$6,000) apply just like a new purchase. The question that decides everything is the <strong>break-even point</strong>: how many months of savings it takes to recover those costs. <code>Break-even = closing costs ÷ monthly savings.</code></p>
<h2>The rule of thumb</h2>
<p>If you'll stay in the home <em>well beyond</em> the break-even point, refinancing usually makes sense. If you might move or sell before then, you'd pay the closing costs without recouping them — a losing trade. A refinance that saves $200/month with $5,000 of costs breaks even at 25 months; stay five years and you're roughly $7,000 ahead, but sell in 18 months and you've lost money.</p>
<h2>Beyond the monthly payment</h2>
<ul>
<li><strong>Watch the term reset.</strong> Refinancing a 30-year loan you're 6 years into back to a fresh 30 years lowers the payment but can increase <em>total</em> interest by stretching the loan to 36 years overall. A lower rate helps; a longer term hurts.</li>
<li><strong>Shortening the term</strong> (e.g. 30→15 years) often barely changes — or raises — the payment while saving enormous interest and building equity faster.</li>
<li><strong>Cash-out refinancing</strong> lets you borrow against equity, but increases your balance and payment; treat it as taking on new debt, not "free money."</li>
</ul>
<h2>When to seriously consider it</h2>
<p>The old guideline was to refinance when rates drop about 1% below your current rate, but the honest test is simply whether the break-even point comfortably fits inside how long you'll stay. Run your real numbers, confirm the closing costs, and make sure a lower payment isn't quietly costing you more interest over a longer term.</p>
""",
        "faqs": [
            ("What is the break-even point on a refinance?", "The number of months of payment savings needed to recover the closing costs. If you'll stay in the home longer than the break-even, refinancing generally pays off; if not, it doesn't."),
            ("Does refinancing reset my loan term?", "Usually yes — a new mortgage starts a fresh term. That lowers the payment but can increase total interest if it extends how long you'll be paying. Compare total interest, not just the monthly figure."),
            ("How much does refinancing cost?", "Closing costs typically run 2–5% of the loan amount — commonly $3,000–$6,000 — covering lender fees, appraisal, title, and taxes. These are central to the break-even calculation."),
        ],
    },
    {
        "slug": "overtime-pay-calculator",
        "emoji": "\u23F0",
        "category": "Salary & Work",
        "title": "Overtime Pay Calculator — Time-and-a-Half and Total Pay",
        "h1": "Overtime Pay Calculator",
        "blurb": "Total weekly pay including overtime at any multiplier.",
        "meta_description": "Calculate overtime pay at time-and-a-half (or any multiplier) and your total weekly earnings from regular and overtime hours.",
        "intro": "Work out your overtime earnings and total weekly pay. Enter your regular hourly rate, the hours you worked, and the overtime multiplier (1.5× is standard time-and-a-half).",
        "fields": [
            {"id": "rate", "label": "Regular hourly rate ($)", "value": 20, "step": 0.5},
            {"id": "regular", "label": "Regular hours", "value": 40, "step": 0.5},
            {"id": "ot", "label": "Overtime hours", "value": 8, "step": 0.5},
            {"id": "mult", "label": "Overtime multiplier", "value": 1.5, "step": 0.1, "hint": "1.5 = time-and-a-half, 2 = double time"},
        ],
        "js": """
function calculate() {
  const rate = val('rate'), reg = val('regular'), ot = val('ot'), mult = val('mult');
  const regPay = rate * reg;
  const otRate = rate * mult;
  const otPay = otRate * ot;
  const total = regPay + otPay;
  show(`<div class="result-main">$${fmt(total)}<small>Total weekly pay (${reg}h regular + ${ot}h overtime)</small></div>
  <table>
    <tr><td>Regular pay</td><td>$${fmt(regPay)}</td></tr>
    <tr><td>Overtime rate (${mult}x)</td><td>$${fmt(otRate)}/hr</td></tr>
    <tr><td>Overtime pay</td><td>$${fmt(otPay)}</td></tr>
    <tr><td>Annualized (52 weeks)</td><td>$${fmt(total*52,0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>How overtime pay works</h2>
<p>Overtime is paid at a premium above your regular rate. The most common is <strong>time-and-a-half (1.5×)</strong>: an extra 50% for each overtime hour. Some situations pay <strong>double time (2×)</strong> — holidays, excessive hours, or certain union agreements. Your overtime pay is simply <code>regular rate × multiplier × overtime hours</code>, added to your regular pay.</p>
<h2>When does overtime kick in?</h2>
<p>Rules vary by country and region. In the US, federal law generally requires time-and-a-half for hours worked beyond 40 in a week for non-exempt employees; some states add daily overtime (e.g. beyond 8 hours in a day). Salaried "exempt" employees often don't qualify. Always check your local labour laws and employment contract — this calculator handles the math once you know your rules and multiplier.</p>
<h2>The value of overtime hours</h2>
<p>Overtime is one of the few ways an hourly worker earns a premium rate, which is why it can meaningfully boost income. At $20/hour, eight overtime hours at 1.5× adds $240 — a 30% bump on top of a $800 regular week. But weigh it against the real cost: fatigue, lost personal time, and (in progressive tax systems) a slightly higher marginal tax rate on the extra income. Overtime is valuable; unlimited overtime is often a sign a role is understaffed.</p>
<h2>A tax note</h2>
<p>Overtime pay isn't taxed at a special higher rate — it's ordinary income. It can <em>appear</em> to be taxed more if a big overtime week pushes that paycheck into higher withholding, but at year-end it's all reconciled as normal income. The figures here are gross (pre-tax); your take-home depends on your tax situation.</p>
""",
        "faqs": [
            ("What is time-and-a-half?", "Overtime paid at 1.5 times your regular hourly rate. If you earn $20/hour, time-and-a-half is $30/hour for each qualifying overtime hour."),
            ("Is overtime taxed more?", "No — it's taxed as ordinary income. A large overtime paycheck may have more tax withheld that week, but it's reconciled at year-end. There's no special penalty rate on overtime earnings."),
            ("When am I entitled to overtime?", "It depends on your country, region, and employment status. Many places require it beyond 40 hours a week for non-exempt employees; some add daily thresholds. Check local law and your contract."),
        ],
    },
    {
        "slug": "paycheck-calculator",
        "emoji": "\U0001F4B5",
        "category": "Salary & Work",
        "title": "Paycheck Calculator — Pay Per Period from Annual Salary",
        "h1": "Paycheck Calculator",
        "blurb": "Gross and net pay per paycheck by pay frequency.",
        "meta_description": "Convert an annual salary into per-paycheck amounts for weekly, biweekly, semimonthly or monthly pay schedules, with an optional estimate of take-home pay.",
        "intro": "Turn your annual salary into what actually lands each payday. Choose your pay frequency and, optionally, an effective tax rate to estimate net pay per paycheck.",
        "fields": [
            {"id": "salary", "label": "Annual salary ($)", "value": 65000},
            {"id": "freq", "label": "Pay frequency", "value": "biweekly", "type": "select",
             "options": [["weekly", "Weekly (52/year)"], ["biweekly", "Biweekly (26/year)"], ["semimonthly", "Semimonthly (24/year)"], ["monthly", "Monthly (12/year)"]]},
            {"id": "tax", "label": "Effective tax & deductions (%)", "value": 20, "step": 0.5, "hint": "optional, for take-home estimate"},
        ],
        "js": """
function calculate() {
  const s = val('salary'), t = val('tax')/100;
  const freq = document.getElementById('freq').value;
  const periods = {weekly:52, biweekly:26, semimonthly:24, monthly:12}[freq];
  const gross = s / periods;
  const net = gross * (1 - t);
  show(`<div class="result-main">$${fmt(gross)}<small>Gross per paycheck (${periods} paychecks/year)</small></div>
  <table>
    <tr><td>Gross per paycheck</td><td>$${fmt(gross)}</td></tr>
    <tr><td>Estimated take-home</td><td>$${fmt(net)}</td></tr>
    <tr><td>Gross per month</td><td>$${fmt(s/12)}</td></tr>
    <tr><td>Paychecks per year</td><td>${periods}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Why pay frequency matters</h2>
<p>Your annual salary is the same regardless of schedule, but the size and rhythm of each paycheck differ — and that affects budgeting. The four common schedules:</p>
<ul>
<li><strong>Weekly (52/year):</strong> smaller, frequent checks; easiest to match to weekly expenses.</li>
<li><strong>Biweekly (26/year):</strong> every two weeks — the most common in the US. Note the quirk: two months a year have <em>three</em> paychecks, a budgeting bonus if you plan for it.</li>
<li><strong>Semimonthly (24/year):</strong> twice a month (e.g. 15th and last day). Always two per month, slightly larger than biweekly.</li>
<li><strong>Monthly (12/year):</strong> one large check; requires the most disciplined budgeting to stretch across the month.</li>
</ul>
<h2>Biweekly vs semimonthly — the confusing pair</h2>
<p>They sound alike but differ: biweekly is <em>every 14 days</em> (26 checks), semimonthly is <em>twice a month</em> (24 checks). Biweekly checks are a bit smaller but there are two more of them, including those two "extra" three-paycheck months. Same annual pay, different cash-flow feel.</p>
<h2>Gross vs net</h2>
<p>The gross figure is before deductions. Real take-home is reduced by income tax, payroll/social contributions, health premiums, and retirement contributions. This tool lets you enter an effective rate for a rough net estimate, but your actual deductions depend on your location and elections. For budgeting, always plan around the net amount that hits your account — and if you're paid biweekly, consider treating the two annual "extra" paychecks as a savings or debt-payoff bonus rather than spending money.</p>
""",
        "faqs": [
            ("What's the difference between biweekly and semimonthly?", "Biweekly means every two weeks — 26 paychecks a year, with two months getting a third check. Semimonthly means twice a month — 24 paychecks, always two per month. Biweekly checks are slightly smaller but more numerous."),
            ("Why are two months bigger when I'm paid biweekly?", "Because 26 biweekly paychecks don't divide evenly into 12 months, two months each contain three paydays. Planning for these 'extra' paychecks makes them a useful savings or debt-payoff boost."),
            ("Is this my take-home pay?", "The gross figure isn't; the take-home estimate uses the effective rate you enter. Actual net pay depends on your specific taxes, benefits, and retirement contributions, which vary by location and choices."),
        ],
    },
    {
        "slug": "markup-calculator",
        "emoji": "\U0001F3F7\uFE0F",
        "category": "Business",
        "title": "Markup Calculator — Selling Price from Cost and Markup",
        "h1": "Markup Calculator",
        "blurb": "Set a selling price from cost and desired markup.",
        "meta_description": "Calculate selling price from cost and markup percentage, and see the resulting profit margin. Understand the crucial difference between markup and margin.",
        "intro": "Set a price by adding a markup to your cost — and instantly see the profit margin it produces. Enter your unit cost and the markup percentage you want to apply.",
        "fields": [
            {"id": "cost", "label": "Unit cost ($)", "value": 40},
            {"id": "markup", "label": "Markup (%)", "value": 50, "step": 1},
        ],
        "js": """
function calculate() {
  const c = val('cost'), mk = val('markup')/100;
  const profit = c * mk;
  const price = c + profit;
  const margin = price>0 ? profit/price*100 : 0;
  show(`<div class="result-main">$${fmt(price)}<small>Selling price at ${val('markup')}% markup</small></div>
  <table>
    <tr><td>Unit cost</td><td>$${fmt(c)}</td></tr>
    <tr><td>Profit per unit</td><td>$${fmt(profit)}</td></tr>
    <tr><td>Resulting profit margin</td><td>${fmt(margin,1)}%</td></tr>
    <tr><td>Markup applied</td><td>${val('markup')}%</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Markup and margin are not the same</h2>
<p>This is the single most costly confusion in pricing. <strong>Markup</strong> is profit as a percentage of <em>cost</em>; <strong>margin</strong> is profit as a percentage of the <em>selling price</em>. A 50% markup on a $40 cost gives a $60 price — but that's only a 33% margin, because the $20 profit is one-third of the $60 price, not half. Every markup produces a smaller-looking margin, and mixing them up quietly erodes profitability.</p>
<h2>Setting price from markup</h2>
<p><code>Price = Cost × (1 + markup)</code>. Retailers often think in markup because they buy at a cost and add a percentage. "Keystone" pricing — a 100% markup (doubling the cost) — is a traditional retail default that produces a 50% margin. This calculator shows both numbers so you always know the margin your markup actually delivers.</p>
<h2>Choosing a markup</h2>
<ul>
<li><strong>Cover more than product cost.</strong> Your markup must fund not just profit but overhead — rent, salaries, marketing, returns. A markup that only beats unit cost can still lose money once fixed costs are counted.</li>
<li><strong>Match your industry.</strong> Grocery runs on thin markups and high volume; jewelry, software, and specialty goods carry much higher ones. Compare to your sector, not a universal figure.</li>
<li><strong>Mind competition and value.</strong> Markup sets a floor; what customers will pay sets the ceiling. Price within that band.</li>
</ul>
<h2>From price to profit</h2>
<p>Remember that gross profit per unit still has to cover all your fixed costs before anything is true profit — see the <a href="/calculators/break-even-point-calculator/">break-even calculator</a> for how many units that takes. And if you prefer to work backwards from a target margin instead of a markup, the <a href="/calculators/profit-margin-calculator/">profit margin calculator</a> handles that direction.</p>
""",
        "faqs": [
            ("What's the difference between markup and margin?", "Markup is profit as a percentage of cost; margin is profit as a percentage of selling price. A 50% markup equals a 33% margin. Confusing them leads to underpricing."),
            ("How do I convert markup to margin?", "Margin = markup ÷ (1 + markup). A 50% markup gives 0.5 ÷ 1.5 = 33% margin. This calculator shows both automatically so you don't have to."),
            ("What is keystone pricing?", "Doubling the cost — a 100% markup, which is a 50% margin. It's a traditional retail starting point, though competitive or specialty markets often use higher or lower markups."),
        ],
    },
    {
        "slug": "cac-ltv-calculator",
        "emoji": "\U0001F3AF",
        "category": "Business & Self-Employment",
        "title": "LTV:CAC Ratio Calculator — Customer Economics",
        "h1": "LTV : CAC Ratio Calculator",
        "blurb": "Lifetime value vs acquisition cost — is growth healthy?",
        "meta_description": "Calculate customer lifetime value (LTV), customer acquisition cost (CAC), and the LTV:CAC ratio that tells you whether your growth is profitable and sustainable.",
        "intro": "For any subscription or repeat-purchase business, one ratio reveals whether growth is healthy: lifetime value versus what it costs to acquire a customer. Enter your numbers to get LTV, CAC and the ratio investors look for.",
        "fields": [
            {"id": "revenue", "label": "Average revenue per customer / month ($)", "value": 50},
            {"id": "margin", "label": "Gross margin (%)", "value": 80, "step": 1, "hint": "share of revenue that's profit"},
            {"id": "months", "label": "Average customer lifespan (months)", "value": 24, "step": 1},
            {"id": "spend", "label": "Total sales & marketing spend ($)", "value": 20000},
            {"id": "customers", "label": "New customers acquired", "value": 100, "step": 1},
        ],
        "js": """
function calculate() {
  const rev = val('revenue'), gm = val('margin')/100, life = val('months');
  const spend = val('spend'), cust = Math.max(1, val('customers'));
  const ltv = rev * gm * life;
  const cac = spend / cust;
  const ratio = cac>0 ? ltv/cac : 0;
  const payback = (rev*gm)>0 ? cac/(rev*gm) : 0;
  let verdict;
  if (ratio >= 3 && ratio <= 5) verdict = 'Healthy — the classic 3–5x sweet spot';
  else if (ratio > 5) verdict = 'Very high — you may be under-investing in growth';
  else if (ratio >= 1) verdict = 'Weak — each customer barely pays back acquisition';
  else verdict = 'Unprofitable — you lose money on every customer';
  show(`<div class="result-main">${fmt(ratio,1)} : 1<small>LTV to CAC ratio &mdash; ${verdict}</small></div>
  <table>
    <tr><td>Customer lifetime value (LTV)</td><td>$${fmt(ltv)}</td></tr>
    <tr><td>Customer acquisition cost (CAC)</td><td>$${fmt(cac)}</td></tr>
    <tr><td>CAC payback period</td><td>${fmt(payback,1)} months</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>The two numbers that decide a subscription business</h2>
<p><strong>LTV (lifetime value)</strong> is the total gross profit a customer generates before they leave: <code>monthly revenue × gross margin × average lifespan</code>. <strong>CAC (customer acquisition cost)</strong> is what you spend on sales and marketing to win one customer: <code>total spend ÷ new customers</code>. Together they answer the only question that matters for growth: does each customer bring in more than they cost to acquire?</p>
<h2>The 3:1 rule</h2>
<p>The widely-cited benchmark is an <strong>LTV:CAC ratio around 3:1 to 5:1</strong>. Below 3, you're spending too much relative to what customers are worth — growth burns cash. Above 5, counterintuitively, you may be <em>under-investing</em>: you could likely spend more to acquire customers faster and still profit. Exactly 1:1 means each customer just barely pays back their acquisition cost, leaving nothing for overhead or profit.</p>
<h2>Payback period: the cash-flow reality</h2>
<p>A great ratio can still strain cash if it takes too long to recover CAC. The <strong>CAC payback period</strong> — months of gross profit needed to earn back acquisition cost — should ideally be under 12 months for a healthy startup. A 3:1 ratio with a 3-month payback is a money machine; the same ratio with a 30-month payback can bankrupt you before the value arrives, because you fund acquisition today and collect slowly.</p>
<h2>Improving the ratio</h2>
<ul>
<li><strong>Raise LTV:</strong> reduce churn (longer lifespan is the biggest lever), increase prices, or expand revenue per customer through upsells.</li>
<li><strong>Lower CAC:</strong> improve conversion, lean on organic and referral channels, and target higher-intent audiences.</li>
<li><strong>Watch churn above all</strong> — because LTV multiplies by lifespan, cutting churn compounds through the whole model.</li>
</ul>
<p>These unit economics are what separate a business that grows profitably from one that simply buys revenue at a loss. Get the ratio and payback right, and scaling makes you money; get them wrong, and scaling accelerates the losses.</p>
""",
        "faqs": [
            ("What is a good LTV:CAC ratio?", "Around 3:1 to 5:1 is the healthy benchmark. Below 3 suggests you're overspending to acquire customers; above 5 may mean you're under-investing and could grow faster."),
            ("What is CAC payback period?", "The number of months of gross profit from a customer needed to recover their acquisition cost. Under 12 months is a common target for healthy, cash-efficient growth."),
            ("How do I calculate customer lifetime value?", "A simple version: average monthly revenue × gross margin × average customer lifespan in months. More advanced models discount future value and account for expansion revenue, but this captures the core."),
        ],
    },
    {
        "slug": "percentage-calculator",
        "emoji": "\U0001F522",
        "category": "Everyday Math",
        "title": "Percentage Calculator — Percent Of, Is What Percent, and % Change",
        "h1": "Percentage Calculator",
        "blurb": "Three everyday percentage questions in one tool.",
        "meta_description": "A simple percentage calculator: find X% of a number, work out what percent one number is of another, or calculate the percentage increase or decrease between two values.",
        "intro": "The three percentage questions everyone actually needs, in one place. Pick the type, enter two numbers, and get a clear answer with the working shown.",
        "fields": [
            {"id": "mode", "label": "What do you want to calculate?", "value": "of", "type": "select",
             "options": [["of", "What is X% of Y"], ["ispct", "X is what % of Y"], ["change", "% change from X to Y"]]},
            {"id": "a", "label": "First number (X)", "value": 25},
            {"id": "b", "label": "Second number (Y)", "value": 200},
        ],
        "js": """
function calculate() {
  const mode = document.getElementById('mode').value, a = val('a'), b = val('b');
  if (mode === 'of') {
    const res = a/100 * b;
    show(`<div class="result-main">${fmt(res)}<small>${fmt(a)}% of ${fmt(b)}</small></div>
    <table><tr><td>Calculation</td><td>${fmt(a)} ÷ 100 × ${fmt(b)}</td></tr><tr><td>Result</td><td>${fmt(res)}</td></tr></table>`);
  } else if (mode === 'ispct') {
    if (b === 0) { show('<div class="result-main">Y can\\'t be zero for this.</div>'); return; }
    const res = a/b*100;
    show(`<div class="result-main">${fmt(res)}%<small>${fmt(a)} is ${fmt(res)}% of ${fmt(b)}</small></div>
    <table><tr><td>Calculation</td><td>${fmt(a)} ÷ ${fmt(b)} × 100</td></tr><tr><td>Result</td><td>${fmt(res)}%</td></tr></table>`);
  } else {
    if (a === 0) { show('<div class="result-main">Starting value can\\'t be zero for % change.</div>'); return; }
    const diff = b - a, res = diff/Math.abs(a)*100;
    show(`<div class="result-main">${res>=0?'+':''}${fmt(res)}%<small>change from ${fmt(a)} to ${fmt(b)} (${diff>=0?'increase':'decrease'})</small></div>
    <table><tr><td>Difference</td><td>${fmt(diff)}</td></tr><tr><td>Calculation</td><td>(${fmt(b)} − ${fmt(a)}) ÷ ${fmt(a)} × 100</td></tr></table>`);
  }
}
""",
        "body_html": """
<h2>The three percentage questions</h2>
<p>Almost every real percentage problem is one of three types, and this calculator covers all of them:</p>
<ul>
<li><strong>What is X% of Y?</strong> — finding a portion. 25% of 200 is 50. Formula: <code>X ÷ 100 × Y</code>. Use it for discounts, tips, tax, and commissions.</li>
<li><strong>X is what percent of Y?</strong> — expressing a part as a percentage. 25 out of 200 is 12.5%. Formula: <code>X ÷ Y × 100</code>. Use it for test scores, market share, and progress toward a goal.</li>
<li><strong>Percentage change from X to Y</strong> — measuring growth or decline. From 200 to 250 is a +25% increase. Formula: <code>(Y − X) ÷ X × 100</code>. Use it for price changes, investment returns, and any before-and-after comparison.</li>
</ul>
<h2>The mistake to avoid: percentage points vs percent</h2>
<p>A rate rising from 5% to 6% is a <em>1 percentage point</em> increase — but a <em>20% increase</em> in relative terms. News and marketing exploit this ambiguity constantly. "Approval rose 3 points" and "approval rose 3%" can mean very different things. When a percentage is itself changing, be clear whether you mean the absolute point difference or the relative percent change.</p>
<h2>Why percentage change uses the starting value</h2>
<p>Percentage change is always measured against the <em>original</em> number, which creates an asymmetry people forget: a value that drops 50% must then rise 100% to recover, because the base shrank. A $100 stock that falls to $50 (−50%) needs a +100% gain to return to $100. This is why big losses hurt disproportionately — and why "up 50%, down 50%" leaves you down 25%, not even.</p>
""",
        "faqs": [
            ("How do I find what percent one number is of another?", "Divide the part by the whole and multiply by 100. For example, 25 out of 200 is 25 ÷ 200 × 100 = 12.5%. Use the 'X is what % of Y' mode above."),
            ("What's the difference between percent and percentage points?", "Percentage points measure the absolute gap between two percentages (5% to 6% is 1 point). Percent change measures it relative to the start (5% to 6% is a 20% increase). They're easily and often confused."),
            ("Why does a 50% loss need a 100% gain to recover?", "Because percentage change is measured against the current (reduced) value. Falling 50% halves your money; getting back to the start means doubling what remains, which is a 100% gain."),
        ],
    },
]
