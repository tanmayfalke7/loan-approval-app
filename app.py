import streamlit as st

st.set_page_config(page_title="Loan Eligibility Checker", page_icon="🏦", layout="centered")

st.title("🏦 Loan Approval Eligibility System")
st.write("Fill out the applicant details below to check instant loan eligibility.")

with st.form("loan_form"):
    full_name = st.text_input("Applicant Full Name", placeholder="e.g., Aarav Sharma")
    col1, col2 = st.columns(2)

    with col1:
        monthly_income = st.number_input("Monthly Income ($)", min_value=0, value=5000, step=250)
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=700)
        employment_status = st.selectbox(
            "Employment Status",
            ["Salaried", "Self-Employed", "Unemployed", "Student"]
        )

    with col2:
        loan_amount = st.number_input("Requested Loan Amount ($)", min_value=500, value=20000, step=500)
        loan_tenure_years = st.selectbox("Loan Tenure (Years)", [1, 2, 3, 5, 10, 15, 20])
        existing_emi = st.number_input("Existing Monthly Debt / EMI ($)", min_value=0, value=500, step=100)

    submitted = st.form_submit_button("Check Eligibility")

if submitted:
    if not full_name.strip():
        st.warning("Please enter the applicant's full name.")
    else:
        # Basic EMI estimation (assuming ~10% annual interest rate)
        monthly_rate = 0.10 / 12
        months = loan_tenure_years * 12
        estimated_emi = (
            loan_amount * monthly_rate * ((1 + monthly_rate) ** months)
        ) / (((1 + monthly_rate) ** months) - 1)

        total_monthly_debt = existing_emi + estimated_emi
        dti_ratio = (total_monthly_debt / monthly_income) if monthly_income > 0 else 1.0

        reasons = []
        if employment_status in ["Unemployed", "Student"]:
            reasons.append("Applicant must be Salaried or Self-Employed.")
        if credit_score < 650:
            reasons.append(f"Credit score ({credit_score}) is below the minimum requirement of 650.")
        if monthly_income < 2000:
            reasons.append("Monthly income must be at least $2,000.")
        if dti_ratio > 0.45:
            reasons.append(f"Debt-to-Income ratio ({dti_ratio:.0%}) exceeds the 45% threshold.")

        st.divider()
        if not reasons:
            st.success(f"Congratulations, {full_name}! You are **ELIGIBLE** for the loan.")
            st.info(
                f"**Estimated New EMI:** ${estimated_emi:,.2f}/month | "
                f"**Projected Debt-to-Income Ratio:** {dti_ratio:.1%}"
            )
        else:
            st.error(f"Sorry, {full_name}. You are **NOT ELIGIBLE** for the loan.")
            st.markdown("**Reasons for Rejection:**")
            for reason in reasons:
                st.markdown(f"- {reason}")