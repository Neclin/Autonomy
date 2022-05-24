import pygame
import time

from eventManager import EventManager
from placer import Placer
from level import Level
from renderer import Renderer
from settings import *

from item import Item
from path import Path

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)

Level.loadLevel("levels/level1.txt")

path = Path()

items = []

for i in range(10):
    temp = path.head
    for j in range(i*2):
        temp = temp.next
    items.append(Item(temp))

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
        Renderer.update(window)
        for item in items:
            item.moveForwards(deltaTime)
            item.show(window)
        path.show(window)
        pygame.display.update()