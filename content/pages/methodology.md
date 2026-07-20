---
slug: methodology
title: Our Methodology & Editorial Standards
description: How FinCalc Lab builds and tests its calculators, sources its information, and maintains accuracy — the standards behind every tool and guide.
---
Financial tools are only useful if they're accurate and honest. This page explains exactly how we build, test, and maintain everything on FinCalc Lab, so you can trust the numbers and understand their limits.

## How our calculators are built

Every calculator on this site implements standard, well-established financial formulas — the same math used in finance textbooks, spreadsheets, and professional practice. For example:

- **Loans and mortgages** use the standard amortization formula.
- **Savings and investment projections** use compound interest and future-value-of-an-annuity formulas.
- **Retirement tools** apply widely-cited frameworks such as the 4% safe-withdrawal guideline (from the Trinity study).
- **Business tools** use conventional definitions of contribution margin, cap rate, EBITDA, and similar.

Each calculator's page includes a plain-English explanation of the formula it uses and the assumptions it makes, so nothing is a black box.

## How our calculators are tested

Accuracy is enforced by an automated test suite that runs before every update:

1. **Functional tests** run each calculator with realistic inputs and verify the output is correct.
2. **Edge-case tests** run every calculator with extreme inputs (zeros, negatives, very large numbers) to ensure no calculator ever displays a broken result like "NaN" or crashes.
3. **Link checks** confirm every internal link points to a real page.
4. **Structured-data validation** confirms the technical markup on every page is valid.
5. **Live health checks** verify the published site is serving every page correctly after each deployment.

A change is only published if all of these checks pass.

## What earns a place here (and what gets retired)

We deliberately keep the catalog curated rather than maximal. A calculator earns a page when it answers a question people genuinely ask, with a method meaningfully distinct from its neighbors. We merge or retire tools that duplicate another tool's job, solve a rarely-asked variant of the same equation, or drift away from personal-finance decisions. When a tool is retired, its address permanently redirects to the closest substitute, so bookmarks and links keep working. The goal is that every tool you find here is the one worth finding — not one of five near-identical pages competing for your click.

## Our sources

Our calculators rely on standard financial mathematics, which doesn't change. Our guides draw on widely-accepted principles from reputable sources including academic research (such as the Trinity study on retirement withdrawals), long-run market data, and the consensus of mainstream financial education. Where we cite a specific rule of thumb (like 50/30/20 budgeting or the 28/36 mortgage guideline), we explain where it comes from and its limitations.

## Important limitations

We are transparent about what our tools can and cannot do:

- **They are educational estimates, not personalized advice.** Every calculator uses simplified models and general assumptions. Your real situation involves details — taxes, local rules, fees, personal circumstances — that a general tool cannot capture.
- **Tax and legal rules vary** by country, region, and year. Where taxes are involved, we let you enter your own rate rather than assuming one, because there is no universal figure.
- **Markets are uncertain.** Investment projections assume a steady return you choose; real returns are volatile and never guaranteed.
- **Nothing here is financial, tax, or legal advice.** For decisions with real stakes, consult a qualified, licensed professional in your jurisdiction.

## Who writes this

FinCalc Lab is built and maintained by a graduate researcher in accounting and financial data analysis, with a background in corporate finance, financial statement analysis, and quantitative modeling. Every calculator's logic and every guide is reviewed against standard formulas and reputable sources before publication. Read more on our [About page](/about/).

## Corrections

We take accuracy seriously and fix errors quickly. If you believe a calculator or guide contains a mistake, please tell us via our [contact page](/contact/) — include the page, the inputs you used, and what you expected. Verified corrections are published promptly.

## Our promise

Free tools, transparent math, honest limitations, and no dark patterns. Your inputs never leave your browser, we don't require accounts, and we tell you when a result is an estimate. That's the standard we hold every page to.
