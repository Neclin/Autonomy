from tkinter import Place
from tracemalloc import start
import pygame

from eventManager import EventManager
from placer import Placer
from level import Level
from settings import *

class Renderer():
    gridCellSprite = pygame.image.load("assets/light/gridCell.png")

    @classmethod

    def update(self, window):
        window.fill((204,204,204))

        self.drawGrid(self, window)

        for conveyor in Level.conveyors:
            conveyor.show(Level.offset, window)

        if Placer.mouseDown:
            startPos, endPos = Placer.conveyorLine(Placer)
            pygame.draw.line(window, (0,255,0), startPos, Placer.anchor)
            pygame.draw.line(window, (0,255,0), Placer.anchor, endPos)

        pygame.display.update()
    
    def drawGrid(self, window):
        # draw the grid
        for y in range(0, Level.height):
            y = y * cellSize
            for x in range(0, Level.width):
                x = x * cellSize
                window.blit(self.gridCellSprite, (Level.offset.x + x, Level.offset.y + y))