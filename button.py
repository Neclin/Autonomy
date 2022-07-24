import pygame

class Button():
    def __init__(self, pos, text):
        self.width = 100
        self.height = 100
        self.pos = pos

        self.font = pygame.font.SysFont("Arial", 32)
        self.text = self.font.render(text, True, (0,0,0))

    
    def show(self, window):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(window, (180,180,180), rect, width=1)
        window.blit(self.text, rect)

    
    def isPressed(self):
        mousePos = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(mousePos[0], mousePos[1])

        if mousePos.x > self.pos.x and mousePos.x < self.pos.x + self.width and mousePos.y > self.pos.y and mousePos.y < self.pos.y + self.height:
            return True