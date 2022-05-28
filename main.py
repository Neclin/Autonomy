import pygame
import time

from eventManager import EventManager
from placer import Placer
from level import Level
from renderer import Renderer
from settings import *

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)

Level.loadLevel("levels/level1.txt", Placer)




# temp = path.head
# items.append(Item(temp))

oldTime = time.time()
while EventManager.running:
    newTime = time.time()
    deltaTime = newTime - oldTime
    EventManager.checkEvents()
    pos = pygame.mouse.get_pos()
    pos = pygame.Vector2(pos[0], pos[1])
    if EventManager.mouseDown and Renderer.isPointInGrid(pos):
        Placer.conveyor()
    if deltaTime > 1/60:
        oldTime = newTime
        Renderer.update(window, deltaTime)