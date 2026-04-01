import streamlit as st
import pandas as pd

# Title
st.title("👨‍💼 Employee Performance Dashboard")

# Load CSV
emp_data = pd.read_csv("dataset/employee.csv")
hike_data = pd.read_csv("dataset/rating.csv")

# Split rating range (0-2 → Min, Max)
hike_data[["Min_Rating", "Max_Rating"]] = hike_data["Rating Range"].str.split("-", expand=True)
hike_data["Min_Rating"] = hike_data["Min_Rating"].astype(float)
hike_data["Max_Rating"] = hike_data["Max_Rating"].astype(float)

# Input (Dropdown better than text)
name = st.selectbox("Select Employee", emp_data["Name"])

# Logic
emp = emp_data[emp_data["Name"] == name].iloc[0]

dept = emp["Department"]
rating = emp["Rating"]
salary = emp["Salary"]

# Find hike %
hike_row = hike_data[
    (hike_data["Department"] == dept) &
    (hike_data["Min_Rating"] <= rating) &
    (hike_data["Max_Rating"] >= rating)
]

hike_percent = hike_row.iloc[0]["HikePercent"]

new_salary = salary + (salary * hike_percent / 100)

# UI
st.subheader("📊 Employee Details")

col1, col2 = st.columns(2)

col1.metric("Employee ID", emp["Id"])
col1.metric("Department", dept)
col1.metric("Rating", rating)

col2.metric("Current Salary", f"₹{salary:,}")
col2.metric("Hike %", f"{hike_percent}%")
col2.metric("New Salary", f"₹{int(new_salary):,}")

# Insight
if rating >= 3.5:
    st.success("🌟 High Performer")
elif rating >= 2.0:
    st.warning("👍 Average Performer")
else:
    st.error("⚠️ Needs Improvement")