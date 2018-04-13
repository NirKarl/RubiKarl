import cv2
import numpy as np
import json
import time
import sys
import math

camera = 1  # camera port usually 0
cap = cv2.VideoCapture(camera)
c = 0
while(c < 30):
    ret, frameRGB1 = cap.read()
    ret, frameRGB2 = cap.read()
    c += 1
    print(c)

print("now")
ret, frameRGB1 = cap.read()
ret, frameRGB2 = cap.read()
diff = np.subtract(frameRGB1, frameRGB2, dtype=np.int16)
print(frameRGB1[100:110, 50:60])
print(frameRGB2[100:110, 50:60])
print(diff[100:110, 50:60])
cap.release()
cv2.destroyAllWindows()