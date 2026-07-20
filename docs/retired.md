# Retired pages log

Slimming policy: keep tools whose search demand is real and intent distinct; merge or retire
tools that duplicate a neighbor's job, solve a third direction of the same equation, or sit
off-mission for a personal-finance decision site. Every retirement gets a 301 to the nearest
substitute (emitted into `dist/_redirects` from `RETIRED` in `content/calcs_data.py`), and the
definition stays in its `calcs_part*.py` file for easy resurrection.

## 2026-07-21 slimming pass — calculators 120 → 110

| Retired slug | 301 target | Rationale |
|---|---|---|
| percentage-calculator | discount-calculator | Generic math utility, off-mission for a finance-decision site; discount page covers the shopping use case. |
| markup-calculator | profit-margin-calculator | Markup and margin are one relationship viewed from two sides; margin page explains the conversion. |
| required-return-calculator | savings-goal-calculator | Third solve-direction of the same goal equation (goal/monthly/rate); weakest search demand of the three. |
| latte-factor-calculator | subscription-cost-calculator | Same "small recurring habits compound" lesson; the subscription audit is the modern, actionable version. |
| ebitda-calculator | profit-margin-calculator | Corporate-finance metric; site mission is personal finance decisions. |
| vat-calculator | sales-tax-calculator | Same mechanics; site is US-focused and sales-tax page carries the intent. |
| cost-of-waiting-calculator | compound-interest-calculator | Its whole story (start now vs later) is one comparison run inside compound interest. |
| salary-gross-up-calculator | take-home-pay-calculator | Niche HR reverse-calculation of take-home; demand too thin for a standalone. |
| blended-debt-rate-calculator | debt-consolidation-calculator | Education stat with little standalone search demand; consolidation is where the question actually arises. |
| how-much-can-i-borrow-calculator | home-affordability-calculator | Subset of the 28/36 affordability tool with a weaker method (lender-limit only). |

Internal links to all ten were rewritten to their successors in the same pass (verify_links green).

## 2026-07-21 — articles 71 → 70

| Retired slug | 301 target | Rationale |
|---|---|---|
| roth-vs-traditional-retirement-accounts | roth-vs-traditional-decision | Two guides answered the same question; the "one question decides it" version is stronger and links the calculator. |
