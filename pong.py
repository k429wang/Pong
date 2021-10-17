#First Fame using Python: Pong
#Kai Wang, August 13, 2019
import pygame
import sys

#background colours
backgroundLite=(250,250,250)       
backgroundDark=(50,50,50)

#define screen size
screenWidth = 1400     
screenLength = 800

#initiates the game
pygame.init()

#sets the parameters to the window size we choosed
gameWindow = pygame.display.set_mode( (screenWidth, screenLength) ) 

#displays the title of the game
pygame.display.set_caption("Pong by Kai Wang")

#text box on screen
font = pygame.font.Font('freesansbold.ttf', 32)

leftScoreValue=0
leftScore = font.render(("SCORE:" + str(leftScoreValue)), True, (100,150,0))
textRect0 = leftScore.get_rect()
textRect0.center = (100, 60)

rightScoreValue=0
rightScore = font.render(("SCORE:" + str(rightScoreValue)), True, (100,150,0))
textRect1 = rightScore.get_rect()
textRect1.center = (screenWidth-100, 60)

#loads the music and sound files
bounceSound=pygame.mixer.Sound("bounce.wav")

#sets up a clock for the game and keeps track of time
clock = pygame.time.Clock()

class Ball:
    def __init__(self, xPos, yPos, size, color, xSpeed = 0, ySpeed = 0):
        self.xPos = xPos
        self.yPos = yPos
        self.xSpeed = 20
        self.ySpeed = 5
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.xPos, self.yPos, self.size, self.size)

    def move(self):
        self.xPos += self.xSpeed
        self.yPos += self.ySpeed
        self.rect = pygame.Rect(self.xPos, self.yPos, self.size, self.size)

    def wallDetect(self):
        global leftScoreValue
        global rightScoreValue
        #Left wall
        if (self.xPos <= 0):
            self.xSpeed *= -1
            rightScoreValue += 1
        #Right wall
        elif(self.xPos + self.size >= screenWidth):
            self.xSpeed *= -1
            leftScoreValue += 1
        #Top wall OR bottom
        elif (self.yPos <= 0 or self.yPos + self.size >= screenLength):
            self.ySpeed *= -1

    def draw(self):
        pygame.draw.rect(gameWindow, self.color, self.rect)

class Paddle0:
    def __init__(self, xPos, yPos, width, height, color, speed, isAI=False):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)

    def getBall(self, aBall):
        self.aBall = aBall

    def ballCollide(self):
        if (self.rect.colliderect(self.aBall.rect)):
            if (self.aBall.xSpeed < 0):
                pygame.mixer.Sound.play(bounceSound)
            self.aBall.xSpeed *= -1
            self.aBall.xPos = self.xPos + 1
            pygame.mixer.Sound.play(bounceSound)

    def move(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            if(self.yPos-self.speed<0):
                self.yPos=0
            else:
                self.yPos -= self.speed
            
        if pressed[pygame.K_s]:
            if((self.yPos+self.height)+self.speed>screenLength):
                self.yPos=screenLength-self.height
            else:
                self.yPos += self.speed

        self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        
    def draw(self):
        pygame.draw.rect(gameWindow, self.color, self.rect)


class Paddle1:
    def __init__(self, xPos, yPos, width, height, color, speed, isAI=True):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.isAI = isAI
        self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)

    def getBall(self, aBall):
        self.aBall = aBall

    def ballCollide(self):
        if (self.rect.colliderect(self.aBall.rect)):
            if (self.aBall.xSpeed > 0):
                pygame.mixer.Sound.play(bounceSound)
            self.aBall.xSpeed *= -1
            self.aBall.xPos = self.xPos - self.aBall.size - 30
            
    def move(self):
        if(not self.isAI):
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if(self.yPos-self.speed<0):
                    self.yPos=0
                else:
                    self.yPos -= self.speed
                
            if pressed[pygame.K_DOWN]:
                if((self.yPos+self.height)+self.speed>screenLength):
                    self.yPos=screenLength-self.height
                else:
                    self.yPos += self.speed
        else:
            if(self.aBall.yPos<self.yPos):
                self.yPos-=self.speed
                #if(self.yPos-self.speed<0):
                    #self.yPos=0
                #else:
                    #self.yPos -= self.speed
            elif(self.aBall.yPos>self.yPos+self.height):
                self.yPos+=self.speed
                #if((self.yPos+self.height)+self.speed>screenLength):
                    #self.yPos=screenLength-self.height
                #else:
                    #self.yPos += self.speed
            

        self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        
    def draw(self):
        pygame.draw.rect(gameWindow, self.color, self.rect)        
        
gameBall = Ball(screenWidth/2, screenLength/2, 30, (250,0,155), 0, 0) 
#qameBall = Ball(180, screenLength - 200, 50, (200,200,0), 20, 10)
#wameBall = Ball(400, screenLength - 700, 50, (200,100,50), 20, 10)
#eameBall = Ball(800, screenLength - 230, 50, (150,250,100), 20, 10)

leftPaddle = Paddle0(20, screenLength/2, 15, 130, (200,100,100), 30, False)
rightPaddle = Paddle1(screenWidth-35, screenLength/2, 15, 130, (100,100,200), 20, True)
#Main Game Loop
#loop forever until user quits
while True:

    #goes through every event that occurs in pygame and executes code accordingly
    for event in pygame.event.get():

        #checks for the quit event
        if event.type == pygame.QUIT:

            #quit the program
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rightPaddle.isAI = not rightPaddle.isAI

    #fill the background colour
    gameWindow.fill(backgroundDark)

    #draw a ball
    gameBall.move()
    gameBall.wallDetect()
    gameBall.draw()

    #draw the paddles
    leftPaddle.draw()
    leftPaddle.getBall(gameBall)
    leftPaddle.move()
    leftPaddle.ballCollide()
    rightPaddle.draw()
    rightPaddle.getBall(gameBall)
    rightPaddle.ballCollide()
    rightPaddle.move()

    #display the scores
    leftScore = font.render(("SCORE:" + str(leftScoreValue)), True, (100,150,0))
    rightScore = font.render(("SCORE:" + str(rightScoreValue)), True, (100,150,0))
    gameWindow.blit(leftScore, textRect0)
    gameWindow.blit(rightScore, textRect1)

    #update gameWindow's graphics
    pygame.display.flip()

    #sets maximum framrate
    clock.tick(60)
