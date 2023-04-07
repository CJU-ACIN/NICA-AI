from ultralytics import YOLO

model = YOLO('yolov8n-seg.pt')
results = model.predict(source="0", show=True)
