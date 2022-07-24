import pygame

from settings import cellSize, beltPoints
from level import Level

class Belt():
    def __init__(self, x, y, type, rotation):
        self.vel = 0

        self.x = x
        self.y = y
        if Level.offset:
            self.pos = pygame.Vector2(x * cellSize + Level.offset.x, y * cellSize + Level.offset.y)
        self.type = type
        self.rotation = rotation
        
        self.directionVector = None
        self.next = None
        self.points = []
        self.occupied = [None for i in range(beltPoints)]

    def quadraticBezier(self, t, p0, p1, p2):
        return pygame.Vector2((1-t)**2 * p0.x + 2 * (1-t) * t * p1.x + t**2 * p2.x, (1-t)**2 * p0.y + 2 * (1-t) * t * p1.y + t**2 * p2.y)

    # generates the points for items to stored on the belt
    def genPoints(self, numPoints):
        # clear the points
        self.points = []
        self.occupied = [None for i in range(beltPoints)]

        if self.directionVector == None:
            return

        pointY = self.pos.y + cellSize / 2 # calcultes the y coordinate of the middle of the belt
        pointX = self.pos.x + cellSize / 2 # calculates the x cordinate of the middle of the belt

        # straight belts
        if self.type == 0:

            # gets the coordinates of the points
            for index in range(numPoints):
                gap = cellSize / numPoints # distaces between the points
                offset = int((gap / 2) + (index * gap)) # calculates the offset of each point
                # selects the right axis to place the points
                if self.directionVector.y == 0.0: # the belt is placed horizontaly
                    direction = self.directionVector.x / abs(self.directionVector.x)
                    point = pygame.Vector2(self.pos.x + offset, pointY)
                
                if self.directionVector.x == 0.0: # the belt is placed verticaly
                    direction = self.directionVector.y / abs(self.directionVector.y)
                    point = pygame.Vector2(pointX, self.pos.y + offset)

                # appends it to the list of points stored in the belt
                if direction > 0:
                    self.points.append(point)
                else:
                    self.points.insert(0, point)

        # left belts
        elif self.type == 1:
            # selects the right axis to place the points
            if self.directionVector.y == 0.0: # the belt is placed horizontaly
                # right
                if self.directionVector.x == 1:
                    start = pygame.Vector2(self.pos.x, pointY)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(pointX, self.pos.y)
                # left
                elif self.directionVector.x == -1:
                    start = pygame.Vector2(self.pos.x+cellSize, pointY)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(pointX, self.pos.y+cellSize)
            
            if self.directionVector.x == 0.0: # the belt is placed verticaly
                # up
                if self.directionVector.y == -1:
                    start = pygame.Vector2(pointX, self.pos.y+cellSize)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(self.pos.x, pointY)
                # down
                elif self.directionVector.y == 1:
                    start = pygame.Vector2(pointX, self.pos.y)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(self.pos.x+cellSize, pointY)

            for index in range(numPoints):
                point = self.quadraticBezier((index+0.5)/numPoints, start, anchor, end)
                self.points.append(point)
            
        # right belts
        elif self.type == 2:
            # selects the right axis to place the points
            if self.directionVector.y == 0.0: # the belt is placed horizontaly
                # right
                if self.directionVector.x == 1:
                    start = pygame.Vector2(self.pos.x, pointY)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(pointX, self.pos.y+cellSize)
                # left
                elif self.directionVector.x == -1:
                    start = pygame.Vector2(self.pos.x+cellSize, pointY)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(pointX, self.pos.y)
            
            if self.directionVector.x == 0.0: # the belt is placed verticaly
                # up
                if self.directionVector.y == -1:
                    start = pygame.Vector2(pointX, self.pos.y+cellSize)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(self.pos.x+cellSize, pointY)
                # down
                elif self.directionVector.y == 1:
                    start = pygame.Vector2(pointX, self.pos.y)
                    anchor = pygame.Vector2(pointX, pointY)
                    end = pygame.Vector2(self.pos.x, pointY)
            
            for index in range(numPoints):
                point = self.quadraticBezier((index+0.5)/numPoints, start, anchor, end)
                self.points.append(point)


    # draws the belt to the screen
    def show(self, offset, window, animationFrame):
        # sets the sprite sheet for the type of belt
        if self.type == 0:
            self.spriteSheet = pygame.image.load("assets/light/belt.png")
        elif self.type == 1:
            self.spriteSheet = pygame.image.load("assets/light/beltL.png")
        elif self.type == 2:
            self.spriteSheet = pygame.image.load("assets/light/beltR.png")

        # updates the sprite
        self.sprite = self.spriteSheet.subsurface(animationFrame * 32, 0, 32, 32)
        self.sprite = pygame.transform.smoothscale(self.sprite, (cellSize, cellSize))
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation) # rotates the sprite

        window.blit(self.sprite, (offset.x + self.x * cellSize, offset.y + self.y * cellSize))

        # Debug function to show the points of the belt
        #__________________________________________________________________________________________________________
        for index in range(len(self.points)-1):
            pygame.draw.line(window, (0,0,255), self.points[index], self.points[index+1])
            pygame.draw.circle(window, (0,255,0), self.points[index], 2)

        pygame.draw.circle(window, (0,255,0), self.points[-1], 2)
        if self.next and self.next.points:
            pygame.draw.line(window, (0,0,255), self.points[-1], self.next.points[0])

    # places the belt
    def place(self, x, y, type, rotation, directionVector, vel):
        x, y = int(x), int(y)

        # places the belt if its empty
        building = Level.array[y][x]
        if (building == None):
            belt = Belt(x, y, type, rotation)
            belt.vel = vel
            belt.directionVector = directionVector
            belt.genPoints(beltPoints) # generates the points for the belt
            Level.array[y][x] = belt
            Level.belts.append(belt)

            # straight belts
            if type == 0:
                nextX = int(x + directionVector.x)
                nextY = int(y + directionVector.y)
                next = None
                if 0 <= nextX < Level.width and 0 <= nextY < Level.height:
                    next = Level.array[nextY][nextX]
                if (isinstance(next,Belt)) and next.directionVector == directionVector:
                    belt.next = next

                prevX = int(x - directionVector.x)
                prevY = int(y - directionVector.y)
                prev = None
                if 0 <= prevX < Level.width and 0 <= prevY < Level.height:
                    prev = Level.array[prevY][prevX]#

                # both belts are straight
                if (isinstance(prev,Belt)) and prev.directionVector == directionVector:
                    prev.next = belt
                # belt needs to curve
                elif (isinstance(prev,Belt)) and prev.rotation == (belt.rotation+360-90)%360: # left
                    prev.type = 1
                    prev.genPoints(beltPoints)
                    prev.next = belt

                elif (isinstance(prev,Belt)) and prev.rotation == (belt.rotation+360+90)%360: # right
                    prev.type = 2
                    prev.genPoints(beltPoints)
                    prev.next = belt

        
        # overwrites the current belt
        elif (isinstance(building, Belt) and building.rotation != rotation):
            building.rotate(rotation)
    
    def rotate(self, rotation):
        belt = Belt(self.x, self.y, self.type, rotation)
        self.remove()
        belt.rotation = rotation

    def remove(self):
        prevX = int(self.x - self.directionVector.x)
        prevY = int(self.y - self.directionVector.y)
        prev = None
        if 0 <= prevX < Level.width and 0 <= prevY < Level.height:
            prev = Level.array[prevY][prevX]
        if (isinstance(prev,Belt)):
                prev.next = None

        for item in self.occupied:
            if item:
                Level.items.remove(item)
                del(item)

        Level.array[self.y][self.x] = None
        Level.belts.remove(self)
        del(self)
            