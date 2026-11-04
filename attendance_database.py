
import cv2
import sqlite3
import time
from datetime import datetime
from ultralytics import YOLO

# Connect to database
connection = sqlite3.connect("classroom_monitoring.db")
cursor = connection.cursor()

# Create database table
cursor.execute("""
CREATE TABLE IF NOT EXISTS classroom_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    people_count INTEGER,
    phone_count INTEGER
)
""")

connection.commit()

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open webcam
camera = cv2.VideoCapture(0)

last_saved = 0

print("Classroom monitoring started!")

while True:

    # Capture camera frame
    success, frame = camera.read()

    if not success:
        print("Camera not detected")
        break

    # Detect people and phones
    results = model.predict(
        frame,
        classes=[0, 67],
        conf=0.25,
        verbose=False
    )

    result = results[0]

    # Count detected objects
    class_ids = result.boxes.cls.tolist()

    people_count = sum(
        int(class_id) == 0 for class_id in class_ids
    )

    phone_count = sum(
        int(class_id) == 67 for class_id in class_ids
    )

    # Save data every 5 seconds
    if time.time() - last_saved >= 5:

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """INSERT INTO classroom_logs
            (timestamp, people_count, phone_count)
            VALUES (?, ?, ?)""",
            (current_time, people_count, phone_count)
        )

        connection.commit()

        print(
            "Saved:", current_time,
            "| People:", people_count,
            "| Phones:", phone_count
        )

        last_saved = time.time()

    # Draw detection boxes
    output = result.plot()

    # Display counts
    cv2.putText(
        output,
        "People: " + str(people_count),
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        output,
        "Phones: " + str(phone_count),
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.imshow("Classroom Monitoring", output)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.release()
cv2.destroyAllWindows()

connection.close()

print("Monitoring stopped. Database saved.")
