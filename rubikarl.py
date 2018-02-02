from time import sleep
import RPi.GPIO as GPIO
import kociemba
import re

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
    GPIO.output(UNSLEEP[rotate[0]], GPIO.HIGH)
    GPIO.output(DIR, rotate[1])
    for i in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    GPIO.output(UNSLEEP[rotate[0]], GPIO.LOW)

TEST = 'FRBRUDRFURFLURUDDLBLFLFRRUFUFLLDBUBBRFDLLULBBUDDBBDDRF'

solution = kociemba.solve(TEST)
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
