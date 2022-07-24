import pygame
import math

from level import Level
from belt import Belt
from forge import Forge
from settings import cellSize

class Placer():

    rotation = 0
    startPos = None
    anchor = None
    
    points = []

    belt = Belt(0,0,0,0)
    forge = Forge
    active = belt

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

    @classmethod # returns the array point in that direction
    def getVectorFromAngle(self, angle):
        return pygame.Vector2(-math.floor(math.sin(math.radians(angle-90))), -math.floor(math.cos(math.radians(angle-90))))