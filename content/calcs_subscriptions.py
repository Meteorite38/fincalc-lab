# -*- coding: utf-8 -*-
"""Subscription audit — itemized monthly stack, annual total, 10-year invested opportunity cost, keep/kill scenario."""

SUBSCRIPTIONS = [
    {
        "slug": "subscription-cost-calculator",
        "emoji": "\U0001F4F1",
        "category": "Budgeting & Life",
        "title": "Subscription Cost Calculator — What the Stack Really Costs You",
        "h1": "Subscription Cost Calculator",
        "blurb": "Your subscription stack's yearly bill, its 10-year invested cost, and what trimming half buys.",
        "meta_description": "Free subscription audit calculator: add up streaming, music, fitness, cloud, delivery and app subscriptions — see the annual total, the 10-year opportunity cost if invested instead, and what cutting the unused half is actually worth.",
        "intro": "No single subscription hurts — that's the design. $12 here, $16 there, each canceling-eligible any time and therefore never canceled. Stack eight of them and the drip becomes a four-figure annual bill on autopilot. This calculator totals your stack, prices it over a decade, and shows what auditing the bottom half is worth.",
        "fields": [
            {"id": "video", "label": "Video streaming ($/mo)", "value": 35, "hint": "Netflix + Disney + Max + ... — count them all"},
            {"id": "music", "label": "Music & audio ($/mo)", "value": 12, "hint": "Spotify, Audible, podcasts"},
            {"id": "fitness", "label": "Fitness & wellness ($/mo)", "value": 30, "hint": "gym, apps, classes"},
            {"id": "cloud", "label": "Cloud, software & AI tools ($/mo)", "value": 20, "hint": "storage, Office, password manager, AI"},
            {"id": "delivery", "label": "Delivery & shopping memberships ($/mo)", "value": 25, "hint": "Prime, DoorDash, meal kits"},
            {"id": "gaming", "label": "Gaming & entertainment ($/mo)", "value": 10},
            {"id": "other", "label": "Everything else ($/mo)", "value": 15, "hint": "news, dating, apps you forgot"},
            {"id": "ret", "label": "Investment return for comparison (%/yr)", "value": 7, "step": 0.1},
            {"id": "cutpct", "label": "Share you could cut without missing it (%)", "value": 40, "step": 5},
        ],
        "js": """
function calculate() {
  const cats = ['video','music','fitness','cloud','delivery','gaming','other'];
  const labels = {video:'Video streaming', music:'Music & audio', fitness:'Fitness & wellness', cloud:'Cloud, software & AI', delivery:'Delivery & memberships', gaming:'Gaming & entertainment', other:'Everything else'};
  let mo = 0, rows = '';
  const vals = {};
  cats.forEach(c => { vals[c] = Math.max(0, val(c)); mo += vals[c]; });
  if (mo <= 0) { show('<div class="result-main">Enter at least one subscription.</div>'); return; }
  const sorted = cats.filter(c => vals[c] > 0).sort((a,b) => vals[b] - vals[a]);
  sorted.forEach(c => { rows += `<tr><td>${labels[c]}</td><td>$${fmt(vals[c],0)}/mo</td><td>$${fmt(vals[c]*12,0)}/yr</td></tr>`; });
  const yr = mo * 12;
  const r = val('ret')/100/12, n = 120;
  const fv10 = r > 0 ? mo * ((Math.pow(1+r,n)-1)/r) : mo * n;
  const cut = Math.min(100, Math.max(0, val('cutpct')))/100;
  const cutMo = mo * cut;
  const cutFv = r > 0 ? cutMo * ((Math.pow(1+r,n)-1)/r) : cutMo * n;
  show(`<div class="result-main">$${fmt(yr,0)}/year<small>$${fmt(mo,0)}/month across the stack &middot; kept for 10 years, that's <strong>$${fmt(fv10,0)}</strong> of forgone wealth at ${fmt(val('ret'),1)}%</small></div>
  <table>
    <tr><th>Category</th><th>Monthly</th><th>Yearly</th></tr>
    ${rows}
    <tr><td><strong>Total</strong></td><td><strong>$${fmt(mo,0)}</strong></td><td><strong>$${fmt(yr,0)}</strong></td></tr>
  </table>
  <table>
    <tr><td>Cut the ${fmt(cut*100,0)}% you wouldn't miss</td><td>frees $${fmt(cutMo,0)}/mo &middot; $${fmt(cutMo*12,0)}/yr</td></tr>
    <tr><td>That slice invested for 10 years</td><td><strong>$${fmt(cutFv,0)}</strong></td></tr>
    <tr><td>Hours of work the stack costs at $25/hr (after tax)</td><td>~${fmt(yr/25,0)} hours/year — ${fmt(yr/25/8,1)} working days</td></tr>
  </table>
  <p>The audit question isn't \"is this worth $${fmt(12,0)}?\" — everything is worth $12 in isolation. It's \"which of these did I actually use in the last 30 days?\" Cancel the rest today; anything you genuinely miss can be re-subscribed in ninety seconds, which is exactly why canceling is so safe.</p>`);
}
""",
        "body_html": """
<h2>Why subscription spending is invisible by design</h2>
<p>Subscriptions weaponize three biases at once. <strong>Small-number framing:</strong> $14.99 never triggers the mental alarm a $180 annual bill would — which is the same purchase. <strong>Default persistence:</strong> canceling requires an action; continuing requires nothing, so the default wins for years past the last use. <strong>Loss aversion at cancel time:</strong> the moment you consider canceling, you imagine the one week you might want it — so the median household pays for roughly <em>double-digit</em> subscriptions while actively using half. Surveys keep finding people underestimate their subscription spend by 2-3&times; when asked to guess before counting. That gap — guessed $80, actual $190 — is precisely the money this calculator surfaces, and it's the cheapest money in your budget to reclaim because <strong>cutting it changes nothing about your life this week</strong>.</p>
<h2>The audit, operationalized</h2>
<ul>
<li><strong>Find them all:</strong> scan 90 days of card and bank statements for recurring charges (banks and card apps increasingly list \"recurring\" as a filter), plus the app-store subscription pages (iOS/Android), plus PayPal's automatic payments page — the three places forgotten trials go to live.</li>
<li><strong>Apply the 30-day test:</strong> used in the last 30 days → keep. Not used in 90 → cancel today. In between → cancel and see if you notice; re-subscribing takes ninety seconds, which makes aggressive canceling nearly risk-free.</li>
<li><strong>Rotate instead of stacking:</strong> streaming services are the classic overlap — subscribe to one at a time, binge its catalog for a month or two, swap. Half the video line for the same actual watching.</li>
<li><strong>Check annual-plan math both ways:</strong> annual billing cuts 15-40% off services you're certain about — and silently renews the ones you're not. Annual for the provable keepers, monthly for everything on probation.</li>
<li><strong>Downgrade before canceling:</strong> ad-supported tiers, family-plan splits, and student/loyalty pricing routinely halve a line item you do want to keep. Calling to cancel often triggers a retention offer — accept it and calendar the expiry.</li>
</ul>
<h2>Where the freed money should land</h2>
<p>An audit that frees $60/month only builds wealth if the money is <em>redirected on purpose</em> — otherwise it dissolves back into general spending within two cycles. Same day as the cancellations, raise an automatic transfer by the freed amount: toward the <a href="/calculators/emergency-fund-calculator/">emergency fund</a> if it's thin, the <a href="/calculators/credit-card-payoff-calculator/">card balance</a> if one exists, or the index-fund autopilot otherwise. $60/month at 7% is <a href="/calculators/compound-interest-calculator/">$10,400 in ten years</a> — from a change whose entire lifestyle cost is remembering which password streams the shows. This is the classic latte-factor logic applied where it's most defensible: not to the coffee that brings daily joy, but to the services nobody remembered paying for. (That distinction — cut the unfelt, keep the loved — is the whole <a href="/articles/value-based-spending/">value-based spending</a> playbook.)</p>
<h2>The corporate-side fine print worth knowing</h2>
<ul>
<li><strong>Price creep is the business model:</strong> major streaming services have raised prices 30-60% over the past few years, usually a couple of dollars at a time — the frog-boiling is deliberate, and each hike is a natural audit trigger.</li>
<li><strong>\"Click to cancel\" rules are improving</strong> — regulators have pushed services toward cancellation flows as easy as sign-up. If a service makes canceling genuinely hard, that's information about how they retain customers.</li>
<li><strong>Free trials want your card for a reason:</strong> the conversion event is the forgotten renewal, not the delighted user. Calendar the trial's end the minute you start it, or use virtual-card numbers that can be turned off.</li>
<li><strong>Bundles reprice the comparison:</strong> a bundle at $25 replacing $35 of separates is real savings — but only if you'd genuinely keep paying for all the parts. Bundling three services you'd otherwise cancel is a $25 loss dressed as a $10 saving.</li>
</ul>
""",
        "faqs": [
            ("How much does the average person spend on subscriptions?", "Recent surveys put the typical American household in the $200-300/month range once streaming, music, fitness, cloud storage, delivery memberships, gaming and apps are all counted — while people asked to guess before counting typically say $80-120. The 2-3× underestimate is the headline finding, and it's why a statement-scan audit almost always finds money."),
            ("What's the easiest way to find all my subscriptions?", "Three sweeps catch nearly everything: (1) 90 days of card/bank statements filtered for recurring charges, (2) the subscription pages inside the Apple/Google app stores — where app trials hide, and (3) PayPal's automatic-payments page. Add any annual renewals from your email (search 'receipt' or 'renewal') and you have the complete list in about 20 minutes."),
            ("Should I use a subscription-cancellation app?", "They can surface forgotten charges, but read the pricing: several charge subscription fees themselves (the irony is real) or take a cut of 'negotiated savings.' The DIY version — statement scan plus the app-store pages — takes 20 minutes and costs nothing. If an app does the audit that you'd otherwise never do, though, even a paid one can earn its keep."),
            ("Is it better to pay annually or monthly?", "Annual pricing typically saves 15-40% — on services you're certain you'll keep all year. The risk is silent renewal of something you stopped using in month three. A working rule: annual billing only for services that survived a full year of monthly billing first, with the renewal date in your calendar. Everything newer stays monthly, on probation."),
            ("How do I stop subscription spending from creeping back up?", "Two structural habits beat vigilance: a quarterly 15-minute re-scan (prices creep and new trials accumulate — a calendar reminder does it), and routing every cancellation's amount into an automatic transfer the same day, so the freed money is captured rather than reabsorbed. Some people also run subscriptions on a single dedicated card, which makes the quarterly scan a one-statement job."),
        ],
    },
]
