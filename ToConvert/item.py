import pygame

class Item():
    def __init__(self, currentPoint):
        self.vel = 100
        self.currentPoint = currentPoint
        self.currentPoint.occupied = True
        self.pos = pygame.Vector2(currentPoint.pos.x, currentPoint.pos.y)
        self.stepForNextPoint = pygame.Vector2(0, 0)
    
    def moveForwards(self, DT):
        # returns if the item is at the end of the path
        if self.currentPoint == None:
            return
        # calculates the direction vector to get to the next point
        point = self.currentPoint.pos
        direction = point - self.pos

        # checks to see that the is not touching the point
        if direction.magnitude() > 0:
            # calculates the angle from the item to the point before and after motion
            angle1 = direction.angle_to(point) # angle before
            tempPos = self.pos + direction.normalize() * self.vel * DT # positon after movement
            tempDirection = point - tempPos # distance after
            angle2 = tempDirection.angle_to(point) # angle after

            # checks that the angle is not changing too much
            if abs(180 - abs(angle1 - angle2)) > 10:
                self.pos = tempPos # sets the position to the new position

            # the angle changed a lot and means the item overshot the point
            else:
                self.nextPoint() # sets next point to correct for overshoot caused by the item moving too fast
                
        # calls nextPoint as the item is at the point
        else:
            self.nextPoint()

    # sets the items next point to the next point in the path
    def nextPoint(self):
        # snaps the item to the location of the point to account for rounding errors
        point = self.currentPoint.pos
        self.pos = pygame.Vector2(point.x, point.y)

        # checks the item is not at the end of the path
        if self.currentPoint.next != None:
            # checks the next point is not occupied
            if self.currentPoint.next.occupied:
                return
            # sets the next point to the next point in the path and changes the occupied state of the current point
            self.currentPoint.occupied = False
            self.currentPoint = self.currentPoint.next
            self.currentPoint.occupied = True
        # else:
        #     if self.path.occupied[0]:
        #         return
        #     self.path.occupied[self.pathIndex] = False
        #     self.pathIndex = 0
        #     self.path.occupied[self.pathIndex] = True


    # draws the item
    def show(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 5)