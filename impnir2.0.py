import cv2
import numpy as np
import settings


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


def average_square_area_by_corners(img, lt, rb):
    colors = []
    for i in range(lt[0], lt[1]+1):
        for j in range(rb[0], rb[1]+1):
            colors.append(img[i, j])
    return average_colors(colors)


def average_triangle_area_by_corners(img, lt, rb, corners):
    colors = []
    for i in range(lt[0], lt[1]+1):
        for j in range(rb[0], rb[1]+1):
            colors.append(img[i, j])
    return average_colors(colors)



def average_square_area_by_mid(img, m, s):
    lt = (int(m[0] - s / 2), int(m[1] - s / 2))
    rb = (int(m[0] + s / 2), int(m[1] + s / 2))
    return average_square_area_by_corners(img, lt, rb)


def draw_triangle_area(img, points):
    cv2.line(img, points[0], points[1], (0, 0, 0), 5)
    cv2.line(img, points[1], points[2], (0, 0, 0), 5)
    cv2.line(img, points[2], points[0], (0, 0, 0), 5)


def draw_square_area_by_corners(img, lt, rb):
    cv2.rectangle(img, lt, rb, (0, 0, 0), 5)


def draw_square_area_by_mid(img, m, s):
    lt = (int(m[0] - s / 2), int(m[1] - s / 2))
    rb = (int(m[0] + s / 2), int(m[1] + s / 2))
    cv2.rectangle(img, lt, rb, (0, 0, 0), 5)


def color_by_average(img, m, s):
    # H: 0 - 180, S: 0 - 255, V: 0 - 255
    H_borders = {"red1": (0, 5), "orange": (80, 100), "yellow": (10, 15), "green": (15, 20), "blue": (40, 55), "red2": (25, 30)}
    avgColor = average_square_area_by_mid(img, m, s)
    print(avgColor)
    if avgColor[1] < 20 and avgColor[2] > 180:
        return "white"
    else:
        for color in H_borders.keys():
            if H_borders[color][0] < avgColor[0] < H_borders[color][1]:
                if 'red' in color:
                    return 'red'
                else:
                    return color


frame = cv2.imread('testImg.png', cv2.IMREAD_COLOR)
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(settings.CAMERA_PORT_NUM)


while True:
    # _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    draw_square_area_by_mid(frame, (110, 180), 70)
    draw_square_area_by_mid(frame, (316, 180), 70)
    draw_square_area_by_mid(frame, (522, 180), 70)
    draw_square_area_by_mid(frame, (110, 310), 70)
    draw_square_area_by_mid(frame, (316, 310), 70)
    draw_square_area_by_mid(frame, (522, 310), 70)
    draw_square_area_by_mid(frame, (150, 430), 50)
    draw_square_area_by_mid(frame, (500, 430), 50)
    draw_triangle_area(frame, [(430, 60), (430, 110), (550, 110)])
    draw_triangle_area(frame, [(210, 60), (210, 110), (90, 110)])
    print(6, color_by_average(hsv, (110, 180), 70))
    # print(7, color_by_average(hsv, (316, 180), 70))
    # print(8, color_by_average(hsv, (522, 180), 70))
    # print(9, color_by_average(hsv, (316, 310), 70))
    # print(10, color_by_average(hsv, (522, 310), 70))
    print(11, color_by_average(hsv, (150, 430), 50))
    # print(11, color_by_average(hsv, (500, 430), 50))

    cv2.imshow('hsv', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
# cap.release()