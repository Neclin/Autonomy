import pygame

from eventManager import EventManager
from renderer import Renderer
from level import Level
from settings import *

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)

Level.loadLevel("levels/level1.txt")

while EventManager.running:
    EventManager.checkEvents()
    Renderer.update(window)
