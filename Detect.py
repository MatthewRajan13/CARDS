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

CONFIDENCE_THRESHOLD = .75

cap = cv2.VideoCapture(0)
last_player = []
last_dealer = []

while cap.isOpened():
    dealer = []
    player = []

    success, frame = cap.read()
    if success:
        results = model(frame)
        for result in results:
            for i in range(int(result.boxes.cls.shape[0])):
                name = result.names[int(result.boxes.cls[i])]
                box = result.boxes.xyxy[i]
                conf = result.boxes.conf[i]

                if box[3] < frame.shape[0] / 2 and conf > CONFIDENCE_THRESHOLD:
                    dealer.append(name)
                elif box[3] >= frame.shape[0] / 2 and conf > CONFIDENCE_THRESHOLD:
                    player.append(name)

        if len(player) == 0:
            player = last_player
        if len(dealer) == 0:
            dealer = last_dealer

        last_player = player
        last_dealer = dealer

        print('Dealer: ', dealer)
        print('Player: ', player)

        annotated_frame = results[0].plot()

        cv2.imshow('YOLOv8', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
