
import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open webcam
camera = cv2.VideoCapture(0)

while True:

    # Capture camera frame
    success, frame = camera.read()

    if not success:
        print("Camera not detected")
        break

    # Detect mobile phones
    results = model.predict(
        frame,
        classes=[67],
        conf=0.25,
        verbose=False
    )

    # Get detection result
    result = results[0]

    # Count detected phones
    phone_count = len(result.boxes)

    # Draw bounding boxes
    output = result.plot()

    # Display phone count
    cv2.putText(
        output,
        "Phones Detected: " + str(phone_count),
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Display camera output
    cv2.imshow("AI Mobile Phone Detection", output)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
