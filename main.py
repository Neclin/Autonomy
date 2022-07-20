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
    mousePos = pygame.mouse.get_pos()
    mousePos = pygame.Vector2(mousePos[0], mousePos[1])
    arrayPos = Placer.getCoord(mousePos.x, mousePos.y)

    if EventManager.leftMouseDown and Renderer.isPointInGrid(mousePos):
        Placer.belt.place(arrayPos.x, arrayPos.y, 0, Placer.rotation, Placer.getVectorFromAngle(Placer.rotation))
        
    if EventManager.rightMouseDown and Renderer.isPointInGrid(mousePos):
        building = Level.array[int(arrayPos.y)][int(arrayPos.x)]
        if building != None:
            building.remove()

    if deltaTime > 1/60:
        oldTime = newTime
        animationFrames["belt"] += 1
        animationFrames["belt"] %= 8
        Renderer.update(window, deltaTime, animationFrames)