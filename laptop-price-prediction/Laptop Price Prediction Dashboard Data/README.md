# Laptop Price Prediction Dashboard (Power BI)

This project presents an end-to-end laptop price prediction system built using machine learning and visualized through an interactive Power BI dashboard.

## Overview
- A regression model (XGBoost) was trained to predict laptop prices based on hardware specifications and product attributes.
- Key features include RAM, storage, CPU tier, GPU brand, screen size, brand, and condition (new/refurbished).
- Model performance on the test set:
  - **RMSE:** ~400
  - **R²:** ~0.79

## Dashboard Highlights
- **KPI Cards**
  - Average actual price
  - Average predicted price
  - Average absolute error
- **Brand-level Analysis**
  - Actual vs predicted prices by brand
  - Scatter plot showing prediction alignment across brands
- **CPU Tier Analysis**
  - Comparison of actual and predicted prices across CPU tiers
- **Residual Analysis**
  - Histogram of residuals to assess prediction error distribution and bias
- **Interactive Filters**
  - Brand
  - CPU tier
  - GPU brand

## Key Insights
- The model captures relative price positioning across brands and CPU tiers accurately.
- Predictions scale well from low-end to high-end laptops.
- Residuals are centered around zero, indicating no systematic over- or under-pricing.
- Higher-priced laptops show slightly higher variance, which is expected in real-world pricing.

## Tools & Technologies
- Python (pandas, scikit-learn, XGBoost)
- SHAP for model explainability
- Power BI for visualization and business-facing analysis

## Use Case
This dashboard can be used by pricing, sales, or product teams to:
- Understand price drivers
- Validate pricing strategies
- Explore model confidence across different laptop segments

