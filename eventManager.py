import pygame

from conveyor import Conveyor
from settings import cellSize


class EventManager():
    running = True
    start = True
    rotation = 0

    @classmethod
    def checkEvents(self, conveyors):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    quit()
                
                if event.key == pygame.K_r:
                    self.rotation += 1
                    self.rotation %= 2
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos