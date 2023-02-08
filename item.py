from hashlib import new
from textwrap import indent
import pygame

from settings import cellSize, beltPoints

class Item():
    def __init__(self, pos, index):
        self.pos = pos
        self.belt = None
        self.index = index

        self.type = "iron ore"
    
    
    def moveTowardsPos(self, pos, dt):
        # calculates the direction vector and returns the new position
        direction = pos - self.pos
        if direction.length() != 0:
            direction = direction.normalize()
            return self.pos + direction * cellSize * self.belt.vel * dt
        else:
            return self.pos


    # draws the item
    def show(self, screen, dt):
        if self.type == "iron ore":
            colour = (170, 85, 70)
        if self.type == "iron bar":
            colour = (190, 194, 203)
            
        pygame.draw.circle(screen, colour, (int(self.pos.x), int(self.pos.y)), 5)

        # TODO fix belts of different speeds overlaping items

        # the item moves from a point to a point on the belt
        if self.index + 1 < len(self.belt.points):
            if self.belt.occupied[self.index+1] == None or self.belt.occupied[self.index+1] == self:
                newPos = self.moveTowardsPos(self.belt.points[self.index+1], dt)
            else:
                self.pos = self.belt.points[self.index] 
                return

            # moves past the point
            if pygame.Vector2.distance_to(self.pos, self.belt.points[self.index+1]) < pygame.Vector2.distance_to(newPos, self.belt.points[self.index+1]):
                self.index += 1  
                self.belt.occupied[self.index] = self


            # moves towards the point
            else:
                self.belt.occupied[self.index] = None
                self.belt.occupied[self.index+1] = self
                self.pos = newPos
        
        # the item moves from a point to a point on the next belt
        else:
            if self.belt.next and (self.belt.next.occupied[0] == None or self.belt.next.occupied[0] == self):
                newPos = self.moveTowardsPos(self.belt.next.points[0], dt)
            else:
                self.pos = self.belt.points[self.index]    
                return

            # moves past the point
            if pygame.Vector2.distance_to(self.pos, self.belt.next.points[0]) < pygame.Vector2.distance_to(newPos, self.belt.next.points[0]):
                self.index = 0                
                self.belt = self.belt.next
    
                

            # moves towards the point
            else:
                self.belt.occupied[self.index] = None
                self.belt.next.occupied[0] = self
                self.pos = newPos
        