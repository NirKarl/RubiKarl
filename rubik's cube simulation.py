import pygame
import math
import time
import copy

pygame.init()
window = pygame.display.set_mode((1000, 1000))


scale = (10, 10, 10)
black = (0, 0, 0)
white = (255, 255, 255)


class Matrix2D:

    def __init__(self, flatMat, size):
        self.size = size
        self.flatMat = flatMat
        self.matrix = []
        for i in range(self.size[0]):
            row = []
            for j in range(self.size[1]):
                row.append(self.flatMat[i*self.size[1]+j])
            self.matrix.append(row)

    def flat(self):
        return self.flatMat

    def __add__(self, other):
        rMat = None
        if type(other) == int or type(other) == float:
            rMat = Matrix2D(list(map(lambda x: x+other, self.flat())), self.size)

        elif self.size == other.size:
            rMat = Matrix2D((list(map(lambda x: self.flat()[x] + other.flat()[x], range(self.flat().__len__())))), self.size)

        return rMat

    def __mul__(self, other):
        rMat = None
        if type(other) is int or type(other) is float:
            rMat = Matrix2D(list(map(lambda x: x * other, self.flatMat)), self.size)

        elif self.size[1] == other.size[0]:
            flatMat = []
            for i in range(self.size[0]*other.size[1]):
                flatMat.append(0)
            for i in range(self.size[0]):
                for j in range(other.size[1]):
                    for k in range(other.size[0]):
                        flatMat[i*other.size[1]+j] += self.matrix[i][k] * other.matrix[k][j]
            rMat = Matrix2D(flatMat, (self.size[0], other.size[1]))

        else:
            print("matrix 1 rows and matrix 2 columns do not match...")

        return rMat

    def __repr__(self):
        return self.matrix.__repr__()


class RotationMatrix3D(Matrix2D):

    def __init__(self, teta, axis):
        if axis == "x":
            Matrix2D.__init__(self, [1, 0, 0, 0, math.cos(teta), -math.sin(teta), 0, math.sin(teta), math.cos(teta)], (3, 3))

        elif axis == "y":
            Matrix2D.__init__(self, [math.cos(teta), 0, math.sin(teta), 0, 1, 0, -math.sin(teta), 0, math.cos(teta)], (3, 3))

        elif axis == "z":
            Matrix2D.__init__(self, [math.cos(teta), -math.sin(teta), 0, math.sin(teta), math.cos(teta), 0, 0, 0, 1], (3, 3))


class Point(Matrix2D):

    def __init__(self, xyz):
        Matrix2D.__init__(self, xyz, (3, 1))

    def rotate(self, teta, axis):
        originalPoint = copy.deepcopy(self.flat())
        points = Point(list(map(lambda x: 0, self.flat())))
        r = RotationMatrix3D(teta, axis)
        p = (r * points) + originalPoint
        f = p.flat()
        return Point(f)

    def translate(self, xyz):
        return Point(self + Point(xyz).flat())

    def project(self, projectionMat, distance=200):
        return (projectionMat*(distance / (distance - self.flat()[2])))*self

    def screenLocation(self, projectionMat, screenSize=1000, distance=200):
        return list(map(lambda x: math.floor(x) + int(screenSize / 2), Matrix2D.flat(self.project(projectionMat, distance))))

    def draw(self, projectionMat, surface, size=6, color=white, screenSize=1000, distance=200):
        pygame.draw.circle(surface, color, self.screenLocation(projectionMat, screenSize, distance), size)

class Cube:

    def __init__(self, pos, scale):
        vertices = [
            (pos[0]-scale, pos[1]-scale, pos[2]+scale),
            (pos[0]-scale, pos[1]+scale, pos[2]+scale),
            (pos[0]+scale, pos[1]+scale, pos[2]+scale),
            (pos[0]+scale, pos[1]-scale, pos[2]+scale),
            (pos[0]-scale, pos[1]-scale, pos[2]-scale),
            (pos[0]-scale, pos[1]+scale, pos[2]-scale),
            (pos[0]+scale, pos[1]+scale, pos[2]-scale),
            (pos[0]+scale, pos[1]-scale, pos[2]-scale)
        ]
        self.points = list(map(lambda vertex: Point(vertex), vertices))

    def rotate(self, teta, axis):
        self.points = list(map(lambda x: Point((RotationMatrix3D(teta, axis) * x).flat()), self.points))
        # originalPoints = copy.deepcopy(self.points)
        # points = list(map(lambda x: Point([0, 0, 0]), self.points))
        # points = list(map(lambda x: Point((RotationMatrix3D(teta, axis) * x).flat()), points))
        # for i in range(self.points.__len__()):
        #     self.points[i] = Point((points[i] + originalPoints[i]).flat())

    def translate(self, xyz):
        self.points = list(map(lambda x: Point((x+xyz).flat()), self.points))

    def draw(self, projectionMat, surface, size=4, width=3, pColor=white, lColor=white, screenSize=1000, distance=200):
        for point in self.points:
            point.draw(projectionMat, surface, size, pColor, distance=distance)
        for i in range(4):
            pygame.draw.line(surface, lColor, self.points[i].screenLocation(projectionMat, screenSize, distance), self.points[(i+1) % 4].screenLocation(projectionMat, screenSize, distance), width)
            pygame.draw.line(surface, lColor, self.points[i+4].screenLocation(projectionMat, screenSize, distance), self.points[((i+1) % 4)+4].screenLocation(projectionMat, screenSize, distance), width)
            pygame.draw.line(surface, lColor, self.points[i].screenLocation(projectionMat, screenSize, distance), self.points[i+4].screenLocation(projectionMat, screenSize, distance), width)


# mat1 = Matrix2D([6, 5, 3, 9, 5, 7, 1, 2, 3], (3, 3))
# mat2 = Matrix2D([8, 8, 12, 2, 2, 9, 6, 10, 1, 2, 7, 4], (3, 4))
# mat3 = Matrix2D([1,0,-1,3],(2,2))
# mat4 = Matrix2D([3,1,2,1],(2,2))
# print(mat3+mat4)
# print(mat4+5)

scale = 10
ortho = Matrix2D([1, 0, 0, 0, 1, 0], (2, 3))
perspective = 10

vertices = [
    (-50, -50, 50),
    (-50, 50, 50),
    (50, 50, 50),
    (50, -50, 50),
    (-50, -50, -50),
    (-50, 50, -50),
    (50, 50, -50),
    (50, -50, -50)
]

points = list(map(lambda vertex: Point(vertex), vertices))

cube = Cube((0, 0, 0), 50)
# cube.translate(Point([50, 0, 0]))

beta = 0.0

clock = pygame.time.Clock()
while True:
    distance = 300+math.sin(beta)*100
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    cube.rotate(0.09, "x")
    cube.rotate(0.06, "y")
    cube.rotate(0.03, "z")
    cube.draw(ortho, window, distance=distance)
    pygame.display.flip()
    window.fill(black)
    beta += 0.1
