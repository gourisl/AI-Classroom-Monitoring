
import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open webcam
camera = cv2.VideoCapture(0)

# Set camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define three virtual seat regions
# Format: (x1, y1, x2, y2)
seats = {
    "Seat 1": (20, 100, 200, 460),
    "Seat 2": (220, 100, 420, 460),
    "Seat 3": (440, 100, 620, 460)
}

while True:

    # Capture camera frame
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

    result = results[0]

    # Get detected people
    people = []

    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Find centre of person
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        people.append((center_x, center_y))

    # Check seat occupancy
    occupied_count = 0

    for seat_name, (x1, y1, x2, y2) in seats.items():

        occupied = False

        for px, py in people:
            if x1 <= px <= x2 and y1 <= py <= y2:
                occupied = True
                break

        # Select colour
        if occupied:
            color = (0, 255, 0)
            occupied_count += 1
            status = "Occupied"
        else:
            color = (0, 0, 255)
            status = "Empty"

        # Draw seat region
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Display seat status
        cv2.putText(
            frame,
            seat_name + ": " + status,
            (x1 + 5, y1 + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

    # Calculate empty seats
    total_seats = len(seats)
    empty_count = total_seats - occupied_count

    # Display results
    cv2.putText(
        frame,
        "Occupied: " + str(occupied_count),
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Empty: " + str(empty_count),
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    cv2.imshow("AI Seat Occupancy Detection", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close camera
camera.release()
cv2.destroyAllWindows()
