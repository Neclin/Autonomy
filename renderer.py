import pygame

from settings import cellSize
from placer import Placer
from level import Level
from settings import *

class Renderer():
    gridCellSprite = pygame.image.load("assets/light/gridCell.png")

    cursor1X1 = pygame.image.load("assets/cursor1X1.png")


    @classmethod
    def mapToGrid(self, x, y):
        return pygame.Vector2((x - Level.offset.x) // cellSize * cellSize + Level.offset.x, (y - Level.offset.y) // cellSize * cellSize + Level.offset.y)

    @classmethod
    def isPointInGrid(self, point):
        if point.x > Level.offset.x and point.x < Level.offset.x + Level.width * cellSize and point.y > Level.offset.y and point.y < Level.offset.y + Level.height * cellSize:
            return True
        return False

    @classmethod
    def update(self, window, DT):
        window.fill((204,204,204))

        self.drawGrid(window)
        self.drawCursor(window)

        for conveyor in Level.conveyors:
            conveyor.show(Level.offset, window)
        
        for path in Level.paths:
            path.show(window)
        
        for item in Level.items:
            item.moveForwards(DT)
            item.show(window)
                
#        for i, point in enumerate(Placer.points):
#            # red = 0 blue = 1
#            pygame.draw.circle(window, (255 * ((i + 1)%2),0,255 * (i%2)), point, 3)
            
        pygame.display.update()
    
    @classmethod
    def drawGrid(self, window):
        # draw the grid
        for y in range(0, Level.height):
            y = y * cellSize
            for x in range(0, Level.width):
                x = x * cellSize
                window.blit(self.gridCellSprite, (Level.offset.x + x, Level.offset.y + y))
    
    @classmethod
    def drawCursor(self, window):
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])
        if self.isPointInGrid(mousePos):
            mousePos = self.mapToGrid(mousePos.x, mousePos.y)
            self.cursor1X1 = pygame.image.load("assets/cursor1X1.png")
            self.cursor1X1 = pygame.transform.rotate(self.cursor1X1, Placer.rotation)
            if Placer.rotation % 180 == 0:
                window.blit(self.cursor1X1, (mousePos.x - cellSize, mousePos.y))
            else:
                window.blit(self.cursor1X1, (mousePos.x, mousePos.y - cellSize))