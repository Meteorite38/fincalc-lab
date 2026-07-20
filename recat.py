# -*- coding: utf-8 -*-
"""One-shot: reassign calculator categories to the new 9-group taxonomy (edits calcs_*.py in place)."""
import io
import os
import re
import sys

NEW_CATS = {
    # Mortgages & Home (19)
    "mortgage-calculator": "Mortgages & Home", "house-down-payment-calculator": "Mortgages & Home",
    "mortgage-refinance-calculator": "Mortgages & Home", "extra-mortgage-payment-calculator": "Mortgages & Home",
    "biweekly-mortgage-calculator": "Mortgages & Home", "amortization-schedule-calculator": "Mortgages & Home",
    "home-equity-calculator": "Mortgages & Home", "home-affordability-calculator": "Mortgages & Home",
    "mortgage-points-calculator": "Mortgages & Home", "home-sale-proceeds-calculator": "Mortgages & Home",
    "rent-vs-buy-calculator": "Mortgages & Home", "15-vs-30-year-mortgage-calculator": "Mortgages & Home",
    "arm-vs-fixed-mortgage-calculator": "Mortgages & Home", "pmi-calculator": "Mortgages & Home",
    "closing-costs-calculator": "Mortgages & Home", "mortgage-recast-calculator": "Mortgages & Home",
    "heloc-calculator": "Mortgages & Home", "property-tax-calculator": "Mortgages & Home",
    "home-maintenance-budget-calculator": "Mortgages & Home",
    # Cars & Commuting (6)
    "car-affordability-calculator": "Cars & Commuting", "car-lease-calculator": "Cars & Commuting",
    "lease-vs-buy-car-calculator": "Cars & Commuting", "auto-loan-calculator": "Cars & Commuting",
    "fuel-cost-calculator": "Cars & Commuting", "commute-cost-calculator": "Cars & Commuting",
    # Debt & Credit (13)
    "loan-payment-calculator": "Debt & Credit", "loan-payoff-calculator": "Debt & Credit",
    "debt-snowball-vs-avalanche-calculator": "Debt & Credit", "credit-card-payoff-calculator": "Debt & Credit",
    "debt-to-income-ratio-calculator": "Debt & Credit", "student-loan-calculator": "Debt & Credit",
    "debt-consolidation-calculator": "Debt & Credit", "loan-comparison-calculator": "Debt & Credit",
    "credit-utilization-calculator": "Debt & Credit", "pay-off-debt-vs-invest-calculator": "Debt & Credit",
    "balance-transfer-calculator": "Debt & Credit", "student-loan-refinance-calculator": "Debt & Credit",
    "payday-loan-calculator": "Debt & Credit",
    # Salary & Work (10)
    "salary-to-hourly-calculator": "Salary & Work", "hourly-to-salary-calculator": "Salary & Work",
    "take-home-pay-calculator": "Salary & Work", "paycheck-calculator": "Salary & Work",
    "overtime-pay-calculator": "Salary & Work", "pay-raise-calculator": "Salary & Work",
    "bonus-tax-calculator": "Salary & Work", "rsu-tax-calculator": "Salary & Work",
    "job-offer-comparison-calculator": "Salary & Work", "salary-inflation-calculator": "Salary & Work",
    # Budgeting & Life (13)
    "budget-calculator": "Budgeting & Life", "emergency-fund-calculator": "Budgeting & Life",
    "inflation-calculator": "Budgeting & Life", "net-worth-calculator": "Budgeting & Life",
    "rent-affordability-calculator": "Budgeting & Life", "rent-increase-calculator": "Budgeting & Life",
    "move-or-stay-calculator": "Budgeting & Life", "savings-runway-calculator": "Budgeting & Life",
    "subscription-cost-calculator": "Budgeting & Life", "life-insurance-needs-calculator": "Budgeting & Life",
    "daycare-vs-staying-home-calculator": "Budgeting & Life", "college-roi-calculator": "Budgeting & Life",
    "unit-price-calculator": "Budgeting & Life",
    # Savings & Investing (17)
    "compound-interest-calculator": "Savings & Investing", "savings-goal-calculator": "Savings & Investing",
    "investment-return-calculator": "Savings & Investing", "roi-calculator": "Savings & Investing",
    "rule-of-72-calculator": "Savings & Investing", "present-value-calculator": "Savings & Investing",
    "future-value-calculator": "Savings & Investing", "dividend-income-calculator": "Savings & Investing",
    "simple-interest-calculator": "Savings & Investing", "cd-calculator": "Savings & Investing",
    "cd-ladder-calculator": "Savings & Investing", "apy-calculator": "Savings & Investing",
    "real-return-calculator": "Savings & Investing", "millionaire-calculator": "Savings & Investing",
    "investment-fee-impact-calculator": "Savings & Investing", "college-savings-calculator": "Savings & Investing",
    "time-to-save-calculator": "Savings & Investing", "savings-rate-calculator": "Savings & Investing",
    # Retirement (14)
    "401k-calculator": "Retirement", "roth-ira-calculator": "Retirement",
    "retirement-savings-calculator": "Retirement", "retirement-withdrawal-calculator": "Retirement",
    "annuity-payout-calculator": "Retirement", "fire-number-calculator": "Retirement",
    "coast-fire-calculator": "Retirement", "social-security-break-even-calculator": "Retirement",
    "roth-vs-traditional-401k-calculator": "Retirement", "hsa-calculator": "Retirement",
    "rmd-calculator": "Retirement", "roth-conversion-calculator": "Retirement",
    "401k-early-withdrawal-calculator": "Retirement", "pension-lump-sum-vs-annuity-calculator": "Retirement",
    # Taxes & Shopping (8)
    "sales-tax-calculator": "Taxes & Shopping", "discount-calculator": "Taxes & Shopping",
    "tip-calculator": "Taxes & Shopping", "capital-gains-tax-calculator": "Taxes & Shopping",
    "tax-bracket-calculator": "Taxes & Shopping", "quarterly-estimated-tax-calculator": "Taxes & Shopping",
    "tax-withholding-calculator": "Taxes & Shopping", "charitable-donation-bunching-calculator": "Taxes & Shopping",
    # Business & Self-Employment (9)
    "break-even-point-calculator": "Business & Self-Employment", "profit-margin-calculator": "Business & Self-Employment",
    "freelance-hourly-rate-calculator": "Business & Self-Employment", "cac-ltv-calculator": "Business & Self-Employment",
    "startup-runway-calculator": "Business & Self-Employment", "payback-period-calculator": "Business & Self-Employment",
    "rental-property-calculator": "Business & Self-Employment", "self-employment-tax-calculator": "Business & Self-Employment",
    "solo-401k-vs-sep-ira-calculator": "Business & Self-Employment",
}

changed = 0
for fn in sorted(os.listdir("content")):
    if not (fn.startswith("calcs_") and fn.endswith(".py")) or fn == "calcs_data.py":
        continue
    path = os.path.join("content", fn)
    src = io.open(path, encoding="utf-8").read()
    out = src
    # For each slug present in this file, rewrite the category line in its block.
    for slug, cat in NEW_CATS.items():
        marker = f'"slug": "{slug}"'
        idx = out.find(marker)
        if idx == -1:
            continue
        m = re.compile(r'("category":\s*")([^"]+)(")').search(out, idx)
        if m and m.group(2) != cat:
            out = out[:m.start(2)] + cat + out[m.end(2):]
            changed += 1
    if out != src:
        io.open(path, "w", encoding="utf-8").write(out)
        print("updated", fn)

print("category lines changed:", changed)
sys.path.insert(0, "content")
from calcs_data import CALCS  # noqa: E402
import collections  # noqa: E402
print(collections.Counter(c["category"] for c in CALCS))
