import pygame
import time

from eventManager import EventManager
from placer import Placer
from level import Level
from renderer import Renderer
from settings import *

from item import Item
from path import Path, Node

pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)

Level.loadLevel("levels/level1.txt", Placer)

path = Path()

gap = 16

for y in range(100, screenHeight - 100, gap):
    node = Node(pygame.Vector2(100, y))
    path.addNode(node)

for x in range(100, screenWidth - 100, gap):
    node = Node(pygame.Vector2(x, screenHeight - 100))
    path.addNode(node)

for y in range(screenHeight - 100, 100, -gap):
    node = Node(pygame.Vector2(screenHeight - 100, y))
    path.addNode(node)

for x in range(screenWidth - 100, 100, -gap):
    node = Node(pygame.Vector2(x, 100))
    path.addNode(node)

path.tail.next = path.head

Level.paths.append(path)

for i in range(50):
    temp = path.head
    for j in range(i):
        temp = temp.next
    Level.items.append(Item(temp))

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