import pygame
from pathlib import Path
from time import sleep
from random import randint, shuffle
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


def renderhand(hand): # Pass in player hand as a parameter
    # Return: returns None, if card is clicked then return index of card in hand
    returnvar = None

    hoverflag = False # Checks if a card is already being hovered over (only one card can be hovered at a time)
    for i in range(len(hand)):
        card = Card(carddict[hand[i]])
        size = 1

        if len(hand) > 5: # If large hand, small cards
            size = 1
        else: # If small hand, large cards
            size = 1.3
        scale = width/960 * size

        offset = width / (len(hand) + 1) # Position of the card evenly spaced on the screen
        centercorrection = width/60 * (i - (len(hand)-1)/2) # Groups the cards closer together
        x = (offset * (i+1)) - centercorrection - 45*scale # Final x position
        y = height * 21/40 # Final y position
        cardbutton = Button(x, y, card.sprite, card.sprite, scale) # Creates initial button
        if ishover(cardbutton.rect): # If card sprite is hovered over by user
            hoverscale = 1.2 # Scale value of hovered cards, provides visual feedback to the user of selected card
            if not hoverflag: # If there is no card already being hovered over
                hoverflag = True # Sets the flag as this will be the only card that can hovered over in this loop
                # Draws larger card button
                cardbutton = Button(x-90*(hoverscale-1)/2, y-160*(hoverscale-1)/2, card.sprite, card.sprite, scale*hoverscale)

        # If card is clicked
        if cardbutton.drawnobuffer():
            returnvar = i
            #textdisplay('YAY', (100, 100), 100) # Test text to confirm card clicking

    return returnvar


def displaycardpile(pile):
    if len(pile) <= 0: # If pile is empty
        return None

    rownum = (len(pile) // 10) + 1
    cardsperrow = len(pile) // rownum
    cardsonlastrow = len(pile) % cardsperrow
    if cardsonlastrow != 0:
        cardsperrow += 1
        cardsonlastrow = len(pile) % cardsperrow
    scale = 1 / (rownum // 4 + 1)

    for i in range(rownum):
        y = (height / (rownum+1)) * (i + 1) - 80*scale
        if i != rownum - 1 or cardsonlastrow == 0: # Not last row or last row is identical
            cardsinrow = cardsperrow
        else: # Last row
            cardsinrow = cardsonlastrow
        for j in range(cardsinrow):
            index = (cardsinrow*i) + j
            x = (width / (cardsinrow+1)) * (j + 1) - 45*scale
            card = Card(carddict[pile[index]])
            cardbutton = Button(x, y, card.sprite, card.sprite, scale)
            cardbutton.draw()



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
    def __init__(self, name, button, spritelist, startingdeck, startinghealth):
        # Spritelist: 0 - Idle, 1 - Attack, 2 - Defend, 3 - Special
        self.name = name
        self.button = button
        self.spritelist = spritelist
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
        # 0 - name, 1 - basedamage, 2 - basedefence, 3 - cost, 4 - effectlist, 5 - sprite
        self.name = data[0]
        self.basedamage = data[1]
        self.damage = self.basedamage
        self.basedefence = data[2]
        self.defence = self.basedefence
        self.cost = data[3]
        self.effectlist = data[4]
        self.sprite = data[5]
        self.cardeffectdict = {
            # All card special effects
            'selfdelete': False,
            'doublehit': False
        }
        for i in range(len(self.effectlist)):
            self.cardeffectdict[self.effectlist[i]] = True

    def play(self, handindex):
        # Remove card from player hand
        card = player.hand.pop(handindex)

        # Card effects

        # Discard card
        if not 'selfdelete' in self.effectlist:
            player.discardpile.append(card)
        else: # Trash card
            player.trashpile.append(card)


# Enemy Class
class Enemy:
    def __init__(self, data):
        # 0 - name, 1 - maxhealth, 2 - basedamage, 3 - specialdamage, 4 - defendamount, 5 - advancedai, 6 - difficulty, 7 - abilitylist, 8 - spritelist
        # Spritelist: 0 - Idle, 1 - Attack, 2 - Defend, 3 - Special
        self.name = data[0]
        self.maxhealth = data[1]
        self.health = self.maxhealth
        self.basedamage = data[2] # Attack damage can be between +20% and -20% of base
        self.specialdamage = data[3]
        self.defendamount = data[4]
        self.advancedai = data[5] # False = basic ai, True = advanced ai
        self.difficulty = data[6]
        self.abilitylist = data[7]
        self.spritelist = data[8]
        self.enemyabilitydict = {
            # All enemy abilities
            'disguise': False
        }


# Player Class
class Player:
    def __init__(self):
        self.deck = []
        self.drawpile = []
        self.discardpile = []
        self.trashpile = []
        self.hand = []
        self.maxhealth = 100
        self.health = self.maxhealth
        self.defence = 0
        self.maxenergy = 3
        self.energy = self.maxenergy
        self.maxhandsize = 9
        self.character = None
        self.incombat = False

    def startrun(self, newcharacter):
        # Character variables
        self.character = newcharacter
        self.deck = self.character.startingdeck
        self.maxhealth = self.character.startinghealth

        # Other variables reset for backup
        self.drawpile = []
        self.discardpile = []
        self.trashpile = []
        self.hand = []
        self.health = self.maxhealth
        self.defence = 0
        self.maxenergy = 3
        self.energy = self.maxenergy
        self.maxhandsize = 9
        self.incombat = False

    def draw(self, amount):
        for i in range(amount):
            if len(self.drawpile) <= 0:
                self.drawpile = self.discardpile
                self.discardpile = []
                shuffle(self.drawpile)
            if len(self.drawpile) > 0:  # Draw pile may still be empty after an attempted shuffle
                self.hand.append(self.drawpile.pop())


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
cardsprite = pygame.image.load(Path('Cards/cardbackground.png'))
attackcardsprite = pygame.image.load(Path('Cards/attackcard.png'))
defendcardsprite = pygame.image.load(Path('Cards/defendcard.png'))


# ========== Dictionaries ==========

carddict = {
    'attack': ['attack', 6, 0, 1, [], attackcardsprite],
    'defend': ['defend', 0, 5, 1, [], defendcardsprite],
    'strike': ['strike', 5, 0, 0, [], cardsprite],
    'heavy guard': ['heavy guard', 0, 14, 2, [], cardsprite],
    'double strike': ['double strike', 4, 0, 1, ['doublehit'], cardsprite],
    'volatile strike': ['volatile strike', 22, 0, 2, ['self-delete'], cardsprite]
}

enemydict = {
    'virus': [20, 6, 14, 6, False, [], []],
    'trojan': [40, 10, 20, 10, False, ['disguise'], []]
}


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
viewdeckbutton = Button(width*9/10, height*1/10, cardsprite, attackcardsprite, width/1920)
viewdrawpilebutton = Button(width*1/20, height*7/10, cardsprite, attackcardsprite, width/1920)
viewdiscardpilebutton = Button(width*18/20, height*7/10, cardsprite, attackcardsprite, width/1920)
viewtrashpilebutton = Button(width*17/20, height*8/10, cardsprite, attackcardsprite, width/1920)


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

# Deck View Menus
fulldeckmenutitle = settingstitlefont.render('Full Deck', True, white)
fulldeckmenutitlepos = (width/50, height/50)
drawpilemenutitle = settingstitlefont.render('Draw Pile', True, white)
drawpilemenutitlepos = (width/50, height/50)
discardpilemenutitle = settingstitlefont.render('Discard Pile', True, white)
discardpilemenutitlepos = (width/50, height/50)
trashpilemenutitle = settingstitlefont.render('Trash Pile', True, white)
trashpilemenutitlepos = (width/50, height/50)


# Character backup variable
character = None

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
prevplayedcardnow = datetime.now()

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

        # Initial combat setup
        if not player.incombat:
            player.drawpile = player.deck[:]
            shuffle(player.drawpile)
            player.discardpile = []
            player.trashpile = []
            player.incombat = True # Will only run once per combat
            player.draw(1)

        textdisplay(f'{player.health}/{player.maxhealth}', (0, 0), 100)
        textdisplay(f'{player.energy}/{player.maxenergy}', (0, 100), 100)

        # Buttons
        if viewdeckbutton.draw():
            state = 7
        if viewdrawpilebutton.draw():
            state = 8
        if viewdiscardpilebutton.draw():
            state = 9
        if viewtrashpilebutton.draw():
            state = 10

        playedcardindex = renderhand(player.hand)
        if playedcardindex != None:
            playedcardnow = datetime.now()
            if playedcardnow - prevplayedcardnow > timedelta(milliseconds=500):
                playedcard = Card(carddict[player.hand[playedcardindex]])
                if playedcard.cost <= player.energy:
                    playedcard.play(playedcardindex)
                    player.energy -= playedcard.cost
            prevplayedcardnow = playedcardnow



    elif state == 7: # View full deck
        # Title text
        screen.blit(fulldeckmenutitle, fulldeckmenutitlepos)

        displaycardpile(player.deck)


    elif state == 8: # View draw pile
        # Title text
        screen.blit(drawpilemenutitle, drawpilemenutitlepos)

        displaycardpile(player.drawpile)


    elif state == 9: # View discard pile
        # Title text
        screen.blit(discardpilemenutitle, discardpilemenutitlepos)

        displaycardpile(player.discardpile)


    elif state == 10: # View trash pile
        # Title text
        screen.blit(trashpilemenutitle, trashpilemenutitlepos)

        displaycardpile(player.trashpile)




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
                elif event.key == pygame.K_7:
                    state = 7
                elif event.key == pygame.K_8:
                    state = 8
                elif event.key == pygame.K_9:
                    state = 9
                elif event.key == pygame.K_w:
                    state = 10

                elif event.key == pygame.K_o:
                    player.deck.append('attack')
                elif event.key == pygame.K_p:
                    player.deck.append('defend')
                elif event.key == pygame.K_i:
                    player.hand = []
                elif event.key == pygame.K_SPACE:
                    player.draw(1)

                # Quit button
                elif event.key == pygame.K_q:
                    run = False # Quick quit game button for testing


    # Updates visual display every game loop (tick)
    pygame.display.update()

pygame.quit()