import cv2

# opens deafault camera

camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

print("Connected")
print("Camera Opened: ", camera.isOpened())

while True:
    # read frame from camera
    success, frame = camera.read()


    if not success:
        print("Failed to access camera")
        break


    #show fram in a window
    cv2.rectangle(frame, (540, 260), (740, 460), (0, 255, 0), 3)

    cv2.line(frame, (540, 260), (360, 260), (0, 255, 0), 3)
    cv2.line(frame, (540, 460), (360, 460), (0, 255, 0), 3)

    cv2.line(frame, (740, 260), (940, 260), (0, 255, 0), 3)
    cv2.line(frame, (740, 460), (940, 460), (0, 255, 0), 3)

    cv2.line(frame, (540, 260), (540, 60), (0, 255, 0), 3)
    cv2.line(frame, (740, 260), (740, 60), (0, 255, 0), 3)

    cv2.line(frame, (540, 460), (540, 660), (0, 255, 0), 3)
    cv2.line(frame, (740, 460), (740, 660), (0, 255, 0), 3)


    cv2.imshow("Laptop Camera", frame)

    

    # q = quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()
