
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Load the pose detection model
model_path = "pose_landmarker_lite.task"

options = vision.PoseLandmarkerOptions(
    base_options=python.BaseOptions(
        model_asset_path=model_path
    ),
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1
)

# Open webcam
camera = cv2.VideoCapture(0)

frame_number = 0

# Create pose detector
with vision.PoseLandmarker.create_from_options(options) as landmarker:

    while True:

        success, frame = camera.read()

        if not success:
            print("Camera not detected")
            break

        # Convert BGR image to RGB
        rgb_frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )

        # Convert frame to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect body landmarks
        timestamp_ms = frame_number * 33

        results = landmarker.detect_for_video(
            mp_image, timestamp_ms
        )

        message = "No Hand Raised"
        color = (0, 0, 255)

        # Check detected person
        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            # Get shoulder and wrist landmarks
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]

            left_wrist = landmarks[15]
            right_wrist = landmarks[16]

            # Check left hand
            left_raised = (
                left_wrist.visibility > 0.5
                and left_shoulder.visibility > 0.5
                and left_wrist.y < left_shoulder.y
            )

            # Check right hand
            right_raised = (
                right_wrist.visibility > 0.5
                and right_shoulder.visibility > 0.5
                and right_wrist.y < right_shoulder.y
            )

            # Draw shoulder and wrist points
            h, w, _ = frame.shape

            for point in [
                left_shoulder, right_shoulder,
                left_wrist, right_wrist
            ]:
                x = int(point.x * w)
                y = int(point.y * h)
                cv2.circle(frame, (x, y), 7, (255, 255, 0), -1)

            # Display hand status
            if left_raised or right_raised:
                message = "HAND RAISED"
                color = (0, 255, 0)

        cv2.putText(
            frame,
            message,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

        cv2.imshow("AI Hand Raising Detection", frame)

        frame_number += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
