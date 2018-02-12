from time import sleep
import RPi.GPIO as GPIO
import kociemba
import re
import pygame
import os.path

pygame.init()
im = lambda im: os.path.join("images", im)

window_height = 90*3
window_length = 90*4

face_color = 0
ok_button = ((270, 240), im("ok.jpg"))
solve_button = ((240, 240), im("solve.jpg"))
scramble_button = ((300, 240), im("scramble.jpg"))
face_button = ((270, 210), None)
CW_button = ((240, 210), im("CW.jpg"))
CCW_button = ((300, 210), im("CCW.jpg"))
test1_button = ((240, 0), im("test1.jpg"))
test2_button = ((270, 0), im("test2.jpg"))
test3_button = ((300, 0), im("test3.jpg"))
test4_button = ((240, 30), im("test4.jpg"))
test5_button = ((270, 30), im("test5.jpg"))
test6_button = ((300, 30), im("test6.jpg"))


def is_button_pressed(button):
    return button[0][0] < pygame.mouse.get_pos()[0] < button[0][0] + 30 \
           and \
           button[0][1] < pygame.mouse.get_pos()[1] < button[0][1] + 30

gameDisplay = pygame.display.set_mode((window_length, window_height))

clock = pygame.time.Clock()
Exit = False

faces = ["U", "R", "F", "D", "L", "B"]
raw_tiles = ["white.jpg", "blue.jpg", "red.jpg", "yellow.jpg", "green.jpg", "orange.jpg"]
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

def init():
    global colors_count
    colors_count = [9, 9, 9, 9, 9, 9]
    for f in range(0, 6):
        for i in range(1, 10):
            colors[faces[f] + str(i)] = f

init()

DIR = 21
STEP = 20
UNSLEEP = {"U": 11, "R": 26, "F": 19, "D": 13, "L": 6, "B": 5}
CW = 1
CCW = 0
SPR = 200
res = '1/32'
MODE = (14, 15, 18)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
step_count = int(SPR * 8 * (27 / 26))
delay = 0.0104 / 32

def changeResolution(resolution):
    resolutions = {'Full': 'Half', 'Half': '1/4', '1/4': '1/8', '1/8': '1/16', '1/16': '1/32', '1/32': 'Full'}
    GPIO.output(MODE, RESOLUTION[resolutions[resolution]])
    global res
    res = resolutions[res]
    print(res)


def pi_init():
    None
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    for u in UNSLEEP:
        GPIO.setup(UNSLEEP[u], GPIO.OUT)
    GPIO.output(DIR, CW)
    GPIO.setup(MODE, GPIO.OUT)
    GPIO.output(MODE, RESOLUTION['1/32'])

pi_init()

UNSLEEP_gpio = [UNSLEEP[u] for u in faces]

def rotation(unsleep, direction):
    None
    print("rotation: ", unsleep, direction)
    gpios = {11: "U", 26: "R", 19: "F", 13: "D", 6: "L", 5: "B"}
    GPIO.output(unsleep, GPIO.HIGH)
    GPIO.output(DIR, direction)
    # print("Face: {1} - {2} | direction: {3}".format(unsleep, gpios[unsleep], direction))
    for i in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    GPIO.output(unsleep, GPIO.LOW)


def pi():
    None
    commands = re.split(r'\s*', solution)
    for i in commands:
        if i.__len__() == 1:
            rotation(UNSLEEP[i], CW)
        if i.__len__() == 2:
            if i[1] == "'":
                print(UNSLEEP[i[0]])
                rotation(UNSLEEP[i[0]], CCW)
            else:
                rotation(UNSLEEP[i[0]], CW)
                rotation(UNSLEEP[i[0]], CW)


def background():
    backGrondImage = pygame.image.load(im("background.jpg"))
    gameDisplay.blit(backGrondImage, (0, 0))

def display_tile(color, place):
    cardImage = pygame.image.load(color)
    gameDisplay.blit(cardImage, place)

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
def check_pos(pos1, click):
    global solution

    for c in colors:
        if c[1] != "5":  # 5 is a middle tile
            if pos[c][0] < pos1[0] < pos[c][0]+30 and pos[c][1] < pos1[1] < pos[c][1]+30:
                change_color(c, click)
                break

    if is_button_pressed(face_button):
        global face_color
        face_color = (face_color + 1) % 6

    elif is_button_pressed(CW_button):
        rotation(UNSLEEP_gpio[face_color], CW)
        print(raw_tiles[face_color] + ", CW")

    elif is_button_pressed(CCW_button):
        rotation(UNSLEEP_gpio[face_color], CCW)
        print(raw_tiles[face_color] + ", CCW")


    elif is_button_pressed(ok_button) and is_balanced():
        solution = kociemba.solve(translate())
        print(solution)

    elif is_button_pressed(solve_button) and is_balanced():
        solution = kociemba.solve(translate())
        print(solution)
        pi()

    elif is_button_pressed(test1_button):
        changeResolution(res)


def translate():
    arr = ""
    for f in range(0, 6):
        for i in range(1, 10):
            arr += faces[colors[faces[f] + str(i)]]
    return arr

while(not Exit):
    background()
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                init()

        if event.type == pygame.MOUSEBUTTONDOWN:
            check_pos(pygame.mouse.get_pos(), event.button)

    pygame.display.update()
    clock.tick(60)
pygame.quit()
GPIO.cleanup()