import pygame, time

from settings import *

from renderer import Renderer, Camera
from eventManager import EventManager
from world import World
from gameObject import GameObject
from belt import Belt
from item import Item

# # 0 degree belts
# testBelt = Belt(10, 10, pygame.Vector2(1, 0), pygame.Vector2(1, 0))
# testBelt = Belt(10, 10, pygame.Vector2(0, 1), pygame.Vector2(0, 1))
# testBelt = Belt(10, 10, pygame.Vector2(-1, 0), pygame.Vector2(-1, 0))
# testBelt = Belt(10, 10, pygame.Vector2(0, -1), pygame.Vector2(0, -1))

# # 90 degree belts
# testBelt = Belt(10, 10, pygame.Vector2(1, 0), pygame.Vector2(0, 1))
# testBelt = Belt(10, 10, pygame.Vector2(-1, 0), pygame.Vector2(0, -1))
# testBelt = Belt(10, 10, pygame.Vector2(0, 1), pygame.Vector2(-1, 0))
# testBelt = Belt(10, 10, pygame.Vector2(0, -1), pygame.Vector2(1, 0))


# # -90 degree belts
# testBelt = Belt(10, 10, pygame.Vector2(0, 1), pygame.Vector2(1, 0))
# testBelt = Belt(10, 10, pygame.Vector2(0, -1), pygame.Vector2(-1, 0))
# testBelt = Belt(10, 10, pygame.Vector2(1, 0), pygame.Vector2(0, -1))
# testBelt = Belt(10, 10, pygame.Vector2(-1, 0), pygame.Vector2(0, 1))

camera = Camera(0, 0, 800, 800, 350, None)
renderer = Renderer(SCREENWIDTH, SCREENHEIGHT, camera=camera, caption="Autonomy")
eventManager = EventManager()

world = World(WORLDWIDTH, WORLDHEIGHT)
world.load("levels/level1.txt")

while eventManager.running:
    newTime = time.time()
    # run regardless of frame cap
    eventManager.checkEvents(world, camera)
    eventManager.checkMousePress(camera, world)

    # runs only when the screen should update
    if newTime - eventManager.lastFrameTime >= 1/FPS:
        eventManager.deltaTime = newTime - eventManager.lastFrameTime
        eventManager.lastFrameTime = newTime

        eventManager.checkCameraMovement(camera)

        for gameObject in world.gameObjects:
            gameObject.update(eventManager.deltaTime)
        renderer.updateScreen(world, eventManager)

    # runs when the game needs to increment the animation frame
    if newTime - eventManager.lastAnimationFrameTime >= 1/ANIMATIONFPS:
        renderer.incrementAnimationFrame()
        eventManager.lastAnimationFrameTime = newTime
    
