import pygame

from settings import cellSize
from placer import Placer
from level import Level
from settings import *

class Renderer():
    # loads constant sprites
    gridCellSprite = pygame.image.load("assets/light/gridCell.png")

    cursor1X1 = pygame.image.load("assets/cursor1X1.png")

    @classmethod # snaps a point to the grid
    def mapToGrid(self, x, y):
        return pygame.Vector2((x - Level.offset.x) // cellSize * cellSize + Level.offset.x, (y - Level.offset.y) // cellSize * cellSize + Level.offset.y)

    @classmethod # checks if a point is in the grid and not outside the grid
    def isPointInGrid(self, point):
        if point.x > Level.offset.x and point.x < Level.offset.x + Level.width * cellSize and point.y > Level.offset.y and point.y < Level.offset.y + Level.height * cellSize:
            return True
        return False

    @classmethod # draws all entities of the screen
    def update(self, window, DT):
        window.fill((204,204,204)) # fills the background colour

        self.drawGrid(window)
        self.drawCursor(window)

        # draws all conveyors
        for conveyor in Level.conveyors:
            conveyor.show(Level.offset, window)
        
        # draws all paths
        for path in Level.paths:
            path.show(window)
        
        # draws all items
        for item in Level.items:
            item.moveForwards(DT)
            item.show(window)
                
        # for i, point in enumerate(Placer.points):
        #     # red = 0 blue = 1
        #     pygame.draw.circle(window, (255 * ((i + 1)%2),0,255 * (i%2)), point, 3)
            
        pygame.display.update()
    
    @classmethod # draws the grid
    def drawGrid(self, window):
        # draw each square of the grid
        for y in range(0, Level.height):
            y_ = y * cellSize
            for x in range(0, Level.width):
                x_ = x * cellSize
                window.blit(self.gridCellSprite, (Level.offset.x + x_, Level.offset.y + y_))
    
    @classmethod # draws the cursor
    def drawCursor(self, window):
        # gets the mouse position and converts it to a vector
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])

        # checks if the point is in the grid if not dont draw the cursor
        if self.isPointInGrid(mousePos):
            # gets the lopleft of the grid square the mouse is in
            mousePos = self.mapToGrid(mousePos.x, mousePos.y)
            # reloads and rotates the cursor sprite
            self.cursor1X1 = pygame.image.load("assets/cursor1X1.png")
            self.cursor1X1 = pygame.transform.rotate(self.cursor1X1, Placer.rotation)

            # positons the cursor depending on the rotaion
            # when the cursor is rotated 90 or 270 degrees it is moved up
            # when the cursor is rotated 0 or 180 degrees it is moved left
            if Placer.rotation % 180 == 0:
                window.blit(self.cursor1X1, (mousePos.x - cellSize, mousePos.y))
            else:
                window.blit(self.cursor1X1, (mousePos.x, mousePos.y - cellSize))