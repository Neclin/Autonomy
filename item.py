import pygame

from gameObject import GameObject
from settings import POINTSPERBELT

class Item(GameObject):
    def __init__(self, x, y, width, height, ):
        super().__init__(x, y, width, height, colour=(33,131,128), type="Item")

        self.layer = 2

        self.belt = None
        self.beltIndex = 0

        self.currentPoint = None
        self.nextPoint = None

        self.distanceToMove = 0

        self.overflowMovement = 0

        self.speed = 100

    def update(self, deltaTime):
        if self.belt:
            self.nextPoint = self.belt.points[self.beltIndex] 
            self.moveTowardsNextPoint(deltaTime)

    def moveTowardsNextPoint(self, deltaTime):
        if self.nextPoint == None:
            self.belt.occupied[self.beltIndex] = self
            self.overflowMovement = 0
            return
        
        self.distanceToMove = self.getDistanceToPoint(self.nextPoint)
        distanceCanMove = self.speed * deltaTime + self.overflowMovement
        self.overflowMovement = 0

        if distanceCanMove < self.distanceToMove:
            if (self.belt.occupied[self.beltIndex] == None or self.belt.occupied[self.beltIndex] == self):
                self.belt.occupied[self.beltIndex] = self
                self.worldPosition += self.getDirectionToPoint(self.nextPoint) * distanceCanMove

        else:
            self.belt.occupied[self.beltIndex] = None
            self.worldPosition = pygame.Vector2(self.nextPoint.x, self.nextPoint.y)
            self.overflowMovement = distanceCanMove - self.distanceToMove
            self.iterateBeltIndex()
            self.belt.occupied[self.beltIndex] = self


    def getDistanceToPoint(self, point):
        return pygame.Vector2(self.worldPosition.x - point.x, self.worldPosition.y - point.y).length()

    def getDirectionToPoint(self, point):
        return pygame.Vector2(point.x - self.worldPosition.x, point.y - self.worldPosition.y).normalize()
        

    def iterateBeltIndex(self):
        self.beltIndex += 1
        if self.beltIndex == POINTSPERBELT:
            if self.belt.next and self.belt.next.occupied[0] == None:
                self.beltIndex = 0
                self.belt = self.belt.next
            else:
                self.beltIndex -= 1
                self.overflowMovement = 0
        if self.belt.occupied[self.beltIndex] != None:
            self.beltIndex -= 1
            self.overflowMovement = 0

    def show(self, renderer, camera):
        super().show(renderer, camera)
