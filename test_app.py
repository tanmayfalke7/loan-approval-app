import py_compile
import unittest


def evaluate_loan(monthly_income, credit_score, employment_status, loan_amount, loan_tenure_years, existing_emi):
    monthly_rate = 0.10 / 12
    months = loan_tenure_years * 12
    estimated_emi = (
        loan_amount * monthly_rate * ((1 + monthly_rate) ** months)
    ) / (((1 + monthly_rate) ** months) - 1)

    total_monthly_debt = existing_emi + estimated_emi
    dti_ratio = (total_monthly_debt / monthly_income) if monthly_income > 0 else 1.0

    reasons = []
    if employment_status in ["Unemployed", "Student"]:
        reasons.append("Employment status ineligible")
    if credit_score < 650:
        reasons.append("Credit score below 650")
    if monthly_income < 2000:
        reasons.append("Monthly income below 2000")
    if dti_ratio > 0.45:
        reasons.append("DTI ratio exceeds 45%")

    return len(reasons) == 0, round(estimated_emi, 2), reasons


class TestLoanApprovalLogic(unittest.TestCase):
    def test_app_syntax(self):
        """Ensure app.py compiles cleanly with no syntax errors."""
        py_compile.compile("app.py", doraise=True)

    def test_eligible_applicant(self):
        eligible, emi, reasons = evaluate_loan(
            monthly_income=6000,
            credit_score=740,
            employment_status="Salaried",
            loan_amount=20000,
            loan_tenure_years=5,
            existing_emi=400,
        )
        self.assertTrue(eligible)
        self.assertEqual(reasons, [])
        self.assertGreater(emi, 0)

    def test_low_credit_score_rejected(self):
        eligible, _, reasons = evaluate_loan(
            monthly_income=6000,
            credit_score=580,
            employment_status="Salaried",
            loan_amount=15000,
            loan_tenure_years=3,
            existing_emi=200,
        )
        self.assertFalse(eligible)
        self.assertIn("Credit score below 650", reasons)

    def test_high_dti_rejected(self):
        eligible, _, reasons = evaluate_loan(
            monthly_income=3000,
            credit_score=720,
            employment_status="Self-Employed",
            loan_amount=50000,
            loan_tenure_years=2,
            existing_emi=500,
        )
        self.assertFalse(eligible)
        self.assertIn("DTI ratio exceeds 45%", reasons)


if __name__ == "__main__":
    unittest.main()