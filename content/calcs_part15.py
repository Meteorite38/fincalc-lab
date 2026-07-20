# -*- coding: utf-8 -*-
"""Batch 13 calculators: time to save a goal, commute cost."""

PART15 = [
    {
        "slug": "time-to-save-calculator",
        "emoji": "\u23F3",
        "category": "Savings & Investing",
        "title": "Time to Save Calculator — How Long to Reach Your Goal",
        "h1": "Time to Save Calculator",
        "blurb": "How long a monthly amount takes to reach a target.",
        "meta_description": "Find out how long it will take to reach a savings goal given how much you save each month, what you've already saved, and your expected return.",
        "intro": "Know how much you can save each month and want to know when you'll hit your target? Enter the numbers to see how long it takes — including the boost from interest.",
        "fields": [
            {"id": "target", "label": "Savings goal ($)", "value": 30000},
            {"id": "current", "label": "Already saved ($)", "value": 5000},
            {"id": "monthly", "label": "Monthly saving ($)", "value": 500},
            {"id": "rate", "label": "Annual return / interest (%)", "value": 4, "step": 0.1},
        ],
        "js": """
function calculate() {
  const target = val('target'), P = val('current'), pmt = val('monthly'), i = val('rate')/100/12;
  if (P >= target) { show(`<div class="result-main">Already there \\u2705<small>Your current savings already meet the $${fmt(target,0)} goal</small></div>`); return; }
  if (pmt <= 0 && i <= 0) { show('<div class="result-main">Enter a monthly saving above zero.</div>'); return; }
  let bal = P, months = 0, contributed = P;
  while (bal < target && months < 1200) { bal = bal*(1+i) + pmt; contributed += pmt; months++; }
  if (months >= 1200) { show('<div class="result-main">Over 100 years<small>Increase your monthly saving to reach the goal in a realistic time</small></div>'); return; }
  const yrs = Math.floor(months/12), mo = months%12;
  const totalContrib = P + pmt*months;
  show(`<div class="result-main">${yrs} year${yrs==1?'':'s'} ${mo} month${mo==1?'':'s'}<small>to reach $${fmt(target,0)} saving $${fmt(pmt,0)}/month</small></div>
  <table>
    <tr><td>Target date</td><td>${months} months from now</td></tr>
    <tr><td>Total you'll contribute</td><td>$${fmt(totalContrib,0)}</td></tr>
    <tr><td>Interest earned along the way</td><td>$${fmt(Math.max(0,target-totalContrib),0)}</td></tr>
  </table>`);
}
""",
        "body_html": """
<h2>Two ways to plan a savings goal</h2>
<p>There are two questions you can ask about any savings goal. "How much per month to hit it by a deadline?" is answered by our <a href="/calculators/savings-goal-calculator/">savings goal calculator</a>. This tool answers the other one: <strong>"I can save $X a month — when will I get there?"</strong> Both are useful; this one fits when your monthly amount is fixed and you want a realistic timeline.</p>
<h2>How it works</h2>
<p>The calculator grows your balance month by month: each month your existing savings earn a little interest, then your contribution is added. It counts the months until you cross your target. Because interest compounds along the way, you reach the goal a bit sooner than simple division would suggest — and the longer the goal, the more interest helps.</p>
<h2>Using the result</h2>
<ul>
<li><strong>Too far away?</strong> You have three levers: save more per month, lower the target, or (for long-term goals) accept more risk for a higher return. Even small increases to the monthly amount pull the date closer.</li>
<li><strong>Match the account to the timeline.</strong> For a short goal (a year or two), keep the money in safe, liquid savings — don't gamble it in the market. For long horizons, investing for growth shortens the timeline meaningfully.</li>
<li><strong>Automate it.</strong> Set up an automatic transfer of the monthly amount on payday so the timeline actually happens rather than slipping.</li>
</ul>
<h2>The power of the monthly habit</h2>
<p>Seeing a concrete finish date turns a vague "someday" into a plan you can act on and track. And notice the interest line: over longer goals, compounding quietly does a growing share of the work, which is the whole argument for starting now rather than waiting — the <a href="/calculators/compound-interest-calculator/">compound interest calculator</a> makes the gap between a start-now and a start-later plan explicit.</p>
""",
        "faqs": [
            ("How long will it take to reach my savings goal?", "It depends on your target, what you've already saved, how much you add each month, and your return. This calculator simulates the growth month by month and shows the exact time to reach the goal, including compounding."),
            ("How can I reach my goal faster?", "Save more each month, lower the target, or earn a higher return (which for long-term goals usually means investing rather than holding cash). Automating the monthly transfer ensures the plan actually happens."),
            ("Should I invest my savings to get there sooner?", "For long-term goals (5+ years), investing for growth can shorten the timeline. For short-term goals, keep the money safe and liquid — the risk of a market drop right before you need it outweighs the potential gain."),
        ],
    },
    {
        "slug": "commute-cost-calculator",
        "emoji": "\U0001F697",
        "category": "Cars & Commuting",
        "title": "Commute Cost Calculator — The Real Price of Getting to Work",
        "h1": "Commute Cost Calculator",
        "blurb": "Yearly cost of commuting, including the value of your time.",
        "meta_description": "Calculate the true annual cost of your commute — fuel or transit, parking, and even the value of the time it takes — to compare jobs, homes and remote work.",
        "intro": "Your commute costs more than gas. Enter your daily travel to see the yearly cost in money — and optionally in the value of your time — so you can compare jobs, homes, or remote work fairly.",
        "fields": [
            {"id": "dailycost", "label": "Daily travel cost ($)", "value": 12, "hint": "fuel + tolls, or transit fare"},
            {"id": "parking", "label": "Parking per day ($)", "value": 5},
            {"id": "daysweek", "label": "Commute days per week", "value": 5, "step": 1},
            {"id": "weeks", "label": "Working weeks per year", "value": 48, "step": 1},
            {"id": "minutes", "label": "Round-trip commute (minutes/day)", "value": 60, "step": 5},
            {"id": "wage", "label": "Your hourly wage ($, for time value)", "value": 30, "hint": "0 to ignore time value"},
        ],
        "js": """
function calculate() {
  const daily = val('dailycost'), parking = val('parking'), dpw = val('daysweek'), weeks = val('weeks');
  const mins = val('minutes'), wage = val('wage');
  const daysYear = dpw * weeks;
  const moneyCost = (daily + parking) * daysYear;
  const hoursYear = mins/60 * daysYear;
  const timeValue = hoursYear * wage;
  let rows = `<tr><td>Commute days per year</td><td>${fmt(daysYear,0)}</td></tr>
    <tr><td>Out-of-pocket cost per year</td><td>$${fmt(moneyCost,0)}</td></tr>
    <tr><td>Per month</td><td>$${fmt(moneyCost/12,0)}</td></tr>
    <tr><td>Hours spent commuting per year</td><td>${fmt(hoursYear,0)} hrs (${fmt(hoursYear/24,1)} full days)</td></tr>`;
  if (wage > 0) rows += `<tr><td>Value of that time</td><td>$${fmt(timeValue,0)}</td></tr>
    <tr><td>Total cost incl. time</td><td>$${fmt(moneyCost + timeValue,0)}</td></tr>`;
  show(`<div class="result-main">$${fmt(moneyCost,0)} / year<small>Out-of-pocket commuting cost${wage>0 ? ' \\u00b7 $'+fmt(moneyCost+timeValue,0)+' including the value of your time' : ''}</small></div><table>${rows}</table>`);
}
""",
        "body_html": """
<h2>Your commute is a hidden expense</h2>
<p>Commuting quietly consumes both money and time, yet most people never add it up. Between fuel or transit fares, tolls, parking, and the hours themselves, a daily commute can cost thousands of dollars and hundreds of hours a year — a major factor that rarely makes it into job or housing decisions. This calculator makes the full cost visible.</p>
<h2>Counting the money and the time</h2>
<p>The out-of-pocket cost is straightforward: daily travel plus parking, times commuting days per year. A $17/day commute over 240 days is about $4,080 a year — real money that comes straight out of your take-home pay. But the bigger cost is often <strong>time</strong>: a one-hour daily round trip is roughly 240 hours a year, or ten full 24-hour days. Valued at even a modest hourly wage, that time is worth thousands more.</p>
<h2>Where this changes decisions</h2>
<ul>
<li><strong>Comparing job offers.</strong> A higher salary with a long, expensive commute can pay <em>less</em> in real, after-commute terms than a closer job — factor the commute cost into the offer, alongside the effect on your true <a href="/calculators/salary-to-hourly-calculator/">hourly rate</a>.</li>
<li><strong>Choosing where to live.</strong> The cheaper home far from work often isn't cheaper once you add years of commuting cost and time. Weigh the rent or price saving against the commute it creates.</li>
<li><strong>Valuing remote or hybrid work.</strong> Cutting a commute two or three days a week is a real, tax-free raise plus reclaimed time — this tool quantifies exactly how much.</li>
</ul>
<h2>Money isn't the only cost</h2>
<p>Beyond dollars and hours, long commutes carry well-documented costs to health, stress, and life satisfaction. When you see the annual figure — in money <em>and</em> in days of your life — a shorter commute, a move, or negotiating remote days often looks far more valuable than it first appears. Put a number on it, and you can make the trade-off deliberately instead of absorbing it invisibly.</p>
""",
        "faqs": [
            ("How much does commuting really cost?", "Add up daily fuel or transit and parking across your commuting days per year for the out-of-pocket cost, then add the value of the time spent. A typical car commute can easily cost several thousand dollars and hundreds of hours a year."),
            ("Should I include the value of my time?", "Yes, if you want the full picture. Commuting time is time you can't use for work, rest, or family. Valuing it at your hourly wage (or what your time is worth to you) often reveals that time is the biggest commuting cost of all."),
            ("How does this help me compare jobs?", "A higher-paying job with a long, costly commute may deliver less real value than a closer, lower-paying one once you subtract commuting money and time. Comparing total commute cost puts offers on an honest, like-for-like footing."),
        ],
    },
]
