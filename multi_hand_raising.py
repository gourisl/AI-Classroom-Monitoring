
import cv2
import time
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
    num_poses=5
)

camera = cv2.VideoCapture(0)
frame_number = 0

with vision.PoseLandmarker.create_from_options(options) as landmarker:

    while True:
        success, frame = camera.read()

        if not success:
            print("Camera error!")
            break

        # Convert BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect multiple poses
        timestamp_ms = frame_number * 33
        results = landmarker.detect_for_video(
            mp_image, timestamp_ms
        )

        raised_people = 0

        if results.pose_landmarks:

            for landmarks in results.pose_landmarks:

                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]
                left_wrist = landmarks[15]
                right_wrist = landmarks[16]

                left_raised = (
                    left_wrist.visibility > 0.5
                    and left_shoulder.visibility > 0.5
                    and left_wrist.y < left_shoulder.y
                )

                right_raised = (
                    right_wrist.visibility > 0.5
                    and right_shoulder.visibility > 0.5
                    and right_wrist.y < right_shoulder.y
                )

                if left_raised or right_raised:
                    raised_people += 1

                # Draw wrist positions
                h, w, _ = frame.shape

                for point in [left_wrist, right_wrist]:
                    x = int(point.x * w)
                    y = int(point.y * h)

                    cv2.circle(
                        frame, (x, y), 7, (255, 255, 0), -1
                    )

        # Display raised-hand count
        cv2.putText(
            frame,
            "People Raising Hands: " + str(raised_people),
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Multiple Hand Raising Detection", frame)

        frame_number += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
