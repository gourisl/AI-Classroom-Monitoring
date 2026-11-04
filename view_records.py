
import sqlite3

# Connect to existing database
connection = sqlite3.connect("classroom_monitoring.db")

# Create cursor
cursor = connection.cursor()

# Retrieve the latest 20 records
cursor.execute("""
SELECT * FROM classroom_logs
ORDER BY id DESC
LIMIT 20
""")

records = cursor.fetchall()

print("\n===== CLASSROOM MONITORING RECORDS =====")

if records:

    print("\nID | Timestamp | People | Phones")
    print("-" * 55)

    for record in records:
        print(
            record[0], "|",
            record[1], "|",
            record[2], "|",
            record[3]
        )

else:
    print("No records found.")

# Calculate statistics
cursor.execute("""
SELECT
    COUNT(*),
    MAX(people_count),
    AVG(people_count),
    SUM(phone_count)
FROM classroom_logs
""")

statistics = cursor.fetchone()

print("\n===== CLASSROOM SUMMARY =====")

print("Total records:", statistics[0])
print("Maximum people detected:", statistics[1])
print("Average people detected:", round(statistics[2] or 0, 2))
print("Total phone detections:", statistics[3] or 0)

# Close database
connection.close()
