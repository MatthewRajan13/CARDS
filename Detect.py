import cv2
from ultralytics import YOLO
import gameLogic

CONFIDENCE_THRESHOLD = .626


def clean_output(cards):
    cards = list(set(cards))
    cards = [card[:-1] for card in cards]

    face_map = {'J': 10, 'Q': 10, 'K': 10, 'A': 'A'}
    cards = [face_map[card] if card in face_map else int(card) for card in cards]

    return cards


def display(output):
    height, width, _ = annotated_frame.shape
    output = annotated_frame.copy()

    line_color = (169, 169, 169)
    line_thickness = 5
    dash_length = 20

    for i in range(0, width, dash_length * 2):
        start_point = (i, height // 2)
        end_point = (i + dash_length, height // 2)
        cv2.line(output, start_point, end_point, line_color, line_thickness)

    alpha = 0.5

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    text_position = (10, 35)
    cv2.putText(output, "Dealer", text_position, font, font_scale, line_color, font_thickness)

    text_position = (10, height // 2 + 35)
    cv2.putText(output, "Player", text_position, font, font_scale, line_color, font_thickness)

    output = cv2.addWeighted(annotated_frame, 1 - alpha, output, alpha, 0)

    return output


if __name__ == '__main__':

    model = YOLO('best.pt')
    model.to('cuda')

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

            player = clean_output(player)
            dealer = clean_output(dealer)

            print('Dealer: ', dealer)
            print('Player: ', player)

            annotated_frame = results[0].plot()

            screen = display(annotated_frame)

            cv2.imshow('YOLOv8', screen)
            # TODO: BlackJack logic goes here. Inputs: player, dealer. Outputs: move (hit, stand, double, split, surrender)
            suggested_move = gameLogic.logic(player, dealer)
            print(f"Suggested move: {suggested_move}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
