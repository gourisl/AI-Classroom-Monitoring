
import streamlit as st
import sqlite3
import pandas as pd

# Configure dashboard
st.set_page_config(
    page_title="AI Classroom Monitoring",
    page_icon="🎓",
    layout="wide"
)

# Dashboard heading
st.title("🎓 AI Classroom Monitoring System")
st.write("Live classroom monitoring analytics")

# Connect to database
connection = sqlite3.connect("classroom_monitoring.db")

# Retrieve classroom records
query = """
SELECT *
FROM classroom_logs
ORDER BY id DESC
"""

data = pd.read_sql_query(query, connection)

connection.close()

# Check whether records exist
if data.empty:
    st.warning("No classroom records available.")
    st.stop()

# Convert timestamp into datetime
data["timestamp"] = pd.to_datetime(data["timestamp"])

# Calculate statistics
total_records = len(data)
maximum_people = data["people_count"].max()
average_people = data["people_count"].mean()
total_phones = data["phone_count"].sum()

# Display summary
st.subheader("Classroom Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", total_records)
col2.metric("Maximum People", int(maximum_people))
col3.metric("Average People", round(average_people, 2))
col4.metric("Phone Detections", int(total_phones))

st.divider()

# Display people count graph
st.subheader("People Detection Over Time")

chart_data = data.sort_values("timestamp")

people_chart = chart_data.set_index("timestamp")[
    ["people_count"]
]

st.line_chart(people_chart)

# Display phone detection graph
st.subheader("Phone Detection Over Time")

phone_chart = chart_data.set_index("timestamp")[
    ["phone_count"]
]

st.line_chart(phone_chart)

st.divider()

# Display recent records
st.subheader("Recent Classroom Records")

st.dataframe(
    data.head(20),
    use_container_width=True,
    hide_index=True
)

# Footer
st.caption("AI Classroom Monitoring System | Data stored locally using SQLite")
