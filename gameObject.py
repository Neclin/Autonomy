import pygame

class GameObject():
    def __init__(self, x, y, width, height, 
                 colour=(255, 255, 255),
                 spriteList=None, type="GameObject"):

        self.layer = 0

        self.worldPosition = pygame.Vector2(x, y)
        self.width = width
        self.height = height

        self.colour = colour

        self.rect = pygame.Rect(x, y, width, height)

        self.spriteList = spriteList

        self.type = type


    def show(self, renderer, camera):
        if self.spriteList:
            renderer.win.blit(self.spriteList[renderer.animationFrame], camera.position + self.worldPosition - camera.worldPosition)
        else:
            self.rect = pygame.Rect(camera.position.x + self.worldPosition.x - camera.worldPosition.x, 
                                    camera.position.y + self.worldPosition.y - camera.worldPosition.y, 
                                    self.width, self.height)
            pygame.draw.rect(renderer.win, self.colour, self.rect)
    
    def update(self, deltaTime):
        pass