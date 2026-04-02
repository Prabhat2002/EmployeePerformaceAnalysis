import streamlit as st
import pandas as pd

# Title
st.title("👨‍💼 Employee Performance Dashboard")

# Load CSV
emp_data = pd.read_csv("dataset/employee.csv")
hike_data = pd.read_csv("dataset/rating.csv")

# Split rating range (0-2 → Min, Max)
# Adding two new columns Min_Rating and Max_Rating by 
# splitting the "Rating Range" column
hike_data[["Min_Rating", "Max_Rating"]] = hike_data["Rating Range"].str.split("-", expand=True)
hike_data["Min_Rating"] = hike_data["Min_Rating"].astype(float)
hike_data["Max_Rating"] = hike_data["Max_Rating"].astype(float)

# print("Employee Data:")
# print(emp_data)
# print("\nHike Data:")
# print(hike_data)

#input without dropdown
#EmpId = st.number_input("Enter Employee Id:")
#There are other things as well such as text input, date input, 
#file uploader, etc. that you can explore in the 
#Streamlit documentation to enhance your UI further.
# Input (Dropdown better than text)
EmpId = st.selectbox("Select Employee Id", emp_data["Id"])

# adding button in order to get the details of the employee only when the button is clicked 
# else it will directly show the details of the first employee in the dataset 
# which is not good from UI perspective. So, we will add a button and show the details 
# only when the button is clicked.
if st.button("Fetch Employee Details"):

    st.write(f"Fetching details for Employee ID: {EmpId}...")

    # Logic
    emp = emp_data[emp_data["Id"] == EmpId].iloc[0]

    dept = emp["Department"]
    rating = emp["Rating"]
    salary = emp["Salary"]

    # Find hike % Based on Department and Rating of the employee from Hike Data
    hike_row = hike_data[
        (hike_data["Department"] == dept) &
        (hike_data["Min_Rating"] <= rating) &
        (hike_data["Max_Rating"] >= rating)
    ]

    print("\nHike Row:")
    print(hike_row)

    if not hike_row.empty:
        hike_percent = hike_row.iloc[0]["HikePercent"]

        print("\nHike Percent:")
        print(hike_percent)

        new_salary = salary + (salary * hike_percent / 100)

        # UI
        st.subheader("📊 Employee Details")

        col1, col2 = st.columns(2)

        col1.metric("Employee ID", emp["Id"])
        col1.metric("Name", emp["Name"])
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

    else:
        st.error("No hike data found for this employee.")

else:
    st.info("Please select a valid Employee ID and click the button to fetch details.")
