import cv2
import numpy
import matplotlib as plt

# img = cv2.imread('G:/Nir/Desktop/test_pic.jpg', cv2.IMREAD_COLOR)
# cv2.line(img, (100, 50), (150, 100), (255, 255, 255), 15)  # BGR
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

imgHeight = 480/2
imgWidth = 640/2
recSize = 35
BGR_colors = {"U": (255, 255, 255), "R": (255, 0, 0), "F": (0, 0, 255), "L": (0, 255, 0), "B": (0, 125, 255), "D": (0, 255, 255), "Empty": (0, 0, 0)}  # BGR
recPos = [((int(imgWidth - recSize * 2.5 - recSize / 2), int(imgHeight - recSize * 2.5 - recSize / 2)), (int(imgWidth - recSize * 2.5 + recSize / 2), int(imgHeight - recSize * 2.5 + recSize / 2))),
          ((int(imgWidth - recSize / 2), int(imgHeight - recSize * 2.5 - recSize / 2)), (int(imgWidth + recSize / 2), int(imgHeight - recSize * 2.5 + recSize / 2))),
          ((int(imgWidth + recSize * 2.5 - recSize / 2), int(imgHeight - recSize * 2.5 - recSize / 2)), (int(imgWidth + recSize * 2.5 + recSize / 2), int(imgHeight - recSize * 2.5 + recSize / 2))),
          ((int(imgWidth - recSize * 2.5 - recSize / 2), int(imgHeight - recSize / 2)), (int(imgWidth - recSize * 2.5 + recSize / 2), int(imgHeight + recSize / 2))),
          ((int(imgWidth - recSize / 2), int(imgHeight - recSize / 2)), (int(imgWidth + recSize / 2), int(imgHeight + recSize / 2))),
          ((int(imgWidth + recSize * 2.5 - recSize / 2), int(imgHeight - recSize / 2)), (int(imgWidth + recSize * 2.5 + recSize / 2), int(imgHeight + recSize / 2))),
          ((int(imgWidth - recSize * 2.5 - recSize / 2), int(imgHeight + recSize * 2.5 - recSize / 2)), (int(imgWidth - recSize * 2.5 + recSize / 2), int(imgHeight + recSize * 2.5 + recSize / 2))),
          ((int(imgWidth - recSize / 2), int(imgHeight + recSize * 2.5 - recSize / 2)), (int(imgWidth + recSize / 2), int(imgHeight + recSize * 2.5 + recSize / 2))),
          ((int(imgWidth + recSize * 2.5 - recSize / 2), int(imgHeight + recSize * 2.5 - recSize / 2)), (int(imgWidth + recSize * 2.5 + recSize / 2), int(imgHeight + recSize * 2.5 + recSize / 2)))]

colorsRanges = {'yellow': ((17, 100, 100), (40, 255, 255)),
                'red': ((17, 100, 100), (40, 255, 255)),
                'blue': ((100, 100, 100), (140, 255, 255)),
                'orange': ((3, 100, 100), (15, 255, 255)),
                'white': ((0, 0, 255), (0, 10, 255)),
                'green': ((48, 100, 100), (72, 255, 255))
                }

cap = cv2.VideoCapture(0)

def drawRec(img, pos, color, fill=False):
    thickness = 3
    if fill:
        thickness = -1
    line = cv2.rectangle(frame, pos[0], pos[1], color, thickness)  # BGR
    return line

def avgColor(img, pos):
    sumB = 0
    sumG = 0
    sumR = 0
    dev = 0
    for i in range(pos[0][0], pos[1][0]):
        for j in range(pos[0][1], pos[1][1]):
            px = img[pos[0], pos[1]]
            sumB += px[0][0]
            sumG += px[0][1]
            sumR += px[0][2]
            dev += 1
    return (sumB / dev, sumG / dev, sumR / dev)

while True:
    ret, frame = cap.read()
    # cv2.cvtColor(frame, )
    for p in recPos:
        if avgColor(frame, p)[0] > colorsRanges["blue"][0][0] and avgColor(frame, p)[0] < colorsRanges["blue"][1][0] and avgColor(frame, p)[1] > colorsRanges["blue"][0][1] and avgColor(frame, p)[1] < colorsRanges["blue"][1][1] and avgColor(frame, p)[2] > colorsRanges["blue"][0][2] and avgColor(frame, p)[2] < colorsRanges["blue"][1][2]:  # Blue
            drawRec(frame, p, BGR_colors["R"])

        elif avgColor(frame, p)[1] > 0 and avgColor(frame, p)[1] < 255:  # Green
            drawRec(frame, p, BGR_colors["L"])

        else:
            drawRec(frame, p, BGR_colors["Empty"])
    c = avgColor(frame, recPos[5])
    print(c)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()