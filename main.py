import pygame
from pathlib import Path
from time import sleep
from random import randint
from datetime import datetime, timedelta

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

if int(width * 9/16) != height: # Force 16:9 aspect ratio based on width
    height = int(width * 9/16)

# Screen

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# Subroutines

# Devmode test text display
def testtextdisplay(text, pos):
    testtext = font.render(text, True, white)
    screen.blit(testtext, pos)

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

def drawmainmenubackground(): # Draws the main menu background to the screen
    mainmenubackground = pygame.transform.scale(pygame.image.load(Path('Sprites/Matrix Background.png')),(width, height))
    screen.blit(mainmenubackground, (0, 0))




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
        self.buffer = True
        self.enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def draw(self):
        action = False

        # Check mouseover and click conditions
        if ishover(self.rect):
            # Draw hover button to screen
            screen.blit(self.hoverimage, (self.rect.x, self.rect.y))
            if isclicked(self.rect) and not self.clicked and not self.buffer and self.enabled: # 0 = left click
                self.clicked = True # Can only click once at a time
                action = True
        else:
            # Draw normal button to screen
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False # Resets if mouse is not held
            self.buffer = False # User must have not clicked in order to click the button

        return action

    # Draws the button without the buffer, so buttons created during loops can be pressed
    def drawnobuffer(self):
        action = False

        # Check mouseover and click conditions
        if ishover(self.rect):
            # Draw hover button to screen
            screen.blit(self.hoverimage, (self.rect.x, self.rect.y))
            if isclicked(self.rect) and self.clicked == False:  # 0 = left click
                self.clicked = True  # Can only click once at a time
                action = True
        else:
            # Draw normal button to screen
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False  # Resets if mouse is not held

        return action


# Textbox class
class Textbox:
    def __init__(self, x, y, xsize, ysize, colour, hovercolour, selectcolour, textcolour):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x, y), (xsize, ysize))
        self.colour = colour
        self.hovercolour = hovercolour
        self.selectcolour = selectcolour
        self.textcolour = textcolour
        self.selected = False
        self.displaytext = ''
        self.finaltext = ''
        self.textsurface = None
        self.font = pygame.font.Font(fontname, ysize)

    def drawtext(self):
        self.textsurface = self.font.render(self.displaytext, True, self.textcolour)
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

    def submit(self):
        return self.finaltext

    def draw(self):
        submit = None

        if ishover(self.rect) and not self.selected: # If the mouse is hovered but the textbox isnt selected
            self.drawboxhover()
            if isclicked(self.rect): # If user clicks on the textbox
                self.selected = True
        else:
            self.drawbox()
            if pygame.mouse.get_pressed()[0] and not ishover(self.rect): # If anywhere except the textbox is clicked it is unselected
                self.selected = False
        if self.selected: # When the text box is selected
            self.drawboxselect()

            for event in pygame.event.get(): # Loop for detecting key presses in pygame events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.displaytext = self.displaytext[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.finaltext = self.displaytext
                        self.displaytext = ''
                        submit = self.submit()
                        self.selected = False
                    else:
                        self.displaytext += event.unicode
        return submit


# Character Class
class Character:
    def __init__(self, name, sprite, selectbutton, selectbuttonhover, startingdeck):
        self.name = name
        self.sprite = sprite
        self.selectbutton = selectbutton
        self.selectbuttonhover = selectbuttonhover
        self.startingdeck = startingdeck



# Font
fontname = 'mriamc.ttf'
font = pygame.font.Font(fontname, 96)

# Font template: int((font size in 960:540) * (width/960))
titlefontsize = int(96*(width/960))
titlefont = pygame.font.Font(fontname, titlefontsize)

loginlabelfontsize = int(80*(width/960))
loginlabelfont = pygame.font.Font(fontname, loginlabelfontsize)

settingstitlefontsize = int(70*(width/960))
settingstitlefont = pygame.font.Font(fontname, settingstitlefontsize)

quitconfirmfontsize = int(50*(width/960))
quitconfirmfont = pygame.font.Font(fontname, quitconfirmfontsize)

# Colours
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255) # Not using this one
darkgrey = (50, 50, 50)
grey = (75, 75, 75)
lightgrey = (100, 100, 100)



# Sprites
xsprite = pygame.image.load(Path('Sprites/xsprite.png'))
xspritehover = pygame.image.load(Path('Sprites/xspritehover.png'))
ticksprite = pygame.image.load(Path('Sprites/ticksprite.png'))
tickspritehover = pygame.image.load(Path('Sprites/tickspritehover.png'))
backsprite = pygame.image.load(Path('Sprites/backbutton.png'))
backspritehover = pygame.image.load(Path('Sprites/backbuttonhover.png'))
settingssprite = pygame.image.load(Path('Sprites/settingsbutton.png'))
settingsspritehover = pygame.image.load(Path('Sprites/settingsbuttonhover.png'))
blacksprite = pygame.image.load(Path('Sprites/black.png'))
whitesprite = pygame.image.load(Path('Sprites/white.png'))


# Character Instances
hero = Character('Hero', whitesprite, whitesprite, blacksprite, [])
test = Character('test', whitesprite, whitesprite, blacksprite, [])

characterlist = [hero, test]

# Button Instances
quitbutton = Button(width/20, height/20, xsprite, xspritehover, width/1920)
quitconfirmbutton = Button(width*8/20, height/2, ticksprite, tickspritehover, width/1920)
quitcancelbutton = Button(width*11/20, height/2, xsprite, xspritehover, width/1920)
backbutton = Button(width*33/40, height*3/4, backsprite, backspritehover, width/960)
settingsbutton = Button(width*7/9, height/2, settingssprite, settingsspritehover, width/960)
friendsbutton = Button(width*1/7, height/2, blacksprite, whitesprite, width/960)
playbutton = Button(width*2/5, height*2/5, blacksprite, whitesprite, width/480)


# Textbox Instances
usernametextbox = Textbox(width/2, height/3, width*19/40, loginlabelfontsize, darkgrey, grey, lightgrey, green)
passwordtextbox = Textbox(width/2, height*3/5, width*19/40, loginlabelfontsize, darkgrey, grey, lightgrey, green)



# Text

# Login Menu Text
logintitle = titlefont.render('Login Menu', True, green)
logintitlepos = (width/2-(titlefontsize*3), height*1/10)
usernametext = loginlabelfont.render('Username:', True, green)
usernametextpos = (10, height*7/20)
passwordtext = loginlabelfont.render('Password:', True, green)
passwordtextpos = (10, height*6/10)

# Main Menu
quitconfirmbox = pygame.Rect((width/6, height*2/5), (width*2/3, height/5))
quitconfirmtext = quitconfirmfont.render('Exit the simulation?', True, white)
quitconfirmtextpos = (width/5, height*2/5)

# Settings Menu
backgroundbox = pygame.Rect((width/20, height/20), (width*9/10, height*9/10))
settingsmenutitle = settingstitlefont.render('Settings Menu', True, white)
settingsmenutitlepos = (width/20, height/20)

# Friends Menu
friendsmenutitle = settingstitlefont.render('Friends Menu', True, white) # Uses same font as settings
friendsmenutitlepos = (width/20, height/20)

# Essential variables
state = 0 # 0 = Login menu, 1 = Main menu
username = ''
password = ''
quitconfirm = False
quitcancelnow = datetime.now()
playnow = datetime.now()
chrselectnow = datetime.now()

# Devmode variables
toggledev = False
devmode = False

run = True
while run:

    screen.fill((0, 0, 0))  # Black background to reset previous game loop


    # Login menu
    if state == 0:
        screen.blit(logintitle, logintitlepos) # Login Menu Title

        usernametemp = usernametextbox.draw()
        screen.blit(usernametext, usernametextpos)
        if usernametemp != None:
            username = usernametemp

        passwordtemp = passwordtextbox.draw()
        screen.blit(passwordtext, passwordtextpos)
        if passwordtemp != None:
            password = passwordtemp

        testtextdisplay(username, (0, 0))
        testtextdisplay(password, (0, 70))



    # Main menu
    elif state == 1:
        drawmainmenubackground()

        if quitconfirm:
            # Confirmation box
            pygame.draw.rect(screen, black, quitconfirmbox)
            screen.blit(quitconfirmtext, quitconfirmtextpos)

            if quitconfirmbutton.draw(): # If user presses tick, close game
                run = False
            elif quitcancelbutton.draw(): # If user presses x, close quit box
                quitconfirm = False
                quitcancelnow = datetime.now()


        else:
            if settingsbutton.draw():
                state = 2

            if friendsbutton.draw():
                state = 3

            if playbutton.draw():
                playnow = datetime.now()
                if playnow - quitcancelnow > timedelta(milliseconds=500):
                    state = 4

            if quitbutton.draw():
                quitconfirm = True



    # Settings menu
    elif state == 2:
        drawmainmenubackground()

        pygame.draw.rect(screen, black, backgroundbox)
        screen.blit(settingsmenutitle, settingsmenutitlepos)

        if backbutton.draw():
            state = 1


    # Friends menu
    elif state == 3:
        drawmainmenubackground()

        pygame.draw.rect(screen, black, backgroundbox)
        screen.blit(friendsmenutitle, friendsmenutitlepos)


        if backbutton.draw():
            state = 1



    # Starter Deck Select
    elif state == 4:
        y = height*3/5
        chrnum = len(characterlist)

        for i in range(chrnum):
            x = width * ((i+1) / (chrnum+1)) - (50 * width/960)

            characterbutton = Button(x, y, characterlist[i].selectbutton, characterlist[i].selectbuttonhover, width/960)

            if characterbutton.drawnobuffer():
                # Can't select until 500ms after entering menu
                chrselectnow = datetime.now()
                if chrselectnow - playnow > timedelta(milliseconds=500):
                    testtextdisplay("YES!", (0, 0))



        if backbutton.draw():
            state = 1




    # If no valid menu
    else:
        state = 0 # Reset to login







    # Devmode displays
    if devmode:
        devmodetext = font.render('DEVMODE', True, (255, 255, 255))
        screen.blit(devmodetext, (0, 0))
        statetext = font.render(str(state), True, (255, 255, 255))
        screen.blit(statetext, (0, 100))


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

        if devmode: # Devmode keybinds
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    state = 0
                elif event.key == pygame.K_1:
                    state = 1
                elif event.key == pygame.K_2:
                    state = 2
                elif event.key == pygame.K_3:
                    state = 3
                elif event.key == pygame.K_4:
                    state = 4

                elif event.key == pygame.K_q:
                    run = False # Quick quit game button for testing


    # Updates visual display every game loop (tick)
    pygame.display.update()

pygame.quit()