import pygame

from level import Level
from settings import *

class Renderer():

    gridCell = pygame.image.load("assets/light/gridCell.png")

    @classmethod
    def update(self, window):
        window.fill((204,204,204))

        # offset to center the grid
        offset = pygame.Vector2(screenWidth/2 - (Level.width * cellSize)/2, screenHeight/2 - (Level.height * cellSize)/2)
        # draw the grid
        for y in range(0, Level.height):
            y = y * cellSize
            for x in range(0, Level.width):
                x = x * cellSize
                window.blit(self.gridCell, (offset.x + x, offset.y + y))


        pygame.display.update()
