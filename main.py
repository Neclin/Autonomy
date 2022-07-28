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

animationFrames = {
    "belt": 0
}

oldTime = time.time()
while EventManager.running:
    newTime = time.time()
    deltaTime = newTime - oldTime
    EventManager.checkEvents()

    if deltaTime > 1/60:
        oldTime = newTime
        animationFrames["belt"] += 1
        animationFrames["belt"] %= 8
        Renderer.update(window, deltaTime, animationFrames)