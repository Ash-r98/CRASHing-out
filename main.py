import pygame
from time import sleep
from random import randint

pygame.init()
pygame.display.set_caption('Programming Project')

# Screen
width = 960
height = 540

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sleep(3)


# Essential variables
state = 0 # 0 = Main menu,

run = True
while run:

    screen.fill((0, 0, 0))  # Black background to reset previous game loop

    if state == 0:
        pass

    for event in pygame.event.get():
        # If windows X button is used
        if event.type == pygame.QUIT:
            run = False

    # Updates visual display every game loop (tick)
    pygame.display.update()

pygame.quit()

#Hello