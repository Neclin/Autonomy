import pygame

from settings import cellSize

class Conveyor():
    def __init__(self, x, y, type, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.spriteX = 0
        # sets the sprite sheet for the type of conveyor
        if type == 0:
            self.spriteSheet = pygame.image.load("assets/light/conveyor.png")
        elif type == 1:
            self.spriteSheet = pygame.image.load("assets/light/conveyorL.png")
        elif type == 2:
            self.spriteSheet = pygame.image.load("assets/light/conveyorR.png")
        # sets the sprite to the first frame of the animation and resets the rotation
        self.sprite = self.spriteSheet.subsurface(0, 0, cellSize, cellSize)
        self.sprite = pygame.transform.rotate(self.sprite, rotation)
        
        self.path = None
        self.loader = None
        self.ejector = None

    # draws the conveyor to the screen
    def show(self, offset, window):
        window.blit(self.sprite, (offset.x + self.x * cellSize, offset.y + self.y * cellSize))
        # updates the sprite
        self.spriteX += 1 # sets the sprite to the next frame of the animation
        self.spriteX %= 8 # resets when it reaches the end of the animation
        self.sprite = self.spriteSheet.subsurface(self.spriteX * cellSize, 0, cellSize, cellSize)
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation) # rotates the sprite
    
    # gets the ports   
    def getPorts(self, Level):
        # gets the inputs and outputs of the conveyor for each rotation
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

        # gets the conveyor at the position of the loader and ejector
        loader = Level.array[int(loader.y)][int(loader.x)] # input
        ejector = Level.array[int(ejector.y)][int(ejector.x)] # output

        # checks the building at the position of the loader and ejector is a conveyor
        if type(loader) == Conveyor:
            self.loader = loader
        if type(ejector) == Conveyor:
            self.ejector = ejector