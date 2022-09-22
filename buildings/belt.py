import pygame
import math

from settings import cellSize, beltPoints
from managers.level import Level

class Belt():
    def __init__(self):
        self.vel = 0

        self.x = 0
        self.y = 0
        self.pos = None
        self.beltAngle = None

        self.startDirection = None
        self.endDirection = None
        
        self.next = None
        self.prev = None
        self.points = []
        self.occupied = [None for i in range(beltPoints)]

    def quadraticBezier(self, t, p0, p1, p2):
        return pygame.Vector2((1-t)**2 * p0.x + 2 * (1-t) * t * p1.x + t**2 * p2.x, (1-t)**2 * p0.y + 2 * (1-t) * t * p1.y + t**2 * p2.y)

    # calculates the angle of the belt. -90 left 90 right and -180 straight
    def calculateBeltAngle(self):
        self.beltAngle = (self.endDirection.angle_to(self.startDirection)+360)%360-180

    # generates the points for items to stored on the belt
    def genPoints(self):
        # clear the points
        self.points = []
        self.occupied = [None for i in range(beltPoints)]

        if self.startDirection == None or self.endDirection == None:
            return

        # all positions are relative to the belts position
        anchor = pygame.Vector2(cellSize/2, cellSize/2) # sets the anchor to the center of the belt
        start = anchor - self.startDirection * cellSize/2 # sets the start point to the center of the belt minus the start direction
        end = anchor + self.endDirection * cellSize/2 # sets the end point to the center of the belt plus the end direction

        for t in range(1, beltPoints+1):
            t = t/beltPoints
            self.points.append(self.quadraticBezier(t, start, anchor, end))

        # pointY = self.pos.y + cellSize / 2 # calcultes the y coordinate of the middle of the belt
        # pointX = self.pos.x + cellSize / 2 # calculates the x cordinate of the middle of the belt

        # # straight belts
        # if self.beltAngle == -180:

        #     # gets the coordinates of the points
        #     for index in range(beltPoints):
        #         gap = cellSize / beltPoints # distaces between the points
        #         offset = int((gap / 2) + (index * gap)) # calculates the offset of each point
        #         # selects the right axis to place the points
        #         if self.startDirection.y == 0.0: # the belt is placed horizontaly
        #             direction = self.startDirection.x / abs(self.startDirection.x)
        #             point = pygame.Vector2(self.pos.x + offset, pointY)
                
        #         if self.startDirection.x == 0.0: # the belt is placed verticaly
        #             direction = self.startDirection.y / abs(self.startDirection.y)
        #             point = pygame.Vector2(pointX, self.pos.y + offset)

        #         # appends it to the list of points stored in the belt
        #         if direction > 0:
        #             self.points.append(point)
        #         else:
        #             self.points.insert(0, point)

        # # left belts
        # elif self.beltAngle == -90:
        #     # selects the right axis to place the points
        #     if self.startDirection.y == 0.0: # the belt is placed horizontaly
        #         # right
        #         if self.startDirection.x == 1:
        #             start = pygame.Vector2(self.pos.x, pointY)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(pointX, self.pos.y)
        #         # left
        #         elif self.startDirection.x == -1:
        #             start = pygame.Vector2(self.pos.x+cellSize, pointY)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(pointX, self.pos.y+cellSize)
            
        #     if self.startDirection.x == 0.0: # the belt is placed verticaly
        #         # up
        #         if self.startDirection.y == -1:
        #             start = pygame.Vector2(pointX, self.pos.y+cellSize)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(self.pos.x, pointY)
        #         # down
        #         elif self.startDirection.y == 1:
        #             start = pygame.Vector2(pointX, self.pos.y)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(self.pos.x+cellSize, pointY)

        #     for index in range(beltPoints):
        #         point = self.quadraticBezier((index+0.5)/beltPoints, start, anchor, end)
        #         self.points.append(point)
            
        # # right belts
        # elif self.beltAngle == 90:
        #     # selects the right axis to place the points
        #     if self.startDirection.y == 0.0: # the belt is placed horizontaly
        #         # right
        #         if self.startDirection.x == 1:
        #             start = pygame.Vector2(self.pos.x, pointY)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(pointX, self.pos.y+cellSize)
        #         # left
        #         elif self.startDirection.x == -1:
        #             start = pygame.Vector2(self.pos.x+cellSize, pointY)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(pointX, self.pos.y)
            
        #     if self.startDirection.x == 0.0: # the belt is placed verticaly
        #         # up
        #         if self.startDirection.y == -1:
        #             start = pygame.Vector2(pointX, self.pos.y+cellSize)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(self.pos.x+cellSize, pointY)
        #         # down
        #         elif self.startDirection.y == 1:
        #             start = pygame.Vector2(pointX, self.pos.y)
        #             anchor = pygame.Vector2(pointX, pointY)
        #             end = pygame.Vector2(self.pos.x, pointY)
            
        #     for index in range(beltPoints):
        #         point = self.quadraticBezier((index+0.5)/beltPoints, start, anchor, end)
        #         self.points.append(point)


    # draws the belt to the screen
    def show(self, window, animationFrame):
        # updates the sprite
        self.sprite = self.spriteSheet.subsurface(animationFrame * 32, 0, 32, 32)
        self.sprite = pygame.transform.smoothscale(self.sprite, (cellSize, cellSize))
        self.sprite = pygame.transform.rotate(self.sprite, self.startDirection.angle_to((1,0))) # rotates the sprite

        window.blit(self.sprite, self.pos)

    # Debug function to show the points of the belt
    def debug(self, window):
        for index in range(len(self.points)-1):
            currentPoint = self.pos + self.points[index]
            nextPoint = self.pos + self.points[index+1]
            pygame.draw.line(window, (0,0,255), currentPoint, nextPoint, 1)
            pygame.draw.circle(window, (0,255,0), currentPoint, 2)

        lastPoint = self.pos + self.points[-1]
        pygame.draw.circle(window, (0,255,0), lastPoint, 2)
        if self.next and self.next.points:
            nextBeltFirstPoint = self.next.pos + self.next.points[0]
            pygame.draw.line(window, (0,0,255), lastPoint, nextBeltFirstPoint, 1)


    def setNext(self):
        nextX = int(self.x + self.endDirection.x)
        nextY = int(self.y + self.endDirection.y)
        if 0 <= nextX < Level.width and 0 <= nextY < Level.height:
            next = Level.array[nextY][nextX]
            if isinstance(next, Belt):
                if not next.prev:
                    self.next = next
                    next.prev = self
                    next.startDirection = self.endDirection
                    next.update()

        
        prevX = int(self.x - self.startDirection.x)
        prevY = int(self.y - self.startDirection.y)
        if 0 <= prevX < Level.width and 0 <= prevY < Level.height:
            prev = Level.array[prevY][prevX]
            if isinstance(prev, Belt):
                if not prev.next:
                    prev.next = self
                    self.prev = prev
                    prev.endDirection = self.startDirection
                    prev.update()

    def resetNext(self):
        if self.next:
            self.next.prev = None
            self.next = None
        
        if self.prev:
            self.prev.next = None
            self.prev = None

    def changeSprite(self):
        # sets the sprite sheet for the type of belt
        if self.beltAngle == -180:
            self.spriteSheet = pygame.image.load("assets/light/belt.png")
        elif self.beltAngle == -90:
            self.spriteSheet = pygame.image.load("assets/light/beltL.png")
        elif self.beltAngle == 90:
            self.spriteSheet = pygame.image.load("assets/light/beltR.png")

    def update(self):
        self.calculateBeltAngle()
        self.genPoints()
        self.changeSprite()
        self.setNext()

    # places the belt
    def place(self, x, y, startDirection, endDirection, vel):
        x, y = int(x), int(y)

        # places the belt if its empty
        building = Level.array[y][x]
        if isinstance(building, Belt):
            building.remove()
        if building == None:
            belt = Belt()
            # sudo constructor
            belt.x = x
            belt.y = y
            belt.pos = pygame.Vector2(Level.offset.x + x * cellSize, Level.offset.y + y * cellSize)
            belt.vel = vel
            belt.startDirection = startDirection
            belt.endDirection = endDirection
            belt.update()
            Level.array[y][x] = belt
            Level.belts.append(belt)

            # belt.setNext()
            return belt

    
    def rotate(self, rotation):
        self.resetNext()
        self.rotation = rotation
        self.directionVector = pygame.Vector2(-math.floor(math.sin(math.radians(rotation-90))), -math.floor(math.cos(math.radians(rotation-90))))
        self.setNext()
        self.genPoints()

    def remove(self):
        self.resetNext()

        for item in self.occupied:
            if item:
                Level.items.remove(item)
                del(item)

        Level.array[self.y][self.x] = None
        Level.belts.remove(self)
        del(self)
