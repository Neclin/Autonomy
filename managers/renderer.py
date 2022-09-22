import pygame
from buildings.belt import Belt

from settings import cellSize, screenWidth, screenHeight
from managers.placer import Placer
from managers.level import Level
from settings import *

class Renderer():
    # loads constant sprites
    gridCellSprite = pygame.image.load("assets/light/gridCell.png")
    gridCellSprite = pygame.transform.smoothscale(gridCellSprite, (cellSize, cellSize))

    cursor1X1 = pygame.image.load("assets/cursor1X1.png")

    screenPos = pygame.Vector2(0, 0)
    cameraVel = pygame.Vector2(100, 100)

    @classmethod
    def init(self):
        self.screenPos = pygame.Vector2(Level.width * cellSize / 2 - screenWidth / 2, Level.height * cellSize / 2 - screenHeight / 2)

    @classmethod # snaps a point to the grid
    def mapToGrid(self, x, y):
        return pygame.Vector2((x - Level.offset.x) // cellSize * cellSize + Level.offset.x, (y - Level.offset.y) // cellSize * cellSize + Level.offset.y)

    @classmethod # checks if a point is in the grid and not outside the grid
    def isPointInGrid(self, point):
        if point.x > Level.offset.x and point.x < Level.offset.x + Level.width * cellSize and point.y > Level.offset.y and point.y < Level.offset.y + Level.height * cellSize:
            return True
        return False

    @classmethod # draws all entities of the screen
    def update(self, window, dt, animationFrames):
        window.fill((204,204,204)) # fills the background colour

        # print(self.screenPos.x, self.screenPos.y)

        self.drawGrid(window)

        offsetX = self.screenPos.x % cellSize
        offsetY = self.screenPos.y % cellSize
        # draw each square of the grid
        for y in range(0, screenHeight+cellSize, cellSize):
            for x in range(0, screenWidth+cellSize, cellSize):
                levelX = int((x + self.screenPos.x) // cellSize)
                levelY = int((y + self.screenPos.y) // cellSize)
                building = Level.array[levelY][levelX]
                if isinstance(building, Belt):
                    # building.pos = pygame.Vector2(x - offsetX, y - offsetY)
                    # building.genPoints()
                    building.pos = pygame.Vector2(x - offsetX, y - offsetY)
                    building.show(window, animationFrames["belt"])

        # debugging layer
        for y in range(0, screenHeight+cellSize, cellSize):
            for x in range(0, screenWidth+cellSize, cellSize):
                levelX = int((x + self.screenPos.x) // cellSize)
                levelY = int((y + self.screenPos.y) // cellSize)
                building = Level.array[levelY][levelX]
                if isinstance(building, Belt):
                    building.debug(window)

        # draws all belts
        # for belt in Level.belts:
        #     belt.show(Level.offset, window, animationFrames["belt"])
        
        # draws all paths
        for path in Level.paths:
            path.show(window)
        
        # draws all items
        for item in Level.items:
            item.show(window, dt)

        # draw the buttons
        for button in Level.buttons:
            button.show(window)
                
        # for i, point in enumerate(Placer.points):
        #     # red = 0 blue = 1
        #     pygame.draw.circle(window, (255 * ((i + 1)%2),0,255 * (i%2)), point, 3)
            
        self.drawCursor(window)
        
        pygame.display.update()
    
    @classmethod # draws the grid
    def drawGrid(self, window):
        offsetX = self.screenPos.x % cellSize
        offsetY = self.screenPos.y % cellSize
        # draw each square of the grid
        for y in range(0, screenHeight+cellSize, cellSize):
            for x in range(0, screenWidth+cellSize, cellSize):
                window.blit(self.gridCellSprite, (x - offsetX, y - offsetY))
    
    @classmethod # draws the cursor
    def drawCursor(self, window):
        # gets the mouse position and converts it to a vector
        mousePos = pygame.mouse.get_pos()
        offsetX = self.screenPos.x % cellSize
        offsetY = self.screenPos.y % cellSize
        levelX = (mousePos[0]+offsetX) // cellSize
        levelY = (mousePos[1]+offsetY) // cellSize

        # reloads and rotates the cursor sprite
        self.cursor1X1 = pygame.image.load("assets/cursor1X1.png")
        self.cursor1X1 = pygame.transform.smoothscale(self.cursor1X1, (cellSize*3, cellSize))
        self.cursor1X1 = pygame.transform.rotate(self.cursor1X1, Placer.rotation)

        # positons the cursor depending on the rotaion
        # when the cursor is rotated 90 or 270 degrees it is moved up
        # when the cursor is rotated 0 or 180 degrees it is moved left
        if Placer.rotation % 180 == 0:
            window.blit(self.cursor1X1, (levelX*cellSize - cellSize - offsetX, levelY*cellSize - offsetY))
        else:
            window.blit(self.cursor1X1, (levelX*cellSize - offsetX, levelY*cellSize - cellSize - offsetY))