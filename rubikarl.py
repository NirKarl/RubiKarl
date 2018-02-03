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
    for c in colors:
        if c[1] != "5":  # 5 is a middle tile
            if pos1[0] > pos[c][0] and pos1[0] < pos[c][0]+30 and pos1[1] > pos[c][1] and pos1[1] < pos[c][1]+30:
                change_color(c, click)
                break
    if pygame.mouse.get_pos()[0] > 300 and pygame.mouse.get_pos()[0] < 330 and pygame.mouse.get_pos()[1] > 210 and pygame.mouse.get_pos()[1] < 240 and is_balanced():
        # print(colors)
        # print(translate())
        solution = kociemba.solve(translate())
        print(solution)

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

    if is_balanced():
        display_tile(im("ok.jpg"), (300, 210))

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
quit()

###############################################################################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################

DIR = 21
STEP = 20
UNSLEEP = {"U": 23, "R": 26, "F": 19, "D": 13, "L": 6, "B": 5}
CW = 1
CCW = 0
SPR = 200

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(UNSLEEP, GPIO.OUT)
GPIO.output(DIR, CW)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
'Half': (1, 0, 0),
'1/4': (0, 1, 0),
'1/8': (1, 1, 0),
'1/16': (0, 0, 1),
'1/32': (1, 0, 1)}
GPIO.output(MODE, RESOLUTION['1/32'])

step_count = SPR * 32
delay = 0.0104 / 32

def rotation(unsleep, direction):
    GPIO.output(unsleep, GPIO.HIGH)
    GPIO.output(DIR, direction)
    for i in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    GPIO.output(unsleep, GPIO.LOW)

commands = re.split(r'\s*', solution)
for i in commands:
    if i.__len__() == 1:
        rotation(UNSLEEP[i], CW)
    if i.__len__() == 2:
        if i[1] == "'":
            rotation(UNSLEEP[i], CCW)
        else:
            rotation(UNSLEEP[i], CW)
            rotation(UNSLEEP[i], CW)

GPIO.cleanup()
