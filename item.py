import pygame

from settings import cellSize, beltPoints


class Item:
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
        elif self.type == "iron bar":
            colour = (190, 194, 203)
        else:
            colour = (255, 0, 255)

        screenPoint = self.belt.pos + self.pos

        pygame.draw.circle(screen, colour, screenPoint, 5)

        normal = True
        # if the item is on a belt, move it
        if self.index < beltPoints - 1:
            nextPoint = self.belt.points[self.index + 1]
            nextOccupied = self.belt.occupied[self.index + 1]
        else:
            # if the item is at the end of the belt, it will move to the next belt
            if self.belt.next is not None and (
                    self.belt.next.occupied[0] is None or self.belt.next.occupied[0] == self):
                nextPoint = 2 * self.belt.points[-1] - self.belt.next.points[0]
                nextOccupied = self.belt.next.occupied[0]
                normal = False

            # don't move the item
            else:
                return

        oldDirection = (nextPoint - self.pos).normalize()
        newPos = self.moveTowardsPos(nextPoint, dt)
        newDirection = (nextPoint - newPos).normalize()

        # if the directions are the same allow for small errors
        errorSum = abs(newDirection.x - oldDirection.x) + abs(newDirection.y - oldDirection.y)
        if nextOccupied is None or nextOccupied == self:
            if errorSum < 0.01:
                self.pos = newPos
            elif normal:
                self.belt.occupied[self.index] = None
                self.index += 1
                self.belt.occupied[self.index] = self
                self.pos = nextPoint
            else:
                self.belt.occupied[self.index] = None
                self.belt = self.belt.next
                self.index = 0
                self.pos = self.belt.points[1]
                self.belt.occupied[1] = self

        # TODO fix belts of different speeds overlying items

        # # the item moves from a point to a point on the belt
        # if self.index + 1 < len(self.belt.points):
        #     if self.belt.occupied[self.index+1] == None or self.belt.occupied[self.index+1] == self:
        #         newPos = self.moveTowardsPos(self.belt.points[self.index+1], dt)
        #     else:
        #         self.pos = self.belt.points[self.index]
        #         return

        #     # moves past the point
        #     if pygame.Vector2.distance_to(self.pos, self.belt.points[self.index+1]) < pygame.Vector2.distance_to(newPos, self.belt.points[self.index+1]):
        #         self.index += 1
        #         self.belt.occupied[self.index] = self

        #     # moves towards the point
        #     else:
        #         self.belt.occupied[self.index] = None
        #         self.belt.occupied[self.index+1] = self
        #         self.pos = newPos

        # # the item moves from a point to a point on the next belt
        # else:
        #     if self.belt.next and (self.belt.next.occupied[0] == None or self.belt.next.occupied[0] == self):
        #         newPos = self.moveTowardsPos(self.belt.next.points[0], dt)
        #     else:
        #         self.pos = self.belt.points[self.index]
        #         return

        #     # moves past the point
        #     if pygame.Vector2.distance_to(self.pos, self.belt.next.points[0]) < pygame.Vector2.distance_to(newPos, self.belt.next.points[0]):
        #         self.index = 0
        #         self.belt = self.belt.next
        #         self.pos = pygame.Vector2(0, 0)

        #     # moves towards the point
        #     else:
        #         self.belt.occupied[self.index] = None
        #         self.belt.next.occupied[0] = self
        #         self.pos = newPos
