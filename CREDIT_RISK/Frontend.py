import streamlit as st
import requests

# ------------------------------
# Page config
# ------------------------------
st.set_page_config(
    page_title="Credit Risk Pre-Screening",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Credit Risk Pre-Screening")
st.caption("Estimate probability of loan default for fintech pre-screening")

# ------------------------------
# Sidebar (Info)
# ------------------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.write(
        """
        This tool estimates **credit default risk** based on applicant
        financial and loan characteristics.

        ⚠️ *This is a pre-screening tool, not a final approval system.*
        """
    )

# ------------------------------
# Input Form
# ------------------------------
st.subheader("Applicant & Loan Details")

with st.form("risk_form"):
    loan_amnt = st.number_input(
        "Loan Amount (₹)",
        min_value=1000,
        max_value=5000000,
        step=1000
    )

    term = st.selectbox(
        "Loan Term",
        [" 36 months", " 60 months"]
    )

    int_rate = st.number_input(
        "Interest Rate (%)",
        min_value=5.0,
        max_value=40.0,
        step=0.1
    )

    annual_inc = st.number_input(
        "Annual Income (₹)",
        min_value=50000,
        max_value=10000000,
        step=50000
    )

    emp_length = st.selectbox(
        "Employment Length",
        [
            "< 1 year",
            "1 year",
            "2 years",
            "3 years",
            "4 years",
            "5 years",
            "6 years",
            "7 years",
            "8 years",
            "9 years",
            "10+ years"
        ]
    )

    dti = st.number_input(
        "Debt-to-Income Ratio (%)",
        min_value=0.0,
        max_value=50.0,
        step=0.1
    )

    fico_range_low = st.slider(
        "Credit Score (FICO)",
        min_value=300,
        max_value=850,
        value=650
    )

    purpose = st.selectbox(
        "Loan Purpose",
        [
            "debt_consolidation",
            "credit_card",
            "home_improvement",
            "major_purchase",
            "small_business",
            "car",
            "medical",
            "house",
            "vacation",
            "moving",
            "renewable_energy",
            "wedding",
            "educational",
            "other"
        ]
    )
    open_acc=st.number_input(
        "Open Accounts ",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )
    total_acc=st.number_input(
        "Total accounts ",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )
    revol_util=st.number_input(
        "Revol Utilization ",
        min_value=0.0,
        max_value=100.0,
        step=0.1
    )
    inq_last_6mths=st.number_input(
        "Inquiry Last 6Mths ",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )

    submit = st.form_submit_button("🔍 Assess Risk")

# ------------------------------
# Prediction
# ------------------------------
if submit:
    payload = {
        "loan_amnt": loan_amnt,
        "term": term,
        "int_rate": int_rate,
        "annual_inc": annual_inc,
        "emp_length": emp_length,
        "dti": dti,
        "fico_range_low": fico_range_low,
        "purpose": purpose,
        "open_acc": open_acc,
        "total_acc": total_acc,
        "revol_util": revol_util,
        "inq_last_6mths": inq_last_6mths
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload
        )

        if response.status_code == 200:
            result = response.json()

            st.success("Risk Assessment Complete")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Default Probability",
                f"{result['default_probability'] * 100:.1f}%"
            )

            col2.metric(
                "Risk Score",
                result["risk_score"]
            )

            col3.metric(
                "Risk Level",
                result["risk_level"]
            )

            st.subheader("Recommendation")
            st.info(result["decision_recommendation"])

        else:
            st.error("Prediction failed. Please check the API.")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
