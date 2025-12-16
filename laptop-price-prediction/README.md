# Laptop Price Prediction — Machine Learning Project

## Overview

This project predicts laptop prices using hardware specifications such as CPU, GPU, RAM, storage, screen size, and more.
It demonstrates real-world e-commerce pricing logic using machine learning and includes full model explainability with SHAP.

---

## Data Cleaning

Dropped irrelevant columns
Fixed missing values
Unified storage units
Extracted GPU brand
Parsed CPU brand, series, and tier
Converted touchscreen and categorical fields

---

## Feature Engineering

Created meaningful new features:
CPU Brand, CPU Series, CPU Tier
GPU Brand
Storage_High (≥512GB)
RAM_log
One-hot encoded 40+ categorical fields

---

## Models Used

Model	RMSE (prediction scores; the lower the better)
Linear Regression	~455
Ridge Regression	~453
Random Forest		~423
CatBoost		~412
XGBoost (Best)		~401


---

## Explainability (SHAP)

Used SHAP to interpret model decisions.
Key Drivers Increasing Price:
High RAM
Large Storage
High CPU Tier
Nvidia GPU
Bigger screen size
512GB+ storage

---

## Key Drivers Decreasing Price:

Refurbished condition
Entry-level CPUs
eMMC storage
Small screen sizes
Included both global beeswarm plot and single-laptop decision plot.

---

## Final Model
XGBoost Regressor
RMSE ≈ 401
R² ≈ 0.79


## Deployment Notes

To make this model production-ready:
Save model
Save preprocessing pipeline
Save schema
Write predict() function
Deploy using FastAPI / Flask / Streamlit


## Insights

- Hardware specifications dominate pricing.
- CPU/GPU tiers explain most price variation.
- Refurbished status has strong negative impact.
- Brand influences price but less than hardware.
SHAP aligns closely with real-world pricing logic.
