from cv2 import *
import cv2
import numpy as np
photos = {1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}


class Color:
    def __init__(self, low: tuple, high: tuple):
        self.low = np.array(low, np.uint8)
        self.high = np.array(high, np.uint8)


colours = {'yellow': Color((17, 100, 100), (40, 255, 255)),
           'red': Color((17, 100, 100), (40, 255, 255)),
           'blue': Color((100, 100, 100), (140, 255, 255)),
           'orange': Color((3, 100, 100), (15, 255, 255)),
           'white': Color((0, 0, 255), (0, 10, 255)),
           'green': Color((48, 100, 100), (72, 255, 255))
           }


def close(value, target, margin=0.2):
    if target * (1-margin) <= value:
        return True, True
    elif value <= target * (1+margin):
        return True, False
    return False, False


def get_square_contours(frame):

    img = cv2.GaussianBlur(frame, (5, 5), 0)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ret_val = []
    for key in colours:
        lower = colours[key].low
        upper = colours[key].low
        separated = cv2.inRange(img, lower, upper)
        _, gsc_contours, hierarchy = cv2.findContours(separated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        final_contours = []
        max_area = 0
        for contour in gsc_contours:
            area = cv2.contourArea(contour)
            con, abv = close(area, max_area)
            if area > max_area:
                max_area = area
                moment = cv2.moments(contour)
                (x, y) = moment['m10'] / moment['m00'], moment['m01'] / moment['m00']
                final_contours = [(contour, (x, y))]
            elif con:
                moment = cv2.moments(contour)
                (x, y) = moment['m10'] / moment['m00'], moment['m01'] / moment['m00']
                final_contours.append((contour, (x, y)))
        ret_val += final_contours
    return ret_val


def display_contours(image, contours):
    copy = image.copy()
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(copy, [box], 0, (0, 0, 255), 2)
    imshow(copy, 0)
    waitKey(0)


for i in range(6):
    image_read = input("Enter a photo location")
    photos[i+1] = image_read


for key in photos:
    curr_image = photos[key]
    frame = cv2.imread(curr_image)
    contours = [i[0] for i in get_square_contours(frame)]  # Edit this, it is built of (contour object, (x,y))
    display_contours(frame, contours)  # Delete this
