from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import xgboost as xgb
import traceback


class Item(BaseModel):
    loan_amnt: float
    term: str
    int_rate: float
    fico_range_low: float
    annual_inc: float
    dti: float
    emp_length: str
    purpose: str
    open_acc: float
    total_acc: float
    revol_util: float
    inq_last_6mths: float


app = FastAPI()


with open("pre_screening.pkl", "rb") as f:
    model = pickle.load(f)


@app.post("/predict")
async def predict(item: Item):
    try:

        data_dict = item.model_dump()
        df = pd.DataFrame([data_dict])


        expected_columns = [
            "loan_amnt", "term", "int_rate", "fico_range_low", "annual_inc",
            "dti", "emp_length", "purpose", "open_acc", "total_acc",
            "revol_util", "inq_last_6mths"
        ]
        df = df[expected_columns]


        prob = model.predict_proba(df)[0][1]
        prob = float(prob)


        risk_score = int(prob * 100)

        if prob < 0.2:
            risk_level = "Low"
            decision = "Approve"
        elif prob < 0.5:
            risk_level = "Medium"
            decision = "Manual Review"
        else:
            risk_level = "High"
            decision = "Reject"


        return {
            "default_probability": round(prob, 3),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "decision_recommendation": decision
        }

    except Exception as e:
        print("🔥 ERROR OCCURRED 🔥")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )