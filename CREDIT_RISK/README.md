# Credit Risk Prediction — End-to-End ML Project

This project implements an **end-to-end credit risk prediction system** using multiple machine learning models:
- Logistic Regression
- Random Forest Classifier
- XGBoost Classifier

The best-performing model (**XGBoost**) is deployed as a **production-ready FastAPI REST API** with a **Streamlit frontend** for interactive predictions.

---

## 🚀 Project Highlights
- Multiple ML models trained and evaluated
- End-to-end preprocessing using `ColumnTransformer`
- Robust handling of missing values and categorical variables
- Model comparison and selection based on performance
- Production-ready deployment using FastAPI
- Interactive frontend using Streamlit
- Safe JSON serialization and version-consistent deployment

---

## 🧠 Models Used

### 1️⃣ Logistic Regression
- Baseline interpretable model
- Useful for understanding feature influence
- Helps benchmark performance against complex models

### 2️⃣ Random Forest Classifier
- Ensemble-based tree model
- Captures non-linear relationships
- Provides feature importance insights

### 3️⃣ XGBoost Classifier (Final Model)
- Gradient boosting model with superior performance
- Handles complex feature interactions effectively
- Selected for deployment due to best overall metrics

---

## 📊 Model Training & Selection
All models were trained on the same preprocessed dataset and evaluated using classification metrics such as:
- Accuracy
- Precision
- Recall
- ROC-AUC

**XGBoost** achieved the best trade-off between recall and precision and was therefore selected for deployment.

---
## 🏗️ Deployment Architecture

The final deployed system follows a **client–server ML inference architecture**:

### 🔹 Model Selection
Three models were trained and evaluated:
- Logistic Regression
- Random Forest
- XGBoost

Based on evaluation metrics (ROC-AUC, precision–recall tradeoff), **XGBoost** was selected as the **deployment model**.

---

### 🔹 Model Packaging
- The **entire preprocessing pipeline + XGBoost model** is packaged as a **single serialized object** (`pre_screening.pkl`)
- This includes:
  - Missing value imputation
  - Feature scaling
  - One-hot encoding for categorical variables
  - Final trained XGBoost classifier

This guarantees **training–inference consistency**.

---

### 🔹 Backend (FastAPI)
- FastAPI exposes a REST endpoint: `POST /predict`
- Responsibilities:
  - Validate incoming requests using Pydantic
  - Convert input JSON → Pandas DataFrame
  - Pass data through the serialized ML pipeline
  - Post-process predictions into business-friendly outputs

**Returned outputs:**
- Default probability
- Risk score (0–100)
- Risk level (Low / Medium / High)
- Decision recommendation (Approve / Manual Review / Reject)

---

### 🔹 Frontend (Streamlit)
- Streamlit provides a simple UI for:
  - Manual input of loan applicant details
  - Triggering predictions via the FastAPI endpoint
  - Displaying prediction results in real time
- Acts as a client consuming the deployed ML API

---

### 🔹 Data Flow
User (Streamlit UI)
↓
FastAPI (/predict endpoint)
↓
Serialized ML Pipeline
↓
Prediction + Risk Scoring
↓
JSON Response → UI

## 📁 Project Structure
CREDIT_RISK/
├── Backend.py # FastAPI backend (XGBoost model)
├── Frontend.py # Streamlit frontend
├── pre_screening.pkl # Serialized preprocessing + XGBoost pipeline
├── notebooks/
│ ├── Credit_risk(LOGISTIC).ipynb
│ ├── Credit_risk(RFC).ipynb
│ └── Credit_risk(XGBoost).ipynb
│ └── Credit_risk(XGBoost)_Deployed.ipynb
├── requirements.txt
└── README.md


---

## 🧩 Input Features
| Feature | Description |
|------|------------|
loan_amnt | Loan amount |
term | Loan term (36 or 60 months) |
int_rate | Interest rate |
fico_range_low | FICO score |
annual_inc | Annual income |
dti | Debt-to-income ratio |
emp_length | Employment length |
purpose | Loan purpose |
open_acc | Open credit lines |
total_acc | Total credit lines |
revol_util | Revolving utilization |
inq_last_6mths | Credit inquiries in last 6 months |

---

## 🔌 API Usage

### Endpoint
**POST** `/predict`

### Sample Request
```json
{
  "loan_amnt": 250000,
  "term": "36 months",
  "int_rate": 13.5,
  "fico_range_low": 680,
  "annual_inc": 80000,
  "dti": 18.2,
  "emp_length": "5 years",
  "purpose": "debt_consolidation",
  "open_acc": 6,
  "total_acc": 18,
  "revol_util": 45.9,
  "inq_last_6mths": 1
}
```


### Sample Response
```json
{
  "default_probability": 0.27,
  "risk_score": 27,
  "risk_level": "Medium",
  "decision_recommendation": "Manual Review"
}
```
---

## ▶️ Run Locally
Backend
pip install -r requirements.txt
uvicorn Backend:app --reload

Frontend
streamlit run Frontend.py


Access API docs at: http://127.0.0.1:8000/docs

## ⚠️ Deployment Notes

The deployed model is a single serialized pipeline (preprocessing + model)

OneHotEncoder(handle_unknown="ignore") prevents inference crashes

NumPy outputs are converted to native Python types for JSON safety

scikit-learn version consistency is required between training and deployment

##  Future Improvements

Deploy Logistic Regression and Random Forest as optional inference models

Add model comparison dashboard

Dockerize full application

Add CI/CD and automated testing

Add monitoring for data drift

## 👩‍💻 Author

Eshita
Machine Learning & API Development
