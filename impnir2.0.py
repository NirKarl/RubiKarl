import cv2
import numpy as np
import settings

cap = cv2.VideoCapture(settings.CAMERA_PORT_NUM)
# img = cv2.imread('img.jpg', cv2.IMREAD_COLOR)


def average_colors(colorsList):
    avgH = 0
    avgS = 0
    avgV = 0
    for color in colorsList:
        avgH += color[0]
        avgS += color[1]
        avgV += color[2]
    avgH /= colorsList.__len__()
    avgS /= colorsList.__len__()
    avgV /= colorsList.__len__()
    return [avgH, avgS, avgV]


def average_square_area(img, lt, rb):
    colors = []
    for i in range(lt[0], lt[1]+1):
        for j in range(rb[0], rb[1]+1):
            colors.append(img[i, j])
    return average_colors(colors)


def color_by_average(img, lt, rb):
    H_borders = {"red1": (0, 5), "orange": (5, 10), "yellow": (10, 15), "green": (15, 20), "blue": (20, 25), "red2": (25, 30)}
    avgColor = average_square_area(img, lt, rb)
    if avgColor[1] > 90 and avgColor[2] > 90:
        return "white"
    else:
        for color in H_borders.keys():
            if H_borders[color][0] < avgColor[0] < H_borders[color][1]:
                if 'red' in color:
                    return 'red'
                else:
                    return color


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