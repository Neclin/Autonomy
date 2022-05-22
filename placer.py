import pygame

from level import Level
from conveyor import Conveyor
from settings import cellSize

class Placer():

    rotation = 0
    mouseDown = False
    startPos = None
    anchor = None

    @classmethod
    def getCoord(self, x, y):
        return pygame.Vector2((x - Level.offset.x) // cellSize, (y - Level.offset.y) // cellSize)

    def conveyorLine(self):
        mousePos = pygame.mouse.get_pos()
        startPos = pygame.Vector2(self.startPos[0] // cellSize * cellSize + cellSize / 2, self.startPos[1] // cellSize * cellSize + cellSize / 2)
        endPos = pygame.Vector2(mousePos[0] // cellSize * cellSize + cellSize / 2, mousePos[1] // cellSize * cellSize + cellSize / 2)
        if Placer.rotation == 90 or Placer.rotation == 270:
            self.anchor = pygame.Vector2(startPos.x, endPos.y)
        else:
            self.anchor = pygame.Vector2(endPos.x, startPos.y)
        return startPos, endPos

    def convayer(self, pos):
        start = self.getCoord(self.startPos[0], self.startPos[1])
        anchor = self.getCoord(self.anchor.x, self.anchor.y)
        end = self.getCoord(pos[0], pos[1])

        # draw the horizontal line
        if start.x != anchor.x: # horizontal first
            step = int((anchor.x - start.x)/abs(anchor.x - start.x))
            for x in range(int(start.x), int(anchor.x), step):
                if Level.array[x][int(start.y)] == 0: # checks the area is not occupied
                    Level.conveyors.append(Conveyor(x, int(anchor.y), 0, (self.rotation % 180) - 90 + 90 * step))
                    Level.array[x][int(start.y)] = 1
        
        if anchor.x != end.x: # horizontal last
            step = int((end.x - anchor.x)/abs(end.x - anchor.x))
            for x in range(int(anchor.x)+step, int(end.x)+step, step):
                if Level.array[x][int(anchor.y)] == 0: # checks the area is not occupied
                    Level.conveyors.append(Conveyor(x, int(end.y), 0, (self.rotation % 180) - 90 * step))
                    Level.array[x][int(anchor.y)] = 1
        
        # draw the vertical line
        if start.y != anchor.y: # vertical first
            step = int((anchor.y - start.y)/abs(anchor.y - start.y))
            for y in range(int(start.y), int(anchor.y), step):
                if Level.array[int(start.x)][y] == 0: # checks the area is not occupied
                    Level.conveyors.append(Conveyor(int(anchor.x), y, 0, (self.rotation % 180) - 90 - 90 * step))
                    Level.array[int(start.x)][y] = 1
        
        if anchor.y != end.y: # vertical last
            step = int((end.y - anchor.y)/abs(end.y - anchor.y))
            for y in range(int(anchor.y)+step, int(end.y)+step, step):
                if Level.array[int(anchor.x)][y] == 0: # checks the area is not occupied
                    Level.conveyors.append(Conveyor(int(end.x), y, 0, (self.rotation % 180) - 90 * step))
                    Level.array[int(anchor.x)][y] = 1