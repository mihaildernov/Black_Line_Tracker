import cv2

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 160)
video_capture.set(4, 120)

while (True):
    ret, frame = video_capture.read()
    crop_img = frame[60:120, 0:160]

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)

        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

        if cx >= 120:
            print("Поворот влево")

        if cx < 120 and cx > 50:
            print("Вперед")

        if cx <= 50:
            print("Поворот вправо")

    else:
        print("Линию не видно")

    cv2.imshow('frame', crop_img)

    if cv2.waitKey(1) & 0xff == 27:
        break
