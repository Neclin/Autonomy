import pygame, time

from gameObject import GameObject

from settings import CELLSIZE, POINTSPERBELT
from modules import mapVectorToArrayNoCamera, quadraticBezierCurve

spriteSheet = pygame.image.load("assets/sprites.png")
straightBeltSpriteSheet = pygame.Surface.subsurface(spriteSheet, (0,0,32*8,32))
rightBeltSpriteSheet = pygame.Surface.subsurface(spriteSheet, (0,32,32*8,32))
leftBeltSpriteSheet = pygame.Surface.subsurface(spriteSheet, (0, 32*2,32*8,32))

straightBeltSprites0 = [pygame.Surface.subsurface(straightBeltSpriteSheet, (i*32,0,32,32)) for i in range(8)]
straightBeltSprites90 = [pygame.transform.rotate(sprite, 90) for sprite in straightBeltSprites0]
straightBeltSprites180 = [pygame.transform.rotate(sprite, 180) for sprite in straightBeltSprites0]
straightBeltSpritesN90 = [pygame.transform.rotate(sprite, 270) for sprite in straightBeltSprites0]
straightBeltSprites = [straightBeltSprites0, straightBeltSprites90, straightBeltSprites180, straightBeltSpritesN90]

rightBeltSprites0 = [pygame.Surface.subsurface(rightBeltSpriteSheet, (i*32,0,32,32)) for i in range(8)]
rightBeltSprites90 = [pygame.transform.rotate(sprite, 90) for sprite in rightBeltSprites0]
rightBeltSprites180 = [pygame.transform.rotate(sprite, 180) for sprite in rightBeltSprites0]
rightBeltSpritesN90 = [pygame.transform.rotate(sprite, 270) for sprite in rightBeltSprites0]
rightBeltSprites = [rightBeltSprites0, rightBeltSprites90, rightBeltSprites180, rightBeltSpritesN90]

leftBeltSprites0 = [pygame.Surface.subsurface(leftBeltSpriteSheet, (i*32,0,32,32)) for i in range(8)]
leftBeltSprites90 = [pygame.transform.rotate(sprite, 90) for sprite in leftBeltSprites0]
leftBeltSprites180 = [pygame.transform.rotate(sprite, 180) for sprite in leftBeltSprites0]
leftBeltSpritesN90 = [pygame.transform.rotate(sprite, 270) for sprite in leftBeltSprites0]
leftBeltSprites = [leftBeltSprites0, leftBeltSprites90, leftBeltSprites180, leftBeltSpritesN90]

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
            self.spriteList = straightBeltSprites
        if self.angle == 90:
            self.spriteList = rightBeltSprites
        if self.angle == -90:
            self.spriteList = leftBeltSprites

        self.rotation = self.startDirection.angle_to(pygame.Vector2(1, 0))
        if self.rotation == -270:
            self.rotation = 90
        if self.rotation == 270:
            self.rotation = -90
        if self.rotation == -180:
            self.rotation = 180

        if self.spriteList:
            if self.rotation == 0:
                self.spriteList = self.spriteList[0]
            if self.rotation == 90:
                self.spriteList = self.spriteList[1]
            if self.rotation == 180:
                self.spriteList = self.spriteList[2]
            if self.rotation == -90:
                self.spriteList = self.spriteList[3]

        self.next = None
        self.previous = None
        self.getNeighbours(world)

        self.points = [None for i in range(POINTSPERBELT)]
        self.occupied = [None for i in range(POINTSPERBELT)]
        self.generatePoints()


    def show(self, renderer, camera):
        super().show(renderer, camera)
        middle = self.worldPosition + pygame.Vector2(CELLSIZE/2, CELLSIZE/2)
        screenMiddle = camera.position + middle - camera.worldPosition
        # pygame.draw.line(win, (0,0,255), screenMiddle, screenMiddle - self.startDirection * CELLSIZE/2, 2)
        # pygame.draw.line(win, (255,0,0), screenMiddle, screenMiddle + self.endDirection * CELLSIZE/2, 2)
        # for point in self.points:
        #     if point:
        #         screenPoint = camera.position + point - camera.worldPosition
        #         pygame.draw.circle(renderer.win, (255,0,255), screenPoint, 1)

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