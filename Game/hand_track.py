import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def track_hand(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    is_pinching = False
    finger_x = None
    finger_y = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            h, w, _ = frame.shape

            ix = int(index_tip.x * w)
            iy = int(index_tip.y * h)

            tx = int(thumb_tip.x * w)
            ty = int(thumb_tip.y * h)

            distance = ((ix - tx) ** 2 + (iy - ty) ** 2) ** 0.5

            finger_x = ix
            finger_y = iy

            cv2.circle(frame, (ix, iy), 12, (0, 0, 255), -1)
            cv2.circle(frame, (tx, ty), 12, (255, 0, 0), -1)
            cv2.line(frame, (ix, iy), (tx, ty), (0, 255, 255), 3)

            if distance < 40:
                is_pinching = True
                cv2.putText(
                    frame,
                    "PINCHING",
                    (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    4
                )

    return frame, is_pinching, finger_x, finger_y