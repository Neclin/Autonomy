import pygame
from buildings.belt import Belt

from settings import cellSize, screenWidth, screenHeight
from managers.placer import Placer
from managers.level import Level
from settings import *


class Renderer:
    # loads constant sprites
    gridCellSprite = pygame.image.load("assets/light/gridCell.png")
    gridCellSprite = pygame.transform.smoothscale(gridCellSprite, (cellSize, cellSize))

    cursor1X1 = pygame.image.load("assets/cursor1X1.png")

    screenPos = pygame.Vector2(0, 0)
    cameraVel = pygame.Vector2(100, 100)

    @classmethod
    def init(cls):
        cls.screenPos = pygame.Vector2(Level.width * cellSize / 2 - screenWidth / 2,
                                       Level.height * cellSize / 2 - screenHeight / 2)

    @classmethod  # snaps a point to the grid
    def mapToGrid(cls, x, y):
        return pygame.Vector2((x - Level.offset.x) // cellSize * cellSize + Level.offset.x,
                              (y - Level.offset.y) // cellSize * cellSize + Level.offset.y)

    @classmethod  # checks if a point is in the grid and not outside the grid
    def isPointInGrid(cls, point):
        if Level.offset.x < point.x < Level.offset.x + Level.width * cellSize and Level.offset.y < point.y < Level.offset.y + Level.height * cellSize:
            return True
        return False

    @classmethod  # draws all entities of the screen
    def update(cls, window, dt, animationFrames):
        window.fill((204, 204, 204))  # fills the background colour

        # print(self.screenPos.x, self.screenPos.y)

        cls.drawGrid(window)

        offsetX = cls.screenPos.x % cellSize
        offsetY = cls.screenPos.y % cellSize
        # draw each square of the grid
        for y in range(0, screenHeight + cellSize, cellSize):
            for x in range(0, screenWidth + cellSize, cellSize):
                levelX = int((x + cls.screenPos.x) // cellSize)
                levelY = int((y + cls.screenPos.y) // cellSize)
                building = Level.array[levelY][levelX]
                if isinstance(building, Belt):
                    # building.pos = pygame.Vector2(x - offsetX, y - offsetY)
                    # building.genPoints()
                    building.show(window, cls.screenPos, animationFrames["belt"])

        # debugging layer
        for y in range(0, screenHeight + cellSize, cellSize):
            for x in range(0, screenWidth + cellSize, cellSize):
                levelX = int((x + cls.screenPos.x) // cellSize)
                levelY = int((y + cls.screenPos.y) // cellSize)
                building = Level.array[levelY][levelX]
                if isinstance(building, Belt):
                    building.debug(window, cls.screenPos)

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

        cls.drawCursor(window)

        pygame.display.update()

    @classmethod  # draws the grid
    def drawGrid(cls, window):
        offsetX = cls.screenPos.x % cellSize
        offsetY = cls.screenPos.y % cellSize
        # draw each square of the grid
        for y in range(0, screenHeight + cellSize, cellSize):
            for x in range(0, screenWidth + cellSize, cellSize):
                window.blit(cls.gridCellSprite, (x - offsetX, y - offsetY))

    @classmethod  # draws the cursor
    def drawCursor(cls, window):
        # gets the mouse position and converts it to a vector
        mousePos = pygame.mouse.get_pos()
        offsetX = cls.screenPos.x % cellSize
        offsetY = cls.screenPos.y % cellSize
        levelX = (mousePos[0] + offsetX) // cellSize
        levelY = (mousePos[1] + offsetY) // cellSize

        # reloads and rotates the cursor sprite
        cls.cursor1X1 = pygame.image.load("assets/cursor1X1.png")
        cls.cursor1X1 = pygame.transform.smoothscale(cls.cursor1X1, (cellSize * 3, cellSize))
        cls.cursor1X1 = pygame.transform.rotate(cls.cursor1X1, Placer.rotation)

        # positions the cursor depending on the rotation
        # when the cursor is rotated 90 or 270 degrees it is moved up
        # when the cursor is rotated 0 or 180 degrees it is moved left
        if Placer.rotation % 180 == 0:
            window.blit(cls.cursor1X1, (levelX * cellSize - cellSize - offsetX, levelY * cellSize - offsetY))
        else:
            window.blit(cls.cursor1X1, (levelX * cellSize - offsetX, levelY * cellSize - cellSize - offsetY))
