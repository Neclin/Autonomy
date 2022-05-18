import pygame

from settings import cellSize

class Conveyor():
    def __init__(self, x, y, type, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.spriteX = 0
        if type == 0:
            self.spriteSheet = pygame.image.load("assets/light/conveyor.png")
        elif type == 1:
            self.spriteSheet = pygame.image.load("assets/light/conveyorL.png")
        self.sprite = self.spriteSheet.subsurface(0, 0, cellSize, cellSize)
        self.sprite = pygame.transform.rotate(self.sprite, rotation)

    def show(self, offset, window):
        window.blit(self.sprite, (offset.x + self.x * cellSize, offset.y + self.y * cellSize))
        self.spriteX += 1
        self.spriteX %= 8
        self.sprite = self.spriteSheet.subsurface(self.spriteX * cellSize, 0, cellSize, cellSize)
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation)