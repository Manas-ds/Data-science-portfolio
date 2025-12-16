# Data-science-portfolio

# Data Science Portfolio

This repository contains multiple end-to-end data science and machine learning projects.
Each project focuses on solving a real-world business problem using structured data,
with emphasis on clean pipelines, proper evaluation, and explainability.

---

## Projects

### Customer Churn Prediction (Classification)
**Goal:** Predict whether a telecom customer is likely to churn.

**Highlights:**
- End-to-end ML pipeline using `ColumnTransformer` + `Pipeline`
- XGBoost with hyperparameter tuning and threshold optimization
- Evaluation using F1, ROC, Precision–Recall
- Business-oriented insights and churn drivers
- Explainability using feature importance and SHAP

Folder: `customer-churn/`

---

### Laptop Price Prediction (Regression)
**Goal:** Predict laptop prices from hardware and brand specifications.

**Highlights:**
- Feature engineering (CPU tiers, GPU brands, storage flags, log transforms)
- XGBoost regression for non-linear relationships
- Evaluation using RMSE and R²
- Model explainability using SHAP (global + individual predictions)

Folder: `laptop-price-prediction/`

---

### Marketing Campaign Response Prediction (Classification)
**Goal:** Predict whether a customer will respond to a marketing campaign.

**Highlights:**
- Handling class imbalance in classification
- Model evaluation beyond accuracy (F1, Precision–Recall)
- Feature importance and response behavior analysis
- Business interpretation of response drivers

Folder: `marketing-campaign-response/`

---

## Tools & Technologies
- Python
- Pandas, NumPy
- scikit-learn
- XGBoost
- SHAP
- Matplotlib / Seaborn
- Jupyter / Google Colab

---

## How to Use
Each project folder contains:
- A Jupyter notebook with full analysis
- A trained model (saved using `joblib`)
- Supporting images and documentation
- A project-specific README with details

---

## Notes
This repository is actively evolving as more projects are added, including:
- Marketing analytics
- Social media / ad performance analysis
- Advanced feature engineering and modeling techniques
