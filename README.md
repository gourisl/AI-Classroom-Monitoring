# AI Classroom Monitoring System

An AI-powered classroom monitoring prototype built using Python, YOLO, OpenCV, MediaPipe, SQLite and Streamlit.

## Overview

The AI Classroom Monitoring System uses computer vision to analyze a live camera feed and provide useful classroom monitoring information through a dashboard.

## Features

- **Student Detection:** Detects visible people using YOLO.
- **People Counting:** Counts detected people in the camera frame.
- **Seat Occupancy:** Demonstrates occupancy detection using predefined camera regions.
- **Hand-Raising Detection:** Detects raised hands using MediaPipe Pose Landmarker.
- **Phone Detection:** Detects visible mobile phones using YOLO.
- **Database Logging:** Stores periodic classroom monitoring records using SQLite.
- **Dashboard:** Displays monitoring statistics and charts using Streamlit.

## Technologies Used

- Python
- OpenCV
- YOLO (Ultralytics)
- MediaPipe
- SQLite
- Streamlit
- Pandas

## Project Structure

```text
AI-Classroom-Monitoring/
│
├── main.py
├── student_counting.py
├── student_detection.py
├── seat_occupancy.py
├── hand_raising.py
├── multi_hand_raising.py
├── phone_detection.py
├── attendance_database.py
├── view_records.py
├── classroom_monitor.py
├── dashboard.py
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/gourisl/AI-Classroom-Monitoring.git
cd AI-Classroom-Monitoring
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate it on Windows:

```bash
venv\Scripts\activate
```

4. Install the dependencies:

```bash
pip install opencv-python ultralytics mediapipe streamlit pandas
```

5. Download the MediaPipe Pose Landmarker model:

```powershell
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task" -OutFile "pose_landmarker_lite.task"
```

The YOLO model weights are downloaded automatically by Ultralytics when needed.

## Running the Project

Start the integrated classroom monitoring program:

```bash
python classroom_monitor.py
```

Open a second terminal and start the dashboard:

```bash
streamlit run dashboard.py
```

## Important Limitations

This is a learning and development prototype.

- People counting does not establish the identity of individual students.
- Seat occupancy uses manually configured camera regions.
- Hand-raising detection depends on visible pose landmarks.
- Phone detection identifies visible phones, not confirmed phone usage.
- Camera-based detections can be affected by lighting, camera angle and occlusion.

The system should not be treated as a validated attendance or disciplinary system.

## Future Improvements

- Improved multi-person pose tracking.
- More accurate seat occupancy detection.
- Real-time dashboard updates.
- Classroom session management.
- CSV report generation.
- Performance evaluation and testing.

## Author

**Gouri S L**

B.Tech Artificial Intelligence and Machine Learning

Marian Engineering College, Trivandrum

GitHub: [@gourisl](https://github.com/gourisl)