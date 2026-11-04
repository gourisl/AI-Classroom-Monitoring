
from ultralytics import YOLO

# Load a pretrained lightweight AI model
model = YOLO("yolo11n.pt")

# Detect objects in an image
results = model.predict(
    source=0,
    show=True,
    classes=[0],
    conf=0.4
)
