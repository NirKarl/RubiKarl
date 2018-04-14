import cv2
import numpy as np
import pickle
import time
import sys
import math

camera = 1  # camera port usually 0
cap = cv2.VideoCapture(camera)

calFrames = {"RED": None, "BLUE": None, "GREEN": None, "WHITE": None, "ORANGE": None, "YELLOW": None}
calFileName = "calData.dat"
cubeOrientationFileName = "orientationData.dat"
cubeColors = {"UP": None, "FRONT": None, "RIGHT": None, "DOWN": None, "LEFT": None, "BACK": None}
forKociemba = {"RED": "F", "BLUE": "R", "GREEN": "L", "WHITE": "U", "ORANGE": "B", "YELLOW": "D"}
cubeColorArrangement = []
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
        with open(calFileName, 'w+b') as outfile:
            pickle.dump(calFrames, outfile)
    except TypeError as e:
        print(e)
    except:
        print("could no save data...", sys.exc_info()[0])

def loadCalData():
    try:
        with open(calFileName, 'rb') as outfile:
            print("loading")
            return pickle.load(outfile)
    except FileNotFoundError:
        print("first calibration file hasn't been made yet")
    except:
        print("file data has been corrupted")

def saveCubeOrientation():
    try:
        global cubeColorArrangement
        with open(cubeOrientationFileName, 'w+b') as outfile:
            pickle.dump(calFrames, outfile)
    except TypeError as e:
        print(e)
    except:
        print("could no save data...", sys.exc_info()[0])

def areaDif(area, frame1, frame2):
    dif = []
    for i in range(area[0][0], area[1][0]+1):
        for j in range(area[0][1], area[1][1]+1):
            #print(frame1[j][i] - frame2[j][i])
            dif.append(np.subtract(frame1[j][i], frame2[j][i]))
    return dif

def getSumOfAbsValues(mat):
    sumValue = [0, 0, 0]
    for i in mat:
        sumValue[0] += np.abs(i[0])
        sumValue[1] += np.abs(i[1])
        sumValue[2] += np.abs(i[2])
    # print(mat.__len__(), sumValue)
    sumValue[0] /= mat.__len__()
    sumValue[1] /= mat.__len__()
    sumValue[2] /= mat.__len__()
    return sumValue

def findBestColorMatch(frame, area):
    # print("find best color match for", area)
    global calFrames
    colorsRanking = {"RED": 0, "BLUE": 0, "GREEN": 0, "WHITE": 0, "ORANGE": 0, "YELLOW": 0}
    for i in calFrames:
        # print("now getting sum of abs value", i)
        colorsRanking[i] = getSumOfAbsValues(areaDif(area, calFrames[i], frame))

    minColorRank = 1000000
    bestColorMatch = None
    for i in colorsRanking:
        rank = math.sqrt(colorsRanking[i][0]**2 + colorsRanking[i][1]**2 + colorsRanking[i][2]**2)
        if rank < minColorRank:
            minColorRank = rank
            bestColorMatch = i
        # print(i, colorsRanking[i], rank)

    return bestColorMatch

def scanFace(face, frame):
    print("scan face started", face)
    cubeColors[face] = []
    for i in areas:
        #i = areas[3]
        cubeColors[face].append(findBestColorMatch(frame, i))
        # cubeColors[face] = map(lambda i: findBestColorMatch(frame, i), areas)
    for i in cubeColors[face][0:4]: print(i)
    print("*")
    for i in cubeColors[face][4:9]: print(i)

def sortCubeColor(colorsToFaces):
    global cubeColors
    global cubeColorArrangement
    for c in ["UP", "RIGHT", "FRONT", "DOWN", "LEFT", "BACK"]:
        f = colorsToFaces[c]
        cubeColorArrangement.append(translateColorToFace(colorsToFaces, cubeColors[f][0:4]))
        cubeColorArrangement.append(c[0])
        cubeColorArrangement.append(translateColorToFace(colorsToFaces, cubeColors[f][4:9]))
    return cubeColorArrangement

def translateColorToFace(colorsToFaces, colors):
    faces = []
    for c in colors:
        faces.append(colorsToFaces[c])
    return faces



calFrames = loadCalData()
print("loaded successfully")

while(True):
    ret, a = cap.read()
    for i in range(1, 9):
        ret, b = cap.read()
        for i in areas: drawRec(b, i)
        cv2.imshow('HSV', b)
        a = np.add(a, b, dtype=np.int16)
    frameHSV = a/10
    #ret, frameHSV = cap.read()
    # cv2.cvtColor(frameHSV, cv2.COLOR_BGR2HSV, frameHSV)
    # cv2.imshow('HSV', frameHSV)

    key = cv2.waitKey(1)

    if key & 0xFF == ord('q'):
        break

    elif key & 0xFF == ord('R'):
        saveImage(frameHSV, "RED")

    elif key & 0xFF == ord('B'):
        saveImage(frameHSV, "BLUE")

    elif key & 0xFF == ord('W'):
        saveImage(frameHSV, "WHITE")

    elif key & 0xFF == ord('G'):
        saveImage(frameHSV, "GREEN")

    elif key & 0xFF == ord('O'):
        saveImage(frameHSV, "ORANGE")

    elif key & 0xFF == ord('Y'):
        saveImage(frameHSV, "YELLOW")

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

    elif key & 0xFF == ord('r'):
        scanFace("RIGHT", frameHSV)

    elif key & 0xFF == ord('u'):
        scanFace("UP", frameHSV)

    elif key & 0xFF == ord('l'):
        scanFace("LEFT", frameHSV)

    elif key & 0xFF == ord('b'):
        scanFace("BACK", frameHSV)

    elif key & 0xFF == ord('d'):
        scanFace("DOWN", frameHSV)

    elif key & 0xFF == ord('P'):
        calFrames = loadCalData()
        print("loaded successfully")

    elif key & 0xFF == ord('S'):
        saveCubeOrientation()
        print(sortCubeColor(forKociemba))

print(cubeColors)
cap.release()
cv2.destroyAllWindows()