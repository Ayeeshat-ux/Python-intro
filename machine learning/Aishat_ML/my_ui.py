import streamlit as st
import pandas as pd
import joblib

# Set page configuration
st.set_page_config(
    page_title="Loan Approval Predictor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load Trained Model
@st.cache_resource
def load_model():
    try:
        return joblib.load("logistic_regression_model.pkl")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# Header Section
st.markdown('<div class="main-title">🏦 Loan Approval Prediction System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enter applicant financial information in the sidebar to assess loan eligibility in real time.</div>', unsafe_allow_html=True)

st.divider()

# Sidebar - User Inputs
st.sidebar.header("📋 Applicant Profile")
st.sidebar.write("Adjust parameters to model applicant risk:")

income = st.sidebar.number_input(
    "Annual Income ($)",
    min_value=0,
    max_value=2000000,
    value=500000,
    step=10000,
    help="Total annual gross income of the applicant."
)

credit_score = st.sidebar.slider(
    "Credit Score",
    min_value=300,
    max_value=850,
    value=700,
    help="Standard FICO score ranging from 300 to 850."
)

employment_years = st.sidebar.slider(
    "Employment History (Years)",
    min_value=0,
    max_value=40,
    value=5,
    help="Total uninterrupted years in current/previous employment."
)

debt_ratio = st.sidebar.slider(
    "Debt-to-Income Ratio (DTI)",
    min_value=0.0,
    max_value=1.0,
    value=0.35,
    step=0.01,
    help="Ratio of total monthly debt payments to gross monthly income."
)

# Prepare Feature Input DataFrame
input_data = pd.DataFrame({
    'income': [income],
    'credit_score': [credit_score],
    'employment_years': [employment_years],
    'debt_ratio': [debt_ratio]
})

# Layout: Two columns for displaying input summary and decision output
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📊 Applicant Summary")
    
    st.markdown(f"""
    <div class="metric-card">
        <strong>Annual Income:</strong> ${income:,.2f}<br>
        <strong>Credit Score:</strong> {credit_score}<br>
        <strong>Employment History:</strong> {employment_years} years<br>
        <strong>Debt Ratio:</strong> {debt_ratio:.2f} ({debt_ratio * 100:.1f}%)
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Input Data Preview")
    st.dataframe(input_data, hide_index=True, use_container_width=True)

with col2:
    st.subheader("🎯 Automated Assessment")
    
    if st.button("Evaluate Application", type="primary", use_container_width=True):
        if model is not None:
            # Generate Prediction & Probability
            prediction = model.predict(input_data)[0]
            
            # Extract probability if supported by the model
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(input_data)[0]
                approval_prob = probabilities[1]
            else:
                approval_prob = None

            st.write("---")
            if prediction == 1:
                st.success("### ✅ Status: Loan Approved")
                if approval_prob is not None:
                    st.metric(label="Approval Confidence", value=f"{approval_prob * 100:.1f}%")
                    st.progress(approval_prob)
            else:
                st.error("### ❌ Status: Loan Declined")
                if approval_prob is not None:
                    rejection_prob = 1 - approval_prob
                    st.metric(label="Rejection Risk", value=f"{rejection_prob * 100:.1f}%")
                    st.progress(rejection_prob)
        else:
            st.warning("Model file `logistic_regression_model.pkl` not found in current directory.")

# Run App Command:
# streamlit run app.py