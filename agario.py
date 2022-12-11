
## Authors : Thomas Gaubert - Pauline Peyronnel - Mélanie Romano

#chargement des modules
import pygame
import time
from random import *
import math

# Définition des classes
class GameConfig :
    windowW = 800
    windowH = 500
    background = pygame.transform.scale (pygame.image.load('background.jpg'), (windowW, windowH))
    white = (255, 255, 255)

class GameState :
    def __init__(self):
        # init ball size and position
        self.ballR = 15
        self.ballThickness = 5
        self.ballX = GameConfig.windowW/2 - self.ballR/2;
        self.ballY = GameConfig.windowH/2 - self.ballR/2 + 150;
        # create and generate random food
        self.food = foodPoint(8)
        self.food.generatePoint(50)
        # init score
        self.score = 0
        self.highestScore = 400

    def draw(self, window) :
        # display background
        window.blit(GameConfig.background, (0, 0))
        # display food
        self.food.draw(window)
        # dsiplay player circle
        playerBorder = Circle(int(self.ballX), int(self.ballY), self.ballR, (255, 50 , 50))
        playerCircle = Circle(int(self.ballX), int(self.ballY), (self.ballR - self.ballThickness), (255, 100 , 100))
        playerBorder.draw(window)
        playerCircle.draw(window)
        # display interface
        displayMessage(window, "Score:", 20, 30, 20)
        displayMessage(window, str(self.score), 20, 70, 20)
        displayMessage(window, "Appuyer sur Esc/ Echap pour terminer la partie", 20, 400, 20)


    def advanceState(self, moveX, moveY) :
        # new positon of the circle
        self.ballX += moveX
        self.ballY += moveY
        # check if pa=layer is on food point
        upScore = self.food.onAPoint(int(self.ballX), int(self.ballY), int(self.ballR))
        if upScore :
            self.markScore()
    # increment score and trigger player growth
    def markScore(self) :
        self.score += 1
        if (self.score % (self.highestScore/100)) == 0 :
            self.growPlayer()

    # makes the player bigger
    def growPlayer(self) :
        self.ballR += 1
        self.ballThickness = int(self.ballR / 3)

    def findClosestPoint(self) :
        closest = self.food.coord[0]
        shortestDistance = 1000
        length = len(self.food.coord)
        for index in range(0,length):
            (currentX, currentY) = self.food.coord[index]
            distance = abs(math.sqrt((self.ballX - currentX) ** 2 + (self.ballY - currentY) ** 2))
            if distance < shortestDistance :
                shortestDistance = distance
                closest = self.food.coord[index]
        return closest


    # got to tbhe point (x, y)
    def goToPoint(self, goalX, goalY) :
        destX = 0
        destY = 0
        if goalX - Move.speed < self.ballX :
            destX = Move.Left
        elif goalX + Move.speed > self.ballX :
            destX = Move.Right
        if goalY - Move.speed < self.ballY :
            destY = Move.Up
        elif goalY + Move.speed > self.ballY :
            destY = Move.Down
        return (destX, destY)

    # check if the game is over
    def checkGameOver(self, window) :
        # check boudnaries
        notOutOfBoundLeft = self.ballX + self.ballR > 0
        notOutOfBoundRight = self.ballX  - self.ballR < GameConfig.windowW
        notOutOfBoundUp = self.ballY + self.ballR > 0
        notOutOfBoundDown =  self.ballY - self.ballR < GameConfig.windowH
        if not notOutOfBoundLeft or not notOutOfBoundRight or not notOutOfBoundUp or not notOutOfBoundDown :
            displayMessage(window, "Perdu", 225, GameConfig.windowW/2, (GameConfig.windowH/2)-70)
            return True
        if self.score >= self.highestScore :
            displayMessage(window, "Gagné", 225, GameConfig.windowW/2, (GameConfig.windowH/2)-70)
            return True
        return False

#move of the player
class Move :
    speed = 1
    Up = -speed
    Down = speed
    Left = -speed
    Right = speed

# to draw a circle
class Circle :
    def __init__(self, x, y, r, col):
        self.x = x
        self.y = y
        self.r = r
        self.col = col

    def draw(self, window) :
        pygame.draw.circle(window, self.col, (self.x, self.y), self.r)
    #collisions management :
    #math.sqrt((x2-x1)² + (y2-y1)²) =< (c1.r + c2.r)

# food
class foodPoint :
    def __init__ (self, size) :
        self.coord = []
        self.littleR = size
        self. color = (randrange(150,255), randrange(150,255) , randrange(150,255))
    # draw, must be used after generate
    def draw (self, window) :
        k = 0
        while k<len(self.coord):
            (coordX,coordY) = self.coord[k]
            point = Circle(int(coordX), int(coordY), self.littleR, self.color)
            point.draw(window)
            k = k+1
    # generate random food points
    def generatePoint(self, nbPoints) :
        i = 0
        while i < nbPoints :
            j = GameConfig.windowW-self.littleR
            z = self.littleR+10
            x = randrange(self.littleR,j,z)
            j = GameConfig.windowH-self.littleR
            z = self.littleR+10
            y = randrange(self.littleR,j,z)
            if not self.coord :
                self.coord.append((x,y))
            else :
                k = 0
                while k<len(self.coord):
                    (coordX,coordY) = self.coord[k]
                    if x == coordX and  y == coordY :
                        while x != coordX or y != coordY :
                            j = GameConfig.windowW-self.littleR
                            x = randrange(self.littleR,j,self.littleR)
                            j = GameConfig.windowH-self.littleR
                            y = randrange(self.littleR,j,self.littleR)
                    k = k+1
                self.coord.append((x,y))
            i = i+1

    # know if the circle is on a food point
    def onAPoint(self, coordx, coordy, radius) :
        b = False
        length = len(self.coord)
        for index in range(0,length):
            (coordX,coordY) = self.coord[index]
            minusX = coordX-self.littleR >= coordx-radius
            plusX = coordX+self.littleR <= coordx+radius
            minusY = coordY-self.littleR >= coordy-radius
            plusY = coordY+self.littleR <= coordy+radius
            if plusY and minusX and plusX and minusY :
                b = True
                self.coord.remove((coordX, coordY))
                self.generatePoint(1)
        return b;

# fonction du jeu
def gameLoop(window, horloge) :
    game_over = False
    gameState = GameState()
    moveX = 0
    moveY = 0
    autoMode = False
    boost = False

    while not game_over :
        for event in pygame.event.get() :
            # check if game is over
            if event.type == pygame.QUIT :
                game_over = True
        # get pressed keys
        keys = pygame.key.get_pressed()
        # move 
        if keys[pygame.K_UP] :
            moveY = Move.Up
            if boost :
                moveY = Move.Up * 2
        elif keys[pygame.K_DOWN] :
            moveY = Move.Down
            if boost :
                moveY = Move.Down * 2
        # smooth stop
        else :
            moveY *= 0.95
        if keys[pygame.K_LEFT] :
            moveX = Move.Left
            if boost :
                moveX = Move.Left * 2
        elif keys[pygame.K_RIGHT] :
            moveX = Move.Right
            if boost :
                moveX = Move.Right * 2
        # smooth stop
        else :
            moveX *= 0.95
        # stop current game
        if keys[pygame.K_ESCAPE] :
            game_over = True
        if keys[pygame.K_a] :
            autoMode = not autoMode
        if keys[pygame.K_SPACE] :
            boost = True
        else :
            boost = False
        # auto mode
        if autoMode :
            (goalX, goalY) = gameState.findClosestPoint()
            (valueX, valueY) = gameState.goToPoint(goalX, goalY)
            moveX = valueX
            moveY = valueY
        # update datas    
        gameState.advanceState(moveX, moveY)
        # elemnts à afficher
        gameState.draw(window)
        # check if the player is out of boudarie
        game_over = gameState.checkGameOver(window) or game_over
        #display message if game is over
        if game_over :
            displayMessage(window, "Partie Terminée", 125, GameConfig.windowW/2, (GameConfig.windowH/2)+80)
            displayMessage(window, "Appuyer sur une touche pour relancer une partie", 40, GameConfig.windowW/2, (GameConfig.windowH/2) + 160)
        horloge.tick(100)
        # afficher les élémnts chargés
        pygame.display.update()
    if playAgain() :
        gameLoop(window, horloge)
        
def displayMessage(window, text, fontSize, x, y) :
    font = pygame.font.Font('BebasNeue-Regular.ttf', fontSize)
    img = font.render(text, True, GameConfig.white)
    displayRect = img.get_rect()
    displayRect.center=(x,y)
    window.blit(img, displayRect)

def playAgain() :
    time.sleep(2)
    while True :
        for event in pygame.event.get([pygame.KEYDOWN, pygame.QUIT]) :
            if event.type == pygame.QUIT :
                return False
            elif event.type == pygame.KEYDOWN :
                return True
        time.sleep(0.5)

# boucle de jeu

# fonction principale
def main() :
    pygame.init()
    window = pygame.display.set_mode((GameConfig.windowW, GameConfig.windowH))
    pygame.display.set_caption("Agario")
    horloge = pygame.time.Clock()
    gameLoop(window, horloge)
    pygame.quit()
    quit()

# lancement fonction principale
main()
