import pygame
from time import sleep
from random import randint

pygame.init()
pygame.display.set_caption('CRASHing out')

# Backup variables
width = None
height = None
backupwidth = 960
backupheight = 540

# Settings
with open("settings.txt") as settings:
    for line in settings:
        line = line.strip().split("=")
        print(line)
        if line[0] == "width":
            try:
                width = int(line[1])
            except:
                width = backupwidth
        elif line[0] == "height":
            try:
                height = int(line[1])
            except:
                height = backupheight

# Screen
if width == None:
    width = backupwidth
if height == None:
    height == backupheight

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Essential variables
state = 0 # 0 = Main menu,

run = True
while run:

    screen.fill((0, 0, 0))  # Black background to reset previous game loop

    if state == 0:
        pass
    else:
        state = 0

    for event in pygame.event.get():
        # If windows X button is used
        if event.type == pygame.QUIT:
            run = False

    # Updates visual display every game loop (tick)
    pygame.display.update()

pygame.quit()