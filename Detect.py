import cv2
from ultralytics import YOLO


def clean_output(cards):
    cards = list(set(cards))
    cards = [card[:-1] for card in cards]

    face_map = {'J': 10, 'Q': 10, 'K': 10, 'A': 'A'}
    cards = [face_map[card] if card in face_map else int(card) for card in cards]

    return cards


model = YOLO('C:/Users/matth/runs/detect/train5/weights/best.pt')
model.to('cuda')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    cards = []
    if success:
        results = model(frame)
        for result in results:
            for i in range(int(result.boxes.cls.shape[0])):
                name = result.names[int(result.boxes.cls[i])]
                cards.append(name)

        print(clean_output(cards))

        annotated_frame = results[0].plot()

        cv2.imshow('YOLOv8', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
