import pygame

from eventManager import EventManager

from level import Level
from settings import *

class Renderer():
    gridCellSprite = pygame.image.load("assets/light/gridCell.png")

    # offset to center the grid
    offset = pygame.Vector2(0,0)

    @classmethod
    def init(self):
        self.offset = pygame.Vector2(screenWidth/2 - (Level.width * cellSize)/2, screenHeight/2 - (Level.height * cellSize)/2)

    def update(self, window):
        window.fill((204,204,204))

        self.drawGrid(self, window)

        for conveyor in Level.conveyors:
            conveyor.show(self.offset, window)

        pygame.display.update()
    
    
    def drawGrid(self, window):
        # draw the grid
        for y in range(0, Level.height):
            y = y * cellSize
            for x in range(0, Level.width):
                x = x * cellSize
                window.blit(self.gridCellSprite, (self.offset.x + x, self.offset.y + y))