import streamlit as st
import pandas as pd

st.set_page_config(page_title="Employee Performance Dashboard", layout="wide")

st.title("📊 Employee Performance Dashboard")

# -------------------------------
# Load default dataset from repo
# -------------------------------
@st.cache_data
def load_default_data():
    return pd.read_csv("employees.csv", encoding="utf-8-sig")

# File uploader (optional override)
file = st.file_uploader("Upload employees.csv (optional)", type=["csv"])

if file is not None:
    df = pd.read_csv(file, encoding="utf-8-sig")
else:
    try:
        df = load_default_data()
        st.success("Loaded dataset from repository ✅")
    except FileNotFoundError:
        st.error("employees.csv not found in repo. Please upload a file.")
        st.stop()

# -------------------------------
# Clean columns
# -------------------------------
df.columns = df.columns.str.strip().str.lower()

# Convert numeric columns safely
numeric_cols = ["projects_completed", "hours_worked", "performance_score"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Create efficiency column
df["efficiency"] = df["projects_completed"] / df["hours_worked"]

# -------------------------------
# Display Data
# -------------------------------
st.subheader("📄 Processed Data")
st.dataframe(df, use_container_width=True)

# -------------------------------
# Aggregations
# -------------------------------
avg_perf = df.groupby("department")["performance_score"].mean()
total_projects = df.groupby("department")["projects_completed"].sum()
projects_per_employee = df.groupby("employee")["projects_completed"].sum()
efficiency_per_employee = df.set_index("employee")["efficiency"]

most_productive = projects_per_employee.idxmax()
highest_eff_employee = efficiency_per_employee.idxmax()
highest_eff_dept = df.groupby("department")["efficiency"].mean().idxmax()

# -------------------------------
# KPIs
# -------------------------------
st.subheader("📌 Key Insights")
col1, col2, col3 = st.columns(3)

col1.metric("Most Productive Employee", most_productive)
col2.metric("Highest Efficiency Employee", highest_eff_employee)
col3.metric("Top Efficiency Department", highest_eff_dept)

st.divider()

# -------------------------------
# Charts
# -------------------------------
st.subheader("📊 Department Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("Average Performance per Department")
    st.bar_chart(avg_perf)

with col2:
    st.write("Total Projects per Department")
    st.bar_chart(total_projects)

st.divider()

st.subheader("👤 Employee Analysis")

col3, col4 = st.columns(2)

with col3:
    st.write("Projects per Employee")
    st.bar_chart(projects_per_employee)

with col4:
    st.write("Efficiency per Employee")
    st.bar_chart(efficiency_per_employee)
