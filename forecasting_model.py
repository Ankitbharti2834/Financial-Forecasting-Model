"""
Project 4: Financial Forecasting Model & Cost-Profitability Analysis
Aware Custom Biometric Wearables — Enterprise Internal (Confidential)

Demonstrates the forecasting methodology used to support CFO/COO budgeting
cycles: variance decomposition, rolling forecast, A/B pricing impact analysis,
and margin leakage identification across Defense, Industrial, Healthcare, and
Sports product lines.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

DATA_PATH   = "data/financial_forecast_model.csv"
AB_PATH     = "data/ab_pricing_test.csv"
OUTPUT_PATH = "data/"


# ═══════════════════════════════════════════════════════════════════════════
# 1. DATA LOADING & PREPARATION
# ═══════════════════════════════════════════════════════════════════════════

def load_financials(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df[["Year","Quarter"]] = df["Period"].str.extract(r"(\d{4})-Q(\d)")
    df["Year"]    = df["Year"].astype(int)
    df["Quarter"] = df["Quarter"].astype(int)
    df["Period_Num"] = (df["Year"] - df["Year"].min()) * 4 + df["Quarter"]
    return df


# ═══════════════════════════════════════════════════════════════════════════
# 2. VARIANCE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def variance_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes forecast vs actual variance by product line and period.
    Flags outlier quarters where absolute variance exceeds ±10%.
    """
    df = df.copy()
    df["variance_usd"] = df["Revenue_Actual"] - df["Revenue_Forecast"]
    df["variance_pct"] = (df["variance_usd"] / df["Revenue_Forecast"].replace(0, np.nan) * 100).round(2)
    df["variance_flag"] = df["variance_pct"].abs().apply(
        lambda x: "⚠️ OUTLIER" if x > 10 else "OK"
    )
    return df[["Period","Product_Line","Revenue_Actual","Revenue_Forecast",
               "variance_usd","variance_pct","variance_flag"]]


# ═══════════════════════════════════════════════════════════════════════════
# 3. MARGIN ANALYSIS — IDENTIFY COST LEAKAGE
# ═══════════════════════════════════════════════════════════════════════════

def margin_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates gross and net margin per product line per quarter.
    Identifies lines with negative contribution margins (cost leakage).
    """
    df = df.copy()
    df["gross_margin_usd"] = df["Revenue_Actual"] - df["COGS_Actual"]
    df["gross_margin_pct"] = (df["gross_margin_usd"] / df["Revenue_Actual"].replace(0, np.nan) * 100).round(2)
    df["net_margin_usd"]   = df["gross_margin_usd"] - df["OPEX_Actual"]
    df["net_margin_pct"]   = (df["net_margin_usd"] / df["Revenue_Actual"].replace(0, np.nan) * 100).round(2)
    df["cost_leakage_flag"] = df["net_margin_pct"].apply(
        lambda x: "🚨 LEAKAGE" if x < 0 else ("⚠️ LOW" if x < 10 else "✅ HEALTHY")
    )
    return df[["Period","Product_Line","Revenue_Actual","gross_margin_pct",
               "net_margin_pct","cost_leakage_flag"]]


# ═══════════════════════════════════════════════════════════════════════════
# 4. ROLLING FORECAST — SIMPLE LINEAR TREND
# ═══════════════════════════════════════════════════════════════════════════

def rolling_forecast(df: pd.DataFrame, product_line: str, periods_ahead: int = 4) -> pd.DataFrame:
    """
    Fits a simple OLS trend on historical revenue for a given product line
    and projects forward n quarters. In production this feeds into the
    SSRS financial planning reports reviewed by the CFO.
    """
    sub = df[df["Product_Line"] == product_line].sort_values("Period_Num")
    x = sub["Period_Num"].values
    y = sub["Revenue_Actual"].values

    # OLS coefficients
    slope, intercept = np.polyfit(x, y, 1)

    last_period = sub["Period_Num"].max()
    last_year   = sub["Year"].max()
    last_q      = sub["Quarter"].max()

    forecasts = []
    for i in range(1, periods_ahead + 1):
        p_num = last_period + i
        qtr   = (last_q + i - 1) % 4 + 1
        yr    = last_year + (last_q + i - 1) // 4
        forecasted = slope * p_num + intercept
        forecasts.append({
            "Period": f"{yr}-Q{qtr}",
            "Product_Line": product_line,
            "Revenue_Forecast_OLS": round(max(forecasted, 0), 2),
            "Type": "FORECAST"
        })
    return pd.DataFrame(forecasts)


# ═══════════════════════════════════════════════════════════════════════════
# 5. A/B PRICING TEST ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def ab_pricing_analysis(path: str) -> pd.DataFrame:
    """
    Evaluates A/B pricing test results.
    Computes statistical lift and revenue impact per product per variant.
    In production this analysis fed executive presentations on pricing strategy.
    """
    df = pd.read_csv(path)
    summary = (
        df.groupby(["product","variant"])
        .agg(
            avg_price     = ("price_usd",         "mean"),
            total_conv    = ("conversions",        "sum"),
            total_impr    = ("impressions",        "sum"),
            total_revenue = ("revenue_impact",     "sum")
        )
        .reset_index()
    )
    summary["conv_rate_pct"] = (summary["total_conv"] / summary["total_impr"] * 100).round(2)

    # Compute lift of B vs A per product
    pivoted = summary.pivot(index="product", columns="variant",
                            values=["conv_rate_pct","total_revenue"]).reset_index()
    pivoted.columns = ["_".join(c).strip("_") for c in pivoted.columns]
    if "conv_rate_pct_A" in pivoted.columns and "conv_rate_pct_B" in pivoted.columns:
        pivoted["conversion_lift_pct"] = (
            (pivoted["conv_rate_pct_B"] - pivoted["conv_rate_pct_A"])
            / pivoted["conv_rate_pct_A"] * 100
        ).round(2)
        pivoted["revenue_lift_usd"] = (
            pivoted["total_revenue_B"] - pivoted["total_revenue_A"]
        ).round(2)
    return pivoted


# ═══════════════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Aware CBW — Financial Forecasting Model")
    print("="*60)

    df = load_financials(DATA_PATH)

    print("\n[1] Variance Analysis (Top 10 Outliers):")
    var = variance_analysis(df)
    outliers = var[var["variance_flag"] != "OK"].head(10)
    print(outliers.to_string(index=False))

    print("\n[2] Margin Analysis (Cost Leakage Check):")
    margin = margin_analysis(df)
    leakage = margin[margin["cost_leakage_flag"].str.contains("LEAKAGE|LOW")]
    print(leakage.head(10).to_string(index=False))

    print("\n[3] Rolling Forecast — Defense Product Line (4 Quarters):")
    forecast = rolling_forecast(df, "Defense", 4)
    print(forecast.to_string(index=False))

    print("\n[4] A/B Pricing Analysis:")
    ab = ab_pricing_analysis(AB_PATH)
    print(ab.to_string(index=False))

    # Save outputs
    var.to_csv(f"{OUTPUT_PATH}variance_analysis_output.csv", index=False)
    margin.to_csv(f"{OUTPUT_PATH}margin_analysis_output.csv", index=False)
    print("\n✅ Financial model complete. Results saved to data/")
