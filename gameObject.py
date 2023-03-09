import pygame

class GameObject():
    def __init__(self, x, y, width, height, 
                 colour=(255, 255, 255), borderColour=None,
                 spriteList=None, type="GameObject",
                 text=""):

        self.layer = 0

        self.worldPosition = pygame.Vector2(x, y)
        self.width = width
        self.height = height

        self.colour = colour
        self.borderColour = borderColour

        self.rect = pygame.Rect(x, y, width, height)

        self.spriteList = spriteList

        self.type = type

        self.text = text
        self.font = pygame.font.SysFont("Arial", 32)

        self.screenPinned = False


    def show(self, renderer, camera):
        if self.spriteList:
            renderer.win.blit(self.spriteList[renderer.animationFrame], camera.position + self.worldPosition - camera.worldPosition)
        else:
            if self.screenPinned:
                self.rect = pygame.Rect(camera.position.x + self.worldPosition.x, 
                                        camera.position.y + self.worldPosition.y,
                                        self.width, self.height)
            else:
                self.rect = pygame.Rect(camera.position.x + self.worldPosition.x - camera.worldPosition.x, 
                                        camera.position.y + self.worldPosition.y - camera.worldPosition.y, 
                                        self.width, self.height)
            pygame.draw.rect(renderer.win, self.colour, self.rect)
            if self.borderColour:
                pygame.draw.rect(renderer.win, self.borderColour, self.rect, 2)

            if self.text:
                text = self.font.render(self.text, True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = self.rect.center
                renderer.win.blit(text, textRect)
    
    def update(self, deltaTime):
        pass