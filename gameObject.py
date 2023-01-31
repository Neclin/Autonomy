import pygame

class GameObject():
    def __init__(self, x, y, width, height, 
                 colour=(255, 255, 255),
                 sprite=None, type="GameObject"):

        self.worldPosition = pygame.Vector2(x, y)
        self.width = width
        self.height = height

        self.colour = colour

        self.rect = pygame.Rect(x, y, width, height)

        self.sprite = sprite

        self.type = type


    def show(self, win, camera):

        if self.sprite:
            win.blit(self.sprite, camera.position + self.worldPosition - camera.worldPosition)
        else:
            # self.border = pygame.Rect(camera.position.x + self.worldPosition.x - camera.worldPosition.x - 1,
            #                         camera.position.y + self.worldPosition.y - camera.worldPosition.y - 1,
            #                         self.width + 2, self.height + 2)
            # pygame.draw.rect(win, (0, 0, 0), self.border, 1)

            self.rect = pygame.Rect(camera.position.x + self.worldPosition.x - camera.worldPosition.x, 
                                    camera.position.y + self.worldPosition.y - camera.worldPosition.y, 
                                    self.width, self.height)
            pygame.draw.rect(win, self.colour, self.rect)
    