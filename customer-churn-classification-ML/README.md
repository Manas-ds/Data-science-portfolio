# Customer Churn Prediction (Classification)

## Project Overview
This project predicts whether a telecom customer is likely to churn using machine learning.
The goal is to identify high-risk customers early and understand *why* they churn, so the business
can take proactive retention actions.

---

## Dataset
The dataset contains customer demographics, service subscriptions, billing information,
and contract details.

Target variable:
- **Churn** (Yes / No)

---

## Data Preparation
Key preprocessing steps:
- Removed `customerID` from modeling
- Converted `TotalCharges` to numeric
- Handled missing values using appropriate imputation
- Encoded categorical variables using One-Hot Encoding
- Scaled numeric features
- Used `ColumnTransformer` and `Pipeline` to avoid data leakage
- Stratified train-test split to preserve class balance

---

## Exploratory Data Analysis (EDA)
Key observations:
- Customers with **short tenure** churn more
- **Month-to-month contracts** have the highest churn
- **Fiber optic** internet users churn more than others
- **Electronic check** payment method is strongly associated with churn

EDA visuals are available in the `images/` folder.

---

## Modeling Approach
Models evaluated:
- Logistic Regression
- Random Forest
- XGBoost (final model)

Final model:
- **XGBoostClassifier** inside a full preprocessing pipeline
- Hyperparameters tuned using **GridSearchCV** with **StratifiedKFold**
- Class imbalance handled using `scale_pos_weight`

---

## Model Performance
The final model was evaluated using F1 score due to class imbalance.

Metrics (after threshold tuning):
- Improved recall for churned customers
- Balanced precision–recall trade-off
- Strong separation between churn and non-churn customers

Confusion matrix, ROC curve, and Precision-Recall curve are stored in `images/`.

---

## Explainability
Model predictions were interpreted using feature importance and SHAP analysis.

Top churn drivers:
- Low tenure
- High monthly charges
- Electronic check payments
- Fiber optic internet service
- Lack of technical support

These insights align with real-world telecom churn behavior.

---

## Project Structure
customer-churn/
├── notebook.ipynb
├── README.md
├── models/
│ ├── xgb_churn_pipeline.pkl
│ └── threshold.json
└── images/
├── confusion_matrix.png
├── roc_curve.png
├── pr_curve.png
├── feature_importance.png

---

## How to Use the Model
```python
import joblib, json

pipeline = joblib.load("models/xgb_churn_pipeline.pkl")
threshold = json.load(open("models/threshold.json"))["best_threshold"]

prob = pipeline.predict_proba(new_data)[0,1]
prediction = 1 if prob >= threshold else 0
