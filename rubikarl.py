from time import sleep
try:
    import RPi.GPIO as GPIO
except:
    print("no pi i guess...")
import kociemba
import re
import pygame
import os.path
import random
import pickle
import sys
import time
import math

pygame.init()
im = lambda im: os.path.join("images", im)

window_height = 90 * 3  # 270
window_length = 90 * 4  # 360

cubeOrientationFileName = "orientationData.dat"

face_color = 0
ok_button = ((270, 240), im("ok.jpg"))
solve_button = ((240, 240), im("solve.jpg"))
scramble_button = ((300, 240), im("scramble.jpg"))
face_button = ((270, 210), None)
CCW_button = ((240, 210), im("CW.jpg"))
CW_button = ((300, 210), im("CCW.jpg"))
test1_button = ((240, 0), im("test1.jpg"))
test2_button = ((270, 0), im("test2.jpg"))
test3_button = ((300, 0), im("test3.jpg"))
test4_button = ((240, 30), im("test4.jpg"))
test5_button = ((270, 30), im("test5.jpg"))
test6_button = ((300, 30), im("test6.jpg"))
auto_cal_button = ((0, 0), im("auto_cal.png"))
manual_cal_button = ((0, 135), im("manual_cal.png"))

stop = False


def is_button_pressed(button):
    return button[0][0] < pygame.mouse.get_pos()[0] < button[0][0] + 30 \
           and \
           button[0][1] < pygame.mouse.get_pos()[1] < button[0][1] + 30


gameDisplay = pygame.display.set_mode((window_length, window_height))

clock = pygame.time.Clock()
Exit = False

faces = ["U", "R", "F", "D", "L", "B"]
raw_tiles = ["white.jpg", "green.jpg", "orange.jpg", "yellow.jpg", "blue.jpg", "red.jpg"]
tiles = [im(tile) for tile in raw_tiles]

pos = {}
for t in range(1, 10):
    pos["U" + str(t)] = (90 + (t - 1) % 3 * 30, 0 + int((t - 1) / 3) * 30)
    pos["L" + str(t)] = (0 + (t - 1) % 3 * 30, 90 + int((t - 1) / 3) * 30)
    pos["F" + str(t)] = (90 + (t - 1) % 3 * 30, 90 + int((t - 1) / 3) * 30)
    pos["R" + str(t)] = (180 + (t - 1) % 3 * 30, 90 + int((t - 1) / 3) * 30)
    pos["B" + str(t)] = (270 + (t - 1) % 3 * 30, 90 + int((t - 1) / 3) * 30)
    pos["D" + str(t)] = (90 + (t - 1) % 3 * 30, 180 + int((t - 1) / 3) * 30)

colors = {}
colors_count = []

BETWEEN_ROTATIONS = 0.5

def readCubeOrientation(fileName):
    global colors_count
    try:
        with open(fileName, 'rb') as outfile:
            print("loading")
            cubeInfo = pickle.load(outfile)
            print("read: ", cubeInfo)
            colors_count = []
            for f in faces:
                colors_count.append(cubeInfo.count(f))
            print(colors_count)
    except FileNotFoundError:
        print("first calibration file hasn't been made yet")
    # except:
    #     print("file data has been corrupted")
    tilesInfo = translateCubeInfo(cubeInfo)
    print(tilesInfo)
    count = tilesInfo.__len__() - 1
    for f in range(0, 6):
        for i in range(1, 10):
            colors[faces[f] + str(i)] = tilesInfo[count]
            count -= 1

def translateCubeInfo(cubeInfo):
    tilesInfo = []
    # faces = ["U", "R", "F", "D", "L", "B"]
    translation = {"U": 0, "R": 1, "F": 2, "D": 3, "L": 4, "B": 5}
    for c in cubeInfo:
        tilesInfo.append(translation[c])
    return tilesInfo

def init(auto=False):
    global colors_count
    if not auto:
        colors_count = [9, 9, 9, 9, 9, 9]
        for f in range(0, 6):
            for i in range(1, 10):
                colors[faces[f] + str(i)] = f
    else:
        import impnir
        readCubeOrientation(cubeOrientationFileName)

DIR = 24
STEP = 23
UNSLEEP = {"U": 26, "R": 6, "F": 13, "D": 5, "L": 19, "B": 11}
# ADDITION = {'Full': {"U": [18, 1000], "R": [25, 23], "F": [28, 28], "D": [22, 23], "L": [18, 1000], "B": [60, 30]}, 'Half': {"U": [18, 1000], "R": [25, 23], "F": [28, 28], "D": [22, 23], "L": [18, 1000], "B": [60, 30]}, '1/4': {"U": [18, 1000], "R": [25, 23], "F": [28, 28], "D": [22, 23], "L": [18, 1000], "B": [60, 30]}, '1/8': {"U": [18, 1000], "R": [25, 23], "F": [28, 28], "D": [22, 23], "L": [18, 1000], "B": [60, 30]}, '1/16': {"U": [18, 1000], "R": [25, 23], "F": [28, 28], "D": [22, 23], "L": [18, 1000], "B": [60, 30]}, '1/32': {"U": [18, 1000], "R": [25, 23], "F": [28, 28], "D": [22, 23], "L": [18, 1000], "B": [60, 30]}}
ADDITION = {'Full': {"U": [1000, 1000],
                     "R": [1000, 1000],
                     "F": [1000, 1000],
                     "D": [1000, 1000],
                     "L": [1000, 1000],
                     "B": [1000, 1000]},
            'Half': {"U": [20, 1000],
                     "R": [1000, 1000],
                     "F": [1000, 1000],
                     "D": [10, 10],
                     "L": [1000, 1000],
                     "B": [1000, 1000]},
            '1/4': {"U": [1000, 1000],
                    "R": [50, 50],
                    "F": [20, 20],
                    "D": [20, -50],
                    "L": [1000, 1000],
                    "B": [20, 20]},
            '1/8': {"U": [1000, 1000],
                    "R": [1000, 1000],
                    "F": [1000, 1000],
                    "D": [1000, 1000],
                    "L": [1000, 1000],
                    "B": [1000, 1000]},
            '1/16': {"U": [1000, 1000],
                     "R": [1000, 1000],
                     "F": [1000, 1000],
                     "D": [1000, 1000],
                     "L": [1000, 1000],
                     "B": [1000, 1000]},
            '1/32': {"U": [1000, 1000],
                     "R": [1000, 1000],
                     "F": [20, 20],
                     "D": [1000, 1000],
                     "L": [1000, 1000],
                     "B": [1000, 1000]}}
CW = 0
CCW = 1
SPR = 200  # step per revolution
res = '1/4'
MODE = (14, 15, 18)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 1, 1)}
RESOLUTION_FACTOR = {'Full': 1,
                     'Half': 2,
                     '1/4': 4,
                     '1/8': 8,
                     '1/16': 16,
                     '1/32': 32}

step_count = (int(SPR / 4) * RESOLUTION_FACTOR[res])
delay = 0.01 / (32 * RESOLUTION_FACTOR[res])


def changeResolution(resolution):
    resolutions = {'Full': 'Half', 'Half': '1/4', '1/4': '1/8', '1/8': '1/16', '1/16': '1/32', '1/32': 'Full'}
    GPIO.output(MODE, RESOLUTION[resolutions[resolution]])
    global res
    global step_count
    global delay
    res = resolutions[res]
    step_count = (int(SPR / 4) * RESOLUTION_FACTOR[res])
    delay = 0.01 / (32 * RESOLUTION_FACTOR[res])
    print(res, step_count)


def pi_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.output(DIR, 0)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(STEP, 0)
    for u in UNSLEEP:
        GPIO.setup(UNSLEEP[u], GPIO.OUT)
        GPIO.output(UNSLEEP[u], 0)
    GPIO.setup(MODE, GPIO.OUT)
    GPIO.output(MODE, RESOLUTION[res])

try:
    pi_init()
    isPi = True
except:
    print("no pi i guess...")
    isPi = False

UNSLEEP_gpio = [UNSLEEP[u] for u in faces]


def rotation(face, direction=CW):
    global res
    unsleep = UNSLEEP[face]
    print("rotation: ", face, "(", unsleep, ")", direction)
    print("step count & delay:",  int(step_count * (1 - 1 / ADDITION[res][face][direction])), delay)
    GPIO.output(unsleep, GPIO.HIGH)
    sleep(delay)
    GPIO.output(DIR, direction)
    sleep(0.01)
    for i in range(int(step_count * (1 - 1 / ADDITION[res][face][direction]))):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    sleep(0.01)
    GPIO.output(unsleep, GPIO.LOW)
    sleep(BETWEEN_ROTATIONS)


def check_events():
    global Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                init()

        if event.type == pygame.MOUSEBUTTONDOWN:
            check_pos(pygame.mouse.get_pos(), event.button)


def pi(stop):
    commands = re.split(r'\s+', solution)
    for i in commands:
        if stop:
            while pygame.event.wait().type != pygame.KEYDOWN:
                None
            time.sleep(0.1)
        check_events()
        if i.__len__() == 1:
            rotation(i, CW)
        if i.__len__() == 2:
            if i[1] == "'":
                # print(i[0])
                rotation(i[0], CCW)
            else:
                rotation(i[0], CW)
                rotation(i[0], CW)


def background():
    backgroundImage = pygame.image.load(im("background.jpg"))
    gameDisplay.blit(backgroundImage, (0, 0))


def display_tile(color, place):
    tileImage = pygame.image.load(color)
    gameDisplay.blit(tileImage, place)


def change_color(tile, click):
    colors_count[colors[tile]] -= 1
    if click == 1:  # 1 left mouse click
        colors[tile] = (colors[tile] + 1) % 6
    elif click == 3:  # 3 right mouse click
        colors[tile] = (colors[tile] - 1) % 6
    colors_count[colors[tile]] += 1


def is_balanced():
    for i in colors_count:
        if i != 9:
            return False
    return True


solution = ""


def solve_cube(keyQ):
    try:
        global solution
        resolution = revers_solution(kociemba.solve('UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB', translate()))
        print('the reversed solution: ', resolution)
        solution = kociemba.solve(translate(), 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB')
        print('the straight solution: ', solution)
        if solution.__len__() > resolution.__len__():
            solution = resolution
        print('chosen solution: ', solution)
        pi(keyQ)
    except:
        print("The cube arrangement is imposable to solve!")


def check_pos(pos1, click):
    global solution

    for c in colors:
        if c[1] != "5":  # 5 is a middle tile
            if pos[c][0] < pos1[0] < pos[c][0] + 30 and pos[c][1] < pos1[1] < pos[c][1] + 30:
                change_color(c, click)
                break

    if is_button_pressed(face_button):
        global face_color
        face_color = (face_color + 1) % 6

    elif is_button_pressed(CW_button):
        rotation(faces[face_color], CW)
        print(raw_tiles[face_color] + ", CW")

    elif is_button_pressed(CCW_button):
        rotation(faces[face_color], CCW)
        print(raw_tiles[face_color] + ", CCW")


    elif is_button_pressed(ok_button) and is_balanced():
        solve_cube(True)

    elif is_button_pressed(solve_button) and is_balanced():
        solve_cube(False)

    elif is_button_pressed(test1_button):
        changeResolution(res)

    elif is_button_pressed(test3_button):
        readCubeOrientation(cubeOrientationFileName)

    elif is_button_pressed(test2_button):
        try:
            print('now saving')
            global cubeColorArrangement
            data = []
            for f in range(0, 6):
                for i in range(1, 10):
                    data.insert(0, faces[colors[faces[f] + str(i)]])
            with open('manualArrangement.dat', 'w+b') as outfile:
                pickle.dump(data, outfile)
                print('saved:', data)
        except TypeError as e:
            print(e)
        except:
            print("could no save data...", sys.exc_info()[0])

    elif is_button_pressed(test5_button):
        readCubeOrientation('manualArrangement.dat')

    elif is_button_pressed(test6_button):
        solution = kociemba.solve('UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB', translate())
        print(solution)
        try:
            pi(False)
            None
        except:
            print("I SAID NO PI!!! DON'T PLAY WITH ME!")

    elif is_button_pressed(scramble_button):
        numOfRotations = random.randint(6, 31)
        faces_array = ["R", "L", "F", "B", "U", "D"]
        directions_array = [CW, CCW]
        for i in range(0, numOfRotations):
            face = random.choice(faces_array)
            direction = random.choice(directions_array)
            rotation(face, direction)

    elif is_button_pressed(test4_button):
        while not stop:
            for i in range(0, 3):
                rotation("F")
                rotation("R")
                rotation("U")
                rotation("R", CCW)
                rotation("U", CCW)
                rotation("F", CCW)
            for i in range(0, 100):
                check_events()
            sleep(3)
            while not stop:
                for i in range(0, 3):
                    rotation("F")
                    rotation("R")
                    rotation("U")
                    rotation("R", CCW)
                    rotation("U", CCW)
                    rotation("F", CCW)
                for i in range(0, 100):
                    check_events()
                sleep(3)


def translate():
    arr = ""
    for f in range(0, 6):
        for i in range(1, 10):
            arr += faces[colors[faces[f] + str(i)]]
    return arr

def revers_solution(sol):
    steps = sol.split(' ')
    new_steps = []
    for step in reversed(steps):
        if step.__len__() == 1:
            new_steps.append(step + "'")
        elif step[1] == "'":
            new_steps.append(step[0])
        else:
            new_steps.append(step)  # this is like R2 F2 etc.
    return ' '.join(new_steps)

exit_cal = False
while (not exit_cal):
    display_tile(manual_cal_button[1], manual_cal_button[0])
    display_tile(auto_cal_button[1], auto_cal_button[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_cal = True
            Exit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            exit_cal = True
            if pygame.mouse.get_pos()[1] < 135:
                init(True)
            else:
                init(False)

    pygame.display.update()
    clock.tick(60)
# init(input().lower() != "true")

while not Exit:
    background()
    # time.sleep(0.001)
    for c in colors:
        display_tile(tiles[colors[c]], pos[c])

    display_tile(scramble_button[1], scramble_button[0])
    display_tile(tiles[face_color], face_button[0])
    display_tile(CW_button[1], CW_button[0])
    display_tile(CCW_button[1], CCW_button[0])
    display_tile(test1_button[1], test1_button[0])
    display_tile(test2_button[1], test2_button[0])
    display_tile(test3_button[1], test3_button[0])
    display_tile(test4_button[1], test4_button[0])
    display_tile(test5_button[1], test5_button[0])
    display_tile(test6_button[1], test6_button[0])

    if is_balanced():
        display_tile(ok_button[1], ok_button[0])
        display_tile(solve_button[1], solve_button[0])

    check_events()

    pygame.display.update()
    clock.tick(60)
pygame.quit()
try:
    if isPi:
        pi_init()
    GPIO.cleanup()
except:
    print("too lazy to 'clean up'...")
