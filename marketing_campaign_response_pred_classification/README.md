# Marketing Campaign Response Prediction (Classification)

## Overview
Predict whether a customer will respond to a marketing campaign.
Focus: imbalanced classification + evaluation using precision/recall/F1.

## Data Preparation
- Cleaned missing values
- Encoded categorical features (One-Hot Encoding where needed)
- Scaled numeric features when required
- Train/test split with stratification

## Modeling
Models explored:
- Logistic Regression
- Random Forest / XGBoost (final)

Evaluation focus:
- F1 score (primary)
- Precision/Recall
- Confusion Matrix
- ROC + Precision-Recall curves

## Key Findings
- Response class is imbalanced (majority “No”)
- Some features strongly influence response likelihood (see feature importance)
- PR curve is more informative than accuracy for this problem

## Project Structure

marketing-campaign-response/
├── notebook.ipynb
├── README.md
├── models/
│ └── marketing_response_model.pkl
