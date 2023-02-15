import pygame

from settings import CELLSIZE, SCREENWIDTH, SCREENHEIGHT
from modules import *

class Renderer():
    def __init__(self, screenWidth, screenHeight, camera=None, caption="Pygame Window"):
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(caption)

        self.camera = camera

        self.animationFrame = 0

    def updateScreen(self, world, eventManager):
        # clears the screen
        self.win.fill((51,51,51))

        # draw the outline of the camera
        if self.camera:
            pygame.draw.rect(self.win, (0, 0, 0), self.camera.rect, 1)

        # draw a grid over the screen
        self.camera.drawGrid(self.win)

        for gameObject in world.gameObjects:
            if (gameObject.worldPosition.x + gameObject.width >= self.camera.worldPosition.x 
            and gameObject.worldPosition.x <= self.camera.worldPosition.x + self.camera.width 
            and gameObject.worldPosition.y + gameObject.height >= self.camera.worldPosition.y 
            and gameObject.worldPosition.y <= self.camera.worldPosition.y + self.camera.height):
                gameObject.show(self, self.camera)

        self.drawCursor(eventManager)
        self.drawBeltsPath(eventManager)

        pygame.display.update()

    def drawCursor(self, eventManager):
        snappedScreenMousePosition = convertWorldToScreenPosition(eventManager.snappedWorldMousePosition, self.camera)
        middle = snappedScreenMousePosition + pygame.Vector2(CELLSIZE/2, CELLSIZE/2)

        pygame.draw.rect(self.win, (255, 255, 255), (snappedScreenMousePosition.x, snappedScreenMousePosition.y, CELLSIZE, CELLSIZE), 1)
        pygame.draw.line(self.win, (100,100,255), middle, middle - eventManager.startDirection * CELLSIZE/2, 2)
        pygame.draw.line(self.win, (255,100,100), middle, middle + eventManager.endDirection * CELLSIZE/2, 2)

    def drawBeltsPath(self, eventManager):
        if eventManager.position1:
            snappedScreenMousePosition = convertWorldToScreenPosition(eventManager.snappedWorldMousePosition, self.camera)
            screenPosition1 = convertWorldToScreenPosition(eventManager.position1, self.camera)
            if abs(eventManager.startDirection.x) == 1:
                anchor = pygame.Vector2(screenPosition1.x, snappedScreenMousePosition.y)
            else:
                anchor = pygame.Vector2(snappedScreenMousePosition.x, screenPosition1.y)
            halfCellSize = pygame.Vector2(CELLSIZE/2, CELLSIZE/2)
            pygame.draw.line(self.win, (255,255,0), screenPosition1+halfCellSize, anchor+halfCellSize)
            pygame.draw.line(self.win, (255,255,0), anchor+halfCellSize, snappedScreenMousePosition+halfCellSize)

    def incrementAnimationFrame(self):
        self.animationFrame += 1
        self.animationFrame %= 8


class Camera():
    def __init__(self, x, y, width, height, velocity, world):
        self.position = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        self.worldPosition = pygame.Vector2(0, 0)
        self.velocity = velocity

        self.world = world


    def focus(self, gameObject):
        gameObjectMiddle = pygame.Vector2(gameObject.worldPosition.x + gameObject.width / 2, gameObject.worldPosition.y + gameObject.height / 2)
        self.worldPosition = pygame.Vector2(gameObjectMiddle.x - self.width / 2, gameObjectMiddle.y - self.height / 2)

        self.worldPosition.x = max(0, self.worldPosition.x)
        self.worldPosition.y = max(0, self.worldPosition.y)

        self.worldPosition.x = min(self.worldPosition.x, self.world.width - self.width)
        self.worldPosition.y = min(self.worldPosition.y, self.world.height - self.height)

    def drawGrid(self, win):
        # the offset for each grid square
        gridOffset = pygame.Vector2(0, 0)
        gridOffset.x = self.worldPosition.x % CELLSIZE
        gridOffset.y = self.worldPosition.y % CELLSIZE

        # the offset of the array
        arrayOffset = pygame.Vector2(0, 0)
        arrayOffset.x = self.worldPosition.x // CELLSIZE
        arrayOffset.y = self.worldPosition.y // CELLSIZE
        
        # draw a grid over the screen
        for y in range(0, self.height+CELLSIZE, CELLSIZE):
            for x in range(0, self.width+CELLSIZE, CELLSIZE):
                
                pygame.draw.rect(win, (0, 0, 0), 
                (self.position.x + x - gridOffset.x, 
                self.position.y + y - gridOffset.y, 
                CELLSIZE, CELLSIZE), 1)
