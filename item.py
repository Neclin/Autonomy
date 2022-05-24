import pygame

class Item():
    def __init__(self, currentPoint):
        self.vel = 2500
        self.currentPoint = currentPoint
        self.currentPoint.occupied = True
        self.pos = pygame.Vector2(currentPoint.pos.x, currentPoint.pos.y)
        self.stepForNextPoint = pygame.Vector2(0, 0)
    
    def moveForwards(self, DT):
        if self.currentPoint == None:
            return
        point = self.currentPoint.pos
        direction = point - self.pos
        if direction.magnitude() > 0:
            if direction.magnitude() > self.pos.distance_to(point - direction.normalize() * self.vel * DT):
                self.pos += direction.normalize() * self.vel * DT
            else:
                self.nextPoint()
        else:
            self.nextPoint()
            
    def nextPoint(self):
        point = self.currentPoint.pos
        self.pos = pygame.Vector2(point.x, point.y)
        if self.currentPoint.next != None:
            if self.currentPoint.next.occupied:
                return
            self.currentPoint.occupied = False
            self.currentPoint = self.currentPoint.next
            self.currentPoint.occupied = True
        # else:
        #     if self.path.occupied[0]:
        #         return
        #     self.path.occupied[self.pathIndex] = False
        #     self.pathIndex = 0
        #     self.path.occupied[self.pathIndex] = True


    def show(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 5)