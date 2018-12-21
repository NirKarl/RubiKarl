import cv2
import numpy as np
import settings

cap = cv2.VideoCapture(settings.CAMERA_PORT_NUM)
# img = cv2.imread('img.jpg', cv2.IMREAD_COLOR)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([160, 0, 0])
    upper_red = np.array([190, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()