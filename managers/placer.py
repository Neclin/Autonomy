import pygame
import math

from managers.level import Level
from buildings.belt import Belt
from buildings.forge import Forge
from settings import cellSize

class Placer():
    
    mouseDirection = pygame.Vector2(1,0)

    rotation = 0
    startPos = None
    anchor = None
    
    points = []

    belt = Belt()
    forge = Forge()
    active = belt
    activeBuilding = None

    @classmethod # gets the x and y index in the array for a point
    def getCoord(self, x, y): 
        return pygame.Vector2((x - Level.offset.x) // cellSize, (y - Level.offset.y) // cellSize)
    
    @classmethod # returns the top left position of the x and y index of the array
    def getWindowPoint(self, x, y): 
        return pygame.Vector2(x * cellSize + Level.offset.x, y * cellSize + Level.offset.y)
    
    @classmethod # returns the element at the x and y index of the array from a x and y point
    def getBuildingAtPoint(self, x, y):
        arrayPoint = self.getCoord(x, y)
        return Level.array[arrayPoint.y][arrayPoint.x]
    
    @classmethod # overload for getBuildingAtPoint for a vector point instead of x and y
    def getBuildingAtPos(self, pos):
        arrayPoint = self.getCoord(pos.x, pos.y)
        return Level.array[int(arrayPoint.y)][int(arrayPoint.x)]

    @classmethod # returns the direction vector of an angle
    def getVectorFromAngle(self, angle):
        return pygame.Vector2(round(math.cos(math.radians(angle)),1), -round(math.sin(math.radians(angle)),1))