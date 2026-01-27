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
difficulty = None
autosynchighscore = None
backupwidth = 960
backupheight = 540
backupvolume = 1
backupdifficulty = 1
backupautosynchighscore = False

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
        elif line[0] == "difficulty":
            try:
                difficulty = int(line[1])
            except:
                difficulty = backupdifficulty
        elif line[0] == "autosynchighscore":
            if line[1] == '1':
                autosynchighscore = True
            else:
                autosynchighscore = False

if width == None:
    width = backupwidth
if height == None:
    height = backupheight
if volume == None:
    volume = backupheight
if difficulty == None:
    difficulty = backupdifficulty
if autosynchighscore == None:
    autosynchighscore = backupautosynchighscore

if int(width * 9/16) != height: # Force 16:9 aspect ratio based on width
    height = int(width * 9/16)

# Screen

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fontname
fontname = 'mriamc.ttf'


# ========== Subroutines ==========

# Devmode test text display
def textdisplay(text, pos, fontsize):
    tempfont = pygame.font.Font(fontname, int(fontsize))
    testtext = tempfont.render(text, True, white)
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



# ========== Classes ==========

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

            # Only resets clicked and buffer if mouse is not held on hover
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False  # Resets if mouse is not held
                self.buffer = False  # User must have not clicked in order to click the button

            # Draw hover button to screen
            screen.blit(self.hoverimage, (self.rect.x, self.rect.y))
            if isclicked(self.rect) and not self.clicked and not self.buffer and self.enabled: # 0 = left click
                self.clicked = True # Can only click once at a time
                action = True
        else:
            # Draw normal button to screen
            screen.blit(self.image, (self.rect.x, self.rect.y))

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
        if self.displaytext != '':
            self.textsurface = self.font.render(self.displaytext, True, self.textcolour)
        else:
            self.textsurface = self.font.render(self.finaltext, True, (125, 125, 125))
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

            for event in events: # Loop for detecting key presses in pygame events
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
    def __init__(self, name, button, sprite, startingdeck, startinghealth):
        self.name = name
        self.button = button
        self.sprite = sprite
        self.startingdeck = startingdeck
        self.startinghealth = startinghealth


class CharacterButton:
    def __init__(self, name, selectbutton, selectbuttonhover, background, description):
        self.name = name
        self.selectbutton = selectbutton
        self.selectbuttonhover = selectbuttonhover
        self.selectbackground = pygame.transform.scale(pygame.image.load(Path(f'Sprites/{background}')),(width, height))
        self.description = description
        self.selected = False  # True when button in select menu is clicked

    def selectbuttonclick(self):
        self.selected = not self.selected

    def selectdisplay(self):
        screen.blit(self.selectbackground, (0, 0))
        textdisplay(self.name, (0, 0), width/10)
        textdisplay(self.description, (0, 100), width/30)


# Card Class
class Card:
    def __init__(self, data):
        # 0 - basedamage, 1 - basedefence, 2 - cost, 3 - effectlist, 4 - spritelist
        # Spritelist: 0 - Idle, 1 - Attack, 2 - Defend, 3 - Special
        self.basedamage = data[0]
        self.damage = self.basedamage
        self.basedefence = data[1]
        self.defence = self.basedefence
        self.cost = data[2]
        self.effectlist = data[3]
        self.spritelist = data[4]
        self.cardeffectdict = {
            # All card special effects
            'doublehit': False
        }


# Enemy Class
class Enemy:
    def __init__(self, data):
        # 0 - maxhealth, 1 - basedamage, 2 - specialdamage, 3 - defendamount, 4 - advancedai, 5 - difficulty, 6 - abilitylist, 7 - spritelist
        # Spritelist: 0 - Idle, 1 - Attack, 2 - Defend, 3 - Special
        self.maxhealth = data[0]
        self.health = self.maxhealth
        self.basedamage = data[1] # Attack damage can be between +20% and -20% of base
        self.specialdamage = data[2]
        self.defendamount = data[3]
        self.advancedai = data[4] # False = basic ai, True = advanced ai
        self.difficulty = data[5]
        self.abilitylist = data[6]
        self.spritelist = data[7]
        self.enemyabilitydict = {
            # All enemy abilities
            'disguise': False
        }


# Player Class
class Player:
    def __init__(self):
        self.deck = []
        self.hand = []
        self.maxhealth = 100
        self.health = self.maxhealth
        self.defence = 0
        self.maxhandsize = 9
        self.character = None

    def startrun(self, newcharacter):
        # Character variables
        self.character = newcharacter
        self.deck = self.character.startingdeck
        self.maxhealth = self.character.startinghealth

        # Other variables reset for backup
        self.hand = []
        self.health = self.maxhealth
        self.defence = 0
        self.maxhandsize = 9


# ========== Dictionaries ==========

carddict = {
    'attack': [6, 0, 1, [], []],
    'defend': [0, 5, 1, [], []],
    'strike': [5, 0, 0, [], []],
    'heavy guard': [0, 14, 2, [], []],
    'double strike': [4, 0, 1, ['doublehit'], []]
}

enemydict = {
    'virus': [20, 6, 14, 6, False, [], []],
    'trojan': [40, 10, 20, 10, False, ['disguise'], []]
}



# Font template: int((font size in 960:540) * (width/960))
font = pygame.font.Font(fontname, 96)

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
playsprite = pygame.image.load(Path('Sprites/playsprite.png'))
playspritehover = pygame.image.load(Path('Sprites/playspritehover.png'))
heartsprite = pygame.image.load(Path('Sprites/heartsprite.png'))
heartspritehover = pygame.image.load(Path('Sprites/heartspritehover.png'))
blacksprite = pygame.image.load(Path('Sprites/black.png'))
whitesprite = pygame.image.load(Path('Sprites/white.png'))


# Character Instances
herostarterdeck = ['attack', 'attack', 'attack', 'attack', 'defend', 'defend', 'defend', 'defend']
herobutton = CharacterButton('Hero', whitesprite, blacksprite, 'Matrix Background.png', 'The hero is cool')
hero = Character('Hero', herobutton, whitesprite, herostarterdeck, 100)
testbutton = CharacterButton('test', whitesprite, blacksprite, 'xsprite.png', 'test description')
test = Character('test', testbutton, whitesprite, [], 999)

characterlist = [hero, test]


# Button Instances
quitbutton = Button(width/20, height/20, xsprite, xspritehover, width/1920)
quitconfirmbutton = Button(width*8/20, height/2, ticksprite, tickspritehover, width/1920)
quitcancelbutton = Button(width*11/20, height/2, xsprite, xspritehover, width/1920)
backbutton = Button(width*33/40, height*3/4, backsprite, backspritehover, width/960)
settingsbutton = Button(width*7/9, height/2, settingssprite, settingsspritehover, width/960)
friendsbutton = Button(width*1/7, height/2, heartsprite, heartspritehover, width/960)
playbutton = Button(width*2/5, height*2/5, playsprite, playspritehover, width/480)
startrunbutton = Button(width*33/40, height*2/5, playsprite, playspritehover, width/960)
loginconfirmbutton = Button(width*2/5, height*4/5, playsprite, playspritehover, width/960)


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


# Combat Variables, will copy cards from player object deck attribute
drawpile = []
discardpile = []
trashpile = []
character = None # Backup if run is entered without setting a character

# Player object
player = Player()


# Essential variables
state = 0 # 0 = Login menu, 1 = Main menu
username = ''
password = ''
quitconfirm = False
quitcancelnow = datetime.now()
playnow = datetime.now()
chrselectnow = datetime.now()
prevchrselectnow = datetime.now()

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

        # Draw login confirmation button
        if username != '' and password != '':
            if loginconfirmbutton.draw():
                # Future account login/creation code
                state = 1

        #textdisplay(username, (0, 0), 100)
        #textdisplay(password, (0, 70), 100)



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
            # Settings button
            if settingsbutton.draw():
                state = 2 # Move to settings menu

            # Friends button
            if friendsbutton.draw():
                state = 3 # Move to friends menu

            # Play button
            if playbutton.draw():
                playnow = datetime.now()
                if playnow - quitcancelnow > timedelta(milliseconds=500):
                    state = 4  # Move to character select menu

            # Quit button
            if quitbutton.draw():
                quitconfirm = True # Enable confirmation box



    # Settings menu
    elif state == 2:
        drawmainmenubackground()

        # Background box and title
        pygame.draw.rect(screen, black, backgroundbox)
        screen.blit(settingsmenutitle, settingsmenutitlepos)

        # Back button in bottom right
        if backbutton.draw():
            state = 1 # Return to main menu


    # Friends menu
    elif state == 3:
        drawmainmenubackground()

        # Background box and title
        pygame.draw.rect(screen, black, backgroundbox)
        screen.blit(friendsmenutitle, friendsmenutitlepos)

        # Back button in bottom right
        if backbutton.draw():
            state = 1 # Return to main menu



    # Starter Deck Select
    elif state == 4:
        y = height*3/5
        chrnum = len(characterlist)

        # Loop to find what is already selected
        for i in range(chrnum):
            if characterlist[i].button.selected:
                characterlist[i].button.selectdisplay()
                if startrunbutton.drawnobuffer():
                    # Deselect all buttons
                    for j in range(chrnum):
                        characterlist[j].button.selected = False
                    # Start run
                    character = characterlist[i]
                    player.startrun(character)
                    state = 5

        for i in range(chrnum):
            x = width * ((i+1) / (chrnum+1)) - (50 * width/960)

            characterbutton = Button(x, y, characterlist[i].button.selectbutton, characterlist[i].button.selectbuttonhover, width/960)

            if characterbutton.drawnobuffer():
                # Can't select until 500ms after entering menu
                chrselectnow = datetime.now()
                if chrselectnow - playnow > timedelta(milliseconds=500) and chrselectnow - prevchrselectnow > timedelta(milliseconds=500):
                    characterlist[i].button.selectbuttonclick()
                    # Deselect all other buttons
                    for j in range(chrnum):
                        if j != i:
                            characterlist[j].button.selected = False
                prevchrselectnow = datetime.now() # Sets the previous select at the end



        if backbutton.draw():
            # Deselect all characters on back button press
            for i in range(chrnum):
                characterlist[i].button.selected = False
            state = 1


    elif state == 5: # Map Screen
        # Backup in case player has no character
        if character == None:
            character = characterlist[0]
            player.startrun(character)


    elif state == 6: # Combat screen
        # Backup in case player has no character
        if character == None:
            character = characterlist[0]
            player.startrun(character)

        drawmainmenubackground()
        textdisplay(character.name, (0, 0), 96)


    # If no valid menu found for state variable value
    else:
        state = 0 # Reset to login menu







    # Devmode displays
    if devmode:
        # Devmode confirmation text
        devmodetext = font.render('DEVMODE', True, (255, 255, 255))
        screen.blit(devmodetext, (0, 0))

        # State value display text
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


    events = pygame.event.get()
    for event in events:
        # If windows X button is used
        if event.type == pygame.QUIT:
            run = False

        if devmode: # Devmode keybinds
            if event.type == pygame.KEYDOWN:
                # Menu warps
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
                elif event.key == pygame.K_5:
                    state = 5
                elif event.key == pygame.K_6:
                    state = 6

                # Quit button
                elif event.key == pygame.K_q:
                    run = False # Quick quit game button for testing


    # Updates visual display every game loop (tick)
    pygame.display.update()

pygame.quit()