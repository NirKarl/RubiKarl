import cv2
import numpy
import json
import time
import sys
import math

camera = 1  # camera port usually 0
cap = cv2.VideoCapture(camera)

calFrames = {"RED": None, "BLUE": None, "GREEN": None, "WHITE": None, "ORANGE": None, "YELLOW": None}
calFileName = "calData.jason"
cubeColors = {"TOP": None, "FRONT": None, "RIGHT": None, "DOWN": None, "LEFT": None, "BACK": None}
imgHeight = 480 / 2
imgWidth = 640 / 2
areaSize = 55
areas = [((int(imgWidth - areaSize * 2.5 - areaSize / 2), int(imgHeight - areaSize * 2.5 - areaSize / 2)),
         (int(imgWidth - areaSize * 2.5 + areaSize / 2), int(imgHeight - areaSize * 2.5 + areaSize / 2))),

         ((int(imgWidth - areaSize / 2), int(imgHeight - areaSize * 2.5 - areaSize / 2)),
         (int(imgWidth + areaSize / 2), int(imgHeight - areaSize * 2.5 + areaSize / 2))),

         ((int(imgWidth + areaSize * 2.5 - areaSize / 2), int(imgHeight - areaSize * 2.5 - areaSize / 2)),
         (int(imgWidth + areaSize * 2.5 + areaSize / 2), int(imgHeight - areaSize * 2.5 + areaSize / 2))),

         ((int(imgWidth - areaSize * 2.5 - areaSize / 2), int(imgHeight - areaSize / 2)),
         (int(imgWidth - areaSize * 2.5 + areaSize / 2), int(imgHeight + areaSize / 2))),

         #  ((int(imgWidth - areaSize / 2), int(imgHeight - areaSize / 2)),
         #  (int(imgWidth + areaSize / 2), int(imgHeight + areaSize / 2))),

         ((int(imgWidth + areaSize * 2.5 - areaSize / 2), int(imgHeight - areaSize / 2)),
         (int(imgWidth + areaSize * 2.5 + areaSize / 2), int(imgHeight + areaSize / 2))),

         ((int(imgWidth - areaSize * 2.5 - areaSize / 2), int(imgHeight + areaSize * 2.5 - areaSize / 2)),
         (int(imgWidth - areaSize * 2.5 + areaSize / 2), int(imgHeight + areaSize * 2.5 + areaSize / 2))),

         ((int(imgWidth - areaSize / 2), int(imgHeight + areaSize * 2.5 - areaSize / 2)),
         (int(imgWidth + areaSize / 2), int(imgHeight + areaSize * 2.5 + areaSize / 2))),

         ((int(imgWidth + areaSize * 2.5 - areaSize / 2), int(imgHeight + areaSize * 2.5 - areaSize / 2)),
         (int(imgWidth + areaSize * 2.5 + areaSize / 2), int(imgHeight + areaSize * 2.5 + areaSize / 2)))]

def drawRec(frame, pos, color=(0,0,0), fill=False):
    thickness = 3
    if fill:
        thickness = -1
    square = cv2.rectangle(frame, pos[0], pos[1], color, thickness)  # BGR
    return square

def saveImage(frame, color):
    print("save image", color)
    calFrames[color] = frame

def saveCalData():
    try:
        global calFrames
        with open(calFileName, 'w+') as outfile:
            json.dump(calFrames, outfile)
    except:
        print("could no save data...", sys.exc_info()[0])

def loadCalData():
    try:
        with open(calFileName, 'r') as outfile:
            return json.load(outfile)
    except FileNotFoundError:
        print("first calibration file hasn't been made yet")
    except:
        print("file data has been corrupted")

def areaDif(area, frame1, frame2):
    dif = []
    for i in range(area[0][0], area[1][0]+1):
        for j in range(area[0][1], area[1][1]+1):
            dif.append((frame1[j][i][0] - frame2[j][i][0], frame1[j][i][1] - frame2[j][i][1], frame1[j][i][2] - frame2[j][i][2]))
    return dif

def getSumOfAbsValue(mat):
    sumValue = [0, 0, 0]
    for i in mat:
        sumValue[0] += numpy.abs(i[0])
        sumValue[1] += numpy.abs(i[1])
        sumValue[2] += numpy.abs(i[2])
    sumValue[0] /= mat.__len__()
    sumValue[1] /= mat.__len__()
    sumValue[2] /= mat.__len__()
    return sumValue

def findBestColorMatch(frame, area):
    print("find best color match for", area)
    global calFrames
    colorsRanking = {"RED": 0, "BLUE": 0, "GREEN": 0, "WHITE": 0, "ORANGE": 0, "YELLOW": 0}
    for i in calFrames:
        print("now getting sum of abs value", i)
        colorsRanking[i] = getSumOfAbsValue(areaDif(area, calFrames[i], frame))

    minColorRank = 1000000
    bestColorMatch = None
    for i in colorsRanking:
        rank = colorsRanking[i][0]**2 + colorsRanking[i][1]**2 + colorsRanking[i][2]**2
        if rank < minColorRank:
            minColorRank = rank
            bestColorMatch = i
        print(i, colorsRanking[i], rank, minColorRank)

    return bestColorMatch

def scanFace(face, frame):
    print("scan face started", face)
    cubeColors[face] = []
    for i in areas:
        cubeColors[face].append(findBestColorMatch(frame, i))
    # cubeColors[face] = map(lambda i: findBestColorMatch(frame, i), areas)
    for i in cubeColors[face]: print(i)

loadCalData()
while(True):
    ret, frameHSV = cap.read()
    for i in areas: drawRec(frameHSV, i)
    cv2.imshow('HSV', frameHSV)

    key = cv2.waitKey(1)

    if key & 0xFF == ord('q'):
        break

    elif key & 0xFF == ord('R'):
        saveImage(frameHSV, "RED")
        print(calFrames["RED"])

    elif key & 0xFF == ord('B'):
        saveImage(frameHSV, "BLUE")
        print(calFrames["BLUE"])

    elif key & 0xFF == ord('W'):
        saveImage(frameHSV, "WHITE")
        print(calFrames["WHITE"])

    elif key & 0xFF == ord('G'):
        saveImage(frameHSV, "GREEN")
        print(calFrames["GREEN"])

    elif key & 0xFF == ord('O'):
        saveImage(frameHSV, "ORANGE")
        print(calFrames["ORANGE"])

    elif key & 0xFF == ord('Y'):
        saveImage(frameHSV, "YELLOW")
        print(calFrames["YELLOW"])

    elif key & 0xFF == ord('A'):
        saveImage(frameHSV, "YELLOW")
        saveImage(frameHSV, "ORANGE")
        saveImage(frameHSV, "BLUE")
        saveImage(frameHSV, "GREEN")
        saveImage(frameHSV, "WHITE")
        saveImage(frameHSV, "RED")
        print("saved them all (and some of your time ;) )")


    elif key & 0xFF == ord('s'):
        saveCalData()

    elif key & 0xFF == ord('f'):
        scanFace("FRONT", frameHSV)

    elif key & 0xFF == ord('p'):
        print(calFrames)

    elif key & 0xFF == ord('P'):
        print(loadCalData())

print(cubeColors)
cap.release()
cv2.destroyAllWindows()