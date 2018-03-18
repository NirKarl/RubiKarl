import cv2
import numpy
import json
import time

WHITE = 'WHITE'
BLUE = 'BLUE'
RED = 'RED'
YELLOW = 'YELLOW'
GREEN = 'GREEN'
ORANGE = 'ORANGE'
calDataFile = "RubikarlCalibration.json"

NIR_DICT = {WHITE: 'U',
            BLUE: 'R',
            RED: 'F',
            YELLOW: 'D',
            GREEN: 'L',
            ORANGE: 'B'}

recColors = {WHITE: (255, 255, 255),
             BLUE: (255, 0, 0),
             RED: (0, 0, 255),
             YELLOW: (0, 255, 255),
             GREEN: (0, 255, 0),
             ORANGE: (0, 125, 255)
             }

imgHeight = 480 / 2
imgWidth = 640 / 2
recSize = 55
recPos = [((int(imgWidth - recSize * 2.5 - recSize / 2), int(imgHeight - recSize * 2.5 - recSize / 2)),
           (int(imgWidth - recSize * 2.5 + recSize / 2), int(imgHeight - recSize * 2.5 + recSize / 2))),
          ((int(imgWidth - recSize / 2), int(imgHeight - recSize * 2.5 - recSize / 2)),
           (int(imgWidth + recSize / 2), int(imgHeight - recSize * 2.5 + recSize / 2))),
          ((int(imgWidth + recSize * 2.5 - recSize / 2), int(imgHeight - recSize * 2.5 - recSize / 2)),
           (int(imgWidth + recSize * 2.5 + recSize / 2), int(imgHeight - recSize * 2.5 + recSize / 2))),
          ((int(imgWidth - recSize * 2.5 - recSize / 2), int(imgHeight - recSize / 2)),
           (int(imgWidth - recSize * 2.5 + recSize / 2), int(imgHeight + recSize / 2))),
          # ((int(imgWidth - recSize / 2), int(imgHeight - recSize / 2)),
          #  (int(imgWidth + recSize / 2), int(imgHeight + recSize / 2))),
          ((int(imgWidth + recSize * 2.5 - recSize / 2), int(imgHeight - recSize / 2)),
           (int(imgWidth + recSize * 2.5 + recSize / 2), int(imgHeight + recSize / 2))),
          ((int(imgWidth - recSize * 2.5 - recSize / 2), int(imgHeight + recSize * 2.5 - recSize / 2)),
           (int(imgWidth - recSize * 2.5 + recSize / 2), int(imgHeight + recSize * 2.5 + recSize / 2))),
          ((int(imgWidth - recSize / 2), int(imgHeight + recSize * 2.5 - recSize / 2)),
           (int(imgWidth + recSize / 2), int(imgHeight + recSize * 2.5 + recSize / 2))),
          ((int(imgWidth + recSize * 2.5 - recSize / 2), int(imgHeight + recSize * 2.5 - recSize / 2)),
           (int(imgWidth + recSize * 2.5 + recSize / 2), int(imgHeight + recSize * 2.5 + recSize / 2)))]

def saveCalData(data, fileName):
    with open(fileName, 'w+') as outfile:
        json.dump(data, outfile)

def readCalData(fileName):
    with open(fileName, 'r') as outfile:
        return json.load(outfile)

def resetCalData(fileName):
    with open(fileName, 'w+') as outfile:
        json.dump("", outfile)

def getRectColor(frame, p1, p2, drawFrame):
    cube_frame = frame[p1[0]:p2[0], p1[1]:p2[1]].reshape(-1, 3).T
    h = numpy.median(cube_frame[0])
    s = numpy.median(cube_frame[1])
    v = numpy.median(cube_frame[2])
    color = getColor(h, s, v)
    drawRec(drawFrame, (p1, p2), recColors[color])
    return color


def drawRec(img, pos, color, fill=False):
    thickness = 3
    if fill:
        thickness = -1
    square = cv2.rectangle(img, pos[0], pos[1], color, thickness)  # BGR
    return square


# camera = input("enter the camera number: ")

cHSV = {
    BLUE: {"min": [255, 255, 255], "max": [0, 0, 0]},
    WHITE: {"min": [255, 255, 255], "max": [0, 0, 0]},
    YELLOW: {"min": [255, 255, 255], "max": [0, 0, 0]},
    RED: {"min": [255, 255, 255], "max": [0, 0, 0]},
    ORANGE: {"min": [255, 255, 255], "max": [0, 0, 0]},
    GREEN: {"min": [255, 255, 255], "max": [0, 0, 0]}
}

def getColor(h, s, v):
    global cHSV
    if s in range(int(cHSV[WHITE]["min"][1]), int(cHSV[WHITE]["max"][1])):
        return WHITE
    else:
        if h in range(int(cHSV[YELLOW]["min"][0]), int(cHSV[YELLOW]["max"][0])):
            return YELLOW
        elif h in range(int(cHSV[GREEN]["min"][0]), int(cHSV[GREEN]["max"][0])):
            return GREEN
        elif h in range(int(cHSV[BLUE]["min"][0]), int(cHSV[BLUE]["max"][0])):
            return BLUE
        else:
            if v in range(int(cHSV[ORANGE]["min"][1]), int(cHSV[ORANGE]["max"][1])):
                return ORANGE
            else:
                return RED

def calibrate(frame, p1, p2, color, RST = True):
    global cHSV
    if not RST:
        for i in range(0, 3):
            cHSV[color]["min"][i] = 255
            cHSV[color]["max"][i] = 0

    cube_frame = frame[p1[0]:p2[0], p1[1]:p2[1]].reshape(-1, 3).T
    for i in range(0, 3):
        if numpy.median(cube_frame[i]) < cHSV[color]["min"][i]:
            cHSV[color]["min"][i] = numpy.median(cube_frame[i])
        elif numpy.median(cube_frame[i]) > cHSV[color]["max"][i]:
            cHSV[color]["max"][i] = numpy.median(cube_frame[i])

def setRanges(fileName):
    global cHSV
    cHSV = readCalData(fileName)

cap = cv2.VideoCapture(0)
count = 0
B = False
G = False
R = False
O = False
W = False
Y = False
while True:
    ret, frameRGB = cap.read()
    ret, frameHSV = cap.read()
    cv2.cvtColor(frameRGB, cv2.COLOR_BGR2HSV, frameHSV)

    if cv2.waitKey(1) & 0xFF == ord('b') or B:
        B = True
        if count < 50 and count > 10:
            for p in recPos:
                calibrate(frameHSV, p[0], p[1], BLUE)
            # print(cHSV[BLUE])

        elif count == 110:
            print(cHSV[BLUE], BLUE)
            B = False
            count = 0

        count += 1

    if cv2.waitKey(1) & 0xFF == ord('g') or G:
        G = True
        if count < 50 and count > 10:
            for p in recPos:
                calibrate(frameHSV, p[0], p[1], GREEN)
            # print(cHSV[GREEN])

        elif count == 110:
            print(cHSV[GREEN], GREEN)
            saveCalData(cHSV, calDataFile)
            G = False
            count = 0

        count += 1

    if cv2.waitKey(1) & 0xFF == ord('r') or R:
        R = True
        if count < 50 and count > 10:
            for p in recPos:
                calibrate(frameHSV, p[0], p[1], RED)
            # print(cHSV[RED])

        elif count == 110:
            print(cHSV[RED], RED)
            R = False
            count = 0

        count += 1

    if cv2.waitKey(1) & 0xFF == ord('o') or O:
        O = True
        if count < 50 and count > 10:
            for p in recPos:
                calibrate(frameHSV, p[0], p[1], ORANGE)
            # print(cHSV[ORANGE])

        elif count == 110:
            print(cHSV[ORANGE], ORANGE)
            saveCalData(cHSV, calDataFile)
            O = False
            count = 0

        count += 1

    if cv2.waitKey(1) & 0xFF == ord('w') or W:
        W = True
        if count < 50 and count > 10:
            for p in recPos:
                calibrate(frameHSV, p[0], p[1], WHITE)
            # print(cHSV[WHITE])

        elif count == 110:
            print(cHSV[WHITE], WHITE)
            W = False
            count = 0

        count += 1

    if cv2.waitKey(1) & 0xFF == ord('y') or Y:
        Y = True
        if count < 50 and count > 10:
            for p in recPos:
                calibrate(frameHSV, p[0], p[1], YELLOW)
            # print(cHSV[YELLOW])

        elif count == 110:
            print(cHSV[YELLOW], YELLOW)
            saveCalData(cHSV, calDataFile)
            Y = False
            count = 0

        count += 1

    for p in recPos:
        color = getRectColor(frameHSV, p[0], p[1], frameRGB)
        # print(color)

    cv2.imshow('HSV', frameHSV)
    cv2.imshow('RGB', frameRGB)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('R'):
        print("reset")
        resetCalData(calDataFile)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("ranges set")
        setRanges(calDataFile)


cap.release()
cv2.destroyAllWindows()