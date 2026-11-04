
import cv2
from ultralytics import YOLO

# Load the AI model
model = YOLO("yolo11n.pt")

# Open laptop webcam
camera = cv2.VideoCapture(0)

while True:

    # Capture video frame
    success, frame = camera.read()

    if not success:
        print("Camera not detected")
        break

    # Detect people
    results = model.predict(
        frame,
        classes=[0],
        conf=0.4,
        verbose=False
    )

    # Get detection results
    result = results[0]

    # Count detected people
    total_students = len(result.boxes)

    # Draw detection boxes
    output = result.plot()

    # Display student count
    cv2.putText(
        output,
        "Total Students: " + str(total_students),
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Display video
    cv2.imshow("AI Classroom Monitoring", output)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera
camera.release()
cv2.destroyAllWindows()
