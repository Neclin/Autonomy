import pygame

from gameObject import GameObject

from settings import CELLSIZE, POINTSPERBELT
from modules import mapVectorToArrayNoCamera, quadraticBezierCurve

beltSprites = pygame.image.load("assets/belt.png")
straightBeltSprite = pygame.Surface.subsurface(beltSprites, (0,0,CELLSIZE,CELLSIZE))
rightBeltSprite = pygame.Surface.subsurface(beltSprites, (0,CELLSIZE,CELLSIZE,CELLSIZE))
leftBeltSprite = pygame.Surface.subsurface(beltSprites, (0, CELLSIZE*2,CELLSIZE,CELLSIZE))

class Belt(GameObject):
    def __init__(self, x, y, startDirection, endDirection, world):
        super().__init__(x, y, CELLSIZE, CELLSIZE, type="Belt")
        self.startDirection = startDirection
        self.endDirection = endDirection
        self.angle = int(startDirection.angle_to(endDirection))
        if self.angle == -270:
            self.angle = 90
        if self.angle == 270:
            self.angle = -90

        if self.angle == 0:
            self.sprite = straightBeltSprite 
        if self.angle == 90:
            self.sprite = rightBeltSprite
        if self.angle == -90:
            self.sprite = leftBeltSprite

        self.rotation = self.startDirection.angle_to(pygame.Vector2(1, 0))
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation)

        self.next = None
        self.previous = None
        self.getNeighbours(world)

        self.points = [None for i in range(POINTSPERBELT)]
        self.occupied = [None for i in range(POINTSPERBELT)]
        self.generatePoints()


    def show(self, win, camera):
        super().show(win, camera)
        middle = self.worldPosition + pygame.Vector2(CELLSIZE/2, CELLSIZE/2)
        screenMiddle = camera.position + middle - camera.worldPosition
        # pygame.draw.line(win, (0,0,255), screenMiddle, screenMiddle - self.startDirection * CELLSIZE/2, 2)
        # pygame.draw.line(win, (255,0,0), screenMiddle, screenMiddle + self.endDirection * CELLSIZE/2, 2)
        for point in self.points:
            if point:
                screenPoint = camera.position + point - camera.worldPosition
                pygame.draw.circle(win, (255,0,255), screenPoint, 1)

    def getNeighbours(self, world):
        nextPosition = self.worldPosition + self.endDirection * CELLSIZE
        previousPosition = self.worldPosition - self.startDirection * CELLSIZE
        nextArrayPosition = mapVectorToArrayNoCamera(nextPosition)
        previousArrayPosition = mapVectorToArrayNoCamera(previousPosition)

        if world.worldArray[int(nextArrayPosition.y)][int(nextArrayPosition.x)] != 0:
            self.next = world.worldArray[int(nextArrayPosition.y)][int(nextArrayPosition.x)]
        
        if world.worldArray[int(previousArrayPosition.y)][int(previousArrayPosition.x)] != 0:
            self.previous = world.worldArray[int(previousArrayPosition.y)][int(previousArrayPosition.x)]

    def generatePoints(self):
        anchor = self.worldPosition + pygame.Vector2(CELLSIZE//2, CELLSIZE//2)
        start = anchor - self.startDirection * CELLSIZE//2
        end = anchor + self.endDirection * CELLSIZE//2

        for t in range(0, POINTSPERBELT, 1):
            point = quadraticBezierCurve(start, anchor, end, t/POINTSPERBELT)
            self.points[int(t)] = point