import cv2
from ultralytics import YOLO

model = YOLO('C:/Users/matth/runs/detect/train5/weights/best.pt')
model.to('cuda')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model(frame)

        annotated_frame = results[0].plot()

        cv2.imshow('YOLOv8', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
