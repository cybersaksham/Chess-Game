import pygame
import sys
from pygame import mixer
from pygame.locals import *

pygame.init()
mixer.init()

# Global Variables
SCREENWIDTH = 600
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
SPRITE_IMAGES = {}
SPRITE_NAMES_WHITE = []
SPRITE_NAMES_BLACK = []
SPRITE_NAMES = []
PAWN = []
ROOK = []
KNIGHT = []
BISHOP = []
QUEEN = []
KING = []
SPRITE_LOCATIONS = {}
ALLOWED_SPRITE_LOCATIONS = {}
BOX_LOCATION_X = [((i * 72) + 40) for i in range(8)]
BOX_LOCATION_Y = [(520 - (i * 70)) for i in range(8)]
BOX_X = [[22, 91], [95, 162], [165, 234], [238, 304], [308, 377], [381, 448], [451, 518], [523, 589]]
BOX_Y = [[507, 573], [434, 502], [364, 430], [293, 360], [222, 287], [151, 218], [80, 146], [9, 76]]
SPRITE_SELECTED = False
TURN_BLACK = False
TURN_WHITE = True
CLICKED_SPRITE = ""
BLUE_BOXES = []
VALID_BOXES = []
VALID_TURN = True
IS_KILL = False
KILL_POSITION = []
GAME_OVER = False
START_GAME = True
FONT = pygame.font.SysFont(None, 40)


def playSound(sound):
    pygame.mixer.music.load(f"Gallery/{sound}.wav")
    pygame.mixer.music.play()


def setVariables():
    # Sprite Images
    global SPRITE_IMAGES
    SPRITE_IMAGES['board'] = pygame.image.load("Gallery/board.png")
    SPRITE_IMAGES['start'] = pygame.image.load("Gallery/start.png")
    for i in range(8):
        SPRITE_IMAGES[f"w2{i + 1}"] = pygame.image.load(f"Gallery/w1.png")
        SPRITE_IMAGES[f"b7{i + 1}"] = pygame.image.load(f"Gallery/b1.png")
    for i in range(1, 6):
        SPRITE_IMAGES[f"w1{i}"] = pygame.image.load(f"Gallery/w{i + 1}.png")
        SPRITE_IMAGES[f"b8{i}"] = pygame.image.load(f"Gallery/b{i + 1}.png")
    for i in range(6, 9):
        SPRITE_IMAGES[f"w1{i}"] = pygame.image.load(f"Gallery/w{10 - i}.png")
        SPRITE_IMAGES[f"b8{i}"] = pygame.image.load(f"Gallery/b{10 - i}.png")

    # Sprite Names White
    global SPRITE_NAMES_WHITE
    for i in range(2):
        for j in range(8):
            SPRITE_NAMES_WHITE.append(f"w{i + 1}{j + 1}")

    # Sprite Names Black
    global SPRITE_NAMES_BLACK
    for i in range(2):
        for j in range(8):
            SPRITE_NAMES_BLACK.append(f"b{i + 7}{j + 1}")

    # Sprite Names
    global SPRITE_NAMES
    for i in range(2):
        for j in range(8):
            SPRITE_NAMES.append(f"w{i + 1}{j + 1}")
            SPRITE_NAMES.append(f"b{i + 7}{j + 1}")

    # Sprite Categories
    global PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING
    for i in range(8):
        PAWN.append(f"w2{i + 1}")
        PAWN.append(f"b7{i + 1}")
    ROOK.append("w11")
    ROOK.append("w18")
    ROOK.append("b81")
    ROOK.append("b88")
    KNIGHT.append("w12")
    KNIGHT.append("w17")
    KNIGHT.append("b82")
    KNIGHT.append("b87")
    BISHOP.append("w13")
    BISHOP.append("w16")
    BISHOP.append("b83")
    BISHOP.append("b86")
    QUEEN.append("w14")
    QUEEN.append("b84")
    KING.append("w15")
    KING.append("b85")

    # Adding Sprite Locations
    global SPRITE_LOCATIONS
    for i in range(2):
        for j in range(8):
            SPRITE_LOCATIONS[f"w{i + 1}{j + 1}"] = [i + 1, j + 1]
            SPRITE_LOCATIONS[f"b{i + 7}{j + 1}"] = [i + 7, j + 1]


class Player:
    __clicked = ""
    __type = 0
    __color = 0
    __box = []

    def __init__(self, clicked):
        global VALID_BOXES, KILL_POSITION
        self.__clicked = clicked
        self.__type = self.__checkType()
        self.__color = self.__checkColor()
        self.__box = []
        KILL_POSITION = []
        VALID_BOXES = []

    def __checkType(self):
        if self.__clicked in PAWN:
            return 1
        elif self.__clicked in ROOK:
            return 2
        elif self.__clicked in KNIGHT:
            return 3
        elif self.__clicked in BISHOP:
            return 4
        elif self.__clicked in QUEEN:
            return 5
        elif self.__clicked in KING:
            return 6

    @staticmethod
    def __checkColor():
        if TURN_BLACK:
            return 1
        else:
            return 2

    def __finalSet(self):
        global BLUE_BOXES, VALID_BOXES
        BLUE_BOXES = []
        VALID_BOXES = []
        for item in self.__box:
            rectBox(item)
            VALID_BOXES.append(item)

    def __suggestions(self, clicked):
        global VALID_BOXES, SPRITE_LOCATIONS
        self.__box.append([SPRITE_LOCATIONS[clicked][0], SPRITE_LOCATIONS[clicked][1]])
        if self.__type == 1:
            self.__type1(clicked)
            self.__finalSet()
            self.__checkOverlap()
        elif self.__type == 2:
            self.__type2(clicked)
        elif self.__type == 3:
            self.__type3(clicked)
            self.__finalSet()
            self.__checkOverlap()
        elif self.__type == 4:
            self.__type4(clicked)
        elif self.__type == 5:
            self.__type5(clicked)
        elif self.__type == 6:
            self.__type6(clicked)
            self.__finalSet()
            self.__checkOverlap()
        self.__checkKill()
        self.__finalSet()

    def __type1(self, clicked):
        global KILL_POSITION
        if self.__color == 1:
            if self.__box[0][0] == 7:
                self.__box.append([SPRITE_LOCATIONS[clicked][0], SPRITE_LOCATIONS[clicked][1]])
                self.__box[0][0] -= 2
                self.__box[1][0] -= 1
                for item in SPRITE_NAMES_WHITE:
                    if SPRITE_LOCATIONS[item][0] == self.__box[1][0] and SPRITE_LOCATIONS[item][1] == self.__box[1][1]:
                        self.__box = []
                        break
            else:
                self.__box[0][0] -= 1
            KILL_POSITION.append([SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] - 1])
            KILL_POSITION.append([SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] + 1])
        else:
            if self.__box[0][0] == 2:
                self.__box.append([SPRITE_LOCATIONS[clicked][0], SPRITE_LOCATIONS[clicked][1]])
                self.__box[0][0] += 2
                self.__box[1][0] += 1
                for item in SPRITE_NAMES_BLACK:
                    if SPRITE_LOCATIONS[item][0] == self.__box[1][0] and SPRITE_LOCATIONS[item][1] == self.__box[1][1]:
                        self.__box = []
                        break
            else:
                self.__box[0][0] += 1
            KILL_POSITION.append([SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] - 1])
            KILL_POSITION.append([SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] + 1])

    def __type2(self, clicked):
        self.__box = []
        checkPos1 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1]]
        checkPos2 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1]]
        checkPos3 = [SPRITE_LOCATIONS[clicked][0], SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos4 = [SPRITE_LOCATIONS[clicked][0], SPRITE_LOCATIONS[clicked][1] - 1]
        while self.__checkCurOverlap(checkPos1):
            self.__box.append([checkPos1[0], checkPos1[1]])
            checkPos1[0] += 1
        while self.__checkCurOverlap(checkPos2):
            self.__box.append([checkPos2[0], checkPos2[1]])
            checkPos2[0] -= 1
        while self.__checkCurOverlap(checkPos3):
            self.__box.append([checkPos3[0], checkPos3[1]])
            checkPos3[1] += 1
        while self.__checkCurOverlap(checkPos4):
            self.__box.append([checkPos4[0], checkPos4[1]])
            checkPos4[1] -= 1

    def __type3(self, clicked):
        global KILL_POSITION
        self.__box = []
        checkPos1 = [SPRITE_LOCATIONS[clicked][0] + 2, SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos2 = [SPRITE_LOCATIONS[clicked][0] - 2, SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos3 = [SPRITE_LOCATIONS[clicked][0] + 2, SPRITE_LOCATIONS[clicked][1] - 1]
        checkPos4 = [SPRITE_LOCATIONS[clicked][0] - 2, SPRITE_LOCATIONS[clicked][1] - 1]
        checkPos5 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] + 2]
        checkPos6 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] - 2]
        checkPos7 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] + 2]
        checkPos8 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] - 2]
        if 9 > checkPos1[0] > 0 and 9 > checkPos1[1] > 0:
            self.__box.append([checkPos1[0], checkPos1[1]])
        if 9 > checkPos2[0] > 0 and 9 > checkPos2[1] > 0:
            self.__box.append([checkPos2[0], checkPos2[1]])
        if 9 > checkPos3[0] > 0 and 9 > checkPos3[1] > 0:
            self.__box.append([checkPos3[0], checkPos3[1]])
        if 9 > checkPos4[0] > 0 and 9 > checkPos4[1] > 0:
            self.__box.append([checkPos4[0], checkPos4[1]])
        if 9 > checkPos5[0] > 0 and 9 > checkPos5[1] > 0:
            self.__box.append([checkPos5[0], checkPos5[1]])
        if 9 > checkPos6[0] > 0 and 9 > checkPos6[1] > 0:
            self.__box.append([checkPos6[0], checkPos6[1]])
        if 9 > checkPos7[0] > 0 and 9 > checkPos7[1] > 0:
            self.__box.append([checkPos7[0], checkPos7[1]])
        if 9 > checkPos8[0] > 0 and 9 > checkPos8[1] > 0:
            self.__box.append([checkPos8[0], checkPos8[1]])
        for item in self.__box:
            KILL_POSITION.append(item)

    def __type4(self, clicked):
        self.__box = []
        checkPos1 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos2 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos3 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] - 1]
        checkPos4 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] - 1]
        while self.__checkCurOverlap(checkPos1):
            self.__box.append([checkPos1[0], checkPos1[1]])
            checkPos1[0] += 1
            checkPos1[1] += 1
        while self.__checkCurOverlap(checkPos2):
            self.__box.append([checkPos2[0], checkPos2[1]])
            checkPos2[0] -= 1
            checkPos2[1] += 1
        while self.__checkCurOverlap(checkPos3):
            self.__box.append([checkPos3[0], checkPos3[1]])
            checkPos3[0] += 1
            checkPos3[1] -= 1
        while self.__checkCurOverlap(checkPos4):
            self.__box.append([checkPos4[0], checkPos4[1]])
            checkPos4[0] -= 1
            checkPos4[1] -= 1

    def __type5(self, clicked):
        self.__type2(clicked)
        box1 = self.__box
        self.__type4(clicked)
        box2 = self.__box
        self.__box = []

        for item in box1:
            self.__box.append(item)
        for item in box2:
            self.__box.append(item)

    def __type6(self, clicked):
        global KILL_POSITION
        self.__box = []
        checkPos1 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos2 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1]]
        checkPos3 = [SPRITE_LOCATIONS[clicked][0] + 1, SPRITE_LOCATIONS[clicked][1] - 1]
        checkPos4 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos5 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1]]
        checkPos6 = [SPRITE_LOCATIONS[clicked][0] - 1, SPRITE_LOCATIONS[clicked][1] - 1]
        checkPos7 = [SPRITE_LOCATIONS[clicked][0], SPRITE_LOCATIONS[clicked][1] + 1]
        checkPos8 = [SPRITE_LOCATIONS[clicked][0], SPRITE_LOCATIONS[clicked][1] - 1]
        if 9 > checkPos1[0] > 0 and 9 > checkPos1[1] > 0:
            self.__box.append([checkPos1[0], checkPos1[1]])
        if 9 > checkPos2[0] > 0 and 9 > checkPos2[1] > 0:
            self.__box.append([checkPos2[0], checkPos2[1]])
        if 9 > checkPos3[0] > 0 and 9 > checkPos3[1] > 0:
            self.__box.append([checkPos3[0], checkPos3[1]])
        if 9 > checkPos4[0] > 0 and 9 > checkPos4[1] > 0:
            self.__box.append([checkPos4[0], checkPos4[1]])
        if 9 > checkPos5[0] > 0 and 9 > checkPos5[1] > 0:
            self.__box.append([checkPos5[0], checkPos5[1]])
        if 9 > checkPos6[0] > 0 and 9 > checkPos6[1] > 0:
            self.__box.append([checkPos6[0], checkPos6[1]])
        if 9 > checkPos7[0] > 0 and 9 > checkPos7[1] > 0:
            self.__box.append([checkPos7[0], checkPos7[1]])
        if 9 > checkPos8[0] > 0 and 9 > checkPos8[1] > 0:
            self.__box.append([checkPos8[0], checkPos8[1]])
        for item in self.__box:
            KILL_POSITION.append(item)

    def __checkCurOverlap(self, toCheck):
        global KILL_POSITION
        if 9 > toCheck[0] > 0 and 9 > toCheck[1] > 0:
            if self.__color == 1:
                for item in SPRITE_NAMES_WHITE:
                    if SPRITE_LOCATIONS[item] == toCheck:
                        self.__box.append([toCheck[0], toCheck[1]])
                        KILL_POSITION.append([toCheck[0], toCheck[1]])
                        return False
                for item in SPRITE_NAMES_BLACK:
                    if SPRITE_LOCATIONS[item] == toCheck:
                        return False
            else:
                for item in SPRITE_NAMES_WHITE:
                    if SPRITE_LOCATIONS[item] == toCheck:
                        return False
                for item in SPRITE_NAMES_BLACK:
                    if SPRITE_LOCATIONS[item] == toCheck:
                        self.__box.append([toCheck[0], toCheck[1]])
                        KILL_POSITION.append([toCheck[0], toCheck[1]])
                        return False
            return True
        else:
            return False

    def __checkOverlap(self):
        if self.__color == 1:
            for item in SPRITE_NAMES:
                if SPRITE_LOCATIONS[item] in VALID_BOXES:
                    self.__box.remove([SPRITE_LOCATIONS[item][0], SPRITE_LOCATIONS[item][1]])
        else:
            for item in SPRITE_NAMES:
                if SPRITE_LOCATIONS[item] in VALID_BOXES:
                    self.__box.remove([SPRITE_LOCATIONS[item][0], SPRITE_LOCATIONS[item][1]])

    def __checkKill(self):
        if self.__color == 1:
            for item in SPRITE_NAMES_WHITE:
                if SPRITE_LOCATIONS[item] in KILL_POSITION:
                    self.__box.append([SPRITE_LOCATIONS[item][0], SPRITE_LOCATIONS[item][1]])
        else:
            for item in SPRITE_NAMES_BLACK:
                if SPRITE_LOCATIONS[item] in KILL_POSITION:
                    self.__box.append([SPRITE_LOCATIONS[item][0], SPRITE_LOCATIONS[item][1]])

    def startSuggestions(self, clicked):
        self.__suggestions(clicked)


def updateScreen(img, x, y):
    if img is not None:
        SCREEN.blit(img, (x, y))


def drawRect(color, x1, y1, x2, y2):
    pygame.draw.rect(SCREEN, color, pygame.Rect(x1, y1, x2, y2), 5)


def rectBox(where):
    global BLUE_BOXES
    BLUE_BOXES.append([BOX_X[where[1] - 1][0], BOX_Y[where[0] - 1][0], BOX_X[where[1] - 1][1] - BOX_X[where[1] - 1][0],
                       BOX_Y[where[0] - 1][1] - BOX_Y[where[0] - 1][0]])


def playerRole():
    player = Player(CLICKED_SPRITE)
    player.startSuggestions(CLICKED_SPRITE)


def showSprites():
    for i in range(2):
        for j in range(8):
            try:
                location = SPRITE_LOCATIONS[f"w{i + 1}{j + 1}"]
                updateScreen(SPRITE_IMAGES[f"w{i + 1}{j + 1}"], BOX_LOCATION_X[location[1] - 1],
                             BOX_LOCATION_Y[location[0] - 1])
            except Exception as e:
                a = 0
            try:
                location = SPRITE_LOCATIONS[f"b{i + 7}{j + 1}"]
                updateScreen(SPRITE_IMAGES[f"b{i + 7}{j + 1}"], BOX_LOCATION_X[location[1] - 1],
                             BOX_LOCATION_Y[location[0] - 1])
            except Exception as e:
                a = 0


def removeSprite(item):
    global SPRITE_IMAGES, SPRITE_LOCATIONS
    global SPRITE_NAMES_WHITE, SPRITE_NAMES_BLACK, SPRITE_NAMES
    global PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING
    SPRITE_IMAGES[item] = None
    try:
        SPRITE_NAMES_WHITE.remove(item)
    except Exception as e:
        a = 1
    try:
        SPRITE_NAMES_BLACK.remove(item)
    except Exception as e:
        a = 1
    try:
        SPRITE_NAMES.remove(item)
    except Exception as e:
        a = 1
    try:
        PAWN.remove(item)
    except Exception as e:
        a = 1
    try:
        ROOK.remove(item)
    except Exception as e:
        a = 1
    try:
        KNIGHT.remove(item)
    except Exception as e:
        a = 1
    try:
        BISHOP.remove(item)
    except Exception as e:
        a = 1
    try:
        QUEEN.remove(item)
    except Exception as e:
        a = 1
    try:
        KING.remove(item)
    except Exception as e:
        a = 1
    SPRITE_LOCATIONS.pop(item)


def makeQueen():
    global PAWN, QUEEN
    for item in PAWN:
        if item in SPRITE_NAMES_BLACK:
            if SPRITE_LOCATIONS[item][0] == 1:
                PAWN.remove(item)
                QUEEN.append(item)
                SPRITE_IMAGES[item] = pygame.image.load(f"Gallery/b5.png")
                playSound("kill")
        if item in SPRITE_NAMES_WHITE:
            if SPRITE_LOCATIONS[item][0] == 8:
                PAWN.remove(item)
                QUEEN.append(item)
                SPRITE_IMAGES[item] = pygame.image.load(f"Gallery/w5.png")
                playSound("kill")


def gameOver():
    global GAME_OVER
    if "w15" not in SPRITE_NAMES_WHITE:
        GAME_OVER = True
        resetGame()
        playSound("win")
    if "b85" not in SPRITE_NAMES_BLACK:
        GAME_OVER = True
        resetGame()
        playSound("win")


def selectPlayer(row, column):
    global SPRITE_SELECTED, CLICKED_SPRITE
    sprite_iter = []
    if TURN_BLACK:
        sprite_iter = SPRITE_NAMES_BLACK
    else:
        sprite_iter = SPRITE_NAMES_WHITE
    for i in range(len(sprite_iter)):
        try:
            key = sprite_iter[i]
            value = SPRITE_LOCATIONS[key]
            if value[0] == row and value[1] == column:
                CLICKED_SPRITE = key
                break
        except Exception as e:
            CLICKED_SPRITE = ""
    if CLICKED_SPRITE == "":
        SPRITE_SELECTED = False
    else:
        SPRITE_SELECTED = True
        playerRole()
        playSound("start_click")


def movePlayer(row, column):
    global SPRITE_LOCATIONS, SPRITE_SELECTED, CLICKED_SPRITE
    global TURN_BLACK, TURN_WHITE, BLUE_BOXES, VALID_BOXES, VALID_TURN
    if [row, column] in VALID_BOXES:
        VALID_TURN = True
    else:
        VALID_TURN = False
    playSound("start_click")
    if VALID_TURN:
        if [row, column] in KILL_POSITION:
            for item in SPRITE_LOCATIONS:
                if row == SPRITE_LOCATIONS[item][0] and column == SPRITE_LOCATIONS[item][1]:
                    removeSprite(item)
                    playSound("kill")
                    break
        SPRITE_LOCATIONS[CLICKED_SPRITE] = [row, column]
        TURN_BLACK, TURN_WHITE = TURN_WHITE, TURN_BLACK
    SPRITE_SELECTED = False
    CLICKED_SPRITE = ""
    BLUE_BOXES = []
    makeQueen()
    gameOver()


def boxClick(x, y):
    row, column = 1, 1
    for i in range(len(BOX_X)):
        item = BOX_X[i]
        if x in range(item[0], item[1] + 1):
            column = i + 1
            break
    for i in range(len(BOX_Y)):
        item = BOX_Y[i]
        if y in range(item[0], item[1] + 1):
            row = i + 1
            break
    if SPRITE_SELECTED:
        movePlayer(row, column)
    else:
        selectPlayer(row, column)


def resetGame():
    global GAME_OVER, TURN_BLACK, TURN_WHITE, START_GAME
    GAME_OVER = False
    TURN_WHITE = True
    TURN_BLACK = False
    START_GAME = True
    setVariables()


def mainGame():
    global START_GAME
    while True:
        if START_GAME:
            updateScreen(SPRITE_IMAGES['start'], 0, 0)
            SCREEN.blit(FONT.render("Click anywhere to start", True, "black"), [SCREENWIDTH / 4, SCREENHEIGHT / 4])
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    START_GAME = False
        else:
            updateScreen(SPRITE_IMAGES['board'], 0, 0)
            showSprites()
            for item in BLUE_BOXES:
                drawRect((135, 206, 250), item[0], item[1], item[2], item[3])
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if not GAME_OVER:
                        boxClick(x, y)
        pygame.display.update()


if __name__ == '__main__':
    pygame.display.set_caption("Chess Game By Saksham")
    pygame.display.set_icon(pygame.image.load("icon.ico"))
    setVariables()
    mainGame()
