import pygame

from gameObject import GameObject

from settings import CELLSIZE

class Belt(GameObject):
    def __init__(self, x, y, startDirection, endDirection):
        super().__init__(x, y, CELLSIZE, CELLSIZE, type="Belt")
        self.startDirection = startDirection
        self.endDirection = endDirection
        self.angle = int(startDirection.angle_to(pygame.Vector2(endDirection.x, -endDirection.y)))
        if self.angle == -270:
            self.angle = 90
        if self.angle == 270:
            self.angle = -90


    def show(self, win, camera):
        super().show(win, camera)
        middle = self.worldPosition + pygame.Vector2(CELLSIZE/2, CELLSIZE/2)
        screenMiddle = camera.position + middle - camera.worldPosition
        pygame.draw.line(win, (0,0,255), screenMiddle, screenMiddle + self.startDirection * CELLSIZE/2, 2)
        pygame.draw.line(win, (255,0,0), screenMiddle, screenMiddle + self.endDirection * CELLSIZE/2, 2)
    