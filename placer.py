import pygame

from level import Level
from conveyor import Conveyor
from settings import cellSize

class Placer():

    rotation = 0
    startPos = None
    anchor = None

    @classmethod
    def getCoord(self, x, y):
        return pygame.Vector2((x - Level.offset.x) // cellSize, (y - Level.offset.y) // cellSize)

    @classmethod
    def conveyor(self):
        pos = pygame.mouse.get_pos()
        pos = self.getCoord(pos[0], pos[1])
        if Level.array[int(pos.y)][int(pos.x)] == 0:
            Level.conveyors.append(Conveyor(int(pos.x), int(pos.y), 0, self.rotation))
            Level.array[int(pos.y)][int(pos.x)] = 1