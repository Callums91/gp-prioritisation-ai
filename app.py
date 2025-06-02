import streamlit as st
import pandas as pd

# Title
st.title("AI Review Prioritisation Tool for GP Surgeries")

# Instructions
st.markdown("""
Upload a CSV file with a `patient_id` column and a `conditions` column (comma-separated condition names).
Then, set your clinical risk index and generate the patient priority list.
""")

# Upload CSV
uploaded_file = st.file_uploader("Upload patient CSV", type="csv")

# Default Risk Index
default_risk_index = {
    "hypertension": 3,
    "diabetes": 5,
    "learning_disability": 1,
    "asthma": 2,
    "copd": 4,
    "heart_failure": 5,
    "mental_health": 2
}

# Risk Index Editor
st.sidebar.header("🧠 Risk Index (Set Scores)")
risk_index = {}
for condition, default_score in default_risk_index.items():
    risk_index[condition] = st.sidebar.slider(
        condition.replace("_", " ").title(),
        min_value=0,
        max_value=10,
        value=default_score
    )

# Review time logic (example)
def get_review_time(score):
    if score >= 10:
        return "40 minutes"
    elif score >= 5:
        return "20 minutes"
    else:
        return "10 minutes"

# Priority logic
def get_priority(score):
    if score >= 10:
        return "High"
    elif score >= 5:
        return "Medium"
    else:
        return "Low"

# Process data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["conditions"] = df["conditions"].fillna("").apply(lambda x: [c.strip().lower() for c in x.split(",")])
    
    # Score calculation
    scores = []
    priorities = []
    review_times = []

    for _, row in df.iterrows():
        conditions = row["conditions"]
        score = sum(risk_index.get(cond, 0) for cond in conditions)
        scores.append(score)
        priorities.append(get_priority(score))
        review_times.append(get_review_time(score))

    df["score"] = scores
    df["priority"] = priorities
    df["estimated_review_time"] = review_times

    st.success("Patient scoring complete.")
    st.dataframe(df)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results (CSV)", csv, "prioritised_patients.csv", "text/csv")

else:
    st.info("Please upload a CSV to begin.")
