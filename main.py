from hashlib import new
import pygame
import time

from eventManager import EventManager
from level import Level
from renderer import Renderer
from settings import *

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)

Level.loadLevel("levels/level1.txt")
Renderer.init()

oldTime = time.time()
while EventManager.running:
    newTime = time.time()
    deltaTime = newTime - oldTime
    EventManager.checkEvents(Level.conveyors)
    if deltaTime > 1/20:
        oldTime = newTime
        Renderer.update(Renderer, window)