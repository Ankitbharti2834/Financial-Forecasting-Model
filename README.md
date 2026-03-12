# Project - Financial Forecasting Model & Cost-Profitability Analysis

**Organization:** Aware Custom Biometric Wearables  
**Domain:** Financial Analytics | Business Intelligence | Strategic Planning  
**Reported To:** CFO, COO, VPs, Directors  
**Confidentiality:** 🔒 Enterprise Internal Project — Defense-Adjacent Organization  
> *All production financial figures, pricing strategies, internal budgets, and SSRS report configurations are confidential. This repository demonstrates the forecasting methodology and analytical logic using synthetic data across equivalent product lines and time periods.*

---

## Business Problem

Aware CBW's financial forecasting process relied on decentralized Excel workbooks maintained by individual department heads. Multi-team inputs were reconciled manually, variance calculations were error-prone, and the CFO had no consolidated view of profitability by product line. Cost leakage across three segments (Defense, Industrial, Healthcare) was undetected due to the lack of automated segmentation analysis.

## Solution

Redesigned the financial forecasting workflow end-to-end. Built Advanced Excel models using VBA macros and Power Query to consolidate multi-team inputs automatically, eliminating the manual reconciliation step. Developed Python-based forecasting models (OLS trend) for rolling quarterly projections, and SSRS/Power BI reports surfacing unit profitability, expense drivers, pricing impact, and margin performance. Applied A/B testing methodology to evaluate pricing adjustments across three product lines. Established data governance protocols including version control and structured approval workflows for report publication.

## Technical Architecture

```
Multi-team Excel Inputs (Power Query)
        │
        ▼
Consolidated Financial Model (VBA + Python OLS)
        │
        ├──► Variance Analysis       ──► SSRS / Power BI Report
        ├──► Margin / Leakage Check  ──► Executive Presentation
        ├──► Rolling Quarterly Forecast
        └──► A/B Pricing Impact Analysis
```

## Key Deliverables

- Quarterly revenue vs. forecast variance analysis with outlier flagging  
- Net margin and gross margin breakdown by product line with cost leakage detection  
- OLS-based rolling 4-quarter revenue forecast  
- A/B pricing test evaluation: conversion lift and revenue impact per product  
- Executive-ready output for CFO budget reviews  

## Impact

| Metric | Result |
|---|---|
| Forecast accuracy improvement | **25%** |
| Cost leakage identified | **3 product lines** |
| Manual reconciliation eliminated | ✅ |
| Governance protocols established | ✅ |

## Repository Contents

```
Project_04_Financial_Forecasting/
├── python/
│   └── forecasting_model.py         # Variance analysis, margin analysis, OLS forecast, A/B test
├── data/
│   ├── financial_forecast_model.csv # Synthetic quarterly P&L by product line (48 periods)
│   └── ab_pricing_test.csv          # Synthetic A/B pricing test results (60 scenarios)
└── README.md
```

## Running the Model

```bash
pip install pandas numpy
python python/forecasting_model.py
# Outputs: data/variance_analysis_output.csv
#          data/margin_analysis_output.csv
```

## Tools & Technologies

Advanced Excel (VBA, Power Query) · Power BI · SQL Server · SSRS · Python (Pandas, NumPy)

---
*For technical discussion, connect via [LinkedIn](https://linkedin.com/in/ankitbharti2834).*
