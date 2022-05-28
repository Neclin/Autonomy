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
        
        self.path = None
        self.loader = None
        self.ejector = None

    def show(self, offset, window):
        window.blit(self.sprite, (offset.x + self.x * cellSize, offset.y + self.y * cellSize))
        self.spriteX += 1
        self.spriteX %= 8
        self.sprite = self.spriteSheet.subsurface(self.spriteX * cellSize, 0, cellSize, cellSize)
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation)
    
    def getPorts(self, Level):
        if self.rotation == 0:
            loader = pygame.Vector2(self.x - 1, self.y)
            ejector = pygame.Vector2(self.x + 1, self.y)
        elif self.rotation == 90:
            loader = pygame.Vector2(self.x, self.y + 1)
            ejector = pygame.Vector2(self.x, self.y - 1)
        elif self.rotation == 180:
            loader = pygame.Vector2(self.x + 1, self.y)
            ejector = pygame.Vector2(self.x - 1, self.y)
        elif self.rotation == 270:
            loader = pygame.Vector2(self.x, self.y - 1)
            ejector = pygame.Vector2(self.x, self.y + 1)
        # input
        loader = Level.array[int(loader.y)][int(loader.x)]
        ejector = Level.array[int(ejector.y)][int(ejector.x)]
        if type(loader) == Conveyor:
            self.loader = loader
        if type(ejector) == Conveyor:
            self.ejector = ejector