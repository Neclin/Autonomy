import pygame

from conveyor import Conveyor
from settings import screenHeight, screenWidth, cellSize

class Level():

    array = []
    width = 0
    height = 0

    conveyors = []

    @classmethod
    def loadLevel(self, path):
        with open(path) as f:
            dimensions = f.readline().split(',')
            self.width = int(dimensions[0])
            self.height = int(dimensions[1])
            self.offset = pygame.Vector2(screenWidth/2 - (self.width * cellSize)/2, screenHeight/2 - (Level.height * cellSize)/2)

            # create an empty array
            self.array = [[0 for x in range(self.width)] for y in range(self.height)]

            for line in f:
                line = line.split(" ")
                if line[0] == "conveyor":
                    self.conveyors.append(Conveyor(int(line[1]), int(line[2]), int(line[3]), int(line[4])))
                    self.array[int(line[2])][int(line[1])] = 1