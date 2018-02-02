import kociemba
import re
import pygame
import time
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

def check_pos(pos1, click):
    for c in colors:
        if c[1] != "5":  # 5 is a middle tile
            if pos1[0] > pos[c][0] and pos1[0] < pos[c][0]+30 and pos1[1] > pos[c][1] and pos1[1] < pos[c][1]+30:
                change_color(c, click)
                break
    if pygame.mouse.get_pos()[0] > 300 and pygame.mouse.get_pos()[0] < 330 and pygame.mouse.get_pos()[1] > 210 and pygame.mouse.get_pos()[1] < 240 and is_balanced():
        # print(translate())
        print(kociemba.solve(translate()))

def translate():
    arr = ""
    for i in colors:
        arr += faces[colors[i]]
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