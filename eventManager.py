import pygame

from placer import Placer
from item import Item
from level import Level

class EventManager():
    running = True
    start = True
    mouseDown = False

    @classmethod
    def checkEvents(self):
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
                    Placer.rotation -= 90
                    Placer.rotation %= 360
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouseDown = True
                if event.button == 3:
                    item = Item(Level.paths[len(Level.paths)-1].head)
                    Level.items.append(item)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouseDown = False
