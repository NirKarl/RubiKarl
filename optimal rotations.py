import copy
from termcolor import colored
import kociemba

colors_numbers = {0: "cyan", 1: "blue", 2: "yellow", 3: "red", 4: "green", 5: "grey"}

front = [[0, 2, 8, 6], [1, 5, 7, 3], [24, 9, 47, 44], [26, 15, 45, 38], [25, 12, 46, 41]]
z = [[0, 9, 35, 36],
     [1, 10, 34, 37],
     [2, 11, 33, 38],
     [3, 12, 32, 39],
     [4, 13, 31, 40],
     [5, 14, 30, 41],
     [6, 15, 29, 42],
     [7, 16, 28, 43],
     [8, 17, 27, 44],
     [24, 26, 20, 18],
     [25, 23, 19, 21],
     [45, 47, 53, 51],
     [46, 50, 52, 48]]


class Cube:

    def __init__(self):
        self.cubeState = list(range(54))
        self.colors = ["cyan", "blue", "yellow", "red", "green", "grey"]
        self.rotations = {
            'front': [[0, 2, 8, 6],
                      [1, 5, 7, 3],
                      [24, 9, 47, 44],
                      [26, 15, 45, 38],
                      [25, 12, 46, 41]],
            'z': [[0, 9, 35, 36],
                  [1, 10, 34, 37],
                  [2, 11, 33, 38],
                  [3, 12, 32, 39],
                  [4, 13, 31, 40],
                  [5, 14, 30, 41],
                  [6, 15, 29, 42],
                  [7, 16, 28, 43],
                  [8, 17, 27, 44],
                  [24, 26, 20, 18],
                  [25, 23, 19, 21],
                  [45, 47, 53, 51],
                  [46, 50, 52, 48]],

            'x': [[36, 38, 44, 42],
                  [37, 41, 43, 39],
                  [11, 9, 15, 17],
                  [10, 12, 16, 14],
                  [0, 18, 27, 45],
                  [1, 19, 28, 46],
                  [2, 20, 29, 47],
                  [3, 21, 30, 48],
                  [4, 22, 31, 49],
                  [5, 23, 32, 50],
                  [6, 24, 33, 51],
                  [7, 25, 34, 52],
                  [8, 26, 35, 53]]
        }

    def rotate(self, rotationName, ccw=False):
        rotation = self.rotations[rotationName]
        newCubeState = copy.deepcopy(self.cubeState)
        if ccw:
            for one_rotation in rotation:
                for i in range(one_rotation.__len__() - 1):
                    # print("{}={}".format(i, rotation[i]))
                    newCubeState[one_rotation[i]] = self.cubeState[one_rotation[i + 1]]
                newCubeState[one_rotation[one_rotation.__len__() - 1]] = self.cubeState[one_rotation[0]]

        else:
            for one_rotation in rotation:
                for i in range(one_rotation.__len__() - 1):
                    # print("{}={}".format(i, rotation[i]))
                    newCubeState[one_rotation[i + 1]] = self.cubeState[one_rotation[i]]
                newCubeState[one_rotation[0]] = self.cubeState[one_rotation[one_rotation.__len__() - 1]]

        self.cubeState = newCubeState

    def color_number(num):
        # return colored("{:2d}".format(num), colors_numbers[int(num/9)])
        return colored("{}".format(num).zfill(2), colors_numbers[int(num/9)])

    def __repr__(self):
        retVal = ""
        for row in range(3):
            retVal += "         "
            for col in range(3):
                retVal += Cube.color_number(self.cubeState[18+row*3+col])+" "
            retVal += "\n"
        for row in range(3):
            for col in range(3):
                retVal += Cube.color_number(self.cubeState[36+row*3+col])+" "
            for col in range(3):
                retVal += Cube.color_number(self.cubeState[0+row*3+col])+" "
            for col in range(3):
                retVal += Cube.color_number(self.cubeState[9+row*3+col])+" "
            for col in range(3):
                retVal += Cube.color_number(self.cubeState[35-row*3-col])+" "
            retVal += "\n"
        for row in range(3):
            retVal += "         "
            for col in range(3):
                retVal += Cube.color_number(self.cubeState[45+row*3+col])+" "
            retVal += "\n"
        return retVal



myCube = Cube()
print(myCube)
myCube.rotate('z', True)
myCube.rotate('z', True)
myCube.rotate('front')
myCube.rotate('z')
myCube.rotate('z')
print(myCube)
