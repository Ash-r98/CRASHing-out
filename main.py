import pygame
from time import sleep
from random import randint

pygame.init()
pygame.display.set_caption('CRASHing out')

# Backup variables
width = None
height = None
volume = None
backupwidth = 960
backupheight = 540
backupvolume = 1

# Settings
with open("settings.txt", 'r+') as settings:
    for line in settings:
        line = line.strip().split("=")
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
        elif line[0] == "volume":
            try:
                volume = int(line[1])
            except:
                volume = backupvolume

if width == None:
    width = backupwidth
if height == None:
    height = backupheight
if volume == None:
    volume = backupheight


# Screen

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Font
fontname = 'mriamc.ttf'


# Subroutines

# Object mouse hover detection
def ishover(rect): # Takes a pygame rectangle object as a parameter
    # Get mouse position
    pos = pygame.mouse.get_pos()

    # Check if position of mouse is over the object
    if rect.collidepoint(pos):
        return True
    else:
        return False

# Object mouse click detection
def isclicked(rect): # Takes a pygame rectangle object as a parameter
    click = False

    if ishover(rect): # If mouse is on the object
        if pygame.mouse.get_pressed()[0]: # If the left mouse button is pressed
            click = True
    return click # Always returns true or false











# Classes

# Button class
class Button:
    def __init__(self, x, y, image, hoverimage, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.hoverimage = pygame.transform.scale(hoverimage, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        action = False

        # Check mouseover and click conditions
        if ishover(self.rect):
            # Draw hover button to screen
            screen.blit(self.hoverimage, (self.rect.x, self.rect.y))
            if isclicked(self.rect) and self.clicked == False: # 0 = left click
                self.clicked = True # Can only click once at a time
                action = True
        else:
            # Draw normal button to screen
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False # Resets if mouse is not held

        return action

# Textbox class
class Textbox:
    def __init__(self, x, y, xsize, ysize, colour, hovercolour, selectcolour):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x, y), (xsize, ysize))
        self.colour = colour
        self.hovercolour = hovercolour
        self.selectcolour = selectcolour
        self.selected = False
        self.text = ''
        self.font = pygame.font.Font(fontname, ysize)

    def drawtext(self):
        self.textsurface = self.font.render(self.text, True, (0, 255, 0))
        screen.blit(self.textsurface, (self.x,self.y))

    def drawbox(self):
        pygame.draw.rect(screen, self.colour, self.rect)
        self.drawtext()

    def drawboxhover(self):
        pygame.draw.rect(screen, self.hovercolour, self.rect)
        self.drawtext()

    def drawboxselect(self):
        pygame.draw.rect(screen, self.selectcolour, self.rect)
        self.drawtext()

    def draw(self):
        if ishover(self.rect) and not self.selected: # If the mouse is hovered but the textbox isnt selected
            self.drawboxhover()
            if isclicked(self.rect): # If user clicks on the textbox
                self.selected = True
        else:
            self.drawbox()
            if pygame.mouse.get_pressed()[0]: # If anywhere except the textbox is clicked it is unselected
                self.selected = False
        if self.selected: # When the text box is selected
            self.drawboxselect()

            for event in pygame.event.get(): # Loop for detecting key presses in pygame events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode


# Button Instances
testbutton = Button(200, 200, pygame.image.load(r'Matrix Background.png'), pygame.image.load(r'Matrix Background.png'), 1)

# Textbox Instances
testtextbox = Textbox(200, 200, 400, 100, (200, 200, 200), (255, 255, 255), (255, 0, 0))


# Text
font = pygame.font.Font(fontname, 96)

# Essential variables
state = 1 # 0 = Login menu, 1 = Main menu

# Devmode variables
toggledev = False
devmode = False

run = True
while run:

    screen.fill((0, 0, 0))  # Black background to reset previous game loop

    # Devmode displays
    if devmode:
        devmodetext = font.render('DEVMODE', True, (255, 255, 255))
        screen.blit(devmodetext, (0, 0))
        statetext = font.render(str(state), True, (255, 255, 255))
        screen.blit(statetext, (0, 100))

    if state == 0: # Login menu
        if testbutton.draw():
            print("hi")

    elif state == 1:
        testtextbox.draw()

    else:
        state = 0


    # Key detection
    key = pygame.key.get_pressed()
    if key[pygame.K_BACKQUOTE]:
        toggledev = True # Activates toggle flag
    else: # When no keys are held
        if toggledev:
            devmode = not devmode # Invert boolean
            toggledev = False # Only flips once per press



    for event in pygame.event.get():
        # If windows X button is used
        if event.type == pygame.QUIT:
            run = False

    # Updates visual display every game loop (tick)
    pygame.display.update()

pygame.quit()