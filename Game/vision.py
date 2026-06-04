import cv2
from hand_track import track_hand

camera = cv2.VideoCapture(0)

print("Connected")
print("Camera Opened:", camera.isOpened())

pieces = []
holding_piece = None

o_palette_pos = (250, 250)
x_palette_pos = (250, 450)

def draw_o(frame, x, y, color):
    cv2.circle(frame, (x, y), 35, color, 3)

def draw_x(frame, x, y, color):
    cv2.line(frame, (x - 30, y - 30), (x + 30, y + 30), color, 3)
    cv2.line(frame, (x + 30, y - 30), (x - 30, y + 30), color, 3)

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

while True:
    success, frame = camera.read()

    if not success:
        print("Failed to access camera")
        break

    frame, is_pinching, finger_x, finger_y = track_hand(frame)

    cv2.rectangle(frame, (540, 260), (740, 460), (0, 255, 0), 3)

    cv2.line(frame, (540, 260), (360, 260), (0, 255, 0), 3)
    cv2.line(frame, (540, 460), (360, 460), (0, 255, 0), 3)

    cv2.line(frame, (740, 260), (940, 260), (0, 255, 0), 3)
    cv2.line(frame, (740, 460), (940, 460), (0, 255, 0), 3)

    cv2.line(frame, (540, 260), (540, 60), (0, 255, 0), 3)
    cv2.line(frame, (740, 260), (740, 60), (0, 255, 0), 3)

    cv2.line(frame, (540, 460), (540, 660), (0, 255, 0), 3)
    cv2.line(frame, (740, 460), (740, 660), (0, 255, 0), 3)

    if is_pinching and holding_piece is None and finger_x is not None:
        if distance(finger_x, finger_y, o_palette_pos[0], o_palette_pos[1]) < 50:
            holding_piece = ["O", finger_x, finger_y]

        elif distance(finger_x, finger_y, x_palette_pos[0], x_palette_pos[1]) < 50:
            holding_piece = ["X", finger_x, finger_y]

    if holding_piece is not None and finger_x is not None:
        holding_piece[1] = finger_x
        holding_piece[2] = finger_y

    if not is_pinching and holding_piece is not None:
        pieces.append(holding_piece)
        holding_piece = None

    draw_o(frame, o_palette_pos[0], o_palette_pos[1], (0, 0, 255))
    draw_x(frame, x_palette_pos[0], x_palette_pos[1], (0, 0, 255))

    for piece in pieces:
        kind, px, py = piece

        if kind == "O":
            draw_o(frame, px, py, (0, 0, 255))

        elif kind == "X":
            draw_x(frame, px, py, (0, 0, 255))

    if holding_piece is not None:
        kind, px, py = holding_piece

        if kind == "O":
            draw_o(frame, px, py, (0, 255, 255))

        elif kind == "X":
            draw_x(frame, px, py, (0, 255, 255))

    cv2.imshow("Laptop Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
